import os
from bs4 import BeautifulSoup
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


def fix_nested_wrappers():
    filings_dir = FILINGS_DIR
    
    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        changed = False
        
        # 1. Fix nested truncate-wrapper
        wrappers = soup.find_all('div', class_='truncate-wrapper')
        for wrapper in wrappers:
            # If this wrapper has another truncate-wrapper inside it, flatten it
            inner = wrapper.find('div', class_='truncate-wrapper')
            if inner:
                # Keep the original p (truncate-text) and one button
                p = wrapper.find('p', class_='truncate-text')
                # If there are multiple p's, we might have a mess. Let's find the deepest one.
                all_ps = wrapper.find_all('p', class_='truncate-text')
                if all_ps:
                    deepest_p = all_ps[-1]
                    p_text = deepest_p.get_text().strip()
                    
                    # Rebuild the wrapper content
                    wrapper.clear()
                    
                    new_p = soup.new_tag('p', **{'class': 'truncate-text'})
                    new_p.string = p_text
                    wrapper.append(new_p)
                    
                    btn = soup.new_tag('button', **{
                        'class': 'read-more-btn',
                        'type': 'button',
                        'onclick': 'toggleReadMore(this)'
                    })
                    btn.string = "Read more"
                    wrapper.append(btn)
                    changed = True

        # 2. Fix multiple buttons outside wrappers (just in case)
        # Actually the above rebuilds the whole wrapper, so it should be fine.

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Fixed nested wrappers in {filename}")

if __name__ == "__main__":
    fix_nested_wrappers()
