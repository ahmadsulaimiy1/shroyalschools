#!/usr/bin/env python3
"""Two-pass assembly: build the full AMIU Blueprint with an accurate, real-page-numbered TOC."""
import subprocess, re, sys, os

ROOT = "/home/user/shroyalschools"
os.chdir(ROOT)

FRONT = "assets/part0_front_matter.md"
LISTS1 = "assets/lists_figtab.md"
LISTS2 = "assets/lists_abbrev_glossary.md"
BODY = "work_body_dividers.md"
BACK = "assets/part9_back_matter.md"
REFDOC = "assets/amiu-reference.docx"

MARKER = "<<<TOC_PLACEHOLDER>>>"

# TOC entries: (display text, search text for page lookup, level 1 or 2)
TOC_ENTRIES = [
    ("Foreword", "Foreword", 1),
    ("Founder's Message", "Founder’s Message", 1),
    ("Chairman's Message", "Chairman’s Message", 1),
    ("President's Message", "President’s Message", 1),
    ("Executive Summary", "Executive Summary", 1),
    ("AMIU at a Glance", "AMIU at a Glance", 1),
    ("List of Figures", "List of Figures", 1),
    ("List of Charts", "List of Charts", 1),
    ("List of Diagrams", "List of Diagrams", 1),
    ("List of Flowcharts", "List of Flowcharts", 1),
    ("List of Tables", "List of Tables", 1),
    ("List of Abbreviations", "List of Abbreviations", 1),
    # Search text intentionally longer than the bare word "Glossary": the
    # Index cross-references "Glossary" several times on its own late pages,
    # and a last-occurrence search on the bare word matches those instead of
    # the real heading. This phrase is unique to the paragraph right below it.
    ("Glossary", "Islamic-studies terminology is presented with standard transliteration", 1),
]

PART_TITLES = [
    ("I", "Governance & Institutional Foundations", "Sections 1–5",
     [(1, "Institutional Vision 2028–2050"), (2, "Mission, Values, and Identity"),
      (3, "Governance Framework"), (4, "Senate Structure"), (5, "Board Structure")]),
    ("II", "Organizational & Academic Structure", "Sections 6–10",
     [(6, "Organizational Chart"), (7, "Academic Master Plan"), (8, "College Structure"),
      (9, "Faculty Structure"), (10, "Department Structure")]),
    ("III", "Curriculum & Student Journey", "Sections 11–15",
     [(11, "Programme Portfolio"), (12, "Curriculum Architecture"), (13, "Student Journey Map"),
      (14, "Admission Policies"), (15, "Faculty Recruitment Strategy")]),
    ("IV", "Research, Publishing, Partnerships & Accreditation", "Sections 16–20",
     [(16, "Research Strategy"), (17, "Publishing Strategy"), (18, "Global Partnerships Strategy"),
      (19, "Accreditation Roadmap"), (20, "ISO 21001 Roadmap")]),
    ("V", "Digital Infrastructure, AI & Waqf Development", "Sections 21–25",
     [(21, "LMS Ecosystem"), (22, "AI Strategy"), (23, "Digital Transformation Strategy"),
      (24, "Library Strategy"), (25, "Waqf Development Strategy")]),
    ("VI", "Financial Growth, Marketing & Branding", "Sections 26–30",
     [(26, "Scholarship Strategy"), (27, "Revenue Diversification Strategy"), (28, "Marketing Strategy"),
      (29, "Branding Strategy"), (30, "International Expansion Strategy")]),
    ("VII", "Regional Campuses & Student Lifecycle", "Sections 31–35",
     [(31, "Nigeria Campus Strategy"), (32, "Gulf Cooperation Strategy"), (33, "Student Support Framework"),
      (34, "Alumni Framework"), (35, "Career Development Framework")]),
    ("VIII", "Risk, Compliance, Sustainability & the 20-Year Roadmap", "Sections 36–41",
     [(36, "Risk Management Framework"), (37, "Compliance Framework"), (38, "Financial Sustainability Framework"),
      (39, "Capital Development Framework"), (40, "Twenty-Year Strategic Roadmap"),
      (41, "Founding Access & Waqf-First Strategy")]),
]

ROMAN_TO_WORD = {"I": "ONE", "II": "TWO", "III": "THREE", "IV": "FOUR", "V": "FIVE",
                  "VI": "SIX", "VII": "SEVEN", "VIII": "EIGHT"}

for roman, title, secrange, sections in PART_TITLES:
    # Search text targets the hero-spread's small-caps kicker line
    # ("PART FOUR OF EIGHT"), which is short, wrap-proof, and appears
    # exactly once in the whole document (only on that Part's divider page) —
    # this sidesteps both the long-title page-wrap bug and the TOC's-own-row
    # duplicate-occurrence ambiguity that affect the full title string.
    TOC_ENTRIES.append((f"Part {roman} — {title}", f"PART {ROMAN_TO_WORD[roman]} OF EIGHT", 1))
    for num, sec_title in sections:
        TOC_ENTRIES.append((f"Section {num}: {sec_title}", f"Section {num}: {sec_title}", 2))

