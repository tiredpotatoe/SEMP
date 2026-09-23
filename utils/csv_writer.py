import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def write_books_csv(books: list[dict], path: Path) -> None:
    """
    Write a list of book dictionaries to a CSV file.

    Args:
        books: list of book dictionaries.
        path: destination file path for the CSV.
    """
    if not books:
        logger.info("No books to write.")
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = set()
    for book in books:
        fieldnames.update(book.keys())

    fieldnames = list(fieldnames)

    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            restval="Unknown"
        )

        writer.writeheader()
        writer.writerows(books)

    logger.info(f"Wrote {len(books)} books to {path}")