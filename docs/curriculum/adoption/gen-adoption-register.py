# -*- coding: utf-8 -*-
"""SULTAN HANAFI ROYAL SCHOOLS · سجل الاعتماد المؤقت للكتب الدراسية

A Registrar-facing document, generated — never hand-edited. Its content
comes from submission.py (the lists as received) and reconcile.py (the
Board's mapping, tested against the curriculum register). Its design is
the house system already locked at D-01 … D-18.

It settles nothing. It records what may be ordered now, what is carried
by a host book, and what must be decided before حصص are fixed.
"""
import os, sys, html
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import reconcile as R                                              # noqa: E402

e = lambda s: html.escape(str(s))
AR = '٠١٢٣٤٥٦٧٨٩'
ar = lambda n: ''.join(AR[int(c)] for c in str(n))
NAMES = {1: 'الأول', 2: 'الثاني', 3: 'الثالث', 4: 'الرابع', 5: 'الخامس', 6: 'السادس',
         7: 'السابع', 8: 'الثامن', 9: 'التاسع', 10: 'العاشر', 11: 'الحادي عشر',
         12: 'الثاني عشر'}
DIVN = {'BASIC': 'مدارس السلطان حنفي للحضانة والابتدائية',
        'COLLEGE': 'كلية السلطان حنفي الملكية'}
DIVL = {'BASIC': 'Sultan Hanafi Nursery &amp; Primary School',
        'COLLEGE': 'Sultan Hanafi Royal College'}
PCLS = {'القرآن': 'p1', 'اللغة': 'p2', 'الإسلامية': 'p3', 'التتويج': 'p4', '—': 'p0'}
PNAME = {'القرآن': 'القرآن وعلومه', 'اللغة': 'اللغة وعلومها',
         'الإسلامية': 'الدراسات الإسلامية', 'التتويج': 'خدمة سنة التخرج', '—': '—'}

