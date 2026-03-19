# SEC Filings Guide

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://html.spec.whatwg.org/)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://www.w3.org/Style/CSS/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

A comprehensive, educational web application that demystifies SEC filings for investors, analysts, and financial professionals. Built with modern web technologies and powered by authoritative SEC data.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Scripts](#-scripts)
- [Contributing](#-contributing)
- [Data Sources](#-data-sources)
- [License](#-license)
- [Support](#-support)

## 🎯 Overview

The SEC Filings Guide is an interactive, single-page web application that provides detailed explanations of every major SEC filing form. From the ubiquitous Form 10-K to niche filings like Form 13F, this guide helps users understand:

- **What** each form requires and why it exists
- **Who** must file it and when
- **How** to interpret the information for investment decisions
- **Where** to find filings on EDGAR

Perfect for individual investors, financial analysts, compliance officers, and anyone working with corporate financial disclosures.

## ✨ Features

### 📊 Comprehensive Form Coverage
- **93+ SEC forms** documented with detailed explanations
- **Interactive table** with search and filtering capabilities
- **Individual form pages** with deep dives into structure and requirements

### 🎨 Modern User Experience
- **Responsive design** that works on desktop, tablet, and mobile
- **Dark/light theme toggle** for comfortable reading
- **Fast search** across all forms and content
- **Smooth animations** and intuitive navigation

### 📈 Educational Content
- **Key takeaways** for major forms (10-K, 10-Q, 8-K, etc.)
- **Investor insights** and practical applications
- **Regulatory context** and compliance requirements
- **Comparison tools** between similar forms

### 🔧 Developer-Friendly
- **Modular architecture** with separate scripts and assets
- **Automated content generation** from structured data
- **Version-controlled** with comprehensive build tools

## 🚀 Quick Start

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No server required - runs entirely in the browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/talhasiddique7/sec-filings.git
   cd sec-filings
   ```

2. **Open in browser**
   ```bash
   # Simply open index.html in your browser
   open index.html
   # Or use a local server for better development experience
   python -m http.server 8000
   ```

3. **Start exploring!**
   - Browse the overview section
   - Use the search to find specific forms
   - Click on any form for detailed information

## 📁 Project Structure

```
sec-filings/
├── index.html              # Main application page
├── styles.css              # Styling and responsive design
├── script.js               # Client-side interactivity
├── 404.html                # Error page
├── generated_rows.html     # Auto-generated table content
├── assets/                 # Data and static assets
│   ├── data.json          # Form definitions and metadata
│   ├── data_full.json     # Complete form database
│   ├── pdf_mapping.json   # PDF link mappings
│   └── SEC EDGAR All filling type.xlsx  # Source data
├── scripts/                # Python build and maintenance tools
│   ├── generate_html.py   # Generate table rows from data
│   ├── update_filings.py  # Update individual form pages
│   ├── add_read_more.py   # Add truncation controls
│   └── ... (37 additional scripts)
├── filings/                # Individual form detail pages
│   ├── 10k.html          # Form 10-K page
│   ├── 10q.html          # Form 10-Q page
│   ├── 8k.html           # Form 8-K page
│   └── ... (147+ form pages)
└── sec_pdfs/              # SEC form PDF references
    ├── 0012_01_current-report-pursuant-to-section-13-or-15d_form8-k.pdf
    └── ... (additional PDFs)
```

## 🛠 Development

### Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Typography**: Google Fonts (DM Serif Display + Inter)
- **Build Tools**: Python 3.x scripts for content generation
- **Data Format**: JSON for structured form information
- **Styling**: Custom CSS with CSS Variables for theming

### Development Setup

1. **Install Python dependencies** (if running build scripts)
   ```bash
   # Python scripts use only standard library
   # No additional dependencies required
   ```

2. **Run build scripts**
   ```bash
   # Generate table content from data
   python scripts/generate_html.py

   # Update individual form pages
   python scripts/update_filings.py

   # Add read-more functionality
   python scripts/add_read_more.py
   ```

3. **Development workflow**
   - Edit data in `assets/data.json`
   - Run `python scripts/generate_html.py` to update table
   - Run `python scripts/update_filings.py` to sync individual pages
   - Test changes in browser

### Key Scripts

| Script | Purpose |
|--------|---------|
| `generate_html.py` | Generate table rows from JSON data |
| `update_filings.py` | Sync individual form pages with data |
| `add_read_more.py` | Add truncation controls to long content |
| `remove_short_read_more.py` | Remove unnecessary truncation |
| `verify_consistency.py` | Check data integrity and links |

## 🤝 Contributing

We welcome contributions! Here's how to get involved:

### For Content Contributors
1. **Data updates**: Edit `assets/data.json` with new form information
2. **Content improvements**: Update form descriptions and insights
3. **Bug fixes**: Report issues or submit pull requests

### For Developers
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-form`
3. **Make changes** and test thoroughly
4. **Run build scripts** to ensure consistency
5. **Submit a pull request** with detailed description

### Guidelines
- **Data accuracy**: All form information must be verified against SEC sources
- **Consistency**: Follow existing JSON structure and naming conventions
- **Testing**: Test changes across different browsers and devices
- **Documentation**: Update this README for any structural changes

## 📚 Data Sources

This project draws from authoritative SEC and financial industry sources:

- **U.S. Securities and Exchange Commission (SEC)** - Official form definitions and requirements
- **EDGAR database** - Filing examples and historical data
- **DFIN (Donnelley Financial Solutions)** - Compliance guidance and form explanations
- **Financial Industry Regulatory Authority (FINRA)** - Additional regulatory context

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check this README and inline code comments
- **Issues**: [GitHub Issues](https://github.com/talhasiddique7/sec-filings/issues)
- **Discussions**: [GitHub Discussions](https://github.com/talhasiddique7/sec-filings/discussions)

### Common Issues
- **Page not loading**: Ensure you're opening `index.html` directly in a browser
- **Search not working**: Check browser console for JavaScript errors
- **Content outdated**: Run `python scripts/generate_html.py` to refresh

### Contact
- **Project Owner**: [Talha Siddique](https://github.com/talhasiddique7)
- **Repository**: [sec-filings](https://github.com/talhasiddique7/sec-filings)

---

**Disclaimer**: This educational resource is not legal or financial advice. Always consult with qualified professionals and refer to official SEC sources for compliance matters.
