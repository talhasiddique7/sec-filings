import os
import re
from bs4 import BeautifulSoup
import traceback

filings_dir = r'c:\Users\ahmad\OneDrive\Desktop\Blogs\sec-filings\filings'
files = os.listdir(filings_dir)
html_files = [f for f in files if f.endswith('.html')]

# Definitions for specific forms
specific_forms = {
    '10q': {
        'toc': [
            {'id': 'part-i', 'name': 'PART I: Financial Information'},
            {'id': 'part-ii', 'name': 'PART II: Other Information'},
            {'id': 'signatures', 'name': 'Signatures'}
        ],
        'content': '''
        <article class="content-section" id="part-i">
            <div class="part-header">PART I</div>
            <h2>Financial Information</h2>
            <div class="item-grid">
                <div class="item-card highlighted">
                    <span class="item-num">Item 1</span>
                    <h3>Financial Statements</h3>
                    <p>Unaudited interim financial statements including balance sheets, income statements, and cash flows.</p>
                </div>
                <div class="item-card highlighted">
                    <span class="item-num">Item 2</span>
                    <h3>MD&A</h3>
                    <p>Management's Discussion and Analysis of Financial Condition and Results of Operations.</p>
                </div>
                <div class="item-card">
                    <span class="item-num">Item 3</span>
                    <h3>Market Risk</h3>
                    <p>Quantitative and Qualitative Disclosures About Market Risk.</p>
                </div>
                <div class="item-card">
                    <span class="item-num">Item 4</span>
                    <h3>Controls and Procedures</h3>
                    <p>Evaluation of disclosure controls and procedures.</p>
                </div>
            </div>
        </article>
        <article class="content-section" id="part-ii">
            <div class="part-header">PART II</div>
            <h2>Other Information</h2>
            <div class="article-block">
                <div class="item-row">
                    <div class="item-num-tag">Item 1</div>
                    <div class="item-detail">
                        <h3>Legal Proceedings</h3>
                        <p>Brief description of any material legal proceedings commenced during the quarter.</p>
                    </div>
                </div>
                <div class="item-row">
                    <div class="item-num-tag">Item 1A</div>
                    <div class="item-detail">
                        <h3>Risk Factors</h3>
                        <p>Material changes from risk factors previously disclosed in the annual 10-K.</p>
                    </div>
                </div>
                <div class="item-row">
                    <div class="item-num-tag">Item 2</div>
                    <div class="item-detail">
                        <h3>Unregistered Sales & Use of Proceeds</h3>
                        <p>Information on equity sales not registered under the Securities Act and issuer stock repurchases.</p>
                    </div>
                </div>
                <div class="item-row">
                    <div class="item-num-tag">Item 6</div>
                    <div class="item-detail">
                        <h3>Exhibits</h3>
                        <p>A list of financial statements, schedules, and exhibits filed with the 10-Q.</p>
                    </div>
                </div>
            </div>
        </article>
        '''
    },
    '8k': {
        'toc': [
            {'id': 'events', 'name': 'Material Events'},
            {'id': 'exhibits', 'name': 'Financial Statements & Exhibits'},
            {'id': 'signatures', 'name': 'Signatures'}
        ],
        'content': '''
        <article class="content-section" id="events">
            <div class="part-header">SECTIONS 1-8</div>
            <h2>Material Events</h2>
            <p class="section-intro">Form 8-K is triggered by specific events. Here are the most common sections:</p>
            <div class="item-grid">
                <div class="item-card highlighted">
                    <span class="item-num">Section 1</span>
                    <h3>Business and Operations</h3>
                    <p>Includes Entry into or Termination of a Material Definitive Agreement, and Bankruptcy or Receivership.</p>
                </div>
                <div class="item-card highlighted">
                    <span class="item-num">Section 2</span>
                    <h3>Financial Information</h3>
                    <p>Results of Operations and Financial Condition, Creation of a Direct Financial Obligation, and Costs Associated with Exit or Disposal Activities.</p>
                </div>
                <div class="item-card">
                    <span class="item-num">Section 3</span>
                    <h3>Securities and Trading</h3>
                    <p>Notice of Delisting or Failure to Satisfy a Continued Listing Rule, Unregistered Sales of Equity Securities.</p>
                </div>
                <div class="item-card">
                    <span class="item-num">Section 4</span>
                    <h3>Accountants</h3>
                    <p>Changes in Registrant's Certifying Accountant, Non-Reliance on Previously Issued Financial Statements.</p>
                </div>
                <div class="item-card highlighted">
                    <span class="item-num">Section 5</span>
                    <h3>Corporate Governance</h3>
                    <p>Changes in Control, Departure or Election of Directors and Principal Officers, Amendments to Articles of Incorporation.</p>
                </div>
                <div class="item-card">
                    <span class="item-num">Section 7</span>
                    <h3>Regulation FD</h3>
                    <p>Regulation FD Disclosure for the public distribution of important material information.</p>
                </div>
                <div class="item-card">
                    <span class="item-num">Section 8</span>
                    <h3>Other Events</h3>
                    <p>Other Events that the registrant deems of importance to security holders.</p>
                </div>
            </div>
        </article>
        <article class="content-section" id="exhibits">
            <div class="part-header">SECTION 9</div>
            <h2>Financial Statements and Exhibits</h2>
            <div class="article-block">
                <div class="item-row">
                    <div class="item-num-tag">Item 9.01</div>
                    <div class="item-detail">
                        <h3>Financial Statements and Exhibits</h3>
                        <p>Financial statements of businesses acquired, pro forma financial information, and all relevant exhibits (like press releases, contracts).</p>
                    </div>
                </div>
            </div>
        </article>
        '''
    },
    's1': {
        'toc': [
            {'id': 'prospectus-summary', 'name': 'Prospectus Summary'},
            {'id': 'financial-info', 'name': 'Financial Operations'},
            {'id': 'governance', 'name': 'Governance & Backing'},
            {'id': 'signatures', 'name': 'Signatures'}
        ],
        'content': '''
        <article class="content-section" id="prospectus-summary">
            <div class="part-header">PART I</div>
            <h2>Prospectus Core Components</h2>
            <div class="item-grid">
                <div class="item-card highlighted">
                    <h3>Summary Information</h3>
                    <p>A high-level overview of the company, the offering, and key financial metrics. Designed to hook the investor.</p>
                </div>
                <div class="item-card highlighted">
                    <h3>Risk Factors</h3>
                    <p>A comprehensive disclosure of all material risks that could negatively impact the company's business or stock price.</p>
                </div>
                <div class="item-card">
                    <h3>Use of Proceeds</h3>
                    <p>How the company intends to spend the capital raised from the offering (e.g., R&D, debt repayment, acquisitions).</p>
                </div>
                <div class="item-card">
                    <h3>Dividend Policy</h3>
                    <p>Whether the company intends to pay cash dividends to shareholders.</p>
                </div>
            </div>
        </article>
        <article class="content-section" id="financial-info">
            <div class="part-header">FINANCIALS</div>
            <h2>Operations and Capitalization</h2>
            <div class="article-block">
                <div class="item-row">
                    <div class="item-num-tag">MD&A</div>
                    <div class="item-detail">
                        <h3>Management's Discussion & Analysis</h3>
                        <p>A deeply detailed explanation of financial condition and results of operations, written by management.</p>
                    </div>
                </div>
                <div class="item-row">
                    <div class="item-num-tag">Business</div>
                    <div class="item-detail">
                        <h3>Business Description</h3>
                        <p>Full breakdown of the operations, total addressable market (TAM), competitive advantage, and strategy.</p>
                    </div>
                </div>
                <div class="item-row">
                    <div class="item-num-tag">Capital</div>
                    <div class="item-detail">
                        <h3>Capitalization & Dilution</h3>
                        <p>Shows how the balance sheet will change post-IPO and calculates the immediate dilution in book value for new investors.</p>
                    </div>
                </div>
            </div>
        </article>
        <article class="content-section" id="governance">
            <div class="part-header">GOVERNANCE</div>
            <h2>Leadership and Backing</h2>
            <div class="item-grid">
                <div class="item-card">
                    <h3>Management & Compensation</h3>
                    <p>Bios of executives and directors, along with detailed compensation, equity grants, and employment agreements.</p>
                </div>
                <div class="item-card">
                    <h3>Principal Stockholders</h3>
                    <p>The "cap table" showing exactly who owned the company before the IPO and who is selling shares in the offering.</p>
                </div>
                <div class="item-card">
                    <h3>Underwriting</h3>
                    <p>Details the investment banks leading the deal, their fees, and lock-up agreements preventing insiders from selling immediately.</p>
                </div>
            </div>
        </article>
        '''
    },
    '13f': {
        'toc': [
            {'id': 'cover-page', 'name': 'Cover Page'},
            {'id': 'information-table', 'name': 'Information Table'},
            {'id': 'signatures', 'name': 'Signatures'}
        ],
        'content': '''
        <article class="content-section" id="cover-page">
            <div class="part-header">REPORTING ENTITY</div>
            <h2>Cover & Summary Pages</h2>
            <div class="item-grid">
                <div class="item-card highlighted">
                    <h3>Cover Page</h3>
                    <p>Identifies the institutional investment manager filing the report, including contact details and reporting period.</p>
                </div>
                <div class="item-card">
                    <h3>Summary Page</h3>
                    <p>Provides the total number of items on the information table, the total value of all holdings, and any other managers included in the report.</p>
                </div>
            </div>
        </article>
        <article class="content-section" id="information-table">
            <div class="part-header">PORTFOLIO DATA</div>
            <h2>Information Table</h2>
            <div class="article-block">
                <p>The core of the 13F filing. It contains a detailed XML table (formerly text) of all reportable US equity holdings.</p>
                <div class="item-row">
                    <div class="item-num-tag">Issuer</div>
                    <div class="item-detail">
                        <h3>Name of Issuer & Title of Class</h3>
                        <p>The company name and specific class of security (e.g., Common Stock, Put Option, Call Option).</p>
                    </div>
                </div>
                <div class="item-row">
                    <div class="item-num-tag">CUSIP</div>
                    <div class="item-detail">
                        <h3>CUSIP Number</h3>
                        <p>The unique nine-character identifier for the security.</p>
                    </div>
                </div>
                <div class="item-row">
                    <div class="item-num-tag">Value</div>
                    <div class="item-detail">
                        <h3>Value & Number of Shares</h3>
                        <p>The total fair market value of the position in thousands of dollars, and the exact count of shares (or principal amount) held on the last day of the quarter.</p>
                    </div>
                </div>
                <div class="item-row">
                    <div class="item-num-tag">Discretion</div>
                    <div class="item-detail">
                        <h3>Investment Discretion & Voting Authority</h3>
                        <p>Indicates whether the manager has sole, shared, or no voting authority over the shares.</p>
                    </div>
                </div>
            </div>
        </article>
        '''
    }
}

