import os
from bs4 import BeautifulSoup

def deep_clean_read_more():
    filings_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/filings"
    
    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        changed = False
        
        # 1. Remove all read-more buttons everywhere
        btns = soup.find_all('button', class_='read-more-btn')
        for btn in btns:
            btn.decompose()
            changed = True
            
        # 2. Unwrap all truncate-wrapper divs
        wrappers = soup.find_all('div', class_='truncate-wrapper')
        for wrapper in wrappers:
            wrapper.unwrap()
            changed = True
            
        # 3. Clean up p.truncate-text classes
        ps = soup.find_all('p', class_='truncate-text')
        for p in ps:
            p['class'] = [c for c in p['class'] if c != 'truncate-text']
            if not p['class']:
                del p['class']
            changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Deep cleaned Read More in {filename}")

if __name__ == "__main__":
    deep_clean_read_more()
