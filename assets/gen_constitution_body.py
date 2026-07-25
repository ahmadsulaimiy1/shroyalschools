#!/usr/bin/env python3
"""Generate work_constitution_body.md: 23 Article hero-spread dividers
(reusing the exact navy-panel visual system built for the Blueprint's Part
dividers) interleaved with the Constitution's article text. Editorial fixes
applied here (not left for a later pass): 'DVC Administration & Finance' ->
'DVC Admin & Finance' throughout, to match the Blueprint's own canonical
term; Section 6.3.1.3's citation normalized from 'Article 3, Section 3.3' to
'Section 3.3'; Section 6.3.4.2 cross-referenced to the Section 6.4 removal
process it was silently duplicating without a defined procedure."""

PATH = "/home/user/shroyalschools/work_constitution_body.md"

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace("'", "’"))

# (roman, title, secrange, thesis, [(secnum, title), ...])
ARTICLES = [
("I", "Definitions", "Sections 1.1–1.2",
 "Forty-six terms, defined once, binding everywhere this Constitution uses them.",
 [("1.1", "General Definitions"), ("1.2", "Interpretation")]),
("II", "Legal Identity", "Sections 2.1–2.7",
 "A Texas-domiciled 501(c)(3) religious educational corporation, incorporated 6 December 2027 — one name, one seal, one governing law.",
 [("2.1", "Name"), ("2.2", "Legal Status"), ("2.3", "Legal Domicile"), ("2.4", "Date of Establishment"),
  ("2.5", "Official Seal"), ("2.6", "Powers of the University"), ("2.7", "Governing Law")]),
("III", "Mission, Vision and Values", "Sections 3.1–3.4",
 "To spread Islamic education worldwide at the minimum possible cost — governed by the ISLAMIC framework in every decision this Constitution authorizes.",
 [("3.1", "Mission"), ("3.2", "Vision"), ("3.3", "Values"), ("3.4", "Tagline")]),
("IV", "Interpretation", "Sections 4.1–4.3",
 "Who resolves an ambiguity, how a dispute is settled, and what survives if a single provision falls.",
 [("4.1", "Interpretation Authority"), ("4.2", "Dispute Resolution"), ("4.3", "Severability")]),
("V", "Governance Structure", "Sections 5.1–5.5",
 "A bicameral architecture — Board and Senate, co-equal in their own domains, meeting at a single operational link.",
 [("5.1", "Governance Hierarchy"), ("5.2", "Bicameral Governance"), ("5.3", "Separation of Powers"),
  ("5.4", "Non-Delegation"), ("5.5", "Conflict Resolution between Governance Bodies")]),
("VI", "Board of Trustees", "Sections 6.1–6.9",
 "Seven to eleven external Trustees, fiduciary stewards of the University's long-term health, bound by a defined process before any one of them can be removed.",
 [("6.1", "Role and Authority"), ("6.2", "Composition"), ("6.3", "Trustee Qualifications and Appointment"),
  ("6.4", "Removal from Office"), ("6.5", "Chairperson"), ("6.6", "Meetings"), ("6.7", "Responsibilities"),
  ("6.8", "Code of Conduct"), ("6.9", "Committees")]),
("VII", "President & Vice-Chancellor", "Sections 7.1–7.6",
 "The single operational link between Board and Senate — appointed for five years, evaluated annually, removable only for cause.",
 [("7.1", "Role and Authority"), ("7.2", "Appointment"), ("7.3", "Eligibility"), ("7.4", "Responsibilities"),
  ("7.5", "Performance Evaluation"), ("7.6", "Resignation and Removal")]),
("VIII", "University Senate", "Sections 8.1–8.8",
 "Eighteen fixed seats across four groups — supreme academic authority, answerable to no one but itself in matters of curriculum, instruction, and degrees.",
 [("8.1", "Role and Authority"), ("8.2", "Composition"), ("8.3", "Ex-Officio Members"), ("8.4", "Eligibility"),
  ("8.5", "Meetings"), ("8.6", "Voting Procedures"), ("8.7", "Responsibilities"), ("8.8", "Vacancies")]),
("IX", "Administration", "Sections 9.1–9.4",
 "The executive management arm that turns Board policy and Senate academic vision into daily operations.",
 [("9.1", "Role and Authority"), ("9.2", "Composition"), ("9.3", "Appointment"), ("9.4", "Responsibilities")]),
("X", "Academic Program", "Sections 10.1–10.3",
 "A seven-tier credential ladder, fully stackable, taught through six founding colleges, primarily in English.",
 [("10.1", "Academic Ladder"), ("10.2", "The Six Colleges"), ("10.3", "Language of Instruction")]),
("XI", "Waqf and Endowment", "Sections 11.1–11.2",
 "A fiduciary board, a fixed share of gross revenue, and an unbroken commitment to scholarships, mosques, and the world's poorest students.",
 [("11.1", "Waqf Board"), ("11.2", "Waqf Reserve")]),
("XII", "Students' Rights and Responsibilities", "Sections 12.1–12.3",
 "Non-discriminatory admission and dignity, in return for integrity — the reciprocal obligation between the University and every student it enrolls.",
 [("12.1", "Admission"), ("12.2", "Rights"), ("12.3", "Responsibilities")]),
("XIII", "Faculty Rights and Responsibilities", "Sections 13.1–13.2",
 "Academic freedom exercised within, not against, the University's Islamic identity.",
 [("13.1", "Academic Freedom"), ("13.2", "Responsibilities")]),
("XIV", "Financial Sustainability", "Sections 14.1–14.3",
 "A zero-deficit model, a twenty-five percent contingency reserve, and tuition priced so financial capacity is never the barrier.",
 [("14.1", "Revenue Model"), ("14.2", "Tuition"), ("14.3", "Compensation")]),
("XV", "Transparency and Accountability", "Sections 15.1–15.4",
 "An annual report, an independent audit, disclosed conflicts of interest, and protection for anyone who reports misconduct in good faith.",
 [("15.1", "Annual Report"), ("15.2", "Audit"), ("15.3", "Conflict of Interest"), ("15.4", "Whistleblower Protection")]),
("XVI", "Independent Officers", "Sections 16.1–16.3",
 "The Secretary, the Registrar, and the General Counsel — three offices that keep the University's own records and law honest.",
 [("16.1", "Secretary to the Board"), ("16.2", "University Registrar"), ("16.3", "General Counsel")]),
("XVII", "Records and Archives", "Sections 17.1–17.2",
 "What the University keeps, for how long, and who is allowed to see it.",
 [("17.1", "Official Records"), ("17.2", "Access to Records")]),
("XVIII", "Amendment", "Sections 18.1–18.2",
 "Two-thirds of the Board, thirty days' notice, and a filing with the Texas Secretary of State — the only door through which this Constitution may be changed.",
 [("18.1", "Amendment Procedure"), ("18.2", "Effective Date")]),
("XIX", "Transitional Provisions", "Section 19.1",
 "How every prior governing document, appointment, and policy carries forward into this one without a gap in authority.",
 [("19.1", "Transitional Provisions")]),
("XX", "Dissolution", "Section 20.1",
 "A unanimous Board vote, and every remaining asset to another 501(c)(3) charitable purpose — never to a person.",
 [("20.1", "Dissolution")]),
("XXI", "Non-Political and Non-Profit Provisions", "Sections 21.1–21.3",
 "No private inurement, no political campaigning, no activity beyond what Section 501(c)(3) permits.",
 [("21.1", "Private Inurement"), ("21.2", "Political Activities"), ("21.3", "Tax-Exempt Compliance")]),
("XXII", "Indemnification", "Section 22.1",
 "Protection for every Trustee, officer, employee, and agent who serves the University in good faith — and none for gross negligence or willful misconduct.",
 [("22.1", "Indemnification of Trustees, Officers, Employees, and Agents")]),
("XXIII", "Final Provisions", "Sections 23.1–23.2",
 "This Constitution's own supremacy, restated once more, in its final words.",
 [("23.1", "Supremacy"), ("23.2", "Effective Date")]),
]

