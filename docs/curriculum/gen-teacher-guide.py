# -*- coding: utf-8 -*-
"""Generate the SHRS Curriculum Handbook (HTML → PDF) from allocation-v11.json.

An INSTITUTIONAL PRESENTATION of the curriculum as it currently stands — for
teachers, management, the Board and parents. It is a communication document:
it settles nothing, creates no policy, and ratifies nothing. Every fact traces
to allocation-v11.json or 00-LOCKED-DECISIONS.md. Where the allocation carries
no declared form, the handbook SAYS SO rather than guessing.

Never hand-edit the output. Change the source and regenerate.
"""
import os, io, html
import curriculum_data as C
from curriculum_data import D

H = os.path.dirname(os.path.abspath(__file__))
AR = '٠١٢٣٤٥٦٧٨٩'
ar = lambda n: ''.join(AR[int(c)] for c in str(n))
e = html.escape

CLS = {1:'الأول',2:'الثاني',3:'الثالث',4:'الرابع',5:'الخامس',6:'السادس',7:'السابع',
       8:'الثامن',9:'التاسع',10:'العاشر',11:'الحادي عشر',12:'الثاني عشر'}

SECTIONS = [
 ('القسم التمهيدي','FOUNDATION','التهيئة وفكُّ الحرف',[1,2],
  'يتعلّم الطفلُ أن يقرأ. ولا علمَ مستقلًّا في هذين الصفّين إلا اللغةُ والتربيةُ الإسلامية '
  'والتجويدُ تلقينًا؛ وكلُّ ما سواها مسارٌ داخل كتابه، يُدرَّس ولا يُفرَد. '
  'والمرادُ أن تُبنى الآلةُ قبل أن يُحمَّل عليها.'),
 ('القسم الابتدائي','PRIMARY','من القراءة إلى الطلاقة، ثم الجسر',[3,4,5,6],
  'تنضج القراءةُ طلاقةً، وتُلمَس القاعدةُ في النصّ قبل أن تُسمَّى باصطلاحها. '
  'يدخل <b>التفسير</b> في الخامس — ولا يُقدَّم عليه — ويستقلّ <b>التجويد</b> من الرابع بمتنه. '
  'وينتهي القسمُ بعبور الطفل من عربيّة الطفولة إلى عربيّة العلم.'),
 ('القسم الإعدادي','INTERMEDIATE','العلومُ بأسمائها، والنحوُ على متونه',[7,8,9],
  'تنفصل العلومُ وتُسمّى: النحوُ والصرفُ والفقهُ والعقيدةُ والحديثُ والتفسير. '
  'واللغةُ آلةُ كلِّ علمٍ منها، فلا ينزل نصيبُها عن الدراسات الإسلامية. '
  'ويُختَم النحوُ الأساس في التاسع، فيُفتَح ما بُني عليه بعده.'),
 ('القسم الثانوي','SENIOR','علومُ الآلة والمتونُ الكبرى، ثم سنةُ التتويج',[10,11,12],
  'تُفتَح <b>البلاغة</b> في العاشر — بعد تمام النحو لا قبله — وتجري المعاني ثم البيان ثم البديع. '
  'وينضج الإنشاءُ بحثًا وخطابةً ومناظرة. والثاني عشر سنةُ تتويجٍ لا سنةُ أوراقٍ جديدة.')]

GATES = [(1,'بوابة القراءة'),(3,'بوابة الطلاقة'),(5,'الشهادة الابتدائية'),
         (6,'بوابة الجسر'),(9,'الشهادة الإعدادية'),(11,'الثانوية القرآنية'),
         (12,'شهادة التخرج')]

PROGS = [('القرآن','البرنامج الأول','القرآن وعلومه','PROGRAMME ONE · THE QURʾĀN AND ITS SCIENCES','p1','I',
          'القرآنُ أصلُ الرحلة لا مادةٌ فيها. يجري حفظُه في ساعةٍ يومية محميّة خارج الجدول، '
          'ويقوم على خدمته ثلاثةُ علوم: التجويدُ ليُقام اللفظ، والتفسيرُ ليُفهم المعنى، '
          'وأصولُ التفسير لتُضبط طريقةُ الفهم.'),
         ('اللغة','البرنامج الثاني','اللغة وعلومها','PROGRAMME TWO · ARABIC AND ITS SCIENCES','p2','II',
          'العربيّةُ آلةُ كلِّ علمٍ شرعيّ، وليست واحدًا منها. ولذلك تبدأ قبل غيرها وتنتهي بعده. '
          'وهي في هذا المنهج لسانٌ حيٌّ يُتكلَّم ويُكتَب ويُخطَب به، لا قواعدَ تُحفظ وحدها.'),
         ('الإسلامية','البرنامج الثالث','الدراسات الإسلامية','PROGRAMME THREE · ISLAMIC STUDIES','p3','III',
          'تبدأ مساراتٍ أربعةً داخل كتابٍ واحدٍ يناسب الطفل، ثم تنفصل علومًا مسمّاةً حين ينضج، '
          'ثم تُفتَح على المتون الكبرى والخلاف بأدبه في الثانوي.'),
         ('التتويج','برنامج التتويج','خدمة سنة التخرج','THE CROWNING YEAR','p4','IV',
          'ليس برنامجًا تعليميًّا رابعًا، بل خدماتُ سنةِ التخرّج: مراجعةُ WAEC، والتحريرُ '
          'الامتحاني، ومشروعُ الخدمة. وموضعُه في البنية معروضٌ على المجلس.')]

FORMLABEL = {'مستقل':'مستقل','مدمج':'مدمج','مضمّن':'مضمّن','وحدة':'وحدة',
             'دوراني':'دوراني','مسار':'مسار','فصلي':'مقرر فصلي'}
ASSESS = {'مستقل':'ورقةٌ مستقلة · يدخل المعدل',
          'مدمج':'قسمٌ مسمّى في ورقة الشريك · أرضية ٤٠٪',
          'مضمّن':'لا ورقةَ له · يُقوَّم داخل المضيف',
          'وحدة':'تقديرُ إنجاز · لا يدخل المعدل',
          'دوراني':'ملفٌّ وسجلُّ مشاركة',
          'مسار':'ملحقٌ وصفيّ بلا رقم',
          'فصلي':'يُقوَّم في فصله'}

