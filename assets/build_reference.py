#!/usr/bin/env python3
"""Build a branded reference.docx for pandoc: AMIU navy/gold institutional style."""
import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

SRC = "/home/user/shroyalschools/assets/reference-base.docx"
OUT = "/home/user/shroyalschools/assets/amiu-reference.docx"

NAVY = RGBColor(0x12, 0x2A, 0x4E)
NAVY_DK = RGBColor(0x0A, 0x18, 0x30)
GOLD = RGBColor(0xB0, 0x86, 0x25)
TEXT = RGBColor(0x1A, 0x1F, 0x2B)
GREY = RGBColor(0x5B, 0x63, 0x72)

HEAD_FONT = "Bitstream Charter"
BODY_FONT = "Liberation Sans"
SERIF_FONT = "Liberation Serif"

doc = Document(SRC)

def get_style(document, name):
    """Robust lookup bypassing python-docx's lowercase 'heading N' alias bug."""
    for s in document.styles:
        if s.name == name:
            return s
    raise KeyError(name)

def has_style(document, name):
    return any(s.name == name for s in document.styles)

def set_font(style, name=BODY_FONT, size=11, color=TEXT, bold=False, italic=False,
             all_caps=False, spacing=None):
    style.font.name = name
    rpr = style.element.get_or_add_rPr()
    rFonts = rpr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rpr.append(rFonts)
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:eastAsia'), name)
    rFonts.set(qn('w:cs'), name)
    style.font.size = Pt(size)
    style.font.color.rgb = color
    style.font.bold = bold
    style.font.italic = italic
    style.font.all_caps = all_caps
    if spacing is not None:
        rpr2 = style.element.get_or_add_rPr()
        spc = OxmlElement('w:spacing')
        spc.set(qn('w:val'), str(spacing))
        rpr2.append(spc)

def set_para_fmt(style, space_before=0, space_after=8, line=1.15, keep_next=False,
                  align=None, border_bottom=None, border_color=None):
    pf = style.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line
    pf.keep_with_next = keep_next
    if align is not None:
        pf.alignment = align
    if border_bottom:
        pPr = style.element.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), str(border_bottom))
        bottom.set(qn('w:space'), '4')
        bottom.set(qn('w:color'), border_color or '122A4E')
        pBdr.append(bottom)
        pPr.append(pBdr)

# ---------------- Normal / body ----------------
normal = get_style(doc, 'Normal')
set_font(normal, BODY_FONT, 10.5, TEXT)
set_para_fmt(normal, 0, 8, 1.18)

# ---------------- Title (used for the doc's H1-level "Title" para if any) ----------------
title = get_style(doc, 'Title')
set_font(title, HEAD_FONT, 30, NAVY, bold=True)
set_para_fmt(title, 0, 6, 1.05, align=WD_ALIGN_PARAGRAPH.LEFT)

if has_style(doc, 'Subtitle'):
    subtitle = get_style(doc, 'Subtitle')
    set_font(subtitle, BODY_FONT, 15, GOLD, italic=True)
    set_para_fmt(subtitle, 0, 20, 1.15)

# ---------------- Heading 1 ----------------
# NOTE: page breaks before H1 headings are handled by EXPLICIT raw-openxml
# breaks in the markdown, not by a style-level pageBreakBefore. H1 is reused
# across Part dividers *and* front/back-matter section openers with very
# different page-break needs, and stacking a style-level break under an
# already-explicit break produced stray blank pages during QA.
h1 = get_style(doc, 'Heading 1')
set_font(h1, HEAD_FONT, 27, NAVY, bold=True)
set_para_fmt(h1, 4, 16, 1.05, keep_next=True, border_bottom=18, border_color='B08625')

# ---------------- Heading 2 (Sections) ----------------
h2 = get_style(doc, 'Heading 2')
set_font(h2, HEAD_FONT, 15.5, NAVY, bold=True)
set_para_fmt(h2, 20, 8, 1.08, keep_next=True, border_bottom=6, border_color='D8DCE5')

# ---------------- Custom style: Part-divider kicker label ----------------
if not has_style(doc, 'PartKicker'):
    kicker = doc.styles.add_style('PartKicker', WD_STYLE_TYPE.PARAGRAPH)
    kicker.base_style = get_style(doc, 'Normal')
else:
    kicker = get_style(doc, 'PartKicker')
set_font(kicker, BODY_FONT, 11, GOLD, bold=True, all_caps=True, spacing=30)
set_para_fmt(kicker, 0, 2, 1.1)

