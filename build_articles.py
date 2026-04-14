import re
import os
import markdown

# Create articles directory if it doesn't exist (though we decided to put them in root) 
# Wait, the plan said "individual HTML pages (e.g. articles/diabetes-symptoms.html)" and I thought root. 
# Let's put them in root to match privacy.html / terms.html and preserve asset paths perfectly.

TEMPLATE = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{TITLE}} | كيور</title>
<meta name="description" content="{{META_DESC}}" />
<link rel="canonical" href="https://cureztyx.com/{{SLUG}}.html" />
<link rel="icon" type="image/png" href="icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
<style> :root {
  --bg: #12102A;
  --bg2: #1A1535;
  --card: #1E1A3D;
  --purple: #6B5CE7;
  --green: #7ED957;
  --white: #FFFFFF;
  --light: #C8C4E0;
  --muted: #6B7280;
  --border: rgba(107, 92, 231, 0.25);
  --radius: 16px;
  --radius-sm: 10px;
  --font-main: 'Cairo', sans-serif;
  --font-body: 'Tajawal', sans-serif;
  --accent: #FF6B6B;
}

*,
*::before,
*::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  background: var(--bg);
  color: var(--white);
  font-family: var(--font-body);
  line-height: 1.8;
  overflow-x: hidden;
}

a { text-decoration: none; color: var(--green); }
a:hover { text-decoration: underline; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: var(--purple); border-radius: 3px; }

/* Nav */
nav {
  position: sticky; top: 0; z-index: 100;
  background: rgba(18, 16, 42, 0.95); backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border); padding: 16px 24px;
  display: flex; align-items: center; justify-content: space-between;
}

.nav-logo { display: flex; align-items: center; gap: 10px; font-family: var(--font-main); font-size: 20px; font-weight: 900; color: var(--white); }
.nav-back { font-family: var(--font-main); font-size: 13px; font-weight: 700; color: var(--light); display: flex; align-items: center; gap: 6px; transition: color 0.2s; }
.nav-back:hover { color: var(--green); text-decoration: none; }

/* Layout */
.container { max-width: 820px; margin: 0 auto; padding: 0 24px; }
.page-hero { background: linear-gradient(135deg, var(--bg2), var(--bg)); border-bottom: 1px solid var(--border); padding: 64px 24px 48px; text-align: center; }
.page-hero h1 { font-family: var(--font-main); font-size: clamp(26px, 4vw, 40px); font-weight: 900; margin-bottom: 16px; line-height: 1.4; }
.page-hero .badge-date { display: inline-flex; align-items: center; gap: 6px; background: rgba(107, 92, 231, 0.15); border: 1px solid var(--border); color: var(--green); padding: 6px 16px; border-radius: 999px; font-size: 12px; font-weight: 700; font-family: var(--font-main); margin-bottom: 20px; }

/* Content */
.policy-content { padding: 60px 0 80px; }
.policy-content p { font-size: 16px; color: var(--light); line-height: 1.9; margin-bottom: 20px; }
.policy-content h2 { font-family: var(--font-main); font-size: 24px; font-weight: 900; color: var(--white); margin: 40px 0 20px; display: flex; align-items: center; gap: 10px; }
.policy-content h2::before { content: ''; display: block; width: 4px; height: 24px; background: linear-gradient(to bottom, var(--purple), var(--green)); border-radius: 4px; flex-shrink: 0; }
.policy-content h3 { font-family: var(--font-main); font-size: 20px; font-weight: 800; color: var(--white); margin: 30px 0 16px; }
.policy-content ul { padding-right: 20px; margin-bottom: 24px; }
.policy-content ul li { font-size: 16px; color: var(--light); line-height: 2; margin-bottom: 10px; }
.policy-content ul li::marker { color: var(--green); }
.policy-content blockquote { border-right: 4px solid var(--purple); background: rgba(107, 92, 231, 0.08); padding: 18px 20px; margin: 24px 0; border-radius: var(--radius-sm); font-size: 15px; color: var(--light); }
.policy-content blockquote p { margin-bottom: 0; }
.policy-content table { width: 100%; border-collapse: collapse; margin: 30px 0; font-size: 15px; }
.policy-content table th { background: rgba(107, 92, 231, 0.15); padding: 14px; text-align: right; border: 1px solid var(--border); color: var(--white); font-family: var(--font-main); }
.policy-content table td { padding: 14px; border: 1px solid var(--border); color: var(--light); }

.article-featured-img { width: 100%; height: 400px; object-fit: cover; border-radius: var(--radius); margin-bottom: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid var(--border); }
@media (max-width: 768px) { .article-featured-img { height: 250px; margin-bottom: 24px; } }

