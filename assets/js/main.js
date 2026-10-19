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
  const idMenuBtn = document.getElementById('idMenuBtn');
  const idMegaMenu = document.getElementById('idMegaMenu');
  const idDrawerClose = document.getElementById('idDrawerClose');

  window.addEventListener('scroll', () => {
    const isScrolled = window.scrollY > 30;
    if (header) header.classList.toggle('scrolled', isScrolled);
    if (nav) nav.classList.toggle('scrolled', isScrolled);
  }, { passive: true });

  // InDrive Full-Screen Mega Menu Global Support
  if (idMenuBtn && idMegaMenu) {
    const openMegaMenu = () => {
      idMegaMenu.classList.add('active', 'open');
      idMegaMenu.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    };
    const closeMegaMenu = () => {
      idMegaMenu.classList.remove('active', 'open');
      idMegaMenu.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    };

    idMenuBtn.addEventListener('click', openMegaMenu);
    if (idDrawerClose) idDrawerClose.addEventListener('click', closeMegaMenu);

    idMegaMenu.addEventListener('click', (e) => {
      if (e.target === idMegaMenu) closeMegaMenu();
    });

    idMegaMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', closeMegaMenu);
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && idMegaMenu.classList.contains('active')) closeMegaMenu();
    });

    // Category Tabs Switcher
    const megaTabs = idMegaMenu.querySelectorAll('.id-mega-tab-btn');
    const megaPanels = idMegaMenu.querySelectorAll('.id-mega-panel');
    megaTabs.forEach(tab => {
      tab.addEventListener('click', (e) => {
        e.preventDefault();
        megaTabs.forEach(t => t.classList.remove('active'));
        megaPanels.forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        const cat = tab.getAttribute('data-cat');
        const panel = document.getElementById('mega-panel-' + cat);
        if (panel) panel.classList.add('active');
      });
    });
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
   4. PROFESSIONAL BILINGUAL TRANSLATION (Arabic RTL <-> English LTR)
   ───────────────────────────────────── */
window.currentLang = 'ar';

window.setLanguage = function(lang) {
  window.currentLang = lang;
  document.documentElement.lang = lang;
  document.documentElement.dir = (lang === 'en' ? 'ltr' : 'rtl');
  document.body.classList.toggle('lang-en', lang === 'en');
  
  // Update toggle buttons text (preserves globe icon)
  document.querySelectorAll('.lang-toggle-btn, #langToggleBtn').forEach(btn => {
    const lbl = btn.querySelector('.lang-toggle-label') || btn.querySelector('span');
    if (lbl) {
      lbl.textContent = (lang === 'en' ? 'العربية' : 'EN');
    } else {
      btn.textContent = (lang === 'en' ? 'العربية' : 'EN');
    }
    btn.setAttribute('aria-label', lang === 'en' ? 'التبديل إلى العربية' : 'Switch to English');
  });

  // Apply translations dictionary
  if (window.CURE_I18N && window.CURE_I18N[lang]) {
    const dict = window.CURE_I18N[lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key] !== undefined) {
        el.innerHTML = dict[key];
      }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      if (dict[key] !== undefined) {
        el.placeholder = dict[key];
      }
    });
  }

  // Update Hero dynamic title if rotator exists
  if (window.updateHeroLanguageTitle) {
    window.updateHeroLanguageTitle();
  }

  // Update matcher selects if function exists
  if (window.updateSmartMatcher) {
    window.updateSmartMatcher();
  }

  // Persist preference
  try {
    localStorage.setItem('cure_lang', lang);
  } catch (e) {}

  window.dispatchEvent(new CustomEvent('cure_language_switched', { detail: { lang } }));
};

window.toggleLanguage = function() {
  const current = window.currentLang || localStorage.getItem('cure_lang') || 'ar';
  const target = (current === 'ar' ? 'en' : 'ar');
  window.setLanguage(target);
};

