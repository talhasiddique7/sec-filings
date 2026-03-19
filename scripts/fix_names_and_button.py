from bs4 import BeautifulSoup
import os
import re
import json
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


def slugify(text):
    s = text.lower()
    s = s.replace(' ', '')
    s = s.replace('/', '')
    s = s.replace('-', '')
    s = s.replace('.', '')
    return s

def main():
    base_dir = BASE_DIR
    filings_dir = os.path.join(base_dir, "filings")
    data_path = os.path.join(ASSETS_DIR, "data.json")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Map slug to standard form type
    slug_map = {}
    for form in data['forms']:
        ft = form['form_type']
        slug_map[slugify(ft)] = ft
    
    # Add manual handle for H-K if it's meant to be 10-K
    slug_map['10k'] = '10-K'

    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Ensure correct form name in <h1>
        slug = filename.replace('.html', '')
        std_name = slug_map.get(slug)
        
        hero = soup.find('section', class_='filing-hero')
        if hero:
            h1 = hero.find('h1')
            if not h1:
                # Create h1 if missing
                h1 = soup.new_tag('h1')
                hero.insert(1, h1) # after badge
            
            if std_name:
                h1.string = std_name
            elif h1.get_text(strip=True) == "H-K":
                 h1.string = "10-K"

        # 2. Move download button
        # Button is usually in .filing-actions inside hero
        actions = soup.find('div', class_='filing-actions')
        btn = None
        if actions:
            btn = actions.find('a', class_='btn-primary')
            if btn:
                btn_copy = BeautifulSoup(str(btn), 'html.parser').find('a')
                # Add margin for placement
                btn_copy['style'] = "margin-top: 3rem; display: inline-flex;"
                
                # Find the end of content
                content_div = soup.find('div', class_='filing-content')
                if content_div:
                    # Append a wrapper for the button at the bottom of content
                    footer_actions = soup.new_tag('div', **{'class': 'filing-content-footer', 'style': 'margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border-subtle);'})
                    footer_actions.append(btn_copy)
                    content_div.append(footer_actions)
                    
                    # Remove the original actions container from hero
                    actions.decompose()
        
        # 3. Fix breadcrumb name if it was wrong
        breadcrumb = soup.find('div', class_='breadcrumb')
        if breadcrumb:
            spans = breadcrumb.find_all('span')
            if spans:
                last_span = spans[-1]
                if std_name:
                    last_span.string = std_name
                elif last_span.get_text(strip=True) == "H-K":
                    last_span.string = "10-K"

        # Save changes
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
            
    print(f"Updated all HTML files in {filings_dir}")

if __name__ == '__main__':
    main()
