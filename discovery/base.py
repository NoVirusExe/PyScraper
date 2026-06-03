from discovery.wayback import query_wayback
from discovery.common_crawl import query_common_crawl

bad_endings = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot', '.otf', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.7z', '.tar', '.gz', '.mp3', '.mp4', '.avi', '.mkv', '.flv', '.mp3', '.mp4', '.avi', '.mkv', '.flv', '.exe', '.dll', '.sys', '.bin', '.iso', '.img', '.dmg','xml,']



async def find_dirs(url):
    urls = []
    w_urls = await query_wayback(url)
    if w_urls:
        urls = urls + w_urls
    print("--------------------------------------------------------")
    c_urls = await query_common_crawl(url)
    if c_urls:
        urls = urls + c_urls
    print("--------------------------------------------------------")
    print("Merging and filtering URLs...")

    for url in urls:
        if url.endswith(tuple(bad_endings)) and '#' not in url:
            urls.remove(url)
        if url.endswith('/'):
            url = url.rstrip('/')
    urls = list(set(urls))
    print(f"Found {len(urls)} URLs in total")

    return urls
