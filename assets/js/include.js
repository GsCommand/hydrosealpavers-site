/* include.js
   Static HTML includes loader (idempotent).
*/

(async function () {
  if (window.__hs_includes_ran) return;
  window.__hs_includes_ran = true;

  // Prevent the browser's temporary mouse-focus outline from flashing in the
  // upper-left corner while navigating between Learning Center pages. Keyboard
  // focus remains unchanged for accessibility.
  if (document.body.classList.contains("page-learning-center")) {
    document.addEventListener(
      "pointerup",
      (event) => {
        if (event.pointerType && event.pointerType !== "mouse" && event.pointerType !== "pen") return;
        const link = event.target.closest("a[href]");
        if (link && document.body.contains(link)) link.blur();
      },
      true
    );
  }

  function applyLearningCenterFaqAccordions() {
    if (!document.body.classList.contains("page-learning-center")) return;

    const currentPath = location.pathname.replace(/\/$/, "");
    const enabledSections = [
      "/learning-center/cleaning/",
      "/learning-center/cost/",
      "/learning-center/hiring/",
      "/learning-center/local/",
      "/learning-center/maintenance/",
      "/learning-center/problems/",
      "/learning-center/sealing/",
      "/learning-center/surfaces/",
      "/learning-center/travertine/"
    ];
    if (!enabledSections.some((prefix) => currentPath.startsWith(prefix))) return;

    if (!document.getElementById("hs-learning-center-faq-accordion-style")) {
      const style = document.createElement("style");
      style.id = "hs-learning-center-faq-accordion-style";
      style.textContent = `
        .page-learning-center .hs-lc-faq-accordion{margin-top:18px}
        .page-learning-center .hs-lc-faq-item{margin:0 0 10px;border:1px solid #dce3e9;border-radius:14px;background:#fff;overflow:hidden;box-shadow:0 5px 16px rgba(11,45,74,.05)}
        .page-learning-center .hs-lc-faq-item summary{position:relative;display:block;cursor:pointer;list-style:none;padding:17px 50px 17px 18px;color:#0b2d4a;font-weight:800;line-height:1.4}
        .page-learning-center .hs-lc-faq-item summary::-webkit-details-marker{display:none}
        .page-learning-center .hs-lc-faq-item summary::after{content:'+';position:absolute;right:18px;top:50%;transform:translateY(-50%);font-size:24px;font-weight:500;color:#0f6ea8}
        .page-learning-center .hs-lc-faq-item[open] summary::after{content:'−'}
        .page-learning-center .hs-lc-faq-item summary:focus-visible{outline:3px solid rgba(15,110,168,.28);outline-offset:-3px}
        .page-learning-center .hs-lc-faq-answer{padding:0 18px 18px;color:#536475;line-height:1.7}
        .page-learning-center .hs-lc-faq-answer>:first-child{margin-top:0}
        .page-learning-center .hs-lc-faq-answer>:last-child{margin-bottom:0}
      `;
      document.head.appendChild(style);
    }

    const sections = Array.from(document.querySelectorAll(".blog-post__content section"));
    sections.forEach((section) => {
      const heading = section.querySelector(":scope > h2");
      if (!heading || !/^(frequently asked questions|common questions|faq)$/i.test(heading.textContent.trim())) return;
      if (section.dataset.hsFaqAccordion === "1") return;

      const existingDetails = Array.from(section.querySelectorAll(":scope > details"));
      if (existingDetails.length) {
        section.classList.add("hs-lc-faq-accordion");
        existingDetails.forEach((details) => details.classList.add("hs-lc-faq-item"));
        section.dataset.hsFaqAccordion = "1";
        return;
      }

      const questions = Array.from(section.querySelectorAll(":scope > h3"));
      if (!questions.length) return;

      section.classList.add("hs-lc-faq-accordion");
      questions.forEach((question) => {
        if (!question.parentNode) return;
        const details = document.createElement("details");
        details.className = "hs-lc-faq-item";
        const summary = document.createElement("summary");
        summary.textContent = question.textContent.trim();
        const answer = document.createElement("div");
        answer.className = "hs-lc-faq-answer";

        let sibling = question.nextSibling;
        while (sibling) {
          const next = sibling.nextSibling;
          if (sibling.nodeType === 1 && (sibling.tagName === "H3" || sibling.tagName === "H2")) break;
          answer.appendChild(sibling);
          sibling = next;
        }

        question.parentNode.insertBefore(details, question);
        details.append(summary, answer);
        question.remove();
      });
      section.dataset.hsFaqAccordion = "1";
    });
  }

  function addTravertineCleaningImage() {
    const currentPath = location.pathname.replace(/\/$/, "");
    if (currentPath !== "/learning-center/travertine/how-to-clean-travertine-without-damage") return;
    if (document.querySelector(".hs-travertine-cleaning-photo")) return;

    const sections = Array.from(document.querySelectorAll(".blog-post__content > section"));
    const processSection = sections.find((section) => {
      const h2 = section.querySelector(":scope > h2");
      return h2 && h2.textContent.trim().toLowerCase() === "7-step travertine cleaning process";
    });
    if (!processSection || !processSection.parentNode) return;

    const figure = document.createElement("figure");
    figure.className = "hs-travertine-cleaning-photo";
    figure.style.margin = "28px 0 30px";
    figure.innerHTML = '<img src="/assets/hero/travertine-cleaning-before-after.svg" alt="Before and after travertine cleaning project" loading="lazy" style="display:block;width:100%;height:auto;border-radius:18px;">';
    processSection.parentNode.insertBefore(figure, processSection);
  }

  function restoreLearningCenterElfsightGallery() {
    if (!document.body.classList.contains("page-learning-center")) return;
    if (!document.querySelector(".elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26")) return;
    if (document.getElementById("hs-lc-elfsight-gallery-style")) return;

    const style = document.createElement("style");
    style.id = "hs-lc-elfsight-gallery-style";
    style.textContent = `
      .page-learning-center .blog-post .elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26{display:block!important;min-height:260px!important;margin:28px 0 34px!important}
      .page-learning-center .blog-post .elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26 img,
      .page-learning-center .blog-post .elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26 figure,
      .page-learning-center .blog-post .elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26 picture,
      .page-learning-center .blog-post .elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26 svg{display:block!important;visibility:visible!important;opacity:1!important}
      .page-learning-center .blog-post .elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26 iframe{display:block!important;width:100%!important;min-height:260px!important}
    `;
    document.head.appendChild(style);
  }

  applyLearningCenterFaqAccordions();
  addTravertineCleaningImage();
  restoreLearningCenterElfsightGallery();

  document.body.classList.add("includes-loading");

  try {
    // Execute scripts inside a root element by replacing each <script> with a fresh one.
    function runScripts(root) {
      const scripts = Array.from(root.querySelectorAll("script"));

      scripts.forEach((oldScript) => {
        if (oldScript.dataset && oldScript.dataset.includedRan === "1") return;

        const s = document.createElement("script");
        for (const attr of Array.from(oldScript.attributes)) {
          s.setAttribute(attr.name, attr.value);
        }

        s.dataset.includedRan = "1";

        if (!oldScript.src) {
          s.textContent = oldScript.textContent || "";
        }

        oldScript.replaceWith(s);
      });
    }

    // 1) Load includes in parallel, then replace placeholders in DOM order.
    const placeholders = Array.from(document.querySelectorAll("[data-include]"));
    const includeResults = await Promise.all(
      placeholders.map(async (placeholder) => {
        const url = placeholder.getAttribute("data-include");

        try {
          const res = await fetch(url);
          if (!res.ok) throw new Error("Fetch failed: " + url);

          const html = await res.text();
          const wrap = document.createElement("div");
          wrap.className = "include-root";
          wrap.innerHTML = html;

          // Run scripts only within newly included subtree.
          runScripts(wrap);

          const frag = document.createDocumentFragment();
          while (wrap.firstChild) frag.appendChild(wrap.firstChild);

          return { placeholder, url, frag };
        } catch (err) {
          return { placeholder, url, err };
        }
      })
    );

    includeResults.forEach(({ placeholder, url, frag, err }) => {
      if (err) {
        console.error(err);
        placeholder.outerHTML = "<!-- include failed: " + url + " -->";
        return;
      }

      placeholder.replaceChildren();
      placeholder.appendChild(frag);
      placeholder.removeAttribute("data-include");
      placeholder.classList.add("is-loaded");
    });

    // Learning Center pages use the shared footer without the brand/description
    // block so Contact remains aligned with the other footer columns.
    if (document.body.classList.contains("page-learning-center")) {
      document.querySelectorAll("footer .footer-brand").forEach((brand) => brand.remove());
    }

    await new Promise((r) => setTimeout(r, 0));

    // 2) Back-compat: run ONLY scripts explicitly marked
    const includeScripts = document.querySelectorAll('script[data-run-on-include="true"]');
    includeScripts.forEach((oldScript) => {
      if (oldScript.dataset && oldScript.dataset.includedRan === "1") return;

      const s = document.createElement("script");
      for (const attr of Array.from(oldScript.attributes)) s.setAttribute(attr.name, attr.value);

      s.removeAttribute("data-run-on-include");
      s.dataset.includedRan = "1";

      if (oldScript.src) {
        s.src = oldScript.src;
      } else {
        s.textContent = oldScript.textContent || "";
      }

      oldScript.replaceWith(s);
    });


  } finally {
    document.body.classList.remove("includes-loading");
    document.body.classList.add("includes-ready");
    document.dispatchEvent(new Event("includes:ready"));
  }
})();
