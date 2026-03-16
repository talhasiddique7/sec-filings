import os
from bs4 import BeautifulSoup

def remove_unnecessary_read_more():
    filings_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/filings"
    THRESHOLD = 300 # Increased threshold for better UX
    
    for filename in os.listdir(filings_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(filings_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        changed = False
        
        # 1. Handle all truncate-wrappers
        wrappers = soup.find_all('div', class_='truncate-wrapper')
        for wrapper in wrappers:
            # Extract the button if it exists
            btn = wrapper.find('button', class_='read-more-btn')
            if btn:
                btn_extract = btn.extract()
            else:
                btn_extract = None
                
            # Get text from either .truncate-text or directly from wrapper
            text_p = wrapper.find('p', class_='truncate-text')
            if text_p:
                text = text_p.get_text().strip()
            else:
                text = wrapper.get_text().strip()
            
            # Remove Read More if text is short
            if len(text) < THRESHOLD:
                # Replace wrapper with a simple paragraph
                new_p = soup.new_tag('p')
                # If we were in a grid item, we might want to keep some class? 
                # But simple P is usually safer for styles.css
                new_p.string = text
                wrapper.replace_with(new_p)
                changed = True
                print(f"  - Removed button from short section in {filename} ({len(text)} chars)")
            else:
                # For long text, ensure it has the correct internal structure
                wrapper.clear()
                np = soup.new_tag('p', **{'class': 'truncate-text'})
                np.string = text
                wrapper.append(np)
                if btn_extract:
                    wrapper.append(btn_extract)
                else:
                    # If it was long but missing a button, add one
                    new_btn = soup.new_tag('button', **{
                        'class': 'read-more-btn',
                        'type': 'button',
                        'onclick': 'toggleReadMore(this)'
                    })
                    new_btn.string = "Read more"
                    wrapper.append(new_btn)
                changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated {filename}")

if __name__ == "__main__":
    remove_unnecessary_read_more()
