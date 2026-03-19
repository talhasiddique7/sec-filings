
import os
from bs4 import BeautifulSoup
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


def migrate_buttons_to_eye_icon():
    filings_dir = FILINGS_DIR
    
    eye_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="eye-icon"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>"""
    
    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        changed = False
        
        # 1. Find the existing Download button to get the URL
        footer = soup.find('div', class_='filing-content-footer')
        btn = None
        if footer:
            btn = footer.find('a', class_='btn')
        else:
            # Maybe it's just a loose btn-primary at the bottom
            btns = soup.find_all('a', class_='btn-primary')
            if btns:
                btn = btns[-1] # Assume the last one is the download button
        
        if btn and 'href' in btn.attrs:
            pdf_url = btn['href']
            
            # 2. Find the Hero H1
            hero = soup.find('section', class_='filing-hero')
            if hero:
                h1 = hero.find('h1')
                if h1:
                    # Check if already migrated
                    if not hero.find('div', class_='title-action-wrap'):
                        # Create wrapper
                        wrap = soup.new_tag('div', **{'class': 'title-action-wrap'})
                        h1.replace_with(wrap)
                        wrap.append(h1)
                        
                        # Create eye icon link
                        eye_link = soup.new_tag('a', **{
                            'href': pdf_url,
                            'class': 'view-pdf-btn',
                            'title': 'View Original PDF',
                            'target': '_blank'
                        })
                        eye_link.append(BeautifulSoup(eye_svg, 'html.parser'))
                        wrap.append(eye_link)
                        changed = True
            
            # 3. Remove the old footer/button
            if footer:
                footer.decompose()
                changed = True
            elif btn:
                # If it was a loose button, check if it's in a specific wrapper we want to remove
                parent = btn.parent
                btn.decompose()
                if parent and not parent.get_text().strip() and not parent.find_all():
                    parent.decompose()
                changed = True
                    
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Migrated button to eye icon in {filename}")

if __name__ == "__main__":
    migrate_buttons_to_eye_icon()
