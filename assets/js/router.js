/* router.js - lightweight shared page hooks */
(function () {
  function initSharedUi() {
    const y = document.getElementById("y");
    if (y) y.textContent = String(new Date().getFullYear());
  }

  initSharedUi();
  document.addEventListener("includes:ready", initSharedUi);
  document.dispatchEvent(new Event("page:load"));
})();
