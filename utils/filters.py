from utils.config import YEAR_CUTOFF


def filter_books(books):
    filtered_books = []

    # filter books by year cutoff
    for book in books:
        if book.get("first_publish_year", 0) > YEAR_CUTOFF:
            filtered_books.append(book)

    return filtered_books