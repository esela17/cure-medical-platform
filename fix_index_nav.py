import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see what is inside `<ul class="nav-links">...</ul>`
import urllib.parse
html_utf = text
# If 'مقالات طبية' is missing in 'index.html', we add it before 'وظائف'.
pattern = r'(<li><a href="careers\.html"[^>]*>وظائف</a></li>)'
replacement = r'<li><a href="articles.html">مقالات طبية</a></li>\1'

new_text, num = re.subn(pattern, replacement, text)

# Add it also in mobile-menu before careers
p2 = r'(<a href="careers\.html"[^>]*>وظائف</a>)'
r2 = r'<a href="articles.html">مقالات طبية</a>\1'
new_text, num2 = re.subn(p2, r2, new_text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print(f"Index.html replaced {num} nav links and {num2} mobile links.")

# Doing the same for careers.html just in case
try:
    with open('careers.html', 'r', encoding='utf-8') as f:
        ctext = f.read()
    ctext, cnum = re.subn(pattern, replacement, ctext)
    ctext, cnum2 = re.subn(p2, r2, ctext)
    with open('careers.html', 'w', encoding='utf-8') as f:
        f.write(ctext)
    print(f"careers.html replaced {cnum} nav links and {cnum2} mobile links.")
except Exception as e:
    pass

