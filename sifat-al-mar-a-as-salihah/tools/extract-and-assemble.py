#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, html
import docx

SRC = "/root/.claude/uploads/c0d02c27-08d9-5bbc-b193-2fc67eeecf61/a19fec7c-______________.docx"
OUT_DIR = "/home/user/shroyalschools/sifat-al-mar-a-as-salihah"

BOOK_TITLE = "صفات المرأة الصالحة في الإسلام"
BOOK_AUTHOR = "أبو عبد الله أحمد بن إبراهيم بن السليمي"

d = docx.Document(SRC)
paras = [p.text.strip() for p in d.paragraphs]
paras = [t for t in paras if t and t != "-"]

def esc(s):
    return html.escape(s, quote=False)

BAB_RE = re.compile(r"^الباب \S+(?: \S+)?$")
QURAN_RE = re.compile(r"^[{}](.+?)[{}]\.?$")
HADITH_RE = re.compile(r'^"(.+?)"\.?$')
LABEL_LEAD_RE = re.compile(r"^([ء-ي][ء-ي\s]{1,26}?[:：])\s*(.+)$")
POETRY_INTRO = "ولهذا قيل قديمًا:"

def bold_lead(text):
    m = LABEL_LEAD_RE.match(text)
    if m and len(m.group(1)) <= 30:
        return f"<strong>{esc(m.group(1))}</strong> {esc(m.group(2))}"
    return esc(text)

out = []
bab_count = 0
i = 0
n = len(paras)

# ---- front matter: everything before the first "الباب " ----
first_bab_idx = next(i for i, t in enumerate(paras) if BAB_RE.match(t))
intro_paras = paras[:first_bab_idx]  # starts with "المقدمة"
main_paras = paras[first_bab_idx:]

out.append('<section class="page frontmatter content" id="muqaddimah">')
out.append('<div class="page-pad">')
for t in intro_paras:
    if t == "المقدمة":
        out.append("<h2>المقدمة</h2>")
    else:
        out.append(f"<p>{bold_lead(t)}</p>")
out.append("</div></section>")

# ---- main babs ----
i = 0
n = len(main_paras)
content_open = False

def close_content():
    global content_open
    if content_open:
        out.append("</div></section>")
        content_open = False

while i < n:
    t = main_paras[i]

    if BAB_RE.match(t):
        close_content()
        bab_count += 1
        bid = f"bab{bab_count}"
        subtitle = main_paras[i + 1] if i + 1 < n else ""
        out.append(f'<section class="part-opener" id="{bid}">')
        out.append(f'<div class="kicker">{esc(t)}</div>')
        out.append(f'<div class="num">{bab_count}</div>')
        out.append(f"<h2>{esc(subtitle)}</h2>")
        out.append("</section>")
        out.append('<section class="page"><div class="content">')
        content_open = True
        i += 2
        continue

    if t == POETRY_INTRO:
        out.append(f"<p>{esc(t)}</p>")
        if i + 2 < n:
            line1, line2 = main_paras[i + 1], main_paras[i + 2]
            out.append(f'<div class="matn">{esc(line1)} ... {esc(line2)}</div>')
            i += 3
            continue
        i += 1
        continue

    m = QURAN_RE.match(t)
    if m:
        out.append(f'<div class="matn">﴿{esc(m.group(1).strip())}﴾</div>')
        i += 1
        continue

    m = HADITH_RE.match(t)
    if m:
        out.append(f'<div class="hadith">{esc(m.group(1).strip())}</div>')
        i += 1
        continue

    # list detection: paragraph ends with ':' and next 2+ paragraphs are short standalone phrases
    if t.endswith(":") or t.endswith("："):
        j = i + 1
        items = []
        while j < n and len(main_paras[j]) < 30 and not BAB_RE.match(main_paras[j]) \
                and not QURAN_RE.match(main_paras[j]) and not HADITH_RE.match(main_paras[j]) \
                and main_paras[j] != POETRY_INTRO and not main_paras[j].endswith(":"):
            items.append(main_paras[j])
            j += 1
        if len(items) >= 2:
            out.append(f"<p>{esc(t)}</p>")
            out.append("<ul>")
            for it in items:
                out.append(f"<li>{esc(it)}</li>")
            out.append("</ul>")
            i = j
            continue

    out.append(f"<p>{bold_lead(t)}</p>")
    i += 1

