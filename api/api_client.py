import requests
import logging
from utils.config import OPENLIBRARY_SEARCH_URL, FETCH_LIMIT, SEARCH_QUERY

logger = logging.getLogger(__name__)


def fetch_books(limit):
    """
    Fetches books from the OpenLibrary search endpoint with the given limit.
    Returns the raw results from the API as a dictionary (parsed JSON).
    """
    params = {
        "q": SEARCH_QUERY,
        "limit": limit,
        "fields": "title,author_name,first_publish_year",
    }

    try:
        response = requests.get(
            OPENLIBRARY_SEARCH_URL,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Request to OpenLibrary timed out.")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to OpenLibrary failed: {e}")
        return []

    data = response.json()
    return data.get("docs", [])
# test

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    books = fetch_books(50)
    print(f"Fetched {len(books)} books")
    for b in books[:3]:
        print(b)