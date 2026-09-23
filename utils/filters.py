def filter_books(books, year_cutoff):
    """
    Filter books by year cutoff.

    Args:
        books: list of book dicts.
        year_cutoff: the year cutoff.

    Returns:
        A list of filtered book dicts.
    """
    filtered_books = []
    for book in books:
        if book.get("first_publish_year", 0) > year_cutoff:
            filtered_books.append(book)
    return filtered_books