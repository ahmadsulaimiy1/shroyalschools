#!/usr/bin/env python3
"""Two-pass assembly for the AMIU Constitution — Flagship Governance Edition.
Reuses the exact reference.docx (fonts/styles) and several structural
post-processing passes already built and proven for the Blueprint, imported
directly rather than re-implemented, so both flagship publications share one
underlying pipeline as well as one design system."""
import subprocess, re, sys, os

ROOT = "/home/user/shroyalschools"
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "assets"))

from assemble import (
    _justify_body_text, _enable_hyphenation, _suppress_table_hyphenation,
    _isolate_closing_panel_header_footer, _prevent_row_splitting, _insert_cover_seal,
    _retitle_header_footer, _style_premium_tables, _balance_column_widths,
)

FRONT = "assets/constitution_front.md"
BODY = "work_constitution_body.md"
BACK = "assets/constitution_back.md"
REFDOC = "assets/amiu-reference.docx"

MARKER = "<<<TOC_PLACEHOLDER>>>"

ROMANS = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII",
          "XIV","XV","XVI","XVII","XVIII","XIX","XX","XXI","XXII","XXIII"]
ARTICLE_TITLES = [
    "Definitions", "Legal Identity", "Mission, Vision and Values", "Interpretation",
    "Governance Structure", "Board of Trustees", "President & Vice-Chancellor",
    "University Senate", "Administration", "Academic Program", "Waqf and Endowment",
    "Students' Rights and Responsibilities", "Faculty Rights and Responsibilities",
    "Financial Sustainability", "Transparency and Accountability", "Independent Officers",
    "Records and Archives", "Amendment", "Transitional Provisions", "Dissolution",
    "Non-Political and Non-Profit Provisions", "Indemnification", "Final Provisions",
]

TOC_ENTRIES = [
    ("Document Control", "Document Control", 1),
    ("Constitutional Declaration", "Constitutional Declaration", 1),
    ("Preamble", "Preamble", 1),
    ("Governance Architecture", "Governance Architecture", 1),
    ("Academic Framework", "Academic Framework", 1),
    ("The ISLAMIC Framework", "The ISLAMIC Framework", 1),
]
for n, (roman, title) in enumerate(zip(ROMANS, ARTICLE_TITLES), start=1):
    TOC_ENTRIES.append((f"Article {roman} — {title}", f"Article {n} of 23", 1))
TOC_ENTRIES += [
    ("Adoption", "Adoption", 1),
    ("Publication Certification Statement", "Publication Certification Statement", 1),
]

BEFORE_TOC = {"Document Control", "Constitutional Declaration", "Preamble",
              "Governance Architecture", "Academic Framework", "The ISLAMIC Framework"}

def build_toc_markdown(page_lookup=None):
    lines = []
    lines.append('## Table of Contents {.unnumbered}\n')
    lines.append("| | |")
    lines.append("|---|---:|")
    for display, search, level in TOC_ENTRIES:
        pg = "•" if page_lookup is None else str(page_lookup.get(search, "—"))
        lines.append(f"| **{display}** | **{pg}** |")
    lines.append("")
    lines.append('```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```')
    lines.append("")
    return "\n".join(lines)

def assemble(toc_markdown, outpath):
    parts = []
    with open(FRONT, encoding="utf-8") as f:
        front = f.read()
    front = front.replace(MARKER, toc_markdown)
    parts.append(front)
    parts.append('# Main Contents {.unnumbered}\n')
    with open(BODY, encoding="utf-8") as f:
        parts.append(f.read())
    with open(BACK, encoding="utf-8") as f:
        parts.append(f.read())
    full = "\n\n".join(parts)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(full)
    return outpath

PROVISION_RE = re.compile(r'^\d+(\.\d+)+$')

def _style_provision_numbers(docx_path):
    """Numbered legal provisions ('6.1.1 The Board shall...') are authored as
    a bold leading number followed by plain text in the same paragraph.
    Detected structurally (bold first run whose text is a pure dotted-number
    token) rather than a style whitelist, since ~400 provisions across 23
    Articles were authored as plain paragraphs, not a custom style. Recolors
    the number gold and gives the paragraph a hanging indent so it reads as
    book-typeset legal text rather than a Word auto-numbered list."""
    import docx as _docx
    from docx.shared import Pt as _Pt, RGBColor as _RGBColor
    from docx.oxml.ns import qn as _qn
    from docx.oxml import OxmlElement as _El

    GOLD = _RGBColor(0xB0, 0x86, 0x25)
    d = _docx.Document(docx_path)
    n = 0
    for p in d.paragraphs:
        if not p.runs:
            continue
        first = p.runs[0]
        text = first.text.strip()
        if not first.font.bold:
            continue
        if not PROVISION_RE.match(text):
            continue
        first.font.color.rgb = GOLD
        pPr = p._p.get_or_add_pPr()
        ind = pPr.find(_qn('w:ind'))
        if ind is None:
            ind = _El('w:ind')
            pPr.append(ind)
        ind.set(_qn('w:left'), '360')
        ind.set(_qn('w:hanging'), '360')
        n += 1
    d.save(docx_path)
    print(f"  styled {n} numbered provisions")

def run_pandoc(md_path, docx_path):
    subprocess.run(["pandoc", md_path, "-o", docx_path, f"--reference-doc={REFDOC}"], check=True)
    _prevent_row_splitting(docx_path)
    _style_premium_tables(docx_path)
    _balance_column_widths(docx_path)
    _justify_body_text(docx_path)
    _enable_hyphenation(docx_path)
    _suppress_table_hyphenation(docx_path)
    _style_provision_numbers(docx_path)
    _isolate_closing_panel_header_footer(docx_path)
    _retitle_header_footer(docx_path, "Constitution · Flagship Governance Edition", "AMIU-CON-001")
    _insert_cover_seal(docx_path)

def run_soffice(docx_path, profile):
    subprocess.run(["rm", "-rf", profile], check=False)
    os.makedirs(profile, exist_ok=True)
    subprocess.run(["soffice", "--headless", f"-env:UserInstallation=file://{profile}",
                     "--convert-to", "pdf", docx_path], check=True, capture_output=True)

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
    p1_md = assemble(build_toc_markdown(None), "assembled_con_pass1.md")
    run_pandoc(p1_md, "assembled_con_pass1.docx")
    run_soffice("assembled_con_pass1.docx", "/tmp/lo_con_pass1")
    page_map = extract_page_map("assembled_con_pass1.pdf", "assembled_con_pass1.txt")
    unresolved = [k for k, v in page_map.items() if v == "?"]
    print(f"Resolved {len(page_map) - len(unresolved)}/{len(page_map)} TOC page numbers.")
    if unresolved:
        print("UNRESOLVED:", unresolved)

    print("== Pass 2: final TOC with real page numbers ==")
    p2_md = assemble(build_toc_markdown(page_map), "AMIU_Constitution.md")
    run_pandoc(p2_md, "AMIU_Constitution.docx")
    run_soffice("AMIU_Constitution.docx", "/tmp/lo_con_pass2")
    print("DONE -> AMIU_Constitution.docx / .pdf")
