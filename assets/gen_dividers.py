#!/usr/bin/env python3
"""Replace the plain-text Part dividers in work_body_dividers.md with full
navy hero-spread chapter openers (Vision-2030 / NEOM style full-page panels)."""
import re

PATH = "/home/user/shroyalschools/work_body_dividers.md"

PARTS = [
    ("I", "ONE", "Governance & Institutional Foundations", "Sections 1–5", 1,
     "The bicameral architecture — Board of Trustees and University Senate — that lets AMIU govern honestly at $224,747 in Year-1 revenue and still govern honestly at $93.9M in Year 20.",
     [(1, "Institutional Vision 2028–2050"), (2, "Mission, Values, and Identity"),
      (3, "Governance Framework"), (4, "Senate Structure"), (5, "Board Structure")]),
    ("II", "TWO", "Organizational & Academic Structure", "Sections 6–10", 6,
     "How six founding colleges, six departments, and an honoraria-based faculty scale from a lone Head of Department in 2028 to a fully staffed secular-school network by the 2040s — without ever redesigning the org chart.",
     [(6, "Organizational Chart"), (7, "Academic Master Plan"), (8, "College Structure"),
      (9, "Faculty Structure"), (10, "Department Structure")]),
    ("III", "THREE", "Curriculum & Student Journey", "Sections 11–15", 11,
     "The seventy-one-program portfolio, its credit-hour architecture, and the digital-first student journey that lets a Tier-4 applicant enroll, learn, and graduate without ever needing a campus.",
     [(11, "Programme Portfolio"), (12, "Curriculum Architecture"), (13, "Student Journey Map"),
      (14, "Admission Policies"), (15, "Faculty Recruitment Strategy")]),
    ("IV", "FOUR", "Research, Publishing, Partnerships & Accreditation", "Sections 16–20", 16,
     "Mentored research and open-access publishing built on existing faculty honoraria, and the exact, dated accreditation sequence that never gets reordered for convenience.",
     [(16, "Research Strategy"), (17, "Publishing Strategy"), (18, "Global Partnerships Strategy"),
      (19, "Accreditation Roadmap"), (20, "ISO 21001 Roadmap")]),
    ("V", "FIVE", "Digital Infrastructure, AI & Waqf Development", "Sections 21–25", 21,
     "The Moodle-based LMS ecosystem, a Sharī'ah-gated AI strategy, and the Waqf & Stakeholder Reserve's evolution into a diversified, perpetual Islamic endowment.",
     [(21, "LMS Ecosystem"), (22, "AI Strategy"), (23, "Digital Transformation Strategy"),
      (24, "Library Strategy"), (25, "Waqf Development Strategy")]),
    ("VI", "SIX", "Financial Growth, Marketing & Branding", "Sections 26–30", 26,
     "Scholarships as designed policy rather than promise, grassroots near-zero-CAC marketing, and a branded-house architecture that lets expansion extend — never dilute — the AMIU name.",
     [(26, "Scholarship Strategy"), (27, "Revenue Diversification Strategy"), (28, "Marketing Strategy"),
      (29, "Branding Strategy"), (30, "International Expansion Strategy")]),
    ("VII", "SEVEN", "Regional Campuses & Student Lifecycle", "Sections 31–35", 31,
     "The Nigeria Mega-University and Gulf cooperation strategies, framed honestly as funding targets rather than guarantees, alongside the student-support, alumni, and career frameworks a lean budget can actually carry.",
     [(31, "Nigeria Campus Strategy"), (32, "Gulf Cooperation Strategy"), (33, "Student Support Framework"),
      (34, "Alumni Framework"), (35, "Career Development Framework")]),
    ("VIII", "EIGHT", "Risk, Compliance, Sustainability & the 20-Year Roadmap", "Sections 36–40", 36,
     "The fourteen-risk register, the full compliance calendar, the zero-deficit sustainability doctrine, and the single consolidated milestone table that ties 2028 to 2050.",
     [(36, "Risk Management Framework"), (37, "Compliance Framework"), (38, "Financial Sustainability Framework"),
      (39, "Capital Development Framework"), (40, "Twenty-Year Strategic Roadmap")]),
]

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace("’", "’").replace("'", "’"))

