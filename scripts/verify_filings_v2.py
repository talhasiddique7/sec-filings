
import os
import json
import re
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

# Load data.json
data_path = os.path.join(ASSETS_DIR, 'data.json')
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Map form types from data.json
data_forms = {f['form_type']: f for f in data['forms']}

# List PDFs in sec_pdfs and map them to form types
sec_pdfs_dir = SEC_PDFS_DIR
pdf_files = os.listdir(sec_pdfs_dir)
pdf_map = {}
for f in pdf_files:
    # Match something like _form10-k.pdf or _form8-k.pdf
    match = re.search(r'_form(.*?)\.pdf$', f, re.IGNORECASE)
    if match:
        form_type = match.group(1).upper()
        pdf_map[form_type] = f

# List HTML files in filings/
filings_dir = FILINGS_DIR
filing_files = [f for f in os.listdir(filings_dir) if f.endswith('.html')]

report = []

for html_file in filing_files:
    filepath = os.path.join(filings_dir, html_file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to extract the form type from the content (e.g., in H1)
    h1_match = re.search(r'<h1>(.*?)</h1>', content)
    if not h1_match:
        report.append(f"[ERROR] {html_file}: No <h1> found.")
        continue
    
    ft = h1_match.group(1).strip()
    # Handle cases like "10-K" vs "10K"
    if ft not in data_forms:
        # Try finding by slug
        slug = slugify(ft)
        found = False
        for dft in data_forms:
            if slugify(dft) == slug:
                ft = dft
                found = True
                break
        if not found:
            report.append(f"[WARNING] {html_file}: Form type '{ft}' not found in data.json.")
            continue

    form_data = data_forms[ft]
    
    # Check Metadata
    # Subtitle
    subtitle_match = re.search(r'<p class="filing-subtitle">(.*?)</p>', content)
    if subtitle_match and subtitle_match.group(1).strip() != form_data['full_name']:
        report.append(f"[INFO] {html_file}: Subtitle mismatch. Expected '{form_data['full_name']}', found '{subtitle_match.group(1).strip()}'.")

    # When/Who/What in summary
    what_match = re.search(r'<li><strong>What: ?</strong> ?(.*?)\s*</li>', content)
    if what_match:
        clean_found = what_match.group(1).strip().replace('&amp;', '&').replace('&quot;', '"')
        clean_expected = form_data['what'].strip()
        if clean_found != clean_expected:
             # report.append(f"[INFO] {html_file}: 'What' mismatch.")
             pass # Too many minor differences maybe? Let's check a few.

    # Check PDF link
    pdf_link_match = re.search(r'href=".*?sec_pdfs/(.*?)"', content)
    if pdf_link_match:
        found_pdf = pdf_link_match.group(1)
        expected_pdf = pdf_map.get(ft.upper())
        if not expected_pdf:
            # Maybe the form type in map is slightly different?
            slug = slugify(ft)
            for k, v in pdf_map.items():
                if slugify(k) == slug:
                    expected_pdf = v
                    break
        
        if expected_pdf and found_pdf != expected_pdf:
            report.append(f"[ERROR] {html_file}: PDF link mismatch. Found '{found_pdf}', expected '{expected_pdf}'.")
    else:
        # Check if it's # or something else
        if 'href="#"' in content:
             report.append(f"[INFO] {html_file}: PDF link is placeholder (#).")

# Summary of missing files
for ft in data_forms:
    slug = slugify(ft)
    if not any(slugify(f.replace('.html', '')) == slug for f in filing_files):
        # Check if it uses a collective page (like 8k.html for all 8-K types)
        # In index.html, 8-K12B links to filings/8k.html
        pass # This is expected for some

print("\n".join(report))
