
import os
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

# Directories
sec_pdfs_dir = SEC_PDFS_DIR
filings_dir = FILINGS_DIR

# 1. Map PDFs
pdf_files = os.listdir(sec_pdfs_dir)
pdf_info = {}
for f in pdf_files:
    # Pattern: ..._form[TYPE].pdf
    # Split by _form and take the last part
    parts = f.split('_form')
    if len(parts) > 1:
        form_type_raw = parts[-1].replace('.pdf', '').upper()
        # Some are like 'X-17A-5_2'
        # Let's also extract the 'description' part if possible
        # Example: 0033_01_focus-report-part-ii_formx-17a-5_2.pdf
        # Group 1: focus-report-part-ii
        # Group 2: x-17a-5_2
        match = re.search(r'^\d+_\d+_(.*?)_form(.*?)\.pdf$', f)
        if match:
            desc = match.group(1).replace('-', ' ').title()
            ft = match.group(2).upper()
            pdf_info[ft] = {
                'filename': f,
                'type': ft,
                'description': desc
            }
        else:
            # Fallback
            pdf_info[form_type_raw] = {
                'filename': f,
                'type': form_type_raw,
                'description': form_type_raw # placeholder
            }

# 2. Map HTML files and their slugs
html_files = os.listdir(filings_dir)
html_map = {}
for f in html_files:
    slug = slugify(f.replace('.html', ''))
    html_map[slug] = f

# 3. Validation
report = []

# Check if every PDF has an HTML
for ft, info in pdf_info.items():
    slug = slugify(ft)
    if slug not in html_map:
        # Check if there's a variation (e.g. 10-K vs 10k)
        report.append(f"[MISSING HTML] No HTML file found for Form '{ft}' (PDF: {info['filename']})")
    else:
        html_file = html_map[slug]
        filepath = os.path.join(filings_dir, html_file)
        with open(filepath, 'r', encoding='utf-8') as hf:
            content = hf.read()
            
        # Check H1
        h1_match = re.search(r'<h1>(.*?)</h1>', content)
        if h1_match:
            h1 = h1_match.group(1).strip()
            if slugify(h1) != slug and h1 != "SEC Filing":
                report.append(f"[INCONSISTENT H1] {html_file}: H1 is '{h1}', expected something like '{ft}'.")
            if h1 == "SEC Filing":
                report.append(f"[GENERIC H1] {html_file}: H1 is generic 'SEC Filing'.")
        
        # Check Subtitle
        sub_match = re.search(r'<p class="filing-subtitle">(.*?)</p>', content)
        if sub_match:
            subtitle = sub_match.group(1).strip()
            # If the PDF description is in the filename, check if subtitle matches or is close
            # info['description'] might be 'Focus Report Part Ii'
            # subtitle might be 'Focus Report Part Ii'
            if slugify(subtitle) != slugify(info['description']):
                report.append(f"[SUBTITLE MISMATCH] {html_file}: Subtitle is '{subtitle}', expected '{info['description']}'.")

        # Check PDF link
        pdf_link_match = re.search(r'href=".*?sec_pdfs/(.*?)"', content)
        if pdf_link_match:
            linked_pdf = pdf_link_match.group(1)
            if linked_pdf != info['filename']:
                report.append(f"[PDF LINK ERROR] {html_file}: Links to '{linked_pdf}', should link to '{info['filename']}'.")
        else:
            report.append(f"[MISSING PDF LINK] {html_file}: No link to PDF found.")

# Check for orphan HTMLs
for slug, f in html_map.items():
    # Only check if it matches a known form type format (alphanumeric)
    found_pdf = False
    for ft in pdf_info:
        if slugify(ft) == slug:
            found_pdf = True
            break
    if not found_pdf:
        # Check if it corresponds to an index or special page
        if f not in ['index.html', '404.html']:
            report.append(f"[ORPHAN HTML] {f}: No corresponding PDF found for this HTML.")

print("\n".join(report))
