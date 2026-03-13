from bs4 import BeautifulSoup, NavigableString
import os
import re

def check_and_clean(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    changed = False

    # 1. Clean Head
    head = soup.find('head')
    if head:
        for content in list(head.contents):
            if isinstance(content, NavigableString):
                text = content.strip()
                if text and len(text) > 1: # Ignore trivial whitespace
                    print(f"[{os.path.basename(filepath)}] Found head junk: {text[:30]}...")
                    content.extract()
                    changed = True

    # 2. Clean Body (stray text nodes at top level)
    body = soup.find('body')
    if body:
        for content in list(body.contents):
            if isinstance(content, NavigableString):
                text = content.strip()
                if text and len(text) > 1:
                    # Ignore common things if any, but usually body should have tags
                    print(f"[{os.path.basename(filepath)}] Found body junk: {text[:30]}...")
                    content.extract()
                    changed = True

    # 3. Specific known junk: "H-K"
    for tag in soup.find_all(string=re.compile(r'H-K|SEC Filings Guide — Understand', re.I)):
        # If it's just a raw text node not in a meaningful tag (like <h1>, <title>, <span>)
        # Actually, let's just look for "H-K" specifically in parent-less nodes if possible
        pass

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        return True
    return False

import re

def main():
    filings_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/filings"
    count = 0
    for filename in os.listdir(filings_dir):
        if filename.endswith('.html'):
            if check_and_clean(os.path.join(filings_dir, filename)):
                count += 1
    print(f"Finished cleaning. Total files updated: {count}")

if __name__ == '__main__':
    main()
