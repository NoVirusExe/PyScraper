from parser.parser import ParsedPage

def find_keyword(content: ParsedPage, keyword: str):
    if keyword in content.text or keyword in content.links or keyword in content.scripts:
        print(f"Hit: Keyword found in URL: {content.url}")