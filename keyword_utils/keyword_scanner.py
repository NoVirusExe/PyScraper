from parser.parser import ParsedPage

def find_keyword(content: ParsedPage, keyword: str):
    if keyword in content.text:
        print("--------------------------------------------------------")
        print(f"Hit: Keyword: \"{keyword}\" found in URL: {content.url}")
        print("Found in: Source")
    elif any(keyword in link for link in content.links):
        print("--------------------------------------------------------")
        print(f"Hit: Keyword: \"{keyword}\" found in URL: {content.url}")
        print("Found in: Links")
    elif any(keyword in script for script in content.scripts):
        print("--------------------------------------------------------")
        print(f"Hit: Keyword: \"{keyword}\" found in URL: {content.url}")
        print("Found in: Scripts")