import json
import os

def slugify(text):
    s = text.lower()
    s = s.replace(' ', '')
    s = s.replace('/', '')
    s = s.replace('-', '')
    s = s.replace('.', '')
    return s

def alt_slugify(text):
    return text.lower().replace(' ', '').replace('/', '').replace('.', '')

def generate_html(form):
    ft = form.get('form_type', '')
    fn = form.get('full_name', '')
    w = form.get('what', '')
    wn = form.get('when', '')
    who = form.get('who', '')
    val = form.get('why_use_it', '')
    if not val:
        val = w
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/><meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{ft} — {fn} | SEC Filings Guide</title>
<meta content="Detailed guide and reference for SEC Filings. {w}" name="description"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&amp;family=Inter:wght@300;400;500;600;700;800&amp;display=swap" rel="stylesheet"/>
<link href="../styles.css" rel="stylesheet"/>
</head>
<body class="detail-page">
<header class="site-header scrolled" id="site-header">
<div class="header-inner">
<a class="site-logo" href="../index.html">
<div class="logo-icon">SEC</div>
<span class="logo-text">Filings Guide</span>
</a>
<nav class="nav-links" id="nav-links">
<a href="../index.html">Home</a>
<a href="../index.html#popular-filings">Popular Filings</a>
<a href="../index.html#search-filings">Search All</a>
<a href="../index.html#deep-dives">Learn</a>
</nav>
<button aria-label="Toggle theme" class="theme-toggle" id="theme-toggle">
<svg class="sun-icon" fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="5"></circle><line x1="12" x2="12" y1="1" y2="3"></line><line x1="12" x2="12" y1="21" y2="23"></line><line x1="4.22" x2="5.64" y1="4.22" y2="5.64"></line><line x1="18.36" x2="19.78" y1="18.36" y2="19.78"></line><line x1="1" x2="3" y1="12" y2="12"></line><line x1="21" x2="23" y1="12" y2="12"></line><line x1="4.22" x2="5.64" y1="19.78" y2="18.36"></line><line x1="18.36" x2="19.78" y1="5.64" y2="4.22"></line></svg>
<svg class="moon-icon" fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
</button>
<button aria-label="Toggle menu" class="mobile-toggle" id="mobile-toggle">
<span></span><span></span><span></span>
</button>
</div>
</header>
<main class="container">
<div class="breadcrumb">
  <a href="../index.html">Home</a> 
  <span class="sep">/</span> 
  <a href="../index.html#search-filings">Filings</a>
  <span class="sep">/</span> 
  <span>{ft}</span>
</div>

<section class="filing-hero fade-in visible">
  <div class="filing-badge cyan">SEC Filing</div>
  <h1>{ft}</h1>
  <p class="filing-subtitle">{fn}</p>
  
  <div class="filing-meta-grid">
    <div class="meta-box">
      <span class="meta-label">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        Frequency / When
      </span>
      <span class="meta-value">{wn}</span>
    </div>
    <div class="meta-box">
      <span class="meta-label">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        Who Files
      </span>
      <span class="meta-value">{who}</span>
    </div>
    <div class="meta-box">
      <span class="meta-label">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6l3 18h12l3-18H3z"/><path d="M19 6L5 6"/><path d="M10 11L10 17"/><path d="M14 11L14 17"/></svg>
        Authority
      </span>
      <span class="meta-value">SEC Mandate</span>
    </div>
  </div>

  <div class="filing-actions">
    <a class="btn btn-primary" href="https://www.sec.gov/search-filings" target="_blank">
      <span>📄 Search live on EDGAR →</span>
    </a>
  </div>
</section>

<div class="filing-layout">
<aside class="filing-toc fade-in visible">
  <div class="toc-inner">
    <h3>Page Contents</h3>
    <nav>
      <a class="active" href="#general-info">General Disclosure</a>
      <a href="#compliance">Compliance Context</a>
    </nav>
  </div>
</aside>

<div class="filing-content fade-in visible">
<article class="content-section" id="general-info">
  <div class="part-header">Form Purpose</div>
  <h2>General Information &amp; Instructions</h2>
  
  <div class="article-block">
    <div class="callout tip filing-summary" style="margin-bottom: 2rem;">
      <h3 style="margin-top: 0; color: var(--text-primary); margin-bottom: 1.25rem;">Filing Summary</h3>
      <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 1rem;">
        <li><strong style="color:var(--accent-blue)">WHAT: </strong>{w}</li>
        <li><strong style="color:var(--accent-blue)">WHY: </strong>{val}</li>
        <li><strong style="color:var(--accent-blue)">WHEN: </strong>{wn}</li>
        <li><strong style="color:var(--accent-blue)">WHO: </strong>{who}</li>
      </ul>
    </div>

    <div class="professional-insight">
      <div class="insight-header">
        <svg fill="none" height="18" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="18">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" x2="12" y1="16" y2="12"></line>
          <line x1="12" x2="12.01" y1="8" y2="8"></line>
        </svg>
        <h3 class="insight-title">Professional Insight</h3>
      </div>
      <p class="insight-body">{val if val else "This form represents a critical component of the SEC's regulatory framework, ensuring that material information is accessible to all market participants simultaneously."}</p>
    </div>

    <h3 style="margin-top: 3rem; margin-bottom: 1.5rem; font-family: var(--font-heading); font-size: 1.8rem;">Detailed Breakdown</h3>
    <p style="font-size: 1.1rem; line-height: 1.8; color: var(--text-secondary); margin-bottom: 2rem;">{w}</p>
    
    <div class="item-grid" id="compliance">
      <div class="item-card highlighted">
        <span class="item-num">Compliance</span>
        <h3>Regulatory Mandate</h3>
        <p>This filing is required under the Securities Exchange Act to maintain transparent and fair markets. Failure to comply can result in significant legal and financial repercussions for the reporting entity.</p>
      </div>
      <div class="item-card">
        <span class="item-num">Investor Value</span>
        <h3>Why it Matters</h3>
        <p>{val if (val and val != w) else "Investors use this data to perform due diligence, assess risk, and verify the accuracy of corporate statements."}</p>
      </div>
    </div>
  </div>
</article>
</div>
</div>
</main>
<footer class="site-footer"><div class="container"><div class="footer-bottom"><p>© 2026 SEC Filings Guide.</p><a href="../index.html">← Back to Home</a></div></div></footer>
<script src="../script.js"></script>
</body>
</html>
"""
    return html

def main():
    base_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings"
    with open(os.path.join(base_dir, "data.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
        
    filings_dir = os.path.join(base_dir, "filings")
    existing_files = [f for f in os.listdir(filings_dir) if f.endswith('.html')]
    existing_slugs = {f.replace('.html', '') for f in existing_files}
    
    unique_forms = {}
    for form in data['forms']:
        form_type = form['form_type']
        if form_type not in unique_forms:
            unique_forms[form_type] = form
            
    count = 0
    for ft, form in unique_forms.items():
        slug = slugify(ft)
        alt_slug = alt_slugify(ft)
        if slug in existing_slugs or alt_slug in existing_slugs:
            continue
            
        html_content = generate_html(form)
        filepath = os.path.join(filings_dir, f"{slug}.html")
        with open(filepath, "w", encoding="utf-8") as out:
            out.write(html_content)
        count += 1
        print(f"Created {slug}.html for {ft}")
        
    print(f"Created {count} missing HTML files.")
    
if __name__ == "__main__":
    main()
