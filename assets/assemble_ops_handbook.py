#!/usr/bin/env python3
"""Two-pass assembly for the AMIU Operations Handbook (OPS-001 through
OPS-027). Reuses the exact reference.docx (fonts/styles) and structural
post-processing passes already built and proven for the Blueprint,
Constitution, Institutional Governance Compendium, Academic Handbook, and
Student Policies Handbook, imported directly rather than re-implemented, so
all six flagship publications share one underlying pipeline and one design
system."""
import subprocess, re, sys, os

ROOT = "/home/user/shroyalschools"
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "assets"))

from assemble import (
    _justify_body_text, _enable_hyphenation, _suppress_table_hyphenation,
    _isolate_closing_panel_header_footer, _prevent_row_splitting, _insert_cover_seal,
    _retitle_header_footer, _style_premium_tables, _balance_column_widths,
)
from gen_ops_handbook_body import POLICIES

FRONT = "assets/ops_handbook_front.md"
BODY = "work_ops_handbook_body.md"
BACK = "assets/ops_handbook_back.md"
REFDOC = "assets/amiu-reference.docx"

MARKER = "<<<TOC_PLACEHOLDER>>>"

TOC_ENTRIES = [
    ("Document Control", "Document Control", 1),
    ("Operations Policies Declaration", "Operations Policies Declaration", 1),
]
for (num, code, title, steward, owner, authority, thesis, sections) in POLICIES:
    TOC_ENTRIES.append((f"{code} — {title}", f"Operations Handbook &#183; Policy {num} of 27", 1))
TOC_ENTRIES += [
    ("Publication Certification Statement", "Publication Certification Statement", 1),
]

BEFORE_TOC = {"Document Control", "Operations Policies Declaration"}

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

def run_pandoc(md_path, docx_path):
    subprocess.run(["pandoc", md_path, "-o", docx_path, f"--reference-doc={REFDOC}"], check=True)
    _prevent_row_splitting(docx_path)
    _style_premium_tables(docx_path)
    _balance_column_widths(docx_path)
    _justify_body_text(docx_path)
    _enable_hyphenation(docx_path)
    _suppress_table_hyphenation(docx_path)
    _isolate_closing_panel_header_footer(docx_path)
    _retitle_header_footer(docx_path, "Operations Handbook", "AMIU-OPSH-001")
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
        norm_search = norm_search.replace("&#183;", "·")
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
    p1_md = assemble(build_toc_markdown(None), "assembled_opsh_pass1.md")
    run_pandoc(p1_md, "assembled_opsh_pass1.docx")
    run_soffice("assembled_opsh_pass1.docx", "/tmp/lo_opsh_pass1")
    page_map = extract_page_map("assembled_opsh_pass1.pdf", "assembled_opsh_pass1.txt")
    unresolved = [k for k, v in page_map.items() if v == "?"]
    print(f"Resolved {len(page_map) - len(unresolved)}/{len(page_map)} TOC page numbers.")
    if unresolved:
        print("UNRESOLVED:", unresolved)

    print("== Pass 2: final TOC with real page numbers ==")
    p2_md = assemble(build_toc_markdown(page_map), "AMIU_Operations_Handbook_2028.md")
    run_pandoc(p2_md, "AMIU_Operations_Handbook_2028.docx")
    run_soffice("AMIU_Operations_Handbook_2028.docx", "/tmp/lo_opsh_pass2")
    print("DONE -> AMIU_Operations_Handbook_2028.docx / .pdf")
