(function () {
  if (window.__hsAnalyticsInit) return;
  window.__hsAnalyticsInit = true;

  function track(eventName, payload) {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", eventName, payload);
  }

  function closestTrackable(el) {
    if (!(el instanceof Element)) return null;
    return el.closest('a[href^="tel:"], a[href="/get-a-quote"], a[href^="/get-a-quote?"], a[href^="/get-a-quote#"], button[data-quote-link]');
  }

  document.addEventListener(
    "click",
    function (event) {
      const target = closestTrackable(event.target);
      if (!target) return;

      if (target.matches('a[href^="tel:"]')) {
        track("click_to_call", {
          phone_number: target.getAttribute("href") || "",
          page_path: window.location.pathname,
        });
        return;
      }

      if (
        target.matches('a[href="/get-a-quote"], a[href^="/get-a-quote?"], a[href^="/get-a-quote#"], button[data-quote-link]')
      ) {
        track("request_quote_click", {
          page_path: window.location.pathname,
        });
      }
    },
    { passive: true }
  );
})();
