(function () {
  if (location.pathname.replace(/\/$/, '') === '/paver-sealing/driveways') {
    const root = document.documentElement;
    let cssReady = false;
    let jsReady = false;

    root.style.visibility = 'hidden';

    const reveal = () => {
      if (cssReady && jsReady) requestAnimationFrame(() => { root.style.visibility = ''; });
    };

    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = '/assets/css/driveway-redesign.css?v=20260803-2';
    css.dataset.drivewayRedesign = '';
    css.onload = () => { cssReady = true; reveal(); };
    css.onerror = () => { cssReady = true; reveal(); };
    document.head.appendChild(css);

    const js = document.createElement('script');
    js.src = '/assets/js/driveway-redesign-runtime.js?v=20260803-1';
    js.onload = () => { jsReady = true; reveal(); };
    js.onerror = () => { jsReady = true; reveal(); };
    document.head.appendChild(js);

    setTimeout(() => { root.style.visibility = ''; }, 3000);
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