// Global language init on DOM load
window.addEventListener('DOMContentLoaded', () => {
  let savedLang = 'ar';
  try {
    savedLang = localStorage.getItem('cure_lang') || 'ar';
  } catch (e) {}

  ['langToggleBtn', 'langToggleDesktop', 'langToggleMobile', 'idMegaLangToggle'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', (e) => {
      e.preventDefault();
      window.toggleLanguage();
    });
  });

  if (savedLang === 'en') {
    window.setLanguage('en');
  } else {
    document.querySelectorAll('.lang-toggle-label').forEach(lbl => lbl.textContent = 'EN');
  }
});

/* ─────────────────────────────────────
   5. SCROLL REVEAL & COUNTERS
   ───────────────────────────────────── */
(function initPremiumEffects() {
  const counterMap = { '6': [6, ''], '87%': [87, '%'], '91%': [91, '%'] };

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

  document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .num-val').forEach(el => io.observe(el));
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
    const timeText = selectedAreaOpt.getAttribute('data-time') || 'استجابة فورية فائقة';
    const nurseName = selectedAreaOpt.getAttribute('data-nurse') || 'ممرض معتمد';
    const specialty = selectedAreaOpt.getAttribute('data-specialty') || 'أخصائي تمريض منزلي';

    if (priceEl) priceEl.innerHTML = `<span style="font-size: 15px; color: #5256eb; font-weight: 800;"><i class="fas fa-certificate"></i> مسعّرة ومحددة بالتطبيق</span>`;
    if (etaEl) etaEl.textContent = timeText;
    if (nurseNameEl) {
      nurseNameEl.innerHTML = `${nurseName} <span style="font-size: 11px; background: rgba(109, 115, 255, 0.12); color: #5256eb; border: 1px solid rgba(109, 115, 255, 0.3); padding: 2px 8px; border-radius: 12px; font-weight: 800;"><i class="fas fa-certificate"></i> ترخيص ساري</span>`;
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
      resultBox.style.boxShadow = '0 0 25px rgba(109, 115, 255, 0.25)';
      setTimeout(() => {
        resultBox.style.transform = 'scale(1)';
        resultBox.style.boxShadow = '0 10px 28px rgba(109, 115, 255, 0.08)';
      }, 200);
    }
  }

  if (serviceSelect && areaSelect) {
    serviceSelect.addEventListener('change', updateSmartMatcher);
    areaSelect.addEventListener('change', updateSmartMatcher);
    updateSmartMatcher(); // Initialize on page load
  }
});


/* ─────────────────────────────────────
   12. HERO 4-VALUES SYNCHRONIZED ROTATOR
   ───────────────────────────────────── */
