import requests
import logging

logger = logging.getLogger(__name__)

def fetch_books(search_url, query, limit, request_timeout = 10):
    """
    Fetches books from the OpenLibrary search endpoint.

    Args:
        search_url: the OpenLibrary search API base URL.
        query: search term (e.g. a subject/topic).
        limit: max number of books to request.

    Returns:
        A list of raw book dicts from the API's "docs" field.
        Returns an empty list if the request fails.
    """
    params = {
        "q": query,
        "limit": limit,
        "fields": "title,author_name,first_publish_year",
    }

    try:
        response = requests.get(
            search_url,
            params=params,
            timeout=request_timeout,
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