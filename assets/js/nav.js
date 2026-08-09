/* nav.js — hamburger + dropdowns (SAFE with includes) */
(function () {
  if (window.__hs_nav_inited) return;
  window.__hs_nav_inited = true;

  function removeStripResealNavLink() {
    document.querySelectorAll('header a[href="/paver-resealing"], nav a[href="/paver-resealing"]').forEach((link) => {
      if (link.textContent.trim().toLowerCase().startsWith("strip and reseal")) link.remove();
    });
  }

  function resetDropdownState() {
    const groups = Array.from(document.querySelectorAll(".nav-group"));
    groups.forEach((group) => {
      group.classList.remove("open");
      clearMobileDropdownPosition(group);
      const parent = group.querySelector(".nav-parent");
      if (parent) parent.setAttribute("aria-expanded", "false");
    });
  }

  function initHeaderHamburger() {
    const shell = document.querySelector(".nav-shell");
    const btn = document.querySelector(".nav-toggle");
    const overlay = document.querySelector(".nav-overlay");
    const nav = document.querySelector(".header-nav");
    if (!shell || !btn || !overlay || !nav) return;

    if (btn.dataset.bound) return;
    btn.dataset.bound = "1";

    const setOpen = (open) => {
      shell.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      overlay.hidden = !open;
      document.documentElement.classList.toggle("nav-lock", open);
      document.body.classList.toggle("nav-lock", open);
      if (!open) resetDropdownState();
    };

    btn.addEventListener("click", (e) => {
      e.preventDefault();
      setOpen(!shell.classList.contains("open"));
    });

    overlay.addEventListener("click", () => setOpen(false));

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") setOpen(false);
    });

    nav.addEventListener("click", (e) => {
      const a = e.target.closest("a");
      if (a) setOpen(false);
    });
  }

  function isMobile() {
    return window.matchMedia("(max-width: 980px)").matches;
  }

  function positionMobileDropdown(group) {
    if (!isMobile()) return;
    const header = document.querySelector(".header");
    const dd = group.querySelector(".dropdown");
    if (!header || !dd) return;

    const rect = header.getBoundingClientRect();
    const top = Math.round(rect.bottom + 8);

    dd.style.position = "fixed";
    dd.style.left = "12px";
    dd.style.right = "12px";
    dd.style.top = top + "px";
    dd.style.width = "auto";
    dd.style.maxWidth = "none";
    dd.style.zIndex = "10001";
  }

  function clearMobileDropdownPosition(group) {
    const dd = group.querySelector(".dropdown");
    if (!dd) return;
    dd.style.position = "";
    dd.style.left = "";
    dd.style.right = "";
    dd.style.top = "";
    dd.style.width = "";
    dd.style.maxWidth = "";
    dd.style.zIndex = "";
  }

  function initNavDropdowns() {
    const groups = Array.from(document.querySelectorAll(".nav-group"));
    if (!groups.length) return;

    groups.forEach((group) => {
      const parent = group.querySelector(".nav-parent");
      const dropdown = group.querySelector(".dropdown");
      if (!parent || !dropdown) return;

      if (!parent.dataset.bound) {
        parent.dataset.bound = "1";
        parent.setAttribute("aria-haspopup", "menu");
        parent.setAttribute("aria-expanded", "false");

        const toggleGroup = (e) => {
          e.preventDefault();
          e.stopPropagation();

          const wasOpen = group.classList.contains("open");
          resetDropdownState();

          if (!wasOpen) {
            group.classList.add("open");
            parent.setAttribute("aria-expanded", "true");
            positionMobileDropdown(group);
          }
        };

        parent.addEventListener("click", toggleGroup);
        parent.addEventListener("pointerdown", (e) => {
          if (e.pointerType === "mouse") return;
          toggleGroup(e);
        });
        parent.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") toggleGroup(e);
        });
      }

      if (!dropdown.dataset.bound) {
        dropdown.dataset.bound = "1";
        dropdown.addEventListener("pointerdown", (e) => e.stopPropagation());
        dropdown.addEventListener("click", (e) => e.stopPropagation());
      }
    });

    if (!document.body.dataset.navOutsideBound) {
      document.body.dataset.navOutsideBound = "1";

      document.addEventListener("pointerdown", (e) => {
        if (e.target.closest(".header")) return;
        resetDropdownState();
      });

      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") resetDropdownState();
      });

      window.addEventListener("resize", () => {
        groups.forEach((g) => {
          if (g.classList.contains("open")) {
            if (isMobile()) positionMobileDropdown(g);
            else clearMobileDropdownPosition(g);
          }
        });
      });
    }
  }

  function normalizedPath() {
    return (window.location.pathname || "/")
      .replace(/\/index\.html$/, "")
      .replace(/\.html$/, "")
      .replace(/\/$/, "") || "/";
  }

  function isMainPage() {
    return [
      "/",
      "/paver-sealing",
      "/paver-resealing",
      "/paver-sealing/driveways",
      "/paver-sealing/pool-decks",
      "/paver-sealing/patios-walkways",
      "/paver-sealing/travertine-sealing",
      "/paver-sealing/sand-options"
    ].includes(normalizedPath());
  }

  function addLinkOnce(container, href, label) {
    if (!container || container.querySelector('a[href="' + href + '"]')) return;
    const link = document.createElement("a");
    link.href = href;
    link.textContent = label;
    container.appendChild(link);
  }

  function addMainFooterLinks() {
    if (!isMainPage()) return;

    document.querySelectorAll("footer .footer-title").forEach((title) => {
      if (title.textContent.trim().toLowerCase() !== "services") return;
      const links = title.parentElement && title.parentElement.querySelector(".footer-links");
      if (!links) return;
      addLinkOnce(links, "/paver-resealing", "Paver Resealing");
      addLinkOnce(links, "/paver-sealing-cost-calculator", "Paver Sealing Cost Calculator");
    });
  }

  function addHomepageCalculatorNavLink() {
    if (normalizedPath() !== "/") return;

    document.querySelectorAll(".nav-group").forEach((group) => {
      const parent = group.querySelector(".nav-parent");
      const dropdown = group.querySelector(".dropdown");
      if (!parent || !dropdown) return;
      if (parent.textContent.trim().toLowerCase() !== "paver sealing") return;
      addLinkOnce(dropdown, "/paver-sealing-cost-calculator", "Cost Calculator");
    });
  }

  function isTrustbarExcludedPath() {
    const path = normalizedPath();
    return path === "/warranty" || path === "/care-program";
  }

  function moveTrustbarForMobile() {
    if (isTrustbarExcludedPath()) return;

    const trustbar = document.querySelector(".trustbar");
    if (!trustbar) return;

    const heroAnchor = document.querySelector(".home-hero-wrap") || document.querySelector(".hero2");
    if (!heroAnchor) return;

    if (!window.__hs_trustbar_state) {
      window.__hs_trustbar_state = {
        parent: trustbar.parentNode,
        nextSibling: trustbar.nextSibling,
      };
    }

    const state = window.__hs_trustbar_state;

    if (isMobile()) {
      if (heroAnchor.nextElementSibling !== trustbar) {
        heroAnchor.insertAdjacentElement("afterend", trustbar);
      }
      return;
    }

    if (state.parent) state.parent.insertBefore(trustbar, state.nextSibling || null);
  }

  function rebuildPaverResealingMiddle() {
    if (normalizedPath() !== "/paver-resealing") return;
    if (document.documentElement.dataset.resealMiddleBuilt === "1") return;

    const pricing = document.querySelector(".reseal-pricing-wrap");
    if (!pricing) return;

    const recent = Array.from(document.querySelectorAll(".dw-section")).find((section) => {
      const kicker = section.querySelector(".dw-kicker");
      return kicker && kicker.textContent.trim().toLowerCase() === "recent sealing jobs";
    });
    if (!recent || !recent.parentNode) return;

    let node = pricing.nextElementSibling;
    while (node && node !== recent) {
      const next = node.nextElementSibling;
      node.remove();
      node = next;
    }

    if (!document.getElementById("reseal-service-split-styles")) {
      const style = document.createElement("style");
      style.id = "reseal-service-split-styles";
      style.textContent = `
        .reseal-feature-section{padding:86px 0}
        .reseal-feature-section--soft{background:#f4f7f9}
        .reseal-feature-shell{width:min(1180px,calc(100% - 40px));margin:auto}
        .reseal-feature-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:stretch}
        .reseal-feature-card{padding:32px;border:1px solid #dce5ea;border-radius:26px;background:#fff;box-shadow:0 16px 38px rgba(11,45,74,.07)}
        .reseal-feature-kicker{display:block;margin-bottom:10px;color:#0f6ea8;font-size:12px;font-weight:900;letter-spacing:1.8px;text-transform:uppercase}
        .reseal-feature-card h2{margin:0 0 14px;color:#0b2d4a;font-family:"Arial Black",Arial,sans-serif;font-size:clamp(30px,3.4vw,46px);line-height:1.05;letter-spacing:-1px}
        .reseal-feature-card p,.reseal-feature-card li{color:#536475;font-size:16px;line-height:1.68}
        .reseal-feature-card p{margin:0 0 15px}
        .reseal-feature-card ul{margin:18px 0 0;padding-left:20px}
        .reseal-feature-card a{color:#0f6ea8;font-weight:800;text-decoration:none}
        .reseal-feature-media{min-height:430px;overflow:hidden;border-radius:26px;background:#e8eef1;box-shadow:0 18px 42px rgba(11,45,74,.12)}
        .reseal-feature-media img{display:block;width:100%;height:100%;object-fit:cover}
        @media(max-width:980px){.reseal-feature-grid{grid-template-columns:1fr}.reseal-feature-media{min-height:360px}}
        @media(max-width:650px){.reseal-feature-shell{width:calc(100% - 24px)}.reseal-feature-section{padding:64px 0}.reseal-feature-card{padding:24px 20px}.reseal-feature-media{min-height:280px}}
      `;
      document.head.appendChild(style);
    }

    const wrapper = document.createElement("div");
    wrapper.innerHTML = `
      <section class="reseal-feature-section reseal-feature-section--soft">
        <div class="reseal-feature-shell">
          <div class="reseal-feature-grid">
            <article class="reseal-feature-card">
              <span class="reseal-feature-kicker">Paver resealing</span>
              <h2>Previously sealed pavers need the surface restored before a fresh coat goes down.</h2>
              <p><strong>Paver resealing is the maintenance and restoration side of paver sealing.</strong> The core service is still professional cleaning, joint-sand restoration where needed, proper drying, and application of a compatible sealer. The difference is that the pavers have already been sealed before, so the existing coating becomes part of the evaluation.</p>
              <p>On a sound surface, resealing can restore richer color, a more uniform finish, joint stability, and easier maintenance. If the older coating is white, peeling, soft, heavily built up, moisture-damaged, or incompatible, HydroSeal evaluates that condition before another coat is applied.</p>
              <ul>
                <li>Restore faded or dry-looking pavers</li>
                <li>Refresh low or open joint sand where needed</li>
                <li>Match the new sealer to the existing surface and coating</li>
                <li>Identify coating failure before it gets buried under another layer</li>
              </ul>
            </article>
            <div class="reseal-feature-media"><img src="/assets/hero/driveway-before-after-hydroseal.webp" alt="Before and after paver resealing and color restoration by HydroSeal" loading="lazy" decoding="async"></div>
          </div>
        </div>
      </section>

      <section class="reseal-feature-section">
        <div class="reseal-feature-shell">
          <div class="reseal-feature-grid">
            <div class="reseal-feature-media"><img src="/assets/hero/hydroseal-travertine-pool-deck-square.webp" alt="Sealed paver pool deck maintained by HydroSeal in Northeast Florida" loading="lazy" decoding="async"></div>
            <article class="reseal-feature-card">
              <span class="reseal-feature-kicker">When to reseal pavers</span>
              <h2>Resealing is driven by surface condition—not only by the age of the sealer.</h2>
              <p>Many Florida paver surfaces begin showing normal wear as color fades, sheen becomes uneven, joint sand gets shallow, and high-traffic areas lose protection. Those are common reasons homeowners search for <strong>paver resealing</strong> or how to <strong>reseal pavers</strong>.</p>
              <p>HydroSeal uses roughly <strong>three to four years</strong> as a practical planning range for many professionally prepared surfaces, but full sun, vehicle traffic, irrigation, pool chemicals, drainage, coastal exposure, and harsh cleaning can shorten that cycle.</p>
              <p><strong>White, cloudy, peeling, or heavily built-up sealer is different.</strong> Those conditions may require testing, correction, partial removal, or stripping before resealing. We do not automatically coat over a failed surface.</p>
              <p><a href="/learning-center/problems/cleaning-resealing-or-stripping">See whether your pavers need cleaning, resealing, or stripping</a>.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="reseal-feature-section reseal-feature-section--soft">
        <div class="reseal-feature-shell">
          <div class="reseal-feature-grid">
            <article class="reseal-feature-card">
              <span class="reseal-feature-kicker">Professional paver resealing</span>
              <h2>Driveways, pool decks, patios, walkways, and previously sealed outdoor surfaces.</h2>
              <p>Our paver resealing process is built around the condition of the project: inspect the existing coating, clean and prepare the pavers, restore joint sand where needed, verify moisture and weather conditions, then apply a compatible contractor-grade sealing system.</p>
              <p>That approach works across <a href="/paver-sealing/driveways">driveway pavers</a>, <a href="/paver-sealing/pool-decks">pool decks</a>, <a href="/paver-sealing/patios-walkways">patios and walkways</a>, and suitable <a href="/paver-sealing/travertine-sealing">travertine or natural-stone surfaces</a>. Each surface is evaluated differently because traffic, moisture, traction, porosity, and the existing coating all affect the final scope.</p>
              <p>In Jacksonville, Nocatee, Ponte Vedra, and surrounding Northeast Florida communities, intense UV, summer rain, irrigation, humidity, and repeated wet-dry cycles make timely maintenance especially important. Resealing before complete coating failure can often avoid a more involved restoration later.</p>
              <p><a href="/service-areas/st-johns-county/nocatee">View paver resealing service in Nocatee</a> or <a href="/get-a-quote">request a project quote</a>.</p>
            </article>
            <div class="reseal-feature-media"><img src="/assets/images/driveway-before-after.webp" alt="Professional paver cleaning joint restoration and resealing result" loading="lazy" decoding="async"></div>
          </div>
        </div>
      </section>
    `;

    while (wrapper.firstElementChild) {
      recent.parentNode.insertBefore(wrapper.firstElementChild, recent);
    }

    document.documentElement.dataset.resealMiddleBuilt = "1";
  }

  function initAllNav() {
    removeStripResealNavLink();
    addHomepageCalculatorNavLink();
    addMainFooterLinks();
    initHeaderHamburger();
    initNavDropdowns();
    moveTrustbarForMobile();
    rebuildPaverResealingMiddle();
  }

  initAllNav();
  document.addEventListener("includes:ready", initAllNav);
  document.addEventListener("DOMContentLoaded", initAllNav, { once: true });
  window.addEventListener("resize", moveTrustbarForMobile);

  const observer = new MutationObserver(() => {
    removeStripResealNavLink();
    addHomepageCalculatorNavLink();
    addMainFooterLinks();
    initHeaderHamburger();
    initNavDropdowns();
    rebuildPaverResealingMiddle();
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });

  window.initAllNav = initAllNav;
})();
