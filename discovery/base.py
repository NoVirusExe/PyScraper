from discovery.wayback import query_wayback
from discovery.common_crawl import query_common_crawl

bad_endings = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot', '.otf', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.7z', '.tar', '.gz', '.mp3', '.mp4', '.avi', '.mkv', '.flv', '.mp3', '.mp4', '.avi', '.mkv', '.flv', '.exe', '.dll', '.sys', '.bin', '.iso', '.img', '.dmg',]



async def find_dirs(url):
    urls = []
    urls = urls + await query_wayback(url)
    print("--------------------------------------------------------")
    urls = urls + await query_common_crawl(url)
    print("--------------------------------------------------------")
    print("Merging and filtering URLs...")

    for url in urls:
        if url.endswith(tuple(bad_endings)):
            urls.remove(url)
    print(f"Found {len(urls)} URLs in total")

    return list(set(urls))
