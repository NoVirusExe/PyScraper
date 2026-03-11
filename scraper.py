import asyncio

import typer

from discovery.base import find_dirs
from keyword_utils.keyword_scanner import find_keyword
from networking import fetch
from parser.parser import parse_html

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

visited = set()
urlcounter = 0


async def worker(queue, keyword, casesensitive, crawl):
    global urlcounter

    while True:
        url = await queue.get()

        if url in visited:
            queue.task_done()
            continue

        visited.add(url)
        urlcounter += 1

        try:
            response = await fetch.fetch(url)
            parsed, discovered_urls = parse_html(response, casesensitive, crawl)
            find_keyword(parsed, keyword, urlcounter)

            for new_url in discovered_urls:
                if new_url not in visited:
                    await queue.put(new_url)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

        queue.task_done()


async def scan(start_urls, keyword, casesensitive, crawl):
    print("--------------------------------------------------------")
    print("Scanning...")

    queue = asyncio.Queue()

    for url in start_urls:
        await queue.put(url)

    workers = []

    for _ in range(100):
        task = asyncio.create_task(worker(queue, keyword, casesensitive, crawl))
        workers.append(task)

    await queue.join()

    for task in workers:
        task.cancel()


@app.command()
def run(url: str = None, keyword: str = None, casesensitive: bool = False, crawl: bool = False):
    asyncio.run(_run(url, keyword, casesensitive=casesensitive, crawl=crawl))


async def _run(u: str = None, keyword: str = None, casesensitive: bool = False, crawl: bool = False):
    global visited, urlcounter

    print(banner)
    print()
    print("--------------------------------------------------------\n")

    if not casesensitive:
        keyword = keyword.lower()

    visited = set()
    urlcounter = 0

    start_urls = await find_dirs(u)
    await scan(start_urls, keyword, casesensitive, crawl)

    print("--------------------------------------------------------")
    print(f"Scanned {len(visited)} URLs")


if __name__ == "__main__":
    app()
