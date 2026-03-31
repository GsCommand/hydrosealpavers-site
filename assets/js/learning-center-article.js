(function () {
  function text(el) {
    return (el && el.textContent ? el.textContent : '').trim();
  }

  function estimateReadTime(contentEl) {
    var words = text(contentEl).split(/\s+/).filter(Boolean).length;
    return Math.max(3, Math.round(words / 220));
  }

  function detectLocation(titleText, bodyText) {
    var combined = (titleText + ' ' + bodyText).toLowerCase();
    if (combined.includes('nocatee')) return 'Nocatee, FL';
    if (combined.includes('ponte vedra')) return 'Ponte Vedra, FL';
    if (combined.includes('jacksonville')) return 'Jacksonville, FL';
    return 'Florida';
  }

  function buildMetaRow(readTime, locationTag) {
    var meta = document.createElement('div');
    meta.className = 'lc-article-meta';
    meta.innerHTML =
      '<span>Updated March 2026</span>' +
      '<span>' + readTime + ' min read</span>' +
      '<span>' + locationTag + '</span>';
    return meta;
  }

  function ensureFeaturedImage(hero, content) {
    if (!hero || !content || document.querySelector('.lc-featured-media')) return;
    var styleValue = hero.getAttribute('style') || '';
    var urlMatch = styleValue.match(/--lc-hero-image:\s*url\(['\"]?([^'\")]+)['\"]?\)/i);
    if (!urlMatch || !urlMatch[1]) return;

    var figure = document.createElement('figure');
    figure.className = 'lc-featured-media';
    figure.innerHTML =
      '<img src="' + urlMatch[1] + '" alt="Featured image for this learning center article" loading="eager" decoding="async">' +
      '<figcaption>Jacksonville Guide</figcaption>';

    hero.insertAdjacentElement('afterend', figure);
  }

  function styleTakeaways(article) {
    if (!article) return;
    var sections = article.querySelectorAll('.lc-article-section');
    if (!sections.length) return;
    var first = sections[0];
    var h2 = first.querySelector('h2');
    if (!h2) return;
    var heading = text(h2).toLowerCase();
    if (!heading.includes('takeaway') && !heading.includes('tl;dr')) return;
    first.classList.add('lc-takeaways-card');
    h2.textContent = 'Quick Takeaways';
  }

  function styleReusableBlocks(article) {
    if (!article) return;

    article.querySelectorAll('table').forEach(function (table) {
      var wrap = document.createElement('div');
      wrap.className = 'lc-table-wrap';
      table.parentNode.insertBefore(wrap, table);
      wrap.appendChild(table);
      table.classList.add('lc-compare-table');
    });

    article.querySelectorAll('blockquote').forEach(function (quote) {
      quote.classList.add('lc-pull-quote');
    });

    article.querySelectorAll('.lc-article-section').forEach(function (section) {
      var heading = text(section.querySelector('h2')).toLowerCase();
      if (heading.includes('what is included') || heading.includes('what we actually do') || heading.includes('process')) {
        section.classList.add('lc-process-box');
      }
    });
  }

  function enhanceFaq(article) {
    var faqSection = article && article.querySelector('#faq');
    if (!faqSection || faqSection.dataset.enhanced === 'true') return;

    faqSection.classList.add('lc-faq-clean');
    var items = faqSection.querySelectorAll(':scope > article, :scope > .lc-faq-item');

    items.forEach(function (item, index) {
      var question = item.querySelector('h3');
      var answer = item.querySelector('p');
      if (!question || !answer) return;

      var details = document.createElement('details');
      details.className = 'lc-faq-item';
      if (index === 0) details.open = true;
      details.innerHTML = '<summary>' + question.innerHTML + '</summary><p>' + answer.innerHTML + '</p>';
      item.replaceWith(details);
    });

    faqSection.querySelectorAll('.lc-faq-item').forEach(function (item, idx) {
      if (idx > 3) item.classList.add('lc-faq-extra');
    });

    faqSection.dataset.enhanced = 'true';
  }

  function enhanceSidebar() {
    var sidebar = document.querySelector('.lc-article-sidebar');
    if (!sidebar) return;
    if (!sidebar.querySelector('.lc-side-card--numbers')) {
      var numbers = document.createElement('div');
      numbers.className = 'lc-side-card lc-side-card--numbers';
      numbers.innerHTML = '<h2>Key Numbers</h2><ul><li><strong>Starting Price:</strong> Most jobs start around $900</li><li><strong>Typical Driveway:</strong> $900–$1,800</li><li><strong>Reseal Cycle:</strong> 2–3 years</li></ul>';
      sidebar.appendChild(numbers);
    }
    if (!sidebar.querySelector('.lc-side-card--trust')) {
      var trust = document.createElement('div');
      trust.className = 'lc-side-card lc-side-card--trust';
      trust.innerHTML = '<h2>Why Homeowners Choose HydroSeal</h2><ul><li>Master Certified Trident company</li><li>Jacksonville-based crews</li><li>Serving Duval, St. Johns, and Clay</li></ul>';
      sidebar.appendChild(trust);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (!document.body.classList.contains('lc-article-page')) return;

    var hero = document.querySelector('.lc-hero--article .lc-hero-shell');
    var subhead = hero && hero.querySelector('.lc-subhead');
    var article = document.querySelector('.lc-article-content');
    if (hero && subhead && !hero.querySelector('.lc-article-meta')) {
      var readTime = estimateReadTime(article);
      var locationTag = detectLocation(text(document.querySelector('h1')), text(article));
      subhead.insertAdjacentElement('afterend', buildMetaRow(readTime, locationTag));
    }

    ensureFeaturedImage(document.querySelector('.lc-hero--article'), document.querySelector('.lc-article-body'));
    styleTakeaways(article);
    styleReusableBlocks(article);
    enhanceFaq(article);
    enhanceSidebar();

    var cta = document.querySelector('.lc-soft-cta--inline .lc-soft-cta-shell');
    if (cta && !cta.querySelector('.lc-cta-trust')) {
      var trustList = document.createElement('ul');
      trustList.className = 'lc-cta-trust';
      trustList.innerHTML = '<li>Master Certified Trident Company</li><li>Serving Jacksonville, Nocatee, and Ponte Vedra</li><li>Most jobs start around $900</li>';
      cta.appendChild(trustList);
    }
  });
})();
