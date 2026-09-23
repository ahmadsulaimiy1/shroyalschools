# -*- coding: utf-8 -*-
"""SULTAN HANAFI ROYAL SCHOOLS · قائمة الكتب الدراسية — TEXTBOOK LIST

A procurement schedule for the Registrar's Office. School → class →
subject → book → author → copies, and nothing else.

The book information is taken from `submission.py`, which holds the two
lists exactly as they were received. Subject labels, titles, authors and
volume numbers are reproduced as supplied. Nothing is reclassified,
renamed or corrected here; where an attribution genuinely needs checking
before purchase the title carries a dagger and one discreet line says so.
"""
import base64
import html
import os
import re
import sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
from submission import CLASSES, SUBMISSION                          # noqa: E402

e = lambda s: html.escape(str(s))
AR = '٠١٢٣٤٥٦٧٨٩'
ar = lambda n: ''.join(AR[int(c)] for c in str(n))

DIV = {'BASIC': ('مدارس السلطان حنفي للحضانة والابتدائية',
                 'Sultan Hanafi Nursery &amp; Primary School'),
       'COLLEGE': ('كلية السلطان حنفي الملكية',
                   'Sultan Hanafi Royal College')}
SHORT = {'BASIC': 'الحضانة والابتدائية', 'COLLEGE': 'الكلية الملكية'}

# Titles whose author or edition should be confirmed with the supplier before
# the order is placed. Marked with a dagger; no discussion in the document.
CHECK = {'متن الحائية', 'أعباد المسيح', 'مقرر الأستاذ', 'متن الأخضري'}

VOL_ONLY = re.compile(r'^(?:ج\s*[١٢٣٤]|الجزء\s+\S+)$')
VOL_TAIL = re.compile(r'[،,]\s*(ج\s*[١٢٣٤]|الجزء\s+\S+)\s*$')


def split_book(line):
    """Title and author, as supplied. The volume travels with the title,
    which is how a bookseller reads a line; nothing else is moved."""
    title, sep, author = line.partition('—')
    title, author = title.strip(), author.strip()
    if not sep:
        return title, '—'
    if VOL_ONLY.match(author):                  # «… — ج٢» : a volume, not an author
        return f'{title} — {author}', '—'
    m = VOL_TAIL.search(author)                 # «… — خالد يوسف، ج١»
    if m:
        return f'{title} — {m.group(1)}', VOL_TAIL.sub('', author).strip()
    return title, author


def crest():
    fp = os.path.join(os.path.dirname(H), 'assets', 'shrs-crest.png')
    return 'data:image/png;base64,' + base64.b64encode(open(fp, 'rb').read()).decode()


