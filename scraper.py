import typer
import asyncio
from tqdm import tqdm
from networking import fetch
from parser.parser import parse_html
from keyword_utils.keyword_scanner import find_keyword
from discovery.base import find_dirs

banner = r"""
 ________  ___    ___      ________  ________  ________  ________  ________  _______   ________     
|\   __  \|\  \  /  /|    |\   ____\|\   ____\|\   __  \|\   __  \|\   __  \|\  ___ \ |\   __  \    
\ \  \|\  \ \  \/  / /    \ \  \___|\ \  \___|\ \  \|\  \ \  \|\  \ \  \|\  \ \   __/|\ \  \|\  \   
 \ \   ____\ \    / /      \ \_____  \ \  \    \ \   _  _\ \   __  \ \   ____\ \  \_|/_\ \   _  _\  
  \ \  \___|\/  /  /        \|____|\  \ \  \____\ \  \\  \\ \  \ \  \ \  \___|\ \  \_|\ \ \  \\  \| 
   \ \__\ __/  / /            ____\_\  \ \_______\ \__\\ _\\ \__\ \__\ \__\    \ \_______\ \__\\ _\ 
    \|__||\___/ /            |\_________\|_______|\|__|\|__|\|__|\|__|\|__|     \|_______|\|__|\|__|
         \|___|/             \|_________|                                                           

Created by NoVirusExe
"""

app = typer.Typer()

@app.command()
def run(url: str = None, keyword: str = None, casesensitive: bool = False):
    asyncio.run(_run(url, keyword, casesensitive=False))

async def _run(u: str = None, keyword: str = None, casesensitive: bool = False):
    print(banner)
    print()
    print("--------------------------------------------------------")
    print()
    if not casesensitive: keyword = keyword.lower()

    urls = await find_dirs(u)

    urlcounter = 0

    for url in urls:
        urlcounter += 1
        response = await fetch.fetch(url)
        find_keyword(parse_html(response), keyword, urlcounter)

    print("--------------------------------------------------------")

if __name__ == "__main__":
    app()