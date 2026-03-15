import asyncio

import typer

from discovery.base import find_dirs
from keyword_utils.keyword_scanner import find_keyword
from networking import fetch
from parser.parser import parse_html
from datetime import datetime
from progress_bar.bar import Progress_Bar
from manage_data import queue

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


async def worker(queue, keyword, casesensitive, crawl, bar: Progress_Bar):
    global urlcounter
    while True:
        url = await queue.get()
        try:
            if url is None:
                break

            if url in visited:
                continue

            visited.add(url)
            urlcounter += 1
            bar.advance()

            response = await fetch.fetch(url)
            parsed, discovered_urls = parse_html(response, casesensitive, crawl)
            find_keyword(parsed, keyword, urlcounter)

            for new_url in discovered_urls:
                if new_url not in visited:
                    await queue.put(new_url)
        except Exception as e:
            print(f"Error processing {url}: {e}")
        except asyncio.TimeoutError:
            continue
        finally:
            queue.task_done()

async def scan(start_urls, keyword, casesensitive, crawl, threads):

    for url in start_urls:
        await queue.put(url)

    workers = []

    with Progress_Bar() as bar:
        for i in range(threads):
            task = asyncio.create_task(worker(queue, keyword, casesensitive, crawl, bar))
            workers.append(task)

        await queue.join()

        for i in range(threads):
            await queue.put(None)
        await asyncio.gather(*workers)


@app.command()
def run(url: str = None, keyword: str = None, casesensitive: bool = False, crawl: bool = False, threads: int = 100):
    asyncio.run(_run(url, keyword, casesensitive=casesensitive, crawl=crawl, threads=threads))


async def _run(u: str = None, keyword: str = None, casesensitive: bool = False, crawl: bool = False, threads: int = 100):
    global visited, urlcounter

    print(banner)
    print()
    print("--------------------------------------------------------")
    print(f"Started at: {datetime.now().strftime('%H:%M:%S')}")
    print("--------------------------------------------------------")


    if not casesensitive:
        keyword = keyword.lower()

    visited = set()
    urlcounter = 0

    start_urls = await find_dirs(u)
    await scan(start_urls, keyword, casesensitive, crawl, threads)

    print("--------------------------------------------------------")
    print(f"Scanned {len(visited)} URLs")


if __name__ == "__main__":
    app()
