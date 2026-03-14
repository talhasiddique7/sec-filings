import json
import os
from bs4 import BeautifulSoup

def update_variant_navigation():
    base_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings"
    data_path = os.path.join(base_dir, "data.json")
    filings_dir = os.path.join(base_dir, "filings")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    def get_filename(ft):
        overrides = {"3":"3.html", "4":"4.html", "5":"5.html", "Form 15":"15.html", "10-K":"10k.html", "10-Q":"10q.html", "8-K":"8k.html", "SC 13D":"sc13d.html", "DEF 14A":"def14a.html", "424B4":"424b4.html", "S-3":"s3.html", "S-1":"s1.html", "11-K":"11k.html", "NT 10-K":"nt10k.html", "1-A":"1a.html", "F-3":"f3.html", "F-6":"f6.html"}
        if ft in overrides: return overrides[ft]
        return ft.lower().replace('-', '').replace('/', '').replace(' ', '').replace('.', '') + ".html"

    for form in data['forms']:
        if not form.get('is_variant'):
            continue
            
        ft = form['form_type']
        parent_ft = form.get('parent_form')
        
        filename = get_filename(ft)
        parent_filename = get_filename(parent_ft)
        
        filepath = os.path.join(filings_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        # 1. Update Breadcrumb
        breadcrumb = soup.find('div', class_='breadcrumb')
        if breadcrumb:
            # Current breadcrumb: Home / Filings / [This Form]
            # Desired: Home / Filings / [Parent Form] / [This Form]
            spans = breadcrumb.find_all('span', class_='sep')
            if len(spans) >= 2:
                # Find the location of the second sep
                # Home (a) / (span) Filings (a) / (span) [This Form] (span)
                second_sep = spans[1]
                
                # Check if parent link already exists
                if not breadcrumb.find('a', href=parent_filename):
                    parent_link = soup.new_tag('a', href=parent_filename)
                    parent_link.string = parent_ft
                    
                    new_sep = soup.new_tag('span', **{'class': 'sep'})
                    new_sep.string = "/"
                    
                    second_sep.insert_after(parent_link)
                    parent_link.insert_after(new_sep)
                    print(f"Updated breadcrumb for {filename}")

        # 2. Update Footer
        footer_bottom = soup.select_one('.footer-bottom')
        if footer_bottom:
            # Add "Back to [Parent]" before "Back to Home"
            home_link = footer_bottom.find('a', string=re.compile(r'Back to Home', re.I))
            if home_link and not footer_bottom.find('a', href=parent_filename):
                back_link = soup.new_tag('a', href=parent_filename, style="margin-right: 1.5rem; color: var(--accent-blue); font-weight: 500;")
                back_link.string = f"← Back to {parent_ft}"
                home_link.insert_before(back_link)
                print(f"Updated footer for {filename}")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

import re
if __name__ == "__main__":
    update_variant_navigation()
