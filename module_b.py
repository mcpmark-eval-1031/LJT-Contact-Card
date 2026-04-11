"""Module B - Network utilities."""

import requests
import time

# TODO(bug): Fix memory leak in connection pool
# TODO(dev): Add connection pooling configuration


def fetch_data(url, timeout=30, max_retries=3, verify_ssl=True):
    """Fetch data from URL with retry logic, configurable timeout, and SSL control.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds (default 30).
        max_retries: Number of retry attempts on transient failures (default 3).
        verify_ssl: Whether to verify the server TLS certificate (default True).

    Returns:
        requests.Response on success.

    Raises:
        requests.exceptions.RequestException: after max_retries exhausted.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout, verify=verify_ssl)
            response.raise_for_status()
            return response
        except (requests.ConnectionError, requests.Timeout):
            if attempt < max_retries - 1:
                backoff = 2 ** attempt  # exponential backoff: 1 s, 2 s, 4 s, …
                time.sleep(backoff)
            else:
                raise


def post_data(url, payload):
    """Post data to URL."""
    # TODO - Implement request signing
    # TODO(dev): Add response compression support
    pass


def batch_request(urls):
    """Fetch multiple URLs in parallel."""
    # TODO(dev): Implement concurrent batch processing
    pass
