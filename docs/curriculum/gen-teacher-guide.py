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
          'برنامجُ <b>قسم الدراسات الإسلامية والعربية</b> — School of Islamic and Arabic Studies — '
          'بمدارس السلطان حنفي الملكية. '
          'يبدأ مساراتٍ أربعةً داخل كتابٍ واحدٍ يناسب الطفل، ثم تنفصل علومًا مسمّاةً حين ينضج، '
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


# ── counting, stated once so the numbers can be audited ───────────────────
def tally(g):
    """Curriculum areas vs timetabled slots — never conflated."""
    corner, slots, hosted = D[str(g)]
    t = {'areas': len(T[g]), 'ceil': C.CEIL[str(g)],
         'shared': sum(sl[1] for sl in slots), 'prog': {}, 'forms': {}}
    for key, *_ in PROGS:
        n_area = sum(1 for v in T[g].values() if v[2] == key)
        n_slot = sum(x[2] for x in corner if T[g].get(C.clean(x[0]), (None,None,None))[2] == key)
        t['prog'][key] = (n_area, n_slot)
    for s2, v in T[g].items():
        k = v[0] or 'غير مصرَّحة'
        t['forms'][k] = t['forms'].get(k, 0) + 1
    t['own'] = sum(1 for v in T[g].values() if v[0] in ('مستقل', 'فصلي'))
    t['inhost'] = t['areas'] - t['own']
    return t


def slots_of(g, sub):
    """Weekly حصص for this subject in this class — or None when it holds no slot."""
    corner, slots, hosted = D[str(g)]
    for name, prog, n, note in corner:
        if C.clean(name) == sub:
            return n, False
    for lab, cap, terms in slots:
        for term, nt, name, prog, note in terms:
            if C.clean(name) == sub:
                return cap, True
    return None, False


def class_card(g):
    t = tally(g)
    sec = next(x for x in SECTIONS if g in x[3])
    o = ['<div class="ccard"><div class="ccrow">']
    o.append(f'<div class="ccbig s1"><em></em><b>{ar(t["areas"])}</b>'
             '<span>مجالًا في المنهج</span><i>Curriculum areas</i></div>')
    o.append(f'<div class="ccbig s2"><b>{ar(t["ceil"])}</b>'
             '<span>حصّةً في الأسبوع</span><i>Weekly periods</i></div>')
    o.append(f'<div class="ccbig s3"><b>{ar(t["own"])}</b>'
             '<span>بحصّةٍ خاصّة</span><i>Own slot</i></div>')
    o.append(f'<div class="ccbig s4"><b>{ar(t["inhost"])}</b>'
             '<span>داخل مضيفٍ مسمّى</span><i>Within a host</i></div>')
    o.append('</div><div class="ccprog">')
    for key, pn, pt, pen, cls, num, blurb in PROGS:
        a, sl = t['prog'][key]
        if not a:
            continue
        o.append(f'<div class="ccp {cls}"><span class="rn">{num}</span>'
                 f'<h6>{e(pt)}</h6>'
                 f'<div class="ccn"><span><b>{ar(a)}</b> مجالًا</span>'
                 f'<span><b>{ar(sl)}</b> حصّة</span></div></div>')
    if t['shared']:
        o.append(f'<div class="ccp shared"><span class="rn">&#9671;</span>'
                 '<h6>خانات فصلية مشتركة</h6>'
                 f'<div class="ccn"><span><b>{ar(t["shared"])}</b> حصّة</span>'
                 '<span>تتناوبها مقرَّرات الفصول</span></div></div>')
    o.append('</div>')
    # forms breakdown + assessment picture
    fb = ' · '.join(f'{e(FORMLABEL.get(k, k))} <b>{ar(v)}</b>'
                    for k, v in sorted(t['forms'].items(), key=lambda x: -x[1]))
    cond = [n for x, n in GATES if x == g]
    o.append(f'<div class="ccfoot"><div><span class="lb">الصيغ</span> {fb}</div>')
    o.append(f'<div><span class="lb">التقويم</span> '
             f'<b>{ar(t["own"])}</b> بورقةٍ مستقلة · '
             f'<b>{ar(t["inhost"])}</b> يُقوَّم داخل مضيفه'
             + (f' · <b>شرط</b>: {e(cond[0])}' if cond else '') + '</div>')
    o.append(f'<div><span class="lb">القسم</span> {sec[0]} — {e(sec[2])}</div>')
    o.append('</div>')
    o.append('<p class="ccmeth">طريقةُ العدّ: «المجال» كلُّ اسمٍ يلقاه الصفّ بأيِّ صيغة. '
             'و«الحصّة الخاصّة» خانةٌ في الجدول. والمضمَّنُ والمدمجُ والمسارُ تُدرَّس بلا خانةٍ '
             'خاصّة، فلا تُعدّ حصصًا — <b>ولا يعني ذلك أنها أقلُّ إلزامًا</b>. '
             'والساعةُ القرآنية خارج هذه الخانات تمامًا.</p>')
    o.append('</div>')
    return ''.join(o)


def alloc_tables(g):
    o = ['<h3 class="alh">ما يُدرَّس في هذا الصف</h3>']
    for key, pn, pt, pen, cls, num, blurb in PROGS:
        items = [(s2, v) for s2, v in T[g].items() if v[2] == key]
        if not items:
            continue
        rank = {'مستقل': 0, 'فصلي': 1}
        items.sort(key=lambda x: (rank.get(x[1][0], 2), x[0]))
        o.append(f'<div class="alt {cls}"><h4>{e(pt)}</h4><table class="atab"><thead><tr>'
                 '<th>المادة</th><th>الصيغة</th><th>المضيف</th><th>حصص</th><th>التقويم</th>'
                 '</tr></thead><tbody>')
        for s2, (f, h, p, note) in items:
            n, shared = slots_of(g, s2)
            if s2 == 'حفظ القرآن الكريم':
                cells = ('مستقل', 'الساعة القرآنية', '<i>خارج الخانات</i>',
                         'بوابةُ الحفظ — أداءٌ أمام لجنة')
            elif f is None:
                cells = ('<span class="cdr">لم تُصرَّح</span>', e(h or '—'), '—',
                         '<span class="cdr">يُعرَض على المجلس</span>')
            else:
                cells = (e(FORMLABEL.get(f, f)),
                         e(h) if h and f not in ('مستقل', 'فصلي') else '—',
                         (f'<b>{ar(n)}</b>' + (' <i>مشتركة</i>' if shared else '')) if n else '—',
                         ASSESS.get(f, '—'))
            o.append(f'<tr><th>{e(s2)}</th><td>{cells[0]}</td><td>{cells[1]}</td>'
                     f'<td class="c">{cells[2]}</td><td>{cells[3]}</td></tr>')
        o.append('</tbody></table></div>')
    return ''.join(o)


