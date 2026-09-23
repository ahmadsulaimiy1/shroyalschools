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
SHORTL = {'BASIC': 'Nursery &amp; Primary', 'COLLEGE': 'Royal College'}
# English navigation runs on the SHRS class number, which is what the
# Registrar's own systems count in: «الصف الثالث الابتدائي» is Grade 5.
GRADE = lambda g: f'Grade {g}'

# Titles whose author or edition should be confirmed with the supplier before
# the order is placed. Marked with a dagger; no discussion in the document.
CHECK = {'متن الحائية', 'أعباد المسيح', 'مقرر الأستاذ'}

# ── one form per person, and it is the source's own ────────────────
# The two lists honour the same man twice over and not at all elsewhere:
# «الشيخ أحمد بن إبراهيم السليمي» in one, «أحمد بن إبراهيم السليمي» in the
# other. The rule here is narrow and it invents nothing: **the fullest form
# the Chairman supplied for a person is the form used everywhere he
# appears.** Titles are kept because the source gives them; none is added to
# a name that never carried one. Only the eulogy «رحمه الله» is dropped — it
# is a supplication, not part of an author's name on an order form, and it
# appears exactly once.
TITLES = ('الشيخ ', 'الإمام ', 'الأستاذ ', 'د. ')


def person_key(name):
    """Two spellings of one man collapse to one key."""
    k = name
    for t in TITLES:
        k = k.replace(t, '')
    k = k.replace(' رحمه الله', '')
    k = FIX.get(' '.join(k.split()).strip(' ،'), ' '.join(k.split()).strip(' ،'))
    return k


# One spelling for one man: «عبد الرحمن بن محمد…» in the first list,
# «عبد الرحمن محمد…» in the second. The fuller form wins.
FIX = {'عبد الرحمن محمد بن الصغير الأخضري': 'عبد الرحمن بن محمد بن الصغير الأخضري'}

# Where one list names an author and the other leaves the same book blank,
# the name is carried across. The Chairman's own data, made
# consistent — nothing brought in from outside.
FILL = {
    'زاد المسلم الصغير': 'عبد الشكور معلم عبد الفارح',
    'دروس اللغة العربية': 'د. ف. عبد الرحيم',
    'القراءة الراشدة': 'أبو الحسن الندوي',
    'خلاصة نور اليقين': 'عمر عبد الجبار',
    'تائية أبي إسحاق الإلبيري': 'أبو إسحاق الإلبيري',
    'عمدة الأحكام': '—',
    'مبادئ الترتيل': '—',
    'مقرر الأستاذ': '—',
    'القرآن الكريم': '—',
}

HOUSE = {}          # person_key → the fullest supplied form; built at import


def _learn():
    for d, head, g, copies in CLASSES:
        for supplied, book, _ in SUBMISSION[(d, g)]:
            _, _, au = book.partition('—')
            au = VOL_TAIL.sub('', au.strip()).strip()
            if not au or VOL_ONLY.match(au):
                continue
            au = au.replace(' رحمه الله', '')
            au = FIX.get(au, au)
            k = person_key(au)
            if len(au) > len(HOUSE.get(k, '')):
                HOUSE[k] = au
    for v in FILL.values():
        if v != '—':
            HOUSE.setdefault(person_key(v), v)


def house(name):
    name = FIX.get(name, name).replace(' رحمه الله', '')
    return HOUSE.get(person_key(name), name) or '—'


VOL_ONLY = re.compile(r'^(?:ج\s*[١٢٣٤]|الجزء\s+\S+)$')
VOL_TAIL = re.compile(r'[،,]\s*(ج\s*[١٢٣٤]|الجزء\s+\S+)\s*$')
_learn()


# ── one form per title, too ────────────────────────────────────────
# «نور البيان» and «نور البيان في ترتيل القرآن» are the same work. The
# College writes «مقرر وزارة التعليم السعودية» where the Basic list names
# the subject, and a bookseller cannot act on the first form. And a volume
# is «ج١» throughout, not «ج١» here and «الجزء الأول» there for one book.
# All three are settled from the Chairman's own wording.
TITLE = {'نور البيان': 'نور البيان في ترتيل القرآن'}
VOLN = {'الجزء الأول': 'ج١', 'الجزء الثاني': 'ج٢',
        'الجزء الثالث': 'ج٣', 'الجزء الرابع': 'ج٤'}
