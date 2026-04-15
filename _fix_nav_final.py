import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix: replace the entire nav-links ul with the correct version (clean)
old_nav = 'class="nav-links"><li><a href="#about">'
# Find and print the surrounding context to get it RIGHT
idx = text.find('class="nav-links">')
end_idx = text.find('</ul>', idx) + 5
nav_block = text[idx:end_idx]
print("CURRENT NAV BLOCK:")
print(nav_block)
print("---")

# Now replace the entire nav-links block with the correct one
correct_nav = '''class="nav-links"><li><a href="#about">من نحن</a></li><li><a href="#services">خدماتنا</a></li><li><a href="#how">كيف يعمل</a></li><li><a href="#why">لماذا كيور</a></li><li><a href="#join">انضم إلينا</a></li><li><a href="#contact">تواصل معنا</a></li><li><a href="articles.html">مقالات طبية</a></li><li><a href="careers.html" style="color: var(--green)">وظائف</a></li><li><a href="#join" class="nav-cta">سجّل الآن</a></li><li><button class="lang-toggle-btn" onclick="toggleLanguage()">EN</button></li></ul>'''

new_text = text[:idx] + correct_nav + text[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)
print("DONE - nav-links fixed!")
