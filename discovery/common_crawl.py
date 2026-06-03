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
            elif response.status_code == 429:
                print("Rate limited by Common Crawl. Please try again later.")
            elif response.status_code == 504:
                print("Common Crawl is currently unavailable (504 Gateway Timeout). Please try again later.")
            elif response.status_code == 503:
                print("Common Crawl is currently unavailable (503 Service Unavailable). Please try again later")
                
        except Exception as e:
            print(f"Error querying Common Crawl: {e}")
            return []