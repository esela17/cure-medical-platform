import re
import os
import markdown
import json

# Refined Template for Premium Medical Articles
TEMPLATE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{TITLE}} | كيور CURE</title>
    <meta name="description" content="{{META_DESC}}" />
    <link rel="canonical" href="https://cureztyx.com/{{SLUG}}.html" />
    
    <!-- Open Graph / SEO -->
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{{TITLE}}" />
    <meta property="og:description" content="{{META_DESC}}" />
    <meta property="og:url" content="https://cureztyx.com/{{SLUG}}.html" />
    <meta property="og:image" content="https://cureztyx.com/assets/img/articles/{{IMG}}" />
    
    <link rel="icon" type="image/png" href="icon.png" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
    
    <style>
        :root {
            --bg: #0F0C29;
            --bg-gradient: linear-gradient(135deg, #0F0C29 0%, #302B63 50%, #24243E 100%);
            --card-bg: rgba(30, 26, 61, 0.6);
            --purple: #6B5CE7;
            --green: #7ED957;
            --white: #FFFFFF;
            --light: #C8C4E0;
            --muted: #94A3B8;
            --border: rgba(107, 92, 231, 0.2);
            --radius: 24px;
            --font-main: 'Cairo', sans-serif;
            --font-body: 'Tajawal', sans-serif;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        html { scroll-behavior: smooth; }
        body {
            background: var(--bg);
            background-image: var(--bg-gradient);
            background-attachment: fixed;
            color: var(--white);
            font-family: var(--font-body);
            line-height: 1.8;
            overflow-x: hidden;
        }

        .container { max-width: 900px; margin: 0 auto; padding: 0 24px; }
        
        /* Navigation */
        nav {
            position: sticky; top: 0; z-index: 1000;
            background: rgba(15, 12, 41, 0.8);
            backdrop-filter: blur(15px);
            border-bottom: 1px solid var(--border);
            padding: 15px 0;
        }
        .nav-inner { display: flex; justify-content: space-between; align-items: center; }
        .nav-logo img { height: 45px; }
        .nav-links { display: flex; gap: 20px; list-style: none; }
        .nav-links a { color: var(--light); text-decoration: none; font-weight: 600; font-family: var(--font-main); transition: 0.3s; }
        .nav-links a:hover { color: var(--green); }

        /* Article Hero */
        .article-hero { padding: 80px 0 60px; text-align: center; }
        .badge {
            display: inline-block; padding: 6px 16px; background: rgba(107, 92, 231, 0.15);
            border: 1px solid var(--purple); color: var(--green); border-radius: 100px;
            font-size: 13px; font-weight: 700; margin-bottom: 20px;
        }
        h1 { font-family: var(--font-main); font-size: clamp(28px, 5vw, 48px); font-weight: 900; margin-bottom: 25px; line-height: 1.3; }
        .meta-info { color: var(--muted); font-size: 14px; display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; }

        /* Featured Image */
        .featured-image-container { position: relative; margin-bottom: 50px; }
        .featured-image {
            width: 100%; height: 450px; object-fit: cover; border-radius: var(--radius);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4); border: 1px solid var(--border);
        }
        @media (max-width: 768px) { .featured-image { height: 280px; } }

        /* Article Content */
        .content { 
            background: var(--card-bg); backdrop-filter: blur(10px);
            padding: 40px; border-radius: var(--radius); border: 1px solid var(--border);
            margin-bottom: 60px;
        }
        .content p { margin-bottom: 25px; font-size: 18px; color: var(--light); }
        .content h2 { font-family: var(--font-main); font-size: 28px; font-weight: 800; margin: 45px 0 25px; color: var(--white); border-right: 5px solid var(--green); padding-right: 15px; }
        .content h3 { font-family: var(--font-main); font-size: 22px; font-weight: 700; margin: 35px 0 20px; color: var(--green); }
        
        /* Tables */
        .table-wrapper { overflow-x: auto; margin: 30px 0; border-radius: 12px; border: 1px solid var(--border); }
        table { width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.03); }
        th { background: rgba(107, 92, 231, 0.2); color: var(--white); padding: 15px; text-align: right; font-family: var(--font-main); }
        td { padding: 15px; border-top: 1px solid var(--border); color: var(--light); }
        tr:hover { background: rgba(255,255,255,0.05); }

        /* Quotes */
        blockquote {
            background: rgba(126, 217, 87, 0.05); border-right: 5px solid var(--green);
            padding: 25px; margin: 40px 0; border-radius: 12px; font-style: italic; color: var(--white);
        }

        /* FAQ */
        .faq-item { margin-bottom: 20px; border: 1px solid var(--border); border-radius: 12px; padding: 20px; transition: 0.3s; }
        .faq-item:hover { border-color: var(--green); background: rgba(126, 217, 87, 0.05); }
        .faq-q { font-weight: 800; color: var(--white); margin-bottom: 10px; display: flex; gap: 10px; }
        .faq-a { color: var(--light); }

        /* CTA Box */
        .cta-card {
            background: linear-gradient(135deg, #6B5CE7 0%, #4834D4 100%);
            padding: 40px; border-radius: var(--radius); text-align: center;
            box-shadow: 0 15px 35px rgba(107, 92, 231, 0.4); margin-bottom: 60px;
        }
        .cta-card h2 { border: none; padding: 0; margin-top: 0; margin-bottom: 15px; }
        .cta-card p { color: rgba(255,255,255,0.9); margin-bottom: 30px; }
        .cta-btns { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }
        .btn {
            padding: 14px 32px; border-radius: 50px; font-weight: 800; font-family: var(--font-main);
            text-decoration: none; transition: 0.3s; display: inline-flex; align-items: center; gap: 10px;
        }
        .btn-green { background: var(--green); color: #0F0C29; }
        .btn-green:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(126, 217, 87, 0.4); }
        .btn-outline { border: 2px solid var(--white); color: var(--white); }
        .btn-outline:hover { background: var(--white); color: #6B5CE7; }

        footer { padding: 60px 0; border-top: 1px solid var(--border); text-align: center; color: var(--muted); }
        .footer-links { margin-bottom: 20px; }
        .footer-links a { color: var(--light); margin: 0 15px; text-decoration: none; font-size: 14px; }
    </style>
    
    {{SCHEMA}}
</head>
<body>

<nav>
    <div class="container nav-inner">
        <a href="index.html" class="nav-logo"><img src="assets/png/logo-cure-new.png" alt="كيور CURE"></a>
        <ul class="nav-links">
            <li><a href="index.html">الرئيسية</a></li>
            <li><a href="articles.html">المقالات</a></li>
            <li><a href="careers.html">الوظائف</a></li>
        </ul>
    </div>
</nav>

<div class="container">
    <div class="article-hero">
        <span class="badge">نصائح طبية موثوقة</span>
        <h1>{{TITLE}}</h1>
        <div class="meta-info">
            <span><i class="far fa-calendar-alt"></i> أبريل 2025</span>
            <span><i class="far fa-clock"></i> 6 دقائق قراءة</span>
            <span><i class="far fa-user"></i> فريق كيور الطبي</span>
        </div>
    </div>

    <div class="featured-image-container">
        {{IMAGE}}
    </div>

    <article class="content">
        {{CONTENT}}
    </article>

    <div class="cta-card">
        <h2>هل تحتاج إلى رعاية طبية في المنزل؟</h2>
        <p>فريق كيور متاح على مدار 24 ساعة في الفيوم لتلبية جميع احتياجاتك الطبية والتمريضية بأسعار ثابتة.</p>
        <div class="cta-btns">
            <a href="https://wa.me/201070203636?text=مرحباً، أريد حجز خدمة تمريض منزلي" class="btn btn-green">
                <i class="fab fa-whatsapp"></i> احجز الآن عبر واتساب
            </a>
            <a href="index.html#services" class="btn btn-outline">استكشف خدماتنا</a>
        </div>
    </div>
</div>

<footer>
    <div class="container">
        <div class="footer-links">
            <a href="index.html">الرئيسية</a>
            <a href="articles.html">مقالات مفيدة</a>
            <a href="privacy.html">سياسة الخصوصية</a>
            <a href="terms.html">شروط الاستخدام</a>
        </div>
        <p>© 2025 جميع الحقوق محفوظة لمنصة كيور CURE — شريكك في الرعاية المنزلية</p>
    </div>
</footer>

<script>
    // Smooth appearance for sections
    document.addEventListener('DOMContentLoaded', () => {
        const observerOptions = { threshold: 0.1 };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('h2, h3, p, table').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'all 0.6s ease-out';
            observer.observe(el);
        });
    });
