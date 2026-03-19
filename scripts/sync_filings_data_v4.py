import json
import os
import re
from bs4 import BeautifulSoup
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


def sync_filings():
    base_dir = BASE_DIR
    data_path = os.path.join(ASSETS_DIR, "data.json")
    filings_dir = os.path.join(base_dir, "filings")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    forms = data['forms']
    
    def get_filename(ft):
        overrides = {"3":"3.html", "4":"4.html", "5":"5.html", "Form 15":"15.html", "10-K":"10k.html", "10-Q":"10q.html", "8-K":"8k.html", "SC 13D":"sc13d.html", "DEF 14A":"def14a.html", "424B4":"424b4.html", "S-3":"s3.html", "S-1":"s1.html", "11-K":"11k.html", "NT 10-K":"nt10k.html", "1-A":"1a.html", "F-3":"f3.html", "F-6":"f6.html"}
        if ft in overrides: return overrides[ft]
        return ft.lower().replace('-', '').replace('/', '').replace(' ', '').replace('.', '') + ".html"

    def clean_text(text):
        if not text: return ""
        # Handle common garbled characters from utf-16 to utf-8 mess
        text = text.replace('\u0393\u00c7\u00f4', '—') # em dash
        text = text.replace('\u0393\u00c7\u00f6', '—') # em dash variant
        text = text.replace('\u0393\u00c7\u00f8', '—') # em dash variant
        text = text.replace('ΓÇô', '—')
        text = text.replace('ΓÇö', '—')
        return text.strip()

    for form in forms:
        ft = form['form_type']
        fname = get_filename(ft)
        fpath = os.path.join(filings_dir, fname)
        
        if not os.path.exists(fpath):
            continue
            
        with open(fpath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        full_name = clean_text(form['full_name'])
        cat = clean_text(form['category'])
        what = clean_text(form['what'])
        when = clean_text(form['when'])
        who = clean_text(form['who'])
        why = clean_text(form['why_use_it'])
        pdf_url = form.get('pdf_url')
        
        # 1. Update Hero
        hero = soup.find('section', class_='filing-hero')
        if hero:
            badge = hero.find('div', class_='filing-badge')
            if badge:
                badge.string = cat
            
            h1 = hero.find('h1')
            if h1:
                h1.string = ft
                
                # Check for eye icon wrap
                wrap = hero.find('div', class_='title-action-wrap')
                if pdf_url:
                    if not wrap:
                        # Create wrapper and move H1 inside
                        wrap = soup.new_tag('div', **{'class': 'title-action-wrap'})
                        h1.replace_with(wrap)
                        wrap.append(h1)
                    
                    # Ensure/Update Eye icon
                    eye_btn = wrap.find('a', class_='view-pdf-btn')
                    if not eye_btn:
                        eye_btn = soup.new_tag('a', **{
                            'href': pdf_url,
                            'class': 'view-pdf-btn',
                            'title': 'View Original PDF',
                            'target': '_blank'
                        })
                        eye_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="eye-icon"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>"""
                        eye_btn.append(BeautifulSoup(eye_svg, 'html.parser'))
                        wrap.append(eye_btn)
                    else:
                        eye_btn['href'] = pdf_url
                elif wrap:
                    # If wrap exists but no PDF URL (unlikely but safe), unwrap
                    wrap.replace_with(h1)
            
            grid = hero.find('div', class_='filing-meta-grid')
            if grid:
                boxes = grid.find_all('div', class_='meta-box')
                for box in boxes:
                    label_el = box.find('span', class_='meta-label')
                    if not label_el: continue
                    label = label_el.get_text().lower()
                    val = box.find('span', class_='meta-value')
                    if not val: continue
                    
                    if 'frequency' in label or 'deadline' in label:
                        val.string = when
                    elif 'who' in label:
                        val.string = who
                    elif 'authority' in label:
                        val.string = "SEC Mandate"

        # 2. Update Filing Summary List
        summary = soup.find('div', class_='filing-summary')
        if summary:
            items = summary.find_all('li')
            for li in items:
                strength = li.find('strong')
                if not strength: continue
                label = strength.get_text().lower().strip()
                
                if 'what:' == label:
                    li.contents = [strength, " " + what]
                elif 'why:' == label:
                    li.contents = [strength, " " + why]
                elif 'when:' == label:
                    li.contents = [strength, " " + when]
                elif 'who:' == label:
                    li.contents = [strength, " " + who]

        # 3. Update Professional Insight
        insight = soup.find('div', class_='professional-insight')
        if insight:
            p_body = insight.find('p', class_='insight-body')
            if p_body:
                p_body.string = why

        # 4. Update Understanding Header
        u_header = soup.find('h3', string=re.compile(r'Understanding the', re.I))
        if u_header:
            u_header.string = f"Understanding the {ft} Filing"
            p_below = u_header.find_next_sibling('p')
            if p_below:
                p_below.string = what

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    print("Sync complete for all HTML files.")

if __name__ == "__main__":
    sync_filings()
