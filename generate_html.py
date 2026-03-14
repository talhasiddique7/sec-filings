
import json
import os
import re

def slugify(text):
    # Convert form type to lowercase and remove non-alphanumeric except hyphen
    s = text.lower()
    s = s.replace(' ', '')
    s = s.replace('/', '')
    s = s.replace('-', '')
    s = s.replace('.', '')
    # Handle specific names if needed based on files in filings/
    return s

# Load data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# List of files in filings/ to verify links
filings_files = os.listdir('filings')
filings_map = {f.replace('.html', ''): f for f in filings_files}

def get_link(form_type):
    slug = slugify(form_type)
    if slug in filings_map:
        return f'filings/{filings_map[slug]}'
    
    # Try alternate slug for some cases
    alt_slug = form_type.lower().replace(' ', '').replace('/', '').replace('.', '') # with hyphen
    if alt_slug in filings_map:
        return f'filings/{filings_map[alt_slug]}'
    
    # Just return # if not found
    return "#"

def get_cat_bucket(cat):
    cat = cat.lower()
    if any(k in cat for k in ['annual', 'quarterly', 'current', 'late', 'event']):
        return 'periodic'
    if 'registration' in cat or 'prospectus' in cat:
        return 'registration'
    if any(k in cat for k in ['insider', 'holdings', 'ownership', '13f', '13d', 'rule 144']):
        return 'insider'
    if 'foreign' in cat:
        return 'foreign'
    return 'other'

tbody_html = ""
seen_forms = set()
unique_forms = []

def format_cell(text):
    if not text:
        return ""
    if len(text) > 80:
        return f'<div class="truncate-wrapper"><div class="truncate-text">{text}</div><button type="button" class="read-more-btn" onclick="toggleReadMore(this)">Read more</button></div>'
    return text


for form in data['forms']:
    ft = form['form_type']
    # Skip variants in the main table
    if form.get('is_variant', False):
        continue
        
    if ft not in seen_forms:
        seen_forms.add(ft)
        unique_forms.append(form)

for form in unique_forms:
    ft = form['form_type']
    fn = form['full_name']
    c = form['category']
    w = form['what']
    wn = form['when']
    who = form['who']
    val = form['why_use_it']
    
    link = get_link(ft)
    bucket = get_cat_bucket(c)
    
    search_text = f"{ft} {fn} {c} {w} {wn} {who} {val}".replace('"', '&quot;')
    
    row = f'            <tr data-category="{bucket}" data-search="{search_text}">\n'
    row += f'              <td><a href="{link}">{ft}</a></td>\n'
    row += f'              <td>{fn}</td>\n'
    row += f'              <td>{c}</td>\n'
    row += f'              <td>{format_cell(w)}</td>\n'
    row += f'              <td>{format_cell(who)}</td>\n'
    row += f'              <td>{format_cell(wn)}</td>\n'
    row += f'              <td>{format_cell(val)}</td>\n'
    row += f'            </tr>\n'
    tbody_html += row

with open('generated_rows.html', 'w', encoding='utf-8') as f:
    f.write(tbody_html)

print(f"Generated generated_rows.html (unique forms: {len(unique_forms)})")