def title_size(title):
    n = len(title)
    if n <= 30:
        return 34
    if n <= 45:
        return 30
    if n <= 60:
        return 26
    return 23

def hero_spread(roman, word, title, secrange, first_num, thesis, sections):
    tsize = title_size(title)
    rows = []
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="120"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans"/><w:color w:val="8C97AB"/><w:sz w:val="17"/><w:spacing w:val="26"/></w:rPr><w:t>PART {word} OF EIGHT</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Bitstream Charter" w:hAnsi="Bitstream Charter"/><w:color w:val="B08625"/><w:b/><w:sz w:val="108"/></w:rPr><w:t>{roman}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="120" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Bitstream Charter" w:hAnsi="Bitstream Charter"/><w:color w:val="FFFFFF"/><w:b/><w:sz w:val="{tsize*2}"/></w:rPr><w:t>{esc(title)}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="260"/><w:pBdr><w:bottom w:val="single" w:sz="10" w:space="8" w:color="B08625"/></w:pBdr></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans"/><w:color w:val="8C97AB"/><w:sz w:val="17"/><w:spacing w:val="14"/></w:rPr><w:t>{secrange.upper()}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="360"/><w:ind w:right="700"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Liberation Serif" w:hAnsi="Liberation Serif"/><w:i/><w:color w:val="DCE3F0"/><w:sz w:val="25"/></w:rPr><w:t>&#8220;{esc(thesis)}&#8221;</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="140"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans"/><w:color w:val="B08625"/><w:b/><w:sz w:val="16"/><w:spacing w:val="20"/></w:rPr><w:t>CONTENTS OF THIS PART</w:t></w:r></w:p>''')
    for num, sec_title in sections:
        rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="130"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Bitstream Charter" w:hAnsi="Bitstream Charter"/><w:color w:val="B08625"/><w:b/><w:sz w:val="21"/></w:rPr><w:t>{num:02d}&#8194;</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans"/><w:color w:val="FFFFFF"/><w:sz w:val="20"/></w:rPr><w:t>{esc(sec_title)}</w:t></w:r></w:p>''')

    body = "\n".join(rows)
    xml = f'''```{{=openxml}}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
<w:tbl>
  <w:tblPr>
    <w:tblW w:w="9350" w:type="dxa"/>
    <w:tblBorders>
      <w:top w:val="single" w:sz="10" w:space="0" w:color="B08625"/>
      <w:bottom w:val="single" w:sz="10" w:space="0" w:color="B08625"/>
    </w:tblBorders>
  </w:tblPr>
  <w:tblGrid><w:gridCol w:w="9350"/></w:tblGrid>
  <w:tr>
    <w:trPr><w:trHeight w:val="11100" w:hRule="atLeast"/><w:cantSplit/></w:trPr>
    <w:tc>
      <w:tcPr>
        <w:tcW w:w="9350" w:type="dxa"/>
        <w:shd w:val="clear" w:color="auto" w:fill="122A4E"/>
        <w:tcMar><w:top w:w="620" w:type="dxa"/><w:left w:w="620" w:type="dxa"/><w:bottom w:w="620" w:type="dxa"/><w:right w:w="620" w:type="dxa"/></w:tcMar>
        <w:vAlign w:val="center"/>
      </w:tcPr>
{body}
    </w:tc>
  </w:tr>
</w:tbl>
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

'''
    return xml

def main():
    with open(PATH, encoding="utf-8") as f:
        content = f.read()

    for roman, word, title, secrange, first_num, thesis, sections in PARTS:
        # Match the OLD divider block: leading page-break, "# Part ..." heading,
        # kicker/thesis/contents-list, trailing page-break — up to (not including)
        # the first Section heading that follows.
        title_re = re.escape(title)
        pattern = re.compile(
            r'```\{=openxml\}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'
            r'# Part ' + re.escape(roman) + r' — ' + title_re + r' \(' + re.escape(secrange) + r'\)\n'
            r'.*?'
            r'```\{=openxml\}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n',
            re.DOTALL
        )
        new_block = hero_spread(roman, word, title, secrange, first_num, thesis, sections)
        new_content, n = pattern.subn(new_block, content, count=1)
        if n != 1:
            print(f"[WARN] Part {roman}: pattern matched {n} times (expected 1)")
        else:
            content = new_content
            print(f"Part {roman}: replaced OK")

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
