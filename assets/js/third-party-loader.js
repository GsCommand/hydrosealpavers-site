(function () {
  if (window.__hsThirdPartyLoaderRan) return;
  window.__hsThirdPartyLoaderRan = true;

  const hasElfsightWidgets = !!document.querySelector('[class*="elfsight-app-"]');
  if (!hasElfsightWidgets) return;

  let scriptRequested = false;

  function injectElfsightScript() {
    if (scriptRequested || window.ELFSIGHT) return;
    scriptRequested = true;

    const script = document.createElement('script');
    script.src = 'https://static.elfsight.com/platform/platform.js';
    script.async = true;
    script.defer = true;
    script.setAttribute('data-hs-third-party', 'elfsight');
    document.head.appendChild(script);
  }

  function requestWhenIdle() {
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(injectElfsightScript, { timeout: 2500 });
    } else {
      window.setTimeout(injectElfsightScript, 1800);
    }
  }

  const nearFoldWidget = document.querySelector('[class*="elfsight-app-"]');
  if ('IntersectionObserver' in window && nearFoldWidget) {
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting || entry.intersectionRatio > 0)) {
          io.disconnect();
          injectElfsightScript();
        }
      },
      { rootMargin: '300px 0px' }
    );
    io.observe(nearFoldWidget);
  } else {
    requestWhenIdle();
  }

  ['pointerdown', 'touchstart', 'scroll'].forEach((eventName) => {
    window.addEventListener(
      eventName,
      () => {
        injectElfsightScript();
      },
      { once: true, passive: true }
    );
  });
})();
