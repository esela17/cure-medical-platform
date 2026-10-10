import os
import glob
import re

# Tailored 30-second summary points for each article topic
SUMMARIES = {
    'tarkib-kanyoula-fil-manzil': [
        ('متى تحتاجها؟', 'لإعطاء المحاليل الوريدية، محاليل الحديد، المضادات الحيوية، أو سوائل الطوارئ لمرضى الجفاف والقيء الشديد.'),
        ('معايير الأمان:', 'كانيولا معقمة تفتح أمام المريض، تثبيت محكم لمنع التسريب، وتطهير كحولي 70% للوريد.'),
        ('كيف تطلبها؟', 'ممرض مرخص يصلك خلال 15-20 دقيقة في الفيوم لتركيبها والتأكد من سريان المحلول بسلاسة.')
    ],
    'reayat-kibar-alsen-fil-manzil': [
        ('الاحتياج الأساسي:', 'مساعدة يومية في الحركة، النظافة الشخصية، مواعيد الأدوية، والوقاية من مخاطر السقوط.'),
        ('الرعاية التمريضية:', 'متابعة دورية للضغط والسكر، تقليب منتظم لمنع قرح الفراش، وجلسات تنفس عند اللزوم.'),
        ('الخدمة في الفيوم:', 'شيفتات تمريضية مرنة (6 - 12 - 24 ساعة) بممرضين وممرضات متمرسين في رعاية المسنين.')
    ],
    'gheyar-aljorouh-fil-manzil': [
        ('أنواع الجروح:', 'جروح العمليات الجراحية، قرح الفراش، جروح الحوادث، وجروح القدم السكري المعقدة.'),
        ('بروتوكول التعقيم:', 'استخدام شاش ومطهرات معقمة ذات استخدام فردي، وتقييم علامات الالتئام ومكافحة العدوى.'),
        ('التوفر المنزلي:', 'زيارة تمريضية معقمة تغنيك عن مشقة نقل المريض للمستشفى وتجنبه عدوى المنشآت الطبية.')
    ],
    'aljaltta-aldimaghiyya-arad-weliqaya': [
        ('علامات الطوارئ (FAST):', 'اعوجاج بالوجه، ثقل بحركة أحد الذراعين، وصعوبة بالكلام — تستوجب المستشفى فوراً خلال أول 3 ساعات.'),
        ('الرعاية المنزلية اللاحقة:', 'تركيب قسطرة بولية، أنبوبة تغذية رايل، إعطاء مميعات الدم، وتمارين الحركة لمنع التيبس.'),
        ('دور التمريض:', 'مرافقة سريرية متخصصة لمتابعة المؤشرات الحيوية وحماية المريض من قرح الفراش والجفاف.')
    ],
    'arad-marad-alsukkar-annoa-althani': [
        ('العلامات التحذيرية:', 'عطش متكرر، تبول مفرط ليلاً، بطء التئام الجروح، وتعب غير مبرر مع تشوش الرؤية.'),
        ('المتابعة المنزلية:', 'فحص السكر التراكمي دورياً، قياس يومي للسكر العشوائي، وفحص القدمين يومياً لأي خدوش.'),
        ('دعم كيور:', 'زيارات تمريضية دورية لقياس السكر وضبط خطة الرعاية وجرعات الإنسولين بدقة.')
    ],
    'ertifaa-daght-alddam-arad-welaj': [
        ('القاتل الصامت:', 'قد لا تظهر أعراض واضحة إلا عند الارتفاع الشديد: صداع خلف الرأس، طنين بالأذن، وزغللة.'),
        ('الوقاية والتحكم:', 'تقليل الملح، قياس الضغط صباحاً ومساءً بجهاز معاير، والانتظام الصارم على العلاج دون انقطاع.'),
        ('خدمة القياس المنزلي:', 'فحص دقيق للعلامات الحيوية وتسجيل القراءات في سجل المريض الطبي مع كل زيارة.')
    ],
    'arad-alkolesterol-almurtafaa': [
        ('المؤشرات الصامتة:', 'الكوليسترول المرتفع لا يعطي أعراضاً مبكرة، لكنه يهدد الشرايين التاجية والدماغية.'),
        ('التشخيص الدقيق:', 'تحليل دهون الدم الكاملة (Lipid Profile) بعد صيام 10-12 ساعة لتقييم الـ LDL والـ HDL.'),
        ('الحل السريري:', 'نظام غذائي متوازن، نشاط حركي يومي، ومتابعة العلاج الدوائي باشراف طبي دوري.')
    ],
    'arad-qosour-alghudda-aldaraqiyya': [
        ('الأعراض الشائعة:', 'خمول مستمر، زيادة وزن دون إفراط بالطعام، برودة بالأطراف، وجفاف بالبشرة وتساقط الشعر.'),
        ('التشخيص:', 'تحليل هرمون TSH و Free T4 لتحديد الجرعة البديلة الدقيقة (ليفوثيروكسين).'),
        ('نصيحة ذهبية:', 'تناول الدواء على معدة فارغة تماماً صباحاً قبل الإفطار بساعة لضمان أفضل امتصاص.')
    ],
    'ilaj-alanemia-asbab-welaj': [
        ('الأنواع والأسباب:', 'أنيميا نقص الحديد هي الأكثر شيوعاً، وتليها أنيميا فيتامين B12 وأنيميا الأمراض المزمنة.'),
        ('خيارات العلاج:', 'المكملات الفموية للحالات الخفيفة، ومحاليل الحديد الوريدية للحالات الحادة أو الحوامل.'),
        ('الرعاية المنزلية:', 'جلسات إعطاء محاليل الحديد بالمنزل ومتابعة الهيموجلوبين ومخزون الفيريتين دورياً.')
    ],
    'alghaseel-alkalawi-mata-wahow': [
        ('متى يبدأ؟', 'عند وصول القصور الكلوي للمرحلة النهائية (انخفاض معدل الفلترة GFR إلى أقل من 15).'),
        ('الرعاية بين الجلسات:', 'حماية وصلة الغسيل (Fistula)، ضبط السوائل والأملاح، ومراقبة الضغط يومياً.'),
        ('الدعم المنزلي:', 'متابعة سريرية متخصصة في المنزل بين جلسات الغسيل لضبط الأدوية وقياس العلامات الحيوية.')
    ],
    'alaiktiaab-walqalaq-masr': [
        ('الأعراض الحقيقية:', 'فقدان الشغف، اضطراب النوم والشهية، نوبات هلع وضيق تنفس، وعزلة عن الأسرة والعمل.'),
        ('كسر الوصمة:', 'المرض النفسي خلل كيميائي قابل للعلاج تماماً وليس ضعف إيمان أو عيباً شخصياً.'),
        ('بداية التعافي:', 'استشارة متخصصة مع دعم الأسرة والبيئة المحيطة، وتوفر دعم تمريضي منزلي للحالات الحرجة.')
    ],
    'inqas-alwazn-bil-sahha-toroq-mjraaba': [
        ('المبدأ العلمي:', 'عجز سعرات معتدل مستدام مع رفع حصة البروتين والألياف لتجنب فقدان العضلات.'),
        ('الواقعية للمصريين:', 'تعديل الأطباق اليومية وتقليل المقليات والمياه الغازية بدلاً من الحميات القاسية الفاشلة.'),
        ('المتابعة المستمرة:', 'فحص دهون الدم ووظائف الكبد ومقاومة الإنسولين لضمان نزول صحي ومستمر.')
    ],
    'hishasha-alizaam-weliqaya': [
        ('الخطر الخفي:', 'ضعف تدريجي في كثافة العظام يمر دون ألم حتى يحدث كسر مفاجئ في مفصل الفخذ أو الفقرات.'),
        ('الفئات المعرضة:', 'النساء بعد انقطاع الطمث، كبار السن، ومن يعانون من نقص مزمن في فيتامين د والكالسيوم.'),
        ('الوقاية الفعالة:', 'فحص Dexa دوري، ممارسة تمارين المقاومة، وتأمين بيئة المنزل لمنع انزلاق المسنين.')
    ],
    'alrabo-3nd-alatfal-reaya-manziliyya': [
        ('علامات النوبة:', 'سعال جاف مستمر ليلاً، تزييق بالصدر، وسرعة في التنفس مع حركة عضلات القفص الصدري.'),
        ('التعامل السليم:', 'استخدام البخاخ الموسع مع الحجرة (Spacer) فوراً، والابتعاد عن دخان السجائر والأتربة.'),
        ('جلسات النيبولايزر:', 'جلسات بخار منزلية معقمة عبر ممرض متمرس لتهدئة تنفس الطفل سريعاً وبأمان.')
    ],
    'taqweyat-almunaaah-turuq-ilmiyya': [
        ('الركائز المثبتة:', 'نوم عميق 7-8 ساعات، غذاء غني بمضادات الأكسدة والزنك وفيتامين C، والتحكم بالتوتر العصبي.'),
        ('الأساطير الشائعة:', 'لا توجد خلطة سحرية ترفع المناعة بين ليلة وضحاها؛ المناعة أسلوب حياة تراكمي.'),
        ('الحماية الطبية:', 'التطعيمات الدورية (كالإنفلونزا الموسمية) وفحص نسب الفيتامينات والمعادن بانتظام.')
    ],
    'alqastathra-albouliyya-fil-manzil': [
        ('دواعي الاستخدام:', 'احتباس البول الحاد، طريحو الفراش بعد العمليات الكبرى، ومرضى الجلطات أو تضخم البروستاتا.'),
        ('شروط الأمان:', 'تعقيم مطلق، استخدام قسطرة سيليكون أصلية، وتفريغ الكيس بانتظام لمنع صعود البكتيريا للكلى.'),
        ('الخدمة بالفيوم:', 'تركيب وتغيير القسطرة البولية بالمنزل بأيدي ممرض متخصص دون الحاجة لنقل المريض.')
    ],
    'motabaaat-marid-alsukkar-fil-manzil': [
        ('خطة المتابعة:', 'جدول تسجيل القراءات قبل الإفطار وبعد الوجبات بساعتين لضبط الجرعات مع الطبيب.'),
        ('طوارئ الهبوط:', 'التعامل الفوري مع أعراض هبوط السكر (عرق بارد، رعشة، دوار) بقاعدة 15 جرام كربوهيدرات سريعة.'),
        ('حماية القدمين:', 'فحص يومي لأي احمرار أو تشقق للتدخل المبكر ومنع تحولها إلى قرح سكرية.')
    ],
    'aiktiaab-mabead-alwilada': [
        ('الفرق الحاسم:', 'كآبة الأمومة العابرة تختفي خلال أسبوعين، أما الاكتئاب فيستمر ويصحبه عجز عن رعاية الرضيع وشعور بالذنب.'),
        ('أسباب بيولوجية:', 'انخفاض مفاجئ في هرموني الإستروجين والبروجستيرون مع قلة النوم والإجهاد الجسدي للولادة.'),
        ('طريق التعافي:', 'طلب المساعدة الطبية دون خجل، دعم الزوج والأسرة، وتوفير راحة بدنية كافية للأم.')
    ],
    'iltihab-almafasil-alroumatoidee': [
        ('طبيعة المرض:', 'مرض مناعي ذاتي يهاجم بطانة المفاصل ويسبب تيبساً صباحياً يستمر لأكثر من ساعة.'),
        ('العلاج الحديث:', 'الأدوية المعدلة للمرض (DMARDs) والبيولوجية لمنع تآكل وتشوه المفاصل مبكراً.'),
        ('الرعاية اليومية:', 'كمادات دافئة صباحاً، تمارين خفيفة دون إجهاد، ودعم تمريضي لإعطاء الحقن الوريدية أو العضلية.')
    ],
    'aljafaf-3nd-kibar-alsen': [
        ('الخطر الصامت:', 'مركز العطش في الدماغ يضعف مع التقدم بالسن؛ المسن قد يكون جافاً تماماً دون أن يطلب الماء.'),
        ('علامات الخطر:', 'تشوش ذهني مفاجئ، جفاف الفم واللسان، بول داكن مركز، وهبوط حاد بضغط الدم عند الوقوف.'),
        ('الحل المنزلي:', 'تقديم السوائل بانتظام على مدار اليوم، وتعليق محاليل وريدية منزلية إسعافية عند الجفاف الحاد.')
    ],
    'naks-alhadid-3nd-alnisaa': [
        ('لماذا النساء؟', 'الدورة الشهرية الغزيرة، الحمل والرضاعة، والأنظمة الغذائية الفقيرة باللحوم الحمراء.'),
        ('الأعراض الكاشفة:', 'شحوب الوجه، برودة اليدين والقدمين، خفقان بالقلب، وتساقط شديد في الشعر وهشاشة الأظافر.'),
        ('العلاج المتكامل:', 'تغذية علاجية، أقراص حديد مع فيتامين C، أو محاليل حديد وريدية بالمنزل لتعويض النقص الحاد.')
    ],
    'naks-vitameen-d-arad-welaj': [
        ('المفارقة في مصر:', 'انتشار النقص رغم الشمس بسبب عدم التعرض المباشر واستخدام واقيات الشمس والحجاب.'),
        ('الأعراض الشائعة:', 'آلام مبهمة بالعظام وأسفل الظهر، ضعف العضلات، تساقط الشعر، واضطراب الحالة المزاجية.'),
        ('البروتوكول العلاجي:', 'جرعات علاجية مكثفة (50 ألف وحدة أسبوعياً) ثم جرعة وقائية بعد الوصول للمستوى الآمن.')
    ],
    'iltial-alkalya-alsukari-oqaya': [
        ('كيف يبدأ؟', 'ارتفاع السكر المزمن يدمر الفلاتر الدقيقة في الكلى، ويبدأ بتسريب زلال دقيق في البول (Microalbuminuria).'),
        ('الوقاية الحتمية:', 'ضبط السكر التراكمي تحت 7%، ضبط ضغط الدم تحت 130/80، وتجنب المسكنات غير الستيرويدية نهائياً.'),
        ('الفحص السنوي:', 'تحليل نسبة الزلال للكرياتينين في البول ووظائف الكلى سنوياً لاكتشاف أي اعتلال مبكراً.')
    ],
    'tamreed-manzili-fayoum': [
        ('الخدمة المتكاملة:', 'أول منصة ذكية تربط أهالي الفيوم بأقرب ممرض مرخص ومفحوص أمنياً خلال 15-25 دقيقة.'),
        ('الخدمات المغطاة:', 'كانيولا، محاليل، غيار جروح معقم، قسطرة بولية، ورعاية كبار السن على مدار 24 ساعة.'),
        ('التسعير العادل:', 'أسعار معلنة وثابتة 100% دون مساومة أو استغلال طارئ في كافة أنحاء مدينة الفيوم ومراكزها.')
    ],
    'tamreed-manzili-senouris': [
        ('التغطية بسنورس:', 'خدمة فورية تغطي مدينة سنورس، بيهمو، فديمين، ترسا، جرفس، ومطرطارس وكافة القرى المجاورة.'),
        ('سرعة الوصول:', 'ممرضون متأهبون في نطاق سنورس يصلون إليك في 12-18 دقيقة بحقيبة معقمة بالكامل.'),
        ('الحجز السريع:', 'اتصال طوارئ مباشر أو حجز فوري عبر الواتساب والتطبيق بأسعار موحدة ومعتمدة.')
    ],
    'tamreed-manzili-ebshaway': [
        ('التغطية بإبشواي:', 'تغطية شاملة لمدينة إبشواي، العجميين، طامية، شكشوك، وقرى قارون وكافة النطاق المحيط.'),
        ('كادر تمريضي مرخص:', 'ممرضون وممرضات مسجلون بنقابة التمريض ومفحوصون جنائياً لرعاية أهلك بأمان تام.'),
        ('جاهزية 24/7:', 'استجابة طارئة للمحاليل والكانيولا وغيار الجروح في أي وقت ليلاً أو نهاراً بنفس التسعيرة.')
    ]
}

