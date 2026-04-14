import re

try:
    with open('careers.html', 'r', encoding='utf-8') as f:
        ctext = f.read()
    
    # In careers.html, the current page might be marked as active or just regular
    pattern = r'(<li><a href="careers\.html"[^>]*>.*?وظائف.*?</a></li>)'
    replacement = r'<li><a href="articles.html" style="color:var(--light)">مقالات طبية</a></li>\1'
    ctext, cnum = re.subn(pattern, replacement, ctext)
    
    # Mobile menu
    p2 = r'(<a href="careers\.html"[^>]*>.*?وظائف.*?</a>)'
    r2 = r'<a href="articles.html" style="color:var(--light)">مقالات طبية</a>\1'
    ctext, cnum2 = re.subn(p2, r2, ctext)
    
    with open('careers.html', 'w', encoding='utf-8') as f:
        f.write(ctext)
    print(f"careers.html replaced {cnum} nav links and {cnum2} mobile links.")
except Exception as e:
    print(e)
