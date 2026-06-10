# PyScraper

A fast asynchronous keyword discovery and website reconnaissance tool.

PyScraper discovers URLs from public sources such as the Internet Archive (Wayback Machine) and Common Crawl, fetches pages concurrently, extracts content, and searches for user-defined keywords.

This is my first bigger Project so feel free to report bugs or issues.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/NoVirusExe/PyScraper.git
cd pyscraper
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Basic scan:

```bash
python scraper.py https://example.com api
```

Case-sensitive search:

```bash
python scraper.py https://example.com API --casesensitive
```

Enable crawling:

```bash
python scraper.py https://example.com api --crawl
```

Increase worker count:

```bash
python scraper.py https://example.com api --threads 200
```

---

## Arguments

| Argument | Description |
|-----------|------------|
| `url` | Target website |
| `keyword` | Keyword to search for |
| `--casesensitive` | Enable case-sensitive matching |
| `--crawl` | Follow discovered internal links |
| `--threads` | Number of concurrent workers (default: 100) |

---

## Example Output

```text
Started at: 20:13:44
--------------------------------------------------------
Querying Wayback machine...
--------------------------------------------------------
Querying Common Crawl...
Found 297 URLs in Common Crawl
--------------------------------------------------------
Merging and filtering URLs...
Found 812 URLs in total

Hit URL 24:
Keyword: "api"
Found in: Source
URL: https://example.com/api/docs

--------------------------------------------------------
Scanned 812 URLs
```

---

## Requirements

- Python 3.11+
- httpx
- beautifulsoup4
- lxml
- typer
- rich
- python-dotenv

---

## Disclaimer

This tool is intended for:

- Security research
- Website auditing
- Content discovery
- Educational purposes

Only scan websites you own or have permission to assess.

The author is not responsible for misuse of this software.

---

## License

MIT License
