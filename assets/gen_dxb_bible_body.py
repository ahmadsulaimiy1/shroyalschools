#!/usr/bin/env python3
"""Author work_dxb_bible_body.md — the ten-standard body of the AMIU Digital
Experience & Editorial Bible (Doc Codes DXB-001 through DXB-010), the tenth
AMIU flagship publication, in the same navy/gold editorial system as the
Blueprint, Constitution, Institutional Governance Compendium, Academic
Handbook, Student Policies Handbook, Operations Handbook, Legal &
Compliance Handbook, Marketing & Communications Handbook, and Waqf &
Research Handbook.

Origin and scope. This publication answers a directive asking for "the
definitive Editorial Bible and Digital Experience Constitution" governing
the University's public website, LMS, and six operating portals — not a
request to fabricate working software. Accordingly this Bible is written
as what its own name says it is: a governance and standards document (ten
policy-style standards, DXB-001-010) that specifies philosophy,
information architecture, design system, and functional requirements for
each surface. It does not claim, anywhere, that a website or LMS has been
built; every portal chapter is worded as a specification a real
development team would build against ("shall provide," "must include"),
matching the register the rest of this document suite already uses for
not-yet-built items (compare OPS-010's Allowance Framework, which
specifies a policy without inventing figures no Board has approved).

Registration note. DXB-001-010 is a new, self-contained document series,
not yet entered as rows in the Institutional Governance Compendium's
108-document registry (assets/igc_data.py). Folding ten new rows into
that registry would also require regenerating the Compendium's own
Section 17-22 tables (roster, phase roadmap, priority counts,
responsibility matrix), which are generated FROM that data and would
drift out of sync with a hand-edited addition — the exact defect class
igc_data.py's own docstring exists to prevent. Formal registration is
therefore left as a disclosed follow-on step for the Compendium's next
revision cycle, not done silently or partially here. See the Publication
Certification Statement in assets/dxb_bible_back.md for the same
disclosure in the published document itself.

Single-source-of-truth discipline applied throughout:

  1. Titles. Every office named in this Bible is a title that already
     exists elsewhere in this document suite — Director, Communications
     (Office of Communications); Director, Information Technology (Office
     of Information Technology); Deputy Vice-Chancellor, Academic Affairs;
     Deputy Vice-Chancellor, Administration & Finance; Dean of Students;
     University Registrar; Director, Human Resources; Office of Research;
     Office of Institutional Research; President & Vice-Chancellor; Board
     of Trustees. No "Chief Digital Officer," "Chief Experience Officer,"
     "Chief Information Officer," "Chief Marketing Officer," or similar
     C-suite title is used as a real accountable office anywhere in the
     document body — those roles, named in the directive that prompted
     this Bible, are read as describing the breadth of expertise this
     Bible's guidance should reflect, not as new offices to graft onto a
     Constitution that does not have them. Where the directive's own
     language ("Chief X Officer") appears at all, it appears only inside
     an explanatory aside noting the mapping to the real title, never as
     a Document Control steward or approval authority.

  2. Design system. Colour, type, and voice specifications in DXB-002
     restate — never redefine — the values already in force: Deep Navy
     #122A4E, Gold #B08625, Ivory #F7F3E8 (assets/assemble.py's
     NAVY_HEX/BAND_TINT_HEX and the corrected MKT-001 Brand Style Guide
     table); Fraunces display, Source Serif 4 reading, Archivo structural
     (assets/build_reference.py); tagline "Knowledge Without Barriers."

  3. Language strategy. DXB-009 sets English and Arabic as the only two
     languages live at launch, with French, Urdu, Turkish, Bahasa
     Indonesia, Bahasa Melayu, Hausa, and Swahili named as the
     future-readiness roadmap — matching a corresponding correction
     applied to the published homepage artifact in this same session
     (French and Urdu, previously shown as live, are demoted to the same
     dormant "in preparation" state as the other roadmap languages, so
     the live artifact and this Bible's stated policy do not silently
     disagree with each other).

  4. Pricing. DXB-010's Fee & Pricing Presentation Policy is written to
     the same standard already established for compensation in OPS-010:
     no public commitment to a specific pricing mechanism is stated as a
     binding figure; the University presents fees professionally and
     reserves location-specific pricing, scholarships, and waivers to
     Board-approved policy administered by the Office of Finance, exactly
     as the directive that prompted this Bible requested.

Formatting matches house style throughout: numbered outline points as
bold-numbered paragraphs, sentence-case section headers, no ALL-CAPS
except where the underlying divider/cover typography requires it.
"""

OUT = "/home/user/shroyalschools/work_dxb_bible_body.md"

# ---------------------------------------------------------------------------
# Divider generator (mirrors gen_mkt_handbook_body.py's divider() pattern)
# ---------------------------------------------------------------------------

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def title_size(title):
    n = len(title)
    if n <= 22:
        return 40
    if n <= 34:
        return 32
    if n <= 48:
        return 26
    return 21

