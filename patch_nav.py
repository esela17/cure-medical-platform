import re

nav_css = """
/* Nav */
nav {
  position: sticky; top: 0; z-index: 1000;
  background: rgba(14, 12, 34, 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  transition: all 0.3s;
}
nav.solid { background: rgba(14, 12, 34, 0.98); box-shadow: 0 4px 30px rgba(0,0,0,.3); }
.nav-inner {
  max-width: 1300px; margin: 0 auto;
  padding: 16px 32px;
  display: flex; align-items: center; justify-content: space-between;
}
.nav-logo {
  display: flex; align-items: center; gap: 10px;
  font-family: var(--font-main); font-size: 22px; font-weight: 900;
}
.nav-logo img { height: 42px; width: auto; object-fit: contain; }
.nav-links { display: flex; align-items: center; gap: 8px; list-style: none; }
.nav-links a {
  font-family: var(--font-main); font-size: 14px; font-weight: 600;
  color: var(--light); padding: 8px 14px; border-radius: 8px;
  transition: all 0.2s;
}
.nav-links a:hover, .nav-links a.active { background: rgba(107,92,231,.12); color: var(--white); }
.nav-cta {
  background: var(--purple) !important;
  color: var(--white) !important;
  font-weight: 700 !important;
  box-shadow: 0 4px 15px rgba(107,92,231,.3);
}
.nav-cta:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(107,92,231,.4) !important; }
.hamburger { display: none; flex-direction: column; gap: 5px; cursor: pointer; padding: 5px; }
.hamburger span { display: block; width: 26px; height: 2px; background: var(--light); border-radius: 9px; transition: all 0.3s; }
.mobile-menu {
  display: none; flex-direction: column; gap: 4px;
  background: rgba(14,12,34,.97); padding: 20px 32px;
  border-bottom: 1px solid var(--border);
}
.mobile-menu.open { display: flex; }
.mobile-menu a { font-family: var(--font-main); font-size: 16px; font-weight: 600; color: var(--light); padding: 12px 0; border-bottom: 1px solid var(--border2); transition: color 0.2s; }
.mobile-menu a:hover { color: var(--green); }
.lang-toggle-btn {
  background: rgba(255,255,255,0.05); border: 1px solid var(--border);
  color: var(--light); padding: 5px 10px; border-radius: 6px;
  font-weight: 700; cursor: pointer; transition: all 0.3s;
  font-family: var(--font-main); font-size: 14px; z-index: 1001;
}
.lang-toggle-btn:hover { background: rgba(107,92,231,0.15); border-color: var(--purple); color: var(--white); }
.mobile-only { display: none; }
@media (max-width: 991px) { .mobile-only { display: block; } }
@media (max-width: 768px) { .nav-links { display: none; } .hamburger { display: flex; } }
"""

nav_html = """
<nav id="navbar">
  <div class="nav-inner">
    <a href="index.html" class="nav-logo">
      <img src="assets/png/logo-cure-new.png" alt="كيور" />
    </a>
    <ul class="nav-links">
      <li><a href="index.html">الرئيسية</a></li>
      <li><a href="index.html#services">خدماتنا</a></li>
      <li><a href="index.html#about">من نحن</a></li>
      <li><a href="articles.html" class="active">مقالات طبية</a></li>
      <li><a href="careers.html">وظائف</a></li>
      <li><a href="index.html#contact">تواصل معنا</a></li>
      <li><a href="https://wa.me/201070203636?text=مرحباً، أريد حجز خدمة تمريض منزلي" class="nav-cta"><i class="fas fa-hand-holding-medical"></i> احجز الآن</a></li>
      <li><button class="lang-toggle-btn" onclick="toggleLanguage()">EN</button></li>
    </ul>
    <div style="display:flex;align-items:center;gap:12px;">
      <button class="lang-toggle-btn mobile-only" onclick="toggleLanguage()">EN</button>
      <div class="hamburger" onclick="toggleMenu()"><span></span><span></span><span></span></div>
    </div>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <a href="index.html" onclick="toggleMenu()">الرئيسية</a>
    <a href="index.html#services" onclick="toggleMenu()">خدماتنا</a>
    <a href="index.html#about" onclick="toggleMenu()">من نحن</a>
    <a href="articles.html" onclick="toggleMenu()">مقالات طبية</a>
    <a href="careers.html" onclick="toggleMenu()">وظائف</a>
    <a href="index.html#contact" onclick="toggleMenu()">تواصل معنا</a>
    <a href="https://wa.me/201070203636?text=مرحباً، أريد حجز خدمة" style="color:var(--green)">احجز الآن</a>
  </div>
</nav>

<div id="google_translate_element" style="display:none;"></div>
<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
<script>
window.addEventListener('scroll', () => { document.getElementById('navbar').classList.toggle('solid', window.scrollY > 60); });
function toggleMenu() { document.getElementById('mobileMenu').classList.toggle('open'); }
function setCookie(n, v, d) { const x = new Date(); x.setTime(x.getTime() + d*24*60*60*1000); document.cookie = n+'='+v+'; expires='+x.toUTCString()+'; path=/'; }
function getCookie(n) { const d = decodeURIComponent(document.cookie).split(';'); for (let c of d) { while (c.charAt(0)===' ') c=c.substring(1); if (c.indexOf(n+'=')===0) return c.substring((n+'=').length); } return ''; }
function toggleLanguage() { const l = getCookie('googtrans'); if (l && l.includes('/en')) { document.cookie='googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'; document.cookie='googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain='+location.hostname+'; path=/;'; location.reload(); } else { setCookie('googtrans','/ar/en',30); location.reload(); } }
window.addEventListener('DOMContentLoaded', () => { const l = getCookie('googtrans'); document.querySelectorAll('.lang-toggle-btn').forEach(b => b.textContent = (l && l.includes('/en')) ? 'AR' : 'EN'); if (l && l.includes('/en')) document.documentElement.dir = 'ltr'; });
function googleTranslateElementInit() { new google.translate.TranslateElement({pageLanguage:'ar',includedLanguages:'ar,en',autoDisplay:false},'google_translate_element'); }
</script>
"""

with open('build_articles.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace CSS
css_start = text.find('/* Nav */')
css_end = text.find('/* Layout */')
text = text[:css_start] + nav_css + text[css_end:]

# Replace HTML
html_start = text.find('<nav>')
html_end = text.find('<div class="page-hero">')
text = text[:html_start] + nav_html + "\n" + text[html_end:]

with open('build_articles.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("build_articles.py updated with full nav.")
