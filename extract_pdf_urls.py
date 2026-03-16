
import os
import json
import re

def extract_pdf_urls():
    pdfs_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/sec_pdfs"
    base_url = "https://github.com/talhasiddique7/sec-filings/blob/main/sec_pdfs/"
    
    mapping = {}
    
    for filename in os.listdir(pdfs_dir):
        if not filename.endswith('.pdf'):
            continue
            
        # Try to find the form type in the filename
        # Pattern: ..._form[TYPE].pdf or ..._form-[TYPE].pdf
        match = re.search(r'_form-?([a-z0-9-]+)\.pdf$', filename, re.I)
        if match:
            ft_code = match.group(1).upper()
            # Normalize some names
            if ft_code == '10-K': ft_code = '10-K'
            elif ft_code == '10-Q': ft_code = '10-Q'
            elif ft_code == '8-K': ft_code = '8-K'
            
            mapping[ft_code] = base_url + filename
            
    # Add some manual corrections if needed
    # (Checking the list_dir output...)
    # 0161_01_..._form4.pdf -> 4
    # 0163_01_..._form3.pdf -> 3
    # 0153_01_..._form5.pdf -> 5
    
    # Save the mapping
    with open('pdf_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)
        
    print(f"Extracted {len(mapping)} PDF mappings.")

if __name__ == "__main__":
    extract_pdf_urls()
