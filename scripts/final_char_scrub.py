import os
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


def final_char_scrub():
    filings_dir = FILINGS_DIR
    
    # Patterns to catch
    patterns = [
        "ΓÇô", "ΓÇö", "ΓÇô", "ΓÇö", # common garbled
        "\u0393\u00c7\u00f4", "\u0393\u00c7\u00f6", # unicode forms
        "", "???", " ??? ", " — " # broken segments
    ]
    
    # We want to be careful with ??? but in this context (SEC filings full names) 
    # it's almost always a broken hyphen.
    
    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        original = content
        
        # Specific cleanup for the "????" clusters seen in grep
        content = content.replace("??????", "—")
        content = content.replace("???", "—")
        content = content.replace("Г—", "—")
        content = content.replace("ГўГўГ©", "—")
        
        # Re-scrub standard ones
        for p in ["ΓÇô", "ΓÇö", "ΓÇô", "ΓÇö"]:
            content = content.replace(p, "—")
            
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Scrubbed chars in {filename}")

if __name__ == "__main__":
    final_char_scrub()