CSS = """
@page{size:A4;}
*{box-sizing:border-box;} html,body{margin:0;padding:0;}
body{--ink:#241A11;--brown:#3B2A1D;--bronze:#6B4A2E;--gold:#B08E4E;--gold2:#C6A15B;
 --champ:#E4C98A;--panel:#2A1C10;--paper:#FDFBF6;--paper2:#FAF5EB;--ivory:#FAF4E9;
 --cream:#F3E7D2;--parch:#EBDDC2;--line:#E0D2B8;--hair:#EDE3D1;--mute:#9A8A76;
 --green:#0F3F38;--greentint:#EAF2EE;--blue:#082A66;--bluetint:#EDF2F9;
 --ox:#5E1B26;--oxtint:#F8EDEB;--char:#3A342C;--chartint:#F3F1EA;--burg:#7C1F2E;
 --fa:'Amiri',serif;--fk:'Reem Kufi',sans-serif;--fn:'Noto Kufi Arabic',sans-serif;
 --fl:'EB Garamond',Georgia,serif;--fd:'Cormorant Garamond',Georgia,serif;
 --fu:'Archivo','Helvetica Neue',sans-serif;
 font-family:var(--fa);font-size:10pt;line-height:1.75;color:var(--ink);
 background:var(--paper);direction:rtl;}
h1,h2,h3,h4{font-family:var(--fa);font-weight:700;letter-spacing:0;}
p{margin:0 0 4mm;}
.lat{font-family:var(--fu);font-weight:600;font-size:6.6pt;letter-spacing:.14em;
 text-transform:uppercase;color:var(--bronze);direction:ltr;}
/* ── masthead ───────────────────────────────────────────────────── */
.mast{border-top:2.4pt solid var(--gold);border-bottom:.5pt solid var(--line);
 padding:6mm 0 5mm;margin:0 0 7mm;text-align:center;
 background:linear-gradient(180deg,var(--paper2),var(--paper));}
.mast .l1{font-family:var(--fu);font-weight:600;font-size:7.4pt;letter-spacing:.26em;
 text-transform:uppercase;color:var(--bronze);direction:ltr;margin:0 0 3mm;}
.mast h1{font-size:21pt;color:var(--brown);margin:0 0 3mm;line-height:1.4;}
.mast .div{display:flex;align-items:center;justify-content:center;margin:0 0 3.4mm;}
.mast .div:before,.mast .div:after{content:'';width:24mm;height:.4pt;background:var(--line);}
.mast .div i{width:2.2mm;height:2.2mm;margin:0 3mm;display:block;transform:rotate(45deg);
 background-image:linear-gradient(135deg,#F2E2BB,#8A6A2E);}
.mast .l2{font-family:var(--fd);font-weight:600;font-size:12.6pt;letter-spacing:.2em;
 text-transform:uppercase;color:var(--brown);direction:ltr;margin:0 0 3mm;}
.mast .ses{display:inline-block;font-size:9.4pt;color:var(--brown);
 border-top:.9pt solid var(--gold);border-bottom:.9pt solid var(--gold);padding:1.6mm 7mm;}
.docid{display:flex;gap:5mm;border-top:1.3pt solid var(--gold);
 border-bottom:.35pt solid var(--line);padding:2.6mm 0 3mm;margin:0 0 6mm;
 font-size:8.6pt;color:var(--bronze);align-items:baseline;}
.docid b{color:var(--brown);font-weight:700;}
.docid .st{margin-right:auto;color:var(--burg);}
/* ── sections ───────────────────────────────────────────────────── */
h2{font-size:13.4pt;color:var(--brown);margin:9mm 0 4mm;padding:0 0 2.6mm;
 border-bottom:.5pt solid var(--line);position:relative;page-break-after:avoid;}
h2:after{content:'';position:absolute;bottom:-.5pt;right:0;width:22mm;height:1.4pt;
 background:var(--gold);}
h2 .rn{font-family:var(--fd);font-size:11pt;color:var(--gold);direction:ltr;
 margin-left:3.4mm;}
h3{font-size:11pt;color:var(--brown);margin:6mm 0 3mm;page-break-after:avoid;}
.lead{font-size:9.8pt;line-height:1.9;color:#3F2E20;margin:0 0 5mm;}
.note{border-right:1.4pt solid var(--gold);background:var(--paper2);padding:3mm 5mm 3.6mm;
 font-size:9.2pt;line-height:1.8;margin:0 0 5mm;}
.warn{border-right:1.4pt solid var(--burg);background:#FAF4F2;}
.warn b{color:var(--burg);}
/* ── tables ─────────────────────────────────────────────────────── */
table{width:100%;border-collapse:collapse;font-size:8.4pt;margin:0 0 5mm;}
thead th{font-family:var(--fn);font-size:6.8pt;font-weight:400;letter-spacing:0;
 color:var(--champ);background:var(--panel);padding:2.2mm 2.4mm;text-align:right;
 border-top:1.4pt solid var(--gold);}
tbody th{text-align:right;font-family:var(--fa);font-weight:700;color:var(--brown);
 padding:1.6mm 2.4mm 2mm;border-bottom:.3pt solid var(--hair);vertical-align:top;}
td{padding:1.6mm 2.4mm 2mm;border-bottom:.3pt solid var(--hair);vertical-align:top;
 color:#3F3225;line-height:1.55;}
tbody tr:nth-child(even) th,tbody tr:nth-child(even) td{background:var(--ivory);}
tbody tr:last-child th,tbody tr:last-child td{border-bottom:.8pt solid var(--brown);}
tr,thead{break-inside:avoid;page-break-inside:avoid;}
thead{break-after:avoid;page-break-after:avoid;}
td.c{text-align:center;} td.n{font-family:var(--fa);text-align:center;color:var(--brown);}
.pg{display:inline-block;font-family:var(--fn);font-size:6.4pt;padding:.5mm 2.2mm;
 color:#fff;white-space:nowrap;}
.pg.p1{background:var(--green);} .pg.p2{background:var(--blue);}
.pg.p3{background:var(--ox);} .pg.p4{background:var(--char);}
.pg.p0{background:var(--mute);}
.st-ind{color:var(--green);font-family:var(--fn);font-size:7pt;}
.st-emb{color:var(--bronze);font-family:var(--fn);font-size:7pt;}
.st-ask{color:var(--burg);font-family:var(--fn);font-size:7pt;font-weight:700;}
.sup{color:var(--mute);font-size:7.6pt;}
.brk{page-break-before:always;}
/* ── decisions ──────────────────────────────────────────────────── */
.bd{border-top:1.1pt solid var(--gold);background:var(--paper2);padding:3mm 4.4mm 3.6mm;
 margin:0 0 3.4mm;page-break-inside:avoid;}
.bd .id{font-family:var(--fu);font-weight:700;font-size:7pt;letter-spacing:.14em;
 color:var(--gold);direction:ltr;margin:0 0 1.4mm;}
.bd h4{font-size:10.2pt;color:var(--brown);margin:0 0 1.8mm;}
.bd p{font-size:8.8pt;line-height:1.72;margin:0 0 1.8mm;color:#3F3225;}
.bd .out{font-family:var(--fn);font-size:7.4pt;color:var(--burg);border-top:.35pt solid var(--hair);
 padding-top:1.8mm;}
.bd.ok{background:var(--greentint);} .bd.ok .out{color:var(--green);}
/* ── signature ──────────────────────────────────────────────────── */
.sig{display:flex;gap:10mm;margin-top:10mm;page-break-inside:avoid;}
.sig div{flex:1;border-top:.9pt solid var(--brown);padding-top:2.4mm;font-size:8.6pt;
 color:var(--bronze);}
.sig b{display:block;color:var(--brown);font-size:9.6pt;margin-bottom:1.2mm;}
"""


