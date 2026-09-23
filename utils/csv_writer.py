import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def write_books_csv(books: list[dict], path: Path) -> None:
    """
    Write a list of book dicts to a CSV file.

    Args:
        books: list of dicts, each with 'title', 'author_name', 'first_publish_year'.
        path: destination file path for the CSV.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["title", "author_name", "first_publish_year"]

    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for book in books:
            writer.writerow({
                "title": book.get("title", "Unknown"),
                "author_name": ", ".join(book.get("author_name", [])) or "Unknown",
                "first_publish_year": book.get("first_publish_year", "Unknown"),
            })

    logger.info(f"Wrote {len(books)} books to {path}")

#test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    fake_books = [
        {"title": "Test Book One", "author_name": ["Author A"], "first_publish_year": 2010},
        {"title": "Test Book Two", "author_name": ["Author B", "Author C"], "first_publish_year": 2021},
        {"title": "No Author Book", "author_name": [], "first_publish_year": 1999},
    ]

    write_books_csv(fake_books, Path("output/test_books.csv"))