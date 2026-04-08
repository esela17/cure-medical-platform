// ═══════════════════════════════════════════════════════════════════
//   CURE — Google Apps Script Backend
//   يحفظ بيانات النماذج في Google Sheets ويرسل إشعاراً بالإيميل
//
//   طريقة الإعداد:
//   1. افتح script.google.com وأنشئ مشروعاً جديداً
//   2. الصق هذا الكود في المحرر
//   3. عدّل ADMIN_EMAIL و SPREADSHEET_ID
//   4. اضغط Deploy → New Deployment → Web App
//   5. انتبه: "Execute as" = Me ، "Who has access" = Anyone
//   6. انسخ الرابط النهائي وضعه في config.js
// ═══════════════════════════════════════════════════════════════════

/* ─────────────────────────────────────────────────────────────────
   ⚙️  CONFIGURATION — غيّر هذه القيم فقط
   ───────────────────────────────────────────────────────────────── */
const CONFIG = {
  adminEmail:    'eslam.hamada@cureztyx.com',   // بريد استقبال الإشعارات
  spreadsheetId: '1SVze2npO8mwXgOpGqiYaA_EM4tru-X3p511iXhewmuw', // معرف الشيت
  timezone:      'Africa/Cairo',
};

/* ─────────────────────────────────────────────────────────────────
   📥  ENTRY POINT — يستقبل طلبات POST من الموقع
   ───────────────────────────────────────────────────────────────── */
function doPost(e) {
  try {
    const params   = e.parameter;
    const formType = params.form_type || 'general';

    // 1. حفظ البيانات في Google Sheets
    saveToSheet(formType, params);

    // 2. إرسال إيميل إشعار
    sendNotificationEmail(formType, params);

    return jsonResponse({ result: 'success' });

  } catch (err) {
    console.error('[Cure] doPost error:', err);
    return jsonResponse({ result: 'error', message: err.message });
  }
}

/* يسمح بالتحقق من أن السكربت يعمل */
function doGet() {
  return ContentService
    .createTextOutput('✅ Cure Backend — Active | ' + new Date().toLocaleString('ar-EG'))
    .setMimeType(ContentService.MimeType.TEXT);
}

/* ─────────────────────────────────────────────────────────────────
   💾  SAVE TO SHEET
   ───────────────────────────────────────────────────────────────── */
function saveToSheet(sheetName, params) {
  const ss = CONFIG.spreadsheetId
    ? SpreadsheetApp.openById(CONFIG.spreadsheetId)
    : SpreadsheetApp.getActiveSpreadsheet();

  // أنشئ الشيت تلقائياً إذا لم يكن موجوداً
  let sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }

  // اختر الأعمدة حسب نوع النموذج
  const schema = getSchema(sheetName, params);

  // أضف رأس الأعمدة في أول سطر إذا كان الشيت فارغاً
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['📅 التاريخ', ...schema.headers, '🏷️ الحالة']);
    sheet.getRange(1, 1, 1, schema.headers.length + 2)
         .setBackground('#6B5CE7')
         .setFontColor('#FFFFFF')
         .setFontWeight('bold');
    sheet.setFrozenRows(1);
  }

  // أضف البيانات
  const timestamp = Utilities.formatDate(
    new Date(), CONFIG.timezone, 'yyyy-MM-dd HH:mm:ss'
  );
  const row = [timestamp, ...schema.extract(params), 'جديد 🆕'];
  sheet.appendRow(row);

  // تنسيق السطر الجديد
  const lastRow = sheet.getLastRow();
  if (lastRow % 2 === 0) {
    sheet.getRange(lastRow, 1, 1, row.length)
         .setBackground('#F8F7FF');
  }
}

/* ─────────────────────────────────────────────────────────────────
   📋  SCHEMAS — هيكل كل نوع نموذج
   ───────────────────────────────────────────────────────────────── */
