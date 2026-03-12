(function () {
  function initSingleAccordions() {
    const roots = document.querySelectorAll('[data-accordion="single"]');

    roots.forEach(root => {
      if (root.dataset.bound === "true") return;
      root.dataset.bound = "true";

      const items = root.querySelectorAll("details");
      items.forEach(item => {
        item.addEventListener("toggle", () => {
          if (!item.open) return;
          items.forEach(other => {
            if (other !== item) other.removeAttribute("open");
          });
        });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", initSingleAccordions);
  document.addEventListener("page:load", initSingleAccordions);
})();
