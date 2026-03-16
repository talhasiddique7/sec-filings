
import json
import os

def update_data_with_pdfs():
    data_path = 'data.json'
    mapping_path = 'pdf_mapping.json'
    
    if not os.path.exists(mapping_path):
        print("pdf_mapping.json not found.")
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
