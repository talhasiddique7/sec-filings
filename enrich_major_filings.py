import os
from bs4 import BeautifulSoup
import re

def enrich_filing_content():
    base_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings/filings"
    
    # Define enrichment content for major forms with "SEC Expert" tone
    data = {
        "10k.html": {
            "part-i": [
                {"num": "Item 1", "title": "Business", "desc": "A comprehensive narrative of the company's core operations, subsidiaries, and competitive strategy. Focus on revenue drivers, seasonal trends, and intellectual property portfolios that define the company's market position."},
                {"num": "Item 1A", "title": "Risk Factors", "desc": "Critically important section detailing everything from macroeconomic headwinds and regulatory changes to specific operational vulnerabilities. Analysts look here for 'black swan' risks and management's risk mitigation awareness."},
                {"num": "Item 1C", "title": "Cybersecurity", "desc": "New SEC Mandate. Disclosures regarding the registrant's processes for the assessment, identification, and management of material risks from cybersecurity threats, and the board's oversight of these risks."},
                {"num": "Item 2", "title": "Properties", "desc": "Inventory of major physical assets, including headquarters, manufacturing facilities, and real estate. Important for asset-heavy industries to assess capacity and geographical footprint."},
                {"num": "Item 3", "title": "Legal Proceedings", "desc": "Disclosure of significant pending or threatened litigation that could materially impact financial standing. Footnotes here often reveal the true scope of potential liabilities."}
            ],
            "part-ii": [
                {"num": "Item 7", "title": "MD&A", "desc": "Management's Discussion & Analysis. This is the 'soul' of the report where management explains fluctuations in liquidity, capital resources, and results of operations. It connects the dots between the numbers."},
                {"num": "Item 7A", "title": "Market Risk", "desc": "Quantitative and qualitative sensitivity analysis regarding interest rate volatility, currency exchange shifts, and commodity price changes. Essential for modeling risk exposure."},
                {"num": "Item 8", "title": "Financial Statements", "desc": "The audited 'Ground Truth.' Contains the Balance Sheet, Income Statement, Statement of Cash Flows, and the Auditor's Report. This is where precision and regulatory compliance are paramount."},
                {"num": "Item 9A", "title": "Controls & Procedures", "desc": "Management's assessment of internal control over financial reporting (ICFR). A 'material weakness' disclosure here is a massive red flag for accounting integrity."}
            ],
            "part-iii": [
                {"num": "Item 10", "title": "Directors & Governance", "desc": "Details on the Board of Directors, their background, and committee structures. Used to evaluate board independence and corporate governance health."},
                {"num": "Item 11", "title": "Executive Pay", "desc": "Full disclosure of compensation for Named Executive Officers (NEOs). Shows the alignment between executive incentives and shareholder value creation."},
                {"num": "Item 12", "title": "Security Ownership", "desc": "Table showing how much stock is held by insiders and 5% beneficial owners. High insider ownership often signals long-term alignment with shareholders."}
            ]
        },
        "10q.html": {
            "part-i": [
                {"num": "Item 1", "title": "Financial Statements", "desc": "Unaudited interim financials providing a snapshot of the most recent 3 and 9-month periods. Used to track quarterly momentum and margin trends."},
                {"num": "Item 2", "title": "MD&A", "desc": "Quarterly narrative update on performance. Analysts compare this line-by-line with the previous 10-Q to find subtle shifts in management's tone or business outlook."},
                {"num": "Item 3", "title": "Market Risk", "desc": "Reports any material changes in market risk since the last 10-K. Crucial during periods of rapid interest rate or currency fluctuations."}
            ],
            "part-ii": [
                {"num": "Item 1", "title": "Legal Proceedings", "desc": "Updates on material litigation. New lawsuits or settlements that occurred during the quarter are disclosed here first."},
                {"num": "Item 1A", "title": "Risk Factors", "desc": "Specifically notes any new risks that have emerged since the annual report. Helps investors stay current on evolving threat landscapes."},
                {"num": "Item 2", "title": "Unregistered Sales", "desc": "Reports any equity sold without SEC registration (e.g., private placements), which can signal upcoming dilution or capital needs."}
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
        "3.html": {
            "key-components": [
                {"num": "Ownership", "title": "Initial Holdings", "desc": "Baseline table showing every share and derivative owned by an insider the moment they reach 'insider' status."},
                {"num": "Relationship", "title": "Insider Role", "desc": "Explicitly defines the filer's position (Director, CEO, 10% Owner) and the date they reached that status."},
                {"num": "Sign-off", "title": "Attestation", "desc": "Formal signature confirming the accuracy of the baseline ownership data provided to the SEC."}
            ]
        },
        "5.html": {
            "key-components": [
                {"num": "Annual", "title": "Cleanup Reporting", "desc": "Captures small transactions like gifts or late-reported trades that were exempt from immediate Form 4 filing."},
                {"num": "Gifts", "title": "Charitable Giving", "desc": "The primary way insiders report stock donations to non-profits, which are exempt from Rule 16(b) short-swing profit rules."},
                {"num": "Accuracy", "title": "Verification", "desc": "Ensures the 'Total Holdings' column matches the company's internal registrar records at fiscal year-end."}
            ]
        },
        "s1.html": {
            "prospectus-summary": [
                {"num": "Prospectus", "title": "Summary", "desc": "The 'hook' of the IPO. Provides an overview of the business model and growth strategy."},
                {"num": "Risk", "title": "Risk Factors", "desc": "Exhaustive list of material risks that could negatively impact the company's business or stock price."},
                {"num": "Proceeds", "title": "Use of Proceeds", "desc": "Details how the IPO capital will be spent—e.g., paying down debt or funding R&D."},
                {"num": "Capital", "title": "Dilution", "desc": "Reveals the gap between what public investors pay per share and the 'net tangible book value' paid by early insiders."}
            ]
        },
        "f1.html": {
            "key-components": [
                {"num": "Home", "title": "Local Market Info", "desc": "Unique disclosures regarding the company's primary listing in its home country and local regulatory requirements."},
                {"num": "FX", "title": "Currency Exposure", "desc": "Detailed analysis of how exchange rate fluctuations will impact the US dollar value of ADR shares and dividends."},
                {"num": "GAAP", "title": "US Reconciliation", "desc": "Essential table reconciling foreign accounting profits to US GAAP standards, allowing direct comparison with US companies."}
            ]
        },
        "s3.html": {
            "key-components": [
                {"num": "Shelf", "title": "The Overhang", "desc": "Specifies the total dollar amount or share count the company intends to issue over the next 3 years."},
                {"num": "ATM", "title": "Market Sales", "desc": "Often used to establish 'At-the-Market' programs where the company drips shares into the market during high-volume rallies."},
                {"num": "WKSI", "title": "Status", "desc": "Confirms if the company is a Well-Known Seasoned Issuer, allowing for automatic, unreviewed effectiveness of the registration."}
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
        "13fhr.html": {
            "key-components": [
                {"num": "Holdings", "title": "Institutional Table", "desc": "The primary data table listing every US-listed security held by the fund manager, including share count and market value."},
                {"num": "Value", "title": "Market Value", "desc": "Reports the total value of the positions in thousands of dollars, used to calculate the 'AUM' (Assets Under Management) of the firm."},
                {"num": "Change", "title": "Sequential Analysis", "desc": "By comparing with the prior 13F-HR, analysts identify 'New Positions' and 'Exited Positions,' or where a manager is significantly increasing their stake."}
            ]
        },
        "sc13d.html": {
            "key-components": [
                {"num": "Item 4", "title": "Purpose", "desc": "The activist's manifesto. Discloses intent to influence strategy, seek board seats, or force a merger/sale of the company."},
                {"num": "Item 3", "title": "Source of Funds", "desc": "Reveals if the investor is using their own capital or borrowed funds (margin) to mount an activist campaign."},
                {"num": "Item 6", "title": "Contracts", "desc": "Details side agreements, swaps, or hedges that aren't visible on the surface of the share count."}
            ]
        },
        "sc13g.html": {
            "key-components": [
                {"num": "Passive", "title": "No-Intent Rule", "desc": "Confirms the 5% holder has no intent to influence control, certifying their role as a purely passive institutional partner."},
                {"num": "Group", "title": "Joint Filing", "desc": "Used when multiple entities (e.g., Vanguard and its subsidiaries) file together to report a combined 5% stake."},
                {"num": "Percent", "title": "Ownership %", "desc": "Calculates the exact percentage of the company's common stock owned, informing market liquidity analysis."}
            ]
        },
        "def14a.html": {
            "general-info": [
                {"num": "Pay", "title": "Executive Comp (CD&A)", "desc": "The most detailed explanation of why executives are paid what they are. Includes the Summary Compensation Table and performance metrics used for bonuses."},
                {"num": "Board", "title": "Director Nominees", "desc": "Biographies and qualifications of the board. Used by proxy advisory firms to issue 'vote for' or 'withhold' recommendations."},
                {"num": "Votes", "title": "Shareholder Proposals", "desc": "Items submitted by shareholders (environmental goals, lobbying disclosure, etc.) that the company is forced to put to a formal vote."}
            ]
        },
        "defa14a.html": {
            "key-components": [
                {"num": "Battle", "title": "Proxy Fight Buffer", "desc": "Additional materials sent to shareholders to counter activist arguments or reinforce management's position before the vote."},
                {"num": "ISS", "title": "Glass Lewis Reply", "desc": "Often contains management's rebuttal to negative recommendations from proxy advisory firms regarding board seats or executive pay."},
                {"num": "Reminder", "title": "Urgency Signal", "desc": "Final 'Get Out the Vote' materials aimed at retail investors, often signaling a close vote on critical governance issues."}
            ]
        },
        "20f.html": {
            "key-components": [
                {"num": "Item 3.D", "title": "Risk Factors", "desc": "Critical disclosure of risks specific to the foreign issuer, including currency volatility, local political stability, and international regulatory shifts."},
                {"num": "Item 5", "title": "Operating Review", "desc": "The foreign equivalent of MD&A. Management explains financial results under IFRS or local GAAP and provides a reconciliation to US GAAP metrics."},
                {"num": "Item 8", "title": "Financial Info", "desc": "Audited semi-annual or annual financials. This section is the primary source for evaluating the creditworthiness and profitability of international ADR stocks."},
                {"num": "Item 16", "title": "Governance", "desc": "Discloses any significant differences between the company's home-country governance practices and the NYSE/Nasdaq standards for US firms."}
            ]
        },
        "6k.html": {
            "key-components": [
                {"num": "Exhibit 1", "title": "Material Events", "desc": "Contains the text of press releases, shareholder circulars, or home-country regulatory filings that are deemed material to US investors."},
                {"num": "Interims", "title": "Interim Financials", "desc": "Provides unaudited quarterly or semi-annual results that are not available through 10-Q filings for foreign private issuers."},
                {"num": "Corporate", "title": "Corporate Actions", "desc": "Updates on dividend declarations, debt issuances, or major leadership changes occurring outside the US jurisdiction."}
            ]
        },
        "s4.html": {
            "key-components": [
                {"num": "History", "title": "Background of Merger", "desc": "A blow-by-blow account of the negotiations, competing bids, and board meetings that led to the acquisition agreement."},
                {"num": "Pro Forma", "title": "Combined Financials", "desc": "Hypothetical financial statements showing how the two companies would have performed as a single entity. Essential for valuation models."},
                {"num": "Opinion", "title": "Fairness Opinion", "desc": "A summary of the valuation analysis performed by investment banks to justify the deal price to shareholders."}
            ]
        },
        "144.html": {
            "key-components": [
                {"num": "Supply", "title": "Intention to Sell", "desc": "Signals that a large block of restricted stock is about to enter the public market, potentially creating a 'supply overhang.'"},
                {"num": "Broker", "title": "Market Maker", "desc": "Identifies the brokerage firm handling the sale, giving a hint as to how the liquidation will be managed."},
                {"num": "Rule 144", "title": "Holding Period", "desc": "Confirms the seller has met the required holding periods (usually 6-12 months) before selling restricted securities."}
            ]
        },
        "sd.html": {
            "key-components": [
                {"num": "Trace", "title": "Origin Inquiry", "desc": "Reasonable Country of Origin Inquiry (RCOI) details where the company attempted to trace conflict minerals to their source mines."},
                {"num": "ESG", "title": "Due Diligence", "desc": "Describes the supply chain framework used (usually OECD) to ensure minerals don't finance African warlords."},
                {"num": "Audit", "title": "Independent Rev.", "desc": "Confirms if an independent private sector audit was required and links to the full Conflict Minerals Report."}
            ]
        },
        "d.html": {
            "key-components": [
                {"num": "Item 6", "title": "Offering Type", "desc": "Specifies which Regulation D exemption (Rule 504, 506(b), 506(c)) the company is using to raise capital legally without SEC registration."},
                {"num": "Item 13", "title": "Offering Amount", "desc": "Discloses the total offering size, how much has already been sold, and the remaining amount to be raised in the private round."},
                {"num": "Item 12", "title": "Sales Commission", "desc": "Reveals the fees paid to finders or placement agents, which can be a signal of how 'expensive' the private capital is to raise."}
            ]
        },
        "ncsr.html": {
            "key-components": [
                {"num": "Schedule", "title": "Full Portfolio", "desc": "Exhaustive list of every security owned by the fund, including asset-backed securities and complex derivatives often hidden in 13Fs."},
                {"num": "Performance", "title": "Manager Review", "desc": "Management's discussion of fund performance, detailing which sectors drove returns and which were a drag on the portfolio."},
                {"num": "Ethics", "title": "Code of Ethics", "desc": "Confirmation that the fund senior officers adhere to strict ethical standards, a key metric for institutional due diligence."}
            ]
        },
        "nport.html": {
            "key-components": [
                {"num": "Liquidity", "title": "Asset Classes", "desc": "Classifies every fund holding into liquidity buckets (Highly Liquid to Illiquid), critical for assessing 'run risk' in mutual funds."},
                {"num": "Flows", "title": "Portfolio Turnover", "desc": "Reports the rate at which the fund is buying and selling securities, informing investors about potential tax inefficiencies or aggressive trading."},
                {"num": "Derivs", "title": "Derivative Risk", "desc": "Detailed breakdown of swaps, futures, and options exposure, providing a true look at the fund's leveraged bets."}
            ]
        },
        "s3asr.html": {
            "key-components": [
                {"num": "Instant", "title": "Pay-as-you-go", "desc": "Special fee structure allowing WKSIs to pay SEC registration fees only when they actually sell the shares, rather than all at once."},
                {"num": "Base", "title": "Core Prospectus", "desc": "The foundational legal document describing the company's business and the general types of securities it may offer under the shelf."},
                {"num": "Supp", "title": "Prospectus Supp", "desc": "The document filed at the time of an actual sale, specifying the exact price and amount of securities being 'taken off the shelf.'"}
            ]
        },
        "n1a.html": {
            "key-components": [
                {"num": "Strategy", "title": "Investment Objective", "desc": "Explicitly states the fund's goal (e.g., long-term capital appreciation) and the primary types of securities it buys to achieve it."},
                {"num": "Fees", "title": "Expense Ratio", "desc": "The most important section for mutual fund investors. Breaks down management fees, 12b-1 distribution fees, and Total Annual Operating Expenses."},
                {"num": "Risks", "title": "Principal Risks", "desc": "Details risks specific to the fund's strategy, such as interest rate risk for bond funds or sector concentration risk for specialty funds."}
            ]
        },
        "s8.html": {
            "key-components": [
                {"num": "Plan", "title": "Employee Stock Plan", "desc": "Registers securities offered to employees and consultants via stock option plans, RSUs, or 401(k) programs."},
                {"num": "Shares", "title": "Share Reserve", "desc": "Specifies the number of shares being registered for issuance under the plan, indicating future potential dilution as options vest."},
                {"num": "Expert", "title": "Legal Opinion", "desc": "Confirms the legality of the shares being issued and their status as fully paid and non-assessable securities."}
            ]
        },
        "424b4.html": {
            "key-components": [
                {"num": "Price", "title": "Offering Terms", "desc": "The final prospectus for an IPO or secondary offering. Discloses the definitive price per share and the total proceeds being raised."},
                {"num": "Use", "title": "Use of Proceeds", "desc": "Provides a specific breakdown of how the millions of dollars raised will be allocated (e.g., funding a specific acquisition or debt retirement)."},
                {"num": "Lockup", "title": "Underwriting", "desc": "Details the agreements that prevent insiders from selling their stock for 180 days post-IPO, preventing immediate massive share dumps."}
            ]
        },
        "adv.html": {
            "key-components": [
                {"num": "AUM", "title": "Assets Managed", "desc": "The 'Report Card' for Investment Advisers. Discloses the total Regulatory Assets Under Management (RAUM) and the number of clients served."},
                {"num": "Strategy", "title": "Fee Structure", "desc": "Breaks down how the adviser gets paid—e.g., percentage of AUM, performance fees, or hourly rates."},
                {"num": "Discipline", "title": "Regulatory History", "desc": "Lists any historical legal or disciplinary actions against the firm or its individuals. Essential for due diligence before hiring an adviser."}
            ]
        },
        "1012b.html": {
            "key-components": [
                {"num": "IPO Alt", "title": "Direct Listing/Spin-off", "desc": "Used by companies becoming SEC reporters without a traditional IPO. Common for spin-offs where a parent company distributes shares to its own holders."},
                {"num": "Business", "title": "Full Disclosure", "desc": "Provides the same depth of business and financial history as an S-1, ensuring the market has a complete record before trading begins on an exchange."},
                {"num": "Audit", "title": "Audited Financials", "desc": "Requires 3 years of audited financials, providing the baseline for future 10-K and 10-Q reporting as a public company."}
            ]
        }
    }

    def update_section(soup, filename, section_id, items):
        section = soup.find('article', id=section_id)
        
        # If section doesn't exist, try to create it after general-info
        if not section:
            gen_info = soup.find('article', id='general-info')
            if gen_info:
                new_section = soup.new_tag('article', **{'class': 'content-section', 'id': section_id})
                header = soup.new_tag('div', **{'class': 'part-header'})
                header.string = "ENRICHED DETAILS"
                new_section.append(header)
                h2 = soup.new_tag('h2')
                h2.string = "Key Form Components"
                new_section.append(h2)
                p_intro = soup.new_tag('p', **{'class': 'section-intro'})
                p_intro.string = "Deep-dive details regarding the specific regulatory requirements and analytical focuses for this filing:"
                new_section.append(p_intro)
                grid = soup.new_tag('div', **{'class': 'item-grid'})
                new_section.append(grid)
                gen_info.insert_after(new_section)
                section = new_section
        
        if not section: return False
        
        grid = section.find('div', class_='item-grid')
        rows = section.find('div', class_='article-block')
        
        if grid:
            grid.clear()
            for item in items:
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
        elif rows:
            # Handle item-row structure often found in Part III
            existing_rows = rows.find_all('div', class_='item-row')
            if existing_rows:
                rows.clear()
                for item in items:
                    row = soup.new_tag('div', **{'class': 'item-row'})
                    tag = soup.new_tag('div', **{'class': 'item-num-tag'})
                    tag.string = item['num']
                    row.append(tag)
                    detail = soup.new_tag('div', **{'class': 'item-detail'})
                    h3 = soup.new_tag('h3')
                    h3.string = item['title']
                    detail.append(h3)
                    p = soup.new_tag('p')
                    p.string = item['desc']
                    detail.append(p)
                    row.append(detail)
                    rows.append(row)
                return True
        return False

    for filename, sections in data.items():
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename} (not found)")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        updated = False
        for section_id, items in sections.items():
            if update_section(soup, filename, section_id, items):
                updated = True
        
        if updated:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Enriched Items in {filename}")

if __name__ == "__main__":
    enrich_filing_content()
