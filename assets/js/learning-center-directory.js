(() => {
  const searchForm = document.querySelector('[data-guide-search]');
  const input = document.querySelector('[data-guide-search-input]');
  const clearButton = document.querySelector('[data-guide-search-clear]');
  const filterButtons = [...document.querySelectorAll('[data-guide-filter]')];
  const cards = [...document.querySelectorAll('[data-guide-card]')];
  const results = document.querySelector('[data-guide-results]');
  const noResults = document.querySelector('[data-guide-no-results]');

  if (!searchForm || !input || !cards.length || !results || !noResults) return;

  let activeCategory = 'all';

  const updateGuides = () => {
    const query = input.value.trim().toLowerCase();
    let visible = 0;

    cards.forEach((card) => {
      const matchesCategory = activeCategory === 'all' || card.dataset.category.split(' ').includes(activeCategory);
      const matchesSearch = !query || card.dataset.search.includes(query);
      const show = matchesCategory && matchesSearch;
      card.hidden = !show;
      if (show) visible += 1;
    });

    const categoryName = filterButtons.find((button) => button.dataset.guideFilter === activeCategory)?.textContent.trim();
    results.textContent = visible === cards.length ? `Showing all ${visible} guides.` : `Showing ${visible} guide${visible === 1 ? '' : 's'}${activeCategory === 'all' ? '' : ` in ${categoryName}`}.`;
    noResults.hidden = visible !== 0;
    clearButton.hidden = !query;
  };

  searchForm.addEventListener('submit', (event) => event.preventDefault());
  searchForm.addEventListener('reset', () => window.setTimeout(updateGuides, 0));
  input.addEventListener('input', updateGuides);
  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      activeCategory = button.dataset.guideFilter;
      filterButtons.forEach((filter) => {
        const active = filter === button;
        filter.classList.toggle('is-active', active);
        filter.setAttribute('aria-pressed', String(active));
      });
      updateGuides();
    });
  });
})();
