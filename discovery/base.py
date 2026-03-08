from discovery.wayback import query_wayback



async def find_dirs(url):
    urls = []
    urls = urls + await query_wayback(url)

    return list(set(urls))
