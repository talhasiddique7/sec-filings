import os
from bs4 import BeautifulSoup
import re

def enrich_filing_content():
    base_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/filings"
    
    # Define enrichment content for major forms
    data = {
        "10k.html": {
            "part-i": [
                {"num": "Item 1", "title": "Business", "desc": "Detailed overview of the company's primary operations, products, services, target markets, and competitive position."},
                {"num": "Item 1A", "title": "Risk Factors", "desc": "A comprehensive list of material risks that could negatively affect the business, financial condition, or stock price."},
                {"num": "Item 1C", "title": "Cybersecurity", "desc": "New SEC requirement. Describes the company’s processes for managing material risks from cybersecurity threats."},
                {"num": "Item 2", "title": "Properties", "desc": "Details regarding the location and nature of the company's significant physical assets and real estate."},
                {"num": "Item 3", "title": "Legal Proceedings", "desc": "Information on significant pending or threatened lawsuits or government investigations."}
            ],
            "part-ii": [
                {"num": "Item 7", "title": "MD&A", "desc": "Management's Discussion & Analysis. A narrative explaining the financial results, year-over-year changes, and liquidity."},
                {"num": "Item 7A", "title": "Market Risk", "desc": "Quantitative and qualitative disclosures about the company's exposure to interest rate and currency volatility."},
                {"num": "Item 8", "title": "Financial Statements", "desc": "The core audited financial records: Balance Sheet, Income Statement, and Cash Flow Statement."},
                {"num": "Item 9A", "title": "Controls & Procedures", "desc": "Management’s assessment of the effectiveness of internal control over financial reporting (ICFR)."}
            ]
        },
        "10q.html": {
            "part-i": [
                {"num": "Item 1", "title": "Financial Statements", "desc": "Unaudited interim financial statements for the most recent quarter and year-to-date period."},
                {"num": "Item 2", "title": "MD&A", "desc": "Quarterly Management's Discussion & Analysis. Focuses on significant shifts in financial condition since year-end."},
                {"num": "Item 3", "title": "Market Risk", "desc": "Updates on the company's exposure to market risks if significant changes occurred during the quarter."},
                {"num": "Item 4", "title": "Controls", "desc": "Maintenance of effective disclosure controls and procedures during the quarter."}
            ],
            "part-ii": [
                {"num": "Item 1", "title": "Legal Proceedings", "desc": "Updates on material legal matters that were previously disclosed or new proceedings."},
                {"num": "Item 1A", "title": "Risk Factors", "desc": "Significant changes or updates to the risk factors previously disclosed in the annual 10-K report."},
                {"num": "Item 2", "title": "Unregistered Sales", "desc": "Details regarding equity securities sold by the company that were not registered under the Securities Act."},
                {"num": "Item 6", "title": "Exhibits", "desc": "A list of required certificates and material contracts filed with this quarterly report."}
            ]
        },
        "8k.html": {
            "events": [
                {"num": "Item 1.01", "title": "Material Agreements", "desc": "Entry into a material definitive agreement (M&A, credit facilities) not made in the ordinary course of business."},
                {"num": "Item 2.02", "title": "Earnings Releases", "desc": "Public announcement of financial results. Usually includes an attached press release as Exhibit 99.1."},
                {"num": "Item 5.02", "title": "Leadership Changes", "desc": "Departure, election, or appointment of directors or certain executive officers."},
                {"num": "Item 7.01", "title": "Regulation FD", "desc": "Disclosures made to satisfy fair disclosure requirements, often used for investor presentations."},
                {"num": "Item 8.01", "title": "Other Events", "desc": "Any other material events that the company deems important to shareholders."},
                {"num": "Item 9.01", "title": "Financial Exhibits", "desc": "Financial statements of businesses acquired, pro forma info, and the list of exhibits."}
            ]
        },
        "4.html": {
            "key-components": [
                {"num": "Table I", "title": "Direct Securities", "desc": "Reports transactions in direct equity, such as common stock. Shows shares bought, sold, or gifted."},
                {"num": "Table II", "title": "Derivatives", "desc": "Reports transactions in stock options or warrants. Includes strike prices and expiration dates."},
                {"num": "Explanation", "title": "Footnotes", "desc": "Critical context. Explains the nature of the transaction, such as price ranges or Rule 10b5-1 plans."},
                {"num": "Codes", "title": "Transaction Codes", "desc": "Standardized codes (P=Purchase, S=Sale, A=Grant, M=Exercise) defining the insider's action."}
            ]
        },
        "s1.html": {
            "prospectus-summary": [
                {"num": "Prospectus", "title": "Summary", "desc": "The 'hook' of the IPO. Provides an overview of the business model and growth strategy."},
                {"num": "Risk", "title": "Risk Factors", "desc": "Exhaustive list of material risks that could negatively impact the company's business or stock price."},
                {"num": "Proceeds", "title": "Use of Proceeds", "desc": "Details how the IPO capital will be spent—e.g., paying down debt or funding R&D."}
            ]
        },
        "13f.html": {
            "general-info": [
                {"num": "List", "title": "List of Holdings", "desc": "Detailed table of all Section 13(f) securities (US-listed stocks) held at the end of the quarter."},
                {"num": "Shares", "title": "Share Count", "desc": "Reports the total number of shares held and the market value as of the last trading day."},
                {"num": "Authority", "title": "Investment Discretion", "desc": "Indicates whether the manager has sole, shared, or no investment discretion."},
                {"num": "Voting", "title": "Voting Authority", "desc": "Discloses how much voting power the manager has over corporate actions."}
            ]
        },
        "def14a.html": {
            "general-info": [
                {"num": "Notice", "title": "Meeting Notice", "desc": "Announcement of the date, time, and location of the annual shareholder meeting."},
                {"num": "Proposals", "title": "Voting Proposals", "desc": "Detailed breakdown of items for vote, including director elections and 'Say-on-Pay'."},
                {"num": "Ownership", "title": "Ownership Table", "desc": "Lists the stock holdings of all directors, executive officers, and 5% beneficial owners."},
                {"num": "Pay", "title": "Executive Pay (CD&A)", "desc": "Explains the company’s pay-for-performance philosophy and justifies executive compensation."}
            ]
        }
    }

    def update_grid(soup, section_id, content_list):
        section = soup.find('article', id=section_id)
        if not section: return False
        
        grid = section.find('div', class_='item-grid')
        if not grid:
            grid = section.find('div', class_='article-block')
            if not grid: return False
        
        grid.clear()
        for item in content_list:
            card = soup.new_tag('div', **{'class': 'item-card'})
            num = soup.new_tag('span', **{'class': 'item-num'})
            num.string = item['num']
            card.append(num)
            h3 = soup.new_tag('h3')
            h3.string = item['title']
            card.append(h3)
            wrapper = soup.new_tag('div', **{'class': 'truncate-wrapper'})
            p = soup.new_tag('p', **{'class': 'truncate-text'})
            p.string = item['desc']
            wrapper.append(p)
            btn = soup.new_tag('button', **{'class': 'read-more-btn', 'type': 'button', 'onclick': 'toggleReadMore(this)'})
            btn.string = "Read more"
            wrapper.append(btn)
            card.append(wrapper)
            grid.append(card)
        return True

    for filename, sections in data.items():
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath): continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        updated = False
        for section_id, content in sections.items():
            if update_grid(soup, section_id, content):
                updated = True
        
        if updated:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Enriched {filename}")

if __name__ == "__main__":
    enrich_filing_content()