# ---------------- Custom style: Part-divider thesis line ----------------
if not has_style(doc, 'PartThesis'):
    thesis = doc.styles.add_style('PartThesis', WD_STYLE_TYPE.PARAGRAPH)
    thesis.base_style = get_style(doc, 'Normal')
else:
    thesis = get_style(doc, 'PartThesis')
set_font(thesis, SERIF_FONT, 13.5, NAVY, italic=True)
set_para_fmt(thesis, 4, 18, 1.35)

# ---------------- Heading 3 ----------------
h3 = get_style(doc, 'Heading 3')
set_font(h3, BODY_FONT, 12, GOLD, bold=True, all_caps=False)
set_para_fmt(h3, 14, 6, 1.1, keep_next=True)

# ---------------- Heading 4 ----------------
if has_style(doc, 'Heading 4'):
    h4 = get_style(doc, 'Heading 4')
    set_font(h4, BODY_FONT, 10.5, NAVY, bold=True, italic=True)
    set_para_fmt(h4, 10, 4, 1.1, keep_next=True)

# ---------------- TOC / Contents heading ----------------
for nm in ['TOC Heading']:
    if has_style(doc, nm):
        tocH = get_style(doc, nm)
        set_font(tocH, HEAD_FONT, 22, NAVY, bold=True)
        set_para_fmt(tocH, 0, 14, 1.1)

for lvl, sz in zip(['TOC 1', 'TOC 2', 'TOC 3'], [12, 10.8, 10]):
    if has_style(doc, lvl):
        st = get_style(doc, lvl)
        set_font(st, BODY_FONT, sz, TEXT, bold=(lvl == 'TOC 1'))
        set_para_fmt(st, 4 if lvl == 'TOC 1' else 1, 4 if lvl == 'TOC 1' else 1, 1.1)

# ---------------- Block quote (pull quotes) ----------------
if has_style(doc, 'Block Text'):
    bq = get_style(doc, 'Block Text')
    set_font(bq, SERIF_FONT, 13, NAVY, italic=True)
    set_para_fmt(bq, 10, 10, 1.3)
if has_style(doc, 'Quote'):
    bq = get_style(doc, 'Quote')
    set_font(bq, SERIF_FONT, 13, NAVY, italic=True)
    set_para_fmt(bq, 10, 10, 1.3)

# ---------------- Caption ----------------
if has_style(doc, 'Caption'):
    cap = get_style(doc, 'Caption')
    set_font(cap, BODY_FONT, 9.5, GOLD, bold=True, italic=False)
    set_para_fmt(cap, 6, 16, 1.15)

# ---------------- Table styles ----------------
if has_style(doc, 'Table Grid'):
    tg = get_style(doc, 'Table Grid')
    try:
        set_font(tg, BODY_FONT, 9.5, TEXT)
    except Exception:
        pass

# ---------------- Compact / First paragraph ----------------
for nm in ['Compact', 'Body Text', 'First Paragraph']:
    if has_style(doc, nm):
        st = get_style(doc, nm)
        set_font(st, BODY_FONT, 10.5, TEXT)
        set_para_fmt(st, 0, 6, 1.18)

# ==================================================================
# Page setup: US Letter, generous but efficient margins, section props
# ==================================================================
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.left_margin = Inches(1.1)
section.right_margin = Inches(1.1)
section.top_margin = Inches(1.0)
section.bottom_margin = Inches(1.0)
section.header_distance = Inches(0.5)
section.footer_distance = Inches(0.5)
section.different_first_page_header_footer = True

# ==================================================================
# Header (title running header) & Footer (page number + confidentiality)
# ==================================================================
def add_field(paragraph, field_code, font=BODY_FONT, size=8.5, color=GREY, bold=False):
    run = paragraph.add_run()
    run.font.name = font
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = field_code
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    return run

# --- Default header (all pages after first) ---
header = section.header
header.is_linked_to_previous = False
hp = header.paragraphs[0]
hp.text = ""
hp.paragraph_format.tab_stops.add_tab_stop(Inches(6.3), WD_TAB_ALIGNMENT.RIGHT)
hp.paragraph_format.space_after = Pt(0)
r1 = hp.add_run("AL-MULK INTERNATIONAL UNIVERSITY")
r1.font.name = BODY_FONT; r1.font.size = Pt(8); r1.font.color.rgb = NAVY; r1.font.bold = True
r1.font.all_caps = True
r2 = hp.add_run("\t")
r3 = hp.add_run("Strategic Implementation Blueprint 2028–2050")
r3.font.name = BODY_FONT; r3.font.size = Pt(8); r3.font.color.rgb = GREY; r3.font.italic = True
# rule under header
pPr = hp._p.get_or_add_pPr()
pBdr = OxmlElement('w:pBdr')
bottom = OxmlElement('w:bottom')
bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '6')
bottom.set(qn('w:space'), '4'); bottom.set(qn('w:color'), 'B08625')
pBdr.append(bottom)
pPr.append(pBdr)

