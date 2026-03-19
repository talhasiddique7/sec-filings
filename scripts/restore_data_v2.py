import json
import os
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


def restore_data_and_mark_variants():
    base_dir = BASE_DIR
    source_path = os.path.join(base_dir, "data_full.json")
    data_path = os.path.join(ASSETS_DIR, "data.json")
    
    # Load source data (147 forms)
    source_data = None
    for enc in ['utf-16', 'utf-8', 'ascii']:
        try:
            with open(source_path, 'r', encoding=enc) as f:
                source_data = json.load(f)
            print(f"Loaded source data using {enc} encoding.")
            break
        except Exception:
            continue
            
    if not source_data:
        print("Failed to load source data.")
        return

    merge_map = {
        "10-K": ["10-KT", "10-K/A"],
        "10-Q": ["10-QT", "10-QT/A"],
        "11-K": ["11-KT"],
        "8-K": ["8-K12B", "8-K12G3", "8-K15D5"],
        "DEF 14A": ["DEFA14A", "DEFC14A", "DEFM14A", "DEFR14A", "DEFS14A", "DEF 14C", "PRE 14A", "PREC14A", "PREM14A", "PREN14A", "PRE 14C"],
        "424B4": ["424B1", "424B2", "424B3", "424B4/A", "424B5", "424B7", "FWP"],
        "S-3": ["S-3ASR", "S-3MEF", "S-3D"],
        "4": ["3", "5"],
        "SC 13D": ["SC 13G"],
        "NT 10-K": ["NT 10-Q", "NT 20-F", "NT 11-K", "NT-NCSR", "NT 10-K/A", "NT 10-Q/A"],
        "Form 15": ["15-12B", "15-12G", "15-15D", "15F-12B", "15F-12G", "Form 25", "25-NSE", "34-12H"],
        "1-A": ["1-A POS", "1-K", "1-SA", "1-Z", "Form C", "C-AR", "C-U"],
        "S-1": ["S-1MEF"],
        "F-3": ["F-3ASR"],
        "F-6": ["F-6 POS"]
    }
    
    # Invert the map
    variant_to_parent = {}
    for p, vs in merge_map.items():
        for v in vs:
            variant_to_parent[v] = p

    # Mark forms
    for form in source_data['forms']:
        ft = form['form_type']
        if ft in variant_to_parent:
            form['parent_form'] = variant_to_parent[ft]
            form['is_variant'] = True
        else:
            form['is_variant'] = False

    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(source_data, f, indent=2)
    print(f"data.json updated: {len(source_data['forms'])} forms with variant flags.")

if __name__ == "__main__":
    restore_data_and_mark_variants()
