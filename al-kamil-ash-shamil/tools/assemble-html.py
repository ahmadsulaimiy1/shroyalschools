#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, html

exec(open("/tmp/book2/meta.py", encoding="utf-8").read())  # BOOK_TITLE, BOOK_SUBTITLE, BOOK_AUTHOR_LINE

fonts_css = open("/tmp/book2/fonts_css.txt", encoding="utf-8").read()
design_css = open("/tmp/book2/design_css.txt", encoding="utf-8").read()
body = open("/tmp/book2/body.html", encoding="utf-8").read()

def esc(s):
    return html.escape(s, quote=False)

# ---------- Build TOC by scanning body.html for part-openers and chapter-titles ----------
toc_items = []  # list of (bab_id, bab_title, [(verse_id, verse_title), ...])
for m in re.finditer(r'<section class="part-opener" id="(bab\d+)">.*?<h2>(.*?)</h2>', body, re.S):
    toc_items.append([m.group(1), m.group(2), []])

for m in re.finditer(r'<article class="chapter" id="((bab\d+)-v\d+)">\s*<h2 class="chapter-title">(.*?)</h2>', body):
    vid, bid, title = m.group(1), m.group(2), m.group(3)
    for entry in toc_items:
        if entry[0] == bid:
            entry[2].append((vid, title))
            break

toc_html = ['<ul class="toc">']
for bid, btitle, verses in toc_items:
    toc_html.append(f'<li><a class="part-link" href="#{bid}"><span>{btitle}</span></a>')
    if verses:
        toc_html.append('<ul>')
        for vid, vtitle in verses:
            toc_html.append(f'<li><a class="chap-link" href="#{vid}"><span>{vtitle}</span><span class="dots"></span></a></li>')
        toc_html.append('</ul>')
    toc_html.append('</li>')
toc_html.append('</ul>')
toc_html = "\n".join(toc_html)
print(f"TOC: {len(toc_items)} babs, {sum(len(v) for _,_,v in toc_items)} verses")

# ---------- Assemble full HTML ----------
HEAD = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(BOOK_TITLE)}</title>
<meta name="description" content="{esc(BOOK_SUBTITLE)}">
<style>
/* Embedded fonts (Amiri, Amiri Quran, Aref Ruqaa, Cairo — Arabic subset, self-contained for offline/print use) */
{fonts_css}
</style>
<style>
{design_css}
</style>
</head>
<body>

<nav class="book-nav">
  <span class="brand">{esc(BOOK_TITLE)} — نسخة فاخرة</span>
  <span>
    <a href="#toc">الفهرس</a> ·
    <a href="#bibliography">قائمة المصادر</a>
  </span>
</nav>
"""

COVER = f"""
<section class="cover">
  <div class="eyebrow">سلسلة المراجع الشرعية · علوم القرآن الكريم</div>
  <div>
    <div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
    <h1>{esc(BOOK_TITLE)}</h1>
    <p class="subtitle">{esc(BOOK_SUBTITLE)}</p>
  </div>
  <div class="divider-star">۞</div>
  <div class="credits">
    <div class="role">تأليف</div>
    <div class="name">{esc(BOOK_AUTHOR_LINE.split('تأليف:')[-1].strip())}</div>
  </div>
  <div class="footer-line">نسخة رقمية — عن مخطوطة الشرح المقدمة من المؤلف</div>
</section>

<section class="half-title">
  <div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
  <h1>{esc(BOOK_TITLE)}</h1>
  <div class="tagline">{esc(BOOK_SUBTITLE)}</div>
</section>
"""

PUBLISHER = f"""
<section class="page frontmatter">
  <div class="page-pad">
    <h2>بيانات النشر</h2>
    <ul class="field-list">
      <li><span class="k">عنوان الكتاب</span><span class="v">{esc(BOOK_TITLE)}</span></li>
      <li><span class="k">الشرح على متن</span><span class="v">تحفة الأطفال والغلمان في تجويد القرآن، للعلامة سليمان الجمزوري رحمه الله</span></li>
      <li><span class="k">المؤلف</span><span class="v">{esc(BOOK_AUTHOR_LINE.split('تأليف:')[-1].strip())} <span class="placeholder">(هكذا عرّف المؤلف نفسه في المخطوطة، ولم يُثبت اسمًا صريحًا)</span></span></li>
      <li><span class="k">الرواية المعتمدة</span><span class="v">حفص عن عاصم</span></li>
      <li><span class="k">رقم الإيداع / ISBN</span><span class="v placeholder">يُستكمل من الناشر عند التسجيل الرسمي</span></li>
      <li><span class="k">سنة النشر</span><span class="v placeholder">يُستكمل من الناشر</span></li>
      <li><span class="k">جميع الحقوق محفوظة</span><span class="v">لا يجوز نسخ أي جزء من هذا الكتاب أو نقله بأي شكل من الأشكال إلا بإذن خطي من المؤلف، فيما عدا الاستشهاد العلمي بالإشارة إلى المصدر</span></li>
    </ul>
    <div class="small-note">
      هذه الصفحة قالبٌ لبيانات النشر الرسمية. تُستكمل من الناشر المعتمد قبل الطباعة النهائية، ولم تُدرَج بيانات افتراضية تجنّباً لأي معلومة غير موثقة.
    </div>
  </div>
</section>

