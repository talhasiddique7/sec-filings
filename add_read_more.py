from bs4 import BeautifulSoup
import os

def main():
    filings_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/filings"
    
    count = 0
    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        changed = False
        
        # Find paragraphs inside cards that aren't the title or section description
        for p in soup.select('.item-card p, .item-detail p'):
            if p.get('class') and 'section-desc' in p.get('class'):
                continue
                
            text = p.get_text(strip=True)
            if len(text) > 80:
                changed = True
                
                # Create wrapper
                wrapper = soup.new_tag('div', **{'class': 'truncate-wrapper'})
                # Copy paragraph styles/classes (if it was a p, maybe we want it to still look like a p, so let's make it a p block instead of div)
                inner = soup.new_tag('p', **{'class': 'truncate-text'})
                inner.extend(p.contents)
                
                btn = soup.new_tag('button', type='button', onclick='toggleReadMore(this)', **{'class': 'read-more-btn'})
                btn.string = 'Read more'
                
                wrapper.append(inner)
                wrapper.append(btn)
                
                p.replace_with(wrapper)
                
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            count += 1
            
    print(f"Updated {count} files.")

if __name__ == '__main__':
    main()
