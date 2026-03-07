/* nav.js — hamburger + dropdowns (SAFE with includes) */
(function () {
  if (window.__hs_nav_inited) return;
  window.__hs_nav_inited = true;

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

    // Close menu when clicking any normal link
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
        parent.setAttribute("aria-haspopup", "true");
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
        if (e.key === "Escape") {
          resetDropdownState();
        }
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

  function isTrustbarExcludedPath() {
    const path = (window.location.pathname || "").replace(/\.html$/, "").replace(/\/$/, "");
    return path === "/warranty" || path === "/care-program";
  }

  function isHomepagePath() {
    const path = (window.location.pathname || "").replace(/\.html$/, "");
    return path === "/" || path === "" || path === "/index";
  }

  function moveTrustbarForMobile() {
    if (isTrustbarExcludedPath() || !isHomepagePath()) return;

    const trustbar = document.querySelector(".trustbar");
    const heroWrap = document.querySelector(".home-hero-wrap");
    if (!trustbar || !heroWrap) return;

    if (!window.__hs_trustbar_state) {
      window.__hs_trustbar_state = {
        parent: trustbar.parentNode,
        nextSibling: trustbar.nextSibling,
      };
    }

    const state = window.__hs_trustbar_state;

    if (isMobile()) {
      if (heroWrap.nextElementSibling !== trustbar) {
        heroWrap.insertAdjacentElement("afterend", trustbar);
      }
      return;
    }

    if (state.parent) {
      state.parent.insertBefore(trustbar, state.nextSibling || null);
    }
  }

  function initAllNav() {
    initHeaderHamburger();
    initNavDropdowns();
    moveTrustbarForMobile();
  }

  // Run now (in case header is already in DOM)
  initAllNav();

  window.addEventListener("resize", moveTrustbarForMobile);


  // Optional debugging hook
  window.initAllNav = initAllNav;
})();
