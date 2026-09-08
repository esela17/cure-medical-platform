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
   2. PAGE LOADER (Instant Presentation)
   ───────────────────────────────────── */
function dismissLoader() {
  const loader = document.getElementById('loader') || document.getElementById('page-loader');
  if (loader) {
    loader.classList.add('hidden', 'is-hidden');
    loader.style.opacity = '0';
    loader.style.visibility = 'hidden';
    loader.style.pointerEvents = 'none';
    setTimeout(() => { loader.style.display = 'none'; }, 300);
  }
}
window.addEventListener('load', () => setTimeout(dismissLoader, 150));
document.addEventListener('DOMContentLoaded', () => setTimeout(dismissLoader, 600));

/* ─────────────────────────────────────
   3. NAVBAR & MOBILE MENU
   ───────────────────────────────────── */
(function initNavigation() {
  const header = document.getElementById('site-header');
  const nav = document.getElementById('navbar');
  const btn = document.getElementById('hamburgerBtn');
  const menu = document.getElementById('mobileMenu');

  window.addEventListener('scroll', () => {
    const isScrolled = window.scrollY > 30;
    if (header) header.classList.toggle('scrolled', isScrolled);
    if (nav) nav.classList.toggle('scrolled', isScrolled);
  }, { passive: true });

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

/* ─────────────────────────────────────
   9. CONVERSION EVENTS TRACKING (GA4 / Custom)
   ───────────────────────────────────── */
function trackEvent(eventName, params = {}) {
  try {
    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, params);
    }
    // Also dispatch a custom event for any analytics listeners
    window.dispatchEvent(new CustomEvent('cure_track_event', { detail: { eventName, params } }));
    console.debug(`[Cure Analytics] Tracked: ${eventName}`, params);
  } catch (e) {
    // Fail silently so user experience is never blocked
  }
}

// Global click event delegation for automated conversion tracking
document.addEventListener('click', (e) => {
  const link = e.target.closest('a');
  if (!link || !link.href) return;

  const href = link.href;

  // 1. Google Play app download clicks
  if (href.includes('play.google.com/store/apps/details?id=com.cureztyx.app')) {
    trackEvent('app_download_click', {
      platform: 'android',
      link_text: link.innerText?.trim() || 'icon',
      location: window.location.pathname
    });
  }
  // 2. WhatsApp bookings
  else if (href.includes('wa.me') || href.includes('whatsapp.com')) {
    trackEvent('whatsapp_contact', {
      source: link.closest('section')?.id || link.closest('nav') ? 'navbar' : 'footer_or_float',
      location: window.location.pathname
    });
  }
  // 3. Direct Phone Calls
  else if (href.startsWith('tel:')) {
    trackEvent('phone_call_click', {
      phone: href.replace('tel:', ''),
      location: window.location.pathname
    });
  }
}, { passive: true });

/* ─────────────────────────────────────
   10. FAQ ACCORDION HANDLER
   ───────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  const faqButtons = document.querySelectorAll('.faq-question');
  faqButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      if (!item) return;
      const isOpen = item.classList.contains('active');
      // Close all items in the same faq-grid
      const grid = item.closest('.faq-grid');
      if (grid) {
        grid.querySelectorAll('.faq-item').forEach(other => other.classList.remove('active'));
      }
      if (!isOpen) {
        item.classList.add('active');
      }
    });
  });

  /* ─────────────────────────────────────
     11. SMART CARE & DISPATCH MATCHER WIDGET
     ───────────────────────────────────── */
  const serviceSelect = document.getElementById('matcherService');
  const areaSelect = document.getElementById('matcherArea');
  const nurseNameEl = document.getElementById('matcherNurseName');
  const specialtyEl = document.getElementById('matcherSpecialty');
  const etaEl = document.getElementById('matcherEta');
  const priceEl = document.getElementById('matcherPrice');
  const dispatchBtn = document.getElementById('matcherDispatchBtn');

  function updateSmartMatcher() {
    if (!serviceSelect || !areaSelect) return;

    const selectedServiceOpt = serviceSelect.options[serviceSelect.selectedIndex];
    const selectedAreaOpt = areaSelect.options[areaSelect.selectedIndex];

    const serviceName = selectedServiceOpt.getAttribute('data-name') || selectedServiceOpt.text;
    const priceText = selectedServiceOpt.getAttribute('data-price') || 'حسب التقييم';

    const areaName = selectedAreaOpt.text.split('(')[0].trim();
    const timeText = selectedAreaOpt.getAttribute('data-time') || '15 دقيقة';
    const nurseName = selectedAreaOpt.getAttribute('data-nurse') || 'ممرض معتمد';
    const specialty = selectedAreaOpt.getAttribute('data-specialty') || 'أخصائي تمريض منزلي';

    if (priceEl) priceEl.innerHTML = `<span style="font-size: 15px; color: var(--c-secondary); font-weight: 800;"><i class="fas fa-certificate"></i> مسعّرة ومحددة بالتطبيق</span>`;
    if (etaEl) etaEl.textContent = timeText;
    if (nurseNameEl) {
      nurseNameEl.innerHTML = `${nurseName} <span style="font-size: 11px; background: rgba(174, 250, 124, 0.18); color: var(--c-secondary); border: 1px solid var(--c-secondary); padding: 2px 8px; border-radius: 12px; font-weight: 800;"><i class="fas fa-certificate"></i> ترخيص ساري</span>`;
    }
    if (specialtyEl) specialtyEl.textContent = `${specialty} · نطاق ${areaName}`;

    if (dispatchBtn) {
      const waText = encodeURIComponent(`مرحباً كيور، قمت بمطابقة الخدمة الذكية وأريد تأكيد طلب:\n- الخدمة: ${serviceName}\n- المركز: ${areaName}\n- الممرض المقترح: ${nurseName}\n- التسعيرة: رسمية ومحددة بالتطبيق`);
      dispatchBtn.href = `https://wa.me/201070203636?text=${waText}`;
      dispatchBtn.setAttribute('title', `طلب فوري لـ ${serviceName} في ${areaName}`);
    }

    // Micro animation on result box
    const resultBox = document.querySelector('.matcher-result-box');
    if (resultBox) {
      resultBox.style.transition = 'transform 0.2s ease, box-shadow 0.2s ease';
      resultBox.style.transform = 'scale(1.01)';
      resultBox.style.boxShadow = '0 0 25px rgba(174, 250, 124, 0.35)';
      setTimeout(() => {
        resultBox.style.transform = 'scale(1)';
        resultBox.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.3)';
      }, 200);
    }
  }

  if (serviceSelect && areaSelect) {
    serviceSelect.addEventListener('change', updateSmartMatcher);
    areaSelect.addEventListener('change', updateSmartMatcher);
    updateSmartMatcher(); // Initialize on page load
  }
});
