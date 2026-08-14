(function () {
  const path = location.pathname.replace(/\/$/, '');

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
