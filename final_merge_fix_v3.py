import json
import os
from bs4 import BeautifulSoup

def final_recheck_and_fix():
    base_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings"
    # Source of truth (older version with all 147 forms)
    source_path = os.path.join(base_dir, "data_backup.json")
    # Current data.json (to be updated to consolidated state)
    data_path = os.path.join(base_dir, "data.json")
    filings_dir = os.path.join(base_dir, "filings")
    
    # Try multiple encodings for the backup file (PowerShell > often uses utf-16)
    source_data = None
    for enc in ['utf-16', 'utf-8', 'ascii']:
        try:
            with open(source_path, 'r', encoding=enc) as f:
                source_data = json.load(f)
            print(f"Loaded source data using {enc} encoding.")
            break
        except Exception:
            continue
            
    if not source_data:
        print("Failed to load source data.")
        return

    forms = source_data['forms']
    
    merge_map = {
        "10-K": ["10-KT", "10-K/A"],
        "10-Q": ["10-QT", "10-QT/A"],
        "11-K": ["11-KT"],
        "8-K": ["8-K12B", "8-K12G3", "8-K15D5"],
        "DEF 14A": ["DEFA14A", "DEFC14A", "DEFM14A", "DEFR14A", "DEFS14A", "DEF 14C", "PRE 14A", "PREC14A", "PREM14A", "PREN14A", "PRE 14C"],
        "424B4": ["424B1", "424B2", "424B3", "424B4/A", "424B5", "424B7", "FWP"],
        "S-3": ["S-3ASR", "S-3MEF", "S-3D"],
        "4": ["3", "5"],
        "SC 13D": ["SC 13G"],
        "NT 10-K": ["NT 10-Q", "NT 20-F", "NT 11-K", "NT-NCSR", "NT 10-K/A", "NT 10-Q/A"],
        "Form 15": ["15-12B", "15-12G", "15-15D", "15F-12B", "15F-12G", "Form 25", "25-NSE", "34-12H"],
        "1-A": ["1-A POS", "1-K", "1-SA", "1-Z", "Form C", "C-AR", "C-U"],
        "S-1": ["S-1MEF"],
        "F-3": ["F-3ASR"],
        "F-6": ["F-6 POS"]
    }

    processed_variants = set()
    for vs in merge_map.values():
        processed_variants.update(vs)

    def find_form(ft):
        for f in forms:
            if f['form_type'] == ft:
                return f
        return None

    def get_filename(ft):
        overrides = {"3":"3.html", "4":"4.html", "5":"5.html", "Form 15":"15.html", "10-K":"10k.html", "10-Q":"10q.html", "8-K":"8k.html", "SC 13D":"sc13d.html", "DEF 14A":"def14a.html", "424B4":"424b4.html", "S-3":"s3.html", "S-1":"s1.html", "11-K":"11k.html", "NT 10-K":"nt10k.html", "1-A":"1a.html", "F-3":"f3.html", "F-6":"f6.html"}
        if ft in overrides: return overrides[ft]
        return ft.lower().replace('-', '').replace('/', '').replace(' ', '').replace('.', '') + ".html"

    # 1. Update HTML Files
    for parent_ft, variant_fts in merge_map.items():
        variant_forms = [find_form(v) for v in variant_fts if find_form(v)]
        if not variant_forms:
            print(f"Warning: No variants found for {parent_ft}")
            continue
            
        parent_file = get_filename(parent_ft)
        parent_path = os.path.join(filings_dir, parent_file)
        
        if os.path.exists(parent_path):
            with open(parent_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
            # Remove existing variants section (even if empty)
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
                # Use a paragraph with wrap
                p = soup.new_tag('p')
                p.string = v['what']
                card.append(p)
                grid.append(card)
            v_section.append(grid)
            
            # Place before signatures
            sigs = soup.find('article', id='signatures')
            if sigs: sigs.insert_before(v_section)
            else:
                content = soup.find('div', class_='filing-content')
                if content: content.append(v_section)
                
            # TOC entry
            toc = soup.select_one('.filing-toc nav')
            if toc and not toc.find('a', href='#variants'):
                link = soup.new_tag('a', href='#variants')
                link.string = "Related Forms"
                sig_link = toc.find('a', href='#signatures')
                if sig_link: sig_link.insert_before(link)
                else: toc.append(link)
                
            with open(parent_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Verified and Repopulated {parent_file} with {len(variant_forms)} variants.")
            
            # Cleanup redundant files
            for v_ft in variant_fts:
                v_file = get_filename(v_ft)
                if v_file == parent_file: continue
                v_path = os.path.join(filings_dir, v_file)
                if os.path.exists(v_path):
                    os.remove(v_path)
                    print(f"  Removed {v_file}")

    # 2. Re-consolidate data.json
    final_forms = [f for f in forms if f['form_type'] not in processed_variants]
    source_data['forms'] = final_forms
    source_data['total_forms'] = len(final_forms)
    
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(source_data, f, indent=2)
    print(f"Synchronized data.json: {len(final_forms)} base forms.")

if __name__ == "__main__":
    final_recheck_and_fix()
