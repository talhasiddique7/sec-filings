import re

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
