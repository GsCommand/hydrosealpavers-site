document.addEventListener('DOMContentLoaded',function(){
  var header=document.querySelector('.hs-modern-header');if(!header)return;
  var toggle=header.querySelector('.hs-modern-toggle'),menu=header.querySelector('.hs-modern-menu'),groups=header.querySelectorAll('.hs-modern-group');
  toggle.addEventListener('click',function(){var open=menu.classList.toggle('hs-open');toggle.setAttribute('aria-expanded',String(open));if(!open)groups.forEach(function(group){group.classList.remove('hs-open');var button=group.querySelector('.hs-modern-parent');if(button)button.setAttribute('aria-expanded','false')})});
  groups.forEach(function(group){var button=group.querySelector('.hs-modern-parent');button.addEventListener('click',function(event){if(window.innerWidth>980)return;event.preventDefault();var willOpen=!group.classList.contains('hs-open');groups.forEach(function(other){other.classList.remove('hs-open');var otherButton=other.querySelector('.hs-modern-parent');if(otherButton)otherButton.setAttribute('aria-expanded','false')});group.classList.toggle('hs-open',willOpen);button.setAttribute('aria-expanded',String(willOpen))})});
});
