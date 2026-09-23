# -*- coding: utf-8 -*-
"""المصدر الواحد · the single definition shared by verify.py and gen-allocation.py

Everything in this file used to exist TWICE — once in the verifier and once in
the generator — and the two copies drifted apart. That drift is what let
`verify.py` report a clean run while the published document carried ten
`[RED — لا مصدر مُسجَّل]` markers, and what let L-19 pass while its line
vanished from the certificate.

Rule of this module: a fact lives here once, or it does not live at all.
Nothing here is a curriculum decision. Every prescribed text carries the title
as the register spells it, and `verify.py` proves that title is in the register
on every run. A text that cannot be traced to 00-LOCKED-DECISIONS.md is listed
in UNSOURCED with its reason — it is never invented here.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'allocation-v11.json'), encoding='utf-8'))
REG = open(os.path.join(HERE, '00-LOCKED-DECISIONS.md'), encoding='utf-8').read()

GRADES = [str(g) for g in range(1, 13)]
CEIL = {g: (13 if int(g) <= 6 else 19) for g in GRADES}

# ── L-08 · the closed vocabulary of instructional forms ────────────────────
# شرط is an assessment category, not a teaching form: it never carries a mark.
FORMS = ('مستقل', 'مدمج', 'مضمّن', 'وحدة', 'دوراني', 'مسار')
ASSESS_ONLY = ('شرط',)

# ── L-03 · three programmes, and nothing outside them ──────────────────────
PROGRAMMES = ('القرآن', 'اللغة', 'الإسلامية')
# التتويج is present in the data as a fourth programme. L-03 fixes three and
# L-04 admits no subject outside them. This is NOT resolved here — verify.py
# reports it as a contradiction awaiting the Chairman's ruling.
PROG_IN_DATA = PROGRAMMES + ('التتويج',)


def clean(name):
    """The lookup key for a subject. Display names keep their own spelling."""
    n = name.replace('*', '').strip()
    if n.startswith('كتاب اللغة'):
        return 'اللغة العربية'
    if n.startswith('كتاب الدراسات'):
        return 'التربية الإسلامية'
    if n == 'الفرائض التطبيقية':
        return 'الفرائض'          # L-19: one ring-fenced door, two spellings
    return n


def display(name):
    n = name.replace('*', '').strip()
    if n.startswith('كتاب اللغة'):
        return 'اللغة العربية'
    if n.startswith('كتاب الدراسات'):
        return 'التربية الإسلامية'
    return n


# ── الساعة القرآنية ────────────────────────────────────────────────────────
# These two figures govern the most protected hour in the school and appear
# NOWHERE in 00-LOCKED-DECISIONS.md nor in allocation-v11.json. They were
# hand-typed into the generator. They are held here so there is one copy, and
# verify.py prints them every run as undeclared until the register carries them.
QURAN_HOUR = {'lower': 290, 'upper': 340}
QURAN_HOUR_DECLARED = False


def quran_minutes(g):
    return QURAN_HOUR['lower'] if int(g) <= 6 else QURAN_HOUR['upper']


# ── the prescribed source per subject, grade-aware ─────────────────────────
# Every **bold title** below must be findable in 00-LOCKED-DECISIONS.md.
# verify.py enforces that. Descriptive entries naming no book are exempt.
def rng(lo, hi, txt):
    return (lo, hi, txt)


SRC = {
 'حفظ القرآن الكريم': [rng(1, 12, '**المصحف — مطبعة الملك فهد، رواية حفص عن عاصم** · **كتاب القرآن وعلومه** (المدرسة)')],
 'التجويد': [rng(1, 3, 'بلا متن — تلقينًا'),
             rng(4, 5, '**تحفة الأطفال والغلمان** — الجمزوري · فتح الأقفال (للمعلم)'),
             rng(6, 9, '**المقدمة الجزرية** — ابن الجزري · الملخص المفيد — معبد · هداية القاري (للمعلم)'),
             rng(10, 11, '**ورقة الإتقان والإقراء** (المدرسة) · هداية القاري'),
             rng(12, 12, 'صيانة — بلا متن')],
 'التفسير': [rng(1, 6, '**المختصر في تفسير القرآن** — مركز تفسير *(مادة المعلم؛ لا متن بيد الطفل)*'),
             rng(7, 9, '**التفسير الميسر** — مجمع الملك فهد'),
             rng(10, 12, '**تيسير الكريم الرحمن** — السعدي · ابن كثير *(مقاطع)* · القرطبي ١١–١٢ · الطبري (للمعلم)')],
 'أصول التفسير': [rng(9, 9, '**مباحث في علوم القرآن** — مناع القطان *(مادة المعلم؛ لا متن، عمدًا)*'),
                  rng(10, 12, '**مقدمة في أصول التفسير** — ابن تيمية')],
 'اللغة العربية': [rng(1, 3, '**مفتاح البيان** (مواد المدرسة) — ٣٣ أسبوعًا ببواباته'),
                   rng(4, 6, 'كتاب اللغة وعلومها (المدرسة) · **النحو الواضح** — الجارم وأمين *(تدريبات)*'),
                   rng(7, 12, '**جامع الدروس العربية** — الغلاييني *(مرجع)* · مواد المدرسة')],
 # Chairman's ruling, 14 Sep 2026: القراءة والتهجي has its own matn.
 'القراءة والتهجي': [rng(1, 3, '**نور البيان** — المتن المعتمد لفكِّ الحرف والتهجّي (المدرسة)')],
 'الخط والإملاء': [rng(1, 6, '**كراسة النسخ والرقعة** (المدرسة) · **قواعد الإملاء** — عبد السلام هارون')],
 'قواعد اللغة الوظيفية': [rng(4, 6, '**مواد استقرائية** (المدرسة) — القاعدة تُلمس في النص. *لا متن، عمدًا* · تدريبات من النحو الواضح')],
 'النشيد والمحفوظات': [rng(1, 5, 'مواد المدرسة'),
                       rng(6, 12, '**ديوان الشافعي · لامية ابن الوردي · تائية الإلبيري** · ملحة الإعراب ٧–٨ *(محفوظات لا متن تدريس)* · نظم الورقات · البيقونية · الرحبية')],
 # L-39 split this ladder in two. The key used to be البحث والخطابة for 4–9,
 # which matched no subject in the data after the rename — six [RED] markers.
 'الإنشاء والتعبير': [rng(4, 9, '**دليل الإنشاء والخطابة** (المدرسة)')],
 'البحث والخطابة': [rng(10, 12, '**دليل الإنشاء والخطابة** (المدرسة) · **جواهر الأدب** — أحمد الهاشمي')],
 'النحو': [rng(7, 7, '**المقدمة الآجرومية** — ابن آجروم · النحو الواضح *(تدريبات)*'),
           rng(8, 9, '**قطر الندى وبل الصدى** — ابن هشام'),
           rng(10, 12, '**ألفية ابن مالك** *(المقاطع المقررة)* · شرح ابن عقيل (للمعلم)')],
 'الصرف': [rng(7, 7, 'مضمّن في كتاب النحو — الميزان والمشتقات'),
           rng(8, 12, '**لامية الأفعال** — ابن مالك · شرح بحرق (للمعلم). *متن البناء مرفوض*')],
 'البلاغة': [rng(9, 9, '— *(لا يُفتَح قبل العاشر — L-34)*'),
             rng(10, 10, '**البلاغة الواضحة** — الجارم وأمين'),
             rng(11, 12, '**الجوهر المكنون** — الأخضري · جواهر البلاغة — الهاشمي *(مرجع)* · **دلائل الإعجاز** — الجرجاني *(مقاطع، ١٢)*')],
 'العروض وعلم القافية': [rng(9, 12, 'مواد المدرسة داخل قناة المحفوظات والبلاغة')],
 'النقد والآداب': [rng(9, 12, 'نصوص مختارة (المدرسة) · **جواهر الأدب** — الهاشمي')],
 'فقه اللغة والمعاجم': [rng(8, 8, '**دورة المعاجم** (المدرسة) · لسان العرب والقاموس المحيط *(تدريب)*')],
 'التربية الإسلامية': [rng(1, 8, '**كتاب الدراسات الإسلامية** (المدرسة) — يضم المسارات؛ ومنه **المقدمة الأخضرية** في السادس')],
 'الفقه': [rng(1, 5, 'مسار داخل كتاب الدراسات الإسلامية'),
           rng(6, 7, '**المقدمة الأخضرية** — الأخضري *(الإطار مالكي مُعلَن)*'),
           rng(8, 8, '**الرسالة** — ابن أبي زيد · **متن الغاية والتقريب** — أبو شجاع *(النظير المقارن الأول)*'),
           rng(9, 9, '**الرسالة** · **عمدة الفقه** — ابن قدامة *(نظير)*'),
           rng(10, 10, '**مختصر القدوري** *(نظير حنفي)* · **المرشد المعين** — ابن عاشر *(يُقرأ وثيقةً)* · الزحيلي (للمعلم)'),
           rng(11, 12, '**بداية المجتهد** — ابن رشد *(متن المقارنة)* · إحياء السنة — ابن فودي ١١ · *مختصر خليل مرفوض متنًا*')],
 'أصول الفقه': [rng(8, 9, 'تأصيل عملي داخل الفقه — بلا دلالات'),
                rng(10, 11, '**الورقات** — الجويني · نظم الورقات — العمريطي *(محفوظ، ١١)* · خلاف (للمعلم)'),
                rng(12, 12, '**مقاصد الشريعة** — ابن عاشور · الموافقات *(مقاطع)* · القواعد — الزرقا · **مجلة الأحكام العدلية ١–٩٩**')],
 # القول السديد and كشف الشبهات are prescribed in the register and were absent
 # from this map entirely, so ʿaqīdah reached the teacher with no reference pack.
 'العقيدة': [rng(7, 7, '**متن الأدلة** (المدرسة) *(بلا مذهب، عمدًا)* · **الأصول الثلاثة** · **كشف الشبهات** (للمعلم)'),
             rng(8, 8, '**لمعة الاعتقاد** — ابن قدامة *(يُعلَن حنبليًّا)* · القواعد الأربع · **كشف الشبهات** (للمعلم)'),
             rng(9, 9, '**العقيدة الطحاوية** — الإلهيات · **كشف الشبهات** (للمعلم)'),
             rng(10, 10, '**أم البراهين** — السنوسي · **الواسطية** — ابن تيمية · نواقض الإسلام *(بعد الموانع)* · **كشف الشبهات** (للمعلم)'),
             rng(11, 11, '**الاعتصام** — الشاطبي *(مقاطع)* · كتاب التوحيد *(وحدة محدودة)* · **كتاب الفِرَق** (المدرسة) · **القول السديد** — السعدي (للمعلم) · **كشف الشبهات** (للمعلم)'),
             rng(12, 12, '**العقيدة الطحاوية** تمامًا · **كشف الشبهات** (للمعلم)')],
 'التوحيد': [rng(1, 6, 'مسار داخل كتاب الدراسات الإسلامية'),
             rng(7, 12, 'باب مسمّى داخل العقيدة')],
 # الأدب المفرد is 7–9 in the register — it is the text of التربية الإسلامية
 # merged into الحديث at 7 and 8 — and the map began it at 8.
 # شرح معاني الآثار is 11–12 in the register, not 10–11.
 'الحديث النبوي': [rng(1, 6, 'مسار داخل كتاب الدراسات الإسلامية'),
                   rng(7, 7, '**الأربعون النووية** + **زيادات ابن رجب** · **الأدب المفرد** *(مختارات — خيط الأخلاق، بقسم مسمّى)*'),
                   rng(8, 9, '**عمدة الأحكام** — المقدسي · **الأدب المفرد** *(مختارات)*'),
                   rng(10, 10, '**بلوغ المرام** — ابن حجر · **الموطأ**'),
                   rng(11, 11, '**بلوغ المرام** — ابن حجر · الشمائل · **شرح معاني الآثار** — الطحاوي'),
                   rng(12, 12, '**البخاري ومسلم** *(كتب مختارة)* · **جامع العلوم والحكم** — ابن رجب · **شرح معاني الآثار** — الطحاوي')],
 # الرفع والتكميل is 11–12 in the register, not 10–12.
 'مصطلح الحديث': [rng(9, 9, '**البيقونية** — محفوظة'),
                  rng(10, 10, '**نخبة الفكر ونزهة النظر** — ابن حجر'),
                  rng(11, 12, '**نخبة الفكر ونزهة النظر** — ابن حجر · **الرفع والتكميل** — اللكنوي *(مرجع)*')],
 'السيرة النبوية': [rng(1, 5, 'مسار داخل كتاب الدراسات الإسلامية')],
 'التاريخ والسيرة': [rng(6, 8, '**الرحيق المختوم** — المباركفوري'),
                     rng(9, 9, '**نسيم الصبا** — الشيخ آدم الإلوري *(علماء أرضه)*'),
                     rng(10, 10, '**الإسلام في نيجيريا وعثمان بن فوديو** — الإلوري'),
                     rng(11, 12, '**إنفاق الميسور** — محمد بلّو *(مرجع)* · كتاب الفِرَق')],
 'الفرائض': [rng(11, 11, '**متن الرحبية** — الرحبي *(محفوظ، شافعي مُعلَن)* · شرح سبط المارديني *(تُحقَّق الطبعة)*'),
             rng(12, 12, '**كراسة التركات النيجيرية** (المدرسة) — *تُراجَع موادها القانونية بمحامٍ نيجيري*')],
 'الدراسات الحديثة': [rng(12, 12, '**كراسة النوازل** (المدرسة) · فقه النوازل — الجيزاني (للمعلم)')],
 'علم الكلام': [rng(12, 12, 'الإبانة ومقالات الإسلاميين — الأشعري · الماتريدي *(مقطع)* · إلجام العوام — الغزالي · تحريم النظر — ابن قدامة · درء التعارض *(مقدمته)* · جوهرة التوحيد *(وثيقةً)*')],
 'المنطق': [rng(12, 12, '**السلم المنورق** — الأخضري')],
 'خدمة التتويج': [rng(12, 12, '**دليل المشروع وملفه** (المدرسة) — الاقتراح · الأذونات · السجل · الأثر · شهادة المستفيد')],
 'WAEC': [rng(12, 12, 'مناهج WAEC — الدراسات الإسلامية والعربية')],
 'التحرير الامتحاني': [rng(12, 12, '**كراسة التحرير** (المدرسة) — قراءة الرأس · الزمن · ألفاظ الأمر · البناء')],
}

# ── what the register genuinely does not carry ─────────────────────────────
# These are NOT invented here. Each is a real gap that only the Director
# General can close, and the generated documents say so in place of a source.
UNSOURCED = {
 'الترجمة': (7, 12,
    'لا نصَّ لها في السجل — و**اللغةُ الهدفُ غيرُ مسمّاة بقرار رئيس المدارس** '
    '(قد تكون الإنجليزية أو الهوسا أو الأردية أو اليوربا). '
    'وL-18 وL-38 ما زالا يكتبان «إلى اليوربا» فيحتاجان تحريرًا'),
 'اللغة العربية · كتاب البرنامج الثاني': (4, 6,
    '«كتاب اللغة وعلومها» مُعتمَدٌ في بيانات التوزيع وليس له مدخلٌ في أبواب '
    'النصوص — والبرنامجان الأول والثالث لكلٍّ كتابُه المسمّى في السجل'),
}


def src(sub, g):
    """The prescribed source, or an honest marker saying why there is none."""
    key = clean(sub)
    for lo, hi, t in SRC.get(key, []):
        if lo <= g <= hi:
            return t
    if key in UNSOURCED:
        lo, hi, why = UNSOURCED[key]
        if lo <= g <= hi:
            return f'**[لا مصدر مُسجَّل]** — {why}'
    return '**[RED — لا مصدر مُسجَّل]**'


def named_books(text):
    """The bold titles a source entry claims. Each must be in the register."""
    out = []
    for t in re.findall(r'\*\*(.+?)\*\*', text or ''):
        t = re.sub(r'\s*\*?\([^)]*\)\*?', '', t.strip().strip('·')).strip()
        if t and not t.startswith('[') and t != 'مواد استقرائية':
            out.append(t)
    return out


# ── subject-specific gate / condition links ────────────────────────────────
SGATE = {
 'حفظ القرآن الكريم': '**الثانوية القرآنية (١١)** — اثنا عشر جزءًا متقنة، وخمسة عشر مرتبةَ امتياز',
 'القراءة والتهجي': '**بوابة القراءة (١)** ثم **بوابة الطلاقة (٣)** — وبوابته تُقوَّم على حدة',
 'قواعد اللغة الوظيفية': '**بوابة الجسر (٦)** — بلجنة ثلاثية',
 'التجويد': 'يُمتحن أمام لجنة **الثانوية القرآنية (١١)**',
 'الفرائض': '**سطر مستقل في الشهادة** — باب مُصان (L-19)',
 'خدمة التتويج': '**شرط استلام شهادة التخرج** — إشراف لا تدريس. لا درجة',
 'WAEC': '**شرط: إثبات الجلوس** لشهادة التخرج',
 'البحث والخطابة': 'المناقشة (المناظرة) في **شهادة التخرج (١٢)**',
 'التربية الإسلامية': 'يحمل المسارات الأربعة — ملحق وصفي بلا رقم في ١–٢',
}


# ── readers over the allocation, used by both scripts ──────────────────────
def cornerstones(g):
    return D[str(g)][0]


def term_slots(g):
    return D[str(g)][1]


def hosted(g):
    return D[str(g)][2]


def subject_grades():
    """{subject: sorted grades} over every form of appearance."""
    out = {}
    for g in GRADES:
        corner, slots, host = D[g]
        for x in corner:
            out.setdefault(clean(x[0]), set()).add(int(g))
        for sl in slots:
            for t in sl[2]:
                out.setdefault(clean(t[2]), set()).add(int(g))
        for x in host:
            out.setdefault(clean(x[0]), set()).add(int(g))
    return {k: sorted(v) for k, v in out.items()}


def books(g):
    """L-31, stated once: the Qurʾān book + one per independent annual subject
    + one folder for all the term courses. Merged and embedded carry none, and
    the muṣḥaf is a root, not a counted book."""
    corner, slots, _ = D[str(g)]
    return 1 + len([x for x in corner if clean(x[0]) != 'التجويد']) + (1 if slots else 0)


# L-05 · the strands of كتاب الدراسات الإسلامية. At class six السيرة is no
# longer a strand — it has become the named subject التاريخ والسيرة — so the
# sixth class carries three, not four. This lived only in the generator, and
# the two scripts counted class six differently because of it.
STRANDS = {g: ['التوحيد', 'الفقه', 'الحديث النبوي', 'السيرة النبوية']
           for g in range(1, 6)}
STRANDS[6] = ['التوحيد', 'الفقه', 'الحديث النبوي']


def sciences(g):
    """Distinct named sciences a class meets, in any form."""
    corner, slots, host = D[str(g)]
    s = {clean(x[0]) for x in corner} | {clean(x[0]) for x in host}
    s |= {clean(t[2]) for sl in slots for t in sl[2]}
    s.add('حفظ القرآن الكريم')
    s |= set(STRANDS.get(int(g), []))
    return s
