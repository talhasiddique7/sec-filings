import json
import os
import re
from bs4 import BeautifulSoup

def sync_filings():
    base_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings"
    data_path = os.path.join(base_dir, "data.json")
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
        text = text.replace('\u0393\u00c7\u00f4', '—')
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
        
        # 1. Update Hero
        hero = soup.find('section', class_='filing-hero')
        if hero:
            badge = hero.find('div', class_='filing-badge')
            if badge:
                badge.string = cat # Use Category instead of generic "SEC Filing"
            
            h1 = hero.find('h1')
            if h1: h1.string = ft
            
            sub = hero.find('p', class_='filing-subtitle')
            if sub: sub.string = full_name
            
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
                    li.clear()
                    li.append(strength)
                    li.append(" " + what)
                elif 'why:' == label:
                    li.clear()
                    li.append(strength)
                    li.append(" " + why)
                elif 'when:' == label:
                    li.clear()
                    li.append(strength)
                    li.append(" " + when)
                elif 'who:' == label:
                    li.clear()
                    li.append(strength)
                    li.append(" " + who)

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