# --- Default footer (all pages after first) ---
footer = section.footer
footer.is_linked_to_previous = False
fp = footer.paragraphs[0]
fp.text = ""
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fp.paragraph_format.space_before = Pt(4)
r4 = fp.add_run("AMIU-SB-002  ·  ")
r4.font.name = BODY_FONT; r4.font.size = Pt(8); r4.font.color.rgb = GREY
add_field(fp, 'PAGE', color=NAVY, bold=True)
r5 = fp.add_run("  of  ")
r5.font.name = BODY_FONT; r5.font.size = Pt(8); r5.font.color.rgb = GREY
add_field(fp, 'NUMPAGES', color=NAVY, bold=True)
r6 = fp.add_run("  ·  Confidential — Institutional Planning Document")
r6.font.name = BODY_FONT; r6.font.size = Pt(8); r6.font.color.rgb = GREY

# --- First-page header/footer: blank (cover page has no running head) ---
fph = section.first_page_header
fph.is_linked_to_previous = False
fph.paragraphs[0].text = ""
fpf = section.first_page_footer
fpf.is_linked_to_previous = False
fpf.paragraphs[0].text = ""

# ==================================================================
# Executive table style: navy header row, gold rule, subtle zebra banding
# ==================================================================
def qn_(tag):
    return qn(tag)

table_style = None
for s in doc.styles.element.findall(qn('w:style')):
    if s.get(qn('w:styleId')) == 'Table':
        table_style = s
        break

if table_style is not None:
    tblPr = table_style.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        table_style.append(tblPr)
    # Clean horizontal-rule borders (no verticals) at table level
    borders = OxmlElement('w:tblBorders')
    for edge, sz, color in [('top', 8, '122A4E'), ('bottom', 8, '122A4E'),
                             ('insideH', 4, 'D8DCE5')]:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), str(sz))
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), color)
        borders.append(el)
    for edge in ['left', 'right', 'insideV']:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'nil')
        borders.append(el)
    tblPr.append(borders)

    # Remove existing firstRow tblStylePr (will be replaced) and any band defs
    for tsp in table_style.findall(qn('w:tblStylePr')):
        table_style.remove(tsp)

    def make_tblStylePr(kind, fill=None, text_color=None, bold=False, border_bottom=None):
        tsp = OxmlElement('w:tblStylePr')
        tsp.set(qn('w:type'), kind)
        if bold or text_color:
            rPr = OxmlElement('w:rPr')
            if bold:
                rPr.append(OxmlElement('w:b'))
            if text_color:
                c = OxmlElement('w:color'); c.set(qn('w:val'), text_color); rPr.append(c)
            tsp.append(rPr)
        tcPr = OxmlElement('w:tcPr')
        if fill:
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear'); shd.set(qn('w:fill'), fill)
            tcPr.append(shd)
        if border_bottom:
            tcBorders = OxmlElement('w:tcBorders')
            b = OxmlElement('w:bottom')
            b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '12'); b.set(qn('w:color'), border_bottom)
            tcBorders.append(b)
            tcPr.append(tcBorders)
        vAlign = OxmlElement('w:vAlign'); vAlign.set(qn('w:val'), 'center')
        tcPr.append(vAlign)
        tcMar = OxmlElement('w:tcMar')
        for side, val in [('top', 80), ('bottom', 80), ('left', 120), ('right', 120)]:
            m = OxmlElement(f'w:{side}')
            m.set(qn('w:w'), str(val)); m.set(qn('w:type'), 'dxa')
            tcMar.append(m)
        tcPr.append(tcMar)
        tsp.append(tcPr)
        return tsp

    # NOTE: table-style rPr color is beaten by the explicit color set on the
    # "Compact" paragraph style pandoc applies to every cell, so header
    # legibility is achieved via a light tint + bold rather than reversed text.
    table_style.append(make_tblStylePr('firstRow', fill='DCE3F0',
                                        bold=True, border_bottom='B08625'))
    table_style.append(make_tblStylePr('band1Horz', fill='F6F7FA'))

doc.save(OUT)
print("Saved", OUT)
