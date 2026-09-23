import requests
import logging

logger = logging.getLogger(__name__)


def fetch_books(search_url, query, limit, fields, request_timeout):
    """
    Fetches books from the OpenLibrary search endpoint.

    Args:
        search_url: The OpenLibrary search API base URL.
        query: Search term (e.g. a subject/topic).
        limit: Max number of books to request.
        fields: Comma-separated fields to request from the API.
        request_timeout: Timeout for the API request, in seconds (default: 10).

    Returns:
        A list of raw book dicts from the API's "docs" field.
        Returns an empty list if the request fails.
    """
    params = {
        "q": query,
        "limit": limit,
        "fields": fields,
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