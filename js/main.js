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
