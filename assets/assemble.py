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
     [(11, "Program Portfolio"), (12, "Curriculum Architecture"), (13, "Student Journey Map"),
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

ROMAN_TO_WORD = {"I": "One", "II": "Two", "III": "Three", "IV": "Four", "V": "Five",
                  "VI": "Six", "VII": "Seven", "VIII": "Eight"}

# TOC-display-only shortenings: the search text (used for page lookup) must
# stay the exact full heading text, but the narrow TOC column can wrap a
# trailing year range ("2028–2050") onto its own line — no other Section
# entry carries one, so trimming it here (not in the body heading itself)
# keeps the row visually consistent with every other Section row.
TOC_TITLE_OVERRIDE = {1: "Institutional Vision"}

for roman, title, secrange, sections in PART_TITLES:
    # Search text targets the hero-spread's small-caps kicker line
    # ("PART FOUR OF EIGHT"), which is short, wrap-proof, and appears
    # exactly once in the whole document (only on that Part's divider page) —
    # this sidesteps both the long-title page-wrap bug and the TOC's-own-row
    # duplicate-occurrence ambiguity that affect the full title string.
    TOC_ENTRIES.append((f"Part {roman} — {title}", f"Part {ROMAN_TO_WORD[roman]} of Eight", 1))
    for num, sec_title in sections:
        toc_title = TOC_TITLE_OVERRIDE.get(num, sec_title)
        TOC_ENTRIES.append((f"Section {num}: {toc_title}", f"Section {num}: {sec_title}", 2))

TOC_ENTRIES += [
    ("Appendix A — Cross-Reference to the Ten-Year Master Plan (AMIU-MP-001)",
     "Appendix A — Cross-Reference", 1),
    ("Appendix B — Master Plan Exhibit Checklist", "Appendix B — Master Plan Exhibit Checklist", 1),
    ("Appendix C — Fixed Revenue Allocation Framework: Quick Reference",
     "Appendix C — Fixed Revenue Allocation Framework: Quick Reference", 1),
    ("Appendix D — Program Catalog Reference", "Appendix D — Program Catalog Reference", 1),
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

def _retitle_header_footer(docx_path, title_text, doc_ref):
    """Both flagship publications share one amiu-reference.docx, whose
    default header/footer text is hardcoded to the Blueprint's own title
    ('Strategic Implementation Blueprint 2028-2050') and document code
    ('AMIU-SB-002') -- correct for the Blueprint, wrong for anything else
    built from the same reference doc. Retexts the title run in the main
    section's header and the document-reference run in its footer after
    pandoc conversion. No-op (returns quietly) if the expected runs aren't
    found, rather than silently leaving stale text in place undetected."""
    import docx as _docx
    d = _docx.Document(docx_path)
    section = d.sections[0]
    retitled_header = retitled_footer = False
    for p in section.header.paragraphs:
        for r in p.runs:
            if 'Strategic Implementation Blueprint' in r.text:
                r.text = title_text
                retitled_header = True
    for p in section.footer.paragraphs:
        for r in p.runs:
            if r.text.strip() == 'AMIU-SB-002':
                r.text = doc_ref
                retitled_footer = True
    d.save(docx_path)
    if not (retitled_header and retitled_footer):
        print(f"  [WARN] _retitle_header_footer: header={retitled_header} footer={retitled_footer} "
              f"— expected run(s) not found, header/footer text may still read 'Blueprint'/AMIU-SB-002")

SEAL_PATH = "assets/brand/amiu_seal_medallion.png"

def _insert_cover_seal(docx_path, seal_path=SEAL_PATH):
    """Place the official AMIU seal at the top of the cover — the first
    navy-fill table in the document. The seal's source artwork sits on a
    plain white background with anti-aliased edges; rather than chroma-key
    it directly onto navy (tested, and it leaves a visible light halo
    around the globe/crown linework), it's presented on its own cream
    medallion disc with a thin gold ring — the standard real-world
    convention for a dark-background institutional seal, and it sidesteps
    the halo entirely since the medallion's own background is a clean
    flat fill, not a matted edge."""
    import os
    if not os.path.exists(seal_path):
        return
    import docx as _docx
    from docx.shared import Inches as _Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH as _ALIGN
    from docx.oxml.ns import qn as _qn
    import copy as _copy

    d = _docx.Document(docx_path)
    target = None
    for t in d.tables:
        for shd in t._tbl.iter(_qn('w:shd')):
            if shd.get(_qn('w:fill')) == '122A4E':
                target = t
                break
        if target is not None:
            break
    if target is None:
        return

    cell = target.rows[0].cells[0]
    first_p = cell.paragraphs[0]
    new_p_elem = _copy.deepcopy(first_p._p)
    # Strip any existing runs from the clone; it becomes the image paragraph
    for child in list(new_p_elem):
        if child.tag == _qn('w:r'):
            new_p_elem.remove(child)
    first_p._p.addprevious(new_p_elem)
    from docx.text.paragraph import Paragraph as _Paragraph
    seal_p = _Paragraph(new_p_elem, cell)
    seal_p.alignment = _ALIGN.CENTER
    seal_p.paragraph_format.space_before = _docx.shared.Pt(0)
    seal_p.paragraph_format.space_after = _docx.shared.Pt(14)
    run = seal_p.add_run()
    run.add_picture(seal_path, width=_Inches(1.15))

    d.save(docx_path)

def run_pandoc(md_path, docx_path):
    subprocess.run(["pandoc", md_path, "-o", docx_path, f"--reference-doc={REFDOC}"], check=True)
    _prevent_row_splitting(docx_path)
    _style_subheading_labels(docx_path)
    _apply_callout_boxes(docx_path)
    _style_premium_tables(docx_path)
    _balance_column_widths(docx_path)
    _justify_body_text(docx_path)
    _enable_hyphenation(docx_path)
    _suppress_table_hyphenation(docx_path)
    _isolate_closing_panel_header_footer(docx_path)
    _insert_cover_seal(docx_path)

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

def _suppress_table_hyphenation(docx_path):
    """Document-wide autoHyphenation (see _enable_hyphenation) is a body-prose
    feature: it belongs in justified narrative paragraphs, not in narrow
    two-column list/TOC-style tables, where a bold row like 'Governance &
    Institutional Foundations' hyphenating mid-word ('IN-STITUTIONAL') looks
    like stray typography in what's meant to read as a clean navigational
    list, not a paragraph.

    Wide, many-column data tables (document registries, cross-reference
    matrices, responsibility assignments — the same >= 4-column tables
    _balance_column_widths targets) are deliberately EXCLUDED from this
    suppression: a genuinely long single word ('Implementation',
    'Administration') in a narrow column has to break somewhere, and a real
    hyphen ('Implementa-tion') is the correct, professional way to do that —
    suppressing hyphenation there just traded a clean hyphenated break for
    an uglier bare character-orphan break ('Implementatio' / 'n') with no
    hyphen mark at all, which is a worse-looking defect, not a better one."""
    import docx as _docx
    from docx.oxml.ns import qn as _qn
    from docx.oxml import OxmlElement as _El
    MIN_COLS_TO_ALLOW_HYPHENATION = 4
    d = _docx.Document(docx_path)
    for table in d.tables:
        rows = table.rows
        ncols = len(rows[0].cells) if rows else 0
        if ncols >= MIN_COLS_TO_ALLOW_HYPHENATION:
            continue
        for row in rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    pPr = p._p.get_or_add_pPr()
                    if pPr.find(_qn('w:suppressAutoHyphens')) is None:
                        pPr.append(_El('w:suppressAutoHyphens'))
    d.save(docx_path)

def _isolate_closing_panel_header_footer(docx_path):
    """Give the closing navy panel (the document's final page, its de facto
    back cover) its own section with a blank header/footer — mirroring the
    front cover, which already gets a blank first-page header/footer via
    build_reference.py. Without this the front and back covers don't match:
    the front is clean and the back still carries the running administrative
    header/footer. Detected structurally (the last navy-fill, w:dropCap-free
    full-bleed table in the document, per the same fill color the hero-spread
    Part dividers and this closing panel share) and isolated by inserting a
    real section break — validated empirically in isolation beforehand that
    LibreOffice's headless conversion honors per-section header/footer
    boundaries correctly (unlike STYLEREF fields, which do not re-evaluate
    under this pipeline)."""
    import copy
    import docx as _docx
    from docx.oxml.ns import qn as _qn

    d = _docx.Document(docx_path)
    navy_tables = []
    for t in d.tables:
        for shd in t._tbl.iter(_qn('w:shd')):
            if shd.get(_qn('w:fill')) == '122A4E':
                navy_tables.append(t)
                break
    if not navy_tables:
        return
    closing_tbl = navy_tables[-1]._tbl

    body = d.element.body
    children = list(body)
    try:
        idx = children.index(closing_tbl)
    except ValueError:
        return
    if idx < 1:
        return
    pagebreak_para = children[idx - 1]
    if pagebreak_para.tag != _qn('w:p'):
        return  # structure isn't what we expect; skip rather than risk corruption

    old_body_sectPr = body.find(_qn('w:sectPr'))
    if old_body_sectPr is None:
        return
    new_sectPr = copy.deepcopy(old_body_sectPr)
    pPr = pagebreak_para.find(_qn('w:pPr'))
    if pPr is None:
        pPr = _docx.oxml.OxmlElement('w:pPr')
        pagebreak_para.insert(0, pPr)
    pPr.append(new_sectPr)

    # CRITICAL: old_body_sectPr (now the closing panel's own sectPr, since
    # new_sectPr above is a deep COPY that keeps section 0's content-bearing
    # header/footer) still carries the ORIGINAL headerReference/
    # footerReference elements — i.e. it points at the exact same relationship
    # IDs, the exact same underlying header/footer parts, as section 0. If
    # left in place, setting is_linked_to_previous=False below is a no-op
    # (a reference already exists) and clearing "the closing section's"
    # paragraph text actually clears the SHARED part section 0 also uses,
    # silently blanking the header/footer on every other page in the
    # document. Stripping these references here makes the closing section
    # genuinely link-then-detach: python-docx sees no reference (inherits
    # section 0's content), then is_linked_to_previous=False below creates
    # a real, separate part copied from that inherited content, which is
    # then safe to clear without touching section 0's part.
    for ref_tag in ('w:headerReference', 'w:footerReference'):
        for ref in list(old_body_sectPr.findall(_qn(ref_tag))):
            old_body_sectPr.remove(ref)

    d.save(docx_path)

    # Re-open so python-docx re-reads the now-two-section structure, then
    # blank the final (closing-panel) section's header and footer.
    d = _docx.Document(docx_path)
    closing_section = d.sections[-1]
    closing_section.header.is_linked_to_previous = False
    closing_section.footer.is_linked_to_previous = False
    for p in closing_section.header.paragraphs:
        p.text = ""
    for p in closing_section.footer.paragraphs:
        p.text = ""
    d.save(docx_path)

    # Verify the fix actually held: section 0's header/footer must still
    # carry real text after the closing section was blanked, or this
    # function just reintroduced the exact bug it exists to prevent.
    d = _docx.Document(docx_path)
    main_header_text = "".join(p.text for p in d.sections[0].header.paragraphs)
    main_footer_text = "".join(p.text for p in d.sections[0].footer.paragraphs)
    if not main_header_text.strip() and not main_footer_text.strip():
        raise RuntimeError(
            "_isolate_closing_panel_header_footer: main section's header/footer "
            "came back empty after isolating the closing panel — the two "
            "sections are still sharing a header/footer part. Aborting the "
            "build rather than silently shipping blank running heads."
        )

def _is_ceremonial_navy_table(table):
    """Covers, closing panels, and Part/Article/Section hero-spread dividers
    are single-row, navy full-bleed tables whose text is deliberately
    hand-styled run by run — they must never be touched by generic table
    post-processing (the premium data-table styling below, the column-width
    balancer, or the eyebrow-label heuristic in _style_subheading_labels).

    Detected structurally by BOTH the navy fill ('122A4E') every ceremonial
    panel shares AND a single row: navy fill alone is no longer sufficient
    once _style_premium_tables runs earlier in the same pipeline, since it
    deliberately navy-fills the HEADER ROW of ordinary multi-row data tables
    too — a fill-only check would then misidentify every already-styled data
    table as ceremonial and skip it in every later pass. A ceremonial panel
    is always exactly one row (one big cell holding the whole stack of
    hand-placed paragraphs); a data table with a navy header always has a
    header row plus at least one body row."""
    from docx.oxml.ns import qn as _qn
    if len(table.rows) != 1:
        return False
    for shd in table._tbl.iter(_qn('w:shd')):
        if shd.get(_qn('w:fill')) == '122A4E':
            return True
    return False

NAVY_HEX = '122A4E'
GOLD_HEX = 'B08625'
BAND_TINT_HEX = 'E9EDF6'

def _style_premium_tables(docx_path):
    """Upgrade every ordinary data table (Board/Senate composition, document
    registries, growth projections, and the like) from a plain office-grid
    look to a designed blue-and-gold editorial exhibit: a solid navy header
    row in reversed (white) small-caps text, a gold hairline underscoring
    that header as a hierarchy indicator, and a pale alternating band down
    the body rows for reading comfort — the same navy/gold vocabulary the
    covers, dividers, and closing panels already use, extended to data
    tables instead of leaving them at the reference doc's generic style.

    Ceremonial navy tables (covers/dividers/closing panels) are skipped via
    _is_ceremonial_navy_table. Tables whose first row is entirely blank (the
    two-column Table of Contents, which has its own hierarchy via indentation
    and bold/plain weight) are also left alone rather than given a solid navy
    blank bar across the top.

    Header text is whitened by setting run-level color directly, not by
    editing the shared Word table style: build_reference.py already found
    (see its 'Executive table style' comment) that pandoc's per-run color
    from the Compact paragraph style overrides a table style's rPr color, so
    a style-only approach silently fails to actually turn the header text
    white. Setting run.font.color.rgb here bypasses that precedence entirely."""
    import docx as _docx
    from docx.shared import RGBColor as _RGBColor, Pt as _Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH as _ALIGN
    from docx.oxml.ns import qn as _qn
    from docx.oxml import OxmlElement as _El

    WHITE = _RGBColor(0xFF, 0xFF, 0xFF)

    def _set_cell_fill(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = tcPr.find(_qn('w:shd'))
        if shd is None:
            shd = _El('w:shd')
            tcPr.append(shd)
        shd.set(_qn('w:val'), 'clear')
        shd.set(_qn('w:color'), 'auto')
        shd.set(_qn('w:fill'), hex_color)

    def _set_cell_margins(cell, top, bottom, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = tcPr.find(_qn('w:tcMar'))
        if tcMar is None:
            tcMar = _El('w:tcMar')
            tcPr.append(tcMar)
        for side, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            m = tcMar.find(_qn(f'w:{side}'))
            if m is None:
                m = _El(f'w:{side}')
                tcMar.append(m)
            m.set(_qn('w:w'), str(val))
            m.set(_qn('w:type'), 'dxa')

    def _set_header_bottom_rule(cell, color, sz=16):
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = tcPr.find(_qn('w:tcBorders'))
        if tcBorders is None:
            tcBorders = _El('w:tcBorders')
            tcPr.append(tcBorders)
        bottom = tcBorders.find(_qn('w:bottom'))
        if bottom is None:
            bottom = _El('w:bottom')
            tcBorders.append(bottom)
        bottom.set(_qn('w:val'), 'single')
        bottom.set(_qn('w:sz'), str(sz))
        bottom.set(_qn('w:space'), '0')
        bottom.set(_qn('w:color'), color)

    def _vcenter(cell):
        tcPr = cell._tc.get_or_add_tcPr()
        vAlign = tcPr.find(_qn('w:vAlign'))
        if vAlign is None:
            vAlign = _El('w:vAlign')
            tcPr.append(vAlign)
        vAlign.set(_qn('w:val'), 'center')

    def _style_header_run(run):
        run.font.bold = True
        run.font.color.rgb = WHITE
        rpr = run._r.get_or_add_rPr()
        caps = rpr.find(_qn('w:caps'))
        if caps is None:
            rpr.append(_El('w:caps'))
        spc = rpr.find(_qn('w:spacing'))
        if spc is None:
            spc = _El('w:spacing')
            rpr.append(spc)
        spc.set(_qn('w:val'), '4')

    d = _docx.Document(docx_path)
    n_styled = 0
    for table in d.tables:
        if _is_ceremonial_navy_table(table):
            continue
        rows = table.rows
        if not rows:
            continue
        header_cells = rows[0].cells
        # A table only gets header treatment if pandoc itself marked row 0 as
        # a real header (w:tblHeader in its trPr). Checking cell text instead
        # ("is row 0 non-blank?") is unreliable: pandoc treats a markdown
        # table whose header cells are BOTH blank (e.g. the two-column
        # "| | |" Table of Contents) as headerless and collapses it away
        # entirely, so row 0 becomes the first real data row (e.g. "Document
        # Control | 3") — non-blank text, but not a header, and it must not
        # be painted as one.
        trPr = rows[0]._tr.find(_qn('w:trPr'))
        header_is_real = trPr is not None and trPr.find(_qn('w:tblHeader')) is not None

        if header_is_real:
            for cell in header_cells:
                _set_cell_fill(cell, NAVY_HEX)
                _set_cell_margins(cell, 130, 130)
                _set_header_bottom_rule(cell, GOLD_HEX, sz=16)
                _vcenter(cell)
                for p in cell.paragraphs:
                    for run in p.runs:
                        _style_header_run(run)
            body_rows = rows[1:]
        else:
            body_rows = rows

        for i, row in enumerate(body_rows):
            for cell in row.cells:
                _set_cell_margins(cell, 100, 100)
                _vcenter(cell)
                if i % 2 == 0:
                    _set_cell_fill(cell, BAND_TINT_HEX)
        n_styled += 1

    d.save(docx_path)
    print(f"  styled {n_styled} premium data tables")

def _balance_column_widths(docx_path):
    """Give wide, many-column data tables (document registries, cross-
    reference matrices, responsibility assignments) explicit, content-aware
    column widths instead of pandoc's even-split default.

    An even split across 6-7 columns starves whichever columns hold real
    prose ('Document', 'Policy Steward') down to just a few characters of
    width, forcing header labels and body text to wrap mid-word with no
    hyphen ('DOCUM' / 'ENT', 'Presiden' / 't') — found on the Section 17
    registry page during a visual spot-check after the premium table
    restyling made it easy to notice a table's proportions for the first
    time.

    Two-tier allocation, not a single relative-weight split: a first pass
    (an earlier version of this function) set each column's width purely
    proportional to a content-length score, which still let a short-word
    column (e.g. 'Important'/'Complete' in a Priority column) get crowded
    out by neighboring prose columns and wrap mid-word anyway. Instead:
    (1) every column first gets a hard FLOOR wide enough for its own longest
    single word — computed in dxa from an estimated per-character glyph
    width, with headers (bold, small-caps, letter-spaced by
    _style_premium_tables) given a size allowance for that — so a column can
    structurally never be narrower than a word it must display on one line;
    (2) only the leftover width beyond all the floors is then handed out
    proportionally to columns with genuinely long-form content (prose gets
    the extra room; short-code columns stay at their floor). Word/
    LibreOffice only honor explicit widths under a fixed table layout, so
    w:tblLayout is forced to 'fixed' wherever widths are set."""
    import docx as _docx, math as _math, re as _re
    from docx.oxml.ns import qn as _qn
    from docx.oxml import OxmlElement as _El

    # Split on whitespace AND slashes: a slash-joined compound like
    # "Synchronous/Asynchronous" (24 characters with no space) can still
    # wrap cleanly right after the slash, so it must not be treated as one
    # 24-character unbreakable token — that single outlier word was enough
    # to inflate its whole column's floor far past what real wrapping needs.
    _WORD_SPLIT_RE = _re.compile(r'[\s/]+')

    MIN_COLS = 4       # narrower tables don't exhibit this problem
    CHAR_DXA = 150      # rough average glyph width at this body size, in twips
    HEADER_INFLATE = 1.3  # bold + all-caps + letter-spacing render wider
    CELL_PAD_DXA = 280  # combined left+right cell margin already in use
    PAGE_TEXT_WIDTH_DXA = 9072  # 8.5in page, 1.1in margins each side (build_reference.py)

    d = _docx.Document(docx_path)
    n_balanced = 0
    for table in d.tables:
        if _is_ceremonial_navy_table(table):
            continue
        rows = table.rows
        if not rows:
            continue
        ncols = len(rows[0].cells)
        if ncols < MIN_COLS:
            continue
        if any(len(row.cells) != ncols for row in rows):
            continue  # merged/irregular rows — skip rather than risk corruption

        trPr0 = rows[0]._tr.find(_qn('w:trPr'))
        row0_is_header = trPr0 is not None and trPr0.find(_qn('w:tblHeader')) is not None

        col_word_max = [0] * ncols       # longest single word, any row
        col_header_word_max = [0] * ncols
        col_text_total = [0] * ncols     # for the "how much prose" growth score
        for ri, row in enumerate(rows):
            is_header_row = row0_is_header and ri == 0
            for ci, cell in enumerate(row.cells):
                text = cell.text.strip()
                words = [w for w in _WORD_SPLIT_RE.split(text) if w]
                wmax = max((len(w) for w in words), default=0)
                if is_header_row:
                    col_header_word_max[ci] = max(col_header_word_max[ci], wmax)
                else:
                    col_word_max[ci] = max(col_word_max[ci], wmax)
                    col_text_total[ci] += len(text)

        n_body_rows = max(len(rows) - (1 if row0_is_header else 0), 1)

        tblGrid = table._tbl.find(_qn('w:tblGrid'))
        existing_total = 0
        if tblGrid is not None:
            for gc in tblGrid.findall(_qn('w:gridCol')):
                wval = gc.get(_qn('w:w'))
                if wval:
                    existing_total += int(wval)
        # Pandoc's own default grid-table width is often narrower than the
        # full text column (e.g. 7917 dxa on a 9072 dxa column for a 6-column
        # table) — using it as the target would inherit that wasted margin
        # instead of fixing the crowding. Always target the full usable page
        # width instead, which is what actually gives long-word columns
        # (all-caps headers, "DVC, Administration & Finance") the room to
        # avoid a mid-word wrap.
        target_total = PAGE_TEXT_WIDTH_DXA

        floors = []
        growth_weights = []
        for ci in range(ncols):
            body_floor = col_word_max[ci] * CHAR_DXA + CELL_PAD_DXA
            header_floor = col_header_word_max[ci] * CHAR_DXA * HEADER_INFLATE + CELL_PAD_DXA + 220
            floors.append(max(body_floor, header_floor, 500))
            avg_len = col_text_total[ci] / n_body_rows
            growth_weights.append(_math.sqrt(avg_len))
        floor_total = sum(floors)

        if floor_total >= target_total:
            # Even the minimums don't fit — scale every floor down
            # proportionally rather than starving one column completely.
            scale = target_total / floor_total
            col_widths = [max(400, round(f * scale)) for f in floors]
        else:
            leftover = target_total - floor_total
            weight_total = sum(growth_weights) or 1.0
            col_widths = [round(f + leftover * (g / weight_total))
                          for f, g in zip(floors, growth_weights)]
        col_widths[-1] += target_total - sum(col_widths)  # absorb rounding drift

        tblPr = table._tbl.find(_qn('w:tblPr'))
        if tblPr is None:
            tblPr = _El('w:tblPr')
            table._tbl.insert(0, tblPr)
        layout = tblPr.find(_qn('w:tblLayout'))
        if layout is None:
            layout = _El('w:tblLayout')
            tblPr.append(layout)
        layout.set(_qn('w:type'), 'fixed')

        if tblGrid is None:
            tblGrid = _El('w:tblGrid')
            tblPr.addnext(tblGrid)
        for gc in list(tblGrid.findall(_qn('w:gridCol'))):
            tblGrid.remove(gc)
        for w in col_widths:
            gc = _El('w:gridCol')
            gc.set(_qn('w:w'), str(w))
            tblGrid.append(gc)

        for row in rows:
            for ci, cell in enumerate(row.cells):
                tcPr = cell._tc.get_or_add_tcPr()
                tcW = tcPr.find(_qn('w:tcW'))
                if tcW is None:
                    tcW = _El('w:tcW')
                    tcPr.append(tcW)
                tcW.set(_qn('w:w'), str(col_widths[ci]))
                tcW.set(_qn('w:type'), 'dxa')
        n_balanced += 1

    d.save(docx_path)
    print(f"  balanced column widths on {n_balanced} wide tables")

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
        # Deliberately NOT bumped to a heading-scale size: these labels recur
        # up to 10 times per section across 41 sections (400+ instances), so
        # they work as wayfinding through color/caps/tracking, not through
        # size competing with the section heading above them — sizing them
        # like true subsection headings would read as visual noise at that
        # repetition density, not authority.
        run.font.bold = True
        run.font.color.rgb = GOLD
        run.font.size = _Pt(11)
        rpr = run._r.get_or_add_rPr()
        caps = rpr.find(_qn('w:caps'))
        if caps is None:
            caps = _El('w:caps')
            rpr.append(caps)
        spc = rpr.find(_qn('w:spacing'))
        if spc is None:
            spc = _El('w:spacing')
            rpr.append(spc)
        spc.set(_qn('w:val'), '18')

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
        if _is_ceremonial_navy_table(table):
            continue
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
    # Despaced (not just whitespace-collapsed): LibreOffice's synthetic
    # small-caps rendering inserts a spurious space-like gap after a run's
    # initial full-height capital before the shrunk small-caps letters
    # (e.g. "Al-Mulk" extracts as "A L -M ULK"), fragmenting pdftotext's
    # word boundaries on every small-caps heading/kicker/running-head. This
    # is a rendering-layer artifact, not real content, so matching must
    # ignore all whitespace rather than merely collapsing runs of it.
    norm_pages = [re.sub(r"\s+", "", p).lower() for p in pages]
    lookup = {}
    for display, search, level in TOC_ENTRIES:
        norm_search = re.sub(r"\s+", "", search).strip().lower()
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