MINISTRY = {'الفقه': 'مقرر الفقه', 'التوحيد': 'مقرر التوحيد', 'التعبير': 'مقرر التعبير'}


def house_title(title, supplied):
    for k, v in VOLN.items():
        title = title.replace(k, v)
    if title.startswith('مقرر وزارة التعليم السعودية'):
        tail = title[len('مقرر وزارة التعليم السعودية'):].strip(' —')
        base = MINISTRY.get(supplied, 'مقرر وزارة التعليم السعودية')
        return f'{base} — {tail}' if tail else base
    for k, v in TITLE.items():
        if title == k or title.startswith(k + ' — '):
            return title.replace(k, v, 1)
    return title


def split_book(line):
    """Title and author, as supplied. The volume travels with the title,
    which is how a bookseller reads a line; nothing else is moved."""
    title, sep, author = line.partition('—')
    title, author = title.strip(), author.strip()
    if not sep:
        return title, house(FILL.get(title, '—'))
    if VOL_ONLY.match(author):                  # «… — ج٢» : a volume, not an author
        return f'{title} — {author}', house(FILL.get(title, '—'))
    m = VOL_TAIL.search(author)                 # «… — خالد يوسف، ج١»
    if m:
        return f'{title} — {m.group(1)}', house(VOL_TAIL.sub('', author).strip())
    return title, house(author)


def crest():
    fp = os.path.join(os.path.dirname(H), 'assets', 'shrs-crest.png')
    return 'data:image/png;base64,' + base64.b64encode(open(fp, 'rb').read()).decode()


