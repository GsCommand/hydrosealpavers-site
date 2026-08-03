(function () {
  if (location.pathname.replace(/\/$/, '') !== '/paver-sealing/driveways') return;

  function installHomepageFooter() {
    fetch('/partials/footer.html', { cache: 'no-cache' })
      .then(function (response) {
        if (!response.ok) throw new Error('Footer request failed');
        return response.text();
      })
      .then(function (html) {
        var holder = document.createElement('div');
        holder.innerHTML = html;
        var homepageFooter = holder.querySelector('footer.site-footer');
        if (!homepageFooter) return;

        var currentFooter = document.querySelector('footer.driveway-homepage-footer, footer.site-footer, footer.footer');
        if (currentFooter) currentFooter.replaceWith(homepageFooter);
        else document.body.appendChild(homepageFooter);

        document.querySelectorAll('.mobile-contactbar').forEach(function (bar) { bar.remove(); });
        var mobileBar = holder.querySelector('.mobile-contactbar');
        if (mobileBar) document.body.appendChild(mobileBar);

        var year = document.getElementById('y');
        if (year) year.textContent = String(new Date().getFullYear());
      })
      .catch(function () {
        /* Keep the existing footer if the shared homepage footer cannot load. */
      });
  }

  function run() {
    window.setTimeout(installHomepageFooter, 60);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();