</script>

</body>
</html>
"""

def extract_meta(art_block):
    title = ""
    slug = ""
    meta_desc = ""
    
    # Flexible regex for title
    title_match = re.search(r'-\s*\*\*(?:عنوان SEO \(H1\)|H1):\*\*\s*(.*)', art_block)
    if title_match: title = title_match.group(1).strip()
    
    # Flexible regex for slug
    url_match = re.search(r'-\s*\*\*(?:URL مقترح|URL):\*\*\s*(?:`|/ar/blog/)*([^`\n\r]+)(?:`|/)*', art_block)
    if url_match: 
        slug = url_match.group(1).strip().split('/')[-1]
    
    # Meta description
    meta_match = re.search(r'-\s*\*\*(?:Meta Description[^:]*|Meta):\*\*\s*(.*)', art_block)
    if meta_match: meta_desc = meta_match.group(1).strip()
    
    return title, slug, meta_desc

def run():
    print("Starting article generation from CURE_SEO_Content_Pack.md...")
    
    if not os.path.exists('CURE_SEO_Content_Pack.md'):
        print("Error: CURE_SEO_Content_Pack.md not found.")
        return

    with open('CURE_SEO_Content_Pack.md', 'r', encoding='utf-8') as f:
        text = f.read()

    # Split by Article headers
    parts = re.split(r'## 📄 المقالة \d+', text)
    if len(parts) < 2:
        print("Could not find articles in MD.")
        return
    
    articles_content = parts[1:] # First part is header info
    
    # We will use markdown with some extensions for tables and code
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'nl2br', 'smarty'])
    
    catalog = []

    for idx, art_block in enumerate(articles_content):
        title, slug, meta_desc = extract_meta(art_block)
        
        if not title or not slug:
            print(f"Skipping article {idx+1} (metadata missing)")
            continue
            
        # Extract Full Content
        content_parts = re.split(r'### (?:المقال الكامل|المحتوى)', art_block)
        if len(content_parts) < 2:
            print(f"Skipping {title} (content section missing)")
            continue
            
        raw_content = content_parts[1]
        raw_content = re.split(r'### (?:Schema Markup|Schema|اقتراحات الصور|CTA)', raw_content)[0].strip()
        
        # Remove the duplicated H1 if it's there
        raw_content = re.sub(r'^#\s+.*?\n', '', raw_content, count=1).strip()
        
        # Convert to HTML
        html_content = md.convert(raw_content)
        
        # Extra styling for tables (wrap them in a div)
        html_content = html_content.replace('<table>', '<div class="table-wrapper"><table>').replace('</table>', '</table></div>')
        
        # Extract Schema
        schema_match = re.search(r'```json\s*(.*?)\s*```', art_block, re.DOTALL)
        schema_html = ""
        if schema_match:
            try:
                # Validate JSON just in case
                json_data = json.loads(schema_match.group(1))
                schema_html = f'<script type="application/ld+json">\n{json.dumps(json_data, ensure_ascii=False, indent=2)}\n</script>'
            except:
                schema_html = f'<script type="application/ld+json">\n{schema_match.group(1).strip()}\n</script>'

        # Image selection (round-robin through available articles)
        img_filename = f"article{(idx % 6) + 1}.png"
        img_tag = f'<img src="assets/img/articles/{img_filename}" alt="{title}" class="featured-image" />'

        # Final Page assembly
        page_html = TEMPLATE.replace('{{TITLE}}', title)\
                            .replace('{{META_DESC}}', meta_desc)\
                            .replace('{{SLUG}}', slug)\
                            .replace('{{SCHEMA}}', schema_html)\
                            .replace('{{IMAGE}}', img_tag)\
                            .replace('{{CONTENT}}', html_content)\
                            .replace('{{IMG}}', img_filename)

        # Write to file
        output_path = f"{slug}.html"
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write(page_html)
            
        print(f"[OK] Generated {output_path}")
        
        catalog.append({
            'title': title,
            'slug': slug,
            'desc': meta_desc,
            'image': img_filename
        })

    # Update Catalog JSON
    with open('articles_catalog.json', 'w', encoding='utf-8') as jf:
        json.dump(catalog, jf, ensure_ascii=False, indent=2)
    
    print(f"\nCompleted! Generated {len(catalog)} articles.")
    print("Catalog updated in articles_catalog.json.")

if __name__ == "__main__":
    run()
