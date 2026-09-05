import os
import re

def main():
    css_path = 'assets/css/style.css'
    with open(css_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 1. tokens.css
    tokens_css = lines[0:85]
    with open('assets/css/tokens.css', 'w', encoding='utf-8') as f:
        f.writelines(tokens_css)
    print("Updated assets/css/tokens.css")

    # 2. base.css
    base_css = lines[85:240]
    with open('assets/css/base.css', 'w', encoding='utf-8') as f:
        f.writelines(base_css)
    print("Updated assets/css/base.css")

    # 3. components.css
    components_css = []
    components_css.extend(lines[240:543])    # Buttons, badges, header, top-bar, navbar, ribbon, section header
    components_css.extend(lines[1054:1317])  # App showcase, FAQ accordion, testimonials, footer, mobile bar
    with open('assets/css/components.css', 'w', encoding='utf-8') as f:
        f.writelines(components_css)
    print("Updated assets/css/components.css")

    # 4. pages/index.css
    index_css = []
    index_css.extend(lines[543:1054])  # Hero, step flow, services grid, numbers, comparison table
    index_css.extend(lines[1317:])     # Smart matcher, live radar, bedside pledge, visual storytelling
    with open('assets/css/pages/index.css', 'w', encoding='utf-8') as f:
        f.writelines(index_css)
    print("Updated assets/css/pages/index.css")

    # 5. Extract styles from careers.html for pages/careers.css
    with open('careers.html', 'r', encoding='utf-8') as f:
        careers_content = f.read()

    style_match = re.search(r'<style>(.*?)</style>', careers_content, re.DOTALL)
    if style_match:
        careers_css = style_match.group(1).strip()
        with open('assets/css/pages/careers.css', 'w', encoding='utf-8') as f:
            f.write("/* Scoped Styles for Careers Page */\n" + careers_css + "\n")
        print("Updated assets/css/pages/careers.css from careers.html")

        # Remove <style>...</style> from careers.html
        new_careers_content = re.sub(r'\s*<style>.*?</style>\s*', '\n\n', careers_content, flags=re.DOTALL)
        with open('careers.html', 'w', encoding='utf-8') as f:
            f.write(new_careers_content)
        print("Removed inline <style> from careers.html")

    # 6. Extract styles from articles.html and single article template for pages/articles.css
    with open('articles.html', 'r', encoding='utf-8') as f:
        articles_content = f.read()

    style_match_art = re.search(r'<style>(.*?)</style>', articles_content, re.DOTALL)
    art_list_css = ""
    if style_match_art:
        art_list_css = style_match_art.group(1).strip()
        # Remove <style>...</style> from articles.html
        new_articles_content = re.sub(r'\s*<style>.*?</style>\s*', '\n\n', articles_content, flags=re.DOTALL)
        with open('articles.html', 'w', encoding='utf-8') as f:
            f.write(new_articles_content)
        print("Removed inline <style> from articles.html")

    # Also grab single article styles from an article file (e.g. gheyar-aljorouh-fil-manzil.html)
    single_art_css = ""
    sample_art_path = 'gheyar-aljorouh-fil-manzil.html'
    if os.path.exists(sample_art_path):
        with open(sample_art_path, 'r', encoding='utf-8') as f:
            sample_content = f.read()
        single_style_match = re.search(r'<style>(.*?)</style>', sample_content, re.DOTALL)
        if single_style_match:
            single_art_css = single_style_match.group(1).strip()

    combined_articles_css = f"""/* ═══════════════════════════════════════════════════════════════════
   CURE ARTICLES & HEALTH ENCYCLOPEDIA STYLESHEET
   ═══════════════════════════════════════════════════════════════════ */

/* ─── 01. ARTICLES HUB & ARCHIVE ────────────────────────────── */
{art_list_css}

/* ─── 02. SINGLE ARTICLE READING & CLINICAL CONTENT ─────────── */
{single_art_css}
"""
    with open('assets/css/pages/articles.css', 'w', encoding='utf-8') as f:
        f.write(combined_articles_css)
    print("Updated assets/css/pages/articles.css with archive and reader styling")

    # 7. Update style.css to be a master stylesheet using @import
    master_style = """/* ═══════════════════════════════════════════════════════════════════
   CURE MEDICAL DESIGN SYSTEM · Master Bundle & Fallback Entry Point
   ═══════════════════════════════════════════════════════════════════ */

@import url('tokens.css');
@import url('base.css');
@import url('components.css');
@import url('pages/index.css');
"""
    with open('assets/css/style.css', 'w', encoding='utf-8') as f:
        f.write(master_style)
    print("Converted assets/css/style.css to master bundle with @import")

if __name__ == '__main__':
    main()