# From the Director General's own working sheet (Book1.xlsx). Only these two
# classes carry a memorisation range there; no other class is given one.
SHEET_HIFZ = {1:'سورة الناس ← سورة التكاثر', 2:'سورة القارعة ← سورة العلق'}


def treatment(g):
    corner, slots, hosted = D[str(g)]
    out = {}
    for name, prog, n, note in corner:
        out[C.clean(name)] = ('مستقل', None, prog, note)
    for lab, cap, terms in slots:
        for term, nt, name, prog, note in terms:
            out[C.clean(name)] = ('فصلي', term, prog, note)
    for name, prog, host, note in hosted:
        f = next((ff for ff in C.FORMS if note.strip().startswith(ff)), None)
        d = note
        if f:
            d = note[len(f):].lstrip(' —·-').strip()
        out[C.clean(name)] = (f, C.clean(host), prog, d)
    if g <= 6:
        for s in C.STRANDS[g]:
            out.setdefault(s, ('مسار', 'كتاب الدراسات الإسلامية', 'الإسلامية', ''))
    out['حفظ القرآن الكريم'] = ('مستقل', 'الساعة القرآنية', 'القرآن',
                                SHEET_HIFZ.get(g, ''))
    return out


T = {g: treatment(g) for g in range(1, 13)}
PROG_OF, FIRST, LAST = {}, {}, {}
for g in range(1, 13):
    for s, (f, h, p, n) in T[g].items():
        PROG_OF[s] = p
        FIRST.setdefault(s, g)
        LAST[s] = g

SUBS_OF = {k: [s for s in sorted(PROG_OF, key=lambda x: (FIRST[x], -len([g for g in range(1,13) if x in T[g]]), x))
               if PROG_OF[s] == k] for k, *_ in PROGS}

CLASSOF = {'مستقل':'ind','مدمج':'mrg','مضمّن':'emb','وحدة':'unt','دوراني':'rot',
           'مسار':'str','فصلي':'trm'}


def lifeline(s):
    """A 12-grade band, read as a timeline rather than a grid."""
    o = ['<div class="ll">']
    for g in range(1, 13):
        v = T[g].get(s)
        if not v:
            o.append('<i class="b0"></i>')
            continue
        f = v[0]
        if f is None:
            o.append('<i class="bq" title="صيغة غير مصرَّحة">؟</i>')
        else:
            o.append(f'<i class="b {CLASSOF.get(f,"emb")}"></i>')
    o.append('</div>')
    return ''.join(o)


def phases(s):
    gs = [g for g in range(1, 13) if s in T[g]]
    ph = []
    for g in gs:
        f = T[g][s][0]
        h = T[g][s][1]
        lbl = FORMLABEL.get(f) if f else 'غير مصرَّحة'
        key = (lbl, h if f not in ('مستقل', 'فصلي') else None)
        if ph and ph[-1][0] == key:
            ph[-1][2] = g
        else:
            ph.append([key, g, g])
    out = []
    for (lbl, h), a, b in ph:
        rng = ar(a) if a == b else f'{ar(a)}–{ar(b)}'
        host = f' <span class="hh">← {e(h)}</span>' if h else ''
        cls = 'ph-warn' if lbl == 'غير مصرَّحة' else ''
        out.append(f'<span class="ph {cls}"><b>{rng}</b> {e(lbl)}{host}</span>')
    return ' '.join(out)


def subject_card(s):
    gs = [g for g in range(1, 13) if s in T[g]]
    src = C.src(s, LAST[s])
    unsourced = 'RED' in src or 'لا مصدر' in src
    if unsourced:
        src = 'لا نصَّ مسجَّلًا بعد'
    indep = [g for g in gs if T[g][s][0] == 'مستقل']
    frm = [T[g][s][0] for g in gs]
    asses = ASSESS['مستقل'] if indep else ASSESS.get(
        next((f for f in frm if f), 'مضمّن'), 'يُقوَّم داخل المضيف')
    if indep and len(indep) < len(gs):
        asses = f'ورقةٌ مستقلة من الصف <b>{ar(min(indep))}</b> — وقبله داخل مضيفه'
    gate = C.SGATE.get(s, '')
    unres = [g for g in gs if T[g][s][0] is None]
    # the most substantive note the allocation carries for this subject
    note = ''
    for g in reversed(gs):
        n = (T[g][s][3] or '').strip()
        if len(n) > len(note):
            note = n
    note = note.replace('**', '')
    o = [f'<div class="card"><div class="ct"><h4>{e(s)}</h4>'
         f'<span class="span">الصفوف {ar(FIRST[s])}–{ar(LAST[s])}'
         f'<b>{ar(len(gs))}</b></span></div>']
    o.append(lifeline(s))
    o.append(f'<div class="phs">{phases(s)}</div>')
    o.append('<dl>')
    o.append(f'<dt>التقويم</dt><dd>{asses}</dd>')
    o.append(f'<dt>النصّ</dt><dd>{"<i>"+e(src)+"</i>" if unsourced else src}'
             f'{" <span class=cdr>يُعرَض على المجلس</span>" if unsourced else ""}</dd>')
    if gate:
        o.append(f'<dt>البوابة</dt><dd>{gate}</dd>')
    if note:
        o.append(f'<dt>المحتوى</dt><dd>{e(note)}</dd>')
    if unres:
        o.append('<dt>موقوف</dt><dd class="warn">صيغتُه غير مصرَّحة في '
                 f'{"، ".join(ar(x) for x in unres)} — والفرقُ بين «مدمج» و«مضمّن» '
                 'فرقٌ في درجة الطالب <span class="cdr">يُعرَض على المجلس</span></dd>')
    o.append('</dl></div>')
    return ''.join(o)


def term_rota(g):
    """The only genuinely term-level data the allocation carries."""
    slots = D[str(g)][1]
    if not slots:
        return ''
    o = ['<div class="rota"><h6>المقرَّرات الفصلية — تتبدّل بالفصل</h6><table><thead><tr>'
         '<th>الخانة</th><th>الفصل الأول</th><th>الفصل الثاني</th><th>الفصل الثالث</th>'
         '</tr></thead><tbody>']
    for lab, cap, terms in slots:
        cells = {}
        for term, nt, name, prog, note in terms:
            for t in term.replace('ف', '').split('+'):
                t = t.strip()
                if t.isdigit():
                    cells[int(t)] = C.clean(name)
            if nt > 1 and '+' not in term:
                pass
        o.append(f'<tr><th>{e(lab)}</th>')
        for t in (1, 2, 3):
            o.append(f'<td>{e(cells.get(t,"—"))}</td>')
        o.append('</tr>')
    o.append('</tbody></table></div>')
    return ''.join(o)