def divider(num, code, title, steward, thesis, section_titles):
    tsize = title_size(title)
    rows = []
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="120"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:color w:val="8C97AB"/><w:sz w:val="19"/><w:spacing w:val="14"/></w:rPr><w:t>Digital Experience &amp; Editorial Bible &#183; Standard {num} of 10</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces Black" w:hAnsi="Fraunces Black"/><w:color w:val="B08625"/><w:b/><w:sz w:val="70"/></w:rPr><w:t>{code}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="120" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces Black" w:hAnsi="Fraunces Black"/><w:color w:val="FFFFFF"/><w:b/><w:sz w:val="{tsize*2}"/></w:rPr><w:t>{esc(title)}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="260"/><w:pBdr><w:bottom w:val="single" w:sz="10" w:space="8" w:color="B08625"/></w:pBdr></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:color w:val="8C97AB"/><w:sz w:val="19"/><w:spacing w:val="10"/></w:rPr><w:t>Standard Steward: {esc(steward)}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="360"/><w:ind w:right="700"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces" w:hAnsi="Fraunces"/><w:i/><w:color w:val="DCE3F0"/><w:sz w:val="24"/></w:rPr><w:t>&#8220;{esc(thesis)}&#8221;</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="140"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:b/><w:color w:val="B08625"/><w:sz w:val="18"/><w:spacing w:val="12"/></w:rPr><w:t>Contents of This Standard</w:t></w:r></w:p>''')
    for sec_num, sec_title in section_titles:
        rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="90"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Archivo SemiBold" w:hAnsi="Archivo SemiBold"/><w:color w:val="B08625"/><w:b/><w:sz w:val="17"/></w:rPr><w:t>{sec_num}&#8194;</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Archivo" w:hAnsi="Archivo"/><w:color w:val="FFFFFF"/><w:sz w:val="16"/></w:rPr><w:t>{esc(sec_title)}</w:t></w:r></w:p>''')
    body = "\n".join(rows)
    height = 10600 + min(len(section_titles), 14) * 155
    hidden_marker = (f'<w:p><w:pPr><w:pStyle w:val="Heading2"/><w:spacing w:before="0" w:after="0"/>'
                      f'<w:keepNext w:val="0"/><w:keepLines w:val="0"/>'
                      f'<w:pBdr><w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/></w:pBdr>'
                      f'<w:rPr><w:vanish/><w:sz w:val="2"/></w:rPr></w:pPr>'
                      f'<w:r><w:rPr><w:vanish/><w:sz w:val="2"/></w:rPr><w:t>{code}: {esc(title)}</w:t></w:r></w:p>')
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

def header_block(doc_num, version, effective, review, approval, steward, owner, authority):
    lines = []
    lines.append("| | |")
    lines.append("|---|---|")
    lines.append(f"| **Document Number** | {doc_num} |")
    lines.append(f"| **Version** | {version} |")
    lines.append(f"| **Effective Date** | {effective} |")
    lines.append(f"| **Review Date** | {review} |")
    lines.append(f"| **Approval Authority** | {approval} |")
    lines.append(f"| **Standard Steward** | {steward} |")
    lines.append(f"| **Implementation Owner** | {owner} |")
    lines.append(f"| **Authority** | {authority} |")
    return "\n".join(lines)

PAGEBREAK = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'

# ---------------------------------------------------------------------------
# Standard metadata: (num, code, title, steward, owner, authority, thesis,
#  [(sec_num, sec_title), ...])
# ---------------------------------------------------------------------------
POLICIES = [
 (1, "DXB-001", "Public Website Editorial & Information Architecture Standard",
  "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "One sitemap, reviewed for prestige and cut for clutter, so every visitor reaches the page that matters in two clicks or fewer.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Editorial Philosophy and Emotional Standard"),("6.0","The Never-Display Rule"),
   ("7.0","Site Architecture"),("8.0","Editorial Governance and Review Cycle"),
   ("9.0","Enforcement"),("10.0","Related Documents"),("11.0","Effective Date")]),
 (2, "DXB-002", "Digital Brand & Design System Standard",
  "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "The same navy, gold, and ivory the printed Constitution wears — carried onto every screen without a single reinvented rule.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Typography"),("6.0","Colour System"),("7.0","Spacing and Layout"),
   ("8.0","Components"),("9.0","Imagery, Photography and Illustration"),
   ("10.0","Diagrams and Data Visualization"),("11.0","Accessibility"),
   ("12.0","Enforcement"),("13.0","Related Documents"),("14.0","Effective Date")]),
 (3, "DXB-003", "Learning Management System Functional Framework",
  "Director, Information Technology", "Office of Information Technology",
  "Constitution Article 9, Section 9.1",
  "Ten portals sharing one identity system and one design language, so no student ever has to learn a second interface.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Design Philosophy"),("6.0","Core Capabilities"),("7.0","Portal Inventory"),
   ("8.0","Data Governance and Interoperability"),("9.0","Enforcement"),
   ("10.0","Related Documents"),("11.0","Effective Date")]),
 (4, "DXB-004", "Student Portal Specification",
  "Dean of Students", "Office of Student Affairs",
  "Constitution Article 9, Section 9.1",
  "Every grade, every transcript request, and every announcement a student needs, in one dashboard that never contradicts the Registrar's own record.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Required Capabilities"),("6.0","Academic Records Integrity"),
   ("7.0","Enforcement"),("8.0","Related Documents"),("9.0","Effective Date")]),
 (5, "DXB-005", "Faculty Portal Specification",
  "Deputy Vice-Chancellor, Academic Affairs", "Office of Academic Affairs",
  "Constitution Article 9, Section 9.1",
  "A teaching dashboard built for the classroom first and the spreadsheet never, so faculty time goes to students, not software.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Required Capabilities"),("6.0","Academic Integrity Safeguards"),
   ("7.0","Enforcement"),("8.0","Related Documents"),("9.0","Effective Date")]),
 (6, "DXB-006", "Staff & Administrative Portal Specification",
  "Director, Human Resources", "Office of Human Resources",
  "Constitution Article 9, Section 9.1",
  "One administrative system, role-scoped so tightly that no employee ever sees a record their function does not require.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Required Capabilities"),("6.0","Access Control"),
   ("7.0","Enforcement"),("8.0","Related Documents"),("9.0","Effective Date")]),
 (7, "DXB-007", "Executive Portal & Institutional Analytics Specification",
  "Deputy Vice-Chancellor, Administration & Finance", "Office of Institutional Research",
  "Constitution Article 9, Section 9.1",
  "The same enrollment, revenue, and reserve figures the Board already reads in the Blueprint — current, not re-derived, every time an officer opens the dashboard.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Required Capabilities"),("6.0","Data Integrity and Board Reporting"),
   ("7.0","Enforcement"),("8.0","Related Documents"),("9.0","Effective Date")]),
 (8, "DXB-008", "Research Portal Specification",
  "Office of Research", "Office of Research",
  "Constitution Article 9, Section 9.1",
  "A single record of record for every output the six colleges produce, discoverable by title, author, college, and year.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Required Capabilities"),("6.0","Enforcement"),
   ("7.0","Related Documents"),("8.0","Effective Date")]),
 (9, "DXB-009", "Mobile Experience & Arabic/RTL Localization Standard",
  "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "Arabic is not a translation of the English site; it is the same site, built right-to-left, to the same standard, from the same source of truth.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Mobile Experience Standard"),("6.0","Language Strategy"),
   ("7.0","Arabic and RTL Parity Standard"),("8.0","Future-Language Readiness"),
   ("9.0","Enforcement"),("10.0","Related Documents"),("11.0","Effective Date")]),
 (10, "DXB-010", "Digital Ecosystem Governance & Admissions/Pricing Presentation Policy",
  "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "No public page ever promises a figure the Board has not approved, and no visitor ever needs to know that.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Digital Ecosystem Governance"),("6.0","Admissions Digital Journey"),
   ("7.0","Fee and Pricing Presentation Policy"),("8.0","Enforcement"),
   ("9.0","Related Documents"),("10.0","Effective Date")]),
]

APPROVAL = {
 1: "Deputy Vice-Chancellor, Administration & Finance",
 2: "Deputy Vice-Chancellor, Administration & Finance",
 3: "President & Vice-Chancellor",
 4: "President & Vice-Chancellor",
 5: "President & Vice-Chancellor",
 6: "Deputy Vice-Chancellor, Administration & Finance",
 7: "Deputy Vice-Chancellor, Administration & Finance",
 8: "President & Vice-Chancellor",
 9: "Deputy Vice-Chancellor, Administration & Finance",
 10: "Board of Trustees",
}

VERSION_EFFECTIVE_REVIEW = ("1.0", "1 January 2028", "Annual")

CONTENT = {}

CONTENT[1] = '''
## 1.0 Purpose

