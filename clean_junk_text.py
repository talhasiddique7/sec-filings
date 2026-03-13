from bs4 import BeautifulSoup, NavigableString
import os

def clean_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Clean head
    head = soup.find('head')
    if head:
        for content in list(head.contents):
            if isinstance(content, NavigableString):
                text = content.strip()
                if text and ("SEC Filings Guide" in text or "—" in text):
                    content.extract()
    
    # 2. Clean main if there's any stray text
    main = soup.find('main')
    if main:
        for content in list(main.contents):
            if isinstance(content, NavigableString):
                text = content.strip()
                if text and ("SEC Filings Guide" in text or "H-K" in text):
                    content.extract()

    # 3. Clean hero if there's any stray text
    hero = soup.find('section', class_='filing-hero')
    if hero:
        for content in list(hero.contents):
            if isinstance(content, NavigableString):
                text = content.strip()
                if text and ("H-K" in text or "SEC Filings Guide" in text):
                    content.extract()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

def main():
    filings_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/filings"
    for filename in os.listdir(filings_dir):
        if filename.endswith('.html'):
            print(f"Cleaning {filename}...")
            clean_html(os.path.join(filings_dir, filename))

if __name__ == '__main__':
    main()
