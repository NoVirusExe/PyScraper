import httpx

DEFAULT_TIMEOUT = 10

def create_client() -> httpx.AsyncClient:
    limits = httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20
    )

    return httpx.AsyncClient(
        timeout=DEFAULT_TIMEOUT,
        follow_redirects=False,
        limits=limits
    )