def class_page(g):
    sec = next(s for s in SECTIONS if g in s[3])
    o = [f'<div class="cls"><div class="clsh"><h3>الصف {CLS[g]}</h3>'
         f'<span class="cn">{ar(g)}</span>'
         f'<span class="csec">{sec[0]}</span></div>']
    gate = next((n for x, n in GATES if x == g), None)
    if gate:
        o.append(f'<p class="gate">بوابةُ هذا الصف: <b>{e(gate)}</b></p>')
    if g in SHEET_HIFZ:
        o.append(f'<p class="hifz">المحفوظ: <b>{SHEET_HIFZ[g]}</b></p>')
    for key, pn, pt, pen, cls, num, blurb in PROGS:
        items = [(s, v) for s, v in T[g].items() if v[2] == key]
        if not items:
            continue
        ind = sorted([s for s, v in items if v[0] == 'مستقل'])
        trm = sorted([s for s, v in items if v[0] == 'فصلي'])
        oth = sorted([(s, v) for s, v in items if v[0] not in ('مستقل', 'فصلي')])
        o.append(f'<div class="cp {cls}"><h6>{e(pt)}</h6>')
        if ind:
            o.append('<p class="ind">' + ' · '.join(f'<b>{e(s)}</b>' for s in ind) + '</p>')
        if trm:
            o.append('<p class="trm">مقرَّرات فصلية: ' + '، '.join(e(s) for s in trm) + '</p>')
        if oth:
            bits = []
            for s, v in oth:
                f, h = v[0], v[1]
                if f is None:
                    bits.append(f'{e(s)} <span class="q">؟ ← {e(h or "—")}</span>')
                else:
                    bits.append(f'{e(s)} <span class="hh">{e(FORMLABEL.get(f,f))}'
                                f'{" ← "+e(h) if h else ""}</span>')
            o.append('<p class="oth">' + '، '.join(bits) + '</p>')
        o.append('</div>')
    o.append(term_rota(g))
    o.append('</div>')
    return ''.join(o)


TEXTS = []
for sub, entries in C.SRC.items():
    for lo, hi, t in entries:
        for b in C.named_books(t):
            kind = ('متن محفوظ' if 'محفوظ' in t else
                    'مرجع المعلّم' if 'للمعلم' in t else
                    'مواد المدرسة' if '(المدرسة)' in t else 'متن تدريس')
            TEXTS.append((lo, hi, b, sub, kind))
TEXTS.sort(key=lambda x: (x[0], x[1], x[3]))

