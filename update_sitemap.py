import os
from datetime import datetime

DIR = "."
BASE_URL = "https://cureztyx.com/"
SITEMAP_PATH = "sitemap.xml"

# Base pages with priorities
PRIORITIES = {
    "index.html": "1.0",
    "pricing.html": "0.95",
    "faq.html": "0.9",
    "articles.html": "0.9",
    "tamreed-manzili-fayoum.html": "0.85",
    "tamreed-manzili-ebshaway.html": "0.85",
    "tamreed-manzili-senouris.html": "0.85",
    "careers.html": "0.8"
}

def generate_sitemap():
    html_files = [f for f in os.listdir(DIR) if f.endswith(".html") and os.path.isfile(os.path.join(DIR, f))]
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Process index first
    if "index.html" in html_files:
        xml.append('  <url>')
        xml.append(f'    <loc>{BASE_URL}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append('    <changefreq>weekly</changefreq>')
        xml.append('    <priority>1.0</priority>')
        xml.append('  </url>')
    
    for f in sorted(html_files):
        if f == "index.html":
            continue
            
        priority = PRIORITIES.get(f, "0.6") # default priority for articles is 0.6
        changefreq = "monthly" if priority == "0.6" else "weekly"
        
        xml.append('  <url>')
        xml.append(f'    <loc>{BASE_URL}{f}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append(f'    <changefreq>{changefreq}</changefreq>')
        xml.append(f'    <priority>{priority}</priority>')
        xml.append('  </url>')
        
    xml.append('</urlset>')
    
    with open(SITEMAP_PATH, "w", encoding="utf-8") as file:
        file.write("\n".join(xml))
        
    print(f"Sitemap updated successfully with {len(html_files)} pages.")

if __name__ == "__main__":
    generate_sitemap()
