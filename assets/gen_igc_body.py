#!/usr/bin/env python3
"""Author work_igc_body.md — the 25-Section body of the AMIU Institutional
Governance Compendium. Structured like gen_dividers.py (hero-spread navy
divider before each Section) plus hand-authored prose per Section, with the
data-heavy Sections 17-22 rendered from assets/igc_data.py so the corrected
priority/roadmap arithmetic can never drift out of sync with the itemized
registry again.

Two structural fixes from the editorial review are applied directly here,
not just in the tables:
  - Section 4.1's "Level 1-4" table is reframed with an explanatory note
    rather than implying a strict linear chain of command (Section 4.4's
    figure already shows Senate/Administration as parallel).
  - Section 4.4's ASCII-art organizational chart is replaced by a reference
    to Exhibit G1, the matplotlib-drawn parallel-structure diagram.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from igc_data import (
    DOCS, DOC_CODES, CATEGORY_ORDER, CATEGORY_NAMES, CATEGORY_TOTALS,
    PRIORITY_COUNTS, PRIORITY_PERCENTAGES, PHASE1_NUMS, PHASE2_NUMS,
    PHASE3_NUMS, PHASE4_NUMS, ranges, table_17_full_inventory,
    table_18_category, table_19_2_summary, table_20_category,
    table_22_1_roadmap,
)

OUT = "/home/user/shroyalschools/work_igc_body.md"

# ---------------------------------------------------------------------------
# Divider generator (mirrors gen_dividers.py's hero_spread pattern)
# ---------------------------------------------------------------------------

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def title_size(title):
    n = len(title)
    if n <= 25:
        return 44
    if n <= 38:
        return 36
    if n <= 52:
        return 28
    return 24

def divider(num, title, subrange, thesis, subsecs):
    tsize = title_size(title)
    rows = []
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="120"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:color w:val="8C97AB"/><w:sz w:val="19"/><w:spacing w:val="14"/></w:rPr><w:t>Section {num} of 25</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces Black" w:hAnsi="Fraunces Black"/><w:color w:val="B08625"/><w:b/><w:sz w:val="108"/></w:rPr><w:t>{num:02d}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="120" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces Black" w:hAnsi="Fraunces Black"/><w:color w:val="FFFFFF"/><w:b/><w:sz w:val="{tsize*2}"/></w:rPr><w:t>{esc(title)}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="260"/><w:pBdr><w:bottom w:val="single" w:sz="10" w:space="8" w:color="B08625"/></w:pBdr></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:color w:val="8C97AB"/><w:sz w:val="19"/><w:spacing w:val="10"/></w:rPr><w:t>{esc(subrange)}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="360"/><w:ind w:right="700"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces" w:hAnsi="Fraunces"/><w:i/><w:color w:val="DCE3F0"/><w:sz w:val="25"/></w:rPr><w:t>&#8220;{esc(thesis)}&#8221;</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="140"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:color w:val="B08625"/><w:b/><w:sz w:val="18"/><w:spacing w:val="12"/></w:rPr><w:t>Subsections</w:t></w:r></w:p>''')
    for subnum, subtitle in subsecs:
        rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="110"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Archivo SemiBold" w:hAnsi="Archivo SemiBold"/><w:color w:val="B08625"/><w:b/><w:sz w:val="19"/></w:rPr><w:t>{subnum}&#8194;</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Archivo" w:hAnsi="Archivo"/><w:color w:val="FFFFFF"/><w:sz w:val="18"/></w:rPr><w:t>{esc(subtitle)}</w:t></w:r></w:p>''')
    body = "\n".join(rows)
    height = 10800 + min(len(subsecs), 9) * 210
    # Hidden Heading-2 marker (see gen_dividers.py) so the running-header
    # STYLEREF field resolves to this Section on its own divider page instead
    # of carrying forward whatever Heading 2 preceded it.
    hidden_marker = (f'<w:p><w:pPr><w:pStyle w:val="Heading2"/><w:spacing w:before="0" w:after="0"/>'
                      f'<w:keepNext w:val="0"/><w:keepLines w:val="0"/>'
                      f'<w:pBdr><w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/></w:pBdr>'
                      f'<w:rPr><w:vanish/><w:sz w:val="2"/></w:rPr></w:pPr>'
                      f'<w:r><w:rPr><w:vanish/><w:sz w:val="2"/></w:rPr><w:t>Section {num}: {esc(title)}</w:t></w:r></w:p>')
    return f'''```{{=openxml}}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
{hidden_marker}
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
    <w:trPr><w:trHeight w:val="{height}" w:hRule="atLeast"/><w:cantSplit/></w:trPr>
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

def kicker(num, subnum):
    return f'::: {{custom-style="SectionKicker"}}\nSection {num} &#183; {subnum}\n:::\n'

PAGEBREAK = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'

# ---------------------------------------------------------------------------
# Section metadata: (num, title, subrange, thesis, [(subnum, subtitle), ...])
# ---------------------------------------------------------------------------
SECTIONS = [
 (1, "Introduction & Purpose", "Subsections 1.1–1.5",
  "One authoritative reference for every institutional governance and policy matter the University will face.",
  [("1.1","Preamble"),("1.2","Purpose of This Compendium"),("1.3","Scope of This Compendium"),
   ("1.4","Governance Principles"),("1.5","Document Numbering System")]),
 (2, "Institutional Identity", "Subsections 2.1–2.7",
  "A Texas-domiciled religious university built on a seven-tier academic ladder and six founding colleges.",
  [("2.1","Legal Identity"),("2.2","Mission"),("2.3","Vision (2037)"),("2.4","Tagline"),
   ("2.5","The AMIU Commitment"),("2.6","The Academic Ladder"),("2.7","The Six Colleges")]),
 (3, "The ISLAMIC Framework — Core Values", "Subsections 3.1–3.4",
  "Illumination, Sanad, Love, Access, Morality, Inquiry, Calling — seven values, one binding pledge.",
  [("3.1","Introduction"),("3.2","The ISLAMIC Framework"),("3.3","The ISLAMIC Framework — Detailed"),
   ("3.4","The ISLAMIC Pledge")]),
 (4, "Governance Hierarchy & Roles", "Subsections 4.1–4.4",
  "The Senate teaches and the Administration executes — parallel authorities, not a chain of command.",
  [("4.1","The Governance Hierarchy"),("4.2","The Board-Senate Relationship"),
   ("4.3","Senate Authority — Defined"),("4.4","Governance Structure — Exhibit G1")]),
 (5, "Board of Trustees — Composition, Roles & Requirements", "Subsections 5.1–5.6",
  "Five to nine Trustees, three-year terms, and fiduciary responsibility for the institution's long-term health.",
  [("5.1","Role & Authority"),("5.2","Composition"),("5.3","Chairperson of the Board"),
   ("5.4","Trustee Requirements"),("5.5","Board of Trustees Key Responsibilities"),
   ("5.6","Board of Trustees — Summary")]),
 (6, "President & Vice-Chancellor — Role & Authority", "Subsections 6.1–6.3",
  "The single operational link between the Board's strategy and the Senate's standards.",
  [("6.1","Role & Authority"),("6.2","President Requirements"),("6.3","President Key Responsibilities")]),
 (7, "University Senate — Composition, Rules & Procedures", "Subsections 7.1–7.9",
  "Eighteen voting seats across four groups, meeting monthly, deciding by simple majority.",
  [("7.1","Role & Authority"),("7.2","Senate Composition (18 Voting Seats)"),
   ("7.3","Senate Member Requirements"),("7.4","Senate Officers"),
   ("7.5","Senate Key Responsibilities"),("7.6","Senate Ex-Officio Members (Non-Voting)"),
   ("7.7","Senate Meetings"),("7.8","Quorum"),("7.9","Voting Procedures")]),
 (8, "Advisory & Proposing Framework", "Subsections 8.1–8.3",
  "Every stakeholder, from Trustee to student, has a defined channel to advise and to propose.",
  [("8.1","Purpose"),("8.2","Advisory and Proposing Framework"),("8.3","The Governance Principle")]),
 (9, "Administration — Deputy Vice-Chancellors, Deans & Directors", "Subsections 9.1–9.7",
  "Two Deputy Vice-Chancellors, six College Deans, and ten functional Directors execute the University's daily operations.",
  [("9.1","DVC, Academic Affairs"),("9.2","DVC, Administration & Finance"),("9.3","College Deans"),
   ("9.4","University Registrar"),("9.5","Dean of Students"),("9.6","Directors (Functional Areas)"),
   ("9.7","Summary Table — All Key Roles")]),
 (10, "Online & Distance Learning Governance", "Subsections 10.1–10.4",
  "The University's primary mode of delivery, governed as a first-class discipline, not an afterthought.",
  [("10.1","Purpose"),("10.2","Technology Governance"),("10.3","Virtual Governance Provisions"),
   ("10.4","Global Accessibility")]),
 (11, "Phased Institutional Growth Framework", "Subsections 11.1–11.4",
  "Fifteen institutional units at launch, forty-eight a decade later — growth that is triggered, not guessed at.",
  [("11.1","Overview"),("11.2","Office Growth Projection"),("11.3","Committee Growth Projection"),
   ("11.4","Growth Triggers")]),
 (12, "Year 1 — Core Institutional Structure", "Subsections 12.1–12.3",
  "Ten offices, five committees, and 347 students — the lean structure the University actually launches with.",
  [("12.1","Overview"),("12.2","Year 1 Offices (10)"),("12.3","Year 1 Committees (5)")]),
 (13, "Year 3 — Expanded Institutional Structure", "Subsections 13.1–13.3",
  "Sixteen offices and nine committees, expanded to match 1,606 students and the University's first two colleges.",
  [("13.1","Overview"),("13.2","Year 3 Offices (16)"),("13.3","Year 3 Committees (9)")]),
 (14, "Year 5 — Mature Institutional Structure", "Subsections 14.1–14.3",
  "All six colleges seated, 3,493 students enrolled, and international operations formally established.",
  [("14.1","Overview"),("14.2","Year 5 Offices (22)"),("14.3","Year 5 Committees (14)")]),
 (15, "Year 10 — Full Institutional Structure", "Subsections 15.1–15.3",
  "Twenty-nine offices, nineteen committees, 11,021 students — the full institutional structure this Compendium plans toward.",
  [("15.1","Overview"),("15.2","Year 10 Offices (29)"),("15.3","Year 10 Committees (19)")]),
 (16, "Compensation Philosophy & Framework", "Subsections 16.1–16.8",
  "Compensation as service to the Ummah, not a market wage — and growing only as revenue grows.",
  [("16.1","Purpose"),("16.2","Guiding Principles"),("16.3","Compensation Components"),
   ("16.4","Revenue Allocation for Compensation"),("16.5","Compensation Philosophy"),
   ("16.6","Incentive & Award Framework"),("16.7","Governance Oversight"),("16.8","Annual Review")]),
 (17, "Complete Document Inventory", "Subsection 17.1",
  "One hundred and eight documents, each with a category, a priority, a status, and a named steward.",
  [("17.1","All 108 Documents at a Glance")]),
 (18, "Document Registry by Category", "Subsections 18.1–18.7",
  "The same 108 documents, regrouped into the seven handbook categories the Senate has approved.",
  [("18.1","Governance Handbook (11)"),("18.2","Academic Handbook (19)"),("18.3","Student Handbook (23)"),
   ("18.4","Operations Handbook (28)"),("18.5","Legal & Compliance Handbook (11)"),
   ("18.6","Marketing & Communications Handbook (7)"),("18.7","Waqf & Research Handbook (9)")]),
 (19, "Priority Ranking & Development Urgency", "Subsections 19.1–19.3",
  "Fifty Critical, fifty-three Important, five already Complete — recomputed directly from the registry.",
  [("19.1","Priority Definitions"),("19.2","Summary by Priority"),("19.3","Pre-Launch Essentials (9)")]),
 (20, "Responsibility Assignment Matrix", "Subsections 20.1–20.7",
  "For every document: who stewards it, who implements it, and who has final authority to approve it.",
  [("20.1","Governance Documents"),("20.2","Academic Documents"),("20.3","Student Documents"),
   ("20.4","Operations Documents"),("20.5","Legal & Compliance Documents"),
   ("20.6","Marketing & Communications Documents"),("20.7","Waqf & Research Documents")]),
 (21, "Cross-Reference Matrix", "Subsections 21.1–21.2",
  "Which documents depend on which — so no policy is drafted before its own foundation exists.",
  [("21.1","Document Dependencies"),("21.2","Dependency Levels")]),
 (22, "Implementation Roadmap", "Subsections 22.1–22.5",
  "Nine documents before launch, 103 more across three phases that follow — every document scheduled exactly once.",
  [("22.1","Phased Development Schedule"),("22.2","Phase 1: Pre-Launch Essentials (9)"),
   ("22.3","Phase 2: Year 1 Critical Documents (41)"),("22.4","Phase 3: Year 2 Important Documents (46)"),
   ("22.5","Phase 4: Year 3+ Documents (7)")]),
 (23, "Senate Resolution & Endorsement", "Subsections 23.1–23.4",
  "Resolution 2028-001: the University Senate's formal endorsement of this Compendium as governing framework.",
  [("23.1","Senate Resolution"),("23.2","Approval Signatures"),("23.3","Document Control"),
   ("23.4","Amendment Record")]),
 (24, "Glossary of Terms", "No subsections",
  "Eleven terms, defined once, used consistently across every AMIU governing publication.",
  []),
 (25, "List of Acronyms", "No subsections",
  "Fifteen acronyms, spelled out once, so no reader is ever left guessing.",
  []),
]

# ---------------------------------------------------------------------------
# Prose content per section (hand-authored, closely following the source
# document, with the two Section 4 fixes applied and Sections 17-22's
# tables generated from igc_data.py instead of transcribed by hand).
# ---------------------------------------------------------------------------
CONTENT = {}

CONTENT[1] = f'''
{kicker(1,"1.1")}
## 1.1 Preamble

```{{=openxml}}
<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="300"/></w:pPr>
  <w:r><w:rPr><w:rFonts w:ascii="Fraunces" w:hAnsi="Fraunces"/><w:i/><w:color w:val="122A4E"/><w:sz w:val="26"/></w:rPr><w:t>In the Name of Allah, the Most Gracious, the Most Merciful.</w:t></w:r></w:p>
```

Al-Mulk International University (AMIU) is established as a Texas-registered, religiously-exempt institution of higher Islamic learning. Its founding purpose is the dissemination of authentic Islamic knowledge across the globe at the minimum possible cost, ensuring that no sincere seeker of knowledge is turned away due to financial constraint.

The University operates primarily as an online and distance learning institution, serving students across all time zones and continents. This mode of delivery is integral to the University's mission of spreading Islamic education worldwide without barriers.

This Institutional Governance Compendium constitutes the definitive governance and policy framework for the University. It establishes the institutional structure, articulates the core values, defines the roles and responsibilities of all governing bodies, and provides a comprehensive inventory of all policies, procedures, and governance instruments required for the operation of the University.

{kicker(1,"1.2")}
## 1.2 Purpose of This Compendium

This Compendium serves as the authoritative reference for all institutional governance and policy matters. It:

**1.2.1** Articulates the University's mission, vision, and core values;

**1.2.2** Establishes the institutional governance structure;

**1.2.3** Defines the roles and responsibilities of all governing bodies;

**1.2.4** Lists all 108 institutional policies, procedures, and governance instruments;

**1.2.5** Assigns clear accountability for each document;

**1.2.6** Provides a phased growth framework for offices and committees;

**1.2.7** Sets forth the compensation philosophy and framework;

**1.2.8** Establishes governance provisions for online and distance learning.

{kicker(1,"1.3")}
## 1.3 Scope of This Compendium

**1.3.1** This Compendium applies to all institutional documents, policies, procedures, and governance instruments of Al-Mulk International University.

**1.3.2** This Compendium covers documents across all seven handbook categories as approved by the University Senate.

**1.3.3** This Compendium is effective as of 1 January 2028 and shall be reviewed annually by the University Senate.

**1.3.4** This Compendium is the authoritative source for institutional governance, policy status, and responsibility assignment.

{kicker(1,"1.4")}
## 1.4 Governance Principles

This Compendium is founded upon the following governance principles:

| Principle | Application |
|---|---|
| Phased Growth | Institutional structure expands strategically as enrollment and faculty grow. |
| Separation of Powers | No single individual serves as both Policy Steward and sole Approval Authority. |
| Accountability | Every document has a clearly designated steward. |
| Transparency | All documents are publicly available, except where legally restricted. |
| Mission-Driven Service | All contributions are framed as service to the Ummah. |
| Revenue-Linked Sustainability | Compensation and operations scale with institutional revenue. |
| Online-First Delivery | All governance and operations assume a primarily online delivery model. |
| Global Accessibility | All policies accommodate students across time zones and regions. |
| Knowledge Without Barriers | The University is committed to removing all barriers to Islamic education. |

{kicker(1,"1.5")}
## 1.5 Document Numbering System

Each document is assigned a unique identifier following this convention:

| Element | Format | Example |
|---|---|---|
| Prefix | AMIU | AMIU |
| Category Code | GOV, ACA, STU, OPS, LEG, MKT, WAQ | AMIU-GOV |
| Sequential Number | 001-999, counted within its own category | AMIU-GOV-001 |
| Version | V-1.0 | AMIU-GOV-001-V1.0 |

**Category Codes**

| Code | Category | Description |
|---|---|---|
| GOV | Governance | Board, Senate, and institutional governance documents |
| ACA | Academic | Program, curriculum, faculty, and academic policy documents |
| STU | Student | Student conduct, services, and support documents |
| OPS | Operations | Finance, HR, IT, facilities, and operational documents |
| LEG | Legal & Compliance | Legal, regulatory, and compliance documents |
| MKT | Marketing | Brand, communications, and marketing documents |
| WAQ | Waqf & Research | Endowment, fundraising, research, and risk documents |

*Note: the Sequential Number in a document's code (e.g. the "003" in AMIU-GOV-003) counts only within that document's own category — it is not the same as the flat 1-108 numbering used for reference in Sections 17 and 20. Section 17's "Doc Code" column gives both side by side for every document, so the two schemes are never in doubt.*
'''

CONTENT[2] = f'''
{kicker(2,"2.1")}
## 2.1 Legal Identity

| Attribute | Detail |
|---|---|
| Legal Name | Al-Mulk International University |
| Acronym | AMIU |
| Tagline | Knowledge Without Barriers |
| Legal Status | Texas Nonprofit Religious Educational Corporation |
| Legal Domicile | State of Texas, United States of America |
| Date of Incorporation | 6 December 2027 |
| Academic Operations Commence | 1 January 2028 |
| Primary Mode of Delivery | Online and Distance Learning |

{kicker(2,"2.2")}
## 2.2 Mission

*"To spread Islamic education all over the world at the minimum possible cost, covering the needy without condition, through a rigorous, stackable, seven-tier credential ladder that never sacrifices academic seriousness for accessibility, and never sacrifices financial self-sufficiency for good intentions."*

{kicker(2,"2.3")}
## 2.3 Vision (2037)

*"For Al-Mulk International University to be internationally recognized as a leading English-medium Islamic university — financially independent, fully accredited in every jurisdiction in which it operates, and proof that a religious university can serve the poorest students in the world at near-zero cost while remaining permanently self-sustaining."*

{kicker(2,"2.4")}
## 2.4 Tagline

*"Knowledge Without Barriers"*

{kicker(2,"2.5")}
## 2.5 The AMIU Commitment

*"AMIU is not a commercial institution. Its aim is not money. It is a vehicle for spreading Islamic education worldwide without barriers. Those who serve AMIU do so as a contribution to the Ummah — a form of Jihad through knowledge. Compensation is provided as a means of sustaining service, not as a market-driven wage. The University grows with its mission, and its people grow with it."*

{kicker(2,"2.6")}
## 2.6 The Academic Ladder

AMIU offers a fully stacked seven-tier academic ladder, with every credential stacking directly into the next:

![The Seven-Tier Stackable Academic Ladder](assets/figures/igc_fig4_ladder.png)

**Exhibit G4. The Academic Ladder**

*Every credential stacks directly into the next tier with no credit lost in the climb — from the Undergraduate Diploma at the entry point to the Post-Doctoral Fellowship at its summit. This is the same ladder governed in full by Article X of the Constitution (AMIU-CON-001).*

{kicker(2,"2.7")}
## 2.7 The Six Colleges

| Number | College |
|---:|---|
| 1 | College of Qur'anic & Hadith Sciences |
| 2 | College of Shari'ah & Islamic Law |
| 3 | College of Islamic Theology & Philosophy (Aqeedah) |
| 4 | College of Arabic Language & Linguistics |
| 5 | College of Da'wah, Islamic Communication & Chaplaincy |
| 6 | College of Islamic Finance, Economics & Waqf Administration |
'''

CONTENT[3] = f'''
{kicker(3,"3.1")}
## 3.1 Introduction

The University is guided by the ISLAMIC framework — a foundation upon which all institutional decisions, policies, and practices are built.

{kicker(3,"3.2")}
## 3.2 The ISLAMIC Framework

![The ISLAMIC Values Framework](assets/figures/igc_fig5_islamic.png)

**Exhibit G5. The ISLAMIC Framework**

*Illumination, Sanad, Love, Access, Morality, Inquiry, Calling — the same seven values Article III of the Constitution (AMIU-CON-001) makes binding on every person acting in the University's name. Section 3.3 below sets out each in full.*

{kicker(3,"3.3")}
## 3.3 The ISLAMIC Framework — Detailed

**I — Illumination.** The pursuit of knowledge is an act of worship that illuminates the heart and draws the seeker closer to Allah. At AMIU, education is not merely the acquisition of information; it is the cultivation of faith, the refinement of the soul, and the awakening of the intellect to the signs of Allah. All academic pursuits are grounded in the Qur'an and Sunnah, and all scholarship is directed toward the service of Allah and the betterment of humanity.

**S — Sanad.** AMIU is bound to the Prophetic tradition by an unbroken golden chain of transmission (sanad). Every faculty appointment is traceable to a documented chain of study, training, and authorization. This sacred chain ensures that the knowledge imparted is authentic, trustworthy, and rooted in the tradition.

**L — Love.** The University exists to serve the Ummah with love and dedication. Its primary purpose is the dissemination of Islamic knowledge to every corner of the world, with particular attention to those who are marginalized, impoverished, or otherwise deprived of access to authentic Islamic education.

**A — Access.** Guided by the Qur'anic principles of compassion (rahmah) and justice (ʿadl), AMIU ensures that financial capacity shall never be a barrier to knowledge. The University opens its doors to all, regardless of economic status, nationality, or circumstance.

**M — Morality.** AMIU cultivates not only knowledgeable scholars but also virtuous human beings. The University is committed to the purification of character (tazkiyah) and the inculcation of noble virtues (akhlāq) — honesty, humility, patience, generosity, and compassion.

**I — Inquiry.** AMIU encourages intellectual rigor, critical inquiry, and the pursuit of truth. The University cultivates scholars who are both deeply rooted in the Islamic tradition and equipped to engage with contemporary challenges through ijtihād (independent reasoning) and taḥqīq (critical investigation).

**C — Calling.** AMIU is committed to the noble mission of da'wah — calling to Allah with wisdom, beauty, and mercy. Through its graduates, publications, and outreach programs, the University spreads the message of Islam with compassion, excellence, and profound respect for all humanity.

{kicker(3,"3.4")}
## 3.4 The ISLAMIC Pledge

*"As members of Al-Mulk International University, we commit ourselves to:*

*Illumination — that our knowledge may be light;*
*Sanad — that our scholarship may be authentic;*
*Love — that our service may be devoted;*
*Access — that no soul may be denied;*
*Morality — that our character may reflect the Prophet, peace be upon him;*
*Inquiry — that our thought may be rigorous;*
*Calling — that our da'wah may be with wisdom.*

*These are our values. This is our promise to the Ummah."*
'''

CONTENT[4] = f'''
{kicker(4,"4.1")}
## 4.1 The Governance Hierarchy

The University operates under a clear governance hierarchy, reflecting the standard bicameral model of higher education. The Board and Senate are supreme in their own domains rather than ranked one above the other — Exhibit G1 and Section 4.2 govern how the two chambers relate in full.

| Tier | Body | Role |
|---|---|---|
| 1 | Board of Trustees | Supreme Governing Authority — responsible for the long-term strategy, financial health, and legal integrity of the University. |
| 2 | President & Vice-Chancellor | Chief Executive Officer — the single operational link between the Board and the Senate. |
| 3 | University Senate | Supreme Academic Authority — responsible for curriculum, standards, examinations, and degrees. |
| 3 | Administration | Executive Management — the administrative arm that implements policies under the leadership of the President. |

*Note: the Senate and the Administration are placed at the same Tier 3 deliberately. Both report through the President as Tier 2, but neither is subordinate to the other — Section 4.2's non-interference principle and Exhibit G1's diagram both establish them as parallel, co-equal bodies, not a fourth link in a single chain.*

{kicker(4,"4.2")}
## 4.2 The Board-Senate Relationship

The Board and Senate maintain a relationship of mutual respect and separation of powers:

| Principle | Application |
|---|---|
| Strategic vs. Academic | The Board governs; the Senate teaches. |
| Non-Interference | The Board shall not interfere in curriculum or grading. The Senate shall not interfere in budget allocation or external strategy. |
| Advisory Role | The Senate advises the Board on academic matters. The Board consults the Senate on financial matters affecting academic quality. |
| The President as Link | The President ensures the Board's vision and the Senate's standards are executed efficiently. |

{kicker(4,"4.3")}
## 4.3 Senate Authority — Defined

| Area | Authority |
|---|---|
| Academic Programs | Full authority to approve, modify, or discontinue academic programs. |
| Academic Standards | Full authority to set and enforce academic standards. |
| Faculty Appointments | Full authority to approve faculty appointments through the Faculty Affairs Committee. |
| Faculty Promotions | Full authority to approve faculty promotions through the Faculty Affairs Committee. |
| Degree Conferrals | Full authority to ratify all degrees and certificates. |
| Academic Budget | Advisory authority — recommends allocation to the Board through the President. |
| Tuition Setting | No authority — this is the Board's exclusive responsibility. |
| Staff Hiring | No authority — this is the Administration's responsibility. |
| Non-Academic Budget | No authority — this is the Board's and Administration's responsibility. |

{kicker(4,"4.4")}
## 4.4 Governance Structure — Exhibit G1

The University's governance structure is presented in full in **Exhibit G1** (Governance Architecture, preceding the Table of Contents): the Board of Trustees at the apex, the President & Vice-Chancellor as the single operational link beneath it, and the University Senate and Administration as parallel, co-equal bodies beneath the President — each supreme within its own domain, neither subordinate to the other.
'''

CONTENT[5] = f'''
{kicker(5,"5.1")}
## 5.1 Role & Authority

The Board of Trustees is the supreme governing authority of Al-Mulk International University. It holds fiduciary responsibility for the institution's long-term health, strategic direction, and legal compliance.

{kicker(5,"5.2")}
## 5.2 Composition

| Category | Number | Description |
|---|---|---|
| Trustees | 5-9 | External members with expertise in finance, law, education, business, and community leadership |
| Ex-Officio Members | 2 | President & Vice-Chancellor; Secretary to the Board |
| **Total** | **7-11** | |

{kicker(5,"5.3")}
## 5.3 Chairperson of the Board

| Attribute | Detail |
|---|---|
| Role | The Chairperson is the principal officer of the Board and the highest-ranking governance official of the University. |
| Appointment | Elected by the Board of Trustees from among its members. |
| Term | Three years, renewable once. |
| Responsibilities | Presides over Board meetings; sets Board agenda; represents the Board externally; ensures Board effectiveness; leads Board evaluation. |
| Succession | Vice-Chairperson assumes role in case of vacancy until election. |

{kicker(5,"5.4")}
## 5.4 Trustee Requirements

| Requirement | Detail |
|---|---|
| Qualification | Demonstrated expertise in at least one of: finance, law, education, business, nonprofit governance, or community leadership. |
| Faith Commitment | Must be a practicing Muslim with commitment to the University's Islamic mission. This is permitted under Texas religious exemption and ensures spiritual alignment with the University's purpose. |
| Term | Three years, renewable once, for a maximum of six years. |
| Age | Minimum 30 years. |
| Residency | No residency requirement; meetings may be held virtually. |
| Conflict of Interest | Must disclose all potential conflicts annually. |
| Attendance | Must attend at least 75% of Board meetings annually. |

{kicker(5,"5.5")}
## 5.5 Board of Trustees Key Responsibilities

| Responsibility | Detail |
|---|---|
| Appointment | Appoints and evaluates the President & Vice-Chancellor |
| Budget | Approves the annual budget and major financial decisions |
| Strategy | Sets institutional strategy and long-term vision |
| Sustainability | Ensures financial sustainability and legal compliance |
| Policy Approval | Approves major policies and governance documents |
| Oversight | Oversees the University Senate through the President |
| Audit | Ensures proper financial audit and internal controls |

{kicker(5,"5.6")}
## 5.6 Board of Trustees — Summary

| Attribute | Detail |
|---|---|
| Chairperson | Elected from among Trustees; 3-year term; renewable once |
| Members | 5-9 Trustees plus 2 Ex-Officio |
| Term | 3 years; renewable once, maximum 6 years |
| Meeting Frequency | Quarterly, minimum |
| Meeting Format | In-person or virtual |
'''

CONTENT[6] = f'''
{kicker(6,"6.1")}
## 6.1 Role & Authority

The President & Vice-Chancellor is the chief executive officer of the University, responsible for the overall leadership, administration, and execution of the Board's strategic vision.

{kicker(6,"6.2")}
## 6.2 President Requirements

| Requirement | Detail |
|---|---|
| Qualification | Doctoral degree (Ph.D. or equivalent) from a recognized university. |
| Experience | Minimum 10 years of senior leadership experience in higher education or a related field. |
| Faith Commitment | Practicing Muslim with demonstrated commitment to Islamic education. |
| Term | Five years, renewable once, for a maximum of ten years. |
| Age | Minimum 40 years. |
| Residency | Must reside in the United States or be willing to relocate. |
| Accountability | Reports to the Board of Trustees. |

{kicker(6,"6.3")}
## 6.3 President Key Responsibilities

| Responsibility | Detail |
|---|---|
| Implementation | Implements Board decisions and policies |
| Leadership | Leads the University's administration |
| Senate | Chairs the University Senate |
| Representation | Represents the University externally |
| Effectiveness | Ensures institutional effectiveness and efficiency |
'''

CONTENT[7] = f'''
{kicker(7,"7.1")}
## 7.1 Role & Authority

The University Senate is the supreme academic authority of the University, responsible for all matters relating to curriculum, instruction, examinations, and the ratification of all degree programs.

{kicker(7,"7.2")}
## 7.2 Senate Composition (18 Voting Seats)

**Group I — Executive Leadership (3 Seats)**

| Seat | Role | Appointment |
|---:|---|---|
| 1 | President & Vice-Chancellor (Chairperson) | Ex-Officio |
| 2 | Deputy Vice-Chancellor, Academic Affairs (Vice-Chairperson) | Appointed by President |
| 3 | Deputy Vice-Chancellor, Administration & Finance (Secretary) | Appointed by President |

**Group II — Academic Operations (5 Seats)**

| Seat | Role | Appointment |
|---:|---|---|
| 4 | Dean, Qur'anic & Hadith Sciences / Shari'ah & Islamic Law | Appointed by President |
| 5 | Dean, Islamic Theology & Philosophy / Da'wah, Communication & Chaplaincy | Appointed by President |
| 6 | Dean, Arabic Language & Linguistics | Appointed by President |
| 7 | Dean, Islamic Finance, Economics & Waqf Administration | Appointed by President |
| 8 | University Librarian | Appointed by President |

**Group III — Frontline Instructional Management (6 Seats)**

| Seat | Role | Appointment |
|---:|---|---|
| 9 | Head of Department, Qur'anic Studies & Tafsir | Appointed by DVC Academic |
| 10 | Head of Department, Hadith Sciences | Appointed by DVC Academic |
| 11 | Head of Department, Shari'ah & Fiqh | Appointed by DVC Academic |
| 12 | Head of Department, Aqeedah & Islamic Philosophy | Appointed by DVC Academic |
| 13 | Head of Department, Arabic Language & Linguistics | Appointed by DVC Academic |
| 14 | Head of Department, Da'wah & Islamic Communication | Appointed by DVC Academic |

**Group IV — Institutional & Digital Strategy (4 Seats)**

| Seat | Role | Appointment |
|---:|---|---|
| 15 | Director of Academic Planning & LMS Infrastructure | Appointed by President |
| 16 | Elected Faculty Representative | Elected by Faculty |
| 17 | Elected Faculty Representative | Elected by Faculty |
| 18 | Elected Faculty Representative | Elected by Faculty |

{kicker(7,"7.3")}
## 7.3 Senate Member Requirements

| Requirement | Detail |
|---|---|
| Qualification | Must hold a doctoral degree (Ph.D. or equivalent) or have equivalent scholarly achievement. |
| Faith Commitment | Practicing Muslim with commitment to Islamic scholarship. |
| Term | Three years for appointed members; two years for elected faculty representatives. |
| Renewal | Appointed members may be reappointed; elected members may seek re-election. |
| Attendance | Must attend at least 75% of Senate meetings annually. |
| Disqualification | Members who fail to meet attendance requirements may be removed by Senate resolution. |

{kicker(7,"7.4")}
## 7.4 Senate Officers

| Officer | Role | Appointment |
|---|---|---|
| Chairperson | President & Vice-Chancellor | Ex-Officio |
| Vice-Chairperson | Deputy Vice-Chancellor, Academic Affairs | Appointed by President |
| Secretary | Deputy Vice-Chancellor, Administration & Finance | Appointed by President |

{kicker(7,"7.5")}
## 7.5 Senate Key Responsibilities

| Responsibility | Detail |
|---|---|
| Academic Programs | Approves all academic programs and courses |
| Academic Standards | Sets academic standards and policies |
| Degree Ratification | Ratifies all degrees and certificates |
| Faculty Quality | Oversees faculty quality and development |
| Advice | Advises the President on academic matters |

{kicker(7,"7.6")}
## 7.6 Senate Ex-Officio Members (Non-Voting)

| Member | Role |
|---|---|
| Undergraduate Student Representative | Appointed by Student Council |
| Postgraduate Student Representative | Appointed by Graduate Student Association |
| Staff Representative | Appointed by Staff Council |

{kicker(7,"7.7")}
## 7.7 Senate Meetings

**7.7.1** The Senate shall meet at least once per month during the academic semester.

**7.7.2** Special meetings may be called by the Chairperson or by written request of any five voting members.

**7.7.3** Notice of meetings shall be sent at least seven days in advance.

**7.7.4** Meetings may be conducted virtually or in person.

**7.7.5** Minutes of all meetings shall be maintained by the Secretary to the Senate.

{kicker(7,"7.8")}
## 7.8 Quorum

**7.8.1** A quorum shall consist of a simple majority of ten of the eighteen voting members.

**7.8.2** Ex-officio and observer members do not count toward the quorum requirement.

{kicker(7,"7.9")}
## 7.9 Voting Procedures

**7.9.1** All decisions shall be made by a simple majority of voting members present, provided a quorum exists.

**7.9.2** Voting may be conducted by voice vote, show of hands, roll call vote, or secret ballot.

**7.9.3** Voting may also be conducted electronically in virtual meetings.

**7.9.4** The Chairperson shall vote only in the case of a tie.

**7.9.5** Proxy voting is not permitted.
'''

CONTENT[8] = f'''
{kicker(8,"8.1")}
## 8.1 Purpose

The University operates on the principle that informed decisions require input from all stakeholders. This section establishes the advisory and proposing framework through which expertise is channeled to decision-making bodies.

{kicker(8,"8.2")}
## 8.2 Advisory and Proposing Framework

| Body | Can Advise? | Can Propose? | To Whom? |
|---|---|---|---|
| Board of Trustees | Yes | Yes | To itself, for internal deliberation |
| President & Vice-Chancellor | Yes | Yes | To the Board |
| University Senate | Yes | Yes | To the Board, through the President |
| Deputy Vice-Chancellors | Yes | Yes | To the President |
| College Deans | Yes | Yes | To the DVC, Academic Affairs |
| Faculty | Yes | Yes | To the Senate or Deans |
| Students | Yes | Yes | To the Senate or Student Affairs |
| Staff | Yes | Yes | To the Administration |

{kicker(8,"8.3")}
## 8.3 The Governance Principle

*"The Senate advises the Board on all matters affecting academic quality and proposes academic initiatives through the President. The Board, in turn, consults the Senate on financial decisions that affect academic delivery. This ensures that academic expertise informs strategic decisions, and strategic decisions support academic excellence."*
'''

CONTENT[9] = f'''
{kicker(9,"9.1")}
## 9.1 Deputy Vice-Chancellor, Academic Affairs

| Attribute | Detail |
|---|---|
| Role | Chief Academic Officer |
| Qualification | Doctoral degree (Ph.D. or equivalent) |
| Experience | Minimum 7 years of academic leadership experience |
| Term | Five years, renewable |
| Key Responsibilities | Academic strategy, curriculum, faculty affairs, quality assurance |
| Reports To | President & Vice-Chancellor |

{kicker(9,"9.2")}
## 9.2 Deputy Vice-Chancellor, Administration & Finance

| Attribute | Detail |
|---|---|
| Role | Chief Operating Officer |
| Qualification | Master's degree, minimum; professional certification preferred |
| Experience | Minimum 7 years of administrative and financial leadership experience |
| Term | Five years, renewable |
| Key Responsibilities | Finance, HR, operations, facilities, risk management |
| Reports To | President & Vice-Chancellor |

{kicker(9,"9.3")}
## 9.3 College Deans

**Dean Requirements**

| Requirement | Detail |
|---|---|
| Qualification | Doctoral degree (Ph.D. or equivalent) in a relevant field |
| Experience | Minimum 5 years of academic or administrative experience |
| Faith Commitment | Practicing Muslim with demonstrated commitment to Islamic scholarship |
| Term | Four years, renewable |
| Key Responsibilities | College leadership, faculty management, program quality |
| Reports To | Deputy Vice-Chancellor, Academic Affairs |

**College Deans (6 Colleges)**

| Number | College | Dean |
|---:|---|---|
| 1 | College of Qur'anic & Hadith Sciences | To be appointed |
| 2 | College of Shari'ah & Islamic Law | To be appointed |
| 3 | College of Islamic Theology & Philosophy | To be appointed |
| 4 | College of Arabic Language & Linguistics | To be appointed |
| 5 | College of Da'wah, Islamic Communication & Chaplaincy | To be appointed |
| 6 | College of Islamic Finance, Economics & Waqf Administration | To be appointed |

{kicker(9,"9.4")}
## 9.4 University Registrar

| Attribute | Detail |
|---|---|
| Role | Chief Academic Records Officer |
| Qualification | Master's degree, minimum |
| Experience | Minimum 5 years of academic records or registry experience |
| Term | Four years, renewable |
| Key Responsibilities | Student records, enrollment, examinations, graduation |
| Reports To | Deputy Vice-Chancellor, Academic Affairs |

{kicker(9,"9.5")}
## 9.5 Dean of Students

| Attribute | Detail |
|---|---|
| Role | Chief Student Affairs Officer |
| Qualification | Master's degree, minimum |
| Experience | Minimum 5 years of student affairs or counseling experience |
| Term | Four years, renewable |
| Key Responsibilities | Student conduct, welfare, support services |
| Reports To | Deputy Vice-Chancellor, Academic Affairs |

{kicker(9,"9.6")}
## 9.6 Directors (Functional Areas)

| Number | Position | Reports To |
|---:|---|---|
| 1 | Director of Human Resources | DVC, Administration & Finance |
| 2 | Director of Information Technology | DVC, Administration & Finance |
| 3 | Director of Facilities | DVC, Administration & Finance |
| 4 | Director of Admissions | DVC, Academic Affairs |
| 5 | Director of Communications | DVC, Academic Affairs |
| 6 | Director of Waqf & Philanthropy | DVC, Administration & Finance |
| 7 | Director of Institutional Research | DVC, Academic Affairs |
| 8 | Director of Career Services | Dean of Students |
| 9 | Director of International Operations | DVC, Administration & Finance |
| 10 | Director of Internal Audit & Risk | Board of Trustees, functionally |

{kicker(9,"9.7")}
## 9.7 Summary Table — All Key Roles

| Number | Role | Qualification | Term | Reports To |
|---:|---|---|---|---|
| 1 | Chairperson, Board of Trustees | Trustee; elected by Board | 3 years | Board |
| 2 | Trustee | Expertise in finance, law, education, or leadership | 3 years | Board |
| 3 | President & Vice-Chancellor | Ph.D.; 10+ years leadership | 5 years | Board |
| 4 | DVC, Academic Affairs | Ph.D.; 7+ years academic leadership | 5 years | President |
| 5 | DVC, Administration & Finance | Master's; 7+ years admin leadership | 5 years | President |
| 6 | College Dean | Ph.D.; 5+ years academic experience | 4 years | DVC Academic |
| 7 | University Registrar | Master's; 5+ years registry experience | 4 years | DVC Academic |
| 8 | Dean of Students | Master's; 5+ years student affairs experience | 4 years | DVC Academic |
| 9 | Director | Master's or Bachelor's; 5+ years experience | 4 years | Respective DVC |
'''

CONTENT[10] = f'''
{kicker(10,"10.1")}
## 10.1 Purpose

This section establishes the governance framework for the University's primary mode of delivery: online and distance learning.

{kicker(10,"10.2")}
## 10.2 Technology Governance

**10.2.1** The University shall maintain a robust Learning Management System (LMS) as the primary platform for all academic activities.

**10.2.2** The Director of Information Technology shall oversee the LMS and ensure its reliability, security, and accessibility.

**10.2.3** The University shall maintain data privacy and security standards in accordance with applicable laws.

**10.2.4** The University shall provide technology support to students and faculty.

{kicker(10,"10.3")}
## 10.3 Virtual Governance Provisions

**10.3.1** All meetings of the Board of Trustees, University Senate, and committees may be conducted virtually.

**10.3.2** Virtual meetings shall be conducted using secure video conferencing technology.

**10.3.3** Notice of virtual meetings shall be sent at least seven days in advance, with the meeting link included.

**10.3.4** Voting in virtual meetings shall be conducted using secure electronic voting systems.

**10.3.5** Minutes of virtual meetings shall be recorded and maintained in the same manner as in-person meetings.

**10.3.6** All participants in virtual meetings must have their cameras on unless excused for exceptional circumstances.

{kicker(10,"10.4")}
## 10.4 Global Accessibility

**10.4.1** All policies and procedures shall accommodate students across all time zones.

**10.4.2** Course materials shall be accessible to students with low bandwidth.

**10.4.3** Recorded sessions shall be available within 24 hours of live sessions.

**10.4.4** Students shall have access to resources regardless of their location.
'''

CONTENT[11] = f'''
{kicker(11,"11.1")}
## 11.1 Overview

AMIU's institutional structure grows strategically over ten years in proportion to enrollment, faculty, and operational complexity.

**Growth Summary**

| Phase | Year | Enrollment | Offices | Committees | Total Units | Faculty (Est.) |
|---|---:|---:|---:|---:|---:|---|
| Launch | 1 | 347 | 10 | 5 | 15 | 15-20 |
| Growth | 3 | 1,606 | 16 | 9 | 25 | 40-50 |
| Mature | 5 | 3,493 | 22 | 14 | 36 | 70-90 |
| Full | 10 | 11,021 | 29 | 19 | 48 | 150-200 |

{kicker(11,"11.2")}
## 11.2 Office Growth Projection

| Category | Year 1 | Year 3 | Year 5 | Year 10 |
|---|---:|---:|---:|---:|
| Executive Offices | 4 | 5 | 5 | 6 |
| Academic Offices | 3 | 5 | 6 | 8 |
| Student Affairs Offices | 2 | 3 | 4 | 5 |
| Administrative & Operational Offices | 1 | 3 | 4 | 5 |
| Institutional Advancement Offices | 0 | 0 | 3 | 5 |
| **TOTAL OFFICES** | **10** | **16** | **22** | **29** |

{kicker(11,"11.3")}
## 11.3 Committee Growth Projection

| Category | Year 1 | Year 3 | Year 5 | Year 10 |
|---|---:|---:|---:|---:|
| Board-Level Committees | 2 | 3 | 3 | 4 |
| Senate-Level Committees | 3 | 5 | 9 | 11 |
| Administrative Committees | 0 | 1 | 2 | 4 |
| **TOTAL COMMITTEES** | **5** | **9** | **14** | **19** |

{kicker(11,"11.4")}
## 11.4 Growth Triggers

| Trigger | Condition | Action |
|---|---|---|
| Enrollment Growth | Enrollment exceeds 1,500 | Expand from Year 1 to Year 3 structure |
| Enrollment Growth | Enrollment exceeds 3,000 | Expand from Year 3 to Year 5 structure |
| Enrollment Growth | Enrollment exceeds 10,000 | Expand from Year 5 to Year 10 structure |
| Faculty Growth | Faculty exceeds 30 | Add appropriate committees |
| Program Growth | New colleges established | Add appropriate deans and committees |

The Senate shall review institutional structure annually and recommend adjustments. Any expansion requires approval by the University Senate.
'''

CONTENT[12] = f'''
{kicker(12,"12.1")}
## 12.1 Overview

| Metric | Year 1 Value |
|---|---|
| Academic Year | 2028 |
| Projected Enrollment | 347 students |
| Projected Faculty | 15-20 |
| Offices | 10 |
| Committees | 5 |
| Total Units | 15 |
| Rationale | Lean structure focused on essential operations only |

{kicker(12,"12.2")}
## 12.2 Year 1 Offices (10 Offices)

| Number | Office | Head Title | Primary Function |
|---:|---|---|---|
| 1 | Office of the President & Vice-Chancellor | President & Vice-Chancellor | Chief Executive Officer; overall institutional leadership |
| 2 | Office of Academic Affairs | Deputy Vice-Chancellor, Academic Affairs | Academic strategy, curriculum, faculty affairs |
| 3 | Office of Administration & Finance | Deputy Vice-Chancellor, Administration & Finance | Financial management, HR, operations |
| 4 | Office of the Registrar | University Registrar | Student records, enrollment, examinations, graduation |
| 5 | Office of Student Affairs | Dean of Students | Student conduct, welfare, support services |
| 6 | Office of Admissions | Director of Admissions | Student recruitment, application processing, enrollment |
| 7 | Office of Information Technology | Director, IT | LMS, systems, data security, technical support |
| 8 | Office of Waqf & Philanthropy | Director | Fundraising, donor relations, Waqf endowment management |
| 9 | Office of Communications | Director, Communications | Brand management, media relations, marketing |
| 10 | Office of Legal Counsel | General Counsel | Legal advisory, compliance, regulatory affairs |

*Total: 10 Offices*

{kicker(12,"12.3")}
## 12.3 Year 1 Committees (5 Committees)

| Number | Committee | Chair | Function | Members |
|---:|---|---|---|---|
| 1 | University Senate | President & Vice-Chancellor | Supreme academic authority; curriculum, instruction, degrees (18 seats) | 18 Seats |
| 2 | Academic Standards Committee | Dean | Curriculum quality, academic policies, student standards | 5 Faculty |
| 3 | Curriculum Committee | Dean | New course and program approval; curriculum review | 5 Faculty |
| 4 | Student Affairs Committee | Dean of Students | Student conduct, welfare, extracurricular activities | 3 Faculty + Staff |
| 5 | Audit & Risk Committee | Trustee (External) | Financial audits, internal controls, risk oversight | 3 Trustees |

*Total: 5 Committees*
'''

CONTENT[13] = f'''
{kicker(13,"13.1")}
## 13.1 Overview

| Metric | Year 3 Value |
|---|---|
| Academic Year | 2030 |
| Projected Enrollment | 1,606 students |
| Projected Faculty | 40-50 |
| Offices | 16 |
| Committees | 9 |
| Total Units | 25 |

{kicker(13,"13.2")}
## 13.2 Year 3 Offices (16 Offices)

*Retain all Year 1 Offices (10) and add the following 6:*

| Number | New Office | Head Title | Primary Function |
|---:|---|---|---|
| 11 | Office of Institutional Research & Accreditation | Director | Data management, institutional research, accreditation preparation |
| 12 | Office of Career Services | Director | Career counseling, job placement, alumni engagement |
| 13 | Office of International Student Services | Director | Visa support, orientation, international student support |
| 14 | Office of Human Resources | Director of Human Resources | Staff recruitment, compensation, benefits, policy administration |
| 15 | College of Qur'anic & Hadith Sciences | Dean | Academic programs in Qur'anic and Hadith disciplines |
| 16 | College of Shari'ah & Islamic Law | Dean | Academic programs in Islamic law and jurisprudence |

*Total: 16 Offices*

{kicker(13,"13.3")}
## 13.3 Year 3 Committees (9 Committees)

*Retain all Year 1 Committees (5) and add the following 4:*

| Number | New Committee | Chair | Function | Members |
|---:|---|---|---|---|
| 6 | Faculty Affairs Committee | Dean | Faculty evaluation, promotion, professional development | 5 Faculty |
| 7 | Admissions & Scholarships Committee | Director of Admissions | Admissions policies and scholarship awards | 3 Faculty + Staff |
| 8 | Waqf & Endowment Committee | Director, Waqf & Philanthropy | Waqf governance, donor stewardship, fund allocation | 5 Members |
| 9 | Finance & Investment Committee | Trustee | Budget oversight, investment policy, financial sustainability | 3 Trustees |

*Total: 9 Committees*
'''

CONTENT[14] = f'''
{kicker(14,"14.1")}
## 14.1 Overview

| Metric | Year 5 Value |
|---|---|
| Academic Year | 2032 |
| Projected Enrollment | 3,493 students |
| Projected Faculty | 70-90 |
| Offices | 22 |
| Committees | 14 |
| Total Units | 36 |

{kicker(14,"14.2")}
## 14.2 Year 5 Offices (22 Offices)

*Retain all Year 3 Offices (16) and add the following 6:*

| Number | New Office | Head Title | Primary Function |
|---:|---|---|---|
| 17 | College of Islamic Theology & Philosophy | Dean | Academic programs in Aqeedah and Islamic philosophy |
| 18 | College of Arabic Language & Linguistics | Dean | Academic programs in Arabic language and literature |
| 19 | College of Da'wah, Islamic Communication & Chaplaincy | Dean | Academic programs in Da'wah, communication, and chaplaincy |
| 20 | College of Islamic Finance, Economics & Waqf Administration | Dean | Academic programs in Islamic finance, economics, and Waqf |
| 21 | Office of Facilities & Operations | Director of Facilities | Campus maintenance, health, safety, emergency preparedness |
| 22 | Office of International Operations | Director | International partnerships and branch campus coordination |

*Total: 22 Offices*

{kicker(14,"14.3")}
## 14.3 Year 5 Committees (14 Committees)

*Retain all Year 3 Committees (9) and add the following 5:*

| Number | New Committee | Chair | Function | Members |
|---:|---|---|---|---|
| 10 | Research & Publication Committee | Dean of Graduate Studies | Research policy, ethics, and publication support | 5 Faculty |
| 11 | Library & Learning Resources Committee | University Librarian | Library services, digital resources, LMS oversight | 3 Faculty |
| 12 | Information Technology Committee | Chief Information Officer | IT strategy, LMS, data security oversight | 5 Members |
| 13 | Health, Safety & Emergency Response Committee | Director of Facilities | Campus safety, health standards, emergency planning | Multi-departmental |
| 14 | Internationalization Committee | Director, International Operations | International partnerships and branch campus strategy | 5 Members |

*Total: 14 Committees*
'''

CONTENT[15] = f'''
{kicker(15,"15.1")}
## 15.1 Overview

| Metric | Year 10 Value |
|---|---|
| Academic Year | 2037 |
| Projected Enrollment | 11,021 students |
| Projected Faculty | 150-200 |
| Offices | 29 |
| Committees | 19 |
| Total Units | 48 |

{kicker(15,"15.2")}
## 15.2 Year 10 Offices (29 Offices)

*Retain all Year 5 Offices (22) and add the following 7:*

| Number | New Office | Head Title | Primary Function |
|---:|---|---|---|
| 23 | AMIU Graduate School | Dean of Graduate Studies | Coordination of all postgraduate programs |
| 24 | Office of Institutional Planning | Director | Strategic planning, policy coordination, performance monitoring |
| 25 | Office of Internal Audit & Risk | Director / Chief Risk Officer | Risk management, internal audit, compliance monitoring |
| 26 | Office of Procurement & Contracts | Director | Purchasing, vendor management, contract administration |
| 27 | Office of Student Support Services | Director | Student counseling, mental health, disability services |
| 28 | Office of the University Secretary | Secretary to the Senate | Governance support; secretariat to the Senate and Board |
| 29 | Office of the Deputy Vice-Chancellor, Administration & Finance | Deputy Vice-Chancellor, Administration & Finance | Full financial and administrative leadership |

*Total: 29 Offices*

{kicker(15,"15.3")}
## 15.3 Year 10 Committees (19 Committees)

*Retain all Year 5 Committees (14) and add the following 5:*

| Number | New Committee | Chair | Function | Members |
|---:|---|---|---|---|
| 15 | Accreditation & Quality Assurance Committee | Director, Institutional Research | Accreditation readiness and institutional quality enhancement | 5 Members |
| 16 | Executive Committee | Chair, Board of Trustees | Acts on behalf of the Board between meetings | Board Officers |
| 17 | Governance & Nominating Committee | Trustee | Board governance, trustee nomination, policy review | 3 Trustees |
| 18 | Staff Welfare Committee | Director of Human Resources | Staff wellness, professional development, engagement | Staff Representatives |
| 19 | Budget & Planning Committee | Chief Financial Officer | Budget planning, resource allocation, financial reporting | Multi-departmental |

*Total: 19 Committees*
'''

CONTENT[16] = f'''
{kicker(16,"16.1")}
## 16.1 Purpose

This section establishes the guiding principles for compensation, incentives, and awards at Al-Mulk International University. It reflects the University's commitment to mission-driven service while ensuring fair and sustainable compensation for all contributors.

{kicker(16,"16.2")}
## 16.2 Guiding Principles

| Principle | Description |
|---|---|
| 1. Mission-Driven Service | The University's primary mission is the dissemination of Islamic knowledge. All compensation is framed as a contribution to this noble cause rather than market maximization. |
| 2. Revenue-Linked Growth | Compensation grows directly with institutional revenue, ensuring sustainability and alignment. |
| 3. Fairness & Transparency | Compensation is transparent and published annually. |
| 4. Sustainability | Compensation structures are designed to be sustainable over the long term. |
| 5. Recognition | Incentives and awards recognize exceptional contributions. |

{kicker(16,"16.3")}
## 16.3 Compensation Components

Compensation at AMIU consists of the following components:

| Component | Description |
|---|---|
| Base Honoraria | Monthly stipend for foundational contributions |
| Semester Incentives | Additional compensation for exceptional performance |
| Annual Awards | Recognition for outstanding service |
| Grants & Offers | Project-specific funding for academic initiatives |
| Service Opportunities | Compensation for specific service roles |
| Promotions | Advancement through academic ranks |

{kicker(16,"16.4")}
## 16.4 Revenue Allocation for Compensation

| Component | Percentage | Source |
|---|---|---|
| Payroll Allocation | 20% of Gross Revenue | Tuition Revenue |
| Faculty Honoraria | 40% of Payroll | Tuition Revenue |
| Founders' Compensation | 24% of Payroll | Tuition Revenue |
| Senate Stipends | 18% of Payroll | Tuition Revenue |
| Core Administration | 18% of Payroll | Tuition Revenue |

*Note: Compensation may be supplemented by revenue from the Independent Commercial Engine (AMIU Global Services LLC) at the discretion of the Board, subject to governance approval.*

{kicker(16,"16.5")}
## 16.5 Compensation Philosophy

**Mission-Driven Approach**

*"AMIU is not a commercial institution. Its aim is not money. It is a vehicle for spreading Islamic education worldwide without barriers. Those who serve AMIU do so as a contribution to the Ummah — a form of Jihad through knowledge."*

| Element | Application |
|---|---|
| Founding Faculty | Serves initially with nominal honoraria, motivated by the mission |
| Mission-Aligned Scholars | Prioritized in recruitment |
| Compensation as Service | Framed as acknowledgment of service, not market wage |
| Growth-Linked | Compensation increases with institutional revenue |

{kicker(16,"16.6")}
## 16.6 Incentive & Award Framework

| Type | Purpose | Frequency |
|---|---|---|
| Semester Incentives | Recognize exceptional teaching or service | Per Semester |
| Annual Awards | Distinguished contributions | Annually |
| Service Grants | Project-based funding for initiatives | As Needed |
| Promotion Awards | Recognition of advancement through ranks | As Needed |

{kicker(16,"16.7")}
## 16.7 Governance Oversight

| Body | Role |
|---|---|
| University Senate | Approves compensation philosophy and major adjustments |
| Board of Trustees | Approves overall compensation framework |
| Deputy Vice-Chancellor, Administration & Finance | Oversees implementation |

{kicker(16,"16.8")}
## 16.8 Annual Review

Compensation structures shall be reviewed annually by the Deputy Vice-Chancellor, Administration & Finance, with recommendations submitted to the University Senate for approval.
'''

CONTENT[17] = f'''
{kicker(17,"17.1")}
## 17.1 All 108 Documents at a Glance

*The "Doc Code" column gives each document's category-relative identifier under the Section 1.5 numbering convention (e.g. GOV-003), alongside the flat 1-108 reference number used throughout this Compendium in Sections 17, 20, and 22.*

{table_17_full_inventory()}
'''

_cat18_labels = {"GOV": "18.1 Governance Handbook", "ACA": "18.2 Academic Handbook",
                  "STU": "18.3 Student Handbook", "OPS": "18.4 Operations Handbook",
                  "LEG": "18.5 Legal & Compliance Handbook", "MKT": "18.6 Marketing & Communications Handbook",
                  "WAQ": "18.7 Waqf & Research Handbook"}
_c18_parts = []
for _i, _cat in enumerate(CATEGORY_ORDER, start=1):
    _label = _cat18_labels[_cat]
    _num, _title = _label.split(" ", 1)
    _c18_parts.append(f'{kicker(18, _num)}\n## {_label} ({CATEGORY_TOTALS[_cat]} Documents)\n\n{table_18_category(_cat)}\n')
CONTENT[18] = "\n".join(_c18_parts)

CONTENT[19] = f'''
{kicker(19,"19.1")}
## 19.1 Priority Definitions

| Priority | Definition | Timeline |
|---|---|---|
| Critical | Must be developed before launch or within Year 1 | Pre-Launch to Year 1 |
| Important | Should be developed within Years 2-3 | Year 2-3 |
| Complete | Already developed and approved | Done |

{kicker(19,"19.2")}
## 19.2 Summary by Priority

*Generated directly from the itemized registry in Section 17, so this summary and that registry can never diverge.*

{table_19_2_summary()}

{kicker(19,"19.3")}
## 19.3 Pre-Launch Essentials (9 Documents)

| Number | Document | Category | Policy Steward |
|---:|---|---|---|
| 3 | Bylaws | Governance | Secretary to the Board |
| 5 | Board of Trustees Charter | Governance | Chair, Board of Trustees |
| 10 | Conflict of Interest Policy | Governance | Office of Legal Counsel |
| 55 | Financial Operations Manual | Operations | DVC, Administration & Finance |
| 60 | HR Policies & Procedures Manual | Operations | DVC, Administration & Finance |
| 69 | Data Privacy & Security Policy | Operations | Director, Information Technology |
| 31 | Student Code of Conduct | Student | Dean of Students |
| 36 | Attendance Policy | Student | Dean of Students |
| 58 | Tuition Collection & Refund Policy | Operations | DVC, Administration & Finance |
'''

_c20_parts = []
for _num, _label in [("20.1","Governance Documents"),("20.2","Academic Documents"),("20.3","Student Documents"),
                      ("20.4","Operations Documents"),("20.5","Legal & Compliance Documents"),
                      ("20.6","Marketing & Communications Documents"),("20.7","Waqf & Research Documents")]:
    _cat = CATEGORY_ORDER[int(_num.split(".")[1]) - 1]
    _c20_parts.append(f'{kicker(20, _num)}\n## {_num} {_label}\n\n{table_20_category(_cat)}\n')
CONTENT[20] = "\n".join(_c20_parts)

CONTENT[21] = f'''
{kicker(21,"21.1")}
## 21.1 Document Dependencies

| Document | Depends On | Referenced By |
|---|---|---|
| Bylaws (GOV-003) | Certificate of Formation | All Documents |
| Board Charter (GOV-005) | Bylaws | Committee Charters |
| Senate Rules (GOV-007) | Bylaws | All Academic Policies |
| Conflict of Interest (GOV-010) | Bylaws | All Policies |
| Academic Catalog (ACA-001) | Academic Policies | Student Handbook |
| Student Code (STU-001) | Academic Integrity | All Student Policies |
| Financial Model (OPS-001) | Strategic Plan | All Financial Policies |
| Data Privacy (OPS-016) | FERPA, GDPR | All IT Policies |
| Waqf Charter (WAQ-001) | Bylaws | Donor Stewardship |
| Institutional Effectiveness Framework (OPS-028) | Program Assessment & Review Policy (ACA-003) | All Administrative Units |

{kicker(21,"21.2")}
## 21.2 Dependency Levels

*The Certificate of Formation's Doc Code is GOV-004, its category-relative position per Section 17.*

**Level 1: Foundation Documents**

- Certificate of Formation (GOV-004)
- Bylaws (GOV-003)
- Strategic Plan (GOV-001)
- Financial Model (OPS-001)

**Level 2: Governance Documents**

- Board Charter (GOV-005)
- Senate Rules (GOV-007)
- Committee Charters (GOV-009)
- Conflict of Interest (GOV-010)
- HR Policies (OPS-007)

**Level 3: Operational Documents**

- Financial Operations Manual (OPS-002)
- Tuition Collection Policy (OPS-005)
- Payroll Policy (OPS-006)
- IT Infrastructure Plan (OPS-014)
- Data Privacy Policy (OPS-016)
- Facilities Management (OPS-020)
- Institutional Effectiveness Framework (OPS-028)

**Level 4: Academic Documents**

- Academic Catalog (ACA-001)
- Curriculum Development (ACA-002)
- Faculty Evaluation (ACA-005)
- Student Code (STU-001)
- Attendance Policy (STU-006)
- Graduation Requirements (ACA-012)

**Level 5: Student Support Documents**

- Student Grievance (STU-002)
- Mental Health Support (STU-009)
- Disability Services (STU-011)
- International Student Support (STU-013)

**Level 6: International & Marketing**

- Gambia Operational Plan (LEG-006)
- Nigeria Development Plan (LEG-007)
- Brand Style Guide (MKT-001)
- Marketing Plan (MKT-007)
- Waqf Charter (WAQ-001)

**Level 7: Risk & Compliance**

- Risk Register (WAQ-007)
- Crisis Management (WAQ-008)
- FERPA Compliance (LEG-001)
- GDPR Compliance (LEG-002)
- Business Continuity (WAQ-009)
'''

CONTENT[22] = f'''
{kicker(22,"22.1")}
## 22.1 Phased Development Schedule

*Phase 2 and Phase 3's document counts are generated directly from the itemized lists in Sections 22.3–22.4, so this summary and those lists can never diverge.*

{table_22_1_roadmap()}

{kicker(22,"22.2")}
## 22.2 Phase 1: Pre-Launch Essentials (9 Documents)

| Number | Document | Policy Steward | Timeline |
|---:|---|---|---|
| 3 | Bylaws | Secretary to the Board | Week 1-2 |
| 5 | Board of Trustees Charter | Chair, Board of Trustees | Week 1-2 |
| 10 | Conflict of Interest Policy | Office of Legal Counsel | Week 2-3 |
| 55 | Financial Operations Manual | DVC, Administration & Finance | Week 2-4 |
| 60 | HR Policies & Procedures Manual | DVC, Administration & Finance | Week 2-4 |
| 69 | Data Privacy & Security Policy | Director, Information Technology | Week 3-4 |
| 31 | Student Code of Conduct | Dean of Students | Week 3-4 |
| 36 | Attendance Policy | Dean of Students | Week 4-5 |
| 58 | Tuition Collection & Refund Policy | DVC, Administration & Finance | Week 4-6 |

{kicker(22,"22.3")}
## 22.3 Phase 2: Year 1 Critical Documents ({len(PHASE2_NUMS)} Documents)

Document numbers: {ranges(PHASE2_NUMS)} (every Critical-priority document not already scheduled in Phase 1). Timeline: Months 2-5.

{kicker(22,"22.4")}
## 22.4 Phase 3: Year 2 Important Documents ({len(PHASE3_NUMS)} Documents)

Document numbers: {ranges(PHASE3_NUMS)} (every Important-priority document not deferred to Phase 4). Timeline: Months 6-10.

{kicker(22,"22.5")}
## 22.5 Phase 4: Year 3+ Documents ({len(PHASE4_NUMS)} Documents)

| Number | Document | Policy Steward | Timeline |
|---:|---|---|---|
| 73 | Facilities Management Policy | Director, Facilities | Month 17-18 |
| 74 | Health & Safety Policy | Director, Facilities | Month 18-19 |
| 75 | Emergency Response Plan | Director, Facilities | Month 18-19 |
| 70 | Backup & Disaster Recovery Plan | Director, IT | Month 19-20 |
| 71 | IT Support Policy | Director, IT | Month 20-21 |
| 72 | Acceptable Use Policy | Director, IT | Month 21-22 |
| 67 | IT Infrastructure Plan | Director, IT | Month 22-23 |
'''

CONTENT[23] = f'''
{kicker(23,"23.1")}
## 23.1 Senate Resolution

**Resolution No. 2028-001**

**Subject:** Approval of the AMIU Institutional Governance Compendium

**Date:** 1 January 2028

Moved By: ______________________ &nbsp;&nbsp;&nbsp; Seconded By: ______________________

*Whereas*, the Al-Mulk International University Senate has reviewed the AMIU Institutional Governance Compendium, a comprehensive governance and policy framework for the University;

*Whereas*, the Compendium establishes the institutional structure, articulates the core values, defines the roles and responsibilities of all governing bodies, and provides a comprehensive inventory of all policies, procedures, and governance instruments;

*Whereas*, the Compendium provides a phased implementation roadmap for the development of all documents;

*Now, Therefore, Be It Resolved*, that the University Senate:

**1.** Approves the AMIU Institutional Governance Compendium as the definitive governance and policy framework;

**2.** Endorses the phased implementation roadmap for document development;

**3.** Authorizes the Office of Institutional Planning to proceed with document development;

**4.** Requires that all Policy Stewards complete their assigned documents in accordance with the phased schedule;

**5.** Requires that the Compendium be reviewed annually by the Senate.

{kicker(23,"23.2")}
## 23.2 Approval Signatures

| Capacity | Name | Signature | Date |
|---|---|---|---|
| President & Vice-Chancellor | ______________________ | ______________________ | _________ |
| Deputy Vice-Chancellor, Academic Affairs | Muhammad Al-Qumash, Ph.D. | ______________________ | _________ |
| Deputy Vice-Chancellor, Administration & Finance | Abdullah Turki, Ph.D. | ______________________ | _________ |
| Secretary to the Senate | ______________________ | ______________________ | _________ |
| Chair, Academic Standards Committee | ______________________ | ______________________ | _________ |
| Dean of Students | ______________________ | ______________________ | _________ |
| University Registrar | ______________________ | ______________________ | _________ |

{kicker(23,"23.3")}
## 23.3 Document Control

| Field | Value |
|---|---|
| Document | AMIU Institutional Governance Compendium |
| Document Control No. | AMIU-IGC-004 |
| Version | 4.0 (Final Edition) |
| Effective Date | 1 January 2028 |
| Review Date | Annually |
| Classification | Restricted - Senate & Board Distribution |
| Prepared By | Office of Institutional Planning |
| Approved By | University Senate |

{kicker(23,"23.4")}
## 23.4 Amendment Record

| Version | Date | Amendment | Approved By |
|---|---|---|---|
| 1.0 | 1 January 2028 | Initial Release | University Senate |
| 2.0 | 1 January 2028 | Online-Ready Edition | University Senate |
| 3.0 | 1 January 2028 | Final Edition with Tagline | University Senate |
| 4.0 | 1 January 2028 | Final Edition with Full Framework | University Senate |
'''

CONTENT[24] = '''
| Term | Definition |
|---|---|
| Academic Year | The period from 1 August to 31 July of the following year. |
| Board of Trustees | The governing body responsible for the overall direction and oversight of the University. |
| DVC | Deputy Vice-Chancellor. |
| Grand Total | The sum of all mandatory fees payable by a student, as published in the Academic Catalog. |
| ISLAMIC Framework | The University's core values framework: Illumination, Sanad, Love, Access, Morality, Inquiry, Calling. |
| LMS | Learning Management System — the digital platform for course delivery and management. |
| Policy Steward | The senior executive responsible for ensuring a policy is current, accurate, and aligned with strategy. |
| Sanad | A documented chain of study and training tracing a scholar's academic lineage. |
| Senate | The University Senate — the supreme academic authority responsible for curriculum, instruction, and degrees. |
| Tuition Tier | Regional pricing classification based on World Bank income classifications. |
| Waqf | An Islamic charitable endowment established for educational or humanitarian purposes. |
'''

CONTENT[25] = '''
| Acronym | Full Term |
|---|---|
| ACA | Academic |
| AMIU | Al-Mulk International University |
| DVC | Deputy Vice-Chancellor |
| FERPA | Family Educational Rights and Privacy Act |
| GDPR | General Data Protection Regulation |
| GOV | Governance |
| HR | Human Resources |
| IGC | Institutional Governance Compendium |
| IT | Information Technology |
| LEG | Legal |
| LMS | Learning Management System |
| MKT | Marketing |
| OPS | Operations |
| STU | Student |
| WAQ | Waqf |
'''

def main():
    parts = []
    for num, title, subrange, thesis, subsecs in SECTIONS:
        parts.append(divider(num, title, subrange, thesis, subsecs))
        parts.append(CONTENT[num])
        parts.append(PAGEBREAK)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Wrote {OUT} ({sum(len(p) for p in parts)} chars)")

if __name__ == "__main__":
    main()
