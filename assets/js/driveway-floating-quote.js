(function () {
  var path = location.pathname.replace(/\/$/, '');
  if (path !== '/paver-sealing/driveways') return;

  var desktopOnly = window.matchMedia('(min-width:1181px) and (hover:hover) and (pointer:fine)');
  if (!desktopOnly.matches) return;
  if (sessionStorage.getItem('hsDrivewayQuoteDismissed') === '1') return;
  if (document.querySelector('.driveway-floating-quote')) return;

  var style = document.createElement('style');
  style.id = 'driveway-floating-quote-style';
  style.textContent = [
    '.driveway-floating-quote{position:fixed;right:26px;top:52%;z-index:120;width:268px;padding:19px 19px 17px;border:1px solid rgba(15,110,168,.14);border-radius:24px;background:rgba(255,255,255,.94);box-shadow:0 18px 48px rgba(11,45,74,.16);color:#0b2d4a;opacity:0;pointer-events:none;transform:translate3d(20px,-44%,0);transition:opacity .24s ease,transform .24s ease,box-shadow .2s ease;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}',
    '.driveway-floating-quote.is-visible{opacity:1;pointer-events:auto;transform:translate3d(0,-50%,0)}',
    '.driveway-floating-quote:hover{box-shadow:0 22px 54px rgba(11,45,74,.20)}',
    '.driveway-floating-quote__close{position:absolute;top:10px;right:10px;display:grid;place-items:center;width:28px;height:28px;border:0;border-radius:999px;background:#f1f5f7;color:#607487;font-size:18px;line-height:1;cursor:pointer;transition:background .16s ease,color .16s ease,transform .16s ease}',
    '.driveway-floating-quote__close:hover,.driveway-floating-quote__close:focus-visible{background:#e4eef3;color:#0b2d4a;transform:scale(1.04)}',
    '.driveway-floating-quote__brand{display:flex;align-items:center;min-height:34px;margin:0 34px 11px 0}',
    '.driveway-floating-quote__logo{display:block;width:112px;height:auto;max-height:44px;object-fit:contain;object-position:left center}',
    '.driveway-floating-quote__eyebrow{margin:0 0 6px;color:#0f6ea8;font-size:10px;font-weight:950;letter-spacing:1.25px;text-transform:uppercase}',
    '.driveway-floating-quote h3{margin:0 0 8px;color:#0b2d4a;font-family:"Arial Black",Arial,sans-serif;font-size:24px;line-height:1.03;letter-spacing:-.55px}',
    '.driveway-floating-quote__copy{margin:0 0 15px;color:#536475;font-size:13.5px;line-height:1.5}',
    '.driveway-floating-quote__button{display:flex;align-items:center;justify-content:center;width:100%;min-height:47px;padding:12px 15px;border-radius:999px;background:#39bfea;color:#fff!important;font-size:12px;font-weight:950;letter-spacing:.72px;text-decoration:none!important;text-transform:uppercase;box-shadow:0 9px 22px rgba(57,191,234,.26);transition:background .16s ease,transform .16s ease,box-shadow .16s ease}',
    '.driveway-floating-quote__button:hover,.driveway-floating-quote__button:focus-visible{background:#2eb3df;transform:translateY(-1px);box-shadow:0 12px 26px rgba(57,191,234,.32)}',
    '.driveway-floating-quote__phone{display:block;margin-top:11px;color:#0b2d4a!important;font-size:11.5px;font-weight:850;text-align:center;text-decoration:none!important}',
    '.driveway-floating-quote__phone:hover,.driveway-floating-quote__phone:focus-visible{color:#0f6ea8!important;text-decoration:underline!important;text-underline-offset:3px}',
    '.driveway-floating-quote__trust{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 10px;margin-top:13px;padding-top:12px;border-top:1px solid #e4edf1;color:#627688;font-size:10.5px;font-weight:800;line-height:1.25}',
    '.driveway-floating-quote__trust span{white-space:nowrap}',
    '.driveway-floating-quote__trust span:before{content:"✓";margin-right:4px;color:#0f6ea8;font-weight:950}',
    '@media(max-width:1180px),(hover:none),(pointer:coarse){.driveway-floating-quote{display:none!important}}',
    '@media(prefers-reduced-motion:reduce){.driveway-floating-quote,.driveway-floating-quote__button,.driveway-floating-quote__close{transition:none!important}}'
  ].join('');
  document.head.appendChild(style);

  var box = document.createElement('aside');
  box.className = 'driveway-floating-quote';
  box.setAttribute('aria-label', 'Quick driveway estimate');
  box.innerHTML = [
    '<button class="driveway-floating-quote__close" type="button" aria-label="Dismiss quote box">×</button>',
    '<div class="driveway-floating-quote__brand"><img class="driveway-floating-quote__logo" src="/assets/hero/Hydrosealpaversealing.png" alt="HydroSeal" loading="lazy" decoding="async"></div>',
    '<p class="driveway-floating-quote__eyebrow">Quick Driveway Estimate</p>',
    '<h3>Ready for a quote?</h3>',
    '<p class="driveway-floating-quote__copy">Send a few photos and your approximate square footage for a quick project review.</p>',
    '<a class="driveway-floating-quote__button" href="/get-a-quote">Get a Quote</a>',
    '<a class="driveway-floating-quote__phone" href="tel:+19045375000">Call or text 904.537.5000</a>',
    '<div class="driveway-floating-quote__trust"><span>5-star rated</span><span>2-year workmanship warranty</span></div>'
  ].join('');
  document.body.appendChild(box);

  var close = box.querySelector('.driveway-floating-quote__close');
  if (close) {
    close.addEventListener('click', function () {
      sessionStorage.setItem('hsDrivewayQuoteDismissed', '1');
      box.classList.remove('is-visible');
      window.setTimeout(function () { box.remove(); }, 220);
    });
  }

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