**1.1** The purpose of this Standard is to govern the public website's editorial philosophy, information architecture, and review discipline, so that every page a visitor reaches reads as the work of a serious, permanent institution.

**1.2** This Standard exists because a website is read once by most visitors and never again; it carries the University's first impression more heavily than any other document in this suite, and must be held to that standard deliberately, not by accident.

## 2.0 Scope

**2.1** This Standard applies to:

**2.1.1** Every publicly reachable page under the University's primary domain;

**2.1.2** Every subdomain, microsite, or campaign page created by any office;

**2.1.3** All editorial content published to the public website, regardless of author;

**2.1.4** Third-party vendors or agencies producing public-facing web content on the University's behalf.

**2.2** This Standard does not apply to the Learning Management System or any of the six operating portals specified in DXB-003 through DXB-008, which are authenticated, non-public surfaces governed separately.

## 3.0 Definitions

**3.1 Public website.** The unauthenticated, publicly reachable surface of the University's digital presence.

**3.2 Information architecture (IA).** The structure, labeling, and navigation scheme of the public website.

**3.3 Never-Display Rule.** The rule, defined in Section 6.0, restricting what categories of internal content may never appear on the public website.

**3.4 Editorial Director role.** For the purposes of this Standard, the function of final editorial review over public-website content, held by the Director, Communications, and not a separate office.

## 4.0 Policy Statement

**4.1** The public website shall be governed as an editorial product, not a technical artifact: every page shall have a stated purpose, a named audience, and a single job, reviewed before publication.

**4.2** The public website's information architecture shall be reviewed against this Standard not less than annually, and any page or menu item that does not strengthen prestige, usability, or scholarly credibility shall be removed, merged, or redesigned.

**4.3** No page shall be published to the public website without passing the Never-Display Rule review in Section 6.0.

## 5.0 Editorial Philosophy and Emotional Standard

**5.1** The public website's target emotional response, on first arrival, is: trust, authority, scholarship, prestige, permanence.

**5.2** The public website shall never read as: a content-management-system template, a school-administration portal, a startup landing page, or a marketing funnel.

**5.3** The standard for comparison is not other university websites in the University's own founding-decade stage; it is the public presence of long-established Gulf, Saudi, and UK institutions, and of premier international organizations — because a founding-decade institution asking to be taken seriously must present at the standard of the institutions it intends to be judged alongside, not the standard of its own current size.

**5.4** Every page shall be reviewed, before publication, against a single test: would an international professor, an accreditation evaluator, a trustee, a donor, or a prospective student conclude, from this page alone, that the University is a serious, permanent institution. A page that fails this test is not published until it passes.

## 6.0 The Never-Display Rule

**6.1** The public website is not an internal working document, and shall never display:

**6.1.1** Internal audits, editorial-review logs, or defect-tracking records of the kind maintained for this document suite's own production;

**6.1.2** Development roadmaps, sprint plans, or "coming soon" language that reveals an internal build schedule;

**6.1.3** Internal committee debates, meeting minutes, or draft-stage disagreements;

**6.1.4** Draft or work-in-progress status markers on any published page — a page is either published, to the standard this Standard sets, or it is not published at all;

**6.1.5** Governance weaknesses, unresolved risks, or open compliance gaps, however honestly they may be recorded in the University's internal governance documents.

**6.2** This rule does not require concealment or misrepresentation. Where the University has not yet completed something a visitor might reasonably expect (see, for example, DXB-004 through DXB-008's specification-stage LMS portals, or the Leadership section's founding-appointment status), the honest and permitted approach is a plainly worded, dignified statement of current status — never a fabricated claim, and never an internal-facing document repurposed for public display.

**6.3** The distinction this Section draws is the same one this entire document suite already observes: a governance document that discloses an audit's own limitations (see the Institutional Governance Compendium's Publication Certification Statement) is written for the Board, Senate, and accreditation reviewers, not for the public website. What belongs on the public website is the University's settled, current position — not the internal record of how it got there.

## 7.0 Site Architecture

**7.1** The public website's top-level navigation shall consist of not more than seven primary items, selected for prestige, usability, and scholarly credibility, and reviewed against Section 7.2 before any addition.

**7.2** The reviewed and adopted top-level structure is:

**7.2.1** Home;

**7.2.2** About AMIU — Vision, Mission, the ISLAMIC Framework, Governance, University Charter;