generic_form = {
    'toc': [
        {'id': 'key-components', 'name': 'Key Form Components'},
        {'id': 'usage', 'name': 'Regulatory Context'},
        {'id': 'signatures', 'name': 'Signatures'}
    ],
    'content': '''
    <article class="content-section" id="key-components">
        <div class="part-header">STRUCTURE</div>
        <h2>Key Form Components</h2>
        <p class="section-intro">This SEC filing consists of mandatory disclosures tailored to its specific regulatory purpose. Typical components include:</p>
        <div class="item-grid">
            <div class="item-card highlighted">
                <h3>Primary Disclosures</h3>
                <p>The core information required by the regulatory mandate. This section provides the detailed factual records, financial details, or ownership changes relevant to the filing.</p>
            </div>
            <div class="item-card">
                <h3>Exhibits & Attachments</h3>
                <p>Supplementary materials, legal agreements, contracts, or prior filings incorporated by reference to support the primary disclosures.</p>
            </div>
            <div class="item-card">
                <h3>Declarations</h3>
                <p>Statements asserting the accuracy, completeness, and compliance of the provided information, standard across official SEC documents.</p>
            </div>
        </div>
    </article>
    <article class="content-section" id="usage">
        <div class="part-header">APPLICATION</div>
        <h2>Regulatory Context</h2>
        <div class="article-block">
            <p>This form serves a distinct function within the SEC's EDGAR database, maintaining market transparency and ensuring fair access to crucial institutional data.</p>
            <div class="item-row">
                <div class="item-num-tag">Integrity</div>
                <div class="item-detail">
                    <h3>Market Integrity</h3>
                    <p>By mandating standardized disclosures, the SEC ensures all market participants have equal access to material information.</p>
                </div>
            </div>
            <div class="item-row">
                <div class="item-num-tag">Compliance</div>
                <div class="item-detail">
                    <h3>Legal Compliance</h3>
                    <p>Filers must adhere to strict formatting and timeline rules. Failure to submit or materially misrepresenting facts results in significant enforcement actions.</p>
                </div>
            </div>
        </div>
    </article>
    '''
}