CSS = """
@page{size:A4;margin:0;}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{font-family:'Amiri',serif;font-size:10.1pt;line-height:1.68;color:#2A2016;
 direction:rtl;background:#fff;
 --brown:#3B2A1D;--esp:#221709;--bronze:#6B4A2E;--gold:#C6A15B;--champ:#E9CE8A;
 --cream:#F7EEDF;--ink:#2A2016;--burg:#7C1F2E;--line:#E3D3B4;}
.kufi,h1,h2,h3,h4,h5,h6,.num,.en{font-family:'Noto Kufi Arabic',sans-serif;font-weight:700;}
.en{direction:ltr;font-family:Georgia,'Times New Roman',serif;font-weight:400;}
.pg{padding:0 15mm;}
.pg>h2:first-child{padding-top:5mm;}
.brk{page-break-before:always;}
.pg.brk{padding-top:5mm;}
.brk{page-break-before:always;}
p{margin:0 0 3mm;}
.g{color:#8A7A66;}
/* ── cover ───────────────────────────────────────────────────────── */
.cover{height:297mm;padding:0;display:flex;flex-direction:column;
 page-break-after:always;background:#3B2A1D;color:#F7EEDF;position:relative;}
.cover .top{flex:1;display:flex;flex-direction:column;justify-content:flex-end;
 padding:0 22mm 0;}
.cover .rule{height:1.2pt;background:#C6A15B;width:34mm;margin:0 0 9mm;}
.cover .inst{font-family:Georgia,serif;font-size:9.5pt;letter-spacing:.22em;
 color:#C6A15B;direction:ltr;margin:0 0 2mm;}
.cover .instar{font-size:11pt;color:#E9CE8A;margin:0 0 16mm;}
.cover h1{font-size:33pt;line-height:1.3;margin:0 0 5mm;color:#fff;}
.cover .en2{font-family:Georgia,serif;font-size:13pt;letter-spacing:.1em;color:#C6A15B;
 direction:ltr;margin:0 0 4mm;}
.cover .sub{font-size:12.5pt;color:#D9CDBB;margin:0 0 20mm;max-width:120mm;}
.cover .foot{background:#221709;padding:11mm 22mm;border-top:1pt solid #6B4A2E;}
.cover .foot .l1{font-size:10pt;color:#E9CE8A;margin:0 0 1.5mm;}
.cover .foot .l2{font-family:Georgia,serif;font-size:8pt;color:#A08F79;direction:ltr;
 letter-spacing:.06em;}
/* ── imprint ─────────────────────────────────────────────────────── */
.imp{padding:6mm 22mm 0;}
.imp h2{border:0;font-size:13pt;margin:0 0 6mm;color:var(--brown);}
.imp .attr{border-right:2pt solid var(--gold);padding:4mm 6mm;background:#FBF7F0;
 margin:0 0 8mm;font-size:9.6pt;}
.imp .attr .lat{font-family:Georgia,serif;direction:ltr;font-size:8.6pt;color:var(--bronze);
 margin-top:2mm;}
.imp .status{border:.7pt solid var(--burg);padding:4mm 6mm;background:#FDF8F7;
 font-size:9.3pt;color:#5A3030;margin:0 0 8mm;}
.toc{font-size:10pt;}
.toc div{display:flex;justify-content:space-between;border-bottom:.4pt dotted #D8C9AE;
 padding:1.7mm 0;}
.toc .t{color:var(--brown);} .toc .p{color:#8A7A66;font-family:Georgia,serif;}
.toc .pt{font-family:'Noto Kufi Arabic',sans-serif;font-size:8.4pt;color:var(--gold);
 letter-spacing:.05em;margin:5mm 0 1mm;}
/* ── part opener ─────────────────────────────────────────────────── */
.opener{page-break-before:always;height:243mm;display:flex;flex-direction:column;
 justify-content:center;padding:0 22mm;border-right:3pt solid var(--gold);}
.opener .pn{font-family:Georgia,serif;font-size:9.5pt;letter-spacing:.24em;
 color:var(--gold);direction:ltr;margin:0 0 5mm;}
.opener h2{font-size:27pt;color:var(--brown);border:0;margin:0 0 3mm;padding:0;}
.opener .ar2{font-size:15pt;color:var(--bronze);margin:0 0 6mm;}
.opener .en3{font-family:Georgia,serif;font-size:9.5pt;letter-spacing:.12em;
 color:#8A7A66;direction:ltr;margin:0 0 10mm;}
.opener p{font-size:11.4pt;color:#4A3826;max-width:132mm;line-height:1.85;}
.opener.p1{border-color:#C6A15B;} .opener.p2{border-color:#6B4A2E;}
.opener.p3{border-color:#7C1F2E;} .opener.p4{border-color:#A08F79;}
.opener .stat{margin-top:11mm;display:flex;gap:14mm;border-top:.6pt solid var(--line);
 padding-top:5mm;}
.opener .stat b{display:block;font-family:'Noto Kufi Arabic',sans-serif;font-size:19pt;
 color:var(--brown);line-height:1.1;}
.opener .stat span{font-size:8.6pt;color:#8A7A66;}
/* ── general headings ────────────────────────────────────────────── */
h2{font-size:15pt;color:var(--brown);border-bottom:1.4pt solid var(--gold);
 padding-bottom:2.5mm;margin:0 0 6mm;page-break-after:avoid;}
h3{font-size:12.4pt;color:var(--brown);margin:8mm 0 3mm;page-break-after:avoid;}
h5{font-size:10.4pt;color:var(--brown);margin:6mm 0 2mm;}
h6{font-size:8.6pt;color:var(--bronze);margin:0 0 2mm;letter-spacing:.04em;font-weight:400;}
.lead{font-size:11pt;color:#4A3826;line-height:1.85;margin-bottom:6mm;}
/* ── journey band ────────────────────────────────────────────────── */
.journey{margin:0 0 7mm;}
.jrow{display:flex;gap:1.1mm;}
.jsec{flex:1;border-top:2.2pt solid var(--gold);padding-top:2mm;}
.jsec:nth-child(2){border-color:#B08E4E;} .jsec:nth-child(3){border-color:#6B4A2E;}
.jsec:nth-child(4){border-color:#7C1F2E;}
.jsec .nm{font-family:'Noto Kufi Arabic',sans-serif;font-size:8.8pt;color:var(--brown);}
.jsec .en4{font-family:Georgia,serif;font-size:6.6pt;letter-spacing:.14em;color:#A08F79;
 direction:ltr;margin-bottom:1.5mm;}
.jsec .cells{display:flex;gap:1mm;}
.jsec .c{flex:1;background:#F6EFE1;text-align:center;padding:2mm 0 1.6mm;
 font-family:'Noto Kufi Arabic',sans-serif;font-size:9.5pt;color:var(--brown);}
.jsec .c.gt{background:#3B2A1D;color:#E9CE8A;}
.jsec .gl{font-size:6.4pt;color:var(--burg);margin-top:1.2mm;line-height:1.3;}
/* ── form legend ─────────────────────────────────────────────────── */
.forms{width:100%;border-collapse:collapse;font-size:9.3pt;margin:0 0 5mm;}
.forms th,.forms td{border-bottom:.5pt solid var(--line);padding:2.2mm 2.5mm;
 text-align:right;vertical-align:top;}
.forms thead th{background:transparent;border-bottom:1pt solid var(--brown);
 font-family:'Noto Kufi Arabic',sans-serif;font-size:8.2pt;color:var(--bronze);font-weight:400;}
.forms .k{width:19%;font-weight:700;color:var(--brown);white-space:nowrap;}
.forms .sw{display:inline-block;width:3.4mm;height:3.4mm;margin-left:2mm;
 vertical-align:-.5mm;border:.5pt solid #C9B896;}
/* ── lifeline ────────────────────────────────────────────────────── */
.ll{display:flex;gap:.8mm;margin:1.5mm 0 2mm;}
.ll i{flex:1;height:4.4mm;display:block;border-radius:.4mm;}
.ll .b0{background:#F4F1EA;}
.ll .ind{background:#3B2A1D;} .ll .trm{background:#B08E4E;}
.ll .mrg{background:#8A6B45;} .ll .emb{background:#C6A15B;}
.ll .unt{background:#D8BE8B;} .ll .rot{background:#DFCBA6;}
.ll .str{background:#EFE2C8;}
.ll .bq{background:#F6E4E0;color:#7C1F2E;font-size:6.6pt;text-align:center;
 line-height:4.4mm;font-style:normal;font-family:'Noto Kufi Arabic',sans-serif;}
.phs{font-size:8.2pt;color:#6B5844;margin:0 0 2mm;line-height:1.9;}
.ph{background:#FBF7F0;border:.4pt solid #EADFC8;padding:.5mm 1.8mm;white-space:nowrap;}
.ph b{color:var(--brown);font-family:'Noto Kufi Arabic',sans-serif;font-size:7.6pt;}
.ph.ph-warn{background:#FCF3F0;border-color:#E8CFC8;color:var(--burg);}
.hh{color:#8A7A66;}
/* ── subject card ────────────────────────────────────────────────── */
.cards{column-count:2;column-gap:7mm;}
.card{break-inside:avoid;page-break-inside:avoid;border-top:1.4pt solid var(--brown);
 padding:2.5mm 0 3.5mm;margin:0 0 4mm;}
.p1 .card{border-color:#C6A15B;} .p2 .card{border-color:#6B4A2E;}
.p3 .card{border-color:#7C1F2E;} .p4 .card{border-color:#A08F79;}
.ct{display:flex;justify-content:space-between;align-items:baseline;}
.ct h4{font-size:11.2pt;color:var(--brown);margin:0;}
.span{font-size:7.4pt;color:#8A7A66;white-space:nowrap;}
.span b{font-family:'Noto Kufi Arabic',sans-serif;color:var(--bronze);font-size:8.6pt;
 margin-right:2mm;}
.card dl{margin:0;display:grid;grid-template-columns:16% 84%;gap:.4mm 0;font-size:8.9pt;}
.card dt{color:#9A8A76;font-size:7.8pt;font-family:'Noto Kufi Arabic',sans-serif;
 font-weight:400;padding-top:.4mm;}
.card dd{margin:0;}
.card dd.warn{color:var(--burg);}
.cdr{font-family:Georgia,serif;font-size:6.6pt;letter-spacing:.04em;color:var(--burg);
 border:.4pt solid #E0C6BE;padding:.2mm 1.2mm;white-space:nowrap;direction:rtl;}
/* ── class page ──────────────────────────────────────────────────── */
.cls{border-top:1.4pt solid var(--brown);padding:3mm 0 4mm;margin:0 0 5mm;
 page-break-inside:avoid;}
.clsh{display:flex;align-items:baseline;gap:4mm;margin:0 0 2.5mm;}
.clsh h3{margin:0;font-size:13pt;}
.cn{font-family:'Noto Kufi Arabic',sans-serif;font-size:20pt;color:#C6A15B;
 line-height:1;}
.csec{margin-right:auto;font-size:8.4pt;color:#8A7A66;}
.gate{background:#3B2A1D;color:#F7EEDF;font-size:8.8pt;padding:1.6mm 3mm;margin:0 0 2.5mm;}
.hifz{background:#F6EFE1;font-size:9.2pt;padding:1.6mm 3mm;margin:0 0 2.5mm;}
.cp{border-right:1.6pt solid var(--gold);padding:0 3mm 0;margin:0 0 2.5mm;}
.cp.p2{border-color:#6B4A2E;} .cp.p3{border-color:#7C1F2E;} .cp.p4{border-color:#A08F79;}
.cp p{margin:0 0 1mm;font-size:9.2pt;}
.cp .ind b{color:var(--brown);}
.cp .trm,.cp .oth{color:#6B5844;font-size:8.8pt;}
.q{color:var(--burg);font-size:8pt;}
.rota{margin-top:2.5mm;}
.rota table{width:100%;border-collapse:collapse;font-size:8.5pt;}
.rota th,.rota td{border:.4pt solid var(--line);padding:1.3mm 2mm;text-align:center;}
.rota thead th{background:#F2E9DA;color:var(--brown);font-family:'Noto Kufi Arabic',sans-serif;
 font-size:7.6pt;font-weight:400;}
.rota tbody th{background:#FBF7F0;color:var(--bronze);font-size:8pt;}
/* ── texts ───────────────────────────────────────────────────────── */
.txt{width:100%;border-collapse:collapse;font-size:9pt;}
.txt th,.txt td{border-bottom:.45pt solid var(--line);padding:1.9mm 2.5mm;text-align:right;}
.txt thead th{border-bottom:1pt solid var(--brown);font-family:'Noto Kufi Arabic',sans-serif;
 font-size:8.2pt;color:var(--bronze);font-weight:400;}
.txt .gr{font-family:'Noto Kufi Arabic',sans-serif;color:var(--brown);white-space:nowrap;
 width:13%;}
.txt .kd{color:#8A7A66;font-size:8.2pt;width:18%;}
.txt tr.sec td{background:#F6EFE1;font-family:'Noto Kufi Arabic',sans-serif;font-size:8.4pt;
 color:var(--brown);padding:1.5mm 2.5mm;}
/* ── notes ───────────────────────────────────────────────────────── */
.rules{margin:0;padding:0;list-style:none;counter-reset:r;}
.rules li{counter-increment:r;position:relative;padding-right:10mm;margin:0 0 4mm;
 font-size:10pt;page-break-inside:avoid;}
.rules li:before{content:counter(r);position:absolute;right:0;top:.2mm;
 font-family:'Noto Kufi Arabic',sans-serif;font-size:11pt;color:var(--gold);}
.rules b{color:var(--brown);}
.open{width:100%;border-collapse:collapse;font-size:9.4pt;margin-top:3mm;}
.open th,.open td{border-bottom:.45pt solid var(--line);padding:2.2mm 2.5mm;text-align:right;
 vertical-align:top;}
.open thead th{border-bottom:1pt solid var(--brown);font-size:8.2pt;color:var(--bronze);
 font-family:'Noto Kufi Arabic',sans-serif;font-weight:400;}
.open .w{width:32%;color:var(--brown);}
.colo{margin-top:9mm;border-top:.6pt solid var(--line);padding-top:4mm;font-size:8.4pt;
 color:#8A7A66;}
"""


