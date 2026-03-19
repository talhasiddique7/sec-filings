
import json
import os
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


def update_data_with_pdfs():
    data_path = os.path.join(ASSETS_DIR, 'data.json')
    mapping_path = os.path.join(ASSETS_DIR, 'pdf_mapping.json')
    
    if not os.path.exists(mapping_path):
        print("pdf_mapping.json not found in assets/.")
        return
        
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    with open(mapping_path, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
        
    updated_count = 0
    for form in data['forms']:
        ft = form['form_type']
        if ft in mapping:
            form['pdf_url'] = mapping[ft]
            updated_count += 1
            
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"Updated {updated_count} forms with PDF URLs in data.json.")

if __name__ == "__main__":
    update_data_with_pdfs()
