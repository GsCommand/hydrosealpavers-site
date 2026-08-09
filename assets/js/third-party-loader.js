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

  if (window.__hsThirdPartyLoaderRan) return;
  window.__hsThirdPartyLoaderRan = true;

  const widget = document.querySelector('[class*="elfsight-app-"]');
  if (!widget) return;

  let requested = false;

  function loadElfsight() {
    if (requested || window.ELFSIGHT) return;
    requested = true;
    const script = document.createElement('script');
    script.src = 'https://static.elfsight.com/platform/platform.js';
    script.async = true;
    script.defer = true;
    script.dataset.hsThirdParty = 'elfsight';
    document.head.appendChild(script);
  }

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (!entries.some((entry) => entry.isIntersecting || entry.intersectionRatio > 0)) return;
      observer.disconnect();
      loadElfsight();
    }, { rootMargin: '300px 0px' });
    observer.observe(widget);
  } else if ('requestIdleCallback' in window) {
    requestIdleCallback(loadElfsight, { timeout: 2500 });
  } else {
    setTimeout(loadElfsight, 1800);
  }

  ['pointerdown', 'touchstart', 'scroll'].forEach((eventName) => {
    window.addEventListener(eventName, loadElfsight, { once: true, passive: true });
  });
})();