**7.2.3** Academics — the six founding Colleges (Qur'anic & Hadith Sciences; Sharī'ah & Islamic Law; Islamic Theology & Philosophy; Arabic Language & Linguistics; Da'wah, Islamic Communication & Chaplaincy; Islamic Finance, Economics & Waqf Administration) and the Academic Ladder;

**7.2.4** Admissions — the seven-step digital journey specified in DXB-010, Section 6.0;

**7.2.5** Research — a placeholder section pointing to the Research Portal (DXB-008) once populated, never a page listing research that does not yet exist;

**7.2.6** Waqf & Endowment — the University's own perpetual-endowment framework;

**7.2.7** Contact.

**7.3** A dedicated "Student Life," "News & Media," "Library," and "Alumni" section shall each be added to the top-level navigation only once there is real content to populate it — a named section with no real content behind it fails the Never-Display Rule (Section 6.1.4) and the emotional standard (Section 5.4) simultaneously, reading as an unfinished template rather than a deliberate omission.

**7.4** Every top-level item shall resolve to real content in not more than two navigation steps from the homepage.

**7.5** The public website shall carry a single persistent identity element (the University seal and wordmark) on every page, per DXB-002, Section 6.0.

## 8.0 Editorial Governance and Review Cycle

**8.1** The Office of Communications shall maintain an editorial calendar for the public website, reviewed quarterly.

**8.2** Any page unreviewed for more than twelve months shall be flagged for re-review, expansion, or removal.

**8.3** No page shall be published without the Director, Communications' review against Sections 5.0 and 6.0 of this Standard.

## 9.0 Enforcement

**9.1** Any office publishing public-website content outside this Standard's review process is subject to correction by the Office of Communications and, for repeated violations, referral to the Deputy Vice-Chancellor, Administration & Finance.

## 10.0 Related Documents

**10.1** Brand Style Guide (MKT-001); Website Content Plan (MKT-002); Digital Brand & Design System Standard (DXB-002); Mobile Experience & Arabic/RTL Localization Standard (DXB-009); Digital Ecosystem Governance & Admissions/Pricing Presentation Policy (DXB-010).

## 11.0 Effective Date

**11.1** This Standard is effective as of the date shown in the Document Control block above.
'''

CONTENT[2] = '''
## 1.0 Purpose

**1.1** The purpose of this Standard is to extend the University's existing print and editorial design system to every digital surface, so that a visitor moving from a printed publication to the website, or from the website to the Student Portal, never perceives a change of institution.

## 2.0 Scope

**2.1** This Standard applies to the public website, the Learning Management System, all six operating portals specified in DXB-003 through DXB-008, and any mobile application the University publishes.

**2.2** This Standard does not create new colours, typefaces, or brand voice; it applies the Brand Style Guide (MKT-001) to digital contexts the print-oriented Guide does not address directly (interactive components, responsive layout, dark-mode presentation, accessibility).

## 3.0 Definitions

**3.1 Design token.** A named, reusable design value (a colour, a type size, a spacing unit) referenced by components rather than hard-coded, so a single update propagates everywhere it is used.

**3.2 Component.** A reusable interface element (a button, a card, a table, a form field) built once to this Standard and reused across every digital surface.

## 4.0 Policy Statement

**4.1** Every digital surface shall be built from the colour, type, spacing, and component standards in this Section, expressed as design tokens rather than page-by-page choices.

**4.2** No digital surface shall introduce a colour, typeface, or component style not defined in this Standard without the Director, Communications' written approval.

## 5.0 Typography

**5.1** Display type (headlines, cover-style moments, large numerals) shall use Fraunces, in Black or SemiBold weight, matching the printed Constitution's cover and Part-divider typography.

**5.2** Reading type (body copy, long-form prose) shall use Source Serif 4.

**5.3** Structural type (navigation, labels, captions, table data, small-caps-style eyebrows) shall use Archivo.

**5.4** Arabic display type shall use Noto Kufi Arabic; Arabic reading and structural type shall use Noto Naskh Arabic — a serif-leaning book face that pairs with Source Serif 4's register, not a generic UI sans substituted for convenience.

**5.5** No digital surface shall substitute a system font, a generic web-safe font, or a font not named in this Section, under any circumstance, including font-loading fallback — every digital surface shall embed its required fonts rather than risk an unstyled fallback rendering.

## 6.0 Colour System

**6.1** The University's three core colours, unchanged from MKT-001's corrected table, are: Deep Navy #122A4E (primary), Gold #B08625 (accent), Ivory #F7F3E8 (background/panel tint).

**6.2** Digital surfaces may extend this palette with tonal variants (a darker navy for high-contrast grounds, a brighter gold for dark-mode accents, a warm near-white for light-mode page backgrounds) provided every variant is derived from, and named in reference to, one of the three core colours — never an unrelated hue introduced independently by a single project.

**6.3** Every digital surface shall support both a light and a dark presentation, each meeting a minimum 4.5:1 text contrast ratio against its ground, per Section 11.0.

## 7.0 Spacing and Layout

**7.1** Digital surfaces shall lay out sibling elements using a consistent spacing scale rather than per-element margins chosen ad hoc.

**7.2** Reading-width text (body copy, policy prose) shall be set to a measure of approximately 60-75 characters per line, matching the readability standard already applied to this document suite's own printed page.

**7.3** Wide content (data tables, credential ladders, dashboards) shall scroll within its own container rather than force the page itself to scroll horizontally.

## 8.0 Components

**8.1 Navigation.** Primary navigation shall carry not more than seven items (per DXB-001, Section 7.1) and shall visually indicate the visitor's current location.

**8.2 Cards.** Where a card-style layout is used, it shall carry a hairline rule or flat panel treatment consistent with the printed exhibit-plate frame already used for this document suite's figures — not a generic drop-shadowed, heavily rounded card of the kind common to template-built sites.

**8.3 Tables.** Every data table on any digital surface shall use a navy header row, a gold rule beneath the header, and alternating ivory/cream row bands — the same premium-table treatment already applied to this document suite's own printed tables (see the Academic Ladder table, DXB-001's companion homepage artifact).

**8.4 Forms.** Every form field shall carry a visible label (not a placeholder-only label), a visible focus state, and an error message that states what is wrong and how to fix it, per Section 11.0.

## 9.0 Imagery, Photography and Illustration

**9.1** The University shall not publish photography purporting to depict a campus, students, or facilities that do not yet exist. During the pre-launch and founding-cohort period, digital surfaces shall use the official seal, abstract geometric brand motifs (see Section 9.2), and typographic composition in place of photography.

**9.2** Approved abstract motifs draw on Islamic geometric and architectural tradition (mashrabiya lattice patterns, eight-fold star geometry, hairline rule compositions) rendered in the brand palette — never a generic stock-photo aesthetic, and never a motif borrowed from another institution's visual identity.

**9.3** Once real photography exists (a physical campus, an enrolled cohort, a graduation), it shall be commissioned to a single consistent style guide (lighting, composition, colour grading) rather than accumulated ad hoc from multiple sources.

## 10.0 Diagrams and Data Visualization

**10.1** Institutional diagrams (governance structure, organisational relationships, process flows) shall be built as clean, custom compositions in the brand system — navy/gold/ivory, Fraunces and Archivo type — never a generic default flowchart of boxes and arrows in an unrelated colour scheme.

**10.2** Data visualizations (enrollment growth, revenue, reserve balances) shall use tabular figures (fixed-width numerals) so that columns of numbers align, and shall cite the source document and figure (for example, "Strategic Blueprint, Section 34") for every number shown.

**10.3** No digital surface shall present a figure that does not also appear, or is not directly derivable from, the Strategic Blueprint, the adopted financial model, or another named governance document — a dashboard number with no traceable source is not permitted.

## 11.0 Accessibility

**11.1** Every digital surface shall meet WCAG 2.1 Level AA at minimum: sufficient colour contrast, full keyboard navigability, visible focus states, and alternative text for non-decorative imagery.

**11.2** Every digital surface shall respect a visitor's reduced-motion preference, disabling non-essential animation when requested.

## 12.0 Enforcement

**12.1** Any digital surface built outside this Standard is subject to remediation before public or authenticated release, at the direction of the Director, Communications in consultation with the Director, Information Technology.

## 13.0 Related Documents

**13.1** Brand Style Guide (MKT-001); Public Website Editorial & Information Architecture Standard (DXB-001); Mobile Experience & Arabic/RTL Localization Standard (DXB-009).

## 14.0 Effective Date

**14.1** This Standard is effective as of the date shown in the Document Control block above.
'''

CONTENT[3] = '''
## 1.0 Purpose

**1.1** The purpose of this Standard is to specify the functional framework the University's Learning Management System and its operating portals shall be built to, so that any future development effort works from one set of requirements rather than each portal being designed independently.

**1.2** This Standard is a specification, not a record of software already built. No provision of this Standard, or of DXB-004 through DXB-008, shall be read to claim that any portal described here is operational.

## 2.0 Scope

