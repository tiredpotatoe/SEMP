# Book Fetcher

اسکریپتی که از API عمومی OpenLibrary تعداد مشخصی کتاب دریافت می‌کند، آن‌هایی که بعد از یک سال مشخص منتشر شده‌اند را فیلتر می‌کند و نتیجه را در یک فایل CSV ذخیره می‌کند.


## اجرا

**ویندوز**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m main
```

**لینوکس / مک**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m main
```

خروجی در مسیر `output_csv_path` از `config.json` ساخته می‌شود (پیش‌فرض: `output/fetched_books.csv`).

## تنظیمات (config.json)

```json
{
  "openlibrary_search_url": "https://openlibrary.org/search.json",
  "search_query": "book",
  "fields": "*",
  "fetch_limit": 50,
  "request_timeout": 15,
  "year_cutoff": 2000,
  "output_csv_path": "output/fetched_books.csv"
}
```

- `search_query` — عبارت جستجو (`q`). کوئری‌های عمومی مثل `"the"` رد می‌شوند.
- `fields` — `"*"` برای همه‌ی فیلدها، یا لیست کاما-جدا مثل `"title,author_name,isbn"`. فیلدهای معتبر: [مستندات Search API](https://openlibrary.org/dev/docs/api/search).
- `fetch_limit` — تعداد کتاب درخواستی.
- `request_timeout` — ثانیه‌های timeout.
- `year_cutoff` — فقط کتاب‌های بعد از این سال.
- `output_csv_path` — مسیر فایل خروجی.

## ساختار پروژه

```
book-fetcher/
├── api/
│   └── api_client.py      # ارتباط با OpenLibrary API
├── utils/
│   ├── config.py           # خواندن مقادیر از config.json
│   ├── filters.py          # فیلتر کتاب‌ها بر اساس سال انتشار
│   └── csv_writer.py       # نوشتن خروجی در CSV
├── output/
│   └── fetched_books.csv   # خروجی نهایی
├── config.json
├── main.py
├── requirements.txt
└── .gitignore
```

هر فایل یک مسئولیت دارد: `api_client.py` فقط با API صحبت می‌کند، `filters.py` فقط فیلتر می‌کند، `csv_writer.py` فقط می‌نویسد، و `main.py` این سه مرحله را پشت‌سرهم صدا می‌زند:

```
fetch_books()  →  filter_books()  →  write_books_csv()
```

## تصمیمات طراحی

**کوئری جستجو و دیباگ اولیه**
در ابتدا `search_query` مقدار `"the"` بود و درخواست همیشه با خطای ۴۲۲ و صفر کتاب برمی‌گشت. اول تصور شد مشکل از نبود هدر `User-Agent` است، اما اضافه کردنش مشکل را حل نکرد. با چاپ `response.text` مشخص شد OpenLibrary خودش کوئری‌های خیلی عمومی مثل `"the"` را رد می‌کند (`Invalid query`). با تغییر کوئری به `"book"` مشکل برطرف شد.

**ستون‌های داینامیک در CSV**
لیست فیلدها اول به‌صورت مجیک‌نامبر داخل کد بود، بعد به کانفیگ منتقل شد. اما وقتی `fields` روی `*` تنظیم می‌شود، فیلدهای برگشتی از API بین کتاب‌ها یکسان نیستند. راه‌حل: به‌جای لیست ثابت، اجتماع (union) کلیدهای همه‌ی کتاب‌ها گرفته می‌شود:

```python
fieldnames = set()
for book in books:
    fieldnames.update(book.keys())
```

و برای سلول‌هایی که آن فیلد را ندارند، `csv.DictWriter(..., restval="Unknown")` به‌صورت خودکار مقدار `"Unknown"` می‌گذارد — بدون نیاز به چک دستی روی هر فیلد.

**مدیریت خطا**
- `timeout` روی درخواست HTTP تا برنامه برای همیشه منتظر نماند.
- `Timeout` جدا از بقیه‌ی `RequestException`ها گرفته می‌شود تا لاگ دقیق‌تر باشد؛ در شکست، `fetch_books` لیست خالی برمی‌گرداند نه `None`.
- کتاب بدون سال انتشار با `book.get("first_publish_year", 0)` به‌طور طبیعی از فیلتر رد می‌شود، نه کرش می‌کند.
- `csv_writer` قبل از نوشتن چک می‌کند لیست خالی نباشد و پوشه‌ی خروجی را در صورت نبودن می‌سازد.

## لاگ‌گیری

به‌جای `print`، از `logging` استفاده شده تا هر مرحله (تعداد دریافت‌شده، تعداد بعد از فیلتر، مسیر فایل نوشته‌شده) در ترمینال شفاف باشد و مشخص شود کدام مرحله شکست خورده.