CSS = """
@page{size:A4;}
*{box-sizing:border-box;} html,body{margin:0;padding:0;}
body{--ink:#26190E;--brown:#3B2A1D;--bronze:#6B4A2E;--gold:#B08E4E;--champ:#E4C98A;
 --panel:#2A1C10;--paper:#FBF6EC;--ivory:#F6EFE1;--cream:#F0E5D0;--line:#DFCFB3;
 --hair:#EBE0CB;--mute:#9C8B74;--burg:#7C1F2E;
 --fa:'Amiri',serif;--fk:'Reem Kufi',sans-serif;--fn:'Noto Kufi Arabic',sans-serif;
 --fd:'Cormorant Garamond',Georgia,serif;--fu:'Archivo','Helvetica Neue',sans-serif;
 font-family:var(--fa);font-size:10.4pt;line-height:1.7;color:var(--ink);
 background:var(--paper);direction:rtl;}
/* ── cover ──────────────────────────────────────────────────────── */
.cov{height:243mm;display:flex;flex-direction:column;align-items:center;
 justify-content:center;text-align:center;page-break-after:always;position:relative;}
.cov:before,.cov:after{content:'';position:absolute;left:0;right:0;height:1.6pt;
 background-image:linear-gradient(90deg,#7E6029,#F2E2BB 50%,#7E6029);}
.cov:before{top:0;} .cov:after{bottom:0;}
.cov img{width:36mm;height:auto;display:block;margin:0 0 9mm;}
.cov .n1{font-family:var(--fk);font-weight:600;font-size:13pt;color:var(--brown);
 line-height:1.6;margin:0 0 2.4mm;}
.cov .n2{font-family:var(--fu);font-weight:600;font-size:7.4pt;letter-spacing:.28em;
 text-transform:uppercase;color:var(--bronze);direction:ltr;margin:0 0 13mm;
 padding-left:.28em;}
.cov .rule{width:52mm;height:1pt;margin:0 0 9mm;
 background-image:linear-gradient(90deg,#7E6029,#F2E2BB 50%,#7E6029);}
.cov h1{font-family:var(--fa);font-weight:700;font-size:31pt;color:var(--brown);
 margin:0 0 5mm;line-height:1.4;}
.cov .en{font-family:var(--fd);font-weight:700;font-size:16pt;letter-spacing:.24em;
 text-transform:uppercase;color:#6B4A2E;direction:ltr;margin:0 0 11mm;
 padding-left:.24em;}
.cov .ses{font-size:13pt;color:var(--brown);border-top:.9pt solid var(--gold);
 border-bottom:.9pt solid var(--gold);padding:2.4mm 11mm;margin:0 0 11mm;}
.cov .to{font-size:10.6pt;color:var(--bronze);line-height:1.8;}
.cov .to span{display:block;font-family:var(--fu);font-weight:500;font-size:7pt;
 letter-spacing:.2em;text-transform:uppercase;color:var(--mute);direction:ltr;
 margin-top:2mm;padding-left:.2em;}
/* ── school heading ─────────────────────────────────────────────── */
.sch{page-break-before:always;background:var(--panel);color:#F4EBD8;
 padding:4.2mm 7mm 4.6mm;border-top:2pt solid var(--gold);margin:0 0 5.6mm;
 display:flex;align-items:center;gap:6mm;}
.sch img{width:16mm;height:auto;display:block;flex:none;}
.sch .t{flex:1;border-right:.5pt solid rgba(226,203,150,.4);padding-right:6mm;}
.sch h2{font-family:var(--fk);font-weight:600;font-size:14pt;color:#FFFAF0;
 margin:0 0 1.6mm;line-height:1.4;}
.sch .l{font-family:var(--fu);font-weight:600;font-size:6.6pt;letter-spacing:.2em;
 text-transform:uppercase;color:#C2A36A;direction:ltr;padding-left:.2em;}
/* ── class block ────────────────────────────────────────────────── */
.cls{margin:0 0 5.4mm;page-break-inside:avoid;}
.clh{display:flex;align-items:baseline;gap:5mm;border-bottom:1.2pt solid var(--gold);
 padding:0 0 1.8mm;margin:0 0 2.4mm;}
.clh h3{font-family:var(--fa);font-weight:700;font-size:13pt;color:var(--brown);margin:0;}
.clh .cp{margin-right:auto;font-family:var(--fn);font-size:8pt;color:#fff;
 background:var(--bronze);padding:.8mm 3.4mm;white-space:nowrap;}
table{width:100%;border-collapse:collapse;font-size:9.2pt;}
thead th{font-family:var(--fn);font-size:6.8pt;font-weight:400;color:var(--bronze);
 padding:1.4mm 3mm;text-align:right;border-bottom:.5pt solid var(--line);
 background:var(--ivory);}
thead th:last-child{text-align:center;}
tbody th{text-align:right;font-family:var(--fa);font-weight:700;color:var(--brown);
 width:19%;padding:1.45mm 3mm 1.75mm;border-bottom:.3pt solid var(--hair);
 vertical-align:top;}
td{padding:1.45mm 3mm 1.75mm;border-bottom:.3pt solid var(--hair);vertical-align:top;
 color:#3A2C1D;line-height:1.45;}
td.bk{width:40%;} td.au{width:29%;color:#5E4C36;font-size:9pt;}
td.cp{width:12%;text-align:center;font-family:var(--fa);font-weight:700;
 font-size:11pt;color:var(--brown);}
tbody tr:nth-child(even) th,tbody tr:nth-child(even) td{background:var(--ivory);}
tbody tr:last-child th,tbody tr:last-child td{border-bottom:.8pt solid var(--brown);}
tr,thead{break-inside:avoid;page-break-inside:avoid;}
thead{break-after:avoid;page-break-after:avoid;}
sup{color:var(--burg);font-size:7pt;}
/* ── summary ────────────────────────────────────────────────────── */
.sum{page-break-before:always;padding-top:4mm;}
.sum h2{font-family:var(--fa);font-weight:700;font-size:17pt;color:var(--brown);
 margin:0 0 1.6mm;padding:0 0 2.6mm;border-bottom:1.2pt solid var(--gold);}
.sum .l{font-family:var(--fu);font-weight:600;font-size:7pt;letter-spacing:.24em;
 text-transform:uppercase;color:var(--bronze);direction:ltr;margin:0 0 6mm;
 padding-left:.24em;}
.sum td.n,.sum th.n{text-align:center;font-family:var(--fa);font-weight:700;
 color:var(--brown);}
.sum tbody tr.tot th,.sum tbody tr.tot td{background:var(--panel);color:var(--champ);
 border-bottom:0;font-size:10.4pt;padding:2.4mm 3mm;}
.sum tbody tr.tot td{color:#FFFAF0;font-size:15pt;}
.grand{margin-top:6mm;border-top:2pt solid var(--gold);padding:4.4mm 0 0;
 display:flex;align-items:baseline;gap:6mm;}
.grand .k{font-family:var(--fa);font-size:12.4pt;color:var(--brown);}
.grand .v{margin-right:auto;font-family:var(--fa);font-weight:700;font-size:26pt;
 color:var(--brown);line-height:1;}
.grand .e{font-family:var(--fu);font-weight:600;font-size:6.8pt;letter-spacing:.2em;
 text-transform:uppercase;color:var(--mute);direction:ltr;}
.foot{margin-top:6mm;border-top:.4pt solid var(--line);padding-top:3mm;
 font-size:8.6pt;color:var(--mute);line-height:1.75;}
.sig{display:flex;gap:11mm;margin-top:9mm;}
.sig div{flex:1;border-top:.9pt solid var(--brown);padding-top:2.4mm;font-size:8.6pt;
 color:var(--bronze);}
.sig b{display:block;color:var(--brown);font-size:9.8pt;margin-bottom:1mm;}
"""