def build():
    o = io.StringIO(); w = o.write
    w('<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8">'
      '<title>مدارس السلطان حنفي الملكية — دليل المنهج العربي والإسلامي</title>'
      f'<style>{CSS}</style></head><body>')

    # ═══ COVER ═══
    w('<div class="cover"><div class="top"><div class="rule"></div>'
      '<div class="inst">SULTAN HANAFI ROYAL SCHOOLS</div>'
      '<div class="instar">مدارس السلطان حنفي الملكية · مدرسة الدراسات الإسلامية والعربية</div>'
      '<h1>دليلُ المنهج<br>العربيِّ والإسلامي</h1>'
      '<div class="en2">THE CURRICULUM HANDBOOK</div>'
      '<div class="sub">البرامجُ الثلاثة، وأقسامُها الأربعة، '
      'وتدرُّجُ موادِّها في اثني عشر صفًّا</div></div>'
      '<div class="foot"><div class="l1">إصدارُ العمل · سبتمبر ٢٠٢٦</div>'
      '<div class="l2">WORKING EDITION &middot; NOT YET RATIFIED BY COUNCIL</div></div></div>')

    # ═══ IMPRINT ═══
    w('<div class="imp"><h2>عن هذا الإصدار</h2>')
    w('<div class="attr">إعدادٌ وإشرافٌ واعتماد:<br>'
      '<b>الهيئة الأكاديمية العالمية للدراسات العربية والإسلامية والدعوة والمناهج والبحوث</b>'
      '<div class="lat">Prepared, Supervised, and Approved by the Global Academic Council '
      'for Arabic and Islamic Studies, Da\'wah, Curriculum and Research (GACAIS)</div></div>')
    w('<div class="status"><b>وثيقةُ عملٍ للعرض والتواصل — لا للتقرير.</b><br>'
      'تنقل هذه النشرةُ ترتيبَ المنهج كما هو قائمٌ اليوم، ليقرأه المعلّمُ والإدارةُ '
      'ومجلسُ الأمناء ووليُّ الأمر على صورةٍ واحدة. '
      '<b>وهي لا تُنشئ قرارًا، ولا تعتمد منهجًا، ولا تحسم مسألةً معروضة.</b> '
      'وما كان منها موقوفًا على المجلس فهو مُعلَّمٌ في موضعه بنصِّه، ولم يُملأ فراغُه باجتهاد. '
      'والأعدادُ والمُدَدُ الزمنية لم تُعتمد بعدُ، فلا تَرِد هنا أصلًا.</div>')
    w('<h2>المحتويات</h2><div class="toc">')
    toc = [('الباب الأول','بنيةُ المنهج',[('الرحلة في اثني عشر صفًّا',''),
            ('كيف تُقرأ صيغُ التدريس',''),('الأقسام الأربعة','')])]
    w('<div class="pt">الباب الأول</div>')
    for t in ['الرحلةُ في اثني عشر صفًّا','كيف تُقرأ هذه الوثيقة — الصيغُ الستّ',
              'الأقسامُ الأربعة وبواباتها']:
        w(f'<div><span class="t">{t}</span><span class="p">—</span></div>')
    for key, pn, pt, pen, cls, num, blurb in PROGS[:3]:
        w(f'<div class="pt">{pn}</div>')
        w(f'<div><span class="t">{pt} — الخريطة وبطاقاتُ المواد</span>'
          f'<span class="p">{ar(len(SUBS_OF[key]))} مادة</span></div>')
    w('<div class="pt">الأبواب الختامية</div>')
    for t in ['ما يُدرَّس في كل صف','مواضعُ المتون','قواعدُ لازمة · وما هو موقوف']:
        w(f'<div><span class="t">{t}</span><span class="p">—</span></div>')
    w('</div></div>')

    # ═══ PART I ═══
    w('<div class="opener"><div class="pn">PART ONE</div>'
      '<h2>بنيةُ المنهج</h2><div class="ar2">الرحلةُ والأقسامُ والبرامج</div>'
      '<div class="en3">THE ACADEMIC ARCHITECTURE</div>'
      '<p>اثنا عشر صفًّا، في أربعة أقسام، تجري فيها ثلاثةُ برامجَ متوازية لا متعاقبة. '
      'والمادةُ الواحدة لا تُدرَّس على صورةٍ واحدة طولَ الرحلة: تبدأ خيطًا داخل كتاب، '
      'ثم تُضمَّن في مضيفٍ مسمّى، ثم تستقلّ بحصّتها وكتابها وورقتها حين ينضج صاحبُها لها.</p>'
      f'<div class="stat"><div><b>{ar(12)}</b><span>صفًّا</span></div>'
      f'<div><b>{ar(4)}</b><span>أقسام</span></div>'
      f'<div><b>{ar(3)}</b><span>برامج</span></div>'
      f'<div><b>{ar(len(PROG_OF))}</b><span>مادة مسمّاة</span></div>'
      f'<div><b>{ar(7)}</b><span>بوابات</span></div></div></div>')

    w('<div class="pg brk"><h2>الرحلةُ في اثني عشر صفًّا</h2>'
      '<p class="lead">كلُّ قسمٍ يسلّم إلى الذي بعده بعبورٍ مسمًّى. والصفُّ المظلَّل بوابةٌ '
      'يُختبَر عندها ما بُني قبلها.</p><div class="journey"><div class="jrow">')
    for name, en, char, gs, desc in SECTIONS:
        w(f'<div class="jsec"><div class="nm">{name}</div><div class="en4">{en}</div>'
          '<div class="cells">')
        for g in gs:
            gt = next((n for x, n in GATES if x == g), None)
            w(f'<div class="c{" gt" if gt else ""}">{ar(g)}'
              f'{f"<div class=gl>{e(gt)}</div>" if gt else ""}</div>')
        w('</div></div>')
    w('</div></div>')

    w('<h2>كيف تُقرأ هذه الوثيقة</h2>'
      '<p class="lead">اسمُ المادة لا يعني حصّةً مستقلّة. <b>الصيغةُ</b> هي التي تقول '
      'كيف تُدرَّس وكيف تُقوَّم. وهي ستٌّ لا سابعَ لها، ومعها «الشرط» وهو أثرُ تقويمٍ '
      'لا صورةُ تدريس.</p>'
      '<table class="forms"><thead><tr><th class="k">الصيغة</th><th>في الحصّة</th>'
      '<th>في الشهادة</th></tr></thead><tbody>'
      '<tr><td class="k"><span class="sw" style="background:#3B2A1D"></span>مستقل</td>'
      '<td>حصّةٌ خاصة، وكتابٌ، ومعلّمٌ مسؤول عنه</td><td>ورقةٌ مستقلة · يدخل المعدّل</td></tr>'
      '<tr><td class="k"><span class="sw" style="background:#8A6B45"></span>مدمج</td>'
      '<td>علمان يُدرَّسان في كتلةٍ واحدة قصدًا، لا اختصارًا</td>'
      '<td>قسمٌ مسمّى في ورقة الشريك · أرضية ٤٠٪</td></tr>'
      '<tr><td class="k"><span class="sw" style="background:#C6A15B"></span>مضمّن</td>'
      '<td>يُدرَّس داخل حصص مضيفٍ <b>مسمّى</b>، بلا كلفةٍ في الجدول</td>'
      '<td>لا ورقةَ له وحده · يُقوَّم داخل مضيفه</td></tr>'
      '<tr><td class="k"><span class="sw" style="background:#D8BE8B"></span>وحدة</td>'
      '<td>كتلةٌ مغلقة، محدودةُ الطول، لها مبتدأٌ ومنتهى</td>'
      '<td>تقديرُ إنجاز · لا يدخل المعدّل</td></tr>'
      '<tr><td class="k"><span class="sw" style="background:#DFCBA6"></span>دوراني</td>'
      '<td>يجري على نوبةٍ، فلا يلقاه كلُّ صفٍّ في الفصل نفسه</td>'
      '<td>ملفٌّ وسجلُّ مشاركة — ولا ورقةَ له</td></tr>'
      '<tr><td class="k"><span class="sw" style="background:#EFE2C8"></span>مسار</td>'
      '<td>خيطٌ داخل كتابٍ جامع، يُدرَّس ولا يُفرَد</td>'
      '<td>ملحقٌ وصفيّ بلا رقم</td></tr>'
      '<tr><td class="k"><span class="sw" style="background:#B08E4E"></span>مقرر فصلي</td>'
      '<td>يشغل خانةً فصلًا واحدًا ثم يسلّمها لغيره</td><td>يُقوَّم في فصله</td></tr>'
      '<tr><td class="k">شرط</td><td>ليس صورةَ تدريسٍ أصلًا</td>'
      '<td><b>لا يحمل درجةً أبدًا</b> · يُستوفى أو لا يُستوفى</td></tr>'
      '</tbody></table>'
      '<p class="g" style="font-size:9pt">وحيثما ورد في هذه الوثيقة '
      '<span class="q">؟</span> فمعناه أنّ المادة تُدرَّس داخل المضيف المذكور، '
      'ولكنّ صيغتَها لم تُصرَّح بعدُ في البيانات — ولم نفترضها، لأنّ الفرق بين '
      '«مدمج» و«مضمّن» فرقٌ في درجة الطالب لا في العبارة.</p>')

    w('<h2 style="margin-top:9mm">الأقسامُ الأربعة</h2>')
    for name, en, char, gs, desc in SECTIONS:
        w(f'<div class="cls" style="page-break-inside:avoid"><div class="clsh">'
          f'<h3>{name}</h3><span class="cn">{ar(gs[0])}–{ar(gs[-1])}</span>'
          f'<span class="csec en">{en}</span></div>'
          f'<p style="color:#6B4A2E;font-size:10.4pt;margin-bottom:2mm">{char}</p>'
          f'<p>{desc}</p></div>')
    w('</div>')

    # ═══ PROGRAMME PARTS ═══
    for key, pn, pt, pen, cls, num, blurb in PROGS:
        subs = SUBS_OF[key]
        if not subs:
            continue
        ind = len({s for s in subs if any(T[g].get(s, (None,))[0] == 'مستقل' for g in range(1, 13))})
        w(f'<div class="opener {cls}"><div class="pn">PROGRAMME {num}</div>'
          f'<h2>{pt}</h2><div class="ar2">{pn}</div>'
          f'<div class="en3">{pen}</div><p>{blurb}</p>'
          f'<div class="stat"><div><b>{ar(len(subs))}</b><span>مادة</span></div>'
          f'<div><b>{ar(ind)}</b><span>تستقلّ بورقة</span></div>'
          f'<div><b>{ar(min(FIRST[s] for s in subs))}–{ar(max(LAST[s] for s in subs))}</b>'
          '<span>مدى الصفوف</span></div></div></div>')
        w(f'<div class="pg brk {cls}"><h2>{e(pt)} — خريطةُ المواد</h2>'
          '<p class="lead">كلُّ شريطٍ رحلةُ مادةٍ من أول صفٍّ تلقاه فيه إلى آخره. '
          'وتغيُّرُ اللون تغيُّرٌ في صيغة التدريس، لا في المادة نفسها.</p>'
          '<div class="cards">')
        for s in subs:
            w(subject_card(s))
        w('</div></div>')

    # ═══ CLASS BY CLASS ═══
    w('<div class="opener"><div class="pn">PART FIVE</div>'
      '<h2>ما يُدرَّس في كل صف</h2><div class="ar2">المنظرُ المقلوب</div>'
      '<div class="en3">THE CLASS-BY-CLASS VIEW</div>'
      '<p>المعلّمُ يسأل عن صفِّه لا عن رحلة المادة، ووليُّ الأمر يسأل عن ابنه لا عن المنهج. '
      'وهذا البابُ جوابُهما: كلُّ صفٍّ وما يلقاه فيه الطالبُ من البرامج الثلاثة، '
      'ومقرَّراتُه الفصلية إن كانت له.</p></div>')
    w('<div class="pg brk">')
    for g in range(1, 13):
        w(class_page(g))
    w('</div>')

    # ═══ TEXTS ═══
    w('<div class="opener"><div class="pn">PART SIX</div>'
      '<h2>مواضعُ المتون</h2><div class="ar2">أين يقع كلُّ كتاب</div>'
      '<div class="en3">THE CLASSICAL TEXT PROGRESSION</div>'
      '<p>المتونُ مرتَّبةٌ بأول صفٍّ تُفتَح فيه. وكلُّ موضعٍ هنا مأخوذٌ من السجل بنصّه؛ '
      'وما لم يُسجَّل موضعُه فليس هنا، ولا يُوضَع بالاجتهاد.</p></div>')
    w('<div class="pg brk"><h2>مواضعُ المتون</h2><table class="txt"><thead><tr>'
      '<th class="gr">الصفوف</th><th>المتن</th><th>المادة</th><th class="kd">وجهُ استعماله</th>'
      '</tr></thead><tbody>')
    cur = None
    for lo, hi, b, sub, kind in TEXTS:
        sec = next((s for s in SECTIONS if lo in s[3]), None)
        if sec and sec[0] != cur:
            cur = sec[0]
            w(f'<tr class="sec"><td colspan="4">{cur} — الصفوف {ar(sec[3][0])}–{ar(sec[3][-1])}</td></tr>')
        rng = ar(lo) if lo == hi else f'{ar(lo)}–{ar(hi)}'
        w(f'<tr><td class="gr">{rng}</td><td><b>{e(b)}</b></td><td>{e(sub)}</td>'
          f'<td class="kd">{e(kind)}</td></tr>')
    w('</tbody></table></div>')

    # ═══ NOTES ═══
    unres = sum(1 for g in range(1, 13) for s, v in T[g].items() if v[0] is None)
    w('<div class="opener"><div class="pn">PART SEVEN</div>'
      '<h2>قواعدُ لازمة</h2><div class="ar2">وما هو موقوفٌ على المجلس</div>'
      '<div class="en3">NOTES FOR TEACHERS · AND WHAT REMAINS OPEN</div>'
      '<p>سبعُ قواعدَ يحتاجها من يُدرِّس بهذا المنهج، ثم بيانٌ صريحٌ بما لم يُفصَل فيه بعد. '
      'وإعلانُ الموقوف أنفعُ من إخفائه، لأنّ المعلّمَ الذي لا يعرف حدودَ المقرَّر '
      'يملأ الفراغَ باجتهاده.</p></div>')
    w('<div class="pg brk"><h2>قواعدُ لازمة للمعلّم</h2><ol class="rules">'
      '<li><b>لا تُنشئ مادةً ولا تُلغِها.</b> ما في هذه الخريطة هو المقرَّر. '
      'ومن رأى فيها خطأً رفعه إلى القسم، ولم يُصلحه في صفِّه وحده.</li>'
      '<li><b>المضمَّنُ منهجٌ حقيقيّ.</b> أن يكون بلا ورقةٍ مستقلّة لا يعني أن يُترَك؛ '
      'بل إهمالُه أخفى من إهمال المستقلّ وأشدُّ، لأنه لا يظهر في نتيجة.</li>'
      '<li><b>لا مضيفَ مُختلَق.</b> إن قيل إنّ مادةً تُدرَّس داخل أخرى، وليس للمضيف '
      'اسمٌ في جدولك، فارفع الأمرَ ولا تفترض مضيفًا — فالمادةُ حينئذٍ تتبخّر بلا أثر.</li>'
      '<li><b>صيغةُ التدريس ليست أثرَ التقويم.</b> راجع جدولَ الصيغ في الباب الأول '
      'قبل أن تضع درجةً أو تمنعها.</li>'
      '<li><b>المتنُ لا يُنشئ مذهبًا.</b> وجودُ كتابٍ في القائمة لا يعني أنّ المدرسة '
      'تبنّت مذهبَ مؤلِّفه. الأطرُ المذهبية مُعلَنةٌ بنصِّها في مواضعها، '
      'ولا تُستنبَط من قوائم الكتب.</li>'
      '<li><b>ما كان موقوفًا فلا يُقدَّم تامًّا.</b> ما حمل في هذه الوثيقة '
      '<span class="cdr">يُعرَض على المجلس</span> فهو معروضٌ لم يُفصَل فيه، '
      'ولا يُبنى عليه تدريسٌ ولا امتحان.</li>'
      '<li><b>لا مُدَدَ هنا.</b> عددُ الحصص ومقاديرُ الدقائق لم تُعتمد بعد، '
      'وحُذفت من هذه الوثيقة عمدًا. فلا يُقدَّر منها شيء.</li>'
      '</ol>')
    w('<h2 style="margin-top:9mm">ما هو موقوفٌ اليوم</h2>'
      '<p class="lead">يُعلَن هنا كاملًا، لأنّ وثيقةً تُخفي فراغَها تُورِث المعلّمَ '
      'اجتهادًا في غير موضعه.</p>'
      '<table class="open"><thead><tr><th class="w">الموضع</th><th>الحال</th></tr></thead><tbody>'
      f'<tr><td class="w">صيغةُ {ar(unres)} مدخلًا مستضافًا</td>'
      '<td>تُدرَّس داخل مضيفٍ معلوم، وصيغتُها غير مصرَّحة. والفرقُ بين «مدمج» و«مضمّن» '
      'فرقٌ في درجة الطالب — فرُفع ولم يُفترَض</td></tr>'
      '<tr><td class="w">الترجمة · الصفوف ٧–١٢</td>'
      '<td>لا نصَّ مسجَّلًا لها، <b>واللغةُ الهدفُ غيرُ مسمّاة</b> — وقد يكون النقلُ إلى '
      'الإنجليزية أو الهوسا أو الأردية أو اليوربا</td></tr>'
      '<tr><td class="w">أحكامُ عدم اجتياز البوابات</td>'
      '<td>البواباتُ سبعٌ، ولم يُكتب بعدُ ما يقع بالطالب عند عدم الاجتياز</td></tr>'
      '<tr><td class="w">الكفاياتُ العشر</td>'
      '<td>شرطُ شهادة التخرّج. والعاشرةُ وحدَها لها نصٌّ مسجَّل</td></tr>'
      '<tr><td class="w">كتابُ البرنامج الثاني في ٤–٦</td>'
      '<td>معتمَدٌ في التوزيع، ولا مدخلَ له في أبواب النصوص</td></tr>'
      '<tr><td class="w">عددُ الحصص والمُدَد</td>'
      '<td>لم تُعتمد — وحُذفت من هذه الوثيقة عمدًا</td></tr>'
      '</tbody></table>')
    w('<div class="colo"><b>عن هذا الإصدار.</b> '
      'مولَّدٌ آليًّا من <b>allocation-v11.json</b> و<b>00-LOCKED-DECISIONS.md</b> '
      'بواسطة <code>gen-teacher-guide.py</code> — فلا يُحرَّر باليد، وإنما يُغيَّر المصدرُ '
      'ويُعاد التوليد. وموضعا المحفوظ في الصفّين الأول والثاني من ورقة عمل المدير العام. '
      'ولم يُوضَع في هذه الوثيقة اسمٌ ولا موضعٌ ولا نصٌّ لا أصلَ له في أحد هذين المصدرين. '
      '<br><br><b>وهي وثيقةُ عملٍ غيرُ معتمدة</b> — تُقرأ للتواصل، ولا يُحتجّ بها قرارًا، '
      'ولا تُغني عن الوثائق الحاكمة حين تصدر.</div></div>')

    w('</body></html>')
    return o.getvalue()


if __name__ == '__main__':
    doc = build()
    p = os.path.join(H, 'SHRS-CURRICULUM-HANDBOOK.html')
    open(p, 'w', encoding='utf-8').write(doc)
    print(f'written — {len(doc)//1024} KB · {len(PROG_OF)} subjects · '
          f'{sum(1 for g in range(1,13) for s,v in T[g].items() if v[0] is None)} unresolved')
