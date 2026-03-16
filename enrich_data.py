
import json
import os

def enrich_data():
    base_dir = r"c:/Users/ahmad/OneDrive/Desktop/Blogs/sec-filings"
    data_path = os.path.join(base_dir, "data.json")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Expert Enrichment Dictionary
    enrichment = {
        "10-K": {
            "what": "The definitive annual report for US public companies. It contains audited financial statements including the Balance Sheet, Income Statement, and Cash Flow Statement. Crucially, it includes the MD&A (Item 7), where management explains the 'why' behind the numbers, and Item 1A (Risk Factors), detailing everything that could go wrong. It also covers legal proceedings, executive compensation, and the effectiveness of internal controls (SOX 404).",
            "why_use_it": "The 10-K is the 'gold standard' for fundamental analysis. It's used to build discounted cash flow (DCF) models, assess long-term competitive moats, and verify the integrity of reported earnings via the auditor's report. Professional analysts skip the investor presentation and go straight to the 10-K to find hidden liabilities, pension obligations, and lease commitments that aren't visible in summary data."
        },
        "10-Q": {
            "what": "A quarterly report filed after each of the first three fiscal quarters. Unlike the 10-K, current quarterly financial statements are typically unaudited. It provides a real-time update on a company's financial health, seasonal trends, and any material developments that occurred since the last annual report. It includes condensed financials and a shorter MD&A focused specifically on the recent quarter's performance.",
            "why_use_it": "Investors use 10-Qs to track short-term momentum and identify 'earnings beats' or 'misses' early. It reveals deteriorating margins or slowing growth trends months before the annual report. Comparing the 10-Q to the previous year's corresponding quarter (YoY) is the standard method for measuring fundamental growth in public markets."
        },
        "8-K": {
            "what": "The 'breaking news' filing. Companies must file an 8-K for 'material' events, often within 4 business days. This includes earnings releases (Item 2.02), entering into major contracts (Item 1.01), CEO or CFO departures (Item 5.02), bankruptcy, or dividend changes. It is the primary vehicle for ensuring all investors have access to market-moving information simultaneously.",
            "why_use_it": "An 8-K is the ultimate catalyst for stock price volatility. Day traders and institutional desks monitor 8-K feeds (Item 99.1 exhibits) for earnings slides and press releases. A sudden 8-K filing can signal a company is about to be acquired, is facing a major lawsuit, or is experiencing a management crisis. It is the most time-sensitive filing on EDGAR."
        },
        "SC 13D": {
            "what": "The Activist Investor's calling card. Filed when an investor (or group) acquires more than 5% of a company with the intent to influence or change control. The most critical section is Item 4: Purpose of Transaction, where the activist must disclose if they want to fire the CEO, sell the company, or demand board seats. Any change in 'intent' requires a prompt amendment.",
            "why_use_it": "A 13D filing is a massive bullish signal. When institutional 'raiders' like Elliott Management or Carl Icahn file a 13D, it implies they believe the stock is undervalued and they will fight to unlock that value. Following 13D filings allows retail investors to 'ride the coattails' of the world's most aggressive and successful hedge fund managers."
        },
        "SC 13G": {
            "what": "The passive version of the 5% ownership report. Filed by large institutional investors (like BlackRock, Vanguard, or State Street) who own over 5% but have 'no intent to influence control.' It is a shorter, more administrative filing than the 13D but still signals significant institutional support and liquidity in the stock.",
            "why_use_it": "Rising 13G filings indicate increasing institutional 'buy-in.' High institutional ownership is generally a sign of stability and reduced volatility. If a 13G filer suddenly starts filing 13D reports, it signals a major shift toward activism and is a significant market event."
        },
        "13F-HR": {
            "what": "A quarterly window into the portfolios of the world's largest investment managers (those with $100M+ in US equities). It lists all long positions, including share counts and market values. High-frequency 13Fs (like those from Renaissance Technologies) or value-focused 13Fs (like Berkshire Hathaway) are dissected by the entire financial community.",
            "why_use_it": "13Fs allow you to see what 'The Smart Money' is doing. You can track which sectors managers are rotating into or witness the exact moment Warren Buffett starts selling a position. Many retail strategies involve 'Copycat Investing,' which replicates the top holdings of elite hedge funds based on their 13F disclosures."
        },
        "DEF 14A": {
            "what": "The 'Proxy Statement' for the annual shareholder meeting. This is where you find the 'real' story of corporate governance. It details the Summary Compensation Table (what the CEO actually made), the background of board members, and any shareholder proposals on the ballot. It also discloses 'Related Person Transactions' where the company might be doing business with an insider's family members.",
            "why_use_it": "Essential for ESG (Environmental, Social, and Governance) analysis. It reveals if a CEO's pay is aligned with performance or if the board is 'entrenched' with long-tenured members who lack independence. Activist campaigns often start by analyzing the DEF 14A for governance weaknesses and excessive perk spending."
        },
        "Form 4": {
            "what": "A report of a change in ownership for corporate insiders (officers, directors, or 10% owners). Most Form 4 filings report open-market buys or sells, but they also cover stock option exercises and RSU vestings. Under SEC rules, these must be filed within 2 business days of the trade.",
            "why_use_it": "The most powerful insider signal. While insiders might sell for many reasons (taxes, diversifying, buying a house), they almost always buy for only one: they think the price is going up. 'Cluster Buying'—where multiple insiders buy stock simultaneously—is one of the most reliable indicators of future outperformance."
        },
        "4": {
            "what": "A report of a change in ownership for corporate insiders (officers, directors, or 10% owners). Most Form 4 filings report open-market buys or sells, but they also cover stock option exercises and RSU vestings. Under SEC rules, these must be filed within 2 business days of the trade.",
            "why_use_it": "The most powerful insider signal. While insiders might sell for many reasons (taxes, diversifying, buying a house), they almost always buy for only one: they think the price is going up. 'Cluster Buying'—where multiple insiders buy stock simultaneously—is one of the most reliable indicators of future outperformance."
        },
        "3": {
            "what": "The initial statement of beneficial ownership. Filed within 10 days of a person becoming an officer, director, or 10% shareholder. It sets the baseline for all future insider trading reports.",
            "why_use_it": "Establishing the baseline ownership levels. Analysts use Form 3 to determine 'day zero' holdings and see if a new executive already has 'skin in the game' through prior equity grants or direct purchases."
        },
        "5": {
            "what": "Annual reconciliation of insider ownership. Reports transactions that were either exempt from Form 4 or failed to be reported on time during the year. Acts as the final cumulative check on insider data.",
            "why_use_it": "A cleanup document. While less market-moving than Form 4, it ensures institutional databases have the correct final share counts for governance and valuation purposes."
        },
        "20-F": {
            "what": "The foreign private issuer's equivalent of a 10-K. It is the primary annual disclosure for non-US companies listed on US exchanges (ADRs). It features audited financials, often under IFRS, and includes a critical mandatory reconciliation to US GAAP for certain items. It also covers business risks, governance, and director backgrounds for international entities like ASML, Alibaba, or Sony.",
            "why_use_it": "The only audited source for ADR stock financials. It allows investors to compare foreign giants against US domestic peers by normalizing financial reporting. Analysts look for unique international risk factors (currency, geopolitical, foreign tax) and 'Material Weaknesses' in internal controls that are more common in non-US firms."
        },
        "6-K": {
            "what": "The 'current report' for foreign private issuers (the international version of an 8-K). It is used to report any material information that a foreign company releases in its home market, to its local exchange, or to its shareholders. This includes everything from quarterly results and debt issuances to major executive changes and M&A activity.",
            "why_use_it": "Essential for tracking the 'intra-year' progress of ADRs. Because foreign companies don't file 10-Qs, the 6-K is the only way to get quarterly or semi-annual performance updates. It is the definitive record of how a foreign company is interacting with its global shareholder base."
        },
        "S-4": {
            "what": "The 'Merger & Acquisition' registration statement. Filed when a company issues new shares to acquire another business. It contains the most detailed information available on a corporate deal, including the 'Background of the Merger' (a secret history of the negotiations) and 'Pro Forma' financials showing what the combined company will look like.",
            "why_use_it": "The deal-maker's bible. Risk arbitrageurs and M&A analysts use the S-4 to determine if a deal is actually good for shareholders. It reveals the 'Fairness Opinion' from investment banks and explains exactly how much dilution current shareholders will face in the acquisition."
        },
        "F-1": {
            "what": "The registration statement for foreign private issuers going public in the US for the first time. It is the international version of the S-1. It provides 3 years of audited financials, business history, and an exhaustive list of risk factors specific to the company's home country and the US listing.",
            "why_use_it": "Crucial for analyzing the 'Cross-Border IPO.' It reveals the capital structure of the foreign entity and how the US ADRs will be backed by the underlying foreign shares. Essential for determining if a high-growth international company has the governance standards necessary for a US listing."
        },
        "424B4": {
            "what": "The 'Final Prospectus' filed after a registration statement (like an S-1 or F-1) has become effective. It is the final version of the IPO or secondary offering document, including the actual final offering price, the exact number of shares sold, and the list of participating underwriters.",
            "why_use_it": "The definitive document for any new stock offering. Unlike the 'Preliminary' (Red Herring) prospectus, the 424B4 is the legally binding final version. Analysts use it to confirm the final valuation and to track the 'Lock-Up' agreements that prevent insiders from selling shares immediately after the IPO."
        },
        "S-1": {
            "what": "The 'Initial Public Offering' (IPO) registration statement. It is the first time a private company pulls back the curtain, disclosing 3 years of audited financials, the full competitive landscape, and every conceivable risk factor. It includes the 'Use of Proceeds' section, explaining how the company plans to spend the IPO cash.",
            "why_use_it": "The S-1 is the definitive guide to a new stock. It helps investors determine if an IPO is a 'hype' play or a sustainable business. Analysts focus on the revenue growth rates, path to profitability, and the 'Dual-Class' share structure which often gives founders total voting control even with a minority of shares."
        },
        "144": {
            "what": "A notice of intended sale of restricted or control securities by an insider. It signals that an executive or major backer (like a VC firm) intends to sell a significant block of shares into the public market. It includes details on the broker and the expected date of sale.",
            "why_use_it": "Used to monitor 'supply overhang.' When a major founder or VC investor files a 144, it can put downward pressure on the stock as the market anticipates a large number of shares being dumped. It is a key tool for avoiding 'liquidity traps' where insider selling overwhelms buyer demand."
        },
        "S-3": {
            "what": "The 'Shelf Registration' statement for seasoned companies. It allows a company to register a large amount of securities (stock, bonds, warrants) in advance and then 'pull them off the shelf' to sell to the public over the next 3 years. It is a short-form registration that incorporates previous filings by reference.",
            "why_use_it": "Every S-3 filing is a potential dilution signal. It means the company is preparing to raise capital. Investors track the 'Shelf Overhang' to see how much new stock could suddenly hit the market. It is the primary vehicle for ATM (At-the-Market) offerings, which allow companies to sell shares directly into daily trading volume."
        },
        "N-1A": {
            "what": "The registration form used by open-end management investment companies (Mutual Funds). It contains the fund's investment objectives, strategies, risks, and a detailed fee table. It is the source document for the fund's statutory prospectus.",
            "why_use_it": "The most important guide for mutual fund investors. It is used to compare 'Expense Ratios' (how much the fund charges you) and to understand exactly what the 'Principal Investment Strategies' are. If a fund claims to be 'ESG' or 'Tech-focused,' the N-1A is where they must legally define those terms."
        },
        "S-8": {
            "what": "A registration statement for securities offered to employees, consultants, or advisors under an employee benefit plan (like an ESOP or 401k). It is used to register shares for stock options and restricted stock units (RSUs).",
            "why_use_it": "Provides a view into the company's employee incentive structure. A large S-8 filing indicates that a significant number of shares are being authorized for employee compensation, which informs analysts about potential future dilution as those options vest and are exercised."
        },
        "SD": {
            "what": "The 'Specialized Disclosure' report, most commonly used for Conflict Minerals disclosures. Companies must disclose if their products contain gold, tin, tungsten, or tantalum sourced from the Democratic Republic of the Congo or adjoining countries.",
            "why_use_it": "The primary data source for ESG (Environmental, Social, and Governance) scores regarding supply chain ethics. Institutional investors use SD filings to ensure the companies they invest in aren't indirectly financing regional conflicts through their mineral procurement."
        },
        "ADV": {
            "what": "The registration form for Investment Advisers. It consists of Part 1 (quantitative data about the firm, assets, and employees) and Part 2 (a narrative brochure describing the firm's services, fees, and disciplinary history).",
            "why_use_it": "Fundamental due diligence for anyone hiring a wealth manager or hedge fund. It reveals the firm's total Assets Under Management (AUM), their fee structure, and most importantly, any 'Disciplinary Events' or legal troubles the firm or its individuals have faced."
        },
        "13F": {
            "what": "The general category for quarterly holdings reports by institutional investment managers with over $100M in US-listed assets. It includes 13F-HR (the holdings report) and 13F-NT (notice of joint filing).",
            "why_use_it": "Tracks the 'Smart Money.' It is the only way for the public to see the long portfolios of hedge funds and institutional giants. Used for copy-trading, sector rotation analysis, and sentiment tracking."
        },
        "DEFA14A": {
            "what": "Additional definitive proxy soliciting materials. These are supplemental documents sent to shareholders after the initial proxy statement (DEF 14A) has been filed. They are often used to respond to activist criticism or urge shareholders to vote in a specific way.",
            "why_use_it": "A signal of a governance battle. If you see many DEFA14A filings, it usually means management is fighting for its life against an activist or a negative vote recommendation from ISS/Glass Lewis. It contains the most aggressive 'persuasion' pieces in the corporate world."
        },
        "1012B": {
            "what": "Initial registration of a class of securities on a national securities exchange under Section 12(b). It is often used for direct listings or spin-offs where a company becomes public without a traditional IPO.",
            "why_use_it": "Marks the birth of a new public entity. Analysts study 1012B filings to understand the capitalization and business health of a spin-off company before its shares start trading independently on the NYSE or Nasdaq."
        },
        "Form D": {
            "what": "A notice of an exempt offering of securities (Private Placement) under Regulation D. It is used by private companies, hedge funds, and venture capital funds to raise capital without a full SEC registration.",
            "why_use_it": "The primary way to track private market funding. Every major VC-backed startup or PE fund raise is captured here. It reveals how much a private company is raising, who the investors are, and the date of the first sale."
        },
        "N-CSR": {
            "what": "Certified Shareholder Report of registered management investment companies (Mutual Funds). It contains the annual or semi-annual report sent to shareholders, including full portfolio holdings and financial statements.",
            "why_use_it": "The audited reality of a mutual fund's performance. While 13Fs only show US long positions, N-CSR shows EVERY holding, including shorts, derivatives, and foreign stocks. It is the most comprehensive look at a fund's actual risk profile."
        },
        "N-PORT": {
            "what": "A monthly report of a fund's portfolio holdings. It provides highly granular data on every position, including valuation, performance attribution, and liquidity characteristics.",
            "why_use_it": "Modern fund tracking. Since it is filed monthly (though only the 3rd month is public), it provides much higher resolution data than the quarterly 13F or semi-annual N-CSR. Essential for high-frequency fund analysis."
        },
        "S-3ASR": {
            "what": "Automatic Shelf Registration for 'Well-Known Seasoned Issuers' (WKSIs). It is a shelf registration that is automatically effective upon filing, meaning the company can sell shares instantly without waiting for SEC review.",
            "why_use_it": "The ultimate institutional capital-raising tool. It signals that a company has such high-quality reporting and market cap that the SEC trusts it to raise billions of dollars at a moment's notice. It is a sign of blue-chip corporate strength."
        }
    }
    
    # Apply enrichment
    count = 0
    for form in data['forms']:
        ft = form['form_type']
        if ft in enrichment:
            form['what'] = enrichment[ft]['what']
            form['why_use_it'] = enrichment[ft]['why_use_it']
            count += 1
            
    # Save back
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Enriched {count} major form types in data.json")

if __name__ == "__main__":
    enrich_data()
