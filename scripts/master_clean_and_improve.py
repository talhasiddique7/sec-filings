import os
import json
import re
from bs4 import BeautifulSoup
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


def clean_and_improve_all():
    base_dir = BASE_DIR
    filings_dir = os.path.join(base_dir, "filings")
    data_path = os.path.join(ASSETS_DIR, "data.json")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    form_map = {form['form_type']: form for form in data['forms']}
    
    # Filename slug map
    def slugify(text):
        s = text.lower().replace(' ', '').replace('/', '').replace('-', '').replace('.', '')
        return s
        
    slug_map = {slugify(ft): form for ft, form in form_map.items()}
    # Special overrides for common mismatch slugs
    slug_map['10k'] = form_map.get('10-K')
    slug_map['10q'] = form_map.get('10-Q')
    slug_map['8k'] = form_map.get('8-K')
    slug_map['3'] = form_map.get('3')
    slug_map['4'] = form_map.get('4')
    slug_map['5'] = form_map.get('5')

    def clean_text(text):
        if not text: return ""
        # Garbage chars
        text = text.replace('\u0393\u00c7\u00f4', '—').replace('\u0393\u00c7\u00f6', '—').replace('\u0393\u00c7\u00f8', '—')
        text = text.replace('ΓÇô', '—').replace('ΓÇö', '—')
        text = text.replace('ΓÇô', '—').replace('ΓÇö', '—')
        return text.strip()

    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
        slug = filename.replace('.html', '')
        
        info = slug_map.get(slug)
        if not info:
            # Try to extract from title or H1 if slug fails
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        # 1. Junk Text Removal (Stray text nodes)
        # Check for text nodes directly in main or before hero
        main = soup.find('main')
        if main:
            for node in list(main.children):
                if hasattr(node, 'extract') and not getattr(node, 'name', None):
                    # It's a NavigableString (text node)
                    if node.strip():
                        node.extract()
        
        # 2. Content Sync & Improvement
        ft = info['form_type']
        fn = clean_text(info['full_name'])
        cat = clean_text(info['category'])
        what = clean_text(info['what'])
        why = clean_text(info['why_use_it'])
        when = clean_text(info['when'])
        who = clean_text(info['who'])
        
        # Hero Badge
        badge = soup.find('div', class_='filing-badge')
        if badge: badge.string = cat
        
        # Hero Subtitle
        sub = soup.find('p', class_='filing-subtitle')
        if sub: sub.string = fn
        
        # Filing Summary List
        summary_div = soup.find('div', class_='filing-summary')
        if summary_div:
            items = summary_div.find_all('li')
            for li in items:
                strength = li.find('strong')
                if not strength: continue
                label = strength.get_text().lower()
                if 'what' in label:
                    li.clear(); li.append(strength); li.append(f" {what}")
                elif 'why' in label:
                    li.clear(); li.append(strength); li.append(f" {why}")
                elif 'when' in label:
                    li.clear(); li.append(strength); li.append(f" {when}")
                elif 'who' in label:
                    li.clear(); li.append(strength); li.append(f" {who}")
                    
        # Professional Insight
        insight = soup.find('div', class_='professional-insight')
        if insight:
            p = insight.find('p', class_='insight-body')
            if p: p.string = why
            
        # Understanding section
        u_header = soup.find('h3', string=re.compile(f"Understanding the {ft}", re.I))
        if not u_header:
            u_header = soup.find('h3', string=re.compile("Understanding the", re.I))
            
        if u_header:
            u_header.string = f"Understanding the {ft} Filing"
            p = u_header.find_next_sibling('p')
            if p: p.string = what
            
        # 3. Structural Polish (Fixing nested wrappers)
        wrappers = soup.find_all('div', class_='truncate-wrapper')
        for w in wrappers:
            inner = w.find('div', class_='truncate-wrapper')
            if inner:
                p_text = w.find('p', class_='truncate-text').get_text().strip()
                w.clear()
                np = soup.new_tag('p', **{'class': 'truncate-text'})
                np.string = p_text
                w.append(np)
                nb = soup.new_tag('button', **{'class':'read-more-btn','type':'button','onclick':'toggleReadMore(this)'})
                nb.string = "Read more"
                w.append(nb)

        # 4. Final Meta Clean
        # Remove any generic descriptions that mentions parts of other files (template remnants)
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and "comprehensive report covering business operations" in meta_desc.get('content','').lower():
            meta_desc['content'] = f"Detailed guide and reference for SEC Form {ft} ({fn}). {what}"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    print("Master clean and improvement pass complete.")

if __name__ == "__main__":
    clean_and_improve_all()