<section class="page frontmatter">
  <div class="page-pad">
    <h2>ملاحظة تحريرية</h2>
    <p style="font-family:'Cairo',sans-serif; color:var(--ink-500); line-height:2;">
      أُعدت هذه النسخة الفاخرة مباشرة من مخطوطة الشرح كما وردت من المؤلف، مع الحفاظ التام على نصه العلمي دون تغيير أو اختصار. والمخطوطة المزوَّدة تنتهي أثناء الكلام على «باب المدود» (عند تفصيل المد اللازم الحرفي)، دون خاتمة ختامية للباب أو للكتاب، ودون فهارس علمية بعد. وقد أُبقي المتن على حاله دون إكمال مُفتَرَض أو خاتمة مُستحدثة، حرصًا على الأمانة العلمية؛ وتُستكمل هذه الأجزاء (خاتمة باب المدود، وخاتمة الكتاب، والفهارس) في إصدار لاحق عند توفرها من المؤلف.
    </p>
  </div>
</section>
"""

TOC_SECTION = f"""
<section class="page frontmatter" id="toc">
  <div class="page-pad">
    <h2>فهرس المحتويات</h2>
    {toc_html}
  </div>
</section>
"""

BIBLIOGRAPHY = """
<section class="page frontmatter content" id="bibliography">
  <div class="page-pad">
    <h2>قائمة المصادر</h2>
    <p style="font-family:'Cairo',sans-serif; color:var(--ink-500); font-size:.85rem; margin-bottom:1.2em;">مصنفات الناظم (الجمزوري) والأئمة الذين نص عليهم المؤلف صراحة في متن الشرح:</p>
    <h3 class="plain-h3">مصنفات الناظم (الشيخ سليمان الجمزوري)</h3>
    <ul style="font-family:'Amiri'; line-height:2.3;">
      <li><em>تحفة الأطفال والغلمان في تجويد القرآن</em> — المنظومة موضوع هذا الشرح.</li>
      <li><em>فتح الأقفال بشرح تحفة الأطفال</em>.</li>
      <li><em>الرسالة الفتحية في التجويد</em>.</li>
      <li><em>منحة ذي الجلال في شرح تحفة الأطفال</em>.</li>
      <li><em>كنز المعاني في شرح حرز الأماني</em> (شرح على الشاطبية).</li>
      <li><em>الطرازات المعلمة في شرح المقدمة</em> (شرح على مقدمة ابن الجزري).</li>
    </ul>
    <h3 class="plain-h3">أئمة مذكورون في متن الشرح</h3>
    <ul style="font-family:'Amiri'; line-height:2.3;">
      <li>الإمام أبو عمرو الداني.</li>
      <li>الإمام مكي بن أبي طالب القيسي.</li>
      <li>الإمام أبو القاسم الشاطبي.</li>
      <li>الإمام أبو الخير ابن الجزري — <em>النشر في القراءات العشر</em>، <em>المقدمة الجزرية</em>.</li>
      <li>الإمام أبو الحسن السخاوي.</li>
      <li>الإمام أبو عبد الله المواق.</li>
      <li>الشيخ نور الدين علي بن عمر الميهي — شيخ الناظم.</li>
    </ul>
    <div class="small-note">هذه القائمة مستخلصة من النصوص الصريحة الواردة في متن الشرح نفسه، دون إضافة مصادر لم يُشر إليها المؤلف.</div>
  </div>
</section>
"""

COLOPHON = f"""
<section class="colophon">
  <div class="bismillah">وَآخِرُ دَعْوَانَا أَنِ الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ</div>
  <h2>إلى هنا انتهت المخطوطة المتاحة</h2>
  <p>{esc(BOOK_TITLE)} — {esc(BOOK_SUBTITLE)}</p>
  <p style="font-size:.85rem; opacity:.85;">تنتهي هذه النسخة عند الموضع الذي بلغته المخطوطة المزوَّدة من المؤلف، ضمن باب المدود. نسأل الله أن ييسر إتمامه.</p>
  <div class="motif-rule" style="max-width:280px; margin:1.6em auto;"><span class="diamond"></span></div>
</section>

<footer class="book-footer">
  {esc(BOOK_TITLE)} · نسخة رقمية فاخرة · جميع الحقوق محفوظة للمؤلف
</footer>
"""

SCRIPT = """
<script>
document.addEventListener('DOMContentLoaded', function () {
  var QURAN_RE = /(﴿[^﴾]*﴾)(\\s*\\[[^\\]]*\\])?/g;
  var nodes = document.querySelectorAll('.content p, .content li, .content td, .content dd, .matn, .ruling');
  nodes.forEach(function (el) {
    if (el.querySelector('.ayah')) return;
    if (!/﴿/.test(el.innerHTML)) return;
    el.innerHTML = el.innerHTML.replace(QURAN_RE, function (m, ayah, ref) {
      var out = '<span class="ayah">' + ayah + '</span>';
      if (ref) out += '<span class="ref">' + ref + '</span>';
      return out;
    });
  });
});
</script>
</body>
</html>
"""

full = HEAD + COVER + PUBLISHER + TOC_SECTION + body + BIBLIOGRAPHY + COLOPHON + SCRIPT

with open("/home/user/shroyalschools/al-kamil-ash-shamil/index.html", "w", encoding="utf-8") as f:
    f.write(full)

print("wrote final HTML, total chars:", len(full))