.cure-cta-box { background: linear-gradient(135deg, rgba(107,92,231,.2), rgba(126,217,87,.1)); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; margin-top: 50px; text-align: center; }
.cure-cta-box h3 { font-family: var(--font-main); font-size: 22px; font-weight: 900; margin-bottom: 10px; }
.cure-cta-box p { font-size: 15px; color: var(--light); margin-bottom: 20px; }
.cure-cta-box a { display: inline-flex; align-items: center; gap: 8px; background: var(--purple); color: #fff; padding: 14px 32px; border-radius: var(--radius-sm); font-family: var(--font-main); font-size: 15px; font-weight: 800; transition: all 0.3s; box-shadow: 0 6px 20px rgba(107,92,231,.4); text-decoration: none; }
.cure-cta-box a:hover { background: #8B7CF0; transform: translateY(-2px); text-decoration: none;}

/* Footer */
footer { background: var(--bg2); border-top: 1px solid var(--border); padding: 24px; text-align: center; }
footer p { font-size: 12px; color: var(--muted); }
footer a { color: var(--muted); margin: 0 8px; font-size: 12px; }
footer a:hover { color: var(--green); text-decoration: none;}
</style>
{{SCHEMA}}
</head>
<body>
<nav>
  <a href="index.html" class="nav-logo"><img src="assets/png/logo-cure-new.png" alt="كيور" style="height: 45px; width: auto; object-fit: contain;"></a>
  <div style="display:flex;align-items:center;gap:16px;">
    <a href="articles.html" style="font-family:var(--font-main);font-size:13px;font-weight:700;color:var(--light);display:flex;align-items:center;gap:6px;transition:color 0.2s;"><i class="fas fa-newspaper"></i> مقالات طبية</a>
    <a href="index.html" class="nav-back"><i class="fas fa-arrow-right"></i> العودة للرئيسية</a>
  </div>
</nav>

<div class="page-hero">
  <div class="container">
    <span class="badge-date"><i class="fas fa-calendar"></i> أبريل 2026</span>
    <h1>{{TITLE}}</h1>
    <p>بقلم أطباء وممرضي منصة كيور الطبية</p>
  </div>
</div>

<div class="policy-content">
  <div class="container">
    {{IMAGE}}
    {{CONTENT}}
    
    <div class="cure-cta-box">
      <h3>🏠 هل تحتاج ممرض منزلي الآن؟</h3>
      <p>احصل على رعاية طبية موثوقة في منزلك بالفيوم في أقل من 15 دقيقة</p>
      <a href="https://wa.me/201070203636?text=مرحباً، أريد حجز خدمة تمريض منزلي"><i class="fas fa-hand-holding-medical"></i> احجز عبر واتساب</a>
    </div>
  </div>
</div>

<footer>
  <p>© 2026 كيور — Cure Technology &nbsp;|&nbsp;
  <a href="index.html">الرئيسية</a><a href="privacy.html">سياسة الخصوصية</a><a href="terms.html">شروط الاستخدام</a><a href="careers.html">وظائف</a><a href="articles.html">مقالات طبية</a></p>
</footer>
</body>
</html>"""

def run():
    with open('CURE_SEO_Content_Pack.md', 'r', encoding='utf-8') as f:
        text = f.read()

    articles = re.split(r'## 📄 المقالة \d+', text)
    if len(articles) > 1:
        articles = articles[1:] # Drop preamble
    else:
        print("Could not find articles based on split token.")
        return

    sitemap_entries = []
    generated_data = []

    for idx, art in enumerate(articles):
        # Extract fields
        title_match = re.search(r'-\s*\*\*(?:عنوان SEO \(H1\)|H1):\*\*\s*(.*)', art)
        url_match = re.search(r'-\s*\*\*(?:URL مقترح|URL):\*\*\s*`(?:/ar/blog/)?([^`]+)`', art)
        if not url_match:
             url_match = re.search(r'-\s*\*\*(?:URL مقترح|URL):\*\*\s*(?:/ar/blog/)?(.*)', art)
        meta_match = re.search(r'-\s*\*\*(?:Meta Description[^0-9]*\d*[a-zA-Z]*|Meta):\*\*\s*(.*)', art)
        
        if not title_match or not url_match:
            print(f"Skipping article {idx+1} due to missing metadata.")
            continue
            
        title = title_match.group(1).strip()
        slug = url_match.group(1).strip().replace('`', '').split('/')[-1] # Ensure just the filename part
        meta = meta_match.group(1).strip() if meta_match else title

        # Extract content
        # Content usually starts after '### المقال الكامل' and ends at '### Schema Markup' or '### اقتراحات الصور'
        content_match = re.search(r'### المقال الكامل\s+(.*?)(?=### Schema Markup|### اقتراحات الصور|---)', art, re.DOTALL)
        content_md = content_match.group(1).strip() if content_match else ""

        # Remove the duplicated H1 from markdown if it exists (since we put it in the hero section)
        content_md = re.sub(r'^#\s+.*?\n', '', content_md, count=1).strip()

        # Convert markdown to html
        # using extensions for tables
        content_html = markdown.markdown(content_md, extensions=['tables', 'fenced_code'])
        
        # We can map standard blockquotes to our info-box if they contain specific bold words
        # but the css handles blockquotes well anyway.

        # Extract Schema
        schema_match = re.search(r'```json\s*(.*?)\s*```', art, re.DOTALL)
        schema = ""
        if schema_match:
            schema_json = schema_match.group(1)
            schema = f'<script type="application/ld+json">\n{schema_json}\n</script>'

        # Generate HTML page
        img_num = (idx % 6) + 1
        img_html = f'<img src="assets/img/articles/article{img_num}.png" alt="{title}" class="article-featured-img" />'

        html = TEMPLATE.replace('{{TITLE}}', title)\
                       .replace('{{META_DESC}}', meta)\
                       .replace('{{SLUG}}', slug)\
                       .replace('{{SCHEMA}}', schema)\
                       .replace('{{IMAGE}}', img_html)\
                       .replace('{{CONTENT}}', content_html)
                       
        filepath = os.path.join(os.path.dirname(__file__), f'{slug}.html')
        with open(filepath, 'w', encoding='utf-8') as out:
            out.write(html)
            
        print(f"Generated {slug}.html")
        sitemap_entries.append(slug)
        
        # Save for articles.html grid logic
        generated_data.append({
            'title': title,
            'slug': slug,
            'meta': meta,
        })
        
    print(f"\nSuccessfully generated {len(generated_data)} article pages.")

    # Dump the JSON data for us to update articles.html manually or via script
    with open('articles_catalog.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(generated_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run()
