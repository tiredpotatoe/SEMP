import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def write_books_csv(books: list[dict], path: Path, fields: str) -> None:
    """
    Write a list of book dicts to a CSV file.

    Args:
        books: list of dicts.
        path: destination file path for the CSV.
        fields: comma separated string of field names to use as CSV headers.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [f.strip() for f in fields.split(",")]

    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for book in books:
            row = {}
            for field in fieldnames:
                    row[field] = book.get(field, "Unknown")
            writer.writerow(row)

    logger.info(f"Wrote {len(books)} books to {path}")