**2.1** This Standard applies to the Learning Management System core and to all ten portals it comprises: Student, Faculty, Staff, Executive, Registrar, Admissions, Finance, Examination, Alumni, and Research.

**2.2** DXB-004 through DXB-008 specify five of these ten portals (Student, Faculty, Staff, Executive, Research) in dedicated standards, reflecting their distinct user populations and data-sensitivity profiles. The Registrar, Admissions, Finance, Examination, and Alumni portals are governed by this Standard's Section 7.0 pending dedicated standards of their own in a future revision.

## 3.0 Definitions

**3.1 Learning Management System (LMS).** The University's integrated system for course delivery, assessment, and academic-record management.

**3.2 Portal.** A role-scoped interface into the LMS and its associated institutional systems, serving one defined user population.

**3.3 Single sign-on (SSO).** An authentication scheme allowing one credential to access every portal a person is authorized for.

## 4.0 Policy Statement

**4.1** The LMS and every portal it comprises shall be built to the Digital Brand & Design System Standard (DXB-002), so that no portal feels like a separately branded piece of third-party software.

**4.2** Every portal shall be accessed through a single authentication system supporting single sign-on and multi-factor authentication, with access scoped by role under a role-based access control (RBAC) model.

**4.3** No portal shall expose a data field, record, or capability to a role not expressly authorized for it under the relevant portal specification.

## 5.0 Design Philosophy

**5.1** The LMS shall read as a coherent university operating system, not as a repurposed generic course-management tool: one identity system, one navigation language, one data model, shared across every portal.

**5.2** Every portal shall present its most consequential information first (grades due for release, an application awaiting decision, a reserve balance falling behind plan) rather than requiring the user to search for it — the interface shall surface state, not merely list data.

## 6.0 Core Capabilities

**6.1** The LMS core shall provide: course and curriculum management; content delivery (readings, recorded and live sessions); assessment authoring, submission, and grading; a gradebook feeding directly into the official academic record; attendance capture; and institution-wide announcements.

**6.2** The LMS shall provide academic-integrity tooling (originality/plagiarism checking) and, where a course requires it, integration with a proctoring service for remote assessment — specified as an integration point, not built in-house.

**6.3** The LMS shall provide a messaging system scoped to legitimate academic and administrative communication, and a Help Centre accessible from every portal.

## 7.0 Portal Inventory

**7.1** The ten portals and their primary user populations are:

**7.1.1** Student Portal — enrolled students (DXB-004);

**7.1.2** Faculty Portal — teaching and research faculty (DXB-005);

**7.1.3** Staff Portal — administrative and operational staff (DXB-006);

**7.1.4** Executive Portal — the President & Vice-Chancellor, Deputy Vice-Chancellors, and Board of Trustees (DXB-007);

**7.1.5** Registrar Portal — the Office of the Registrar, for enrollment, transcript issuance, and degree verification;

**7.1.6** Admissions Portal — the Office of Admissions, for the application journey specified in DXB-010, Section 6.0;

**7.1.7** Finance Portal — the Office of Finance, for invoicing, payment processing, and scholarship administration;

**7.1.8** Examination Portal — the Office of the Registrar and relevant Colleges, for examination scheduling, proctoring coordination, and results processing;

**7.1.9** Alumni Portal — graduates, for continued community access and giving;

**7.1.10** Research Portal — the research community (DXB-008).

**7.2** The Registrar, Admissions, Finance, and Examination Portals share the Student and Staff Portals' underlying data model (a single academic record, a single financial record) rather than maintaining independent copies — the transcript a Registrar issues and the transcript a student requests through the Student Portal shall be the same record, not two records reconciled after the fact.

## 8.0 Data Governance and Interoperability

**8.1** The LMS shall maintain a single system of record for each data domain (academic record, financial record, admissions record); no portal shall maintain a competing copy of another portal's system of record.

**8.2** All academic-record data displayed in any portal shall trace to the Registrar's system of record; a discrepancy between a portal's display and the Registrar's record is a defect to be corrected in the portal, never resolved by treating the portal's figure as authoritative.

**8.3** Certificate and transcript issuance shall include a verification mechanism (a QR code and a public verification lookup) sufficient to deter and detect fraudulent alteration.

## 9.0 Enforcement

**9.1** Any portal or integration built outside this framework is subject to review and remediation by the Office of Information Technology before connection to the LMS core.

## 10.0 Related Documents

**10.1** Digital Brand & Design System Standard (DXB-002); Student Portal Specification (DXB-004); Faculty Portal Specification (DXB-005); Staff & Administrative Portal Specification (DXB-006); Executive Portal & Institutional Analytics Specification (DXB-007); Research Portal Specification (DXB-008).

## 11.0 Effective Date

**11.1** This Standard is effective as of the date shown in the Document Control block above.
'''

CONTENT[4] = '''
## 1.0 Purpose

**1.1** The purpose of this Specification is to define the required capabilities of the Student Portal, so that every enrolled student has one dependable place to see their academic standing, communicate with the University, and act on what they see.

## 2.0 Scope

**2.1** This Specification applies to the Student Portal as a component of the Learning Management System defined in DXB-003, and to any mobile application presenting the same capabilities.

## 3.0 Definitions

**3.1 Academic progress record.** The cumulative, Registrar-sourced record of a student's completed and in-progress coursework toward a credential on the Academic Ladder (Constitution Article X, Section 10.1).

## 4.0 Policy Statement

**4.1** The Student Portal shall present the capabilities in Section 5.0, sourced from the systems of record specified in DXB-003, Section 8.0, and from no other source.

**4.2** No figure or status shown in the Student Portal (a grade, a GPA, a transcript, a degree-progress percentage) shall differ from the Registrar's official record; where the two cannot yet be reconciled, the portal shall display nothing rather than an unverified figure.

## 5.0 Required Capabilities

**5.1** The Student Portal shall provide:

**5.1.1** A dashboard summarizing the student's current standing: enrolled courses, upcoming deadlines, and any action required of them;

**5.1.2** A timetable of enrolled course sessions;

**5.1.3** Course access (readings, recorded and live sessions, assignments) for every enrolled course;

**5.1.4** Assessment submission and results, as released by faculty per DXB-005;

**5.1.5** Grades and cumulative GPA, sourced from the Registrar's system of record;

**5.1.6** Transcript requests, routed to the Registrar Portal (DXB-003, Section 7.1.5) and fulfilled through the verification mechanism specified in DXB-003, Section 8.3;

**5.1.7** Certificate access and verification, for any credential the student has completed;

**5.1.8** Academic progress tracking against the student's declared credential on the Academic Ladder, including graduation-eligibility tracking;

**5.1.9** Attendance records, where attendance is a condition of a course or program;

**5.1.10** Institution-wide and course-level announcements;

**5.1.11** Messaging with faculty and relevant administrative offices, scoped to legitimate academic communication;