def nav_table():
    o = ['<table class="nav"><thead><tr><th>الصف</th><th>القسم</th>'
         '<th>مجالات</th><th>حصص</th>'
         '<th>القرآن</th><th>اللغة</th><th>الإسلامية</th><th>البوابة</th>'
         '</tr></thead><tbody>']
    cur = None
    for g in range(1, 13):
        t = tally(g)
        sec = next(x for x in SECTIONS if g in x[3])
        if sec[0] != cur:
            cur = sec[0]
        gate = next((n for x, n in GATES if x == g), '—')
        o.append(f'<tr><th class="ng">{ar(g)}</th><td class="ns">{sec[0][6:]}</td>'
                 f'<td class="c"><b>{ar(t["areas"])}</b></td>'
                 f'<td class="c"><b>{ar(t["ceil"])}</b></td>')
        for key in ('القرآن', 'اللغة', 'الإسلامية'):
            a, sl = t['prog'][key]
            o.append(f'<td class="c">{ar(a)} <span class="sl">/ {ar(sl)}</span></td>')
        o.append(f'<td class="ngate">{e(gate)}</td></tr>')
    o.append('</tbody></table>')
    return ''.join(o)

# ── VIEW 1 · CLASS → WHAT IS TAUGHT ────────────────────────────────────────
MARK = {'مستقل':('m-ind','مستقل'),'مدمج':('m-mrg','مدمج'),'مضمّن':('m-emb','مضمّن'),
        'وحدة':('m-unt','وحدة'),'دوراني':('m-rot','دوراني'),'مسار':('m-str','مسار'),
        'فصلي':('m-trm','مقرر فصلي')}


def glance_row(g):
    """One line per class: the subject NAMES only. The ten-second view."""
    o = [f'<tr><th class="gcell"><b>{ar(g)}</b><span>{CLS[g]}</span></th>']
    for key, pn, pt, pen, cls, num, blurb in PROGS[:3]:
        items = [(s, v) for s, v in T[g].items() if v[2] == key]
        if not items:
            o.append('<td class="gl-none">—</td>'); continue
        ind = [s for s, v in sorted(items) if v[0] in ('مستقل', 'فصلي')]
        oth = [s for s, v in sorted(items) if v[0] not in ('مستقل', 'فصلي')]
        bits = ' · '.join(f'<b>{e(x)}</b>' for x in ind)
        if oth:
            bits += ('<span class="gl-o">' + (' · ' if ind else '')
                     + ' · '.join(e(x) for x in oth) + '</span>')
        o.append(f'<td>{bits}</td>')
    extra = [s for s, v in T[g].items() if v[2] == 'التتويج']
    o.append(f'<td class="gl-x">{" · ".join(e(x) for x in sorted(extra)) if extra else "—"}</td>')
    o.append('</tr>')
    return ''.join(o)


def glance_table():
    o = ['<table class="glance"><thead><tr><th class="gcell">الصف</th>']
    for key, pn, pt, pen, cls, num, blurb in PROGS[:3]:
        o.append(f'<th>{e(pt)}</th>')
    o.append('<th class="gl-x">سنة التتويج</th></tr></thead><tbody>')
    cur = None
    for g in range(1, 13):
        sec = next(x for x in SECTIONS if g in x[3])
        if sec[0] != cur:
            cur = sec[0]
            o.append(f'<tr class="gsec"><td colspan="5">{cur}'
                     f'<span> — الصفوف {ar(sec[3][0])}–{ar(sec[3][-1])}</span></td></tr>')
        o.append(glance_row(g))
    o.append('</tbody></table>')
    return ''.join(o)


def class_full(g):
    """A full page for one class. The definitive answer to: what do I teach?"""
    sec = next(x for x in SECTIONS if g in x[3])
    gate = next((n for x, n in GATES if x == g), None)
    o = [f'<div class="cpage"><div class="cpband"><div class="cpn">{ar(g)}</div>'
         f'<div class="cpt"><h2>الصف {CLS[g]}</h2>'
         f'<div class="cpsec">{sec[0]} <span class="en">&middot; GRADE {g}</span></div></div>']
    if gate:
        o.append(f'<div class="cpgate"><em>بوابة</em>{e(gate)}</div>')
    o.append('<span class="cnr tl"></span><span class="cnr tr"></span></div>')
    if g in SHEET_HIFZ:
        o.append(f'<div class="cphifz">المحفوظ هذا العام — <b>{SHEET_HIFZ[g]}</b></div>')
    o.append(class_card(g))
    o.append(alloc_tables(g))
    o.append(term_rota(g))
    # what to open: the prescribed text for each subject taught this year
    rows = []
    for sub in sorted(T[g], key=lambda x: (T[g][x][0] not in ('مستقل', 'فصلي'), x)):
        t = C.src(sub, g)
        if 'RED' in t or 'لا مصدر' in t:
            rows.append((sub, '<i class="nosrc">لا نصَّ مسجَّلًا بعد</i>')); continue
        t = t.replace('**', '').strip()
        if t.startswith('—') or not t:
            continue
        rows.append((sub, e(t)))
    if rows:
        o.append('<div class="books"><h3>نصوصُ هذا الصف — ما يُفتَح في الحصّة</h3><table>')
        for sub, t in rows:
            o.append(f'<tr><th>{e(sub)}</th><td>{t}</td></tr>')
        o.append('</table></div>')
    n_ind = sum(1 for s, v in T[g].items() if v[0] in ('مستقل', 'فصلي'))
    o.append(f'<div class="cpfoot">يلقى طالبُ هذا الصف <b>{ar(len(T[g]))}</b> مادةً مسمّاة، '
             f'منها <b>{ar(n_ind)}</b> بحصّةٍ خاصّة، وسائرُها داخل مضيفٍ مسمًّى.</div>')
    o.append('</div>')
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
/* ═══════════════════════════════════════════════════════════════════
   SHRS CURRICULUM HANDBOOK · type & page system
   Baseline unit 4.8mm. Arabic leads; Latin supports quietly.
   Gold behaves as foil: hairlines and registration, never fill.
   ═══════════════════════════════════════════════════════════════════ */