def generate_summary_box(slug, title):
    points = SUMMARIES.get(slug, [
        ('ما الذي يقدمه هذا الدليل؟', f'معلومات طبية موثوقة ومبسطة حول {title} أعدها فريق التمريض السريري.'),
        ('معايير الأمان المنزلي:', 'إرشادات عملية لحماية المريض بالمنزل ومتى يجب طلب استشارة طبية أو تمريضية فورية.'),
        ('خدمة كيور بالفيوم:', 'ممرضون مرخصون ومفحوصون يصلون إلى باب بيتك خلال 15-25 دقيقة لتقديم الرعاية بأمان.')
    ])
    
    items_html = ''.join([f'<li><strong>{p[0]}</strong> {p[1]}</li>' for p in points])
    
    return f'''    <!-- Quick 30-Second Clinical Summary Box -->
    <div style="background: var(--c-primary-surface); border: 1.5px solid var(--c-brand-15); border-right: 5px solid var(--c-brand); border-radius: var(--r-md); padding: 24px 26px; margin-bottom: 35px; box-shadow: var(--shadow-xs);">
      <div style="display: flex; align-items: center; gap: 10px; font-family: var(--ff-head); font-weight: 800; color: var(--c-brand-deep); font-size: 18px; margin-bottom: 12px;">
        <i class="fas fa-clipboard-check" style="color: var(--c-secondary); font-size: 22px;"></i>
        <span>ملخص سريري سريع (في 30 ثانية فقط)</span>
      </div>
      <ul style="margin: 0; padding-right: 20px; color: var(--c-body); font-size: 15.5px; line-height: 1.85;">
        {items_html}
      </ul>
    </div>'''

