(function () {
  if (window.__hsAnalyticsInit) return;
  window.__hsAnalyticsInit = true;

  function normalizedPath() {
    return (window.location.pathname || "")
      .replace(/\/index\.html$/, "")
      .replace(/\.html$/, "")
      .replace(/\/$/, "");
  }

  function ensureSharedElfsightLoader() {
    const widget = document.querySelector('[class*="elfsight-app-"]');
    if (!widget) return;

    // Older static pages embedded the Elfsight platform tag next to each widget.
    // Remove every legacy copy and hand control to the one shared deferred loader.
    document.querySelectorAll('script[src="https://elfsightcdn.com/platform.js"]').forEach((script) => script.remove());

    if (window.ELFSIGHT || window.__hsThirdPartyLoaderRan) return;
    if (document.querySelector('script[src="/assets/js/third-party-loader.js"]')) return;

    const loader = document.createElement("script");
    loader.src = "/assets/js/third-party-loader.js";
    loader.defer = true;
    loader.dataset.hsLoader = "elfsight";
    document.head.appendChild(loader);
  }

  function removeStripResealNavLink() {
    document.querySelectorAll('header a[href="/paver-resealing"], nav a[href="/paver-resealing"]').forEach((link) => {
      if (link.textContent.trim().toLowerCase().startsWith("strip and reseal")) link.remove();
    });
  }

  function removePatioHeroDescription() {
    if (normalizedPath() !== "/paver-sealing/patios-walkways") return;

    const target = "Professional paver sealing for patios, walkways, entries, and outdoor living spaces across Jacksonville and St. Johns County.";
    document.querySelectorAll(".patio-service-hero__copy, p").forEach((el) => {
      if (el.textContent.trim() === target) el.remove();
    });
  }

  function injectPatioRecentProjects() {
    if (normalizedPath() !== "/paver-sealing/patios-walkways") return;
    if (document.querySelector(".patio-recent-projects")) return;

    const processSection = document.querySelector("#patio-process");
    if (!processSection || !processSection.parentNode) return;

    const section = document.createElement("section");
    section.className = "section patio-recent-projects";
    section.style.paddingTop = "34px";
    section.style.paddingBottom = "34px";
    section.innerHTML = '<div class="container"><div class="elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26" data-elfsight-app-lazy></div></div>';
    processSection.parentNode.insertBefore(section, processSection);

    ensureSharedElfsightLoader();
    if (typeof window.__hsArmElfsight === "function") {
      window.__hsArmElfsight();
    }
  }

  function fixStripCostArticleHeader() {
    if (normalizedPath() !== "/learning-center/cost/how-much-does-it-cost-to-strip-and-reseal-pavers") return;
    if (document.getElementById("strip-cost-header-fix")) return;

    const style = document.createElement("style");
    style.id = "strip-cost-header-fix";
    style.textContent = `
      body.page-strip-reseal-cost .cost-hero{
        display:block!important;
        width:100%!important;
        max-width:900px!important;
        margin:0 auto 38px!important;
        text-align:center!important;
        grid-template-columns:none!important;
        grid-template-areas:none!important;
      }
      body.page-strip-reseal-cost .cost-hero__eyebrow,
      body.page-strip-reseal-cost .cost-hero h1,
      body.page-strip-reseal-cost .cost-hero__intro,
      body.page-strip-reseal-cost .cost-meta{
        display:block!important;
        width:100%!important;
        float:none!important;
        position:static!important;
      }
      body.page-strip-reseal-cost .cost-hero__eyebrow{
        max-width:none!important;
        margin:0 0 10px!important;
        text-align:center!important;
      }
      body.page-strip-reseal-cost .cost-hero h1{
        max-width:900px!important;
        margin:0 auto 18px!important;
        font-size:clamp(2.7rem,5.4vw,4.8rem)!important;
        line-height:1.02!important;
        letter-spacing:-.04em!important;
        text-align:center!important;
      }
      body.page-strip-reseal-cost .cost-hero__intro{
        max-width:760px!important;
        margin:0 auto!important;
        font-size:1.08rem!important;
        line-height:1.7!important;
        text-align:center!important;
      }
      body.page-strip-reseal-cost .cost-meta{
        max-width:none!important;
        margin:16px auto 0!important;
        text-align:center!important;
      }
      @media(max-width:650px){
        body.page-strip-reseal-cost .cost-hero h1{
          font-size:clamp(2.35rem,11vw,3.5rem)!important;
        }
      }
    `;
    document.head.appendChild(style);
  }

  ensureSharedElfsightLoader();
  removeStripResealNavLink();
  removePatioHeroDescription();
  injectPatioRecentProjects();
  fixStripCostArticleHeader();

  document.addEventListener("DOMContentLoaded", function () {
    ensureSharedElfsightLoader();
    removeStripResealNavLink();
    removePatioHeroDescription();
    injectPatioRecentProjects();
    fixStripCostArticleHeader();
  }, { once: true });

  const navObserver = new MutationObserver(function () {
    ensureSharedElfsightLoader();
    removeStripResealNavLink();
    removePatioHeroDescription();
    injectPatioRecentProjects();
    fixStripCostArticleHeader();
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