def hero_spread(roman, title, secrange, thesis, sections, article_no, total=23):
    tlen = len(title)
    tsize = 30 if tlen <= 30 else (26 if tlen <= 45 else 23)
    rows = []
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="120"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Cinzel" w:hAnsi="Cinzel"/><w:color w:val="8C97AB"/><w:sz w:val="17"/><w:spacing w:val="24"/></w:rPr><w:t>ARTICLE {article_no} OF {total}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Cinzel" w:hAnsi="Cinzel"/><w:color w:val="B08625"/><w:b/><w:sz w:val="100"/></w:rPr><w:t>{roman}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="120" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Cormorant Garamond" w:hAnsi="Cormorant Garamond"/><w:color w:val="FFFFFF"/><w:b/><w:sz w:val="{tsize*2}"/></w:rPr><w:t>{esc(title)}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="260"/><w:pBdr><w:bottom w:val="single" w:sz="10" w:space="8" w:color="B08625"/></w:pBdr></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans"/><w:color w:val="8C97AB"/><w:sz w:val="17"/><w:spacing w:val="14"/></w:rPr><w:t>{secrange.upper()}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="360"/><w:ind w:right="700"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Cormorant Garamond" w:hAnsi="Cormorant Garamond"/><w:i/><w:color w:val="DCE3F0"/><w:sz w:val="25"/></w:rPr><w:t>&#8220;{esc(thesis)}&#8221;</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="140"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans"/><w:color w:val="B08625"/><w:b/><w:sz w:val="16"/><w:spacing w:val="20"/></w:rPr><w:t>SECTIONS OF THIS ARTICLE</w:t></w:r></w:p>''')
    for num, sec_title in sections:
        rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="110"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Cinzel" w:hAnsi="Cinzel"/><w:color w:val="B08625"/><w:b/><w:sz w:val="19"/></w:rPr><w:t>{num}&#8194;</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans"/><w:color w:val="FFFFFF"/><w:sz w:val="18"/></w:rPr><w:t>{esc(sec_title)}</w:t></w:r></w:p>''')

    body = "\n".join(rows)
    return f'''```{{=openxml}}
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
    <w:trPr><w:trHeight w:val="12200" w:hRule="atLeast"/><w:cantSplit/></w:trPr>
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

def main():
    parts = []
    for i, (roman, title, secrange, thesis, sections) in enumerate(ARTICLES, start=1):
        parts.append(hero_spread(roman, title, secrange, thesis, sections, i))
        parts.append(f'<!-- ARTICLE {roman}: {title} — body content goes here -->\n')
    with open(PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Wrote {len(ARTICLES)} article dividers to {PATH}")

if __name__ == "__main__":
    main()
