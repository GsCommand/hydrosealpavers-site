(function () {
  function initHome() {
    if (!document.body.classList.contains("page-home")) return;

    addPriorityLearningLinks();
    initMarquee();
    initProcessAccordion();
    initFaqAccordion();
  }

  function addPriorityLearningLinks() {
    const headings = Array.from(document.querySelectorAll(".related-links-column h3"));
    const learningHeading = headings.find(h => h.textContent.trim() === "Learning Center");
    if (!learningHeading) return;

    const list = learningHeading.parentElement && learningHeading.parentElement.querySelector("ul");
    if (!list || list.dataset.priorityLinksAdded === "true") return;
    list.dataset.priorityLinksAdded = "true";

    const guides = [
      ["/learning-center/local/best-time-of-year-to-seal-pavers-in-florida", "How Long Pavers Must Dry Before Sealing"],
      ["/learning-center/problems/why-are-my-pavers-turning-white-in-florida", "Why Paver Sealer Turns White"],
      ["/learning-center/sealing/water-based-vs-solvent-based-paver-sealer", "Water-Based vs. Solvent-Based Paver Sealer"],
      ["/learning-center/sealing/how-to-choose-the-right-paver-sealer-for-your-home", "Best Paver Sealer for Florida Weather"],
      ["/learning-center/sealing/how-long-does-paver-sealing-last-in-florida", "How Often Florida Pavers Need Resealing"]
    ];

    const existing = new Set(Array.from(list.querySelectorAll("a")).map(a => a.getAttribute("href")));
    guides.reverse().forEach(([href, label]) => {
      if (existing.has(href)) return;
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = href;
      link.textContent = label;
      item.appendChild(link);
      list.prepend(item);
    });
  }

  function initMarquee() {
    const track = document.getElementById("recentJobsTrack");
    if (!track) return;
    if (track.dataset.bound === "true") return;
    track.dataset.bound = "true";

    const marquee = track.closest(".marquee");
    if (!marquee) return;

    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      return;
    }

    const SPEED = 26;
    let running = true;
    let x = 0;
    let loopWidth = 0;
    let last = performance.now();
    let started = false;

    function getGapPx() {
      const st = getComputedStyle(track);
      return parseFloat(st.gap || st.columnGap || "0") || 0;
    }

    function buildClones() {
      track.querySelectorAll('[data-clone="1"]').forEach(n => n.remove());
      const originals = Array.from(track.querySelectorAll('[data-job]'));
      originals.forEach(el => {
        const clone = el.cloneNode(true);
        clone.setAttribute("data-clone","1");
        track.appendChild(clone);
      });
    }

    function measure() {
      const originals = Array.from(track.querySelectorAll('[data-job]'));
      const gap = getGapPx();

      loopWidth = originals.reduce((sum, el, i) => {
        const w = el.getBoundingClientRect().width;
        return sum + w + (i === originals.length - 1 ? 0 : gap);
      }, 0);

      x = loopWidth > 0 ? ((x % loopWidth) + loopWidth) % loopWidth : 0;
    }

    function render() {
      if (loopWidth <= 0) return;
      track.style.transform = `translate3d(${x - loopWidth}px,0,0)`;
    }

    function setStartAt3() {
      const originals = Array.from(track.querySelectorAll('[data-job]'));
      if (originals.length < 3) return;

      const gap = getGapPx();
      const w1 = originals[0].getBoundingClientRect().width;
      const w2 = originals[1].getBoundingClientRect().width;

      x = w1 + gap + w2 + gap;
      x = loopWidth > 0 ? ((x % loopWidth) + loopWidth) % loopWidth : 0;
      render();
    }

    function tick(now) {
      if (!document.body.contains(track)) return;

      const dt = (now - last) / 1000;
      last = now;

      if (!started) {
        started = true;
        measure();
        setStartAt3();
      }

      if (running && loopWidth > 0) {
        x += SPEED * dt;
        if (x >= loopWidth) x -= loopWidth;
        render();
      }

      requestAnimationFrame(tick);
    }

    buildClones();
    measure();
    render();
    requestAnimationFrame(tick);

    marquee.addEventListener("mouseenter", () => (running = false));
    marquee.addEventListener("mouseleave", () => (running = true));

    let touchPause = false;
    marquee.addEventListener(
      "touchstart",
      () => {
        touchPause = true;
        running = false;
      },
      { passive: true }
    );
    marquee.addEventListener(
      "touchend",
      () => {
        if (touchPause) running = true;
        touchPause = false;
      },
      { passive: true }
    );
    marquee.addEventListener(
      "touchcancel",
      () => {
        if (touchPause) running = true;
        touchPause = false;
      },
      { passive: true }
    );

    const re = () => {
      measure();
      setStartAt3();
    };
    window.addEventListener("resize", re);
    window.addEventListener("orientationchange", () => setTimeout(re, 200));
    setTimeout(re, 250);
    setTimeout(re, 1000);
  }

  function initProcessAccordion() {
    const root = document.getElementById("process");
    if (!root || root.dataset.bound === "true") return;
    root.dataset.bound = "true";

    const steps = root.querySelectorAll(".process-accordion details.step");
    steps.forEach(d => {
      d.addEventListener("toggle", () => {
        if (!d.open) return;
        steps.forEach(other => {
          if (other !== d) other.removeAttribute("open");
        });
      });
    });
  }

  function initFaqAccordion() {
    const faq = document.getElementById("faq");
    if (!faq || faq.dataset.bound === "true") return;
    faq.dataset.bound = "true";

    const items = faq.querySelectorAll("details");
    items.forEach(item => {
      item.addEventListener("toggle", () => {
        if (!item.open) return;
        items.forEach(other => {
          if (other !== item) other.removeAttribute("open");
        });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", initHome);
  document.addEventListener("page:load", initHome);
})();
