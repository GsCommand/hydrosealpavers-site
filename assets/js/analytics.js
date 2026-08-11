(function () {
  if (window.__hsAnalyticsInit) return;
  window.__hsAnalyticsInit = true;

  function removeStripResealNavLink() {
    document.querySelectorAll('header a[href="/paver-resealing"], nav a[href="/paver-resealing"]').forEach((link) => {
      if (link.textContent.trim().toLowerCase().startsWith("strip and reseal")) link.remove();
    });
  }

  function injectPatioRecentProjects() {
    const path = (window.location.pathname || "")
      .replace(/\/index\.html$/, "")
      .replace(/\.html$/, "")
      .replace(/\/$/, "");
    if (path !== "/paver-sealing/patios-walkways") return;
    if (document.querySelector(".patio-recent-projects")) return;

    const processSection = document.querySelector("#patio-process");
    if (!processSection || !processSection.parentNode) return;

    if (!document.querySelector('script[src="https://elfsightcdn.com/platform.js"]')) {
      const platform = document.createElement("script");
      platform.src = "https://elfsightcdn.com/platform.js";
      platform.async = true;
      document.head.appendChild(platform);
    }

    const section = document.createElement("section");
    section.className = "section patio-recent-projects";
    section.style.paddingTop = "34px";
    section.style.paddingBottom = "34px";
    section.innerHTML = '<div class="container"><div class="elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26" data-elfsight-app-lazy></div></div>';
    processSection.parentNode.insertBefore(section, processSection);
  }

  removeStripResealNavLink();
  injectPatioRecentProjects();
  document.addEventListener("DOMContentLoaded", function () {
    removeStripResealNavLink();
    injectPatioRecentProjects();
  }, { once: true });

  const navObserver = new MutationObserver(function () {
    removeStripResealNavLink();
    injectPatioRecentProjects();
  });
  navObserver.observe(document.documentElement, { childList: true, subtree: true });

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
