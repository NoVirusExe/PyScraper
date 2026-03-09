import lxml
from .manage_urls import scanned, urls
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
from networking.fetch import FetchResult
from urllib.parse import urlparse
from typing import List
from tqdm import tqdm

@dataclass
class ParsedPage:
    url: str
    subdomain: str
    links: List[str]
    text: str
    scripts: List[str]

def parse_html(fetch_result: FetchResult, iscasesensitive: bool = False, crawl: bool = False) -> ParsedPage:
    soup = BeautifulSoup(fetch_result.content, 'lxml')
    for tag in soup(['script', 'style']):
        tag.extract()
    
    text = soup.get_text(separator=" ", strip=True)

    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])

    scripts = []
    for script in soup.find_all('script', src=True):
        scripts.append(script['src'])

    if crawl:
        for url in scripts:
            if url not in urls and url not in scanned:
                urls.append(url)
                print("--------------------------------------------------------")
                print(f"Added Script: {url}")

    if crawl:
        for link in links:
            if link.startswith(fetch_result.url):
                if link not in urls and link not in scanned:
                    urls.append(link)
                    print("--------------------------------------------------------")
                    print(f"Added Link: {link}")


    return ParsedPage(
        subdomain="/" if urlparse(fetch_result.url).path == "" else urlparse(fetch_result.url).path,
        url=fetch_result.url,
        text=text if iscasesensitive else text.lower(),
        links=links if iscasesensitive else [link.lower() for link in links],
        scripts=scripts if iscasesensitive else [script.lower() for script in scripts]
    )