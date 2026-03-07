import lxml
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
from networking.fetch import FetchResult
from urllib.parse import urlparse
from typing import List

@dataclass
class ParsedPage:
    url: str
    subdomain: str
    links: List[str]
    text: str
    scripts: List[str]

def parse_html(fetch_result: FetchResult, iscasesensitive: bool = False) -> ParsedPage:
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

    return ParsedPage(
        subdomain="/" if urlparse(fetch_result.url).path == "" else urlparse(fetch_result.url).path,
        url=fetch_result.url,
        text=text if iscasesensitive else text.lower(),
        links=links if iscasesensitive else [link.lower() for link in links],
        scripts=scripts if iscasesensitive else [script.lower() for script in scripts]
    )