def build():
    C = crest()
    o = ['<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8">',
         '<title>قائمة الكتب الدراسية — مدارس السلطان حنفي الملكية</title>',
         f'<style>{CSS}</style></head><body>']
    w = o.append

    w(f'<div class="cov"><img src="{C}" alt="">'
      '<div class="n1">مدارسُ السلطان حنفي الملكية</div>'
      '<div class="n2">Sultan Hanafi Royal Schools</div>'
      '<div class="rule"></div>'
      '<h1>قائمةُ الكتب الدراسية</h1>'
      '<div class="en">Textbook List</div>'
      '<div class="ses">العامُ الدراسي ٢٠٢٦ / ٢٠٢٧</div>'
      '<div class="to">مُعَدَّةٌ لمكتب المسجِّل<span>Prepared for the Registrar&rsquo;s '
      'Office &middot; For Procurement</span></div></div>')

    flagged = False
    for div in ('BASIC', 'COLLEGE'):
        ar_name, en_name = DIV[div]
        w(f'<div class="sch"><img src="{C}" alt=""><div class="t">'
          f'<h2>{e(ar_name)}</h2><div class="l">{en_name}</div></div></div>')
        for d, head, g, copies in CLASSES:
            if d != div:
                continue
            w('<div class="cls"><div class="clh">'
              f'<h3>{e(head)}</h3>'
              f'<span class="cp">{ar(copies)} نسخة</span></div>'
              '<table><thead><tr><th>المادة</th><th>الكتاب</th>'
              '<th>المؤلف / الجهة</th><th>النسخ</th></tr></thead><tbody>')
            for supplied, book, _ in SUBMISSION[(d, g)]:
                title, author = split_book(book)
                mark = ''
                if any(k in title for k in CHECK):
                    mark, flagged = '<sup>†</sup>', True
                w(f'<tr><th>{e(supplied)}</th><td class="bk">{e(title)}{mark}</td>'
                  f'<td class="au">{e(author)}</td><td class="cp">{ar(copies)}</td></tr>')
            w('</tbody></table></div>')

    # ── procurement summary ─────────────────────────────────────────
    w('<div class="sum"><h2>ملخَّصُ احتياجات الكتب</h2>'
      '<div class="l">Procurement Summary</div>'
      '<table><thead><tr><th>المدرسة</th><th>الصف</th>'
      '<th class="n">عدد العناوين</th><th class="n">النسخ لكل عنوان</th>'
      '<th class="n">إجمالي النسخ</th></tr></thead><tbody>')
    grand = 0
    for div in ('BASIC', 'COLLEGE'):
        sub = 0
        for d, head, g, copies in CLASSES:
            if d != div:
                continue
            n = len(SUBMISSION[(d, g)])
            tot = n * copies
            sub += tot
            w(f'<tr><th>{e(SHORT[div])}</th>'
              f'<td>{e(head)}</td><td class="n">{ar(n)}</td>'
              f'<td class="n">{ar(copies)}</td><td class="n">{ar(tot)}</td></tr>')
        grand += sub
        w(f'<tr class="tot"><th colspan="4">مجموعُ {e(DIV[div][0])}</th>'
          f'<td class="n">{ar(sub)}</td></tr>')
    w('</tbody></table>')
    w(f'<div class="grand"><span class="k">إجماليُّ النسخ المطلوبة</span>'
      f'<span class="v">{ar(grand)}</span>'
      '<span class="e">Total copies required</span></div>')

    if flagged:
        w('<div class="foot">† بعضُ بيانات المؤلف أو الطبعة تحتاج إلى مراجعةٍ '
          'نهائيةٍ مع المورِّد قبل الشراء.</div>')
    w('<div class="sig"><div><b>الإدارة الأكاديمية</b>التوقيع / التاريخ</div>'
      '<div><b>مكتب المسجِّل</b>التوقيع / التاريخ</div>'
      '<div><b>المدير العام</b>التوقيع / التاريخ</div></div>')
    w('</div></body></html>')
    return ''.join(o)


if __name__ == '__main__':
    doc = build()
    p = os.path.join(H, 'TEXTBOOK-LIST.html')
    open(p, 'w', encoding='utf-8').write(doc)
    print(f'written — {len(doc)//1024} KB')