def table(head, body, cls=''):
    h = ''.join(f'<th>{e(x)}</th>' for x in head)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>'


def stat(d):
    k = 'st-ask' if 'قرار' in d else ('st-ind' if 'مستقلة' in d else 'st-emb')
    return f'<span class="{k}">{e(d)}</span>'


def build():
    rs = R.rows()
    real, carried = R.gaps(rs)
    o = ['<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8">',
         '<title>سجل الاعتماد المؤقت للكتب الدراسية — مدارس السلطان حنفي الملكية</title>',
         f'<style>{CSS}</style></head><body>']
    w = o.append

    # ── masthead ────────────────────────────────────────────────────
    w('<div class="mast"><div class="l1">Sultan Hanafi Royal Schools</div>'
      '<h1>سجلُّ الاعتماد المؤقت للكتب الدراسية</h1>'
      '<div class="div"><i></i></div>'
      '<div class="l2">Temporary Textbook Adoption Register</div>'
      '<div class="ses">العامُ الدراسي ٢٠٢٦ / ٢٠٢٧</div></div>')
    w('<div class="docid"><span><b>الرقم:</b> SHRS/ACB/TTA-01</span>'
      '<span><b>الجهة:</b> المجلس الأكاديمي</span>'
      '<span><b>الموجَّه إلى:</b> مكتب المسجِّل</span>'
      '<span class="st">وثيقةٌ للاعتماد — لم يُقرَّها المجلس بعد</span></div>')

    # ── LAYER 1 · the finding ───────────────────────────────────────
    n_ok = sum(1 for r in rs if 'قرار' not in r['dec'])
    w('<h2><span class="rn">I</span>قرارُ المجلس في سطور — الغرضُ وحالُ هذا السجل</h2>')
    w('<p class="lead">استُؤنفت الدراسةُ قبل تمامِ تأليف كتب المدرسة، فرُفعت قائمتان '
      'بكتبٍ متوفرة. وهذا السجلُّ <b>اعتمادٌ مؤقت</b> لها داخل الإطار الأكاديمي القائم؛ '
      'لا يُنشئ منهجًا، ولا يعدّل السجلَّ الأكاديمي، ولا يُسمّى ما فيه «كتبَ المدرسة».</p>')
    w(f'<div class="note"><b>الخلاصة:</b> رُفع <b>{ar(len(rs))}</b> بندًا في '
      f'<b>{ar(len(R.CLASSES))}</b> صفًّا من شعبتين. '
      f'<b>{ar(n_ok)}</b> منها يصلح للاعتماد المؤقت فورًا، '
      f'و<b>{ar(len(rs) - n_ok)}</b> موقوفةٌ على قرار. '
      f'وثَمَّ <b>{ar(len(real))}</b> موضعًا تُدرَّس فيه مادةٌ بلا كتابٍ مرفوع — '
      f'وليست كلُّها نقصًا، فـ<b>{ar(len(carried))}</b> موضعًا آخر يحملُه كتابُ المضيف '
      'كما يقضي الإطار. <b>ولا تُحدَّد الحصصُ ولا يُبنى الجدولُ في هذه المرحلة.</b></div>')

    # ── II · framework ──────────────────────────────────────────────
    w('<h2><span class="rn">II</span>الإطارُ الحاكم — وقراءةُ مسمّيات الصفوف</h2>')
    w('<p class="lead">الإطارُ القائم هو الحاكم: اثنا عشر صفًّا في أربعة أقسام '
      '(التمهيدي ١–٢ · الابتدائي ٣–٦ · الإعدادي ٧–٩ · الثانوي ١٠–١٢)، وثلاثةُ برامج، '
      'و<b>أربعٌ وثلاثون مادةً</b> مسمّاة — لا ستٌّ وعشرون ولا ثلاثٌ وثلاثون؛ '
      'وقد صدر في ذلك قرارٌ صريح. وكلُّ مادةٍ تحت أحد البرامج الثلاثة، ولا برنامجَ رابع.</p>')
    w('<div class="note"><b>مسألةٌ تتوقف عليها القائمةُ كلُّها.</b> القائمتان تُعنونان '
      '«الصف الأول الابتدائي»، وهو في بنية المدرسة <b>الصفُّ الثالث</b> لا الأول، '
      'لأن الابتدائيَّ يبدأ من الثالث. وقد فُحصت هذه القراءةُ بثلاثة أدلةٍ مستقلة:'
      '<br>١ · <b>نور البيان</b> — وهو متنُ القراءة والتهجي بقرارٍ سابق — مرفوعٌ '
      'لثلاثة صفوفٍ بعينها، وهي الصفوفُ الثلاثة التي تحمل هذه المادة (١–٣).'
      '<br>٢ · <b>تيسير النحو والصرف</b> ج١ ج٢ ج٣ تقع على قواعد اللغة الوظيفية '
      '(٤–٦) مرتين ثم على النحو (٧–١٢) — وهو تدرُّجُ السجل نفسِه بترتيب أجزاء الناشر.'
      '<br>٣ · <b>الإنشاء والتعبير</b> يقع كتاباه داخل مداه (٤–٩).'
      '<br>وعلى القراءة الحرفية يُفتَح النحوُ في الصف الثالث ويتكرر نور البيان في الأول — '
      'وكلاهما مُحال. <b>القراءةُ مثبتةٌ هنا لا مفترَضة، وتُعرض على المجلس للإقرار '
      '(BD-TB-01).</b></div>')

    w('<h3>مطابقةُ المسمّيات</h3>')
    body = ''.join(
        f'<tr><th>{e(h)}</th><td class="n">{ar(g)}</td><td>{e(R.SECTION[g])}</td>'
        f'<td>{e(DIVN[d])}</td><td class="n">{ar(c)}</td></tr>'
        for d, h, g, c in R.CLASSES)
    w(table(['المسمّى في القائمة', 'الصف في بنية المدرسة', 'القسم', 'الشعبة', 'النسخ'], body))

    # ── III · programmes ────────────────────────────────────────────
    w('<h2><span class="rn">III</span>البرامجُ الثلاثة</h2>')
    body = ''.join(
        f'<tr><th><span class="pg {PCLS[k]}">{e(pt)}</span></th>'
        f'<td class="n">{ar(len(R.SUBS_OF[k]))}</td><td>{e(bl)}</td></tr>'
        for k, pn, pt, pen, cls, num, bl in R.PROGS if k != 'التتويج')
    w(table(['البرنامج', 'عدد المواد', 'موضعه في البنية'], body))

    # ── IV / V · the two divisions ──────────────────────────────────
    for div, rn in (('BASIC', 'IV'), ('COLLEGE', 'V')):
        w(f'<h2 class="brk"><span class="rn">{rn}</span>{e(DIVN[div])} — '
          'الكتبُ المعتمدةُ مؤقتًا</h2>')
        w(f'<p class="lead lat" style="text-align:right">{DIVL[div]}</p>')
        for d, h, g, c in R.CLASSES:
            if d != div:
                continue
            w(f'<h3>{e(h)} — الصفُّ {NAMES[g]} · {ar(c)} نسخة</h3>')
            body = ''
            for r in rs:
                if r['div'] != div or r['g'] != g:
                    continue
                body += (f'<tr><th>{e(r["shrs"])}</th>'
                         f'<td><span class="pg {PCLS[r["prog"]]}">{e(PNAME[r["prog"]])}</span></td>'
                         f'<td>{e(r["book"])}<div class="sup">في القائمة: {e(r["supplied"])}</div></td>'
                         f'<td>{e(r["form"])}</td><td>{stat(r["dec"])}'
                         + (f'<div class="sup">{e(r["note"])}</div>' if r['note'] else '')
                         + '</td></tr>')
            w(table(['المادة في إطار SHRS', 'البرنامج', 'الكتاب المعتمد مؤقتًا',
                     'الصيغة', 'الحالة'], body))

    # ── VI · consolidated by programme ──────────────────────────────
    w('<h2 class="brk"><span class="rn">VI</span>السجلُّ المجمَّع بحسب البرامج</h2>')
    w('<p class="lead">الجدولُ الآتي هو <b>جدولُ الاعتماد المرجعي</b>: كلُّ كتابٍ مرفوع، '
      'في شعبته وصفِّه، تحت المادة التي يخدمها من السجل الأكاديمي.</p>')
    for k, pn, pt, pen, cls, num, bl in R.PROGS:
        sel = [r for r in rs if r['prog'] == k]
        if not sel:
            continue
        w(f'<h3><span class="pg {PCLS[k]}">{e(pt)}</span> — {ar(len(sel))} بندًا</h3>')
        body = ''.join(
            f'<tr><th>{e(r["shrs"])}</th><td class="n">{ar(r["g"])}</td>'
            f'<td>{"الأساسية" if r["div"]=="BASIC" else "الكلية"}</td>'
            f'<td>{e(r["book"])}</td><td class="n">{ar(r["copies"])}</td>'
            f'<td>{e(r["form"])}</td></tr>'
            for r in sorted(sel, key=lambda x: (x['g'], x['div'])))
        w(table(['المادة', 'الصف', 'الشعبة', 'الكتاب', 'النسخ', 'الصيغة'], body))

    # ── VII · reconciliation ────────────────────────────────────────
    w('<h2 class="brk"><span class="rn">VII</span>المطابقةُ بين السجل الأكاديمي والقائمة</h2>')

    w('<h3>أ · موادُّ تُدرَّس ولا كتابَ لها ولا لمضيفها</h3>')
    body = ''.join(
        f'<tr><th>{e(x["sub"])}</th><td class="n">{ar(x["g"])}</td>'
        f'<td>{"الأساسية" if x["div"]=="BASIC" else "الكلية"}</td>'
        f'<td><span class="pg {PCLS[x["prog"]]}">{e(PNAME[x["prog"]])}</span></td>'
        f'<td>{e(x["form"])}</td><td>{e(x["host"] or "—")}</td></tr>'
        for x in real)
    w(table(['المادة', 'الصف', 'الشعبة', 'البرنامج', 'الصيغة', 'المضيف'], body))

    w('<h3>ب · موادُّ بلا كتابٍ مستقل — ويحملها كتابُ المضيف</h3>')
    w('<p class="lead">هذه <b>ليست نقصًا</b>. الإطارُ في الصفوف الدنيا يجعل العلمَ '
      'مدمجًا أو مضمّنًا في كتابِ مضيفه، فلا يُحمَّل الطفلُ كتابًا لكلِّ علمٍ مسمّى. '
      f'وعددُها <b>{ar(len(carried))}</b> موضعًا.</p>')
    body = ''.join(
        f'<tr><th>{e(x["sub"])}</th><td class="n">{ar(x["g"])}</td>'
        f'<td>{"الأساسية" if x["div"]=="BASIC" else "الكلية"}</td>'
        f'<td>{e(x["form"])}</td><td>{e(x["by"])}</td></tr>'
        for x in carried)
    w(table(['المادة', 'الصف', 'الشعبة', 'الصيغة', 'يحملها'], body))

    w('<h3>ج · عبءُ الكتب في الصفوف الدنيا</h3>')
    bu = R.burden(rs)
    w('<p class="lead">يقضي الإطارُ بأن يحمل الصفُّ الدنيا <b>كتابًا واحدًا لكل برنامج</b> '
      '(ثلاثةَ كتبٍ لا غير). والمرفوعُ يزيد على ذلك في المواضع الآتية، '
      'وهي مسألةُ قرارٍ لا مسألةُ تنسيق.</p>')
    body = ''.join(
        f'<tr><th>{"الأساسية" if x["div"]=="BASIC" else "الكلية"} — الصف {NAMES[x["g"]]}</th>'
        f'<td><span class="pg {PCLS[x["prog"]]}">{e(PNAME[x["prog"]])}</span></td>'
        f'<td class="n">{ar(x["n"])}</td><td>{e(" · ".join(x["books"]))}</td></tr>'
        for x in bu)
    w(table(['الموضع', 'البرنامج', 'عدد الكتب', 'الكتب'], body))

    w('<h3>د · اختلافُ النسبة والعنوان بين القائمتين</h3>')
    cl = R.clashes()
    body = ''.join(
        f'<tr><th>{e(t)}</th><td>{"<br>".join(e(a) + " — " + e("، ".join(w_)) for a, w_ in by.items())}</td></tr>'
        for t, by in cl.items())
    w(table(['العنوان', 'النسبةُ كما وردت، وموضعُها'], body))

    # ── VIII · decisions ────────────────────────────────────────────
    w('<h2 class="brk"><span class="rn">VIII</span>ما يلزمه قرارُ المجلس</h2>')
    for bd in DECISIONS:
        cls = ' ok' if bd.get('ok') else ''
        w(f'<div class="bd{cls}"><div class="id">{bd["id"]}</div>'
          f'<h4>{bd["t"]}</h4><p>{bd["p"]}</p>'
          f'<div class="out">المطلوب: {bd["o"]}</div></div>')

    # ── X / XI ──────────────────────────────────────────────────────
    w('<h2><span class="rn">IX</span>الترتيبُ بعد هذا السجل</h2>')
    w('<p class="lead">لا تُحدَّد الحصصُ ولا يُبنى الجدولُ قبل إغلاق المطابقة. والترتيب: '
      '<b>١</b> مطابقةُ المنهج · <b>٢</b> الاعتمادُ المؤقت للكتب · <b>٣</b> قراراتُ المجلس '
      'أعلاه · <b>٤</b> تحديدُ الحصص · <b>٥</b> بناءُ الجدول. '
      '<b>وعددُ الكتب لا يحدِّد عددَ الحصص.</b></p>')
    w('<div class="note warn"><b>تنبيه:</b> القائمتان تغطيان الصفوف ١–٧ فقط. '
      'والصفوفُ ٨–١٢ لم يُرفع لها كتابٌ البتة؛ فإن كانت الدراسةُ قائمةً فيها '
      'فهي بلا اعتمادٍ مؤقت (BD-TB-16).</div>')

    w('<h2><span class="rn">X</span>الاعتمادُ وإجراءُ المسجِّل</h2>')
    w('<div class="sig">'
      '<div><b>المجلس الأكاديمي</b>التوقيع / التاريخ</div>'
      '<div><b>مكتب المسجِّل</b>التوقيع / التاريخ</div>'
      '<div><b>رئيس المدارس</b>التوقيع / التاريخ</div></div>')
    w('</body></html>')
    return ''.join(o)