close_content()

body_html = "\n".join(out)
print(f"bab_count={bab_count}, body length={len(body_html)}")

# ============================== ASSEMBLE FULL DOCUMENT ==============================
fonts_css = open("/tmp/book3/fonts_css.txt", encoding="utf-8").read()
design_css = open("/tmp/book3/design_css.txt", encoding="utf-8").read()

# ---- TOC (scan body_html for part-openers) ----
toc_items = []
for mm in re.finditer(r'<section class="part-opener" id="(bab\d+)">\s*<div class="kicker">(.*?)</div>\s*<div class="num">\d+</div>\s*<h2>(.*?)</h2>', body_html):
    toc_items.append((mm.group(1), mm.group(2), mm.group(3)))

toc_html = ['<ul class="toc">']
for bid, kicker, title in toc_items:
    toc_html.append(f'<li><a class="part-link" href="#{bid}"><span>{kicker}: {title}</span></a></li>')
toc_html.append("</ul>")
toc_html = "\n".join(toc_html)
print(f"TOC entries: {len(toc_items)}")

HEAD = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(BOOK_TITLE)}</title>
<meta name="description" content="رسالة في صفات المرأة الصالحة وأثرها في الأسرة والمجتمع">
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
  <span><a href="#toc">الفهرس</a></span>
</nav>
"""

COVER = f"""
<section class="cover">
  <div class="eyebrow">سلسلة المراجع الشرعية · التربية والأخلاق</div>
  <div>
    <div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
    <h1>{esc(BOOK_TITLE)}</h1>
    <p class="subtitle">رسالة في معالم صلاح المرأة المسلمة، وأثرها في بيتها ومجتمعها</p>
  </div>
  <div class="divider-star">۞</div>
  <div class="credits">
    <div class="role">تأليف</div>
    <div class="name">{esc(BOOK_AUTHOR)}</div>
  </div>
  <div class="footer-line">الطبعة الأولى</div>
</section>

<section class="half-title">
  <div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
  <h1>{esc(BOOK_TITLE)}</h1>
  <div class="tagline">تأليف {esc(BOOK_AUTHOR)}</div>
</section>
"""

PUBLISHER = f"""
<section class="page frontmatter">
  <div class="page-pad">
    <h2>بيانات النشر</h2>
    <ul class="field-list">
      <li><span class="k">عنوان الكتاب</span><span class="v">{esc(BOOK_TITLE)}</span></li>
      <li><span class="k">المؤلف</span><span class="v">{esc(BOOK_AUTHOR)}</span></li>
      <li><span class="k">الطبعة</span><span class="v">الأولى</span></li>
      <li><span class="k">رقم الإيداع / ISBN</span><span class="v placeholder">يُستكمل من الناشر عند التسجيل الرسمي</span></li>
      <li><span class="k">سنة النشر</span><span class="v placeholder">يُستكمل من الناشر</span></li>
      <li><span class="k">جميع الحقوق محفوظة</span><span class="v">لا يجوز نسخ أي جزء من هذا الكتاب أو نقله بأي شكل من الأشكال إلا بإذن خطي من المؤلف، فيما عدا الاستشهاد العلمي بالإشارة إلى المصدر</span></li>
    </ul>
    <div class="small-note">
      عنوان الكتاب هذا مقترح مستخلص من موضوعه ومقدمته (وهو العبارة المتكررة في متنه)، إذ لم يرد في المخطوطة المزوَّدة عنوان صريح لها. كما لم يرد فيها اسم مؤلف؛ والاسم المثبت أعلاه ذُكر بطلب صاحب المخطوطة عند إعداد هذه النسخة.
    </div>
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

COLOPHON = f"""
<section class="colophon">
  <div class="bismillah">وَآخِرُ دَعْوَانَا أَنِ الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ</div>
  <h2>تم الكتاب بحمد الله</h2>
  <p>{esc(BOOK_TITLE)} — تأليف {esc(BOOK_AUTHOR)}</p>
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

full = HEAD + COVER + PUBLISHER + TOC_SECTION + body_html + COLOPHON + SCRIPT

import os
os.makedirs(OUT_DIR, exist_ok=True)
with open(f"{OUT_DIR}/index.html", "w", encoding="utf-8") as f:
    f.write(full)

print("wrote final HTML, total chars:", len(full))