(function initHeroRotator() {
  const slides = document.querySelectorAll('.id-hero-slide');
  const tabs = document.querySelectorAll('.id-tab-item');
  const titleEl = document.getElementById('heroDynamicTitle');
  if (!slides.length || !tabs.length) return;

  const heroSlidesContent = {
    ar: [
      { title: '<mark class="cure-marker">تمريض منزلي</mark><br/>بالسعر العادل<br/>ورعاية تطمنك' },
      { title: '<mark class="cure-marker">أمان واطمئنان</mark><br/>ممرض مرخص ومعتمد<br/>حتى باب بيتك' },
      { title: '<mark class="cure-marker">سرعة في الاستجابة</mark><br/>نصلك في منزلك<br/>بأسرع وقت قياسي' },
      { title: '<mark class="cure-marker">أسعار معلنة</mark><br/>تفاصيل واضحة ومحددة<br/>دون أي مساومات' }
    ],
    en: [
      { title: '<mark class="cure-marker">Home Nursing</mark><br/>At Fair Rates<br/>Care You Trust' },
      { title: '<mark class="cure-marker">Safety & Peace</mark><br/>Licensed & Verified Nurse<br/>To Your Doorstep' },
      { title: '<mark class="cure-marker">Lightning Fast</mark><br/>Reaching Your Home<br/>In Record Time' },
      { title: '<mark class="cure-marker">Clear Pricing</mark><br/>Transparent Rates<br/>Zero Haggling' }
    ]
  };

  let activeIdx = 0;
  let progressAnimFrame = null;
  let progressStartTime = null;
  const SLIDE_DURATION = 6000;

  function updateProgress(timestamp) {
    if (!progressStartTime) progressStartTime = timestamp;
    const elapsed = timestamp - progressStartTime;
    const progressPercent = Math.min((elapsed / SLIDE_DURATION) * 100, 100);

    tabs.forEach((tab, i) => {
      const fill = tab.querySelector('.id-tab-progress-fill');
      if (fill) {
        if (i === activeIdx) {
          fill.style.width = progressPercent + '%';
        } else if (i < activeIdx) {
          fill.style.width = '100%';
        } else {
          fill.style.width = '0%';
        }
      }
    });

    if (elapsed < SLIDE_DURATION) {
      progressAnimFrame = requestAnimationFrame(updateProgress);
    } else {
      goToSlide((activeIdx + 1) % slides.length);
    }
  }

  function goToSlide(index) {
    if (progressAnimFrame) cancelAnimationFrame(progressAnimFrame);
    progressStartTime = null;
    activeIdx = index;
    window.currentHeroSlideIndex = index;

    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === index);
    });

    tabs.forEach((tab, i) => {
      tab.classList.toggle('active', i === index);
      const fill = tab.querySelector('.id-tab-progress-fill');
      if (fill) fill.style.width = (i < index ? '100%' : '0%');
    });

    if (titleEl) {
      titleEl.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
      titleEl.style.opacity = '0';
      titleEl.style.transform = 'translateY(6px)';
      setTimeout(() => {
        const lang = window.currentLang === 'en' ? 'en' : 'ar';
        const slideData = heroSlidesContent[lang] && heroSlidesContent[lang][index];
        if (slideData) titleEl.innerHTML = slideData.title;
        titleEl.style.opacity = '1';
        titleEl.style.transform = 'translateY(0)';
      }, 250);
    }

    progressAnimFrame = requestAnimationFrame(updateProgress);
  }

  window.goToHeroSlide = goToSlide;

  window.updateHeroLanguageTitle = function() {
    const lang = window.currentLang === 'en' ? 'en' : 'ar';
    const slideData = heroSlidesContent[lang] && heroSlidesContent[lang][activeIdx];
    if (titleEl && slideData) {
      titleEl.innerHTML = slideData.title;
    }
  };

  tabs.forEach((tab, i) => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      goToSlide(i);
    });
  });

  // Start progress
  progressAnimFrame = requestAnimationFrame(updateProgress);
}());

/* ─────────────────────────────────────
   13. OFFICIAL YOUTUBE VIDEO STORY MODAL
   ───────────────────────────────────── */
window.openVideoModal = function() {
  const modal = document.getElementById('videoModal');
  const iframe = document.getElementById('videoIframe');
  if (modal && iframe) {
    iframe.src = "https://www.youtube-nocookie.com/embed/kPL6iRweoBs?autoplay=1";
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
};

window.closeVideoModal = function(e) {
  if (e && e.target && e.target.closest('.video-modal-content') && !e.target.classList.contains('video-modal-close')) {
    return;
  }
  const modal = document.getElementById('videoModal');
  const iframe = document.getElementById('videoIframe');
  if (modal && iframe) {
    iframe.src = "";
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }
};

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const modal = document.getElementById('videoModal');
    if (modal && modal.classList.contains('open')) window.closeVideoModal();
  }
});

/* ─────────────────────────────────────
   14. INTERACTIVE RADAR MAP HUB SELECTOR
   ───────────────────────────────────── */
window.highlightHub = function(cardId) {
  const card = document.getElementById(cardId);
  if (!card) return;

  document.querySelectorAll('.radar-hub-card').forEach(c => c.classList.remove('highlighted'));
  card.classList.add('highlighted');

  card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  setTimeout(() => {
    card.classList.remove('highlighted');
  }, 3500);
};
