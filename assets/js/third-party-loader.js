(function () {
  if (location.pathname.replace(/\/$/, '') === '/paver-sealing/driveways' && !document.querySelector('script[data-driveway-redesign-loader]')) {
    /*
     * The driveway page still ships legacy HTML that is upgraded by
     * driveway-redesign-runtime.js. Previously the runtime and its CSS were
     * requested only after this deferred loader ran, which allowed the old
     * layout to paint before the redesign replaced it.
     *
     * Start the final CSS and runtime together and keep the document hidden
     * only during that short handoff. Reveal after BOTH assets are ready so
     * visitors never see the legacy layout or an unstyled redesign.
     */
    var root = document.documentElement;
    var cssReady = false;
    var runtimeReady = false;
    var revealed = false;

    root.style.visibility = 'hidden';

    function revealDriveway() {
      if (revealed || !cssReady || !runtimeReady) return;
      revealed = true;
      requestAnimationFrame(function () {
        root.style.visibility = '';
      });
    }

    function failOpen() {
      if (revealed) return;
      revealed = true;
      root.style.visibility = '';
    }

    var drivewayCss = document.querySelector('link[data-driveway-redesign]');
    if (!drivewayCss) {
      drivewayCss = document.createElement('link');
      drivewayCss.rel = 'stylesheet';
      drivewayCss.href = '/assets/css/driveway-redesign.css?v=20260803-2';
      drivewayCss.setAttribute('data-driveway-redesign', '');
      drivewayCss.onload = function () {
        cssReady = true;
        revealDriveway();
      };
      drivewayCss.onerror = failOpen;
      document.head.appendChild(drivewayCss);
    } else {
      cssReady = true;
    }

    var drivewayScript = document.createElement('script');
    drivewayScript.src = '/assets/js/driveway-redesign-runtime.js?v=20260803-1';
    drivewayScript.async = false;
    drivewayScript.setAttribute('data-driveway-redesign-loader', '');
    drivewayScript.onload = function () {
      runtimeReady = true;
      revealDriveway();
    };
    drivewayScript.onerror = failOpen;
    document.head.appendChild(drivewayScript);

    /* Never leave the page hidden if a browser/network edge case occurs. */
    window.setTimeout(failOpen, 3500);
  }

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
