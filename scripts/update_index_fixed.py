import re
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

with open('generated_rows.html', 'r', encoding='utf-8') as f:
    rows = f.read()

# Replace between <tbody> and </tbody>
pattern = re.compile(r'(<table class="filings-table" id="filings-table">.*?<tbody>\n).*?(          </tbody>)', re.DOTALL)
new_content = pattern.sub(r'\g<1>' + rows.replace('\\', '\\\\') + r'\g<2>', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done!")
