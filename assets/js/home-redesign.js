document.addEventListener('DOMContentLoaded',()=>{const menu=document.querySelector('.menu'),toggle=document.querySelector('.nav-toggle');toggle?.addEventListener('click',()=>{const open=menu.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open))});document.querySelectorAll('.nav-parent').forEach(btn=>btn.addEventListener('click',e=>{e.preventDefault();const group=btn.closest('.nav-group');document.querySelectorAll('.nav-group.open').forEach(g=>g!==group&&g.classList.remove('open'));group.classList.toggle('open');btn.setAttribute('aria-expanded',String(group.classList.contains('open')))}));document.addEventListener('keydown',e=>{if(e.key==='Escape'){menu?.classList.remove('open');document.querySelectorAll('.nav-group').forEach(g=>g.classList.remove('open'))}})});


document.addEventListener('DOMContentLoaded',()=>{
  const faq=document.querySelector('.home-faq');
  if(!faq)return;
  const items=faq.querySelectorAll('details');
  items.forEach(item=>{
    item.addEventListener('toggle',()=>{
      if(!item.open)return;
      items.forEach(other=>{if(other!==item)other.removeAttribute('open')});
    });
  });
});

document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('.hero .glass > p').forEach(p=>{
    if(p.textContent.trim()==='Professional paver sealing, driveway restoration, pool deck sealing, and travertine care across Nocatee, Ponte Vedra, Jacksonville, and St. Johns County.') p.remove();
  });
});

document.addEventListener('DOMContentLoaded',()=>{
  const travertineCard=document.querySelector('a.service-image-card[href="/paver-sealing/travertine-sealing"]');
  if(!travertineCard)return;
  travertineCard.querySelector('img')?.remove();
  travertineCard.querySelector('.service-image-shade')?.remove();
  travertineCard.style.background='#0b2d4a';
});
