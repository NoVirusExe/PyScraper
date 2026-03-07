import typer
import asyncio
from networking import fetch
from parser.parser import parse_html
from keyword_utils.keyword_scanner import find_keyword

app = typer.Typer()

@app.command()
def run(url: str = None, keyword: str = None):
    asyncio.run(_run(url, keyword))

async def _run(u: str = None, keyword: str = None):
    fetch_result = await fetch.fetch(u)
    parsed_result = parse_html(fetch_result)
    find_keyword(parsed_result, keyword)



if __name__ == "__main__":
    app()