TOC_ENTRIES += [
    ("Appendix A — Cross-Reference to the Ten-Year Master Plan (AMIU-MP-001)",
     "Appendix A — Cross-Reference to the Ten-Year Master Plan (AMIU-MP-001)", 1),
    ("Appendix B — Master Plan Exhibit Checklist", "Appendix B — Master Plan Exhibit Checklist", 1),
    ("Appendix C — Fixed Revenue Allocation Framework: Quick Reference",
     "Appendix C — Fixed Revenue Allocation Framework: Quick Reference", 1),
    ("Appendix D — Programme Catalog Reference", "Appendix D — Programme Catalog Reference", 1),
    ("References", "References", 1),
    ("Index", "Index", 1),
]

def build_toc_markdown(page_lookup=None):
    """page_lookup: dict search_text -> page number, or None for placeholder pass."""
    lines = []
    lines.append('## Table of Contents {.unnumbered}\n')
    lines.append("| | |")
    lines.append("|---|---:|")
    for display, search, level in TOC_ENTRIES:
        pg = "•" if page_lookup is None else str(page_lookup.get(search, "—"))
        if level == 1:
            lines.append(f"| **{display}** | **{pg}** |")
        else:
            lines.append(f"| &nbsp;&nbsp;&nbsp;&nbsp;{display} | {pg} |")
    lines.append("")
    lines.append('```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```')
    lines.append("")
    return "\n".join(lines)

