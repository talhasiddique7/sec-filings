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

def clean_text(text):
    if not text: return ""
    # Standardize common encoding issues
    text = text.replace('\u0393\u00c7\u00f4', '—').replace('\u0393\u00c7\u00f6', '—').replace('\u0393\u00c7\u00f8', '—')
    text = text.replace('ΓÇô', '—').replace('ΓÇö', '—')
    return text.strip()

def main():
    base_dir = BASE_DIR
    filings_dir = os.path.join(base_dir, "filings")
    data_path = os.path.join(ASSETS_DIR, "data.json")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Map slug to (std_form_type, full_name, category)
    info_map = {}
    for form in data['forms']:
        ft = clean_text(form['form_type'])
        fn = clean_text(form['full_name'])
        cat = clean_text(form['category'])
        info_map[slugify(ft)] = (ft, fn, cat)
    
    # Special handle for 10-K
    info_map['10k'] = ('10-K', 'Annual Report', 'Annual Reports')

    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        slug = filename.replace('.html', '')
        info = info_map.get(slug)
        if not info:
            continue
            
        std_ft, std_fn, std_cat = info

        # 1. Fix <title> tag
        title_tag = soup.find('title')
        if title_tag:
            title_tag.string = f"{std_ft} — {std_fn} | SEC Filings Guide"
        else:
            # If missing, add it to head
            head = soup.find('head')
            if head:
                title_tag = soup.new_tag('title')
                title_tag.string = f"{std_ft} — {std_fn} | SEC Filings Guide"
                head.append(title_tag)

        # 2. Fix Hero Section
        hero = soup.find('section', class_='filing-hero')
        if hero:
            # We want to keep the metadata grid, but reorganize the top part
            grid = hero.find('div', class_='filing-meta-grid')
            
            # Clear everything in hero except maybe the grid?
            # Let's be safer: find the old title/subtitle and update them
            # or just rebuild the top part.
            
            # Rebuild hero contents
            hero.clear()
            
            # Map slug to info
            _, _, cat = info
            
            # Badge
            badge = soup.new_tag('div', **{'class': 'filing-badge cyan'})
            badge.string = cat if cat else "SEC Filing"
            hero.append(badge)
            
            # H1
            h1 = soup.new_tag('h1')
            h1.string = std_ft
            hero.append(h1)
            
            # Subtitle
            sub = soup.new_tag('p', **{'class': 'filing-subtitle'})
            sub.string = std_fn
            hero.append(sub)
            
            # Put the grid back
            if grid:
                hero.append(grid)
                
        # 3. Handle Download Button (ensure it is at bottom and NOT in hero)
        # Find all btn-primary links
        all_btns = soup.find_all('a', class_='btn-primary')
        btn_to_move = None
        for b in all_btns:
            if "Download" in b.get_text() or "EDGAR" in b.get_text():
                # Extract the one from hero specifically if it exists
                if b.find_parent('section', class_='filing-hero') or b.find_parent('div', class_='filing-actions'):
                    btn_to_move = b
                    break
                # Or just take the first one if it's not in the footer yet
                if not b.find_parent('div', class_='filing-content-footer'):
                    btn_to_move = b
                    break
        
        if btn_to_move:
            # Ensure footer exists
            footer = soup.find('div', class_='filing-content-footer')
            if not footer:
                content_div = soup.find('div', class_='filing-content')
                if content_div:
                    footer = soup.new_tag('div', **{'class': 'filing-content-footer', 'style': 'margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border-subtle);'})
                    content_div.append(footer)
            
            if footer and not footer.find('a', class_='btn-primary'):
                btn_copy = BeautifulSoup(str(btn_to_move), 'html.parser').find('a')
                btn_copy['style'] = "display: inline-flex;"
                footer.append(btn_copy)
            
            # Remove original if it wasn't already in footer
            if btn_to_move and not btn_to_move.find_parent('div', class_='filing-content-footer'):
                # Also remove the container if it was in .filing-actions
                actions = btn_to_move.find_parent('div', class_='filing-actions')
                if actions:
                    actions.decompose()
                else:
                    btn_to_move.decompose()

        # 4. Fix Breadcrumb Link
        bc = soup.find('div', class_='breadcrumb')
        if bc:
            f_link = bc.find('a', string=re.compile("Filings", re.I))
            if f_link:
                f_link['href'] = "../index.html#search-filings"

        # Save changes
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    print(f"Repolished all HTML files in {filings_dir}")

if __name__ == '__main__':
    main()
