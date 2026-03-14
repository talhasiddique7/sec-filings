from bs4 import BeautifulSoup
import os

def main():
    filings_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/filings"
    THRESHOLD = 300 # Only truncate if text is truly long
    
    count = 0
    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
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
            count += 1
            
    print(f"Applied high-threshold truncation to {count} files.")

if __name__ == '__main__':
    main()
