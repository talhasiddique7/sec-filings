import os
from bs4 import BeautifulSoup

def remove_unnecessary_read_more():
    filings_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/filings"
    THRESHOLD = 250
    
    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        changed = False
        
        # 1. Clean up messy wrappers first (where text is raw inside div)
        wrappers = soup.find_all('div', class_='truncate-wrapper')
        for wrapper in wrappers:
            # Get all text inside (ignoring the button text)
            btn = wrapper.find('button', class_='read-more-btn')
            if btn:
                # Temporarily remove button to get pure text
                btn_extract = btn.extract()
            else:
                btn_extract = None
                
            text = wrapper.get_text().strip()
            
            if len(text) < THRESHOLD:
                # Remove read more
                new_p = soup.new_tag('p')
                new_p.string = text
                wrapper.replace_with(new_p)
                changed = True
            else:
                # Restore button and ensure proper internal P structure
                if btn_extract:
                    # Clear and rebuild
                    wrapper.clear()
                    np = soup.new_tag('p', **{'class': 'truncate-text'})
                    np.string = text
                    wrapper.append(np)
                    wrapper.append(btn_extract)
                    changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Cleaned/Removed 'Read more' in {filename}")

if __name__ == "__main__":
    remove_unnecessary_read_more()
