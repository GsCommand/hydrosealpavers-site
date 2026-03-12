/* include.js
   Static HTML includes loader (idempotent).
*/

(async function () {
  if (window.__hs_includes_ran) return;
  window.__hs_includes_ran = true;

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
