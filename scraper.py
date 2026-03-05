import typer
import asyncio
from networking import fetch

app = typer.Typer()

@app.command()
def run(url: str = None, keyword: str = None):
    asyncio.run(_run(url, keyword))

async def _run(u: str = None, keyword: str = None):
    result = await fetch.fetch(u)
    print("URL:", result.url)
    print("Domain:", result.subdomain)
    print("Status:", result.status_code)
    print("Content length:", len(result.content))
    print("Content: ", result.content)



if __name__ == "__main__":
    app()