def generate_inline_cta():
    return '''        <!-- Inline Emergency/Home Care Box -->
        <div style="background: linear-gradient(135deg, var(--c-primary-surface) 0%, #ecfdf5 100%); border: 1.5px solid var(--c-secondary); border-radius: var(--r-md); padding: 24px; margin: 35px 0; display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap;">
          <div>
            <h3 style="font-family: var(--ff-head); font-size: 19px; font-weight: 900; color: var(--c-heading); margin: 0 0 6px;">هل تحتاج إلى رعاية تمريضية متخصصة في الفيوم؟</h3>
            <p style="font-size: 14px; color: var(--c-muted); margin: 0;">ممرضون معتمدون ومفحوصون يصلون إلى باب بيتك خلال 15-25 دقيقة بحقيبة معقمة بالكامل.</p>
          </div>
          <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <a href="tel:01070203636" style="background: var(--c-brand); color: #fff; padding: 10px 20px; border-radius: var(--r-pill); font-weight: 800; font-size: 13.5px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
              <i class="fas fa-phone-alt"></i> اتصل بالطوارئ
            </a>
            <a href="https://wa.me/201070203636?text=مرحباً،+أريد+حجز+خدمة+تمريض+منزلي+في+الفيوم" target="_blank" rel="noopener" style="background: var(--c-secondary); color: #fff; padding: 10px 20px; border-radius: var(--r-pill); font-weight: 800; font-size: 13.5px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
              <i class="fab fa-whatsapp"></i> حجز عبر واتساب
            </a>
          </div>
        </div>'''