def assemble(toc_markdown, outpath):
    parts = []
    with open(FRONT, encoding="utf-8") as f:
        parts.append(f.read())
    parts.append('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
    parts.append(toc_markdown)
    with open(LISTS1, encoding="utf-8") as f:
        parts.append(f.read())
    parts.append('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
    with open(LISTS2, encoding="utf-8") as f:
        parts.append(f.read())
    parts.append('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
    parts.append('# Main Contents {.unnumbered}\n')
    with open(BODY, encoding="utf-8") as f:
        parts.append(f.read())
    with open(BACK, encoding="utf-8") as f:
        parts.append(f.read())
    full = "\n\n".join(parts)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(full)
    return outpath

def run_pandoc(md_path, docx_path):
    subprocess.run(["pandoc", md_path, "-o", docx_path, f"--reference-doc={REFDOC}"], check=True)
    _prevent_row_splitting(docx_path)
    _style_subheading_labels(docx_path)
    _apply_callout_boxes(docx_path)
    _justify_body_text(docx_path)
    _enable_hyphenation(docx_path)

# Paragraph styles that carry running narrative prose. Deliberately excludes
# Caption, Block Text/Quote (pull quotes stay centered, never justified),
# PartKicker/PartThesis/SectionKicker, and every Heading/Title style.
BODY_PROSE_STYLES = {'Normal', 'Compact', 'Body Text', 'First Paragraph'}

def _justify_body_text(docx_path):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    """Full justification for narrative body text — never for table cells.
    Table cells use the same 'Compact' style as ordinary paragraphs (pandoc's
    default), so the style name alone can't distinguish them; the reliable
    signal is structural: python-docx's Document.paragraphs returns only
    top-level body paragraphs, excluding every paragraph that lives inside a
    table cell. Justifying at that structural level, rather than by editing
    the shared style, is what keeps tables left-aligned automatically."""
    import docx as _docx
    d = _docx.Document(docx_path)
    for p in d.paragraphs:
        if p.style.name in BODY_PROSE_STYLES:
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    d.save(docx_path)

def _enable_hyphenation(docx_path):
    """Turn on automatic hyphenation document-wide. Justification without
    hyphenation on a column this width produces exactly the 'rivers of
    white space' / oversized word gaps that read as amateur; the hunspell
    hyph_en_US dictionary (assets/fonts or apt hyphen-en-us) must be
    installed for LibreOffice to actually hyphenate rather than silently
    no-op. consecutiveHyphenLimit caps hyphenated-line runs at 2, matching
    the directive's own warning against excessive hyphenation."""
    import docx as _docx
    from docx.oxml.ns import qn as _qn
    from docx.oxml import OxmlElement as _El
    d = _docx.Document(docx_path)
    settings = d.settings.element
    if settings.find(_qn('w:autoHyphenation')) is None:
        settings.append(_El('w:autoHyphenation'))
    zone = _El('w:hyphenationZone')
    zone.set(_qn('w:val'), '360')
    settings.append(zone)
    limit = _El('w:consecutiveHyphenLimit')
    limit.set(_qn('w:val'), '2')
    settings.append(limit)
    d.save(docx_path)

def _style_subheading_labels(docx_path):
    """Restyle the bold sub-dimension labels ('**KPIs**', '**Risks & Mitigation**',
    etc.) that open each Section's ten dimensions into a small-caps gold
    editorial eyebrow, instead of leaving them as plain black bold text —
    matching the caption/eyebrow treatment used everywhere else in the design
    system. Detected structurally (first run in its paragraph, bold, short)
    rather than via a fixed label whitelist, since section authors phrased
    the labels slightly differently across the document."""
    import docx as _docx
    from docx.shared import Pt as _Pt, RGBColor as _RGBColor
    from docx.oxml.ns import qn as _qn
    from docx.oxml import OxmlElement as _El

    GOLD = _RGBColor(0xB0, 0x86, 0x25)
    d = _docx.Document(docx_path)

    def style_run(run):
        run.font.bold = True
        run.font.color.rgb = GOLD
        run.font.size = _Pt(10)
        rpr = run._r.get_or_add_rPr()
        caps = rpr.find(_qn('w:caps'))
        if caps is None:
            caps = _El('w:caps')
            rpr.append(caps)
        spc = rpr.find(_qn('w:spacing'))
        if spc is None:
            spc = _El('w:spacing')
            rpr.append(spc)
        spc.set(_qn('w:val'), '14')

    def process_paragraphs(paragraphs):
        for p in paragraphs:
            if p.style.name not in ('Normal', 'Compact', 'Body Text', 'First Paragraph'):
                continue
            if not p.runs:
                continue
            first = p.runs[0]
            text = first.text.strip()
            if not first.font.bold:
                continue
            if not (2 <= len(text) <= 58):
                continue
            if text.endswith('.') or text.endswith(','):
                continue
            style_run(first)

    process_paragraphs(d.paragraphs)
    for table in d.tables:
        for row in table.rows:
            for cell in row.cells:
                process_paragraphs(cell.paragraphs)

    d.save(docx_path)

def _apply_callout_boxes(docx_path):
    """Wrap the KPI and Risks & Mitigation paragraphs of every section in a
    shaded callout band with a gold accent bar — the 'signature callout
    framework' — instead of leaving them as plain gold-eyebrow paragraphs.
    Detection is structural (an already gold-styled eyebrow, run by
    _style_subheading_labels, whose text contains KPI or RISK) so it needs
    no label whitelist. Any instance immediately followed by a table before
    the next eyebrow/heading is skipped entirely rather than guessed at —
    shading across a table cleanly is not worth the risk to a working
    176-page pipeline for a handful of edge cases."""
    import docx as _docx
    from docx.shared import RGBColor as _RGBColor
    from docx.oxml.ns import qn as _qn
    from docx.oxml import OxmlElement as _El

    GOLD = _RGBColor(0xB0, 0x86, 0x25)
    TINT = "F7F3E8"
    BORDER = "B08625"

    d = _docx.Document(docx_path)
    para_by_elem = {p._p: p for p in d.paragraphs}

    def is_eyebrow(p):
        if not p.runs:
            return False
        r = p.runs[0]
        try:
            return bool(r.font.bold) and r.font.color and r.font.color.rgb == GOLD
        except Exception:
            return False

    def is_heading(p):
        return p.style.name.startswith("Heading") or p.style.name in ("Title", "Subtitle")

    def is_target(p):
        t = p.text.strip().upper()
        return ("KPI" in t) or ("RISK" in t)

    def set_spacing(p, before=None, after=None):
        pPr = p._p.get_or_add_pPr()
        spacing = pPr.find(_qn('w:spacing'))
        if spacing is None:
            spacing = _El('w:spacing')
            pPr.append(spacing)
        if before is not None:
            spacing.set(_qn('w:before'), str(before))
        if after is not None:
            spacing.set(_qn('w:after'), str(after))

    def box_paragraph(p):
        pPr = p._p.get_or_add_pPr()
        shd = pPr.find(_qn('w:shd'))
        if shd is None:
            shd = _El('w:shd')
            pPr.append(shd)
        shd.set(_qn('w:val'), 'clear')
        shd.set(_qn('w:color'), 'auto')
        shd.set(_qn('w:fill'), TINT)
        pBdr = pPr.find(_qn('w:pBdr'))
        if pBdr is None:
            pBdr = _El('w:pBdr')
            pPr.append(pBdr)
        left = pBdr.find(_qn('w:left'))
        if left is None:
            left = _El('w:left')
            pBdr.append(left)
        left.set(_qn('w:val'), 'single')
        left.set(_qn('w:sz'), '24')
        left.set(_qn('w:space'), '10')
        left.set(_qn('w:color'), BORDER)
        ind = pPr.find(_qn('w:ind'))
        if ind is None:
            ind = _El('w:ind')
            pPr.append(ind)
        ind.set(_qn('w:left'), '300')

    body = d.element.body
    children = list(body)
    n = len(children)
    i = 0
    while i < n:
        el = children[i]
        if el.tag == _qn('w:p') and el in para_by_elem:
            p = para_by_elem[el]
            if is_eyebrow(p) and is_target(p):
                j = i + 1
                box_elems = [el]
                aborted = False
                while j < n:
                    ce = children[j]
                    if ce.tag != _qn('w:p') or ce not in para_by_elem:
                        aborted = True
                        break
                    cp = para_by_elem[ce]
                    if is_eyebrow(cp) or is_heading(cp):
                        break
                    box_elems.append(ce)
                    j += 1
                if not aborted and len(box_elems) >= 1:
                    box_paras = [para_by_elem[e] for e in box_elems]
                    for bp in box_paras:
                        box_paragraph(bp)
                    for k, bp in enumerate(box_paras):
                        set_spacing(bp, before=(None if k == 0 else 0),
                                    after=(None if k == len(box_paras) - 1 else 0))
                    i = j
                    continue
        i += 1

    d.save(docx_path)

def _prevent_row_splitting(docx_path):
    """Set cantSplit on every table row so a row never breaks across a page
    (avoids stray wrapped fragments like a lone '001)' orphaned at a page top)."""
    import docx as _docx
    from docx.oxml.ns import qn as _qn
    from docx.oxml import OxmlElement as _El
    d = _docx.Document(docx_path)
    for table in d.tables:
        for row in table.rows:
            trPr = row._tr.find(_qn('w:trPr'))
            if trPr is None:
                trPr = _El('w:trPr')
                row._tr.insert(0, trPr)
            if trPr.find(_qn('w:cantSplit')) is None:
                trPr.append(_El('w:cantSplit'))
    d.save(docx_path)

def run_soffice(docx_path, profile):
    subprocess.run(["rm", "-rf", profile], check=False)
    os.makedirs(profile, exist_ok=True)
    subprocess.run(["soffice", "--headless", f"-env:UserInstallation=file://{profile}",
                     "--convert-to", "pdf", docx_path], check=True, capture_output=True)

# These entries' TRUE content occurs BEFORE the TOC block (front matter);
# every other entry's true content occurs AFTER the TOC block. The TOC itself
# lists all entries too, so each search string appears twice in the document —
# we must pick the earlier occurrence for "before-TOC" entries and the later
# (last) occurrence for everything else, or we'd match the TOC's own row.
BEFORE_TOC = {"Foreword", "Founder’s Message", "Chairman’s Message", "President’s Message", "Executive Summary",
              "AMIU at a Glance"}

def extract_page_map(pdf_path, txt_path):
    subprocess.run(["pdftotext", "-layout", pdf_path, txt_path], check=True)
    with open(txt_path, encoding="utf-8") as f:
        content = f.read()
    pages = content.split("\x0c")
    norm_pages = [re.sub(r"\s+", " ", p) for p in pages]
    lookup = {}
    for display, search, level in TOC_ENTRIES:
        norm_search = re.sub(r"\s+", " ", search).strip()
        found = None
        page_range = range(1, len(norm_pages) + 1)
        if search not in BEFORE_TOC:
            page_range = reversed(list(page_range))
        for i in page_range:
            if norm_search in norm_pages[i - 1]:
                found = i
                break
        if found is None:
            print("  [WARN] not found on any page:", search)
        lookup[search] = found if found is not None else "?"
    return lookup

if __name__ == "__main__":
    print("== Pass 1: placeholder TOC ==")
    p1_md = assemble(build_toc_markdown(None), "assembled_pass1.md")
    run_pandoc(p1_md, "assembled_pass1.docx")
    run_soffice("assembled_pass1.docx", "/tmp/lo_pass1")
    page_map = extract_page_map("assembled_pass1.pdf", "assembled_pass1.txt")
    unresolved = [k for k, v in page_map.items() if v == "?"]
    print(f"Resolved {len(page_map) - len(unresolved)}/{len(page_map)} TOC page numbers.")
    if unresolved:
        print("UNRESOLVED:", unresolved)

    print("== Pass 2: final TOC with real page numbers ==")
    p2_md = assemble(build_toc_markdown(page_map), "AMIU_Strategic_Blueprint_Premium.md")
    run_pandoc(p2_md, "AMIU_Strategic_Blueprint_Premium.docx")
    run_soffice("AMIU_Strategic_Blueprint_Premium.docx", "/tmp/lo_pass2")
    print("DONE ->", "AMIU_Strategic_Blueprint_Premium.docx / .pdf")
