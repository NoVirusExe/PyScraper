import asyncio
from .client import create_client
from dataclasses import dataclass
from typing import Optional

@dataclass
class FetchResult:
    url: str
    subdomain: str
    status_code: int
    content: str
    content_type: Optional[str]

async def fetch(url: str)-> FetchResult:
    client = create_client()
    response = await client.get(url)

    return FetchResult(
        url=url,
        subdomain=response.url.host,
        status_code=response.status_code,
        content=response.text,
        content_type=response.headers.get("Content-Type")
    )