@page{size:A4;margin:0;}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{font-family:'Amiri',serif;font-size:10.6pt;line-height:1.78;
 color:#241A11;background:#FDFBF6;direction:rtl;
 -webkit-font-feature-settings:"liga" 1,"calt" 1;
 --ink:#241A11;--brown:#3B2A1D;--esp:#1E1409;--bronze:#6B4A2E;
 --gold:#B08E4E;--gold2:#C6A15B;--champ:#E4C98A;
 --cream:#F5ECDC;--paper:#FDFBF6;--paper2:#FAF5EB;
 --line:#E0D2B8;--hair:#EDE3D1;--mute:#9A8A76;--burg:#7C1F2E;}
/* ── Latin is a quiet supporting voice, never a competitor ──────── */
.en,.lat{direction:ltr;font-family:'EB Garamond',Georgia,'Times New Roman',serif;
 font-weight:400;letter-spacing:.16em;text-transform:uppercase;
 font-size:7.1pt;color:var(--mute);}
.kufi{font-family:'Noto Kufi Arabic',sans-serif;font-weight:400;}
h1,h2,h3,h4{font-family:'Amiri',serif;font-weight:700;letter-spacing:0;}
h5,h6{font-family:'Noto Kufi Arabic',sans-serif;font-weight:400;}
p{margin:0 0 4.8mm;}
.g{color:var(--mute);}
.pg{padding:0 19mm;}
.pg>h2:first-child{padding-top:5mm;}
.brk{page-break-before:always;}
.pg.brk{padding-top:5mm;}
/* ── cover ──────────────────────────────────────────────────────── */
.cover{height:297mm;padding:0;display:flex;flex-direction:column;
 page-break-after:always;background:#3B2A1D;color:#F3E8D6;position:relative;}
.cover:before{content:'';position:absolute;top:13mm;right:13mm;left:13mm;bottom:13mm;
 border:.5pt solid rgba(196,161,91,.42);pointer-events:none;}
.cover .top{flex:1;display:flex;flex-direction:column;justify-content:flex-end;
 padding:0 26mm 0;}
.cover .rule{height:1.1pt;background:var(--gold2);width:26mm;margin:0 0 11mm;}
.cover .inst{font-family:'EB Garamond',Georgia,serif;font-size:8.2pt;letter-spacing:.3em;
 color:var(--gold2);direction:ltr;margin:0 0 3mm;text-transform:uppercase;}
.cover .instar{font-size:11.4pt;color:#D7C5A4;margin:0 0 19mm;letter-spacing:.02em;}
.cover h1{font-size:36pt;line-height:1.34;margin:0 0 6mm;color:#FFFCF6;font-weight:700;}
.cover .en2{font-family:'EB Garamond',Georgia,serif;font-size:10pt;letter-spacing:.26em;
 color:var(--gold2);direction:ltr;margin:0 0 6mm;text-transform:uppercase;}
.cover .sub{font-size:12.4pt;color:#C9B79A;margin:0 0 24mm;max-width:118mm;line-height:1.95;}
.cover .foot{background:#1E1409;padding:12mm 26mm;border-top:.5pt solid rgba(196,161,91,.4);}
.cover .foot .l1{font-size:10pt;color:var(--champ);margin:0 0 2mm;}
.cover .foot .l2{font-family:'EB Garamond',Georgia,serif;font-size:7.2pt;color:#8E7C63;
 direction:ltr;letter-spacing:.2em;text-transform:uppercase;}
/* ── imprint ────────────────────────────────────────────────────── */
.imp{padding:8mm 26mm 0;}
.imp h2{border:0;font-size:12.4pt;margin:0 0 6mm;color:var(--brown);padding:0;
 letter-spacing:.01em;}
.imp h2:before{content:'';display:block;width:16mm;height:.9pt;background:var(--gold);
 margin:0 0 3mm;}
.imp .attr{border-right:.9pt solid var(--gold);padding:4mm 6mm;background:var(--paper2);
 margin:0 0 7mm;font-size:9.6pt;line-height:1.8;}
.imp .attr .lat{display:block;font-size:7pt;margin-top:3mm;letter-spacing:.1em;
 text-transform:none;color:var(--bronze);line-height:1.6;}
.imp .status{border-top:.9pt solid var(--burg);border-bottom:.4pt solid var(--hair);
 padding:3.4mm 0 3.8mm;font-size:9.4pt;color:#4A3226;margin:0 0 7mm;line-height:1.8;}
.toc{font-size:10pt;}
.toc div{display:flex;justify-content:space-between;align-items:baseline;
 border-bottom:.35pt solid var(--hair);padding:1.7mm 0;}
.toc .t{color:var(--ink);} .toc .p{color:var(--mute);font-family:'EB Garamond',Georgia,serif;
 font-size:8pt;letter-spacing:.08em;}
.toc .pt{font-family:'Noto Kufi Arabic',sans-serif;font-size:7.6pt;color:var(--gold);
 letter-spacing:.1em;margin:5mm 0 1.2mm;border-bottom:.7pt solid var(--gold);
 padding-bottom:1.5mm;}
/* ── part opener ────────────────────────────────────────────────── */
.opener{page-break-before:always;height:240mm;display:flex;flex-direction:column;
 justify-content:center;padding:0 26mm;position:relative;}
.opener:before{content:'';position:absolute;right:0;top:34mm;bottom:34mm;width:1.6pt;
 background:var(--gold);}
.opener .pn{font-family:'EB Garamond',Georgia,serif;font-size:8pt;letter-spacing:.34em;
 color:var(--gold);direction:ltr;margin:0 0 7mm;text-transform:uppercase;}
.opener h2{font-size:30pt;color:var(--brown);border:0;margin:0 0 4mm;padding:0;
 line-height:1.3;}
.opener .ar2{font-size:14.5pt;color:var(--bronze);margin:0 0 7mm;}
.opener .en3{font-family:'EB Garamond',Georgia,serif;font-size:8pt;letter-spacing:.22em;
 color:var(--mute);direction:ltr;margin:0 0 12mm;text-transform:uppercase;}
.opener p{font-size:11.6pt;color:#3F2E20;max-width:126mm;line-height:2.02;}
.opener.p1:before{background:var(--gold);} .opener.p2:before{background:var(--bronze);}
.opener.p3:before{background:var(--burg);} .opener.p4:before{background:#A08F79;}
.opener .stat{margin-top:14mm;display:flex;gap:0;border-top:.5pt solid var(--line);
 padding-top:6mm;}
.opener .stat>div{padding-left:12mm;margin-left:12mm;border-left:.35pt solid var(--hair);}
.opener .stat>div:last-child{border-left:0;}
.opener .stat b{display:block;font-family:'Amiri',serif;font-size:23pt;
 color:var(--brown);line-height:1;margin-bottom:1.5mm;}
.opener .stat span{font-size:8pt;color:var(--mute);}
/* ── headings ───────────────────────────────────────────────────── */
h2{font-size:16pt;color:var(--brown);margin:0 0 6mm;padding:0 0 3mm;
 border-bottom:.5pt solid var(--line);position:relative;page-break-after:avoid;}
h2:after{content:'';position:absolute;bottom:-.5pt;right:0;width:22mm;height:1.4pt;
 background:var(--gold);}
h3{font-size:12.6pt;color:var(--brown);margin:9mm 0 3.5mm;page-break-after:avoid;}
h5{font-size:10.4pt;color:var(--brown);margin:6mm 0 2mm;}
h6{font-size:7.6pt;color:var(--bronze);margin:0 0 2mm;letter-spacing:.09em;}
.lead{font-size:11pt;color:#3F2E20;line-height:1.98;margin-bottom:7mm;}
/* ── journey band ───────────────────────────────────────────────── */
.journey{margin:0 0 9mm;}
.jrow{display:flex;gap:2mm;}
.jsec{flex:1;border-top:1.4pt solid var(--gold);padding-top:2.5mm;}
.jsec:nth-child(2){border-color:#A7854A;} .jsec:nth-child(3){border-color:var(--bronze);}
.jsec:nth-child(4){border-color:var(--burg);}
.jsec .nm{font-size:9.6pt;color:var(--brown);font-weight:700;font-family:'Amiri',serif;}
.jsec .en4{font-family:'EB Garamond',Georgia,serif;font-size:6.2pt;letter-spacing:.22em;
 color:var(--mute);direction:ltr;margin-bottom:2.5mm;text-transform:uppercase;}
.jsec .cells{display:flex;gap:1.2mm;}
.jsec .c{flex:1;background:var(--paper2);border-top:.35pt solid var(--hair);
 text-align:center;padding:2.6mm 0 2mm;font-family:'Amiri',serif;font-size:11pt;
 color:var(--brown);}
.jsec .c.gt{background:var(--brown);color:var(--champ);border-top-color:var(--brown);}
.jsec .gl{font-size:6pt;color:var(--champ);margin-top:1.4mm;line-height:1.35;
 font-family:'Noto Kufi Arabic',sans-serif;letter-spacing:.02em;}
/* ── the forms legend ───────────────────────────────────────────── */
.forms{width:100%;border-collapse:collapse;font-size:9.6pt;margin:0 0 6mm;}
.forms thead th{border-top:1pt solid var(--brown);border-bottom:.4pt solid var(--line);
 padding:2.4mm 3mm;font-family:'Noto Kufi Arabic',sans-serif;font-size:7.4pt;
 color:var(--bronze);font-weight:400;letter-spacing:.07em;text-align:right;}
.forms td{border-bottom:.35pt solid var(--hair);padding:2.9mm 3mm;text-align:right;
 vertical-align:top;line-height:1.65;}
.forms tbody tr:last-child td{border-bottom:.8pt solid var(--brown);}
.forms .k{width:20%;font-weight:700;color:var(--brown);white-space:nowrap;}
.forms .sw{display:inline-block;width:3mm;height:3mm;margin-left:2.4mm;
 vertical-align:-.3mm;}
/* ── glance + navigation ────────────────────────────────────────── */
.glance,.nav{width:100%;border-collapse:collapse;font-size:8.8pt;}
.glance th,.glance td,.nav th,.nav td{padding:2.7mm 2.6mm;text-align:right;
 vertical-align:top;line-height:1.66;border-bottom:.35pt solid var(--hair);}
.glance thead th,.nav thead th{border-top:1pt solid var(--brown);
 border-bottom:.5pt solid var(--brown);background:transparent;
 font-family:'Noto Kufi Arabic',sans-serif;font-size:7.2pt;color:var(--bronze);
 font-weight:400;letter-spacing:.07em;}
.nav thead th{text-align:center;}
.glance tbody tr:last-child td,.nav tbody tr:last-child td{border-bottom:.8pt solid var(--brown);}
.glance .gcell{width:9%;text-align:center;white-space:nowrap;}
.glance .gcell b{display:block;font-family:'Amiri',serif;font-size:15pt;
 color:var(--brown);line-height:1.05;}
.glance .gcell span{font-size:6.8pt;color:var(--mute);}
.glance td b{color:var(--brown);}
.glance .gl-o{color:var(--mute);}
.glance .gl-x{width:11%;color:var(--mute);font-size:8pt;}
.glance .gl-none{color:#CBBFA9;}
.glance tr.gsec td{background:transparent;border-bottom:.4pt solid var(--gold);
 border-top:.4pt solid var(--gold);color:var(--brown);font-family:'Amiri',serif;
 font-weight:700;font-size:9.4pt;padding:2.4mm 2.6mm;}
.glance tr.gsec span{color:var(--mute);font-weight:400;font-size:7.6pt;}
.nav .ng{font-family:'Amiri',serif;font-size:15pt;color:var(--brown);
 text-align:center;width:7%;font-weight:700;}
.nav .ns{color:var(--mute);font-size:8.2pt;width:12%;}
.nav td.c{text-align:center;}
.nav td b{font-family:'Amiri',serif;color:var(--brown);font-size:10.4pt;}
.nav .sl{color:#A89880;font-size:7.6pt;}
.nav .ngate{font-size:8pt;color:var(--burg);width:19%;}
/* ── class page ─────────────────────────────────────────────────── */
.cpage{page-break-before:always;padding:9mm 19mm 5mm;}
.cph{display:flex;align-items:center;gap:7mm;padding-bottom:4.5mm;margin:0 0 7mm;
 border-bottom:.5pt solid var(--line);position:relative;}
.cph:after{content:'';position:absolute;bottom:-.5pt;right:0;width:30mm;height:1.4pt;
 background:var(--gold);}
.cpn{font-family:'Amiri',serif;font-size:40pt;line-height:1;color:var(--gold2);
 font-weight:700;min-width:20mm;text-align:center;
 border-left:.35pt solid var(--hair);padding-left:6mm;}
.cpt{flex:1;}
.cpt h2{border:0;padding:0;margin:0;font-size:21pt;line-height:1.25;}
.cpt h2:after{display:none;}
.cpsec{font-size:9.4pt;color:var(--mute);margin-top:1.6mm;}
.cpsec .en{display:inline;margin-right:2mm;}
.cpgate{margin-right:auto;align-self:center;font-family:'Amiri',serif;font-size:9.6pt;
 color:var(--burg);border-top:.9pt solid var(--burg);border-bottom:.35pt solid var(--line);
 padding:1.8mm 0 1.8mm;min-width:34mm;text-align:center;}
.cphifz{border-right:.9pt solid var(--gold);padding:2.6mm 5mm;background:var(--paper2);
 font-size:10pt;margin:0 0 6mm;}
/* ── the class card — editorial architecture, not a widget ──────── */
.ccard{margin:0 0 8mm;page-break-inside:avoid;}
.ccrow{display:flex;page-break-inside:avoid;border-top:1.4pt solid var(--gold);
 border-bottom:.5pt solid var(--line);padding:5mm 0 4.5mm;margin:0 0 5mm;}
.ccbig{flex:1;text-align:center;padding:0 5mm;border-left:.35pt solid var(--hair);}
.ccbig:last-child{border-left:0;}
.ccbig b{display:block;font-family:'Amiri',serif;font-size:30pt;line-height:.96;
 color:var(--brown);font-weight:700;margin-bottom:2.6mm;}
.ccbig.alt b{color:var(--bronze);}
.ccbig span{display:block;font-size:8.4pt;color:#5A4A38;line-height:1.4;}
.ccbig i{display:block;font-family:'EB Garamond',Georgia,serif;font-style:normal;
 font-size:6pt;letter-spacing:.18em;color:#B0A18C;text-transform:uppercase;
 direction:ltr;margin-top:1.6mm;white-space:nowrap;}
.ccprog{display:flex;gap:7mm;margin:0 0 5mm;}
.ccp{flex:1;border-top:.9pt solid var(--gold);padding-top:2.6mm;}
.ccp.p2{border-color:var(--bronze);} .ccp.p3{border-color:var(--burg);}
.ccp.p4{border-color:#A08F79;} .ccp.shared{border-color:var(--hair);}
.ccp h6{margin:0 0 2mm;font-size:8pt;color:var(--brown);font-family:'Amiri',serif;
 font-weight:700;letter-spacing:0;}
.ccn{display:flex;gap:6mm;font-size:8.2pt;color:var(--mute);}
.ccn b{font-family:'Amiri',serif;font-size:13pt;color:var(--brown);
 margin-left:1.4mm;font-weight:700;}
.ccfoot{border-top:.35pt solid var(--hair);padding-top:3mm;font-size:8.8pt;
 color:#4A3B2C;line-height:2.05;}
.ccfoot b{color:var(--brown);}
.ccfoot .lb{display:inline-block;width:17mm;color:var(--mute);font-size:7.2pt;
 font-family:'Noto Kufi Arabic',sans-serif;letter-spacing:.06em;}
.ccmeth{font-size:7.8pt;color:var(--mute);line-height:1.78;margin:3.5mm 0 0;
 border-top:.35pt solid var(--hair);padding-top:2.6mm;}
/* ── academic tables — rules above and below, none between ──────── */
.alh{font-size:12.6pt;color:var(--brown);margin:0 0 4.5mm;padding:0 0 2.5mm;
 border-bottom:.5pt solid var(--line);position:relative;}
.alh:after{content:'';position:absolute;bottom:-.5pt;right:0;width:22mm;height:1.4pt;
 background:var(--gold);}
.alt{margin:0 0 6mm;page-break-inside:avoid;}
.alt h4{font-size:10.4pt;color:var(--brown);margin:0 0 2.4mm;padding-right:3.4mm;
 border-right:1.6pt solid var(--gold);line-height:1.35;}
.alt.p2 h4{border-color:var(--bronze);} .alt.p3 h4{border-color:var(--burg);}
.alt.p4 h4{border-color:#A08F79;}
.atab{width:100%;border-collapse:collapse;font-size:9pt;}
.atab thead th{background:transparent;color:var(--bronze);
 font-family:'Noto Kufi Arabic',sans-serif;font-size:7.2pt;font-weight:400;
 letter-spacing:.07em;padding:2.2mm 2.4mm;text-align:right;
 border-top:.9pt solid var(--brown);border-bottom:.4pt solid var(--line);}
.atab tbody th{text-align:right;font-family:'Amiri',serif;font-weight:700;
 color:var(--brown);width:22%;padding:2.4mm;border-bottom:.3pt solid var(--hair);}
.atab td{padding:2.4mm;border-bottom:.3pt solid var(--hair);color:#3F3225;
 vertical-align:top;line-height:1.6;}
.atab tbody tr:nth-child(even) th,.atab tbody tr:nth-child(even) td{background:#FBF7EF;}
.atab tbody tr:last-child th,.atab tbody tr:last-child td{border-bottom:.8pt solid var(--brown);}
.atab td.c{text-align:center;}
.atab td b{font-family:'Amiri',serif;font-size:10.4pt;color:var(--brown);}
.atab td i{color:var(--mute);font-style:normal;font-size:7.4pt;}
.rota{margin-top:5mm;page-break-inside:avoid;}
.rota h6{font-family:'Amiri',serif;font-weight:700;font-size:9.4pt;color:var(--brown);
 letter-spacing:0;margin-bottom:2.4mm;}
.rota table{width:100%;border-collapse:collapse;font-size:8.8pt;}
.rota th,.rota td{padding:2.2mm 2.4mm;text-align:center;
 border-bottom:.3pt solid var(--hair);}
.rota thead th{border-top:.9pt solid var(--brown);border-bottom:.4pt solid var(--line);
 color:var(--bronze);font-family:'Noto Kufi Arabic',sans-serif;font-size:7.2pt;
 font-weight:400;letter-spacing:.07em;}
.rota tbody th{color:var(--brown);font-family:'Amiri',serif;font-weight:700;}
.rota tbody tr:last-child th,.rota tbody tr:last-child td{border-bottom:.8pt solid var(--brown);}
.books{margin-top:6mm;page-break-inside:auto;}
.books h3{margin:0 0 2.8mm;font-size:10.6pt;color:var(--brown);padding-bottom:2mm;
 border-bottom:.9pt solid var(--gold);}
.books table{width:100%;border-collapse:collapse;font-size:8.8pt;}
.books tr{page-break-inside:avoid;}
.books th{width:21%;text-align:right;vertical-align:top;padding:2mm 3.4mm 2mm 0;
 color:var(--bronze);font-family:'Amiri',serif;font-weight:700;
 border-bottom:.3pt solid var(--hair);}
.books td{padding:2mm 0;color:#3F3225;border-bottom:.3pt solid var(--hair);
 line-height:1.62;}
.books tr:last-child th,.books tr:last-child td{border-bottom:.8pt solid var(--brown);}
.books .nosrc{color:var(--burg);font-style:normal;}
.cpfoot{margin-top:5mm;border-top:.35pt solid var(--hair);padding-top:3mm;
 font-size:8.8pt;color:var(--mute);}
.cpfoot b{color:var(--brown);font-family:'Amiri',serif;font-size:10pt;}
/* ── marks & flags ──────────────────────────────────────────────── */
.slist{list-style:none;margin:0;padding:0;}
.slist li{position:relative;padding-right:5.6mm;margin:0 0 2.4mm;font-size:9.8pt;}
.slist .mk{position:absolute;right:0;top:1.8mm;width:2.6mm;height:2.6mm;display:block;}
.mk.m-ind{background:var(--brown);} .mk.m-trm{background:#A7854A;}
.mk.m-mrg{background:#8A6B45;} .mk.m-emb{background:var(--gold2);}
.mk.m-unt{background:#D8BE8B;} .mk.m-rot{background:#DFCBA6;}
.mk.m-str{background:#EFE2C8;} .mk.m-q{background:#EFD6CF;}
.keyrow{display:flex;flex-wrap:wrap;gap:2.6mm 7mm;font-size:8.8pt;margin:0 0 6mm;
 border-top:.9pt solid var(--gold);border-bottom:.35pt solid var(--hair);
 padding:4mm 0 4mm;}
.keyrow span{display:flex;align-items:center;gap:2.2mm;}
.keyrow i{width:2.8mm;height:2.8mm;display:block;}
.cdr{font-family:'Noto Kufi Arabic',sans-serif;font-size:6.6pt;letter-spacing:.05em;
 color:var(--burg);border-bottom:.4pt solid #DEBFB6;padding-bottom:.3mm;
 white-space:nowrap;direction:rtl;}

/* ═══ SHRS SURFACE & ORNAMENT SYSTEM ═══════════════════════════════
   Six paper tones, one gold, one deep anchor. Every surface carries a
   different class of information — tone is meaning, not decoration.
   The ornament is a single form: the rotated lozenge (المِعيَن), used as
   registration mark, divider centre and corner. Nothing else is added.
   ════════════════════════════════════════════════════════════════ */
body{--ivory:#FAF4E9;--cream:#F3E7D2;--parch:#EBDDC2;--pcoffee:#E2D0B2;
 --panel:#332314;}
/* the lozenge — the one ornament in the system */
.loz{display:inline-block;width:2.2mm;height:2.2mm;background:var(--gold);
 transform:rotate(45deg);vertical-align:middle;margin:0 2.4mm;}
.divider{display:flex;align-items:center;gap:0;margin:7mm 0;}
.divider:before,.divider:after{content:'';flex:1;height:.4pt;background:var(--line);}
.divider i{width:2.6mm;height:2.6mm;background:var(--gold);transform:rotate(45deg);
 margin:0 3mm;display:block;}
.cnr{position:absolute;width:4.2mm;height:4.2mm;}
.cnr.tl{top:0;left:0;border-top:.9pt solid var(--gold2);border-left:.9pt solid var(--gold2);}
.cnr.tr{top:0;right:0;border-top:.9pt solid var(--gold2);border-right:.9pt solid var(--gold2);}
/* ── class page: a composed band, not a rule ─────────────────────── */
.cpband{position:relative;background:var(--panel);color:#F3E8D6;
 display:flex;align-items:center;gap:7mm;padding:6.5mm 7mm;margin:0 0 7mm;
 border-top:2pt solid var(--gold);}
.cpband .cpn{font-family:'Amiri',serif;font-size:42pt;line-height:1;color:var(--champ);
 font-weight:700;min-width:22mm;text-align:center;
 border-left:.5pt solid rgba(196,161,91,.45);padding-left:7mm;}
.cpband .cpt{flex:1;}
.cpband .cpt h2{border:0;padding:0;margin:0;font-size:22pt;color:#FFFCF6;line-height:1.25;}
.cpband .cpt h2:after{display:none;}
.cpband .cpsec{font-size:9.4pt;color:#BFAB8B;margin-top:1.8mm;}
.cpband .cpsec .en{color:#9B876A;}
.cpgate{margin-right:auto;align-self:center;text-align:center;font-family:'Amiri',serif;
 font-size:10pt;color:var(--champ);border:.5pt solid rgba(196,161,91,.55);
 padding:2.4mm 5mm;min-width:36mm;background:rgba(0,0,0,.16);}
.cpgate em{display:block;font-family:'EB Garamond',Georgia,serif;font-style:normal;
 font-size:6pt;letter-spacing:.24em;text-transform:uppercase;color:#9B876A;
 margin-bottom:1mm;direction:ltr;}
/* ── the metric family: one dominant, three graded ───────────────── */
.ccrow{display:flex;gap:3mm;border:0;padding:0;margin:0 0 6mm;}
.ccbig{flex:1;text-align:center;padding:5mm 4mm 4.5mm;border:.35pt solid var(--line);
 position:relative;}
.ccbig:before{content:'';position:absolute;top:0;right:0;left:0;height:1.4pt;
 background:var(--gold);}
.ccbig.s1{background:var(--panel);border-color:var(--panel);flex:1.18;}
.ccbig.s1:before{background:var(--champ);height:2pt;}
.ccbig.s1 b{color:var(--champ);font-size:34pt;}
.ccbig.s1 span{color:#E4D6BC;} .ccbig.s1 i{color:#9B876A;}
.ccbig.s1 em{position:absolute;top:3.4mm;left:3.4mm;width:2.2mm;height:2.2mm;
 background:var(--gold2);transform:rotate(45deg);}
.ccbig.s2{background:var(--cream);border-color:#DFCBA6;}
.ccbig.s3{background:var(--ivory);}
.ccbig.s4{background:var(--parch);border-color:#DCC9A6;}
.ccbig.s4 b{color:var(--bronze);}
.ccbig b{display:block;font-family:'Amiri',serif;font-size:29pt;line-height:.98;
 color:var(--brown);font-weight:700;margin-bottom:2.8mm;}
.ccbig span{display:block;font-size:8.4pt;color:#4A3B2C;line-height:1.4;}
.ccbig i{display:block;font-family:'EB Garamond',Georgia,serif;font-style:normal;
 font-size:5.9pt;letter-spacing:.18em;color:#A8967C;text-transform:uppercase;
 direction:ltr;margin-top:1.8mm;white-space:nowrap;}
/* ── the three programmes as academic divisions ──────────────────── */
.ccprog{display:flex;gap:3mm;margin:0 0 5mm;}
.ccp{flex:1;position:relative;padding:4mm 4mm 3.4mm 4mm;border:.35pt solid var(--line);
 background:var(--ivory);}
.ccp:before{content:'';position:absolute;top:0;right:0;left:0;height:1.6pt;
 background:var(--gold);}
.ccp.p2{background:#F6EFE2;border-color:#DDCDAF;}
.ccp.p2:before{background:var(--bronze);}
.ccp.p3{background:#F7EDE9;border-color:#E2CDC6;}
.ccp.p3:before{background:var(--burg);}
.ccp.p4{background:#F4F1EA;} .ccp.p4:before{background:#A08F79;}
.ccp.shared{background:var(--paper2);} .ccp.shared:before{background:var(--line);}
.ccp .rn{position:absolute;top:3mm;left:4mm;font-family:'EB Garamond',Georgia,serif;
 font-size:12pt;color:rgba(59,42,29,.19);direction:ltr;line-height:1;}
.ccp h6{margin:0 0 2.4mm;font-size:9.4pt;color:var(--brown);font-family:'Amiri',serif;
 font-weight:700;letter-spacing:0;}
.ccn{display:flex;gap:6mm;font-size:8.2pt;color:#6B5C48;}
.ccn b{font-family:'Amiri',serif;font-size:14pt;color:var(--brown);margin-left:1.4mm;
 font-weight:700;}
.ccfoot{border-top:.35pt solid var(--hair);border-bottom:.35pt solid var(--hair);
 padding:3.2mm 0;font-size:8.8pt;color:#4A3B2C;line-height:2.05;background:var(--paper2);
 padding-right:4mm;padding-left:4mm;}
/* ── section openings: four academic stages ──────────────────────── */
.secop{margin:0 0 7mm;page-break-inside:avoid;border:.35pt solid var(--line);
 background:var(--ivory);}
.secop.s1{background:var(--ivory);} .secop.s2{background:#F8F1E4;}
.secop.s3{background:#F5EDDE;} .secop.s4{background:#F2E8D6;}
.sob{display:flex;align-items:center;gap:6mm;background:var(--panel);color:#F3E8D6;
 padding:4.5mm 6mm;border-top:1.8pt solid var(--gold);}
.son{font-family:'Amiri',serif;font-size:26pt;color:var(--champ);line-height:1;
 font-weight:700;min-width:13mm;text-align:center;
 border-left:.5pt solid rgba(196,161,91,.42);padding-left:6mm;}
.sot{flex:1;} .sot h3{margin:0;font-size:16pt;color:#FFFCF6;}
.soe{font-size:6.4pt;letter-spacing:.24em;color:#9B876A;margin-top:1.4mm;}
.socells{display:flex;gap:1.6mm;}
.socells i{width:8mm;height:8mm;line-height:8mm;text-align:center;font-style:normal;
 font-family:'Amiri',serif;font-size:11pt;color:#E4D6BC;
 border:.5pt solid rgba(196,161,91,.4);}
.socells i.gt{background:var(--gold);color:var(--esp);border-color:var(--gold);
 font-weight:700;}
.sob2{padding:4.5mm 6mm 3.5mm;}
.soc{color:var(--bronze);font-size:10.6pt;margin:0 0 2.4mm;font-weight:700;
 font-family:'Amiri',serif;}
.sod{margin:0;font-size:10pt;line-height:1.9;}
/* ── programme openers: a division, not a heading ────────────────── */
.opener{background:transparent;}
.opener.p1,.opener.p2,.opener.p3,.opener.p4{padding:0 26mm;}
.opener .pmark{position:absolute;top:30mm;right:26mm;font-family:'EB Garamond',Georgia,serif;
 font-size:74pt;color:rgba(59,42,29,.055);direction:ltr;line-height:1;}
.opener .ornrow{display:flex;align-items:center;margin:0 0 9mm;}
.opener .ornrow:before{content:'';flex:0 0 22mm;height:1.4pt;background:var(--gold);}
.opener .ornrow i{width:2.6mm;height:2.6mm;background:var(--gold);transform:rotate(45deg);
 margin:0 3mm;display:block;}
.opener .ornrow:after{content:'';flex:1;height:.4pt;background:var(--line);}
/* ── lifeline & subject cards ───────────────────────────────────── */
.ll{display:flex;gap:1mm;margin:2mm 0 2.4mm;}
.ll i{flex:1;height:4.6mm;display:block;}
.ll .b0{background:#F3EFE6;}
.ll .ind{background:var(--brown);} .ll .trm{background:#A7854A;}
.ll .mrg{background:#8A6B45;} .ll .emb{background:var(--gold2);}
.ll .unt{background:#D8BE8B;} .ll .rot{background:#DFCBA6;}
.ll .str{background:#EFE2C8;}
.ll .bq{background:#EFD6CF;color:var(--burg);font-size:6.6pt;text-align:center;
 line-height:4.6mm;font-style:normal;font-family:'Amiri',serif;}
.phs{font-size:8.2pt;color:#5A4A38;margin:0 0 2.4mm;line-height:2;}
.ph{border-bottom:.35pt solid var(--hair);padding:0 1.4mm .6mm;white-space:nowrap;}
.ph b{color:var(--brown);font-family:'Amiri',serif;font-size:8.4pt;}
.ph.ph-warn{border-bottom-color:#DEBFB6;color:var(--burg);}
.hh{color:var(--mute);}
.cards{column-count:2;column-gap:9mm;}
.card{break-inside:avoid;page-break-inside:avoid;border-top:.9pt solid var(--brown);
 padding:2.8mm 0 4mm;margin:0 0 5mm;}
.p1 .card{border-color:var(--gold);} .p2 .card{border-color:var(--bronze);}
.p3 .card{border-color:var(--burg);} .p4 .card{border-color:#A08F79;}
.ct{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.6mm;}
.ct h4{font-size:11.4pt;color:var(--brown);margin:0;}
.span{font-size:7.2pt;color:var(--mute);white-space:nowrap;}
.span b{font-family:'Amiri',serif;color:var(--bronze);font-size:9.4pt;margin-right:2mm;}
.card dl{margin:0;display:grid;grid-template-columns:16% 84%;gap:.8mm 0;font-size:9pt;}
.card dt{color:var(--mute);font-size:7.2pt;font-family:'Noto Kufi Arabic',sans-serif;
 letter-spacing:.05em;padding-top:.9mm;}
.card dd{margin:0;line-height:1.6;}
.card dd.warn{color:var(--burg);}
/* ── texts, rules, open items ───────────────────────────────────── */
.txt{width:100%;border-collapse:collapse;font-size:9.2pt;}
.txt th,.txt td{border-bottom:.3pt solid var(--hair);padding:2.4mm 2.6mm;text-align:right;}
.txt thead th{border-top:.9pt solid var(--brown);border-bottom:.4pt solid var(--line);
 font-family:'Noto Kufi Arabic',sans-serif;font-size:7.2pt;color:var(--bronze);
 font-weight:400;letter-spacing:.07em;}
.txt tbody tr:last-child td{border-bottom:.8pt solid var(--brown);}
.txt .gr{font-family:'Amiri',serif;color:var(--brown);white-space:nowrap;width:12%;
 font-weight:700;}
.txt .kd{color:var(--mute);font-size:8pt;width:17%;}
.txt tr.sec td{border-top:.4pt solid var(--gold);border-bottom:.4pt solid var(--gold);
 background:transparent;font-family:'Amiri',serif;font-weight:700;font-size:9.4pt;
 color:var(--brown);padding:2.4mm 2.6mm;}
.rules{margin:0;padding:0;list-style:none;counter-reset:r;}
.rules li{counter-increment:r;position:relative;padding-right:12mm;margin:0 0 5.4mm;
 font-size:10.2pt;page-break-inside:avoid;line-height:1.85;}
.rules li:before{content:counter(r);position:absolute;right:0;top:-.6mm;
 font-family:'Amiri',serif;font-size:15pt;color:var(--gold2);font-weight:700;}
.rules b{color:var(--brown);}
.open{width:100%;border-collapse:collapse;font-size:9.4pt;margin-top:4mm;}
.open th,.open td{border-bottom:.3pt solid var(--hair);padding:2.8mm 2.6mm;
 text-align:right;vertical-align:top;line-height:1.7;}
.open thead th{border-top:.9pt solid var(--brown);border-bottom:.4pt solid var(--line);
 font-size:7.2pt;color:var(--bronze);font-family:'Noto Kufi Arabic',sans-serif;
 font-weight:400;letter-spacing:.07em;}
.open tbody tr:last-child td{border-bottom:.8pt solid var(--brown);}
.open .w{width:31%;color:var(--brown);font-weight:700;}
.colo{margin-top:11mm;border-top:.9pt solid var(--gold);padding-top:4.5mm;
 font-size:8.4pt;color:var(--mute);line-height:1.85;}
.cls{border-top:.9pt solid var(--brown);padding:3.4mm 0 4.5mm;margin:0 0 6mm;
 page-break-inside:avoid;}
.clsh{display:flex;align-items:baseline;gap:5mm;margin:0 0 3mm;}
.clsh h3{margin:0;font-size:13pt;}
.cn{font-family:'Amiri',serif;font-size:21pt;color:var(--gold2);line-height:1;font-weight:700;}
.csec{margin-right:auto;font-size:8.4pt;color:var(--mute);}
"""


def build():
    o = io.StringIO(); w = o.write
    w('<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8">'
      '<title>مدارس السلطان حنفي الملكية — دليل المنهج العربي والإسلامي</title>'
      f'<style>{CSS}</style></head><body>')

    # ═══ COVER ═══
    w('<div class="cover"><div class="top"><div class="rule"></div>'
      '<div class="inst">SULTAN HANAFI ROYAL SCHOOLS</div>'
      '<div class="instar">مدارس السلطان حنفي الملكية<br>'
      '<span style="font-size:9.6pt;color:#B29C7C">قسم الدراسات الإسلامية والعربية</span></div>'
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
    w('<div class="pt">الباب الأول · بنيةُ المنهج</div>')
    for t in ['الرحلةُ في اثني عشر صفًّا','كيف تُقرأ هذه الوثيقة — الصيغُ الستّ',
              'الأقسامُ الأربعة']:
        w(f'<div><span class="t">{t}</span><span class="p">—</span></div>')
    w('<div class="pt">الباب الثاني · ما يُدرَّس في كل صف — المنظرُ الأول</div>')
    w('<div><span class="t"><b>المنهجُ كلُّه في صفحة واحدة</b> — الصفوف ١–١٢</span>'
      '<span class="p">جدول</span></div>')
    w('<div><span class="t">لوحةُ التنقّل — الصفوف الاثنا عشر</span>'
      '<span class="p">جدول</span></div>')
    w('<div><span class="t">صفحةُ كلِّ صفٍّ على حدة — من الأول إلى الثاني عشر</span>'
      f'<span class="p">{ar(12)} صفحة</span></div>')
    w('<div class="pt">الأبواب الثالث والرابع والخامس · رحلةُ كلِّ مادة</div>')
    for key, pn, pt, pen, cls, num, blurb in PROGS[:3]:
        w(f'<div><span class="t">{pt} — بطاقاتُ المواد</span>'
          f'<span class="p">{ar(len(SUBS_OF[key]))} مادة</span></div>')
    w('<div class="pt">الأبواب الختامية</div>')
    for t in ['مواضعُ المتون','قواعدُ لازمة · وما هو موقوف']:
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
    for idx, (name, en, char, gs, desc) in enumerate(SECTIONS, 1):
        gate_cells = ''.join(
            f'<i class="{"gt" if any(x==c for x,_ in GATES) else ""}">{ar(c)}</i>' for c in gs)
        w(f'<div class="secop s{idx}"><div class="sob">'
          f'<span class="son">{ar(idx)}</span>'
          f'<div class="sot"><h3>{name}</h3>'
          f'<div class="soe en">{en} &middot; GRADES {gs[0]}&ndash;{gs[-1]}</div></div>'
          f'<div class="socells">{gate_cells}</div></div>'
          f'<div class="sob2"><p class="soc">{char}</p><p class="sod">{desc}</p></div></div>')
    w('</div>')


    # ═══ PART TWO · VIEW 1 — CLASS → WHAT IS TAUGHT ═══
    w('<div class="opener"><div class="pn">PART TWO</div>'
      '<h2>ما يُدرَّس في كل صف</h2><div class="ar2">المنظرُ الأول، وأسرعُ جواب</div>'
      '<div class="en3">WHAT IS TAUGHT IN EACH CLASS</div>'
      '<p>هذا البابُ يجيب سؤالًا واحدًا في ثوانٍ: <b>ماذا أُدرِّس في صفّي؟</b> '
      'جدولٌ جامعٌ يضع المنهجَ كلَّه في صفحةٍ واحدة، ثم صفحةٌ كاملةٌ لكلِّ صفٍّ على حدة. '
      'ومن أراد رحلةَ مادةٍ بعينها عبر الصفوف فبابُها بعدَ هذا.</p>'
      '<div class="stat"><div><b>١٢</b><span>صفحة صف</span></div>'
      '<div><b>٣</b><span>برامج في كل صفحة</span></div>'
      '<div><b>٠</b><span>رمزٍ يحتاج فكًّا</span></div></div></div>')

    w('<div class="pg brk"><h2>لوحةُ التنقّل — الصفوف الاثنا عشر</h2>'
      '<p class="lead">صفحةُ الملاحة. كلُّ صفٍّ بعددِ مجالاته وحصصه، ونصيبِ كلِّ برنامجٍ منه، '
      'وبوابتِه إن كانت له. والرقمُ الأول في خانة البرنامج عددُ المجالات، '
      'والثاني بعد الشَّرطة عددُ الحصص الخاصّة به.</p>')
    w(nav_table())
    w('<p class="ccmeth" style="margin-top:4mm">حصصُ الأسبوع ١٣ في الصفوف ١–٦ و١٩ في '
      '٧–١٢ — وهو عددٌ مقفل. وقد تقلّ جملةُ حصص البرامج الثلاثة عن هذا العدد في الصفوف '
      'التي فيها <b>خانات فصلية مشتركة</b>، لأنّ الخانة المشتركة تتناوبها مقرَّرات من '
      'أكثر من برنامج فلا تُنسَب إلى واحدٍ منها. '
      'وكذلك في <b>الصف الثاني عشر</b>، حيث تأخذ خدماتُ سنة التتويج ثلاثَ حصصٍ '
      '(WAEC والتحرير الامتحاني) خارج البرامج الثلاثة — وهي مبيَّنةٌ في صفحة الصف. '
      'وجملةُ ما في كل صف تستوفي العددَ المقفل تمامًا.</p>')
    w('</div>')
    w('<div class="pg brk"><h2>المنهجُ كلُّه في صفحةٍ واحدة</h2>'
      '<p class="lead">الأسماءُ <b>الغامقة</b> موادُّ لها حصّةٌ خاصّة في الجدول. '
      'والأسماءُ الفاتحة تُدرَّس داخل مادةٍ أخرى مسمّاة — وهي منهجٌ حقيقيّ يُدرَّس '
      'ويُقوَّم، لا إضافةٌ اختيارية.</p>')
    w(glance_table())
    w('</div>')

    w('<div class="pg brk"><h2>صفحةُ الصف — كيف تُقرأ</h2>'
      '<p class="lead">كلُّ صفٍّ في صفحةٍ واحدة، وبرامجُه الثلاثة في ثلاثة أعمدة. '
      'وأمام كلِّ مادةٍ مربّعٌ صغير يقول كيف تُدرَّس:</p>'
      '<div class="keyrow">'
      '<span><i class="m-ind"></i> <b>مستقلّ</b> — حصّة وكتاب وورقة</span>'
      '<span><i class="m-trm"></i> مقرَّر فصليّ — فصلٌ واحد</span>'
      '<span><i class="m-mrg"></i> مدمج — في ورقة الشريك</span>'
      '<span><i class="m-emb"></i> مضمّن — داخل مضيفه</span>'
      '<span><i class="m-unt"></i> وحدة</span>'
      '<span><i class="m-rot"></i> دوراني</span>'
      '<span><i class="m-str"></i> مسار — خيطٌ في كتاب</span>'
      '<span><i class="m-q"></i> لم تُصرَّح صيغتُه — يُعرَض على المجلس</span>'
      '</div>'
      '<p class="g" style="font-size:9.2pt">والمادةُ التي لا تظهر في صفحة صفٍّ '
      '<b>لا تُدرَّس فيه</b>. وما ظهر بمربّعٍ فاتحٍ ومعه «← اسمُ مادة» فهو يُدرَّس '
      'داخل حصص تلك المادة، ومعلّمُها مسؤولٌ عنه.</p></div>')

    for g in range(1, 13):
        w(class_full(g))

    # ═══ PROGRAMME PARTS ═══
    for key, pn, pt, pen, cls, num, blurb in PROGS:
        subs = SUBS_OF[key]
        if not subs:
            continue
        ind = len({s for s in subs if any(T[g].get(s, (None,))[0] == 'مستقل' for g in range(1, 13))})
        w(f'<div class="opener {cls}"><div class="pmark">{num}</div>'
          f'<div class="pn">PROGRAMME {num}</div>'
          f'<h2>{pt}</h2><div class="ar2">{pn}</div>'
          f'<div class="en3">{pen}</div>'
          '<div class="ornrow"><i></i></div>'
          f'<p>{blurb}</p>'
          f'<div class="stat"><div><b>{ar(len(subs))}</b><span>مادة</span></div>'
          f'<div><b>{ar(ind)}</b><span>تستقلّ بورقة</span></div>'
          f'<div><b>{ar(min(FIRST[s] for s in subs))}–{ar(max(LAST[s] for s in subs))}</b>'
          '<span>مدى الصفوف</span></div></div></div>')
        w(f'<div class="pg brk {cls}"><h2>{e(pt)} — رحلةُ كلِّ مادة</h2>'
          '<p class="lead">البابُ الثاني أجاب: «ماذا أُدرِّس في صفّي؟» '
          'وهذا يجيب عكسَه: <b>«أُدرِّس هذه المادة — فأين تقع في الرحلة؟»</b> '
          'كلُّ شريطٍ رحلةُ مادةٍ من أول صفٍّ تلقاه فيه إلى آخره، '
          'وتغيُّرُ اللون تغيُّرٌ في صيغة التدريس لا في المادة.</p>'
          '<div class="cards">')
        for s in subs:
            w(subject_card(s))
        w('</div></div>')

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
