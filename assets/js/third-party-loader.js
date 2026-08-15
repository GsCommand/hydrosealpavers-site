(function () {
  const path = location.pathname.replace(/\/$/, '');

  function fixJointSandColorCards() {
    if (path !== '/learning-center/surfaces/what-is-the-best-sand-for-paver-joints-in-florida') return;

    if (!document.getElementById('hs-joint-sand-card-fix')) {
      const style = document.createElement('style');
      style.id = 'hs-joint-sand-card-fix';
      style.textContent = `
        .sand-color-options .hs-sand-card-link{display:block;height:100%;color:inherit!important;text-decoration:none!important;border-radius:16px}
        .sand-color-options .hs-sand-card-link:focus-visible{outline:3px solid rgba(15,110,168,.35);outline-offset:3px}
        .sand-color-options .sand-color-card{height:100%;transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}
        .sand-color-options .hs-sand-card-link:hover .sand-color-card{transform:translateY(-2px);box-shadow:0 12px 28px rgba(11,45,74,.14);border-color:rgba(15,110,168,.35)}
        .sand-color-options .hs-sand-card-photo{display:block!important;width:100%!important;aspect-ratio:1/1!important;min-height:120px!important;border-radius:12px;border:1px solid rgba(0,0,0,.12);background-size:cover!important;background-position:center!important;background-repeat:no-repeat!important}
      `;
      document.head.appendChild(style);
    }

    document.querySelectorAll('.sand-color-options .sand-color-card').forEach((card) => {
      if (card.dataset.hsSandFixed === '1') return;
      const img = card.querySelector('img');
      if (!img) return;

      const photo = document.createElement('span');
      photo.className = 'hs-sand-card-photo';
      photo.setAttribute('role', 'img');
      photo.setAttribute('aria-label', img.getAttribute('alt') || 'Paver joint sand color sample');
      photo.style.backgroundImage = `url("${img.getAttribute('src')}")`;
      img.replaceWith(photo);

      if (!card.parentElement || !card.parentElement.classList.contains('hs-sand-card-link')) {
        const link = document.createElement('a');
        link.className = 'hs-sand-card-link';
        link.href = '/paver-sealing/sand-options';
        link.setAttribute('aria-label', `${(card.querySelector('strong') || {}).textContent || 'Paver sand'} color options`);
        card.parentNode.insertBefore(link, card);
        link.appendChild(card);
      }

      card.dataset.hsSandFixed = '1';
    });
  }

  fixJointSandColorCards();

  if (path === '/paver-sealing/pool-decks') {
    const gallery = document.querySelector('.elfsight-app-aac62a49-a425-47be-9c8a-13971e000940');
    const sandSection = document.querySelector('.sand-bar-section');
    const heroCopy = document.querySelector('.pool-service-hero__copy');

    if (gallery && sandSection && sandSection.parentNode) {
      sandSection.parentNode.insertBefore(gallery, sandSection);
    }

    if (heroCopy && heroCopy.textContent.includes('Professional pool deck sealing with deep cleaning')) {
      heroCopy.remove();
    }
  }

  if (window.__hsThirdPartyLoaderRan) {
    if (typeof window.__hsArmElfsight === 'function') window.__hsArmElfsight();
    return;
  }
  window.__hsThirdPartyLoaderRan = true;

  const WIDGET_SELECTOR = '[class*="elfsight-app-"]';
  const PLATFORM_SELECTOR = [
    'script[src="https://elfsightcdn.com/platform.js"]',
    'script[src="https://static.elfsight.com/platform/platform.js"]'
  ].join(',');

  let requested = false;
  let intersectionObserver = null;
  let mutationObserver = null;

  function hasWidget() {
    return !!document.querySelector(WIDGET_SELECTOR);
  }

  function loadElfsight() {
    if (!hasWidget()) return;
    if (requested || window.ELFSIGHT) return;

    // Never add a second platform copy when an older page still contains
    // a legacy Elfsight script tag. The page will be migrated separately,
    // but this guard prevents double-loading in the meantime.
    if (document.querySelector(PLATFORM_SELECTOR)) {
      requested = true;
      return;
    }

    requested = true;
    const script = document.createElement('script');
    script.src = 'https://static.elfsight.com/platform/platform.js';
    script.async = true;
    script.defer = true;
    script.dataset.hsThirdParty = 'elfsight';
    document.head.appendChild(script);
  }

  function armElfsight() {
    const widget = document.querySelector(WIDGET_SELECTOR);
    if (!widget) return false;

    if (intersectionObserver) intersectionObserver.disconnect();

    if ('IntersectionObserver' in window) {
      intersectionObserver = new IntersectionObserver((entries) => {
        if (!entries.some((entry) => entry.isIntersecting || entry.intersectionRatio > 0)) return;
        intersectionObserver.disconnect();
        loadElfsight();
      }, { rootMargin: '300px 0px' });
      intersectionObserver.observe(widget);
    } else if ('requestIdleCallback' in window) {
      requestIdleCallback(loadElfsight, { timeout: 2500 });
    } else {
      setTimeout(loadElfsight, 1800);
    }

    return true;
  }

  window.__hsLoadElfsight = loadElfsight;
  window.__hsArmElfsight = armElfsight;

  if (!armElfsight() && 'MutationObserver' in window) {
    mutationObserver = new MutationObserver(() => {
      if (!armElfsight()) return;
      mutationObserver.disconnect();
    });
    mutationObserver.observe(document.documentElement, { childList: true, subtree: true });
  }

  ['pointerdown', 'touchstart', 'scroll'].forEach((eventName) => {
    window.addEventListener(eventName, loadElfsight, { once: true, passive: true });
  });
})();
