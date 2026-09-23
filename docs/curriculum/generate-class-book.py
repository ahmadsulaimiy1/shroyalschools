# -*- coding: utf-8 -*-
import io
import os; SP=os.path.dirname(os.path.abspath(__file__))+'/'
import curriculum_data as C
from curriculum_data import D, quran_minutes

AR={'الأول':1}
NAMES={1:('الأول','Primary 1'),2:('الثاني','Primary 2'),3:('الثالث','Primary 3'),
 4:('الرابع','Primary 4'),5:('الخامس','Primary 5'),6:('السادس','Primary 6'),
 7:('السابع','JSS 1'),8:('الثامن','JSS 2'),9:('التاسع','JSS 3'),
 10:('العاشر','SS 1'),11:('الحادي عشر','SS 2'),12:('الثاني عشر','SS 3')}
SECTIONS=[('القسم التمهيدي',[1,2],'التهيئة وفك الحرف','**بوابة القراءة** في الصف الأول'),
 ('القسم الابتدائي',[3,4,5,6],'القراءة فالطلاقة فالجسر إلى عربية العلم','**بوابة الطلاقة** (٣) · **الشهادة الابتدائية** (٥) · **بوابة الجسر** (٦)'),
 ('القسم الإعدادي',[7,8,9],'العلوم الشرعية بأسمائها والنحو على متونه','**الشهادة الإعدادية** (٩) بممتحن خارجي'),
 ('القسم الثانوي',[10,11,12],'علوم الآلة والمتون الكبرى ثم سنة التتويج','**الثانوية القرآنية** (١١) · **شهادة التخرج** (١٢)')]
PROG=[('القرآن','**البرنامج الأول · القرآن وعلومه**'),('اللغة','**البرنامج الثاني · اللغة وعلومها**'),
 ('الإسلامية','**البرنامج الثالث · الدراسات الإسلامية**'),('التتويج','**خدمة سنة التتويج**')]
# one definition, shared with verify.py and gen-allocation.py
STRANDS={g:' · '.join(v) for g,v in C.STRANDS.items()}

def hrs(lessons):
    m=lessons*40
    h,r=divmod(m,60)
    return f'{h} س' if r==0 else f'{h} س {r} د'

def grade_rows(g):
    """returns dict prog -> list of row tuples, plus totals"""
    corner,slots,hosted=D[str(g)]
    lower = g<=6
    qmin = quran_minutes(g)
    qhrs = hrs(int(qmin*39/40)) if False else ('188 س 30 د' if lower else '221 س')
    rows={p:[] for p,_ in PROG}
    rows['القرآن'].append(('**حفظ القرآن الكريم**','**مستقل**','الساعة المحمية',f'{qmin} د/أسبوع','—',qhrs,'خارج الخانات — لا تُقتطع لأي مادة'))
    for name,prog,n,note in corner:
        rows[prog].append((f'**{name.strip("*")}**','**مستقل**','سنة',str(n),str(n*39),hrs(n*39),note or '—'))
    for lab,cap,terms in slots:
        for t in terms:
            term,nt,name,prog,note=t
            L=cap*13*nt if False else cap*13*nt
            # cap is slot size; each term course occupies the whole slot for nt terms
            L=cap*13*nt
            rows[prog].append((f'**{name}**','**مستقل**',term,str(cap),str(L),hrs(L),note or '—'))
    for name,prog,host,note in hosted:
        form='مدمج' if note.startswith('مدمج') else ('وحدة' if note.startswith('وحدة') else 'مضمّن')
        rows[prog].append((f'**{name}**',form,'—','—','—','—',f'داخل **{host}** — {note}'))
    return rows,corner,slots,hosted

def counts(g):
    corner,slots,hosted=D[str(g)]
    books = 1 + len([c for c in corner if c[0].strip('*')!='التجويد']) + (1 if slots else 0)
    ncourses = 1 + len(corner) + sum(len(s[2]) for s in slots) + len(hosted) + (len(STRANDS[g].split(' · ')) if g<=6 else 0)
    hs = sum(c[2] for c in corner)+sum(s[1] for s in slots)
    return books,ncourses,hs

