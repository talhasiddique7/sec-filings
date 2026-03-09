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
  var resultCount = document.getElementById('result-count');
  var faqItems = document.querySelectorAll('.faq-item');
  var fadeElements = document.querySelectorAll('.fade-in');
  var navAnchors = document.querySelectorAll('.nav-links a');
  var tableRows = filingsTable ? filingsTable.querySelectorAll('tbody tr') : [];

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
    var visibleCount = 0;

    tableRows.forEach(function (row) {
      var category = row.getAttribute('data-category') || '';
      var text = row.textContent.toLowerCase();
      var matchesFilter = activeFilter === 'all' || category === activeFilter;
      var matchesSearch = !query || text.indexOf(query) !== -1;
      var show = matchesFilter && matchesSearch;
      row.style.display = show ? '' : 'none';
      if (show) visibleCount++;

      // Highlight matching text
      var cells = row.querySelectorAll('td');
      cells.forEach(function (cell) {
        highlightText(cell, query);
      });
    });

    if (resultCount) {
      if (query || activeFilter !== 'all') {
        resultCount.textContent = visibleCount + ' of ' + tableRows.length + ' forms shown';
      } else {
        resultCount.textContent = '';
      }
    }
  }

  if (tableSearch) {
    tableSearch.addEventListener('input', filterTable);
  }

  if (filterPills) {
    filterPills.addEventListener('click', function (e) {
      var pill = e.target.closest('.filter-pill');
      if (!pill) return;
      activeFilter = pill.getAttribute('data-filter') || 'all';
      filterPills.querySelectorAll('.filter-pill').forEach(function (p) {
        p.classList.toggle('active', p === pill);
      });
      filterTable();
    });
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
      threshold: 0.1,
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
      link: "filings/10k.html"
    },
    {
      id: "10-q",
      class: "cyan",
      title: "Form 10-Q — Quarterly Snapshot",
      desc: "Understand a company's ongoing financial health. Form 10-Q provides regular, unaudited quarterly check-ups to track working capital, risk shifts, and legal updates.",
      tags: ["Q1-Q3 Updates", "Interim Financials", "Timely Disclosures"],
      link: "filings/10q.html"
    },
    {
      id: "8-k",
      class: "purple",
      title: "Form 8-K — Material Events",
      desc: "Stay ahead of the market. The Form 8-K alerts investors to unscheduled material events such as bankruptcies, executive departures, asset acquisitions, and M&A.",
      tags: ["Event-Driven", "4 Day Deadline", "Market Mover"],
      link: "filings/8k.html"
    },
    {
      id: "13F",
      class: "green",
      title: "Form 13F — Institutional Holdings",
      desc: "Track the smart money. Learn how to decode Form 13F filings from institutional managers holding over $100M+ to identify high conviction trades.",
      tags: ["Smart Money", "Hedge Funds", "Portfolio Trackers"],
      link: "filings/13f.html"
    }
  ];

  const featWrapper = document.getElementById('featured-content-wrapper');
  const featIcon = document.getElementById('feat-icon');
  const featTitle = document.getElementById('feat-title');
  const featDesc = document.getElementById('feat-desc');
  const featTags = document.getElementById('feat-tags');
  const featLink = document.getElementById('feat-link');
  const featProgress = document.getElementById('feat-progress');

  if (featWrapper && featIcon && featTitle && featDesc && featTags && featLink && featProgress) {
    let currentIndex = 0;
    const rotateInterval = 5000;
    let progressInterval = 100; // Update progress bar every 100ms
    let currentProgress = 0;
    
    function cycleFeaturedFiling() {
      // Start fade out animation
      featWrapper.classList.add('animating-out');
      
      setTimeout(() => {
        // Move index
        currentIndex = (currentIndex + 1) % featuredData.length;
        const nextData = featuredData[currentIndex];
        
        // Swap content while hidden
        featIcon.textContent = nextData.id;
        featIcon.className = `filing-card-icon ${nextData.class}`;
        featTitle.textContent = nextData.title;
        featDesc.textContent = nextData.desc;
        featLink.setAttribute("href", nextData.link);
        
        featTags.innerHTML = nextData.tags.map(tag => `<span class="tag">${tag}</span>`).join("");

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