**5.1.12** A Help Centre and a defined path to submit an academic appeal, consistent with the Student Policies Handbook.

**5.2** The Student Portal may provide an academic-assistant feature (a tool helping a student navigate their own academic record, deadlines, and University policy) provided any such feature is scoped to the student's own verified data and to published University policy, and is clearly identified to the student as an automated tool, not a substitute for an academic advisor.

## 6.0 Academic Records Integrity

**6.1** Grade changes, once released to a student, shall follow the correction process specified in the Academic Handbook; the Student Portal shall never allow a silent, unlogged change to a released grade.

**6.2** Every transcript and certificate generated through the Student Portal shall carry the verification mechanism specified in DXB-003, Section 8.3.

## 7.0 Enforcement

**7.1** Any deviation between the Student Portal's displayed figures and the Registrar's system of record is a reportable defect under the Office of Information Technology's incident process.

## 8.0 Related Documents

**8.1** Learning Management System Functional Framework (DXB-003); Academic Handbook (AMIU-ACAH-001); Student Policies Handbook (AMIU-STUH-001).

## 9.0 Effective Date

**9.1** This Specification is effective as of the date shown in the Document Control block above.
'''

CONTENT[5] = '''
## 1.0 Purpose

**1.1** The purpose of this Specification is to define the required capabilities of the Faculty Portal, so that teaching, assessment, and research-tracking time is spent on substance, not on navigating software.

## 2.0 Scope

**2.1** This Specification applies to the Faculty Portal as a component of the Learning Management System defined in DXB-003.

## 3.0 Definitions

**3.1 Teaching load.** The set of course sections a faculty member is assigned to in a given term.

## 4.0 Policy Statement

**4.1** The Faculty Portal shall present the capabilities in Section 5.0, built to the Digital Brand & Design System Standard (DXB-002) and sharing the Student Portal's underlying course and academic-record data model.

**4.2** Grade release through the Faculty Portal shall write directly to the Registrar's system of record; no parallel gradebook shall be maintained outside the Faculty Portal for any course of record.

## 5.0 Required Capabilities

**5.1** The Faculty Portal shall provide:

**5.1.1** A teaching dashboard summarizing the faculty member's current teaching load, upcoming sessions, and pending grading;

**5.1.2** Course management (syllabus, content, session scheduling) for every assigned section;

**5.1.3** Attendance capture for every assigned section;

**5.1.4** Assessment tools: assignment and examination authoring, submission collection, rubric-based grading, and integration with the academic-integrity tooling specified in DXB-003, Section 6.2;

**5.1.5** Research tracking: a faculty member's own ongoing research projects, grants, and collaborations, feeding into the Research Portal (DXB-008) rather than being maintained separately;

**5.1.6** Publication records, similarly feeding into the Research Portal;

**5.1.7** Student advising tools, where a faculty member holds an advising role, showing only the advisees assigned to them;

**5.1.8** Academic analytics scoped to the faculty member's own courses (grade distributions, engagement indicators) to support teaching improvement — not institution-wide analytics, which are reserved to the Executive Portal (DXB-007).

## 6.0 Academic Integrity Safeguards

**6.1** Grade submission shall require faculty authentication and shall be logged; a released grade may be changed only through the correction process specified in the Academic Handbook, never by silent overwrite.

**6.2** Assessment content shall be access-controlled so that only the assigned faculty member and authorized Registrar staff can view it before the assessment date.

## 7.0 Enforcement

**7.1** Any bypass of the Faculty Portal's grade-submission or assessment-security controls is subject to review under the Academic Handbook's academic-integrity provisions.

## 8.0 Related Documents

**8.1** Learning Management System Functional Framework (DXB-003); Student Portal Specification (DXB-004); Research Portal Specification (DXB-008); Academic Handbook (AMIU-ACAH-001).

## 9.0 Effective Date

**9.1** This Specification is effective as of the date shown in the Document Control block above.
'''

CONTENT[6] = '''
## 1.0 Purpose

**1.1** The purpose of this Specification is to define the required capabilities of the Staff & Administrative Portal, so that every non-academic function of the University operates from one shared administrative system rather than a patchwork of spreadsheets and email.

## 2.0 Scope

**2.1** This Specification applies to the Staff Portal as used by the Offices of Human Resources, Facilities, Communications, Information Technology, and other administrative units not separately specified in DXB-004, DXB-005, DXB-007, or DXB-008.

## 3.0 Definitions

**3.1 Functional area.** An administrative office (per Constitution Article 9, Section 9.2(f)) with a defined operational scope.

## 4.0 Policy Statement

**4.1** The Staff Portal shall present each staff member only the capabilities and records relevant to their own functional area, per the access-control model in Section 6.0.

## 5.0 Required Capabilities

**5.1** The Staff Portal shall provide, scoped by functional area:

**5.1.1** An administrative dashboard summarizing tasks, requests, and approvals pending the staff member's action;

