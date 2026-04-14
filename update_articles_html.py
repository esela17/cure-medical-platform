import json
import re

def update_articles_page():
    with open('articles_catalog.json', 'r', encoding='utf-8') as f:
        catalog = json.load(f)
        
    tags = ['tag-green', 'tag-purple', 'tag-gold', 'tag-teal', 'tag-accent']
    categories = ['chronic', 'nursing', 'elderly', 'wounds', 'emergency', 'chronic']
    
    html_cards = []
    sitemap_entries = []
    
    for i, article in enumerate(catalog):
        img_num = (i % 6) + 1
        tag_class = tags[i % len(tags)]
        cat = categories[i % len(categories)]
        slug = article['slug']
        title = article['title']
        meta = article['meta']
        
        card = f"""
      <a href="{slug}.html" class="art-card reveal" data-cat="{cat}" style="display:block; text-decoration:none; color:inherit;">
        <div class="art-img">
          <img src="assets/img/articles/article{img_num}.png" alt="{title}" loading="lazy" />
        </div>
        <div class="art-content">
          <div class="art-meta2">
            <span><i class="fas fa-calendar-alt"></i> أبريل 2026</span>
          </div>
          <h3>{title}</h3>
          <p>{meta}</p>
          <div class="art-footer">
            <span class="art-read-more" style="width:100%; justify-content:flex-end;">اقرأ المقال <i class="fas fa-arrow-left"></i></span>
          </div>
        </div>
      </a>"""
        html_cards.append(card)
        
        # Add to sitemap entries
        sitemap_entries.append(f"""  <url>
    <loc>https://cureztyx.com/{slug}.html</loc>
    <lastmod>2026-04-14</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

    # --- UPDATE articles.html ---
    with open('articles.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace grid content
    grid_start = '<div class="articles-grid" id="articlesGrid">'
    grid_end = '</div>\n  </div>\n</div>\n\n<!-- CTA STRIP -->'
    
    parts = re.split(r'(<div class="articles-grid" id="articlesGrid">)(.*?)(</div>\s*</div>\s*</div>\s*<!-- CTA STRIP -->)', html, flags=re.DOTALL)
    
    if len(parts) >= 4:
        new_html = parts[0] + parts[1] + "\n".join(html_cards) + "\n    " + parts[3] + parts[4]
    else:
        print("Failed to replace grid in articles.html")
        return
        
    # Remove modal code
    new_html = re.sub(r'<!-- ARTICLE MODALS -->.*?</div>\s*</div>\s*</div>', '', new_html, flags=re.DOTALL)
    
    # Remove javascript array and modal functions
    new_html = re.sub(r'const articles = \[.*?\];', '', new_html, flags=re.DOTALL)
    new_html = re.sub(r'function openArticle\(.*\).*?}', '', new_html, flags=re.DOTALL)
    new_html = re.sub(r'function closeArticle\(\).*?}', '', new_html, flags=re.DOTALL)
    new_html = re.sub(r'function handleOverlayClick\(.*\).*?}', '', new_html, flags=re.DOTALL)
    
    with open('articles.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print("Updated articles.html successfully.")
        
    # --- UPDATE sitemap.xml ---
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        sitemap = f.read()
        
    if '</urlset>' in sitemap:
        new_sitemap = sitemap.replace('</urlset>', "\n" + "\n".join(sitemap_entries) + "\n</urlset>")
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
             f.write(new_sitemap)
        print("Updated sitemap.xml successfully.")

if __name__ == '__main__':
    update_articles_page()
