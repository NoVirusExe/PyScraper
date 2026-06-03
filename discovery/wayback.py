import httpx
import asyncio

async def query_wayback(url):
    api_url = f"https://web.archive.org/cdx/search/cdx?url={url}/*&output=json&fl=original&collapse=urlkey"
    print("Querying Wayback machine...")
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.get(api_url)
            if response.status_code == 200:
                data = response.json()

                if len(data) > 1:
                    urls = list({entry[0] for entry in data[1:]})
                    print(f"Found {len(urls)} URLs in Wayback Machine")
                    return urls
            elif response.status_code == 429:
                print("Rate limited by Wayback Machine. Please try again later.")
            elif response.status_code == 504:
                print("Wayback Machine is currently unavailable (504 Gateway Timeout). Please try again later.")
            elif response.status_code == 503:
                print("Wayback Machine is currently unavailable (503 Service Unavailable). Please try again later")
                
        except Exception as e:
            print(f"Error querying Wayback Machine: {e}")
        return []