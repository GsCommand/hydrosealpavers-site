(function(){
  'use strict';

  var SCRIPT_VERSION = '2026-09-03';
  var FULL_CALCULATOR = 'https://hydrosealpavers.com/paver-sealing-cost-calculator?utm_source=embed&utm_medium=widget&utm_campaign=paver_cost_widget';

  function money(value){
    return new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(value);
  }

  function mount(host){
    if (!host || host.dataset.hydrosealMounted === 'true') return;
    host.dataset.hydrosealMounted = 'true';

    var root = host.attachShadow ? host.attachShadow({mode:'open'}) : host;
    var wrap = document.createElement('div');
    wrap.innerHTML = `
      <style>
        :host{all:initial}
        *{box-sizing:border-box}
        .hsw{--navy:#0b2d4a;--blue:#0f6ea8;--sky:#39bfea;--ink:#183247;--muted:#627786;--line:#dce7ed;--soft:#f4f9fb;font-family:Arial,Helvetica,sans-serif;width:100%;max-width:680px;margin:0 auto;color:var(--ink)}
        .card{overflow:hidden;border:1px solid var(--line);border-radius:22px;background:#fff;box-shadow:0 16px 42px rgba(11,45,74,.10)}
        .head{padding:24px;background:linear-gradient(135deg,#0b2d4a,#0f6ea8);color:#fff}
        .eyebrow{margin:0 0 7px;font-size:11px;font-weight:900;letter-spacing:1.3px;text-transform:uppercase;color:#9ee5f7}
        h2{margin:0;font-size:26px;line-height:1.06;color:#fff}
        .head p{margin:9px 0 0;color:#d9edf6;font-size:14px;line-height:1.55}
        .body{padding:22px}
        .grid{display:grid;grid-template-columns:1fr 1fr;gap:13px}
        label{display:block;margin:0 0 6px;font-size:12px;font-weight:900;color:var(--navy)}
        input,select{width:100%;min-height:48px;padding:11px 12px;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--ink);font:inherit;font-size:15px;outline:none}
        input:focus,select:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(15,110,168,.10)}
        .result{margin-top:17px;padding:19px;border-radius:16px;background:var(--soft);border:1px solid #d9ebf3}
        .result small{display:block;color:var(--muted);font-size:12px}
        .price{display:block;margin:5px 0;color:var(--navy);font-size:32px;font-weight:950;letter-spacing:-1px}
        .sub{color:var(--muted);font-size:12px;line-height:1.5}
        .actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
        .btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:11px 16px;border-radius:999px;background:var(--blue);color:#fff!important;text-decoration:none;font-size:12px;font-weight:900;letter-spacing:.4px}
        .brand{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-top:16px;padding-top:14px;border-top:1px solid var(--line);color:var(--muted);font-size:11px;line-height:1.4}
        .brand a{color:var(--blue);font-weight:800;text-decoration:none}
        .note{margin:11px 0 0;color:var(--muted);font-size:11px;line-height:1.5}
        @media(max-width:560px){.grid{grid-template-columns:1fr}.price{font-size:28px}.head,.body{padding:19px}}
      </style>
      <section class="hsw" aria-label="HydroSeal paver sealing cost estimator">
        <div class="card">
          <div class="head">
            <p class="eyebrow">Free planning tool</p>
            <h2>Paver Sealing Cost Estimator</h2>
            <p>Estimate a starting price from square footage and surface type. Final pricing depends on prep, repairs, staining, access, drainage and existing coatings.</p>
          </div>
          <div class="body">
            <div class="grid">
              <div>
                <label for="hsw-sqft-${Math.random().toString(36).slice(2)}">Approximate square feet</label>
                <input class="sqft" inputmode="numeric" type="number" min="1" step="25" value="800" aria-label="Approximate square feet">
              </div>
              <div>
                <label>Surface</label>
                <select class="surface" aria-label="Surface type">
                  <option value="1.50">Concrete or brick pavers — from $1.50/sq ft</option>
                  <option value="1.60">Travertine / natural stone — from $1.60/sq ft</option>
                </select>
              </div>
            </div>
            <div class="result" aria-live="polite">
              <small>Published starting estimate</small>
              <strong class="price">$1,200</strong>
              <span class="sub">Based on HydroSeal's published starting rate. This is not a final quote.</span>
            </div>
            <div class="actions">
              <a class="btn" href="${FULL_CALCULATOR}" target="_blank" rel="nofollow noopener">Open Full Calculator</a>
            </div>
            <p class="note">Failed sealer removal, specialty stain treatment, repairs and unusual access conditions require separate review.</p>
            <div class="brand"><span>Tool by HydroSeal · Northeast Florida</span><a href="https://hydrosealpavers.com/" target="_blank" rel="nofollow noopener">hydrosealpavers.com</a></div>
          </div>
        </div>
      </section>`;

    root.appendChild(wrap);
    var sqft = root.querySelector('.sqft');
    var surface = root.querySelector('.surface');
    var price = root.querySelector('.price');

    function recalc(){
      var area = Math.max(0, Number(sqft.value || 0));
      var rate = Number(surface.value || 1.5);
      price.textContent = area ? money(area * rate) : '$0';
    }

    sqft.addEventListener('input', recalc);
    surface.addEventListener('change', recalc);
    recalc();
  }

  function boot(){
    document.querySelectorAll('[data-hydroseal-cost-widget]').forEach(mount);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, {once:true});
  else boot();

  window.HydroSealPaverCostWidget = {version:SCRIPT_VERSION,mount:mount};
})();