function getSchema(formType, params) {
  const schemas = {

    nurse_registration: {
      headers: ['الاسم', 'الهاتف', 'المنطقة', 'التخصص', 'الخبرة', 'الرسالة'],
      extract: p => [p.name, p.phone, p.area, p.specialty, p.experience, p.message],
    },

    internship_application: {
      headers: ['الاسم', 'البريد', 'السن', 'العنوان', 'المرحلة الدراسية',
                'مجال الإنترنشيب', 'طريقة العمل', 'CV / Portfolio',
                'هل عرف أحد CURE؟'],
      extract: p => [
        p.name, p.email, p.age, p.address, p.education,
        p.internship_field, p.work_preference, p.cv_link,
        p.knew_about_nursing,
      ],
    },

    contact_form: {
      headers: ['الاسم', 'البريد', 'الهاتف', 'نوع الاستفسار', 'الرسالة'],
      extract: p => [p.name, p.email, p.phone, p.inquiry_type, p.message],
    },

  };

  // Fallback: احفظ كل الحقول
  return schemas[formType] || {
    headers: Object.keys(params).filter(k => k !== 'form_type'),
    extract: (p) => Object.entries(p).filter(([k]) => k !== 'form_type').map(([, v]) => v),
  };
}

/* ─────────────────────────────────────────────────────────────────
   📧  EMAIL NOTIFICATION — إرسال إيميل إشعار
   ───────────────────────────────────────────────────────────────── */
function sendNotificationEmail(formType, params) {
  const templates = {

    nurse_registration: {
      subject: `🩺 ممرض جديد يريد التسجيل — ${params.name || ''}`,
      body: `
مرحباً!

طلب تسجيل جديد من ممرض على موقع كيور:

━━━━━━━━━━━━━━━━━━━━━━━
👤 الاسم       : ${params.name     || '—'}
📞 الهاتف      : ${params.phone    || '—'}
📍 المنطقة     : ${params.area     || '—'}
🩺 التخصص      : ${params.specialty || '—'}
⏱️ الخبرة      : ${params.experience || '—'}
💬 رسالة        : ${params.message   || '—'}
━━━━━━━━━━━━━━━━━━━━━━━

يمكنك الرد مباشرة على الهاتف أو من خلال Google Sheets.

— نظام كيور الآلي
      `.trim(),
    },

    internship_application: {
      subject: `🎓 طلب إنترنشيب جديد — ${params.name || ''}`,
      body: `
طلب إنترنشيب جديد على منصة كيور:

━━━━━━━━━━━━━━━━━━━━━━━
👤 الاسم           : ${params.name              || '—'}
📧 البريد           : ${params.email             || '—'}
🎂 السن             : ${params.age               || '—'}
📍 العنوان          : ${params.address           || '—'}
📚 المرحلة الدراسية : ${params.education         || '—'}
💼 المجال           : ${params.internship_field  || '—'}
🏠 طريقة العمل     : ${params.work_preference   || '—'}
📄 رابط CV         : ${params.cv_link           || '—'}
🏥 تجربة CURE      : ${params.knew_about_nursing || '—'}
━━━━━━━━━━━━━━━━━━━━━━━

— نظام كيور الآلي
      `.trim(),
    },

    contact_form: {
      subject: `📩 رسالة جديدة من الموقع — ${params.name || 'زائر'}`,
      body: `
رسالة جديدة من موقع كيور:

━━━━━━━━━━━━━━━━━━━━━━━
👤 الاسم    : ${params.name         || '—'}
📧 البريد   : ${params.email        || '—'}
📞 الهاتف  : ${params.phone        || '—'}
📂 النوع   : ${params.inquiry_type || '—'}
💬 الرسالة : ${params.message      || '—'}
━━━━━━━━━━━━━━━━━━━━━━━

      `.trim(),
    },

  };

  const tpl = templates[formType] || {
    subject: `📩 إرسال جديد من موقع كيور (${formType})`,
    body:    JSON.stringify(params, null, 2),
  };

  MailApp.sendEmail({
    to:      CONFIG.adminEmail,
    subject: tpl.subject,
    body:    tpl.body,
  });
}

/* ─────────────────────────────────────────────────────────────────
   🔧  HELPER — JSON response مع CORS headers
   ───────────────────────────────────────────────────────────────── */
function jsonResponse(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
