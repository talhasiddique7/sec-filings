from bs4 import BeautifulSoup
import os
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')


def add_read_more_to_file(filepath):
    THRESHOLD = 300  # Only truncate if text is truly long
    
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    changed = False
    
    # Target paragraphs in item grids or detail blocks
    for p in soup.select('.item-card p, .item-detail p, .article-block p'):
        # Skip if already wrapped or has class to skip
        if p.find_parent('div', class_='truncate-wrapper'):
            continue
        if p.get('class') and ('section-desc' in p.get('class') or 'insight-body' in p.get('class')):
            continue
            
        text = p.get_text(strip=True)
        if len(text) > THRESHOLD:
            changed = True
            
            # Create the premium structure
            wrapper = soup.new_tag('div', **{'class': 'truncate-wrapper'})
            inner_p = soup.new_tag('p', **{'class': 'truncate-text'})
            inner_p.extend(p.contents)
            
            btn = soup.new_tag('button', **{
                'class': 'read-more-btn',
                'type': 'button',
                'onclick': 'toggleReadMore(this)'
            })
            btn.string = 'Read more'
            
            wrapper.append(inner_p)
            wrapper.append(btn)
            
            p.replace_with(wrapper)
            
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True
    return False

def main():
    base_dir = os.getcwd()
    filings_dir = os.path.join(base_dir, 'filings')
    
    # Key form types (without .html extension)
    key_forms = ['10k', '10q', '8k', '20f', '40f', '6k', '13d', '13g', '4', '5', '25', '15', '144', '424b1', '424b2', '424b3', '424b4', '424b5', '425', '497', '497k']
    
    count = 0
    
    # Process index.html
    index_path = os.path.join(base_dir, 'index.html')
    if os.path.exists(index_path):
        if add_read_more_to_file(index_path):
            count += 1
    
    # Process key filings
    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
        form_type = filename[:-5]  # Remove .html
        if form_type in key_forms:
            filepath = os.path.join(filings_dir, filename)
            if add_read_more_to_file(filepath):
                count += 1
            
    print(f"Applied high-threshold truncation to {count} files.")

if __name__ == '__main__':
    main()