def generate_progress_bar_script():
    return '''<script>
  // Reading Progress Bar
  window.addEventListener('scroll', () => {
    const doc = document.documentElement;
    const winScroll = doc.scrollTop || document.body.scrollTop;
    const height = doc.scrollHeight - doc.clientHeight;
    const scrolled = (winScroll / height) * 100;
    const bar = document.getElementById('readingProgress');
    if (bar) bar.style.width = scrolled + '%';
  });
</script>'''

def upgrade_article(filepath):
    slug = os.path.basename(filepath).replace('.html', '')
    if slug == 'mahloul-hadid-waridee-fil-manzil':
        print(f"Skipping {slug} (already upgraded).")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add reading progress bar after </nav> if not present
    if 'id="readingProgress"' not in html:
        nav_pattern = re.compile(r'(</nav>)', re.IGNORECASE)
        progress_div = '\n\n<div id="readingProgress" style="position: fixed; top: 0; right: 0; left: 0; height: 3.5px; background: var(--c-secondary); width: 0%; z-index: 9999; transition: width 0.1s ease;"></div>'
        html = nav_pattern.sub(r'\1' + progress_div, html, count=1)

    # 2. Update badge in article-hero
    badge_pattern = re.compile(r'<span class="badge">.*?</span>', re.DOTALL)
    new_badge = '''<span class="badge" style="background: var(--c-secondary-bg); color: var(--c-secondary); border: 1px solid rgba(5, 150, 105, 0.3); font-weight: 800; padding: 4px 14px; border-radius: var(--r-pill); display: inline-flex; align-items: center; gap: 6px;">
          <i class="fas fa-stethoscope"></i> دليل الرعاية الطبية المعتمدة بالمنزل
        </span>'''
    html = badge_pattern.sub(new_badge, html, count=1)

    # 3. Add 30-second summary box before <article class="content"> if not present
    if 'ملخص سريري سريع' not in html:
        title_match = re.search(r'<h1>(.*?)</h1>', html)
        title = title_match.group(1) if title_match else slug
        summary_box = generate_summary_box(slug, title)
        article_content_pattern = re.compile(r'(<article class="content">)', re.IGNORECASE)
        html = article_content_pattern.sub(summary_box + '\n\n    ' + r'\1', html, count=1)

    # 4. Add inline CTA box before FAQ or before </article> if not present
    if 'هل تحتاج إلى رعاية تمريضية متخصصة في الفيوم؟' not in html:
        inline_cta = generate_inline_cta()
        if '<hr />' in html:
            # Insert before the last <hr /> or before <h2>الأسئلة الشائعة
            faq_pos = html.find('<h2>الأسئلة الشائعة')
            if faq_pos != -1:
                html = html[:faq_pos] + inline_cta + '\n\n        ' + html[faq_pos:]
            else:
                html = html.replace('</article>', inline_cta + '\n    </article>', 1)
        else:
            html = html.replace('</article>', inline_cta + '\n    </article>', 1)

    # 5. Upgrade bottom cta-card buttons
    old_cta_block = re.search(r'<div class="cta-card">.*?</div>\s*</div>', html, re.DOTALL)
    if old_cta_block:
        title_cta = "هل تحتاج إلى ممرض منزلي معتمد في الفيوم الآن؟"
        new_cta_card = f'''<div class="cta-card">
      <h2>{title_cta}</h2>
      <p>فريق كيور الطبي متاح على مدار 24 ساعة في كافة مراكز محافظة الفيوم. رعاية طبية متكاملة حتى باب بيتك بأسعار معلنة وثابتة.</p>
      <div class="cta-btns">
        <a href="https://wa.me/201070203636?text=مرحباً،+أريد+حجز+خدمة+تمريض+منزلي+في+الفيوم" class="btn-green-cta" target="_blank" rel="noopener">
          <i class="fab fa-whatsapp"></i> حجز سريع عبر واتساب
        </a>
        <a href="tel:01070203636" class="btn-white-cta">
          <i class="fas fa-phone-alt"></i> اتصال هاتفي مباشر
        </a>
      </div>
    </div>'''
        html = re.sub(r'<div class="cta-card">.*?</div>\s*(?=</div>|\s*<footer)', new_cta_card + '\n', html, flags=re.DOTALL)

    # 6. Add Progress Bar script before </body> if not present
    if 'id="readingProgress"' in html and 'readingProgress.style.width' not in html:
        html = html.replace('</body>', generate_progress_bar_script() + '\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Successfully upgraded {slug}.html")

def main():
    articles = glob.glob('*.html')
    exclude = ['index.html', 'pricing.html', 'faq.html', 'careers.html', 'articles.html', 'terms.html', 'privacy.html']
    target_articles = [a for a in articles if a not in exclude]
    
    print(f"Starting batch upgrade for {len(target_articles)} articles...")
    for a in target_articles:
        upgrade_article(a)
    print("Batch upgrade completed successfully!")

if __name__ == '__main__':
    main()
