import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the navbar block using regex
pattern = r'<nav id="navbar">.*?</nav>'
match = re.search(pattern, content, re.DOTALL)

if match:
    print('FOUND navbar block, length:', len(match.group(0)))
    old_nav = match.group(0)

    new_nav = '''<nav id="navbar">
  <div class="nav-inner">
    <a href="#hero" class="nav-logo">
      <img src="assets/png/logo-cure-new.png" alt="شعار كيور للتمريض المنزلي" width="140" height="44">
    </a>
    <ul class="nav-links" id="navLinks">
      <li><a href="#about">من نحن</a></li>
      <li><a href="#services">خدماتنا</a></li>
      <li><a href="#how">كيف يعمل</a></li>
      <li><a href="#why">لماذا كيور</a></li>
      <li><a href="articles.html">المقالات</a></li>
      <li><a href="careers.html" style="color: var(--green)">وظائف</a></li>
      <li><a href="#join" class="nav-cta">سجّل الآن</a></li>
      <li><button class="lang-toggle-btn" id="langToggleDesktop" aria-label="تغيير اللغة">EN</button></li>
    </ul>
    <div style="display: flex; align-items: center; gap: 12px;">
      <button class="lang-toggle-btn mobile-only" id="langToggleMobile" aria-label="تغيير اللغة">EN</button>
      <button class="hamburger" id="hamburgerBtn" aria-expanded="false" aria-label="افتح القائمة">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <a href="#about">من نحن</a>
    <a href="#services">خدماتنا</a>
    <a href="#how">كيف يعمل</a>
    <a href="#why">لماذا كيور</a>
    <a href="#join">انضم إلينا</a>
    <a href="#contact">تواصل معنا</a>
    <a href="articles.html">مقالات طبية</a>
    <a href="careers.html" style="color:var(--green)">وظائف</a>
  </div>
</nav>'''

    new_content = content[:match.start()] + new_nav + content[match.end():]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('SUCCESS - navbar HTML replaced cleanly')
else:
    print('ERROR: navbar block not found in file')
