
import os
import re

def slugify(text):
    s = text.lower()
    s = s.replace(' ', '')
    s = s.replace('/', '')
    s = s.replace('-', '')
    s = s.replace('.', '')
    # Check if ends with data or other suffixes
    s = s.replace('data', '')
    return s

# Directories
sec_pdfs_dir = r'C:\Users\ahmad\OneDrive\Desktop\Blogs\sec-filings\sec_pdfs'
filings_dir = r'C:\Users\ahmad\OneDrive\Desktop\Blogs\sec-filings\filings'

# 1. Map PDFs by form slug
pdf_files = os.listdir(sec_pdfs_dir)
pdf_map = {}
for f in pdf_files:
    # Pattern: ..._form[TYPE].pdf or ..._form[TYPE][SUFF].pdf
    # Examples: form10-k.pdf, form4data.pdf, formn-cen.pdf
    match = re.search(r'_form(.*?)\.pdf$', f, re.IGNORECASE)
    if match:
        raw_type = match.group(1)
        slug = slugify(raw_type)
        if slug not in pdf_map:
            pdf_map[slug] = []
        pdf_map[slug].append(f)

# 2. Check HTML files
html_files = [f for f in os.listdir(filings_dir) if f.endswith('.html')]
results = []

for html_file in html_files:
    filepath = os.path.join(filings_dir, html_file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract H1 (Form Type)
    h1_match = re.search(r'<h1>(.*?)</h1>', content)
    if not h1_match:
        results.append(f"[FAIL] {html_file}: No <h1> form type found.")
        continue
    
    form_type_h1 = h1_match.group(1).strip()
    h1_slug = slugify(form_type_h1)
    
    # Extract filing-subtitle
    subtitle_match = re.search(r'<p class="filing-subtitle">(.*?)</p>', content)
    subtitle = subtitle_match.group(1).strip() if subtitle_match else "N/A"
    
    # Extract PDF link
    # Pattern: href="...sec_pdfs/[FILENAME]"
    pdf_link_match = re.search(r'href=".*?/sec_pdfs/(.*?)"', content)
    
    if pdf_link_match:
        linked_pdf = pdf_link_match.group(1)
        
        # Verify if this PDF exists
        if not os.path.exists(os.path.join(sec_pdfs_dir, linked_pdf)):
            results.append(f"[FAIL] {html_file}: Linked PDF '{linked_pdf}' does NOT exist in sec_pdfs.")
            continue
            
        # Verify if the linked PDF matches the form type in H1
        # Extract form type from the linked_pdf filename
        lp_match = re.search(r'_form(.*?)\.pdf$', linked_pdf, re.IGNORECASE)
        if lp_match:
            lp_raw = lp_match.group(1)
            lp_slug = slugify(lp_raw)
            if lp_slug != h1_slug:
                # Special cases: 10-K vs 10K, or index.html slugs
                # But here we check internal consistency of the filing page.
                results.append(f"[ISSUE] {html_file}: H1 is '{form_type_h1}' (slug:{h1_slug}), but linked PDF is '{linked_pdf}' (type slug:{lp_slug}).")
    else:
        # Check if it has a placeholder link
        if 'href="#"' in content:
            # Check if we have a PDF for this form type
            if h1_slug in pdf_map:
                results.append(f"[MISSING LINK] {html_file}: PDF exists for '{form_type_h1}' ({pdf_map[h1_slug][0]}), but HTML link is '#'.")
            else:
                # No PDF found for this form
                pass 
    
    # Check if links to home/index are correct (should be ../index.html)
    home_links = re.findall(r'href="(.*?index\.html)"', content)
    for link in home_links:
        if link != '../index.html' and link != 'index.html': # depends on context, but filings/ should use ../
            results.append(f"[LINK ISSUE] {html_file}: Home link '{link}' might be incorrect.")

print("\n".join(results))
