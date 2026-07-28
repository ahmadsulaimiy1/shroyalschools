#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classifies the plain, unstructured paragraphs of "الكامل الشامل الممل في
تجويد القرآن" (a verse-by-verse commentary on Tuhfat al-Atfal) into the
same semantic HTML structure used for "الكافي في التجويد", so it shares
the same flagship CSS design system and the same HTML->DOCX pipeline.
"""
import re
import html
import docx

SRC = "/root/.claude/uploads/c0d02c27-08d9-5bbc-b193-2fc67eeecf61/9d1c369a-___________________________________.docx"
OUT = "/tmp/book2/body.html"

d = docx.Document(SRC)
paras = [p.text.strip() for p in d.paragraphs]
paras = [t for t in paras if t]  # drop blank paragraphs entirely

NOISE = {
    "تابع الكامل الشامل الممل في تجويد القرآن",
    "شرح متن تحفة الأطفال والغلمان",
}
paras = [t for t in paras if t not in NOISE and t != "---"]

BAB_RE = re.compile(r"^باب .{2,45}$")
KHATIMAH_BAB_RE = re.compile(r"^خاتمة باب ")
VERSE_RE = re.compile(r"^(البيت|البيتان|الأبيات|شرح البيت|شرح البيتين)\b")
MASALA_RE = re.compile(r"^المسألة ال\S+[:：]")
BULLET_RE = re.compile(r"^[·•]\s*")
NUMBERED_RE = re.compile(r"^(\d+)[\.\)]\s+")
POEM_INTRO_RE = re.compile(r"^قال (الناظم|الإمام ابن الجزري|الشافعي)\b.*[:：]\s*$")
LABEL_LEAD_RE = re.compile(r"^([ء-ي][ء-ي\s]{1,26}?[:：])\s*(.+)$")

FRONT_H1 = [
    "مقدمة الشرح",
    "تمهيد لطيف في التعريف بالناظم ونسبه وشيوخه ومؤلفاته",
    "في فضل علم التجويد والترغيب في تعلمه وتعليمه",
]
FRONT_H3 = {
    "اسمه ونسبه", "مولده ونشأته", "شيوخه", "تلاميذه", "مؤلفاته", "وفاته",
    "الأدلة من الكتاب والسنة", "أقوال السلف في التجويد", "حكم التجويد", "في اللحن وحكمه",
}

def esc(s):
    return html.escape(s, quote=False)

def bold_lead(text):
    m = LABEL_LEAD_RE.match(text)
    if m and len(m.group(1)) <= 30:
        return f"<strong>{esc(m.group(1))}</strong> {esc(m.group(2))}"
    return esc(text)

class Emitter:
    def __init__(self):
        self.out = []
        self.bullet_buf = []
        self.numbered_buf = []

    def flush_lists(self):
        if self.bullet_buf:
            self.out.append("<ul>")
            for it in self.bullet_buf:
                self.out.append(f"<li>{bold_lead(it)}</li>")
            self.out.append("</ul>")
            self.bullet_buf = []
        if self.numbered_buf:
            self.out.append("<ol>")
            for it in self.numbered_buf:
                self.out.append(f"<li>{bold_lead(it)}</li>")
            self.out.append("</ol>")
            self.numbered_buf = []

    def emit_block(self, kind, text):
        if kind == "bullet":
            self.bullet_buf.append(text)
            return
        if kind == "numbered":
            self.numbered_buf.append(text)
            return
        self.flush_lists()
        if kind == "subhead" or kind == "masala":
            self.out.append(f'<h4 class="subsection-title">{esc(text)}</h4>')
        elif kind == "label_short":
            self.out.append(f'<p class="lead-label"><strong>{esc(text)}</strong></p>')
        elif kind == "matn":
            self.out.append(f'<div class="matn">{esc(text)}</div>')
        elif kind == "para":
            self.out.append(f"<p>{bold_lead(text)}</p>")

    def raw(self, s):
        self.flush_lists()
        self.out.append(s)


def classify(text):
    if BAB_RE.match(text):
        return ("bab", text)
    if text == "تمهيد الباب":
        return ("bab_intro_label", text)
    if KHATIMAH_BAB_RE.match(text):
        return ("bab_khatimah", text)
    if VERSE_RE.match(text):
        return ("verse", text)
    if text in {
        "تحليل البيت لغة وإعرابًا", "تحليل البيتين لغة وإعرابًا",
        "المعنى الإجمالي للبيت", "المعنى الإجمالي للبيتين",
        "تفصيل المسائل المتعلقة بالبيت", "تفصيل المسائل المتعلقة بالبيتين",
        "تطبيق تجويدي للبيت", "تطبيق تجويدي للبيتين",
        "خاتمة البيت", "خاتمة البيتين",
    }:
        return ("subhead", text)
    if MASALA_RE.match(text):
        return ("masala", text)
    if POEM_INTRO_RE.match(text):
        return ("poem_intro", text)
    if BULLET_RE.match(text):
        return ("bullet", BULLET_RE.sub("", text))
    if NUMBERED_RE.match(text):
        return ("numbered", NUMBERED_RE.sub("", text))
    if text in FRONT_H1:
        return ("front_h1", text)
    if text in FRONT_H3:
        return ("front_h3", text)
    if len(text) < 46 and not text.endswith((".", "؟", "!", "،", ")", "»")):
        return ("label_short", text)
    if " ... " in text and len(text) < 170:
        return ("matn", text)
    return ("para", text)


BOOK_TITLE = paras[0]
BOOK_SUBTITLE = paras[1]
BOOK_AUTHOR_LINE = paras[2]  # "تأليف: ..." -- kept verbatim, no fabricated name

items = [classify(t) for t in paras]
from collections import Counter
print("counts:", Counter(k for k, v in items))

body_start = next(i for i, (k, v) in enumerate(items) if v == "شرح المتن")
front_items = items[3:body_start]  # skip title/subtitle/author (used for the cover instead)
main_items = items[body_start + 1:]

with open("/tmp/book2/meta.py", "w", encoding="utf-8") as f:
    f.write(f"BOOK_TITLE = {BOOK_TITLE!r}\nBOOK_SUBTITLE = {BOOK_SUBTITLE!r}\nBOOK_AUTHOR_LINE = {BOOK_AUTHOR_LINE!r}\n")

E = Emitter()
ORD_WORDS = ["", "الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر"]

# ============================== FRONT MATTER ==============================
E.raw('<section class="page frontmatter content" id="muqaddimah-shahr">')
E.raw('<div class="page-pad">')
page_open = True
for kind, text in front_items:
    if kind == "front_h1":
        E.raw(f"<h2>{esc(text)}</h2>")
    elif kind == "front_h3":
        E.raw(f'<h3 class="plain-h3">{esc(text)}</h3>')
    else:
        E.emit_block(kind, text)
E.flush_lists()
E.raw("</div></section>")

# ============================== MAIN BODY ==============================
bab_count = 0
verse_count = 0
content_open = False
verse_open = False
awaiting_bab_desc = False
summary_pending = False
summary_buf = []
current_bab_id = None

def close_content():
    global content_open
    if content_open:
        E.flush_lists()
        E.raw("</div></section>")
        content_open = False

def close_verse():
    global verse_open
    if verse_open:
        E.flush_lists()
        E.raw("</article>")
        verse_open = False

def close_summary():
    global summary_pending
    if summary_pending and summary_buf:
        E.raw('<div class="summary-card"><h3>خلاصة الباب</h3>')
        for p in summary_buf:
            E.raw(f"<p>{bold_lead(p)}</p>")
        E.raw("</div>")
    summary_buf.clear()
    summary_pending = False

i = 0
n = len(main_items)
while i < n:
    kind, text = main_items[i]

    if kind == "bab":
        close_verse(); close_summary(); close_content()
        bab_count += 1
        verse_count = 0
        current_bab_id = f"bab{bab_count}"
        title = re.sub(r"^باب ", "", text)
        E.raw(f'<section class="part-opener" id="{current_bab_id}">')
        kicker = ORD_WORDS[bab_count] if bab_count < len(ORD_WORDS) else str(bab_count)
        E.raw(f'<div class="kicker">الباب {kicker}</div>')
        E.raw(f'<div class="num">{bab_count}</div>')
        E.raw(f"<h2>{esc(title)}</h2>")
        # peek ahead: if next item is a plain descriptive paragraph (with or without تمهيد الباب label), use as desc
        j = i + 1
        if j < n and main_items[j][0] == "bab_intro_label":
            j += 1
        desc = None
        if j < n and main_items[j][0] == "para":
            desc = main_items[j][1]
            i = j  # consume it here
        E.raw(f'<p class="part-desc">{esc(desc)}</p>' if desc else "")
        E.raw("</section>")
        E.raw('<section class="page"><div class="content">')
        content_open = True
        i += 1
        continue

    if kind == "bab_intro_label":
        i += 1
        continue

    if kind == "bab_khatimah":
        close_verse()
        summary_pending = True
        summary_buf.clear()
        i += 1
        continue

    if summary_pending and kind == "para":
        summary_buf.append(text)
        i += 1
        continue
    if summary_pending and kind not in ("para",):
        close_summary()

    if kind == "verse":
        close_verse()
        verse_count += 1
        vid = f"{current_bab_id}-v{verse_count}"
        title = re.sub(r"^شرح ", "", text)
        E.raw(f'<article class="chapter" id="{vid}">')
        E.raw(f'<h2 class="chapter-title">{esc(title)}</h2>')
        verse_open = True
        i += 1
        continue

    if kind == "poem_intro":
        i += 1
        while i < n and main_items[i][0] == "matn":
            E.emit_block("matn", main_items[i][1])
            i += 1
        continue

    if kind in ("subhead", "masala", "label_short", "bullet", "numbered", "para", "matn"):
        E.emit_block(kind, text)
        i += 1
        continue

    i += 1

close_verse()
close_summary()
close_content()

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(E.out))

print("bab_count:", bab_count, "verse_count total emitted articles: see log above")
print("output length:", sum(len(x) for x in E.out))