updated_count = 0
for f in html_files:
    if f == '10k.html':
        continue # Leave 10k intact as it's the valid template
        
    filepath = os.path.join(filings_dir, f)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            
        file_slug = f.replace('.html', '').lower()
        
        # Select appropriate content based on the form
        data = specific_forms.get(file_slug, generic_form)
        
        # Update the TOC
        toc_nav = soup.find('aside', class_='filing-toc')
        if toc_nav:
            nav = toc_nav.find('nav')
            if nav:
                nav.clear()
                # Ensure General Info is still there since we keep that article
                gen_info = soup.new_tag('a', href='#general-info', **{'class': 'active'})
                gen_info.string = "General Information"
                nav.append(gen_info)
                
                for item in data['toc']:
                    tag = soup.new_tag('a', href=f"#{item['id']}")
                    tag.string = item['name']
                    nav.append(tag)
        
        # Now update the content section.
        filing_content = soup.find('div', class_='filing-content fade-in visible')
        
        # It's better to preserve the #general-info article which has the Quick Summary,
        # and remove all the others (#financial-disclosure, #part-i, #part-ii, #part-iii, #part-iv, #signatures).
        # We also want to put the 'signatures' article back if needed.
        if filing_content:
            articles = filing_content.find_all('article', class_='content-section')
            gen_info_article = None
            
            for art in articles:
                if art.get('id') == 'general-info':
                    gen_info_article = art.extract()
                else:
                    art.extract() # Remove all other articles
            
            filing_content.clear()
            
            # Put the general-info back
            if gen_info_article:
                filing_content.append(gen_info_article)
                
            # Parse the new content and append
            new_content_soup = BeautifulSoup(data['content'], 'html.parser')
            for new_art in new_content_soup.find_all('article'):
                filing_content.append(new_art)
                
            # Add signatures if it was in the TOC
            if any(item['id'] == 'signatures' for item in data['toc']):
                sig_art = soup.new_tag('article', **{'class': 'content-section', 'id': 'signatures'})
                h2 = soup.new_tag('h2')
                h2.string = "Signatures"
                art_block = soup.new_tag('div', **{'class': 'article-block dark'})
                p = soup.new_tag('p')
                p.string = "The report must be signed by the registrant and by its authorized officers/directors in accordance with SEC rules."
                art_block.append(p)
                sig_art.append(h2)
                sig_art.append(art_block)
                filing_content.append(sig_art)
                
            with open(filepath, 'w', encoding='utf-8') as out_file:
                out_file.write(str(soup))
            updated_count += 1
            
    except Exception as e:
        print(f"Error processing {f}: {e}")

print(f"Done processing {updated_count} files!")