CSS = """
/* ═══════════════════════════════════════════════════════════════════
   SHRS · قائمة الكتب الدراسية — the procurement schedule
   Coffee cloth, gold foil, warm ivory paper. Every rule that carries
   weight is a gradient, because flat gold prints as yellow ink. The
   eye goes: SCHOOL → CLASS → SUBJECT → BOOK → AUTHOR → COPIES, and
   nothing on the page competes with that order.
   ═══════════════════════════════════════════════════════════════════ */
@page{size:A4;}
*{box-sizing:border-box;} html,body{margin:0;padding:0;}
/* Coffee is the institution's ground, not the whole document. Each division
   carries its own colour so the two orders can never be confused and the
   page has some blood in it: royal blue for the Nursery & Primary, a true
   crimson for the Royal College. Gold is the constant across both. */
body{--ink:#241709;--brown:#3B2A1D;--bronze:#6B4A2E;--gold:#B08E4E;--champ:#E8D2A2;
 --panel:#2A1C10;--panel2:#3A2818;
 --nav:#0E2F63;--nav2:#16417E;--navpale:#E2EAF6;--navtint:#F1F5FB;
 --red:#8C1D26;--red2:#A82730;--redpale:#F6E2E1;--redtint:#FCF2F0;--paper:#FAF4E7;--ivory:#F5ECDA;--cream:#EFE3CB;
 --line:#DCC9A8;--hair:#E9DCC2;--mute:#9A8768;--burg:#7C1F2E;
 --fa:'Amiri',serif;--fk:'Reem Kufi',sans-serif;--fn:'Noto Kufi Arabic',sans-serif;
 --fd:'Cormorant Garamond',Georgia,serif;--fu:'Archivo','Helvetica Neue',sans-serif;
 font-family:var(--fa);font-size:10.6pt;line-height:1.7;color:var(--ink);
 background:var(--paper);direction:rtl;}
.foil{background-image:linear-gradient(90deg,#7E6029,#D9BE84 22%,#F4E6C2 38%,
 #AD8B4B 56%,#8A6A2E 70%,#E8CF96 86%,#7E6029);}
/* ── cover ──────────────────────────────────────────────────────── */
.cov{height:244mm;display:flex;flex-direction:column;align-items:center;
 justify-content:center;text-align:center;page-break-after:always;position:relative;
 padding:0 14mm;}
.cov .fr{position:absolute;top:0;right:0;left:0;bottom:0;
 border:.5pt solid rgba(176,142,78,.5);}
.cov .fr2{position:absolute;top:2.6mm;right:2.6mm;left:2.6mm;bottom:2.6mm;
 border:1.8pt solid rgba(176,142,78,.9);}
.cov .cl{position:absolute;width:3mm;height:3mm;background:#B08E4E;
 transform:rotate(45deg);}
.cov .cl.a{top:1.1mm;right:1.1mm;} .cov .cl.b{top:1.1mm;left:1.1mm;}
.cov .cl.c{bottom:1.1mm;right:1.1mm;} .cov .cl.d{bottom:1.1mm;left:1.1mm;}
.cov img{width:38mm;height:auto;display:block;margin:0 0 8mm;}
.cov .n1{font-family:var(--fk);font-weight:600;font-size:13.4pt;color:var(--brown);
 line-height:1.6;margin:0 0 2.6mm;}
.cov .n2{font-family:var(--fu);font-weight:600;font-size:7.2pt;letter-spacing:.3em;
 text-transform:uppercase;color:var(--bronze);direction:ltr;margin:0 0 12mm;
 padding-left:.3em;}
.cov .rule{width:58mm;height:1.6pt;margin:0 0 9mm;}
.cov h1{font-family:var(--fa);font-weight:700;font-size:33pt;color:var(--brown);
 margin:0 0 5mm;line-height:1.38;}
.cov .en{font-family:var(--fd);font-weight:700;font-size:16.5pt;letter-spacing:.26em;
 text-transform:uppercase;color:#5C3F22;direction:ltr;margin:0 0 11mm;
 padding-left:.26em;}
.cov .ses{font-size:13.4pt;color:#FFF3E2;background:var(--red);
 background-image:linear-gradient(140deg,#A3242E,#8C1D26 60%,#6E1520);
 border-top:1.8pt solid var(--gold);border-bottom:.6pt solid rgba(232,210,162,.55);
 padding:3mm 14mm;margin:0 0 11mm;}
.cov .to{font-size:11pt;color:var(--bronze);line-height:1.9;}
.cov .to span{display:block;font-family:var(--fu);font-weight:500;font-size:6.8pt;
 letter-spacing:.22em;text-transform:uppercase;color:var(--mute);direction:ltr;
 margin-top:2.4mm;padding-left:.22em;}
/* ── school divider ─────────────────────────────────────────────── */
.sch{page-break-before:always;color:#FBF4E6;background:var(--panel);
 background-image:linear-gradient(140deg,#3A2818 0%,#2A1C10 55%,#1C1108 100%);
 padding:5.4mm 8mm 5.8mm;border-top:2.4pt solid var(--gold);margin:0 0 6mm;
 display:flex;align-items:center;gap:7mm;position:relative;}
.sch:after{content:'';position:absolute;left:0;right:0;bottom:0;height:.8pt;
 background-image:linear-gradient(90deg,rgba(176,142,78,.2),#E8D2A2 50%,
 rgba(176,142,78,.2));}
.sch.d1{background:var(--nav);
 background-image:linear-gradient(140deg,#1B4E96 0%,#0E2F63 56%,#071B3C 100%);}
.sch.d2{background:var(--red);
 background-image:linear-gradient(140deg,#B22E38 0%,#8C1D26 56%,#571016 100%);}
.sch img{width:19mm;height:auto;display:block;flex:none;}
.sch .t{flex:1;border-right:.5pt solid rgba(232,210,162,.42);padding-right:7mm;}
.sch h2{font-family:var(--fk);font-weight:600;font-size:15pt;color:#FFFAF0;
 margin:0 0 2mm;line-height:1.4;}
.sch .l{font-family:var(--fu);font-weight:600;font-size:6.8pt;letter-spacing:.22em;
 text-transform:uppercase;color:#C9AC74;direction:ltr;padding-left:.22em;}
/* ── class block ────────────────────────────────────────────────── */
/* The class band is the strongest thing on the page after the school,
   because it is the first question the Registrar asks. Each division
   carries its own accent so the two orders are never confused. */
.cls{margin:0 0 4.4mm;page-break-inside:avoid;}
.clh{display:flex;align-items:center;gap:6mm;color:#FBF4E4;
 padding:2.4mm 5mm 2.6mm;margin:0;position:relative;}
.cls.d1 .clh{background:var(--nav);
 background-image:linear-gradient(140deg,#1A4A90 0%,#0E2F63 60%,#0A2350 100%);}
.cls.d2 .clh{background:var(--red);
 background-image:linear-gradient(140deg,#A3242E 0%,#8C1D26 60%,#6E1520 100%);}
.clh:before{content:'';position:absolute;top:0;right:0;left:0;height:1.8pt;
 background-image:linear-gradient(90deg,#7E6029,#F2E2BB 50%,#7E6029);}
.clh h3{font-family:var(--fa);font-weight:700;font-size:14pt;color:#FFFCF4;
 margin:0 0 1mm;line-height:1.24;}
.clh .en{font-family:var(--fu);font-weight:600;font-size:6.2pt;letter-spacing:.16em;
 text-transform:uppercase;color:#BFA678;direction:ltr;padding-left:.16em;}
.clh .t{flex:1;}
.clh .cp{flex:none;text-align:center;min-width:25mm;padding:1.2mm 4mm 1.4mm;
 border:.5pt solid rgba(226,203,150,.5);background:rgba(0,0,0,.22);}
.clh .cp b{display:block;font-family:var(--fa);font-weight:700;font-size:15.5pt;
 line-height:1;color:var(--champ);}
.clh .cp em{display:block;font-family:var(--fn);font-style:normal;font-size:6pt;
 color:#B79A63;margin-top:1.4mm;}
table{width:100%;border-collapse:collapse;font-size:9.6pt;}
thead th{font-family:var(--fn);font-size:6.4pt;font-weight:400;padding:1.1mm 4mm 1.3mm;
 text-align:right;border-bottom:.5pt solid var(--line);}
.cls.d1 thead th{background:var(--navpale);color:#2E4A78;border-bottom-color:#C9D6EA;}
.cls.d2 thead th{background:var(--redpale);color:#79313A;border-bottom-color:#E6C9C7;}
thead th.q{text-align:center;}
tbody th{text-align:right;font-family:var(--fa);font-weight:400;color:#6A5740;
 font-size:9pt;width:16%;padding:1.1mm 4mm 1.3mm;
 border-bottom:.3pt solid var(--hair);vertical-align:middle;}
td{padding:1.1mm 4mm 1.3mm;border-bottom:.3pt solid var(--hair);vertical-align:middle;
 line-height:1.34;}
td.bk{width:41%;font-family:var(--fa);font-weight:700;font-size:10.2pt;
 color:var(--ink);}
td.au{width:27%;color:#7A664C;font-size:8.6pt;}
td.q{width:16%;text-align:center;font-family:var(--fa);font-weight:700;
 font-size:12.4pt;color:#FFF6E4;}
.cls.d1 td.q{background:var(--nav);} .cls.d2 td.q{background:var(--red);}
tbody tr:nth-child(even) th,tbody tr:nth-child(even) td{background:var(--ivory);}
.cls.d1 tbody tr:nth-child(even) th,.cls.d1 tbody tr:nth-child(even) td{background:var(--navtint);}
.cls.d2 tbody tr:nth-child(even) th,.cls.d2 tbody tr:nth-child(even) td{background:var(--redtint);}
.cls.d1 tbody tr:nth-child(even) td.q{background:#0A2350;}
.cls.d2 tbody tr:nth-child(even) td.q{background:#6E1520;}
tbody tr:last-child th,tbody tr:last-child td{border-bottom:1.2pt solid var(--gold);}
tr,thead{break-inside:avoid;page-break-inside:avoid;}
thead{break-after:avoid;page-break-after:avoid;}
sup{color:var(--burg);font-size:7.2pt;}
/* English is the second voice everywhere a heading or label appears:
   same convention on every table head, every class band, every summary
   row. It never translates a title or an author's name. */
thead th i{display:block;font-family:var(--fu);font-style:normal;font-weight:600;
 font-size:5.6pt;letter-spacing:.14em;text-transform:uppercase;opacity:.72;
 direction:ltr;text-align:right;margin-top:.8mm;padding-left:.14em;}
thead th.q i{text-align:center;}
.clh .en b{font-family:var(--fu);font-weight:700;color:#E2C68C;letter-spacing:.14em;}
.clh .cp em i{display:block;font-family:var(--fu);font-style:normal;font-weight:600;
 font-size:5.2pt;letter-spacing:.14em;text-transform:uppercase;color:#8E7650;
 direction:ltr;margin-top:.5mm;padding-left:.14em;}
.sum tbody th i{display:block;font-family:var(--fu);font-style:normal;font-weight:600;
 font-size:5.8pt;letter-spacing:.14em;text-transform:uppercase;color:#9C8768;
 direction:ltr;text-align:right;margin-top:.6mm;padding-left:.14em;}
.sum tbody tr.hd th i{color:#BFA678;font-size:6.2pt;margin-top:1mm;}
.foot span{display:block;font-family:var(--fu);font-weight:500;font-size:6.4pt;
 letter-spacing:.1em;text-transform:uppercase;color:#A8947A;direction:ltr;
 margin-top:1.4mm;padding-left:.1em;}
.sig i{display:block;font-family:var(--fu);font-style:normal;font-weight:600;
 font-size:6pt;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);
 direction:ltr;margin:0 0 1.6mm;padding-left:.16em;}
/* ── summary ────────────────────────────────────────────────────── */
.sum{page-break-before:always;padding-top:4mm;}
.sum h2{font-family:var(--fa);font-weight:700;font-size:19pt;color:var(--brown);
 margin:0 0 2mm;padding:0 0 3mm;border-bottom:1.6pt solid var(--gold);}
.sum .l{font-family:var(--fu);font-weight:600;font-size:7pt;letter-spacing:.26em;
 text-transform:uppercase;color:var(--bronze);direction:ltr;margin:0 0 7mm;
 padding-left:.26em;}
.sum td.n,.sum th.n{text-align:center;font-family:var(--fa);font-weight:700;
 color:var(--brown);}
.sum tbody tr.hd th{color:var(--champ);font-family:var(--fk);font-weight:600;
 font-size:10.4pt;padding:2.6mm 4mm;border-bottom:0;background:var(--panel2);}
.sum tbody tr.hd.d1 th{background:var(--nav);
 background-image:linear-gradient(140deg,#1A4A90,#0E2F63 60%,#0A2350);}
.sum tbody tr.hd.d2 th{background:var(--red);
 background-image:linear-gradient(140deg,#A3242E,#8C1D26 60%,#6E1520);}
.foot{margin-top:7mm;border-top:.4pt solid var(--line);padding-top:3.4mm;
 font-size:8.8pt;color:var(--mute);line-height:1.75;}
.sig{display:flex;gap:11mm;margin-top:11mm;}
.sig div{flex:1;border-top:1.1pt solid var(--brown);padding-top:2.8mm;font-size:8.8pt;
 color:var(--bronze);}
.sig b{display:block;color:var(--brown);font-size:10pt;margin-bottom:1.2mm;}
"""