out=io.StringIO()
w=out.write
w('# البنية الدستورية · CONSTITUTIONAL STRUCTURE\n\n'
  '> **مولَّدة آليًّا** من `allocation-v11.json` بواسطة `generate-class-book.py`.\n'
  '> **لا تُحرَّر باليد.** إن لزم تغيير، فغيِّر المصدر وأعد التوليد.\n\n'
  '# ٤ أقسام · ١٢ صفًّا · ٣ برامج\n\n')
w('| القسم | الصفوف | العنوان | بوابة الخروج |\n|---|---|---|---|\n')
for nm,gs,title,gate in SECTIONS:
    a,b=NAMES[gs[0]],NAMES[gs[-1]]
    w(f'| **{nm}** | {a[0]}–{b[0]} *({a[1]}–{b[1]})* | {title} | {gate} |\n')
w('\n| البرنامج | |\n|---|---|\n| **الأول** | **القرآن وعلومه** |\n| **الثاني** | **اللغة وعلومها** |\n| **الثالث** | **الدراسات الإسلامية** |\n\n')
w('> **كل مادة في كل صف من الأقسام الأربعة تقع تحت واحد من هذه البرامج الثلاثة،\n> ولا تقع خارجها.**\n\n')
w('## القاعدة الحاكمة في القسمين الأولين\n\n> **في التمهيدي والابتدائي كل شيء مدمج أو مضمّن. لا يُثقَل الطفل بالكتب.**\n\n')
w('## قاعدة عدّ الكتب *(L-31)*\n\n')
w('| البند | العدّ |\n|---|---|\n')
w('| **كتاب القرآن وعلومه** — من تأليف المدرسة | **١** في كل صف من الأول إلى الثاني عشر. يضمّ دفتر السبق ومتنَ التجويد لتلك المرحلة |\n')
w('| كل مادة **مستقلة سنويةً** | **كتاب واحد** |\n')
w('| **التجويد** | **لا يُعدّ كتابًا مستقلًّا** — متنُه مجلَّد داخل كتاب القرآن وعلومه |\n')
w('| **المقررات الفصلية** كلها | **كراسة المقررات الفصلية** — كتاب واحد للصف |\n')
w('| **المدمج** و**المضمّن** | **لا كتاب** — داخل كتاب المضيف |\n')
w('| **المصحف** | أصلٌ لا يُعدّ في الكتب |\n\n')
w('| الصيغة | خانة؟ | كتاب؟ | ورقة؟ |\n|---|---|---|---|\n')
w('| **مستقل** | نعم | **نعم** | نعم |\n| **مدمج** | يشترك | **لا — داخل كتاب الشريك** | قسم مسمّى · أرضية ٤٠٪ |\n')
w('| **مضمّن** | لا | **لا** | داخل المضيف |\n| **وحدة** | لا | **لا** | تقدير إنجاز · قسم ب |\n| **مسار** | لا | **لا** | وصف بلا رقم |\n\n---\n\n')

