import re

with open('careers.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the text logo
html = html.replace('<div class="logo-mark">ك</div>', '<img src="assets/png/2.png" alt="كيور" style="height: 45px; width: auto; object-fit: contain;"> ')

# Remove the old CSS .logo-mark
html = re.sub(r'\.logo-mark\s*\{[^}]+\}', '', html)

# Add the Language Toggle CSS
css_to_add = """
/* Lang Toggle */
.lang-toggle-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border);
  color: var(--light);
  padding: 5px 10px;
  border-radius: 6px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  font-family: var(--font-main);
  font-size: 14px;
  z-index: 1001;
}
.lang-toggle-btn:hover {
  background: rgba(107, 92, 231, 0.15);
  border-color: var(--purple);
  color: var(--white);
}
.mobile-only { display: none; }
@media (max-width: 991px) {
  .mobile-only { display: block; }
}

/* Hide Google Translate Banner */
.goog-te-banner-frame.skiptranslate, .goog-te-gadget-icon, #goog-gt-tt { display: none !important; }
body { top: 0px !important; }
.goog-tooltip { display: none !important; }
.goog-tooltip:hover { display: none !important; }
.goog-text-highlight { background-color: transparent !important; border: none !important; box-shadow: none !important; }
"""
html = html.replace('</style></head>', f'{css_to_add}</style></head>')

# Add JS logic for the Translate at the end of the file
js_to_add = """
<script src="assets/js/jobsData.js"></script>
<script>
function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') c = c.substring(1);
    if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
  }
  return "";
}

function toggleLanguage() {
  const currentLang = getCookie('googtrans');
  if (currentLang && currentLang.includes('/en')) {
    document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=" + location.hostname + "; path=/;";
    location.reload();
  } else {
    setCookie("googtrans", "/ar/en", 30);
    location.reload();
  }
}

window.addEventListener("DOMContentLoaded", () => {
    const lang = getCookie("googtrans");
    const toggleBtns = document.querySelectorAll(".lang-toggle-btn");
    if(lang && lang.includes("/en")) {
        toggleBtns.forEach(btn => btn.textContent = "AR");
        document.documentElement.dir = "ltr";
        // Also ensure modal translates appropriately
        const jobView = document.getElementById('job-info-view');
        if(jobView) jobView.style.direction = "ltr";
    } else {
        toggleBtns.forEach(btn => btn.textContent = "EN");
    }
});

function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'ar', includedLanguages: 'ar,en', autoDisplay: false}, 'google_translate_element');
}
</script>
<div id="google_translate_element" style="display:none;"></div>
<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</body>
"""
html = html.replace('</body>', js_to_add)


# Replace logic in openModal in JS (inside the giant line or the script tags)
# It's currently in the script block later.
# Let's add the Job Info View HTML.
modal_html = """
<div id="job-info-view" style="display:none; padding: 24px 40px; color: var(--light);">
  <div style="background: rgba(107, 92, 231, 0.1); border: 1px solid rgba(107, 92, 231, 0.2); border-radius: 12px; padding: 16px; margin-bottom: 24px; text-align: center;">
    <h3 id="info-title" style="color: var(--white); font-size: 20px; font-weight: 800; margin-bottom: 8px;"></h3>
    <span id="info-type" style="display: inline-block; background: var(--purple); color: #fff; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700;"></span>
  </div>
  
  <h4 style="color: var(--white); margin-bottom: 8px; font-size: 16px;">عن الوظيفة</h4>
  <p id="info-about" style="font-size: 14px; line-height: 1.6; margin-bottom: 24px;"></p>
  
  <h4 style="color: var(--white); margin-bottom: 8px; font-size: 16px;">المسؤوليات الرئيسية</h4>
  <ul id="info-resp" style="font-size: 14px; line-height: 1.6; padding-inline-start: 20px; margin-bottom: 24px; list-style-type: disc;"></ul>
  
  <h4 style="color: var(--white); margin-bottom: 8px; font-size: 16px;">المتطلبات</h4>
  <ul id="info-req" style="font-size: 14px; line-height: 1.6; padding-inline-start: 20px; margin-bottom: 24px; list-style-type: disc;"></ul>
  
  <h4 style="color: var(--white); margin-bottom: 8px; font-size: 16px;">المميزات</h4>
  <ul id="info-ben" style="font-size: 14px; line-height: 1.6; padding-inline-start: 20px; margin-bottom: 32px; list-style-type: none;"></ul>
  
  <button class="btn-primary" style="width: 100%; justify-content: center;" onclick="startApplication()">قدّم الآن <i class="fas fa-arrow-left"></i></button>
</div>
"""
# Insert modal_html into the modal-body before step1
html = html.replace('<div class="step-panel active" id="step1">', f'{modal_html}<div class="step-panel" id="step1">')


# Add the startApplication function and modify openModal function
# In original script, openModal sets title and starts at step 1.
# We want it to open the job-info-view instead.
openModalReplacement = """function openModal(title) {
  const job = window.jobsData ? window.jobsData[title] : null;
  document.getElementById('modal-job-title').textContent = title;
  document.getElementById('form-position').value = title;
  document.getElementById('form-subject').value = 'طلب تدريب — ' + title + ' — كيور';
  
  if (job) {
    document.getElementById('info-title').textContent = title;
    document.getElementById('info-type').textContent = job.type;
    document.getElementById('info-about').textContent = job.about;
    document.getElementById('info-resp').innerHTML = job.responsibilities.map(r => `<li>${r}</li>`).join('');
    document.getElementById('info-req').innerHTML = job.requirements.map(r => `<li>${r}</li>`).join('');
    document.getElementById('info-ben').innerHTML = job.benefits.map(b => `<li style="margin-bottom:6px;"><i class="fas fa-check-circle" style="color:var(--green); margin-inline-end:8px;"></i>${b}</li>`).join('');
    
    document.getElementById('job-info-view').style.display = 'block';
    
    // Hide standard form elements during view
    document.querySelector('.progress-wrap').style.display = 'none';
    for(let i=1; i<=4; i++) {
        let p = document.getElementById('step'+i);
        if(p) p.classList.remove('active');
    }
  } else {
    // Fallback if no data
    startApplication();
  }

  document.getElementById('overlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function startApplication() {
  document.getElementById('job-info-view').style.display = 'none';
  document.querySelector('.progress-wrap').style.display = 'block';
  currentStep = 1;
  showStep(1);
}
"""

html = re.sub(r'function openModal\(title\)\s*\{[^}]+\s*currentStep=1;\s*showStep\(1\);\s*\}', openModalReplacement, html)


# Fix language button in nav
# Replace `</ul></div>` with `<li><button class="lang-toggle-btn" onclick="toggleLanguage()">EN</button></li></ul><div style="display: flex; align-items: center; gap: 12px;"><button class="lang-toggle-btn mobile-only" onclick="toggleLanguage()">EN</button><div class="hamburger" onclick="toggleMenu()"><span></span><span></span><span></span></div></div></div>` (adjusting for minification if needed)
# A safer way to inject nav items:
html = html.replace('<a href="#positions" class="nav-cta">قدّم الآن</a></li></ul></div></nav>', 
                    '<a href="#positions" class="nav-cta">قدّم الآن</a></li><li><button class="lang-toggle-btn" onclick="toggleLanguage()">EN</button></li></ul><div style="display: flex; align-items: center; gap: 12px;"><button class="lang-toggle-btn mobile-only" onclick="toggleLanguage()">EN</button><div class="hamburger" onclick="toggleMenu()"><span></span><span></span><span></span></div></div></div></nav>')

with open('careers.html', 'w', encoding='utf-8') as f:
    f.write(html)

