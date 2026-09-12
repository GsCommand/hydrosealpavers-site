(function () {
  if (window.__hsSearchIntentCopyRan) return;
  window.__hsSearchIntentCopyRan = true;

  function normalizedPath() {
    return (window.location.pathname || "")
      .replace(/\/index\.html$/, "")
      .replace(/\.html$/, "")
      .replace(/\/$/, "");
  }

  function ensureStyles() {
    if (document.getElementById("hs-search-intent-style")) return;
    var style = document.createElement("style");
    style.id = "hs-search-intent-style";
    style.textContent = [
      ".hs-search-intent{width:min(1180px,calc(100% - 40px));margin:34px auto 48px;padding:24px 26px;border:1px solid #dce7ed;border-radius:20px;background:linear-gradient(145deg,#f7fbfd,#ffffff);box-shadow:0 12px 32px rgba(11,45,74,.06)}",
      ".hs-search-intent__eyebrow{margin:0 0 7px;color:#0f6ea8;font-size:11px;font-weight:900;letter-spacing:1.2px;text-transform:uppercase}",
      ".hs-search-intent h2{margin:0 0 10px;color:#0b2d4a;font-family:Arial,sans-serif;font-size:clamp(24px,3vw,34px);line-height:1.12;letter-spacing:-.5px}",
      ".hs-search-intent p{margin:0;color:#536475;font-size:15px;line-height:1.7}",
      ".hs-search-intent a{color:#0f6ea8;font-weight:800;text-decoration:underline;text-underline-offset:3px}",
      "@media(max-width:650px){.hs-search-intent{width:calc(100% - 24px);margin:24px auto 34px;padding:20px 18px;border-radius:16px}.hs-search-intent p{font-size:14px}}"
    ].join("");
    document.head.appendChild(style);
  }

  function addHomepageFaq() {
    var path = normalizedPath();
    if (path !== "") return;
    var faq = document.querySelector(".home-faq .faq-wrap, .home-faq");
    if (!faq || document.getElementById("hs-near-me-home-faq")) return;

    var details = document.createElement("details");
    details.id = "hs-near-me-home-faq";
    details.innerHTML = '<summary>How do I find a paver sealing company near me?</summary><div class="faq-body"><p>If you are searching for <strong>paver sealing near me</strong> or <strong>paver cleaning and sealing near me</strong>, HydroSeal serves Jacksonville, St. Johns County, Ponte Vedra, Nocatee, Orange Park, Fleming Island and nearby Northeast Florida communities. We evaluate the paver condition, joint sand, previous sealer, drainage and surface type before recommending cleaning, resealing or restoration.</p></div>';
    faq.appendChild(details);
  }

  function addPageIntentBlock() {
    var path = normalizedPath();
    var pages = {
      "/paver-cleaning": {
        eyebrow: "Local paver cleaning & restoration",
        heading: "Paver cleaning, sealing and restoration near Jacksonville.",
        copy: 'Homeowners searching for <strong>paver cleaning and sealing near me</strong> or <strong>paver restoration near me</strong> often need more than high-pressure washing. HydroSeal serves Jacksonville, St. Johns County, Ponte Vedra, Nocatee, Orange Park, Fleming Island and nearby communities with surface-specific cleaning, joint evaluation and sealing-ready preparation. <a href="/paver-resealing/">See our paver resealing and restoration process.</a>'
      },
      "/paver-resealing": {
        eyebrow: "Local resealing & restoration",
        heading: "Paver restoration and resealing across Northeast Florida.",
        copy: 'If you are searching for <strong>paver restoration near me</strong> or <strong>paver sealing near me</strong>, the condition of the old coating matters as much as the new sealer. HydroSeal evaluates whitening, peeling, fading, joint-sand loss, moisture and coating compatibility before recommending cleaning, resealing or stripping. <a href="/learning-center/problems/cleaning-resealing-or-stripping">Learn when cleaning, resealing or stripping is appropriate.</a>'
      },
      "/paver-sealing/driveways": {
        eyebrow: "Driveway service near you",
        heading: "Driveway paver sealing for Jacksonville and nearby communities.",
        copy: 'Homeowners searching for <strong>driveway paver sealing near me</strong> can use HydroSeal for professional cleaning, joint-sand restoration and breathable sealing throughout Jacksonville, St. Johns County, Ponte Vedra, Nocatee, Orange Park, Fleming Island and nearby Northeast Florida areas. <a href="/get-a-quote">Request a driveway quote.</a>'
      },
      "/paver-sealing/travertine-sealing": {
        eyebrow: "Natural-stone service near you",
        heading: "Travertine sealing for Northeast Florida pool decks and patios.",
        copy: 'If you are searching for <strong>travertine sealing near me</strong>, HydroSeal provides material-specific cleaning and protection for travertine pool decks, patios and outdoor living areas across Jacksonville, St. Johns County, Ponte Vedra, Nocatee and surrounding communities. Natural stone is evaluated for porosity, moisture, fill condition, staining and previous treatments before sealing. <a href="/get-a-quote">Request a travertine quote.</a>'
      },
      "/service-areas/st-johns-county": {
        eyebrow: "St. Johns County paver sealing",
        heading: "Paver sealing in St. Johns and St. Augustine, Florida.",
        copy: 'HydroSeal provides <strong>paver sealing in St. Johns, FL</strong> and serves homeowners looking for <strong>paver sealing in St. Augustine, FL</strong>, along with Nocatee, Ponte Vedra, Palm Valley, Julington Creek, World Golf Village and nearby St. Johns County communities. Services include driveway sealing, pool deck sealing, paver cleaning, joint-sand restoration and travertine sealing. <a href="/get-a-quote">Request a local paver sealing quote.</a>'
      }
    };

    var config = pages[path];
    if (!config || document.getElementById("hs-search-intent-block")) return;
    var main = document.querySelector("main");
    if (!main) return;

    ensureStyles();
    var section = document.createElement("section");
    section.id = "hs-search-intent-block";
    section.className = "hs-search-intent";
    section.setAttribute("aria-label", config.heading);
    section.innerHTML = '<p class="hs-search-intent__eyebrow">' + config.eyebrow + '</p><h2>' + config.heading + '</h2><p>' + config.copy + '</p>';

    var lastSection = main.querySelector(":scope > section:last-of-type");
    if (lastSection && lastSection.parentNode === main) main.insertBefore(section, lastSection);
    else main.appendChild(section);
  }

  function run() {
    addHomepageFaq();
    addPageIntentBlock();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run, { once: true });
  else run();
})();