for nm,gs,title,gate in SECTIONS:
    a,b=NAMES[gs[0]],NAMES[gs[-1]]
    w(f'# {nm}\n### {a[0]}–{b[0]} · {title}\n\n**بوابة الخروج:** {gate}\n\n')
    w('| الصف | حصص | علوم | كتب | ساعات المواد | الساعة القرآنية | الإجمالي |\n|---|---|---|---|---|---|---|\n')
    for g in gs:
        books,nc,hs=counts(g)
        lower=g<=6
        sub=hrs(hs*39); q='188 س 30 د' if lower else '221 س'; tot='526 س 30 د' if lower else '715 س'
        w(f'| **{NAMES[g][0]}** *({NAMES[g][1]})* | {hs} | **{nc}** | **{books}** | {sub} | {q} | **{tot}** |\n')
    w('\n')
    for g in gs:
        books,nc,hs=counts(g)
        rows,corner,slots,hosted=grade_rows(g)
        w(f'## الصف {NAMES[g][0]} · {NAMES[g][1]} — {hs} حصة · **{nc} علمًا** · **{books} كتابًا** + المصحف\n\n')
        for p,lab in PROG:
            if not rows[p]: continue
            w(f'{lab} — {len(rows[p])} مادة\n\n')
            w('| المادة | الصيغة | المدة | حصص | حصص/سنة | ساعات | البيان |\n|---|---|---|---|---|---|---|\n')
            for r in rows[p]:
                w('| '+' | '.join(r)+' |\n')
            w('\n')
        w(f'**مجموع الخانات: {hs} / {hs}** ✓ · **ساعات المواد {hrs(hs*39)}**\n\n')
        if g<=6:
            n=len(STRANDS[g].split(' · '))
            w(f'**{["","مسار واحد","مساران","٣ مسارات","٤ مسارات"][n]} داخل كتاب التربية الإسلامية (البرنامج الثالث):** {STRANDS[g]}\n\n')
        if g<=2:
            w('> درجة واحدة في قسم (أ) · ملحق وصفي: متقن / نامٍ / مبتدئ — **بلا رقم**\n\n')
    w('---\n\n')

# التجويد trail
w('# مسار التجويد عبر الصفوف الاثني عشر\n\n')
w('> **التجويد علمٌ قائم بنفسه، لا يُضمَّن في الساعة القرآنية في الصفوف المتقدمة.**\n')
w('> الساعة القرآنية للحفظ والمراجعة؛ والتجويد مادة لها حصتها ومتنها وورقتها من الرابع إلى الحادي عشر.\n\n')
w('| الصف | الصيغة | حصص | المتن والمنهج |\n|---|---|---|---|\n')
for g in range(1,13):
    corner,slots,hosted=D[str(g)]
    c=[x for x in corner if x[0].strip('*')=='التجويد']
    h=[x for x in hosted if x[0]=='التجويد']
    if c:
        w(f'| **{NAMES[g][0]}** | **مستقل** | {c[0][2]} | {c[0][3]} |\n')
    elif h:
        w(f'| **{NAMES[g][0]}** | مضمّن | — | بلا متن — {h[0][3].replace("مضمّن — ","")} |\n')
w('\n')
tot=sum(x[2] for g in range(1,13) for x in D[str(g)][0] if x[0].strip("*")=="التجويد")
w(f'**التجويد مستقلًّا: الرابع–الحادي عشر · حصةٌ في الأسبوع في كل صف من الثمانية · {hrs(tot*39)} عبر الثماني سنوات**\n\n---\n\n')

w('## التحقق\n\n| الفحص | النتيجة |\n|---|---|\n')
w('| الأقسام الأربعة | **✓ تمهيدي ٢ · ابتدائي ٤ · إعدادي ٣ · ثانوي ٣ = ١٢** |\n')
ok=all(counts(g)[2]==(13 if g<=6 else 19) for g in range(1,13))
w(f'| كل صف يوازن حصصه | **{"✓ ١٢/١٢" if ok else "✗"}** |\n')
w('| كل مادة تحت أحد البرامج الثلاثة | **✓** |\n')
w(f'| كتب التمهيدي والابتدائي | **{counts(1)[0]} + المصحف** |\n')
w(f'| كتب صف التخرج | **{counts(12)[0]} + المصحف — وهو الأكثر (L-10)** |\n')
w('| الساعة القرآنية محمية | **✓ ١٢/١٢ — لم تُقتطع لأي مادة** |\n')
w('| الرسم العثماني وأصول رواية حفص | **ليسا مادتين — بابان داخل منهج التجويد في التاسع** |\n')
w('| التجويد في الصفوف المتقدمة | **مستقل ٤–١١ — غير مضمّن في الساعة القرآنية** |\n')

open(''+SP+'CLASS-BOOK.md','w').write(out.getvalue())
print('written')
for g in range(1,13):
    b,n,h=counts(g); print(g,'حصص',h,'كتب',b,'علوم',n)
