import os
import glob
import re

GA4_SNIPPET = """
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-CUREZTYX26"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-CUREZTYX26');
  </script>
"""

def optimize_html():
    html_files = glob.glob('*.html')
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # 1. Add GA4 Snippet if not present
        if 'googletagmanager.com/gtag' not in content:
            content = content.replace('</head>', GA4_SNIPPET + '</head>')
            changed = True

        # 2. Add loading="lazy" to images (except those with loading="eager")
        # Find all img tags
        img_tags = re.findall(r'<img[^>]*>', content)
        for img in img_tags:
            if 'loading=' not in img and 'class="hero' not in img:
                new_img = img.replace('<img ', '<img loading="lazy" ')
                content = content.replace(img, new_img)
                changed = True

        if changed:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Optimized {file}")

def update_main_js():
    js_path = 'assets/js/main.js'
    if not os.path.exists(js_path):
        return
        
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'app_download_click' in content:
        print("GA4 Events already in main.js")
        return

    ga_events_code = """
/* ─────────────────────────────────────
   Analytics Conversion Events (GA4)
   ───────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
    // 1. App Downloads
    const gpBtns = document.querySelectorAll('a[href*="play.google.com"]');
    gpBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if(typeof gtag !== 'undefined') {
                gtag('event', 'app_download_click', { platform: 'android' });
            }
        });
    });

    // 2. WhatsApp Clicks
    const waBtns = document.querySelectorAll('a[href*="wa.me"]');
    waBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if(typeof gtag !== 'undefined') {
                gtag('event', 'whatsapp_contact', { source: 'website' });
            }
        });
    });
});
"""
    # Append to the end of main.js
    with open(js_path, 'a', encoding='utf-8') as f:
        f.write("\n" + ga_events_code)
    
    # Also update handleFormSubmit for the 'nurse_form_complete' event
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace the success part of handleFormSubmit
    submit_str = "if (successMsg) {"
    if submit_str in content and "gtag('event', 'nurse_form_complete')" not in content:
        new_submit_str = """
    if (typeof gtag !== 'undefined') {
      gtag('event', formId === 'nurseForm' ? 'nurse_form_complete' : 'form_complete');
    }
    if (successMsg) {"""
        content = content.replace(submit_str, new_submit_str)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Updated main.js with GA4 events")

if __name__ == '__main__':
    optimize_html()
    update_main_js()
