(function(){
  if(location.pathname.replace(/\/$/,'')!=='/paver-sealing/driveways') return;
  if(document.documentElement.dataset.drivewayRedesign==='1') return;
  document.documentElement.dataset.drivewayRedesign='1';

  function addStyles(){
    if(!document.querySelector('link[data-driveway-redesign]')){
      var link=document.createElement('link');
      link.rel='stylesheet';
      link.href='/assets/css/driveway-redesign.css?v=20260803-1';
      link.setAttribute('data-driveway-redesign','');
      document.head.appendChild(link);
    }
  }

  function buildHero(){
    var oldHero=document.querySelector('main#page section.hero2');
    if(!oldHero) return;

    var hero=document.createElement('div');
    hero.innerHTML='\
<section class="driveway-home-hero">\
  <img class="driveway-home-hero__bg" src="/assets/hero/hydroseal-driveway.webp" width="1920" height="1080" alt="Professionally restored and sealed paver driveway in Jacksonville" loading="eager" decoding="async" fetchpriority="high">\
  <div class="driveway-home-hero__grid hs-modern-shell">\
    <div class="driveway-home-hero__glass">\
      <span class="driveway-home-hero__eyebrow">DRIVEWAY PAVER SEALING IN NORTHEAST FLORIDA</span>\
      <h1>Driveway Paver Sealing Jacksonville &amp; St. Johns County</h1>\
      <h2>Cleaned. Resanded. Sealed. Built for Florida Driveways.</h2>\
      <p>Professional driveway paver sealing with deep cleaning, ASTM C144 joint sand, breathable sealer, and careful preparation across Jacksonville, St. Johns County, and Clay County.</p>\
      <div class="driveway-home-hero__actions">\
        <a class="driveway-home-hero__primary" href="/get-a-quote">Request a Quote</a>\
        <a class="driveway-home-hero__secondary" href="/paver-sealing-cost-calculator">Try Instant Pricing</a>\
      </div>\
    </div>\
    <div class="driveway-home-hero__proof">\
      <article class="driveway-home-review">\
        <div class="driveway-home-review__google">Google</div>\
        <div class="driveway-home-review__stars" aria-label="Five stars">★★★★★</div>\
        <h3>5-STAR RATED DRIVEWAY RESTORATION.</h3>\
        <p>Homeowners choose HydroSeal when faded, dirty driveway pavers need more than a quick pressure wash.</p>\
        <a href="https://share.google/4ddHhmrSn3woAYR6h" target="_blank" rel="noopener noreferrer">Read customer reviews →</a>\
      </article>\
      <div class="driveway-home-certified">TRIDENT MASTER CERTIFIED</div>\
    </div>\
  </div>\
</section>\
<section class="driveway-home-features hs-modern-shell" aria-label="Driveway sealing service standards">\
  <article><h3>DEEP CLEANING</h3><p>Surface preparation before sealing.</p></article>\
  <article><h3>JOINT SAND</h3><p>ASTM C144 kiln-dried sand.</p></article>\
  <article><h3>BREATHABLE SEALER</h3><p>Two controlled coats for Florida conditions.</p></article>\
  <article><h3>2-YEAR WARRANTY</h3><p>Covered workmanship and adhesion.</p></article>\
</section>\
<nav class="driveway-home-breadcrumb" aria-label="Breadcrumb">\
  <div class="hs-modern-shell"><a href="/">Home</a><span>›</span><a href="/paver-sealing">Paver Sealing</a><span>›</span><span aria-current="page">Driveways</span></div>\
</nav>';

    var nodes=Array.prototype.slice.call(hero.childNodes);
    oldHero.replaceWith.apply(oldHero,nodes);

    ['.trustbar','.breadcrumb','[data-include="/partials/reminder-badges.html"]'].forEach(function(selector){
      document.querySelectorAll('body > '+selector+', body > main + '+selector).forEach(function(el){el.remove();});
    });
  }

  function addResults(){
    if(document.querySelector('.driveway-results')) return;
    var heading=Array.prototype.find.call(document.querySelectorAll('h2'),function(h){return h.textContent.trim()==='Driveway Sealing in Jacksonville, FL';});
    if(!heading) return;
    var section=heading.closest('section');
    if(!section) return;

    var results=document.createElement('section');
    results.className='driveway-results';
    results.innerHTML='\
<div class="driveway-results__head">\
  <span>REAL HYDROSEAL DRIVEWAY RESULTS</span>\
  <h2>From faded and weathered to clean, protected, and finished.</h2>\
  <p>These Northeast Florida driveway projects show the difference proper cleaning, fresh joint sand, and a controlled sealing system can make.</p>\
</div>\
<div class="driveway-results__grid">\
  <figure class="driveway-results__card driveway-results__card--wide">\
    <img src="/assets/hero/driveway-before-after-hydroseal.webp" alt="Before and after driveway paver sealing by HydroSeal" loading="lazy" decoding="async">\
    <figcaption><strong>Driveway Color Restoration</strong><span>Deep cleaning, joint restoration, and sealing brought the original paver color back.</span></figcaption>\
  </figure>\
  <figure class="driveway-results__card driveway-results__card--portrait">\
    <img src="/assets/hero/ponte-vedra-driveway-before-after.webp" alt="Before and after Ponte Vedra driveway paver sealing" loading="lazy" decoding="async">\
    <figcaption><strong>Ponte Vedra Driveway Sealing</strong><span>A cleaner, more uniform finish designed for Florida sun, rain, and vehicle traffic.</span></figcaption>\
  </figure>\
</div>';
    section.insertAdjacentElement('afterend',results);
  }

  function run(){addStyles();buildHero();addResults();}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run,{once:true});
  else run();
})();
