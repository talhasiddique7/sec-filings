
import os
import re
from collections import Counter
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

# Directories
sec_pdfs_dir = SEC_PDFS_DIR
filings_dir = FILINGS_DIR

# 1. Map PDFs
pdf_files = os.listdir(sec_pdfs_dir)
pdf_info = {}
for f in pdf_files:
    # Pattern: 0000_00_description_formTYPE.pdf
    match = re.search(r'^\d+_\d+_(.*?)_form(.*?)\.pdf$', f, re.IGNORECASE)
    if match:
        desc = match.group(1).replace('-', ' ').title()
        ft = match.group(2).upper()
        pdf_info[ft] = {'filename': f, 'desc': desc}
    else:
        # Fallback for different naming
        parts = f.split('_form')
        if len(parts) > 1:
            ft = parts[-1].replace('.pdf', '').upper()
            pdf_info[ft] = {'filename': f, 'desc': ft}

# 2. Check HTML files
html_files = [f for f in os.listdir(filings_dir) if f.endswith('.html')]
issues = []
stats = Counter()

for html_file in html_files:
    stats['total_html'] += 1
    filepath = os.path.join(filings_dir, html_file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # H1 check
    h1_match = re.search(r'<h1>(.*?)</h1>', content)
    h1 = h1_match.group(1).strip() if h1_match else "NONE"
    
    if h1 == "SEC Filing":
        stats['generic_h1'] += 1
        issues.append(f"{html_file}: Generic H1 'SEC Filing'")
    
    # PDF Link Check
    pdf_link_match = re.search(r'href=".*?/sec_pdfs/(.*?)"', content)
    if pdf_link_match:
        linked_pdf = pdf_link_match.group(1)
        if not os.path.exists(os.path.join(sec_pdfs_dir, linked_pdf)):
            stats['broken_pdf_link'] += 1
            issues.append(f"{html_file}: Broken PDF link to '{linked_pdf}'")
    else:
        if 'href="#"' in content:
            stats['placeholder_pdf_link'] += 1
            issues.append(f"{html_file}: Placeholder PDF link (#)")

print(f"Total HTML files: {stats['total_html']}")
print(f"Files with generic H1 ('SEC Filing'): {stats['generic_h1']}")
print(f"Files with broken PDF links: {stats['broken_pdf_link']}")
print(f"Files with placeholder PDF links (#): {stats['placeholder_pdf_link']}")
print("\nTop 10 Issues:")
for issue in issues[:20]:
    print(issue)
