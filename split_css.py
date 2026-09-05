import os
import glob

def main():
    css_path = 'assets/css/style.css'
    if not os.path.exists(css_path):
        print(f"Error: {css_path} not found.")
        return

    with open(css_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    tokens_css = lines[0:85]
    base_css = lines[85:240]
    
    components_css = []
    components_css.extend(lines[240:543])
    components_css.extend(lines[1054:1317])
    components_css.extend(lines[1631:])

    index_css = lines[543:1054]
    careers_css = lines[1317:1494]
    articles_css = lines[1494:1631]

    # Create directories
    os.makedirs('assets/css/pages', exist_ok=True)

    # Write files
    with open('assets/css/tokens.css', 'w', encoding='utf-8') as f:
        f.writelines(tokens_css)
    with open('assets/css/base.css', 'w', encoding='utf-8') as f:
        f.writelines(base_css)
    with open('assets/css/components.css', 'w', encoding='utf-8') as f:
        f.writelines(components_css)
    with open('assets/css/pages/index.css', 'w', encoding='utf-8') as f:
        f.writelines(index_css)
    with open('assets/css/pages/careers.css', 'w', encoding='utf-8') as f:
        f.writelines(careers_css)
    with open('assets/css/pages/articles.css', 'w', encoding='utf-8') as f:
        f.writelines(articles_css)

    print("CSS files split successfully.")

    # Now update HTML files
    html_files = glob.glob('*.html')
    
    core_css = """<link rel="stylesheet" href="assets/css/tokens.css" />
  <link rel="stylesheet" href="assets/css/base.css" />
  <link rel="stylesheet" href="assets/css/components.css" />"""

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'assets/css/tokens.css' in content:
            continue # already updated

        page_css = ""
        if file == 'careers.html':
            page_css = '<link rel="stylesheet" href="assets/css/pages/careers.css" />'
        elif file == 'articles.html':
            page_css = '<link rel="stylesheet" href="assets/css/pages/articles.css" />'
        elif file in ['index.html', 'pricing.html', 'faq.html', 'privacy.html', 'terms.html']:
            page_css = '<link rel="stylesheet" href="assets/css/pages/index.css" />'
        else:
            # Assuming individual articles might need articles.css or just components
            page_css = '<link rel="stylesheet" href="assets/css/pages/articles.css" />'
            # Wait, some specific location pages (tamreed-manzili-*.html) are like index!
            if 'tamreed-manzili' in file or 'reayat-kibar' in file:
                page_css = '<link rel="stylesheet" href="assets/css/pages/index.css" />'

        replacement = core_css + "\n  " + page_css

        # Replace style.css
        # It could be <link rel="stylesheet" href="assets/css/style.css" />
        # Or <link rel="stylesheet" href="assets/css/style.css">
        import re
        content = re.sub(r'<link rel="stylesheet" href="assets/css/style\.css"\s*/?>', replacement, content)

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Updated CSS links in {file}")

    print("All HTML files updated.")

if __name__ == '__main__':
    main()
