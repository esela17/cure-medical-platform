import os

html_files = ['index.html', 'careers.html', 'terms.html', 'privacy.html']

for html_file in html_files:
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace 2.png with logo-cure-new.png
        # Also let's check for %D9%84%D9%88%D8%AC%D9%88 just in case
        content = content.replace('assets/png/2.png', 'assets/png/logo-cure-new.png')
        content = content.replace('assets/png/%D9%84%D9%88%D8%AC%D9%88.png', 'assets/png/logo-cure-new.png')

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {html_file}")
