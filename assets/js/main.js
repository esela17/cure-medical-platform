/* ═══════════════════════════════════════════════════════════════════
   CURE  ·  assets/js/main.js
   Unified Logic — Professional Refactor (Phase 3)
   ═══════════════════════════════════════════════════════════════════ */

'use strict';

/* ─────────────────────────────────────
   1. UTILS (Cookies & Helpers)
   ───────────────────────────────────── */
function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  const expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  const name = cname + "=";
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') c = c.substring(1);
    if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
  }
  return "";
}

/* ─────────────────────────────────────
   2. PAGE LOADER
   ───────────────────────────────────── */
window.addEventListener('load', () => {
  const loader = document.getElementById('loader') || document.getElementById('page-loader');
  if (loader) {
    setTimeout(() => loader.classList.add('hidden', 'is-hidden'), 1000); // Support both class names used in different versions
  }
});

/* ─────────────────────────────────────
   3. NAVBAR & MOBILE MENU
   ───────────────────────────────────── */
(function initNavigation() {
  const nav = document.getElementById('navbar');
  const btn = document.getElementById('hamburgerBtn');
  const menu = document.getElementById('mobileMenu');

  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    }, { passive: true });
  }

  if (btn && menu) {
    const toggleMenu = () => {
      const isOpen = menu.classList.toggle('open') || menu.classList.toggle('is-open');
      btn.classList.toggle('is-open', isOpen);
      btn.setAttribute('aria-expanded', String(isOpen));
    };

    btn.addEventListener('click', toggleMenu);

    menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        menu.classList.remove('open', 'is-open');
        btn.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });
  }
}());

/* ─────────────────────────────────────
   4. LANGUAGE TOGGLE (Google Translate)
   ───────────────────────────────────── */
function toggleLanguage() {
  const currentLang = getCookie('googtrans');
  if (currentLang && currentLang.includes('/en')) {
    // Revert to Arabic
    document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=" + location.hostname + "; path=/;";
    location.reload();
  } else {
    // Translate to English
    setCookie("googtrans", "/ar/en", 30);
    location.reload();
  }
}

// Global init for language UI
window.addEventListener("DOMContentLoaded", () => {
  const lang = getCookie("googtrans");
  const toggleBtns = document.querySelectorAll(".lang-toggle-btn");
  if (lang && lang.includes("/en")) {
    toggleBtns.forEach(btn => btn.textContent = "AR");
    document.documentElement.dir = "ltr";
  } else {
    toggleBtns.forEach(btn => btn.textContent = "EN");
  }

  // Bind buttons
  ['langToggleDesktop', 'langToggleMobile'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', toggleLanguage);
  });
});

/* ─────────────────────────────────────
   5. SCROLL REVEAL & COUNTERS
   ───────────────────────────────────── */
(function initPremiumEffects() {
  const counterMap = { '150+': [150, '+'], '87%': [87, '%'], '91%': [91, '%'] };

  const animate = (el, target, suffix) => {
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    const tick = setInterval(() => {
      current += step;
      if (current >= target) { el.textContent = target + suffix; clearInterval(tick); }
      else el.textContent = Math.floor(current) + suffix;
    }, 16);
  };

  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      
      // Reveal animation
      e.target.classList.add('visible', 'is-visible');
      
      // Counter logic
      const valEl = e.target.classList.contains('num-val') ? e.target : e.target.querySelector('.num-val');
      if (valEl && !valEl.dataset.counted) {
        const text = valEl.textContent.trim();
        if (counterMap[text]) {
          valEl.dataset.counted = 'true';
          animate(valEl, ...counterMap[text]);
        }
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.reveal, .num-val').forEach(el => io.observe(el));
}());

/* ─────────────────────────────────────
   6. SMOOTH SCROLL (fixed navbar offset)
   ───────────────────────────────────── */
(function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const href = a.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const top = target.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });
}());

/* ─────────────────────────────────────
   7. FORM SUBMISSION (Unified GAS/Formspree/Web3)
   ───────────────────────────────────── */
async function handleFormSubmit(e, formId, successId) {
  e.preventDefault();
  const form = document.getElementById(formId);
  const success = document.getElementById(successId);
  const btn = form.querySelector('[type="submit"]') || form.querySelector('button');
  if (!form || !success || !btn) return;

  btn.disabled = true;
  const originalBtnText = btn.innerHTML;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري الإرسال...';

  try {
    const formData = new FormData(form);
    
    // Fallback backends if one fails or isn't set
    const endpoint = form.action || 'https://formspree.io/f/xreodypz';
    
    const res = await fetch(endpoint, {
      method: "POST",
      body: formData,
      headers: { 'Accept': 'application/json' }
    });

    if (res.ok) {
      form.style.display = 'none';
      success.style.display = 'block';
      success.scrollIntoView({ behavior: 'smooth', block: 'center' });
      if (typeof gtag !== 'undefined') gtag('event', 'form_complete', { form_id: formId });
    } else {
      throw new Error("Submission failed");
    }
  } catch (err) {
    console.error('[Cure] Form error:', err);
    btn.disabled = false;
    btn.innerHTML = originalBtnText;
    alert('حدث خطأ أثناء الإرسال — يرجى التواصل معنا مباشرة على 01070203636');
  }
}

/* ─────────────────────────────────────
   8. TAB SWITCHER
   ───────────────────────────────────── */
function switchTab(id, btn) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => { 
    b.classList.remove('active'); 
    b.setAttribute('aria-selected', 'false'); 
  });
  const panel = document.getElementById(id);
  if (panel) panel.classList.add('active');
  if (btn) {
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
  }
}
