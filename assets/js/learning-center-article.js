(function () {
  function text(el) {
    return (el && el.textContent ? el.textContent : '').trim();
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

  document.addEventListener('DOMContentLoaded', function () {
    if (!document.body.classList.contains('lc-article-page')) return;

    var article = document.querySelector('.learning-article__body');
    styleTakeaways(article);
    styleReusableBlocks(article);
    enhanceFaq(article);
  });
})();
