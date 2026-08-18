(function () {
  const path = location.pathname.replace(/\/$/, '');

  function fixJointSandColorCards() {
    if (path !== '/learning-center/surfaces/what-is-the-best-sand-for-paver-joints-in-florida') return;

    if (!document.getElementById('hs-joint-sand-card-fix')) {
      const style = document.createElement('style');
      style.id = 'hs-joint-sand-card-fix';
      style.textContent = `
        .sand-color-options .hs-sand-card-link{display:block;height:100%;color:inherit!important;text-decoration:none!important;border-radius:16px}
        .sand-color-options .hs-sand-card-link:focus-visible{outline:3px solid rgba(15,110,168,.35);outline-offset:3px}
        .sand-color-options .sand-color-card{height:100%;transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}
        .sand-color-options .hs-sand-card-link:hover .sand-color-card{transform:translateY(-2px);box-shadow:0 12px 28px rgba(11,45,74,.14);border-color:rgba(15,110,168,.35)}
        .sand-color-options .hs-sand-card-photo{display:block!important;width:100%!important;aspect-ratio:1/1!important;min-height:120px!important;border-radius:12px;border:1px solid rgba(0,0,0,.12);background-size:cover!important;background-position:center!important;background-repeat:no-repeat!important}
      `;
      document.head.appendChild(style);
    }

    document.querySelectorAll('.sand-color-options .sand-color-card').forEach((card) => {
      if (card.dataset.hsSandFixed === '1') return;
      const img = card.querySelector('img');
      if (!img) return;

      const photo = document.createElement('span');
      photo.className = 'hs-sand-card-photo';
      photo.setAttribute('role', 'img');
      photo.setAttribute('aria-label', img.getAttribute('alt') || 'Paver joint sand color sample');
      photo.style.backgroundImage = `url("${img.getAttribute('src')}")`;
      img.replaceWith(photo);

      if (!card.parentElement || !card.parentElement.classList.contains('hs-sand-card-link')) {
        const link = document.createElement('a');
        link.className = 'hs-sand-card-link';
        link.href = '/paver-sealing/sand-options';
        link.setAttribute('aria-label', `${(card.querySelector('strong') || {}).textContent || 'Paver sand'} color options`);
        card.parentNode.insertBefore(link, card);
        link.appendChild(card);
      }

      card.dataset.hsSandFixed = '1';
    });
  }

  function styleLearningCenterCtas() {
    if (!document.body.classList.contains('page-learning-center')) return;
    const ctas = document.querySelectorAll('.blog-post__cta');
    if (!ctas.length) return;

    if (!document.getElementById('hs-learning-center-cta-pills')) {
      const style = document.createElement('style');
      style.id = 'hs-learning-center-cta-pills';
      style.textContent = `
        .page-learning-center .blog-post__cta h2{text-align:center!important;text-transform:capitalize!important}
        .page-learning-center .blog-post__cta>p{text-align:center!important}
        .page-learning-center .blog-post__cta .hs-cta-actions{display:flex!important;flex-wrap:wrap!important;gap:12px!important;align-items:center!important;justify-content:center!important;margin-top:18px!important;text-align:center!important}
        .page-learning-center .blog-post__cta .hs-cta-actions a{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:48px!important;padding:13px 20px!important;border-radius:999px!important;text-decoration:none!important;font-size:14px!important;font-weight:900!important;line-height:1!important;letter-spacing:.01em!important;transition:transform .18s ease,box-shadow .18s ease!important}
        .page-learning-center .blog-post__cta .hs-cta-call{background:#0b2d4a!important;color:#fff!important;border:1px solid #0b2d4a!important;box-shadow:0 8px 20px rgba(11,45,74,.16)!important}
        .page-learning-center .blog-post__cta .hs-cta-quote{background:#39bfea!important;color:#fff!important;border:1px solid #39bfea!important;box-shadow:0 8px 20px rgba(57,191,234,.24)!important}
        .page-learning-center .blog-post__cta .hs-cta-actions a:hover,.page-learning-center .blog-post__cta .hs-cta-actions a:focus-visible{transform:translateY(-1px)!important}
        @media(max-width:520px){.page-learning-center .blog-post__cta .hs-cta-actions a{width:100%!important}}
      `;
      document.head.appendChild(style);
    }

    ctas.forEach((cta) => {
      const heading = cta.querySelector('h2');
      if (heading) heading.style.textAlign = 'center';
      cta.querySelectorAll(':scope > p').forEach((p) => { p.style.textAlign = 'center'; });

      if (cta.querySelector('.hs-cta-actions')) return;

      const actionLinks = Array.from(cta.querySelectorAll('a')).filter((link) => {
        const href = (link.getAttribute('href') || '').toLowerCase();
        const text = link.textContent.trim().toLowerCase();
        return href.startsWith('tel:') || href.startsWith('sms:') || href === '/get-a-quote' || href.endsWith('/get-a-quote') || text === 'request a quote' || text.startsWith('text 904.537.5000') || text.startsWith('call 904.537.5000');
      });

      actionLinks.forEach((link) => {
        const parent = link.parentElement;
        link.remove();
        if (parent && parent.tagName === 'P') {
          const leftover = parent.textContent.replace(/[·•|]/g, '').trim();
          if (!leftover && !parent.querySelector('a')) parent.remove();
        }
      });

      const row = document.createElement('div');
      row.className = 'hs-cta-actions';

      const call = document.createElement('a');
      call.className = 'hs-cta-call';
      call.href = 'tel:+19045375000';
      call.textContent = 'Call 904.537.5000';

      const quote = document.createElement('a');
      quote.className = 'hs-cta-quote';
      quote.href = '/get-a-quote';
      quote.textContent = 'Request a Quote';

      row.append(call, quote);
      cta.appendChild(row);
    });
  }

  function styleHiringTemplateCtas() {
    const templatePages = new Map([
      ['/learning-center/sealing/is-paver-sealing-worth-it-in-florida', 'Need an Honest Paver Assessment?'],
      ['/learning-center/sealing/what-should-professional-paver-sealing-include', 'Compare a Clear Project Scope'],
      ['/learning-center/local/best-time-of-year-to-seal-pavers-in-florida', 'Need a Safe Sealing Window?']
    ]);
    if (!templatePages.has(path)) return;

    const cta = document.querySelector('.blog-post__cta');
    if (!cta) return;
    cta.classList.add('hs-hiring-template-cta');

    const heading = cta.querySelector('h2');
    if (heading) heading.textContent = templatePages.get(path);

    if (!document.getElementById('hs-hiring-template-cta-style')) {
      const style = document.createElement('style');
      style.id = 'hs-hiring-template-cta-style';
      style.textContent = `
        body.page-learning-center.blog-story-prototype .blog-post__cta.hs-hiring-template-cta{
          box-sizing:border-box!important;
          width:100%!important;
          max-width:none!important;
          margin:30px 0 32px!important;
          padding:30px!important;
          border:0!important;
          border-radius:22px!important;
          background:#0b2d4a!important;
          text-align:center!important;
          color:#fff!important;
        }
        body.page-learning-center.blog-story-prototype .blog-post__cta.hs-hiring-template-cta h2{
          margin:0 0 8px!important;
          color:#fff!important;
          text-align:center!important;
          text-transform:none!important;
        }
        body.page-learning-center.blog-story-prototype .blog-post__cta.hs-hiring-template-cta>p{
          margin:0!important;
          color:#dceef6!important;
          text-align:center!important;
        }
        body.page-learning-center.blog-story-prototype .blog-post__cta.hs-hiring-template-cta .hs-cta-actions{
          margin-top:15px!important;
        }
        body.page-learning-center.blog-story-prototype .blog-post__cta.hs-hiring-template-cta .hs-cta-call{
          background:#fff!important;
          color:#0b2d4a!important;
          border:1px solid #fff!important;
          box-shadow:none!important;
        }
        body.page-learning-center.blog-story-prototype .blog-post__cta.hs-hiring-template-cta .hs-cta-quote{
          background:#39bfea!important;
          color:#fff!important;
          border:1px solid #39bfea!important;
          box-shadow:none!important;
        }
        @media(max-width:520px){
          body.page-learning-center.blog-story-prototype .blog-post__cta.hs-hiring-template-cta{padding:26px 18px!important}
        }
      `;
      document.head.appendChild(style);
    }
  }

  function featureTopLearningCenterGuides() {
    if (path !== '/learning-center') return;
    if (document.querySelector('.hs-lc-popular-guides')) return;

    const featured = document.querySelector('.lc-featured');
    if (!featured || !featured.parentNode) return;

    if (!document.getElementById('hs-lc-popular-guides-style')) {
      const style = document.createElement('style');
      style.id = 'hs-lc-popular-guides-style';
      style.textContent = `
        .hs-lc-popular-guides{margin:0 0 26px}
        .hs-lc-popular-guides__heading{margin:0 0 14px;color:#0b2d4a;font-size:clamp(1.55rem,3vw,2rem);text-align:center}
      `;
      document.head.appendChild(style);
    }

    const section = document.createElement('section');
    section.className = 'hs-lc-popular-guides';
    section.setAttribute('aria-labelledby', 'hs-lc-popular-guides-title');
    section.innerHTML = `
      <h2 class="hs-lc-popular-guides__heading" id="hs-lc-popular-guides-title">Popular Guides</h2>
      <div class="lc-grid">
        <article class="lc-card">
          <p class="lc-card__category">Joint Sand</p>
          <h2><a href="/learning-center/surfaces/what-is-the-best-sand-for-paver-joints-in-florida">What Is the Best Sand for Paver Joints in Florida?</a></h2>
          <p>Compare joint-sand options, performance, installation considerations, and what matters most for Florida paver systems.</p>
          <a class="lc-card__link" href="/learning-center/surfaces/what-is-the-best-sand-for-paver-joints-in-florida">Read guide →</a>
        </article>
        <article class="lc-card">
          <p class="lc-card__category">Paver Problems</p>
          <h2><a href="/learning-center/problems/why-is-sand-coming-out-of-my-pavers">Why Is Sand Coming Out of My Pavers?</a></h2>
          <p>Understand washout, joint depth, drainage, cleaning pressure, and why sand can disappear from paver joints.</p>
          <a class="lc-card__link" href="/learning-center/problems/why-is-sand-coming-out-of-my-pavers">Read guide →</a>
        </article>
      </div>`;

    featured.parentNode.insertBefore(section, featured);
  }

  function spaceRebuiltTemplateCtas() {
    const rebuiltPages = new Set([
      '/learning-center/hiring/how-to-choose-a-paver-sealing-company-in-northeast-florida',
      '/learning-center/problems/cleaning-resealing-or-stripping'
    ]);
    if (!rebuiltPages.has(path)) return;
    const cta = document.querySelector('.cost-cta');
    if (cta) cta.style.marginBottom = '32px';
  }

  function positionLandingRecentJobs() {
    if (path !== '/landing') return;
    const title = document.querySelector('.lp-recent-jobs-title');
    const gallery = document.querySelector('.lp-pricing-gallery');
    const recentJobsWidget = document.querySelector('.elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26');
    const included = document.querySelector('.lp-included-section');
    if (!title || !gallery || !included || document.querySelector('.hs-recent-jobs-wrap')) return;

    const wrap = document.createElement('div');
    wrap.className = 'hs-recent-jobs-wrap';
    wrap.style.background = '#f8fafb';
    wrap.style.borderBottom = '1px solid rgba(0,0,0,.06)';

    const inner = document.createElement('div');
    inner.className = 'lp-section';
    inner.append(title, gallery);
    wrap.appendChild(inner);

    included.parentNode.insertBefore(wrap, included);
    if (recentJobsWidget) included.parentNode.insertBefore(recentJobsWidget, included);
  }

  fixJointSandColorCards();
  styleLearningCenterCtas();
  styleHiringTemplateCtas();
  featureTopLearningCenterGuides();
  spaceRebuiltTemplateCtas();
  positionLandingRecentJobs();

  if (path === '/learning-center/surfaces/what-is-the-best-sand-for-paver-joints-in-florida') {
    const cta = document.querySelector('.blog-post__cta');
    if (cta) {
      const heading = cta.querySelector('h2');
      if (heading) heading.textContent = 'Need Joint-Sand Restoration?';
    }
  }

  if (path === '/paver-sealing/pool-decks') {
    const gallery = document.querySelector('.elfsight-app-aac62a49-a425-47be-9c8a-13971e000940');
    const sandSection = document.querySelector('.sand-bar-section');
    const heroCopy = document.querySelector('.pool-service-hero__copy');

    if (gallery && sandSection && sandSection.parentNode) {
      sandSection.parentNode.insertBefore(gallery, sandSection);
    }

    if (heroCopy && heroCopy.textContent.includes('Professional pool deck sealing with deep cleaning')) {
      heroCopy.remove();
    }
  }

  if (window.__hsThirdPartyLoaderRan) {
    if (typeof window.__hsArmElfsight === 'function') window.__hsArmElfsight();
    return;
  }
  window.__hsThirdPartyLoaderRan = true;

  const WIDGET_SELECTOR = '[class*="elfsight-app-"]';
  const PLATFORM_SELECTOR = [
    'script[src="https://elfsightcdn.com/platform.js"]',
    'script[src="https://static.elfsight.com/platform/platform.js"]'
  ].join(',');

  let requested = false;
  let intersectionObserver = null;
  let mutationObserver = null;

  function hasWidget() {
    return !!document.querySelector(WIDGET_SELECTOR);
  }

  function loadElfsight() {
    if (!hasWidget()) return;
    if (requested || window.ELFSIGHT) return;

    if (document.querySelector(PLATFORM_SELECTOR)) {
      requested = true;
      return;
    }

    requested = true;
    const script = document.createElement('script');
    script.src = 'https://static.elfsight.com/platform/platform.js';
    script.async = true;
    script.defer = true;
    script.dataset.hsThirdParty = 'elfsight';
    document.head.appendChild(script);
  }

  function armElfsight() {
    const widget = document.querySelector(WIDGET_SELECTOR);
    if (!widget) return false;

    if (intersectionObserver) intersectionObserver.disconnect();

    if ('IntersectionObserver' in window) {
      intersectionObserver = new IntersectionObserver((entries) => {
        if (!entries.some((entry) => entry.isIntersecting || entry.intersectionRatio > 0)) return;
        intersectionObserver.disconnect();
        loadElfsight();
      }, { rootMargin: '300px 0px' });
      intersectionObserver.observe(widget);
    } else if ('requestIdleCallback' in window) {
      requestIdleCallback(loadElfsight, { timeout: 2500 });
    } else {
      setTimeout(loadElfsight, 1800);
    }

    return true;
  }

  window.__hsLoadElfsight = loadElfsight;
  window.__hsArmElfsight = armElfsight;

  if (!armElfsight() && 'MutationObserver' in window) {
    mutationObserver = new MutationObserver(() => {
      if (!armElfsight()) return;
      mutationObserver.disconnect();
    });
    mutationObserver.observe(document.documentElement, { childList: true, subtree: true });
  }

  ['pointerdown', 'touchstart', 'scroll'].forEach((eventName) => {
    window.addEventListener(eventName, loadElfsight, { once: true, passive: true });
  });
})();