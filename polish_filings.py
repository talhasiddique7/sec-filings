from bs4 import BeautifulSoup
import os
import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Update Breadcrumb
    breadcrumb = soup.find('div', class_='breadcrumb')
    if breadcrumb:
        # Find the form type (last child or span)
        form_type = breadcrumb.get_text(strip=True).split('/')[-1].strip()
        new_breadcrumb = soup.new_tag('div', **{'class': 'breadcrumb'})
        
        home_link = soup.new_tag('a', href='../index.html')
        home_link.string = 'Home'
        
        sep1 = soup.new_tag('span', **{'class': 'sep'})
        sep1.string = '/'
        
        filings_link = soup.new_tag('a', href='../index.html#search-filings')
        filings_link.string = 'Filings'
        
        sep2 = soup.new_tag('span', **{'class': 'sep'})
        sep2.string = '/'
        
        current_span = soup.new_tag('span')
        current_span.string = form_type
        
        new_breadcrumb.append(home_link)
        new_breadcrumb.append(sep1)
        new_breadcrumb.append(filings_link)
        new_breadcrumb.append(sep2)
        new_breadcrumb.append(current_span)
        
        breadcrumb.replace_with(new_breadcrumb)

    # 2. Update Filing Hero & Subtitle
    subtitle = soup.find('p', class_='filing-subtitle')
    if subtitle:
        # Style is handled in CSS, but let's ensure the class is correct
        pass

    # 3. Update Meta Grid Icons
    meta_boxes = soup.find_all('div', class_='meta-box')
    icon_map = {
        'frequency': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        'when': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        'deadline': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        'who': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
        'authority': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6l3 18h12l3-18H3z"/><path d="M19 6L5 6"/><path d="M10 11L10 17"/><path d="M14 11L14 17"/></svg>'
    }

    for box in meta_boxes:
        label_span = box.find('span', class_='meta-label')
        if label_span:
            label_text = label_span.get_text(strip=True).lower()
            icon_html = None
            for key in icon_map:
                if key in label_text:
                    icon_html = icon_map[key]
                    break
            
            if icon_html and not label_span.find('svg'):
                icon_soup = BeautifulSoup(icon_html, 'html.parser')
                label_span.insert(0, icon_soup.find('svg'))
                # Ensure spacing
                label_span.append(' ') 

    # 4. Polish the "Quick Summary" or "Filing Summary"
    summary_h3 = soup.find('h3', string=re.compile(r'Summary', re.I))
    if summary_h3:
        summary_h3.string = "Filing Summary"
        summary_h3['style'] = "margin-top: 0; color: var(--text-primary); margin-bottom: 1.25rem;"
        
        ul = summary_h3.find_next('ul')
        if ul:
            ul['style'] = "list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 1rem;"
            for li in ul.find_all('li'):
                strong = li.find('strong')
                if strong:
                    strong['style'] = "color:var(--accent-blue)"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

def main():
    dir_path = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/filings"
    for filename in os.listdir(dir_path):
        if filename.endswith('.html'):
            print(f"Polishing {filename}...")
            update_file(os.path.join(dir_path, filename))

if __name__ == '__main__':
    main()
