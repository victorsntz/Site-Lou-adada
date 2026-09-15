/* Louçadada — o mínimo de JS pra casa funcionar bem.
   Sem biblioteca: menu do celular, entrada suave e o ano do rodapé. */
(function () {
  'use strict';

  /* --- menu do celular --------------------------------------------------- */
  var menu = document.getElementById('menu');
  var abrir = document.querySelector('.abrir-menu');
  var fechar = document.querySelector('.fechar-menu');

  function estado(aberto) {
    if (!menu || !abrir) return;
    menu.setAttribute('data-aberto', aberto ? 'true' : 'false');
    abrir.setAttribute('aria-expanded', aberto ? 'true' : 'false');
    document.body.style.overflow = aberto ? 'hidden' : '';
    if (aberto) {
      var primeiro = menu.querySelector('a');
      if (primeiro) primeiro.focus();
    } else {
      abrir.focus();
    }
  }

  if (abrir) abrir.addEventListener('click', function () {
    estado(menu.getAttribute('data-aberto') !== 'true');
  });
  if (fechar) fechar.addEventListener('click', function () { estado(false); });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu && menu.getAttribute('data-aberto') === 'true') estado(false);
  });

  if (menu) {
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && window.matchMedia('(max-width:860px)').matches) estado(false);
    });
  }

  /* fecha sozinho quando a tela cresce, pra não travar o scroll no desktop */
  var largo = window.matchMedia('(min-width:861px)');
  var aoMudar = function (m) { if (m.matches) estado(false); };
  if (largo.addEventListener) largo.addEventListener('change', aoMudar);
  else if (largo.addListener) largo.addListener(aoMudar);

  /* --- entrada suave ----------------------------------------------------- */
  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var alvos = document.querySelectorAll('.surge');

  if (quieto || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(alvos, function (el) { el.classList.add('visivel'); });
  } else {
    var olho = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add('visivel');
        olho.unobserve(entrada.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    Array.prototype.forEach.call(alvos, function (el, i) {
      el.style.transitionDelay = (Math.min(i % 4, 3) * 70) + 'ms';
      olho.observe(el);
    });
  }

  /* --- ano do rodapé ----------------------------------------------------- */
  var anos = document.querySelectorAll('[data-ano]');
  Array.prototype.forEach.call(anos, function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
