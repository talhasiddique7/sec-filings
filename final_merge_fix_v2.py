import json
import os
import re
from bs4 import BeautifulSoup

def merge_filings():
    base_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings"
    data_path = os.path.join(base_dir, "data.json")
    filings_dir = os.path.join(base_dir, "filings")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
        
    forms = full_data['forms']
    
    # EXACT MAPPING BASED ON data.json form_type field
    merge_map = {
        "10-K": ["10-KT", "10-K/A"],
        "10-Q": ["10-QT", "10-QT/A"],
        "11-K": ["11-KT"],
        "8-K": ["8-K12B", "8-K12G3", "8-K15D5"],
        "DEF 14A": ["DEFA14A", "DEFC14A", "DEFM14A", "DEFR14A", "DEFS14A", "DEF 14C", "PRE 14A", "PREC14A", "PREM14A", "PREN14A", "PRE 14C"],
        "424B4": ["424B1", "424B2", "424B3", "424B5", "424B7", "FWP"],
        "S-3": ["S-3ASR", "S-3MEF", "S-3D"],
        "4": ["3", "5"], # Insider Trading
        "SC 13D": ["SC 13G"],
        "NT 10-K": ["NT 10-Q", "NT 20-F", "NT 11-K", "NT-NCSR", "NT 10-K/A", "NT 10-Q/A"],
        "Form 15": ["15-12B", "15-12G", "15-15D", "15F-12B", "15F-12G", "Form 25", "25-NSE", "34-12H"],
        "1-A": ["1-A POS", "1-K", "1-SA", "1-Z", "Form C", "C-AR", "C-U"],
        "S-1": ["S-1MEF"],
        "F-3": ["F-3ASR"],
        "F-6": ["F-6 POS"]
    }

    def find_form_info(ft):
        for f in forms:
            if f['form_type'] == ft:
                return f
        return None

    def get_filename(ft):
        overrides = {
            "3": "3.html",
            "4": "4.html",
            "5": "5.html",
            "Form 15": "15.html",
            "10-K": "10k.html",
            "10-Q": "10q.html",
            "8-K": "8k.html",
            "SC 13D": "sc13d.html",
            "DEF 14A": "def14a.html",
            "424B4": "424b4.html",
            "S-3": "s3.html",
            "S-1": "s1.html",
            "11-K": "11k.html",
            "NT 10-K": "nt10k.html",
            "1-A": "1a.html",
            "F-3": "f3.html",
            "F-6": "f6.html"
        }
        if ft in overrides: return overrides[ft]
        return ft.lower().replace('-', '').replace('/', '').replace(' ', '').replace('.', '') + ".html"

    variant_to_parent = {}
    for p, vs in merge_map.items():
        for v in vs: variant_to_parent[v] = p

    # 1. Update HTML files for parents
    for parent_ft, variant_fts in merge_map.items():
        parent_form = find_form_info(parent_ft)
        if not parent_form: continue
        
        variant_forms = [find_form_info(v) for v in variant_fts if find_form_info(v)]
        if not variant_forms: continue
        
        parent_file = get_filename(parent_ft)
        parent_path = os.path.join(filings_dir, parent_file)
        
        if os.path.exists(parent_path):
            with open(parent_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            
            # Remove existing variants section if any
            existing = soup.find('article', id='variants')
            if existing: existing.decompose()
            
            v_section = soup.new_tag('article', **{'class': 'content-section', 'id': 'variants'})
            v_section.append(soup.new_tag('div', **{'class': 'part-header'}, string="TECHNICAL VARIANTS"))
            v_section.append(soup.new_tag('h2', string="Related Forms & Specialized Variants"))
            
            grid = soup.new_tag('div', **{'class': 'item-grid', 'style': 'margin-top: 2rem;'})
            for v in variant_forms:
                card = soup.new_tag('div', **{'class': 'item-card', 'style': 'border-left: 4px solid var(--accent-blue);'})
                card.append(soup.new_tag('span', **{'class': 'item-num', 'style': 'background: var(--bg-hover); color: var(--accent-blue);'}, string=v['form_type']))
                card.append(soup.new_tag('h3', string=v['full_name']))
                card.append(soup.new_tag('p', string=v['what']))
                grid.append(card)
            v_section.append(grid)
            
            sigs = soup.find('article', id='signatures')
            if sigs: sigs.insert_before(v_section)
            else: 
                content = soup.find('div', class_='filing-content')
                if content: content.append(v_section)
            
            # TOC update
            toc = soup.select_one('.filing-toc nav')
            if toc:
                if not toc.find('a', href='#variants'):
                    link = soup.new_tag('a', href='#variants')
                    link.string = "Related Forms"
                    sig_link = toc.find('a', href='#signatures')
                    if sig_link: sig_link.insert_before(link)
                    else: toc.append(link)
                
            with open(parent_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated {parent_file}")
            
            # Delete redundant
            for v_ft in variant_fts:
                v_file = get_filename(v_ft)
                if v_file == parent_file: continue
                v_path = os.path.join(filings_dir, v_file)
                if os.path.exists(v_path):
                    os.remove(v_path)
                    print(f"  Deleted {v_file}")

    # 2. Rebuild data.json
    final_forms = []
    for f in forms:
        if f['form_type'] not in variant_to_parent:
            final_forms.append(f)
            
    full_data['forms'] = final_forms
    full_data['total_forms'] = len(final_forms)
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, indent=2)
    print(f"Data.json updated: {len(final_forms)} forms remaining.")

if __name__ == "__main__":
    merge_filings()
