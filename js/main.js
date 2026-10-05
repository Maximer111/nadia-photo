// Nadia Photo — header state, mobile nav, scroll reveals. No dependencies.
(() => {
  'use strict';

  // sticky header
  const head = document.querySelector('.site-head');
  if (head) {
    const onScroll = () => head.classList.toggle('is-stuck', window.scrollY > 40);
    onScroll();
    addEventListener('scroll', onScroll, { passive: true });
  }

  // mobile nav
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');
  if (burger && nav) {
    burger.addEventListener('click', () => {
      const open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
      document.body.style.overflow = open ? '' : 'hidden';
    });
    nav.addEventListener('click', e => {
      if (e.target.closest('a')) {
        burger.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        document.body.style.overflow = '';
      }
    });
    addEventListener('keydown', e => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) burger.click();
    });
  }

  // portfolio viewer: links still open the full file without JS
  const lb = document.querySelector('.lb');
  const shots = [...document.querySelectorAll('.g__item')];
  if (lb && shots.length && lb.showModal) {
    const big = lb.querySelector('img');
    let at = 0;
    const show = i => {
      at = (i + shots.length) % shots.length;
      const thumb = shots[at].querySelector('img');
      const want = at;
      big.src = thumb.currentSrc || thumb.src;
      big.alt = thumb.alt;
      const hi = new Image();
      hi.onload = () => { if (at === want) big.src = hi.src; };
      hi.src = shots[at].href;
    };
    shots.forEach((a, i) => a.addEventListener('click', e => {
      e.preventDefault(); show(i); lb.showModal();
    }));
    lb.querySelector('.lb__prev').addEventListener('click', () => show(at - 1));
    lb.querySelector('.lb__next').addEventListener('click', () => show(at + 1));
    lb.querySelector('.lb__close').addEventListener('click', () => lb.close());
    lb.addEventListener('click', e => { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') show(at - 1);
      if (e.key === 'ArrowRight') show(at + 1);
    });
    let x0 = null;
    lb.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', e => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) show(at + (dx < 0 ? 1 : -1));
      x0 = null;
    });
    lb.addEventListener('close', () => { big.removeAttribute('src'); });
  }

  // scroll reveals — stagger siblings inside the same block
  const items = document.querySelectorAll('.rv');
  if (!items.length) return;

  if (!('IntersectionObserver' in window) ||
      matchMedia('(prefers-reduced-motion: reduce)').matches) {
    items.forEach(el => el.classList.add('is-in'));
    return;
  }

  const io = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const sibs = [...(el.parentElement?.children || [])].filter(n => n.classList.contains('rv'));
      el.style.setProperty('--d', `${Math.max(0, sibs.indexOf(el)) * 110}ms`);
      el.classList.add('is-in');
      obs.unobserve(el);
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.06 });

  items.forEach(el => io.observe(el));
})();