**5.1.2** Human-resources self-service (leave requests, benefits information, the allowance-framework requests specified in OPS-010's Allowance Framework);

**5.1.3** Facilities and procurement request tracking;

**5.1.4** Internal announcements and directory access;

**5.1.5** A Help Centre and internal-ticketing capability for the Office of Information Technology.

## 6.0 Access Control

**6.1** Access to the Staff Portal shall be governed by role-based access control per DXB-003, Section 4.2; a staff member's access shall be limited to their own functional area's records unless expressly granted broader access by their Director.

**6.2** Access shall be revoked upon separation from the University, per the Human Resources & Personnel Policy (OPS-007).

## 7.0 Enforcement

**7.1** Unauthorized access to another functional area's records through the Staff Portal is subject to the Human Resources & Personnel Policy's disciplinary provisions.

## 8.0 Related Documents

**8.1** Learning Management System Functional Framework (DXB-003); Human Resources & Personnel Policy (OPS-007); Compensation, Honoraria, Stipends, Allowances & Revenue Participation Policy (OPS-010).

## 9.0 Effective Date

**9.1** This Specification is effective as of the date shown in the Document Control block above.
'''

CONTENT[7] = '''
## 1.0 Purpose

**1.1** The purpose of this Specification is to define the required capabilities of the Executive Portal, so that the President & Vice-Chancellor, the Deputy Vice-Chancellors, and the Board of Trustees can see the University's current position without re-deriving it from separate reports.

## 2.0 Scope

**2.1** This Specification applies to the Executive Portal as used by the President & Vice-Chancellor, the Deputy Vice-Chancellors, and, through Board-level reporting exports, the Board of Trustees and its committees.

## 3.0 Definitions

**3.1 Institutional KPI.** A key performance indicator drawn from the adopted Strategic Blueprint or financial model, not a locally invented metric.

## 4.0 Policy Statement

**4.1** Every figure presented in the Executive Portal shall trace to a named source document (the Strategic Blueprint, the adopted financial model, the Registrar's or Office of Finance's systems of record) and shall be labeled with that source, per DXB-002, Section 10.3.

**4.2** The Executive Portal shall not present a projection or estimate as though it were an actual, recorded figure; projections shall be clearly labeled as such.

## 5.0 Required Capabilities

**5.1** The Executive Portal shall provide:

**5.1.1** Institutional KPIs against the adopted Strategic Blueprint's Growth Scenario (enrollment, revenue, and reserve figures by year);

**5.1.2** Academic analytics (enrollment by College, program completion rates, credential-ladder progression) aggregated from the Registrar's system of record;

**5.1.3** Financial analytics (revenue, the eight fixed budget-allocation categories, the Liquidity and Waqf Reserve balances) sourced from the Office of Finance;

**5.1.4** Admissions analytics (application volume, conversion by stage of the admissions journey specified in DXB-010, Section 6.0);

**5.1.5** Student-success metrics (retention, progression, time-to-credential);

**5.1.6** Accreditation-monitoring status, tracking the University's accreditation-candidacy timeline (Strategic Blueprint, Years 11-12) against milestones;

**5.1.7** Risk monitoring, surfacing indicators the Audit & Risk Committee has flagged for tracking;

**5.1.8** Strategic reporting exports formatted for Board of Trustees meetings.

## 6.0 Data Integrity and Board Reporting

**6.1** Figures presented to the Board of Trustees through the Executive Portal shall be reconciled against the Office of Finance's audited figures before each Board meeting; a discrepancy shall be disclosed to the Board, not silently corrected after the fact.

## 7.0 Enforcement

**7.1** Any figure shown in the Executive Portal without a traceable source, per Section 4.1, shall be removed from the interface until its source is established.

## 8.0 Related Documents

**8.1** Learning Management System Functional Framework (DXB-003); Strategic Implementation Blueprint 2028-2050 (AMIU-SB-002); Institutional Governance Compendium (AMIU-IGC-004).

## 9.0 Effective Date

**9.1** This Specification is effective as of the date shown in the Document Control block above.
'''

CONTENT[8] = '''
## 1.0 Purpose

**1.1** The purpose of this Specification is to define the required capabilities of the Research Portal, so that the research output of the six founding Colleges is discoverable and attributable from a single record of record.

## 2.0 Scope

**2.1** This Specification applies to the Research Portal as used by faculty, research staff, and, for published outputs, the public.

## 3.0 Definitions

**3.1 Research output.** A publication, dataset, or funded project attributable to University faculty or affiliated researchers.

## 4.0 Policy Statement

**4.1** The Research Portal shall maintain a single record of research output per faculty member, populated from the Faculty Portal's research-tracking fields (DXB-005, Section 5.1.5-5.1.6) rather than a separately maintained list.

**4.2** Published research outputs shall be publicly discoverable; unpublished or in-progress projects shall be visible only to the researcher and authorized collaborators.

## 5.0 Required Capabilities

**5.1** The Research Portal shall provide:

**5.1.1** A searchable record of research output by title, author, College, and year;

**5.1.2** Project and grant tracking for in-progress research;

**5.1.3** A conference and events listing for University-affiliated research activity;

**5.1.4** Once the University publishes its own research journal, a dedicated repository section for it, added only when real content exists (per the Never-Display Rule, DXB-001, Section 6.1.4).

## 6.0 Enforcement

**6.1** Any research output attributed to the University through the Research Portal shall be verifiable against the Faculty Portal's own record; unverifiable attributions shall be removed pending confirmation.

## 7.0 Related Documents

**7.1** Faculty Portal Specification (DXB-005); Learning Management System Functional Framework (DXB-003).

## 8.0 Effective Date

**8.1** This Specification is effective as of the date shown in the Document Control block above.
'''

CONTENT[9] = '''
## 1.0 Purpose

**1.1** The purpose of this Standard is to govern the mobile experience of every digital surface and the University's language strategy, so that Arabic-reading and mobile visitors receive the same standard of design the English-reading desktop visitor receives, not a reduced version of it.

## 2.0 Scope

**2.1** This Standard applies to every digital surface specified in this Bible, on every device and in every supported language.

## 3.0 Definitions

**3.1 RTL (right-to-left).** The reading direction of Arabic and other Semitic scripts, requiring layout mirroring, not merely text-direction reversal.

**3.2 Launch language.** A language presented as fully live and functional to visitors at a given time, as distinct from a roadmap language.

**3.3 Roadmap language.** A language named as a future-readiness commitment but not yet live, shown honestly as such (per the Never-Display Rule, DXB-001, Section 6.1.4, read together with Section 6.2's permission for dignified current-status statements).

## 4.0 Policy Statement

**4.1** English and Arabic are the University's two launch languages, live and complete on every digital surface from first release.

**4.2** French, Urdu, Turkish, Bahasa Indonesia, Bahasa Melayu, Hausa, and Swahili are the University's named future-readiness roadmap, architected for but not launched.

**4.3** No digital surface shall present a roadmap language as though it were live; every roadmap-language affordance (a language-selector entry, for example) shall be visibly and honestly marked as not yet available, per Section 8.0.

## 5.0 Mobile Experience Standard

**5.1** Every digital surface shall be designed mobile-first: legible without zooming, operable with touch targets of adequate size, and functional on the connection speeds typical of the University's target markets.

**5.2** Where a native mobile application is built, it shall meet a premium native-application standard of polish (fluid navigation, offline access to already-loaded course content, push notifications for deadlines and announcements) — not a web page wrapped in an application shell.

## 6.0 Language Strategy

**6.1** Arabic shall receive equal design quality to English, not a translated overlay on an English-designed layout: typography, spacing, and component proportions shall each be reviewed and, where the script requires it, adjusted for Arabic specifically (see Section 7.0).

**6.2** Full localization (not machine translation) shall be the standard for both launch languages; every string presented to a user shall be authored or reviewed by a competent speaker of that language before release.

## 7.0 Arabic and RTL Parity Standard

**7.1** Every digital surface's layout shall mirror correctly under Arabic: navigation, forms, tables, and diagrams shall reorder to right-to-left reading order, not merely reverse text alignment while leaving layout structure unchanged.

**7.2** Arabic display type shall use Noto Kufi Arabic and Arabic reading type shall use Noto Naskh Arabic, per DXB-002, Section 5.4, each embedded rather than left to system-font fallback.

**7.3** Arabic body text shall be set with generously increased line-height relative to the Latin-script equivalent, reflecting the script's own typographic requirements, not the Latin measure applied unchanged.

**7.4** A structural device with a fixed meaning in English (for example, the ISLAMIC-framework acronym's seven initial letters) shall be retained in its original form in Arabic rather than force-translated into a device that no longer carries the same meaning, with the surrounding prose fully translated around it.

## 8.0 Future-Language Readiness

**8.1** The digital architecture shall support adding a roadmap language (Section 4.2) without a structural rebuild: all user-facing strings shall be maintained in a translatable, centrally managed form, not hard-coded per page.

**8.2** A roadmap language's selector entry, where shown at all, shall be visibly inactive and labeled as being in preparation; it shall never link to untranslated or partially translated content presented as complete.

## 9.0 Enforcement

**9.1** Any digital surface found presenting a roadmap language as live, or presenting machine-translated content as fully localized, shall be corrected before continued public release.

## 10.0 Related Documents

**10.1** Digital Brand & Design System Standard (DXB-002); Public Website Editorial & Information Architecture Standard (DXB-001).

## 11.0 Effective Date

**11.1** This Standard is effective as of the date shown in the Document Control block above.
'''

CONTENT[10] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to assign accountability for the digital ecosystem as a whole, to specify the admissions digital journey, and to govern how fees and pricing are presented to the public — so that no single office can silently commit the University to a claim, figure, or promise no properly constituted authority has approved.

## 2.0 Scope

**2.1** This Policy applies to the governance of the digital ecosystem specified across DXB-001 through DXB-009, to the admissions journey presented on any digital surface, and to the public presentation of fees, tuition, and pricing.

## 3.0 Definitions

**3.1 Digital ecosystem.** The public website, the Learning Management System, and all portals specified in this Bible, considered collectively.

**3.2 Location-specific pricing adjustment.** A variation in the price presented to an applicant based on their country or region of residence, applied automatically by the system rather than separately negotiated.

## 4.0 Policy Statement

**4.1** Accountability for the digital ecosystem is distributed across the real offices named in Section 5.0; no single new office is created by this Bible to hold blanket authority over it.

**4.2** The admissions digital journey shall follow the seven stages specified in Section 6.0, in order, for every applicant.

**4.3** Fees and pricing shall be presented professionally and without public explanation of the University's internal pricing-variation mechanism, per Section 7.0.

## 5.0 Digital Ecosystem Governance

**5.1** Accountability for the digital ecosystem is held as follows:

**5.1.1** The Director, Communications (Office of Communications) is accountable for the public website's editorial standard (DXB-001) and the Digital Brand & Design System Standard (DXB-002), and for this Standard;

**5.1.2** The Director, Information Technology (Office of Information Technology) is accountable for the Learning Management System and portal infrastructure (DXB-003), and for information security across the digital ecosystem;

**5.1.3** Each portal's specification (DXB-004 through DXB-008) is stewarded by the office whose function it primarily serves, per that Specification's own Document Control block;

**5.1.4** The President & Vice-Chancellor holds final accountability for any cross-cutting conflict between offices' digital-ecosystem responsibilities, consistent with the President's constitutional role as the single operational link between the Board of Trustees and the University Senate (Constitution Article V, Section 5 and Article VIII);

**5.1.5** The Board of Trustees, through its Audit & Risk Committee, receives periodic reporting on digital-ecosystem risk (security incidents, data-integrity findings) via the Executive Portal (DXB-007).

**5.2** No "Chief Digital Officer," "Chief Experience Officer," or comparable new executive office is established by this Policy; the breadth of expertise such a title might imply is exercised collectively by the offices named in Section 5.1, coordinated by the President & Vice-Chancellor.

## 6.0 Admissions Digital Journey

**6.1** The admissions digital journey, presented consistently across the public website and the Admissions Portal, consists of seven stages:

**6.1.1** Explore Programme — the prospective applicant reviews the Academic Ladder and College offerings (DXB-001, Section 7.2.3);

**6.1.2** Eligibility Review — the applicant checks program-specific eligibility criteria before beginning an application;

**6.1.3** Apply — the applicant submits the application and required materials through the Admissions Portal;

**6.1.4** Document Verification — the Office of Admissions verifies submitted credentials and identity documents;

**6.1.5** Admission Decision — a decision is issued and communicated through the Admissions Portal and, where applicable, the Student Portal;

**6.1.6** Enrolment — the admitted applicant completes enrollment, including any financial arrangement per Section 7.0;

**6.1.7** Orientation — the enrolled student is onboarded into the Student Portal and introduced to the Academic Handbook and Student Policies Handbook.

**6.2** Every stage shall show the applicant their current stage and what is required of them next; the journey shall never leave an applicant uncertain of their own status.

## 7.0 Fee and Pricing Presentation Policy

**7.1** The public website and Admissions Portal shall present program fees clearly and professionally, without a public statement explaining that different applicants may be charged different amounts for the same program.

**7.2** The system shall be capable of applying location-specific pricing adjustments, scholarships, discounts, and waivers automatically, under policy the Board of Trustees approves, without requiring the applicant to understand or navigate the underlying mechanism.

**7.3** No public digital surface shall commit the University to a specific tuition figure as a guaranteed, binding rate beyond the current admissions cycle; published figures shall be reviewed and, where changed, updated for each new cycle, consistent with the Board-discretion principle already established for compensation in the Compensation, Honoraria, Stipends, Allowances & Revenue Participation Policy (OPS-010, Section 6.3).

**7.4** Any scholarship, discount, or waiver applied to an individual applicant shall be recorded in the Finance Portal's system of record; the public digital surface itself need not, and shall not, disclose the internal criteria by which regional or individual adjustments are calculated.

## 8.0 Enforcement

**8.1** Any digital surface publicly disclosing the internal mechanics of location-specific pricing, or presenting a fee as a permanently guaranteed figure, is subject to correction by the Office of Communications under Section 7.0.

## 9.0 Related Documents

**9.1** Public Website Editorial & Information Architecture Standard (DXB-001); Compensation, Honoraria, Stipends, Allowances & Revenue Participation Policy (OPS-010); Constitution Articles V, VIII, and IX.

## 10.0 Effective Date

**10.1** This Policy is effective as of the date shown in the Document Control block above.
'''

def main():
    out = []
    for (num, code, title, steward, owner, authority, thesis, sections) in POLICIES:
        out.append(divider(num, code, title, steward, thesis, sections))
        out.append(f"## {code}: {title} {{.unnumbered}}\n")
        out.append(header_block(code, VERSION_EFFECTIVE_REVIEW[0], VERSION_EFFECTIVE_REVIEW[1],
                                 VERSION_EFFECTIVE_REVIEW[2], APPROVAL[num], steward, owner, authority))
        out.append("")
        out.append(CONTENT[num].strip())
        out.append("")
        out.append(f"*End of {'AMIU-' + code}*")
        out.append("")
        out.append(PAGEBREAK)
    text = "\n\n".join(out)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote {OUT} ({len(text)} chars)")

if __name__ == "__main__":
    main()