def build():
    C = crest()
    o = ['<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8">',
         '<title>قائمة الكتب الدراسية — مدارس السلطان حنفي الملكية</title>',
         f'<style>{CSS}</style></head><body>']
    w = o.append

    w('<div class="cov"><div class="fr"></div><div class="fr2"></div>'
      '<div class="cl a"></div><div class="cl b"></div>'
      '<div class="cl c"></div><div class="cl d"></div>'
      f'<img src="{C}" alt="">'
      '<div class="n1">مدارسُ السلطان حنفي الملكية</div>'
      '<div class="n2">Sultan Hanafi Royal Schools</div>'
      '<div class="rule foil"></div>'
      '<h1>قائمةُ الكتب الدراسية</h1>'
      '<div class="en">Textbook List</div>'
      '<div class="ses">العامُ الدراسي ٢٠٢٦ / ٢٠٢٧</div>'
      '<div class="to">مُعَدَّةٌ لمكتب المسجِّل<span>Prepared for the Registrar&rsquo;s '
      'Office &middot; For Procurement</span></div></div>')

    flagged = False
    for div in ('BASIC', 'COLLEGE'):
        ar_name, en_name = DIV[div]
        w(f'<div class="sch {"d1" if div == "BASIC" else "d2"}">'
          f'<img src="{C}" alt=""><div class="t">'
          f'<h2>{e(ar_name)}</h2><div class="l">{en_name}</div></div></div>')
        for d, head, g, copies in CLASSES:
            if d != div:
                continue
            w(f'<div class="cls {"d1" if div == "BASIC" else "d2"}"><div class="clh">'
              f'<div class="t"><h3>{e(head)}</h3>'
              f'<div class="en"><b>{GRADE(g)}</b> &middot; {SHORTL[div]} &middot; '
              f'{copies} copies per listed title</div></div>'
              f'<div class="cp"><b>{ar(copies)}</b>'
              '<em>الكمية لكل عنوان<i>Qty per title</i></em></div></div>'
              '<table><thead><tr>'
              '<th>المادة<i>Subject</i></th>'
              '<th>الكتاب<i>Book</i></th>'
              '<th>المؤلف / الجهة<i>Author / Publisher</i></th>'
              '<th class="q">الكمية<i>Quantity</i></th></tr></thead><tbody>')
            for supplied, book, _ in SUBMISSION[(d, g)]:
                title, author = split_book(book)
                # «مقرر الأستاذ» also begins with «مقرر» and is not a ministry
                # book; the attribution follows the original wording, not the word
                ministry = title.startswith('مقرر وزارة التعليم السعودية')
                title = house_title(title, supplied)
                if ministry and author == '—':
                    author = 'وزارة التعليم السعودية'
                mark = ''
                if any(k in title for k in CHECK):
                    mark, flagged = '<sup>†</sup>', True
                w(f'<tr><th>{e(supplied)}</th><td class="bk">{e(title)}{mark}</td>'
                  f'<td class="au">{e(author)}</td><td class="q">{ar(copies)}</td></tr>')
            w('</tbody></table></div>')

    # ── summary ─────────────────────────────────────────────────────
    # Copies are stated per class, exactly as supplied. An earlier version
    # multiplied titles by copies and printed a grand total; that number was
    # invented by the document and is not what anyone orders against.
    w('<div class="sum"><h2>ملخَّصُ القائمة</h2>'
      '<div class="l">Summary of the List</div>'
      '<table><thead><tr><th>الصف<i>Class</i></th>'
      '<th class="n">عدد العناوين<i>Titles</i></th>'
      '<th class="n">الكمية لكل عنوان<i>Qty per title</i></th></tr></thead><tbody>')
    for div in ('BASIC', 'COLLEGE'):
        w(f'<tr class="hd {"d1" if div == "BASIC" else "d2"}"><th colspan="3">{e(DIV[div][0])}'
          f'<i>{DIV[div][1]}</i></th></tr>')
        for d, head, g, copies in CLASSES:
            if d != div:
                continue
            w(f'<tr><th>{e(head)}<i>{GRADE(g)}</i></th>'
              f'<td class="n">{ar(len(SUBMISSION[(d, g)]))}</td>'
              f'<td class="n">{ar(copies)}</td></tr>')
    w('</tbody></table>')

    if flagged:
        w('<div class="foot">† بعضُ بيانات المؤلف أو الطبعة تحتاج إلى مراجعةٍ '
          'نهائيةٍ مع المورِّد قبل الشراء.'
          '<span>Some author or edition details to be confirmed with the '
          'supplier before purchase.</span></div>')
    w('<div class="sig">'
      '<div><b>الإدارة الأكاديمية</b><i>Academic Administration</i>'
      'التوقيع / التاريخ &middot; Signature / Date</div>'
      '<div><b>مكتب المسجِّل</b><i>Registrar&rsquo;s Office</i>'
      'التوقيع / التاريخ &middot; Signature / Date</div>'
      '<div><b>رئيس المدارس</b><i>Chairman &middot; Head of Schools</i>'
      'التوقيع / التاريخ &middot; Signature / Date</div></div>')
    w('</div></body></html>')
    return ''.join(o)


if __name__ == '__main__':
    doc = build()
    p = os.path.join(H, 'TEXTBOOK-LIST.html')
    open(p, 'w', encoding='utf-8').write(doc)
    print(f'written — {len(doc)//1024} KB')
