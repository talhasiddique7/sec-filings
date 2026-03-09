(function () {
  'use strict';

  // ===== DOM REFERENCES =====
  var header = document.getElementById('site-header');
  var navLinks = document.getElementById('nav-links');
  var mobileToggle = document.getElementById('mobile-toggle');
  var backToTop = document.getElementById('back-to-top');
  var heroSearchInput = document.getElementById('hero-search-input');
  var heroSearchBtn = document.getElementById('hero-search-btn');
  var tableSearch = document.getElementById('table-search');
  var filingsTable = document.getElementById('filings-table');
  var filterPills = document.getElementById('filter-pills');
  var showAllFilingsBtn = document.getElementById('show-all-filings');
  var resultCount = document.getElementById('result-count');
  var tablePagination = document.getElementById('table-pagination');
  var paginationPrev = document.getElementById('pagination-prev');
  var paginationNext = document.getElementById('pagination-next');
  var paginationPages = document.getElementById('pagination-pages');
  var faqItems = document.querySelectorAll('.faq-item');
  var fadeElements = document.querySelectorAll('.fade-in');
  var navAnchors = document.querySelectorAll('.nav-links a');
  var tableRows = filingsTable ? filingsTable.querySelectorAll('tbody tr') : [];
  var themeToggle = document.getElementById('theme-toggle');
  var root = document.documentElement;

  // ===== THEME SUPPORT =====
  function setTheme(theme) {
    if (theme === 'light') {
      root.setAttribute('data-theme', 'light');
    } else {
      root.removeAttribute('data-theme');
    }
    localStorage.setItem('sec-filing-theme', theme);
  }

  // Initial Theme Load
  var savedTheme = localStorage.getItem('sec-filing-theme');
  var systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  if (savedTheme) {
    setTheme(savedTheme);
  } else if (!systemDark) {
    setTheme('light');
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var isLight = root.getAttribute('data-theme') === 'light';
      setTheme(isLight ? 'dark' : 'light');
    });
  }

  // ===== STICKY HEADER =====
  var lastScroll = 0;
  function handleScroll() {
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;
    if (header) {
      header.classList.toggle('scrolled', scrollY > 50);
    }
    if (backToTop) {
      backToTop.classList.toggle('visible', scrollY > 600);
    }
    lastScroll = scrollY;
  }
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  // ===== MOBILE NAV TOGGLE =====
  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', function () {
      navLinks.classList.toggle('open');
    });
    // Close on link click
    navLinks.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        navLinks.classList.remove('open');
      }
    });
  }

  // ===== BACK TO TOP =====
  if (backToTop) {
    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ===== ACTIVE NAV HIGHLIGHTING =====
  var sections = [];
  navAnchors.forEach(function (a) {
    var href = a.getAttribute('href');
    if (href && href.startsWith('#')) {
      var el = document.querySelector(href);
      if (el) sections.push({ link: a, el: el });
    }
  });

  function updateActiveNav() {
    var scrollY = window.pageYOffset + 120;
    var current = null;
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].el.offsetTop <= scrollY) {
        current = sections[i].link;
      }
    }
    navAnchors.forEach(function (a) { a.classList.remove('active'); });
    if (current) current.classList.add('active');
  }
  window.addEventListener('scroll', updateActiveNav, { passive: true });
  updateActiveNav();

  // ===== HERO SEARCH → TABLE SEARCH =====
  if (heroSearchBtn && heroSearchInput && tableSearch) {
    heroSearchBtn.addEventListener('click', function () {
      var query = heroSearchInput.value.trim();
      if (query) {
        document.getElementById('search-filings').scrollIntoView({ behavior: 'smooth' });
        setTimeout(function () {
          tableSearch.value = query;
          tableSearch.dispatchEvent(new Event('input'));
        }, 500);
      }
    });
    heroSearchInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') heroSearchBtn.click();
    });
  }

  // ===== TABLE SEARCH & FILTER =====
  var activeFilter = 'all';
  var currentPage = 1;
  var rowsPerPage = 20;
  var totalPages = 1;

  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function highlightText(cell, query) {
    // Remove existing marks
    var marks = cell.querySelectorAll('mark');
    marks.forEach(function (m) {
      var parent = m.parentNode;
      parent.replaceChild(document.createTextNode(m.textContent), m);
      parent.normalize();
    });

    if (!query) return;

    var walker = document.createTreeWalker(cell, NodeFilter.SHOW_TEXT, null, false);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    var regex = new RegExp('(' + escapeRegex(query) + ')', 'gi');
    nodes.forEach(function (textNode) {
      if (textNode.parentNode.tagName === 'MARK') return;
      if (!regex.test(textNode.nodeValue)) return;
      var span = document.createElement('span');
      span.innerHTML = textNode.nodeValue.replace(regex, '<mark>$1</mark>');
      textNode.parentNode.replaceChild(span, textNode);
    });
  }

  function filterTable() {
    var query = tableSearch ? tableSearch.value.trim().toLowerCase() : '';
    var matchingRows = [];

    tableRows.forEach(function (row) {
      var category = row.getAttribute('data-category') || '';
      var text = ((row.getAttribute('data-search') || '') + ' ' + row.textContent).toLowerCase();
      var matchesFilter = activeFilter === 'all' || category === activeFilter;
      var matchesSearch = !query || text.indexOf(query) !== -1;
      var matches = matchesFilter && matchesSearch;
      if (matches) matchingRows.push(row);

      // Hide first; pagination pass decides what is visible.
      row.style.display = 'none';

      // Highlight matching text
      var cells = row.querySelectorAll('td');
      cells.forEach(function (cell) {
        highlightText(cell, query);
      });
    });

    totalPages = Math.max(1, Math.ceil(matchingRows.length / rowsPerPage));
    if (currentPage > totalPages) currentPage = totalPages;

    var start = (currentPage - 1) * rowsPerPage;
    var end = start + rowsPerPage;
    var pageRows = matchingRows.slice(start, end);
    pageRows.forEach(function (row) {
      row.style.display = '';
    });

    var startLabel = matchingRows.length === 0 ? 0 : start + 1;
    var endLabel = start + pageRows.length;
    if (resultCount) {
      resultCount.textContent = 'Showing ' + startLabel + '-' + endLabel + ' of ' + matchingRows.length + ' matching forms (' + tableRows.length + ' total)';
    }

    renderPagination(matchingRows.length);
  }

  function renderPagination(totalMatches) {
    if (!tablePagination || !paginationPrev || !paginationNext || !paginationPages) return;

    if (totalMatches <= rowsPerPage) {
      tablePagination.style.display = 'none';
      paginationPages.innerHTML = '';
      paginationPrev.disabled = true;
      paginationNext.disabled = true;
      return;
    }

    tablePagination.style.display = 'flex';
    paginationPrev.disabled = currentPage === 1;
    paginationNext.disabled = currentPage === totalPages;

    paginationPages.innerHTML = '';
    for (var page = 1; page <= totalPages; page++) {
      var pageBtn = document.createElement('button');
      pageBtn.type = 'button';
      pageBtn.className = 'pagination-page' + (page === currentPage ? ' active' : '');
      pageBtn.setAttribute('data-page', String(page));
      pageBtn.textContent = String(page);
      paginationPages.appendChild(pageBtn);
    }
  }

  function resetFilingsTable() {
    activeFilter = 'all';
    currentPage = 1;
    if (tableSearch) {
      tableSearch.value = '';
    }
    if (filterPills) {
      filterPills.querySelectorAll('.filter-pill[data-filter]').forEach(function (p) {
        p.classList.toggle('active', p.getAttribute('data-filter') === 'all');
      });
    }
    filterTable();
  }

  if (tableSearch) {
    tableSearch.addEventListener('input', function () {
      currentPage = 1;
      filterTable();
    });
  }

  if (filterPills) {
    filterPills.addEventListener('click', function (e) {
      var pill = e.target.closest('.filter-pill');
      if (!pill || !pill.hasAttribute('data-filter')) return;
      activeFilter = pill.getAttribute('data-filter') || 'all';
      currentPage = 1;
      filterPills.querySelectorAll('.filter-pill').forEach(function (p) {
        p.classList.toggle('active', p === pill);
      });
      filterTable();
    });
  }

  if (paginationPrev) {
    paginationPrev.addEventListener('click', function () {
      if (currentPage <= 1) return;
      currentPage--;
      filterTable();
    });
  }

  if (paginationNext) {
    paginationNext.addEventListener('click', function () {
      if (currentPage >= totalPages) return;
      currentPage++;
      filterTable();
    });
  }

  if (paginationPages) {
    paginationPages.addEventListener('click', function (e) {
      var pageBtn = e.target.closest('.pagination-page');
      if (!pageBtn) return;
      var page = Number(pageBtn.getAttribute('data-page'));
      if (!page || page === currentPage) return;
      currentPage = page;
      filterTable();
    });
  }

  if (showAllFilingsBtn) {
    showAllFilingsBtn.addEventListener('click', resetFilingsTable);
  }

  // Ensure the section always starts in "show all filings" mode.
  if (tableRows.length > 0) {
    resetFilingsTable();
  }

  // ===== FAQ ACCORDION =====
  faqItems.forEach(function (item) {
    var question = item.querySelector('.faq-question');
    if (question) {
      question.addEventListener('click', function () {
        var wasOpen = item.classList.contains('open');
        // Close all
        faqItems.forEach(function (f) { f.classList.remove('open'); });
        // Toggle current
        if (!wasOpen) item.classList.add('open');
      });
    }
  });

  // ===== INTERSECTION OBSERVER — FADE IN =====
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      // Large elements (like the full filings table) may never hit 10% in view on initial load.
      threshold: 0.01,
      rootMargin: '0px 0px -50px 0px'
    });

    fadeElements.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    // Fallback: show all
    fadeElements.forEach(function (el) {
      el.classList.add('visible');
    });
  }

  // ===== DETAIL PAGE TOC HIGHLIGHTING =====
  var tocLinks = document.querySelectorAll('.toc-inner nav a');
  var contentSections = document.querySelectorAll('.content-section');

  if (tocLinks.length > 0 && contentSections.length > 0 && 'IntersectionObserver' in window) {
    var tocObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var id = entry.target.getAttribute('id');
          tocLinks.forEach(function (link) {
            link.classList.toggle('active', link.getAttribute('href') === '#' + id);
          });
        }
      });
    }, {
      threshold: 0.2,
      rootMargin: '-10% 0px -70% 0px'
    });

    contentSections.forEach(function (section) {
      tocObserver.observe(section);
    });
  }

  // ===== FEATURED FILING ROTATION =====
  const featuredData = [
    {
      id: "10-k",
      class: "blue",
      title: "Form 10-K — The Annual Report",
      desc: "Go beyond the summary. Our dedicated Form 10-K guide breaks down all 19 pages of the official SEC requirements, from Item 1 Business descriptions to Item 15 Exhibits.",
      tags: ["Part I-IV", "16 Items Detailed", "Legal Reference"],
      link: "filings/10k.html",
      what: "Comprehensive annual report with audited financial statements, risk factors, MD&A, and business/legal disclosures.",
      who: "Domestic public issuers subject to Exchange Act annual reporting obligations.",
      when: "Annual deadline is tied to filer status under SEC rules (typically 60, 75, or 90 days after fiscal year-end)."
    },
    {
      id: "10-q",
      class: "cyan",
      title: "Form 10-Q — Quarterly Snapshot",
      desc: "Understand a company's ongoing financial health. Form 10-Q provides regular, unaudited quarterly check-ups to track working capital, risk shifts, and legal updates.",
      tags: ["Q1-Q3 Updates", "Interim Financials", "Timely Disclosures"],
      link: "filings/10q.html",
      what: "Quarterly update with unaudited financial statements, management analysis, and material disclosure updates.",
      who: "Reporting companies required to file periodic Exchange Act reports.",
      when: "Filed after each of Q1, Q2, and Q3 based on SEC filer category deadlines."
    },
    {
      id: "8-k",
      class: "purple",
      title: "Form 8-K — Material Events",
      desc: "Stay ahead of the market. The Form 8-K alerts investors to unscheduled material events such as bankruptcies, executive departures, asset acquisitions, and M&A.",
      tags: ["Event-Driven", "4 Day Deadline", "Market Mover"],
      link: "filings/8k.html",
      what: "Current report for material corporate events outside the normal periodic reporting cycle.",
      who: "Issuers that report under Exchange Act Sections 13 or 15(d) when a triggering event occurs.",
      when: "Generally due within four business days of the reportable event, subject to item-specific rules."
    },
    {
      id: "13F",
      class: "green",
      title: "Form 13F — Institutional Holdings",
      desc: "Track the smart money. Learn how to decode Form 13F filings from institutional managers holding over $100M+ to identify high conviction trades.",
      tags: ["Smart Money", "Hedge Funds", "Portfolio Trackers"],
      link: "filings/13f.html",
      what: "Quarterly holdings report showing long positions in SEC-defined 13F securities.",
      who: "Institutional investment managers with discretion over at least $100 million in 13F securities.",
      when: "Due within 45 days after each calendar quarter-end."
    }
  ];

  const featWrapper = document.getElementById('featured-content-wrapper');
  const featIcon = document.getElementById('feat-icon');
  const featTitle = document.getElementById('feat-title');
  const featDesc = document.getElementById('feat-desc');
  const featTags = document.getElementById('feat-tags');
  const featLink = document.getElementById('feat-link');
  const featProgress = document.getElementById('feat-progress');
  const featPreviewWhat = document.getElementById('feat-preview-what');
  const featPreviewWho = document.getElementById('feat-preview-who');
  const featPreviewWhen = document.getElementById('feat-preview-when');

  if (featWrapper && featIcon && featTitle && featDesc && featTags && featLink && featProgress) {
    let currentIndex = 0;
    const rotateInterval = 10000;
    let progressInterval = 100; // Update progress bar every 100ms
    let currentProgress = 0;

    function renderFeaturedContent(data) {
      featIcon.textContent = data.id;
      featIcon.className = `filing-card-icon ${data.class}`;
      featTitle.textContent = data.title;
      featDesc.textContent = data.desc;
      featLink.setAttribute("href", data.link);
      featTags.innerHTML = data.tags.map(tag => `<span class="tag">${tag}</span>`).join("");

      if (featPreviewWhat && featPreviewWho && featPreviewWhen) {
        featPreviewWhat.textContent = data.what;
        featPreviewWho.textContent = data.who;
        featPreviewWhen.textContent = data.when;
      }
    }

    renderFeaturedContent(featuredData[currentIndex]);
    
    function cycleFeaturedFiling() {
      // Start fade out animation
      featWrapper.classList.add('animating-out');
      
      setTimeout(() => {
        // Move index
        currentIndex = (currentIndex + 1) % featuredData.length;
        const nextData = featuredData[currentIndex];
        
        // Swap content while hidden
        renderFeaturedContent(nextData);

        // Switch animation class to slide from right
        featWrapper.classList.remove('animating-out');
        featWrapper.classList.add('animating-in');
        
        // Trigger reflow to apply the animating-in state instantly
        void featWrapper.offsetWidth;
        
        // Finally, remove animating class to fade/slide back to normal position
        featWrapper.classList.remove('animating-in');
        
        // Reset Progress bar
        currentProgress = 0;
        featProgress.style.width = '0%';
        
      }, 500); // Wait half a second for fade out to complete
    }

    // Progress Bar Animation Loop
    setInterval(() => {
      currentProgress += (progressInterval / rotateInterval) * 100;
      if (currentProgress >= 100) {
        cycleFeaturedFiling();
        currentProgress = 0; // Prevent overshooting while waiting for timeout
      } else {
        featProgress.style.width = `${currentProgress}%`;
      }
    }, progressInterval);
  }

})();
