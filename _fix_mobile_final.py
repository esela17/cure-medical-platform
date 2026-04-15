with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Also fix the mobile menu
idx = text.find('class="mobile-menu"')
end_idx = text.find('</div>', idx) + 6
mob_block = text[idx:end_idx]
print("CURRENT MOBILE MENU:")
print(mob_block)
print("---")

# Replace the entire mobile menu with the correct one
correct_mob = '''class="mobile-menu" id="mobileMenu"><a href="#about" onclick="toggleMenu()">من نحن</a><a href="#services" onclick="toggleMenu()">خدماتنا</a><a href="#how" onclick="toggleMenu()">كيف يعمل</a><a href="#why" onclick="toggleMenu()">لماذا كيور</a><a href="#join" onclick="toggleMenu()">انضم إلينا</a><a href="#contact" onclick="toggleMenu()">تواصل معنا</a><a href="articles.html" onclick="toggleMenu()">مقالات طبية</a><a href="careers.html" onclick="toggleMenu()" style="color:var(--green)">وظائف</a></div>'''

new_text = text[:idx] + correct_mob + text[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)
print("DONE - mobile menu fixed!")
