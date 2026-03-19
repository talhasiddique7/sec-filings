import os
from bs4 import BeautifulSoup
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


def remove_read_more_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    changed = False
    
    # Find all truncate-wrappers
    wrappers = soup.find_all('div', class_='truncate-wrapper')
    for wrapper in wrappers:
        # Extract the button
        btn = wrapper.find('button', class_='read-more-btn')
        if btn:
            btn.extract()
        
        # Get the text paragraph
        text_p = wrapper.find('p', class_='truncate-text')
        if text_p:
            # Replace wrapper with the paragraph
            wrapper.replace_with(text_p)
            changed = True
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True
    return False

def main():
    base_dir = os.getcwd()
    filings_dir = os.path.join(base_dir, 'filings')
    
    count = 0
    
    # Process all filing pages
    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(filings_dir, filename)
        if remove_read_more_from_file(filepath):
            count += 1
    
    print(f"Removed read more from {count} filing files.")

if __name__ == '__main__':
    main()
