/* ═══════════════════════════════════════════════════════════════════
   CURE  ·  assets/js/main.js
   Shared logic — runs on every page
   ═══════════════════════════════════════════════════════════════════ */

'use strict';

/* ─────────────────────────────────────
   1. PAGE LOADER
   ───────────────────────────────────── */
window.addEventListener('load', () => {
  const loader = document.getElementById('page-loader');
  if (loader) setTimeout(() => loader.classList.add('is-hidden'), 1400);
});

/* ─────────────────────────────────────
   2. NAVBAR — scroll behaviour
   ───────────────────────────────────── */
(function initNavbar() {
  const nav = document.getElementById('navbar');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 50);
  }, { passive: true });
}());

/* ─────────────────────────────────────
   3. MOBILE MENU
   ───────────────────────────────────── */
function toggleMenu() {
  const menu = document.getElementById('mobile-nav');
  const btn = document.getElementById('hamburger-btn');
  if (!menu) return;
  const open = menu.classList.toggle('is-open');
  if (btn) {
    btn.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', open);
  }
}

/* ─────────────────────────────────────
   4. SCROLL REVEAL & COUNTERS
   ───────────────────────────────────── */
(function initReveal() {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { 
      if (e.isIntersecting) {
        e.target.classList.add('is-visible'); 
        
        // Counter Animation Logic
        if(e.target.classList.contains('number-item') && !e.target.dataset.counted) {
          e.target.dataset.counted = 'true';
          const valEl = e.target.querySelector('.num-val');
          if (valEl) {
            const originalText = valEl.innerText;
            const targetNum = parseInt(originalText.replace(/[^0-9]/g, ''));
            const suffix = originalText.replace(/[0-9]/g, '');
            if(!isNaN(targetNum)) {
              let current = 0;
              const increment = Math.ceil(targetNum / 40);
              const timer = setInterval(() => {
                current += increment;
                if(current >= targetNum) {
                  current = targetNum;
                  clearInterval(timer);
                }
                valEl.innerText = current + suffix;
              }, 40);
            }
          }
        }
      }
    });
  }, { threshold: 0.1 });
  
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
}());

/* ─────────────────────────────────────
   5. SMOOTH SCROLL (fixed navbar offset)
   ───────────────────────────────────── */
(function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (id === '#') return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
}());

/* ─────────────────────────────────────
   6. GOOGLE APPS SCRIPT HANDLER
   ───────────────────────────────────── */
/**
 * @param {Event}  e         submit event
 * @param {string} formId    <form> id
 * @param {string} successId success message element id
 */
async function handleFormSubmit(e, formId, successId) {
  e.preventDefault();
  const form = document.getElementById(formId);
  const success = document.getElementById(successId);
  const btn = form.querySelector('[type="submit"]');
  if (!form || !success || !btn) return;

  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري الإرسال...';

  try {
    const formData = new FormData(form);

    const res = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      body: formData
    });
    
    const data = await res.json();

    if (data.success) {
      form.style.display = 'none';
      success.style.display = 'block';
      if (typeof gtag !== 'undefined') gtag('event', 'form_submit', { form_id: formId });
    } else {
      throw new Error(data.message || 'تعذر الإرسال بسبب خادم Web3Forms');
    }

  } catch (err) {
    console.error('[Cure] Form error:', err);
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-paper-plane"></i> أرسل مرة أخرى';
    alert('حدث خطأ أثناء الإرسال — يرجى التواصل مباشرة على 01070203636');
  }
}

/* ─────────────────────────────────────
   7. SERVICE REQUEST — Formspree
   ───────────────────────────────────── */
/**
 * Opens Formspree hosted form for service request.
 * @param {string} name  Service display name
 * @param {string} price Price string  e.g. "150 جنيه"
 */
function requestService(name, price) {
  const url = `https://formspree.io/f/xreodypz?Subject=${encodeURIComponent('طلب خدمة: ' + name)}&Service=${encodeURIComponent(name)}`;
  window.open(url, '_blank', 'noopener,noreferrer');
}

/* ─────────────────────────────────────
   8. COUNTER ANIMATION
   ───────────────────────────────────── */
(function initCounters() {
  const map = { '150+': [150, '+'], '87%': [87, '%'], '91%': [91, '%'] };

  function animate(el, target, suffix) {
    const step = target / (2000 / 16);
    let current = 0;
    const tick = setInterval(() => {
      current += step;
      if (current >= target) { el.textContent = target + suffix; clearInterval(tick); }
      else el.textContent = Math.floor(current) + suffix;
    }, 16);
  }

  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const val = e.target.textContent.trim();
      if (map[val]) animate(e.target, ...map[val]);
      io.unobserve(e.target);
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.num-val').forEach(el => io.observe(el));
}());

/* ─────────────────────────────────────
   9. TAB SWITCHER (How It Works)
   ───────────────────────────────────── */
function switchTab(id, btn) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected', 'false'); });
  const panel = document.getElementById(id);
  if (panel) panel.classList.add('active');
  btn.classList.add('active');
  btn.setAttribute('aria-selected', 'true');
}
