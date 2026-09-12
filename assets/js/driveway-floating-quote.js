(function () {
  var path = location.pathname.replace(/\/$/, '');
  if (path !== '/paver-sealing/driveways') return;
  if (document.querySelector('.driveway-floating-quote')) return;

  var style = document.createElement('style');
  style.id = 'driveway-floating-quote-style';
  style.textContent = [
    '.driveway-floating-quote{position:fixed;right:22px;top:52%;z-index:120;width:226px;padding:18px;border:1px solid rgba(255,255,255,.65);border-radius:22px;background:linear-gradient(145deg,rgba(11,54,88,.97),rgba(15,110,168,.96));box-shadow:0 18px 46px rgba(5,32,51,.28);color:#fff;opacity:0;pointer-events:none;transform:translate3d(18px,-44%,0);transition:opacity .24s ease,transform .24s ease;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}',
    '.driveway-floating-quote.is-visible{opacity:1;pointer-events:auto;transform:translate3d(0,-50%,0)}',
    '.driveway-floating-quote__eyebrow{margin:0 0 6px;color:#a9edff;font-size:10px;font-weight:950;letter-spacing:1.35px;text-transform:uppercase}',
    '.driveway-floating-quote h3{margin:0 0 7px;color:#fff;font-family:"Arial Black",Arial,sans-serif;font-size:22px;line-height:1.04;letter-spacing:-.45px}',
    '.driveway-floating-quote__copy{margin:0 0 14px;color:rgba(255,255,255,.86);font-size:12.5px;line-height:1.45}',
    '.driveway-floating-quote__button{display:flex;align-items:center;justify-content:center;width:100%;min-height:44px;padding:11px 14px;border-radius:999px;background:#39bfea;color:#fff!important;font-size:12px;font-weight:950;letter-spacing:.7px;text-decoration:none!important;text-transform:uppercase;box-shadow:0 10px 24px rgba(57,191,234,.30)}',
    '.driveway-floating-quote__button:hover,.driveway-floating-quote__button:focus-visible{background:#56c9eb;transform:translateY(-1px)}',
    '.driveway-floating-quote__phone{display:block;margin-top:10px;color:#fff!important;font-size:11px;font-weight:850;text-align:center;text-decoration:none!important}',
    '.driveway-floating-quote__phone:hover,.driveway-floating-quote__phone:focus-visible{text-decoration:underline!important;text-underline-offset:3px}',
    '@media(max-width:1180px){.driveway-floating-quote{display:none!important}}',
    '@media(prefers-reduced-motion:reduce){.driveway-floating-quote{transition:none!important}}'
  ].join('');
  document.head.appendChild(style);

  var box = document.createElement('aside');
  box.className = 'driveway-floating-quote';
  box.setAttribute('aria-label', 'Free paver sealing estimate');
  box.innerHTML = [
    '<p class="driveway-floating-quote__eyebrow">Free Estimate</p>',
    '<h3>Ready for a quote?</h3>',
    '<p class="driveway-floating-quote__copy">Send photos and approximate square footage for a quick project review.</p>',
    '<a class="driveway-floating-quote__button" href="/get-a-quote">Get a Quote</a>',
    '<a class="driveway-floating-quote__phone" href="tel:+19045375000">Call or text 904.537.5000</a>'
  ].join('');
  document.body.appendChild(box);

  var hero = document.querySelector('.dw-hero');
  if (!hero) return;

  function update() {
    var rect = hero.getBoundingClientRect();
    box.classList.toggle('is-visible', rect.bottom < 140);
  }

  update();
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
})();
