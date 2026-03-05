import httpx

DEFAULT_TIMEOUT = 10


def create_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        timeout=DEFAULT_TIMEOUT,
        follow_redirects=True,
    )