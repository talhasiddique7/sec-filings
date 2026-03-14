import json
import os
from bs4 import BeautifulSoup

def link_variants_to_pages():
    base_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings"
    data_path = os.path.join(base_dir, "data.json")
    filings_dir = os.path.join(base_dir, "filings")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    forms = data['forms']
    
    # Map parents to their variants
    parent_map = {}
    for f in forms:
        if f.get('is_variant'):
            p = f.get('parent_form')
            if p not in parent_map:
                parent_map[p] = []
            parent_map[p].append(f)

    def get_filename(ft):
        overrides = {"3":"3.html", "4":"4.html", "5":"5.html", "Form 15":"15.html", "10-K":"10k.html", "10-Q":"10q.html", "8-K":"8k.html", "SC 13D":"sc13d.html", "DEF 14A":"def14a.html", "424B4":"424b4.html", "S-3":"s3.html", "S-1":"s1.html", "11-K":"11k.html", "NT 10-K":"nt10k.html", "1-A":"1a.html", "F-3":"f3.html", "F-6":"f6.html"}
        if ft in overrides: return overrides[ft]
        return ft.lower().replace('-', '').replace('/', '').replace(' ', '').replace('.', '') + ".html"

    for parent_ft, variant_forms in parent_map.items():
        parent_file = get_filename(parent_ft)
        parent_path = os.path.join(filings_dir, parent_file)
        
        if os.path.exists(parent_path):
            with open(parent_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            
            # Find the variants section
            v_section = soup.find('article', id='variants')
            if not v_section:
                # If not found, we create it (fallback)
                v_section = soup.new_tag('article', **{'class': 'content-section', 'id': 'variants'})
                v_section.append(soup.new_tag('h2', string="Related Forms & Specialized Variants"))
                sigs = soup.find('article', id='signatures')
                if sigs: sigs.insert_before(v_section)
                else: 
                    content = soup.find('div', class_='filing-content')
                    if content: content.append(v_section)
            
            # Find the grid
            grid = v_section.find('div', class_='item-grid')
            if grid: grid.decompose()
            
            grid = soup.new_tag('div', **{'class': 'item-grid', 'style': 'margin-top: 2rem;'})
            for v in variant_forms:
                v_file = get_filename(v['form_type'])
                link_path = v_file # Since we are in filings dir, they are siblings
                
                card = soup.new_tag('div', **{'class': 'item-card', 'style': 'border-left: 4px solid var(--accent-blue); transition: transform 0.2s; cursor: pointer;', 'onclick': f"window.location.href='{link_path}'"})
                
                # Make the badge a link too for accessibility
                a_tag = soup.new_tag('a', href=link_path, style="text-decoration: none; color: inherit; display: block;")
                
                badge = soup.new_tag('span', **{'class': 'item-num', 'style': 'background: var(--bg-hover); color: var(--accent-blue); display: inline-block; margin-bottom: 0.5rem;'})
                badge.string = v['form_type']
                a_tag.append(badge)
                
                h3 = soup.new_tag('h3', style="margin: 0.5rem 0;")
                h3.string = v['full_name']
                a_tag.append(h3)
                
                p = soup.new_tag('p', style="margin-top: 0.5rem;")
                p.string = v['what']
                a_tag.append(p)
                
                # Add an indicator link
                view_more = soup.new_tag('span', style="font-size: 0.85rem; color: var(--accent-blue); font-weight: 600; margin-top: 1rem; display: block;")
                view_more.string = "View Full Guide →"
                a_tag.append(view_more)
                
                card.append(a_tag)
                grid.append(card)
            
            v_section.append(grid)
            
            with open(parent_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated links in {parent_file}")

if __name__ == "__main__":
    link_variants_to_pages()
