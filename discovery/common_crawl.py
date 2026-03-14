import httpx
import asyncio
import json

async def query_common_crawl(url):
    api_url = f"https://index.commoncrawl.org/CC-MAIN-2026-08-index?url={url}/*&output=json&fl=url&collapse=path"
    print("Querying Common Crawl...")
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.get(api_url)
            if response.status_code == 200:
                urls = []

                for line in response.text.splitlines():
                    if line.strip():
                        entry = json.loads(line)
                        urls.append(entry["url"])
                print(f"Found {len(urls)} URLs in Common Crawl")
                return urls
                
        except Exception as e:
            print(f"Error querying Common Crawl: {e}")
            return []