import logging

from api.api_client import fetch_books
from utils.filters import filter_books
from utils.csv_writer import write_books_csv
from utils.config import (
    OPENLIBRARY_SEARCH_URL,
    SEARCH_QUERY,
    FETCH_LIMIT,
    YEAR_CUTOFF,
    OUTPUT_CSV_PATH,
    FIELDS,
    REQUEST_TIMEOUT,
)


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info(f"Fetching {FETCH_LIMIT} books from OpenLibrary...")
    raw_books = fetch_books(OPENLIBRARY_SEARCH_URL, SEARCH_QUERY, FETCH_LIMIT, FIELDS, REQUEST_TIMEOUT)
    logger.info(f"Fetched {len(raw_books)} books.")

    filtered_books = filter_books(raw_books, YEAR_CUTOFF)
    logger.info(f"{len(filtered_books)} books published after {YEAR_CUTOFF}.")

    write_books_csv(filtered_books, OUTPUT_CSV_PATH, FIELDS)


if __name__ == "__main__":
    main()