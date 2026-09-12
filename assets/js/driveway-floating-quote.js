(function () {
  var path = location.pathname.replace(/\/$/, '');
  if (path !== '/paver-sealing/driveways') return;

  var desktopOnly = window.matchMedia('(min-width:1181px) and (hover:hover) and (pointer:fine)');
  if (!desktopOnly.matches) return;
  if (sessionStorage.getItem('hsDrivewayQuoteDismissedV2') === '1') return;
  if (document.querySelector('.driveway-floating-quote')) return;

  var style = document.createElement('style');
  style.id = 'driveway-floating-quote-style';
  style.textContent = [
    '.driveway-floating-quote{position:fixed;right:32px;top:52%;z-index:120;width:304px;padding:27px 22px 18px;border:1px solid rgba(15,110,168,.13);border-radius:17px;background:rgba(255,255,255,.97);box-shadow:0 16px 42px rgba(11,45,74,.15);color:#0b2d4a;opacity:0;pointer-events:none;overflow:hidden;transform:translate3d(22px,-45%,0);transition:opacity .24s ease,transform .24s ease,box-shadow .2s ease;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}',
    '.driveway-floating-quote:before{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:linear-gradient(90deg,#0f6ea8,#39bfea)}',
    '.driveway-floating-quote.is-visible{opacity:1;pointer-events:auto;transform:translate3d(0,-50%,0)}',
    '.driveway-floating-quote:hover{box-shadow:0 20px 48px rgba(11,45,74,.19)}',
    '.driveway-floating-quote__close{position:absolute;top:11px;right:11px;display:grid;place-items:center;width:25px;height:25px;border:0;border-radius:999px;background:transparent;color:#8a9aaa;font-size:18px;line-height:1;cursor:pointer;transition:background .16s ease,color .16s ease}',
    '.driveway-floating-quote__close:hover,.driveway-floating-quote__close:focus-visible{background:#eef5f8;color:#0b2d4a}',
    '.driveway-floating-quote__eyebrow{margin:0 34px 7px 0;color:#0f6ea8;font-size:10.5px;font-weight:950;letter-spacing:1.35px;text-transform:uppercase}',
    '.driveway-floating-quote h3{margin:0 0 10px;color:#0b2d4a;font-family:"Arial Black",Arial,sans-serif;font-size:21px;line-height:1.12;letter-spacing:-.42px}',
    '.driveway-floating-quote__copy{margin:0 0 16px;color:#526577;font-size:13.5px;line-height:1.48}',
    '.driveway-floating-quote__button{display:flex;align-items:center;justify-content:center;width:100%;min-height:48px;padding:12px 16px;border-radius:12px;background:#31b9e6;color:#fff!important;font-size:12.5px;font-weight:950;letter-spacing:.8px;text-decoration:none!important;text-transform:uppercase;box-shadow:0 8px 19px rgba(49,185,230,.25);transition:background .16s ease,transform .16s ease,box-shadow .16s ease}',
    '.driveway-floating-quote__button:hover,.driveway-floating-quote__button:focus-visible{background:#1faddd;transform:translateY(-1px);box-shadow:0 11px 23px rgba(49,185,230,.31)}',
    '.driveway-floating-quote__phone{display:block;margin-top:12px;color:#0b2d4a!important;font-size:12.5px;font-weight:900;text-align:center;text-decoration:none!important}',
    '.driveway-floating-quote__phone span{color:#66798a;font-weight:750}',
    '.driveway-floating-quote__phone:hover,.driveway-floating-quote__phone:focus-visible{color:#0f6ea8!important}',
    '.driveway-floating-quote__trust{margin-top:13px;padding-top:12px;border-top:1px solid #e7eef2;color:#5f7283;font-size:10.8px;font-weight:850;line-height:1.3;text-align:center;white-space:nowrap}',
    '.driveway-floating-quote__stars{color:#0f6ea8;letter-spacing:.45px}',
    '@media(max-width:1180px),(hover:none),(pointer:coarse){.driveway-floating-quote{display:none!important}}',
    '@media(prefers-reduced-motion:reduce){.driveway-floating-quote,.driveway-floating-quote__button,.driveway-floating-quote__close{transition:none!important}}'
  ].join('');
  document.head.appendChild(style);

  var box = document.createElement('aside');
  box.className = 'driveway-floating-quote';
  box.setAttribute('aria-label', 'Free driveway estimate');
  box.innerHTML = [
    '<button class="driveway-floating-quote__close" type="button" aria-label="Dismiss quote box">×</button>',
    '<p class="driveway-floating-quote__eyebrow">Free Driveway Estimate</p>',
    '<h3>Get a fast quote for your driveway.</h3>',
    '<p class="driveway-floating-quote__copy">Send 2–3 photos and approximate square footage. We\'ll review the project and get back to you.</p>',
    '<a class="driveway-floating-quote__button" href="/get-a-quote">Get My Quote&nbsp; →</a>',
    '<a class="driveway-floating-quote__phone" href="tel:+19045375000">904.537.5000 <span>· Call or text</span></a>',
    '<div class="driveway-floating-quote__trust"><span class="driveway-floating-quote__stars">★★★★★</span> Google Rated&nbsp; · &nbsp;2-Year Warranty</div>'
  ].join('');
  document.body.appendChild(box);

  var close = box.querySelector('.driveway-floating-quote__close');
  if (close) {
    close.addEventListener('click', function () {
      sessionStorage.setItem('hsDrivewayQuoteDismissedV2', '1');
      box.classList.remove('is-visible');
      window.setTimeout(function () { box.remove(); }, 220);
    });
  }

  var hero = document.querySelector('.dw-hero');
  if (!hero) return;

  function update() {
    var rect = hero.getBoundingClientRect();
    box.classList.toggle('is-visible', rect.bottom < 120);
  }

  update();
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
})();