DECISIONS = [
 dict(id='BD-TB-01', ok=True, t='قراءةُ مسمّيات الصفوف',
      p='«الصف الأول الابتدائي» في القائمتين هو <b>الصفُّ الثالث</b> في بنية المدرسة، '
        'و«الأول الإعدادي» هو <b>السابع</b>. فُحصت القراءةُ بثلاثة أدلةٍ مستقلة واتفقت. '
        'وعلى القراءة الحرفية يُفتَح النحوُ في الصف الثالث، وهو نقضٌ لترتيب العلوم.',
      o='إقرارُ المطابقة كما في القسم II، أو تصحيحُها قبل أيِّ شراء.'),
 dict(id='BD-TB-02', t='كتابُ البرنامج في الصفوف الدنيا — أُبدل بكتبِ المسارات',
      p='يقضي الإطارُ بكتابٍ واحدٍ للدراسات الإسلامية في الصفوف ١–٦ '
        '(«التربية الإسلامية»)، تجري فيه أربعةُ مساراتٍ: التوحيد والفقه والحديث والسيرة. '
        'والمرفوعُ يقدّم ثلاثةَ كتبٍ أو أربعةً منفصلة، ولا يقدّم كتابَ البرنامج نفسَه. '
        'وهذا تبديلٌ في بنية الحمل لا في الكتب وحدها.',
      o='إمّا اعتمادُ الكتب المنفصلة استثناءً مؤقتًا مع تسجيل مخالفتها لقاعدة الكتاب '
        'الواحد، وإمّا اختيارُ كتابٍ جامعٍ واحد. لا يُحسم هنا.'),
 dict(id='BD-TB-03', t='«القراءة الراشدة» في الصفين الرابع والخامس',
      p='القراءةُ والتهجي مادةٌ تنتهي بالصف الثالث. والكتابُ مرفوعٌ للرابع والخامس، '
        'حيث لا وجودَ لها في السجل.',
      o='إمّا إدراجُه قارئًا داخل «اللغة العربية» (وهي مستقلةٌ ولها كتاب)، '
        'وإمّا قرارٌ بمدِّ المادة — وهو تعديلُ منهجٍ لا اعتمادُ كتاب.'),
 dict(id='BD-TB-04', t='«متن الحائية» — نسبتان متعارضتان',
      p='نُسب في قائمة الأساسية إلى <b>ابن تيمية</b>، وفي قائمة الكلية إلى '
        '<b>ابن أبي داود السجستاني</b>، وهما مختلفان. ولم يُصحَّح هنا من المعرفة العامة.',
      o='[IDENTITY/EDITION TO BE CONFIRMED] — تُثبت النسبةُ من النسخة المشتراة.'),
 dict(id='BD-TB-05', t='«أعباد المسيح» — عنوانٌ غيرُ محقَّق',
      p='مرفوعٌ للمحفوظات في الصف الثالث في الشعبتين، منسوبًا إلى ابن قيم الجوزية. '
        'ولم يُتحقق العنوانُ على هذه الصورة، ولم يُبدَّل.',
      o='[IDENTITY/EDITION TO BE CONFIRMED] — يُراجَع العنوانُ على النسخة.'),
 dict(id='BD-TB-06', t='«مقرر الأستاذ» — الخط والإملاء',
      p='مرفوعٌ في أربعة مواضع بلا عنوانٍ ولا ناشرٍ ولا مؤلف.',
      o='[IDENTITY/EDITION TO BE CONFIRMED] — لا يصحُّ أمرُ شراءٍ على هذا الوصف.'),
 dict(id='BD-TB-07', t='تسميةُ المصحف تختلف في ثلاثة مواضع',
      p='ورد «القرآن الكريم» و«المصحف الشريف — مجمع الملك فهد» و«مبادئ الترتيل». '
        'والسجلُّ يحدّد المصحفَ بمطبعة الملك فهد برواية حفص. '
        'و«مبادئ الترتيل» كتابُ تلاوةٍ وتجويد، لا مصحف.',
      o='توحيدُ تسمية المصحف، وإعادةُ «مبادئ الترتيل» إلى موضعه الصحيح إن أُريد.'),
 dict(id='BD-TB-08', t='الخطُّ والإملاء في الصف السابع',
      p='المادةُ في السجل من الأول إلى السادس. و«الكافي في قواعد الإملاء» مرفوعٌ للسابع.',
      o='إمّا اعتمادُه مرجعًا للمعلّم، وإمّا قرارٌ بمدِّ المادة إلى السابع.'),
 dict(id='BD-TB-09', t='العقيدةُ في الصف السابع بلا كتاب',
      p='العقيدةُ مادةٌ مستقلةٌ من السابع إلى الثاني عشر. والمرفوعُ للسابع «الأصول الثلاثة» '
        'تحت اسم التوحيد، والتوحيدُ في السابع <b>مضمَّنٌ في العقيدة</b> لا العكس.',
      o='تحديدُ كتابِ العقيدة للسابع، أو إقرارُ أن «الأصول الثلاثة» يخدمها.'),
 dict(id='BD-TB-10', t='التفسيرُ بلا كتابٍ في ثلاثة صفوف',
      p='التفسيرُ يبدأ من الصف الخامس. ولا كتابَ له في الخامس ولا السادس (وهو مضمَّنٌ '
        'في الساعة القرآنية) ولا في السابع — <b>وهو في السابع مستقل</b>.',
      o='تحديدُ كتابِ التفسير للصف السابع على الأقل قبل تحديد الحصص.'),
 dict(id='BD-TB-11', t='اللغةُ العربية في الصف السابع بلا كتاب',
      p='«اللغة العربية» مادةٌ مستقلةٌ في السابع، ولم يُرفع لها كتاب؛ '
        'وإنما رُفعت فروعُها: النحو والصرف والإنشاء والإملاء والمحفوظات.',
      o='تحديدُ كتابِ اللغة العربية للسابع، أو قرارٌ بأن فروعَها تكفي عنه.'),
 dict(id='BD-TB-12', t='الترجمةُ في الصف السابع بلا نص',
      p='الترجمةُ محميّةٌ بقرارٍ قائم وتبدأ من السابع، مضمَّنةً في الإنشاء والتعبير. '
        'ولا نصَّ مرفوعٌ لها. <b>واللغةُ المترجَمُ إليها غيرُ محدَّدةٍ بقرارٍ سابق.</b>',
      o='إمّا إقرارُ أنّ كتابَ الإنشاء يحملها، وإمّا تحديدُ مادةٍ لها.'),
 dict(id='BD-TB-13', t='«مقرر وزارة التعليم السعودية» يخدم مادتين بعنوانٍ واحد',
      p='العنوانُ نفسُه مرفوعٌ للفقه وللتوحيد في الصفوف ٣–٥ بالكلية. '
        'ولا يُميَّز الكتابان في أمر الشراء.',
      o='طلبُ العنوان الدقيق والطبعة لكلٍّ منهما.'),
 dict(id='BD-TB-14', t='سطران لمادةٍ واحدة في الصف السابع',
      p='«الإنشاء الواضح» و«مقرر التعبير» كلاهما يقع على <b>الإنشاء والتعبير</b>، وهي '
        'مادةٌ واحدة. وقد يكون أحدهما كتابَ الطالب والآخرُ مرجعَ المعلّم.',
      o='تحديدُ أيِّهما كتابُ الطالب — وإلا فهو ازدواجٌ في الشراء.'),
 dict(id='BD-TB-15', t='ثمانيةُ اختلافاتٍ في النسبة بين القائمتين',
      p='منها متعارضٌ صريح (الحائية)، ومنها اختلافُ رسمٍ (الأخضري)، '
        'ومنها إسقاطُ النسبة في إحدى القائمتين. مفصَّلةٌ في القسم VII/د.',
      o='توحيدُ النسبة قبل أمر الشراء؛ ولم يُصحَّح منها شيءٌ هنا.'),
 dict(id='BD-TB-16', t='الصفوفُ ٨–١٢ بلا اعتمادٍ مؤقت',
      p='القائمتان تنتهيان عند الصف السابع. فإن كانت الدراسةُ قائمةً في الثامن فما فوق، '
        'فهي بلا كتبٍ معتمدة — ومن مواد تلك الصفوف ما هو محميٌّ بقرار: '
        'الفرائضُ والترجمةُ والبحثُ والخطابة والعروضُ وعلمُ القافية.',
      o='بيانٌ من الإدارة بالصفوف العاملة فعلًا هذا العام، ثم قائمةٌ لها.'),
]

if __name__ == '__main__':
    doc = build()
    p = os.path.join(H, 'ADOPTION-REGISTER.html')
    open(p, 'w', encoding='utf-8').write(doc)
    print(f'written — {len(doc)//1024} KB')
