
import json
import os
import re

def slugify(text):
    s = text.lower()
    s = s.replace(' ', '')
    s = s.replace('/', '')
    s = s.replace('-', '')
    s = s.replace('.', '')
    return s

# Load data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

filings_dir = 'filings'
filings_files = os.listdir(filings_dir)
filings_map = {f.replace('.html', ''): f for f in filings_files if f.endswith('.html')}

def update_file(filepath, form_data):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update title
    content = re.sub(
        r'(<title>)(.*?)(</title>)',
        fr'\g<1>{form_data["form_type"]} — {form_data["full_name"]} | SEC Filings Guide\g<3>',
        content
    )

    # Update h1
    content = re.sub(
        r'(<h1>)(.*?)(</h1>)',
        fr'\g<1>{form_data["form_type"]}\g<3>',
        content
    )

    # Update breadcrumb
    content = re.sub(
        r'(<span class="current">)(.*?)(</span>)',
        fr'\g<1>{form_data["form_type"]}\g<3>',
        content
    )

    # Update subtitle
    content = re.sub(
        r'(<p class="filing-subtitle">)(.*?)(</p>)',
        fr'\g<1>{form_data["full_name"]}\g<3>',
        content,
        flags=re.DOTALL
    )

    # Determine Frequency based on Category
    cat = form_data["category"].lower()
    freq = "Periodic"
    if "annual" in cat: freq = "Annual"
    elif "quarterly" in cat: freq = "Quarterly"
    elif "current" in cat or "event" in cat: freq = "Event-Based"
    elif "registration" in cat: freq = "Registration"
    elif "proxy" in cat: freq = "Proxy"
    elif "insider" in cat or "ownership" in cat or "holdings" in cat: freq = "Insider/Ownership"
    elif "deregistration" in cat or "delisting" in cat: freq = "Critical Event"

    # Update Hero Meta Grid
    # Frequency
    content = re.sub(
        r'(<span class="meta-label">Frequency</span><span class="meta-value">)(.*?)(</span>)',
        fr'\1{freq}\3',
        content
    )
    # Deadline
    content = re.sub(
        r'(<span class="meta-label">Deadline</span><span class="meta-value">)(.*?)(</span>)',
        fr'\1{form_data["when"]}\3',
        content
    )
    # Who Files
    content = re.sub(
        r'(<span class="meta-label">Who Files</span><span class="meta-value">)(.*?)(</span>)',
        fr'\1{form_data["who"]}\3',
        content
    )

    # Update Quick Summary
    # What
    content = re.sub(
        r'(<li><strong>What:</strong> )(.*?)(</li>)',
        lambda m: f'<li><strong>What:</strong> {form_data["what"]}</li>',
        content
    )
    # When
    content = re.sub(
        r'(<li><strong>When:</strong> )(.*?)(</li>)',
        lambda m: f'<li><strong>When:</strong> {form_data["when"]}</li>',
        content
    )
    # Who
    content = re.sub(
        r'(<li><strong>Who:</strong> )(.*?)(</li>)',
        lambda m: f'<li><strong>Who:</strong> {form_data["who"]}</li>',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

updated_count = 0
for form in data['forms']:
    ft = form['form_type']
    slug = slugify(ft)
    if slug in filings_map:
        filepath = os.path.join(filings_dir, filings_map[slug])
        update_file(filepath, form)
        updated_count += 1
    else:
        # Try alternate slug
        alt_slug = ft.lower().replace(' ', '').replace('/', '').replace('.', '')
        if alt_slug in filings_map:
            filepath = os.path.join(filings_dir, filings_map[alt_slug])
            update_file(filepath, form)
            updated_count += 1

print(f"Updated {updated_count} filing detail pages.")
