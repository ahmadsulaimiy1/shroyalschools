#!/usr/bin/env python3
"""Author work_mkt_handbook_body.md — the 7-policy body of the AMIU
Marketing & Communications Handbook (Doc Codes MKT-001 through MKT-007),
the eighth AMIU flagship publication, in the same navy/gold editorial
system as the Blueprint, Constitution, Institutional Governance
Compendium, Academic Handbook, Student Policies Handbook, Operations
Handbook, and Legal & Compliance Handbook.

Source: the 7 fully-drafted MKT policies supplied by the user, transcribed
here with the fixes found during the editorial review applied directly
(not just noted) — see the Publication Certification Statement in
assets/mkt_handbook_back.md for what each fix was and why. The defects
found mirror the same systemic patterns already found and fixed in the
Operations and Legal & Compliance Handbooks:

  1. Authority citations. All seven policies cited "Constitution Article
     15, Section 15.1" (Transparency and Accountability — Annual
     Report/Audit/Conflict of Interest/Whistleblower), which does not
     address brand, web content, social media, media relations, crisis
     communications, or marketing in any way. No Article of the
     Constitution addresses marketing or communications specifically, so
     all seven are corrected to Article 9, Section 9.1 (Administration's
     general operational authority) — the same fallback already used in
     the Operations and Legal & Compliance Handbooks for policies with no
     more specific Article to cite.

  2. Approval Authority assigned to the Deputy Vice-Chancellor, Academic
     Affairs for five policies with no academic content (Brand Style
     Guide, Content Creation Policy, Social Media Policy, Media Relations
     Policy, Crisis Communications Plan, Marketing Plan) — the same
     bicameral non-interference conflict found and fixed across the
     Operations and Legal & Compliance Handbooks. Reassigned by scope:
     the two narrowest, routine content-workflow policies (Website
     Content Plan, Content Creation Policy) are approved by the Director,
     Communications directly — the same self-approval pattern already
     used for narrowly technical OPS policies stewarded by a single
     functional Director (e.g., Backup & Disaster Recovery, OPS-017). The
     institution-wide, reputationally- or financially-consequential
     policies (Brand Style Guide, Social Media Policy, Media Relations
     Policy, Crisis Communications Plan, Marketing Plan) are reassigned to
     the Deputy Vice-Chancellor, Administration & Finance — matching the
     approval authority already assigned to the Emergency Response Plan
     (OPS-022), the comparable institution-wide crisis-protocol document.

  3. MKT-006's Crisis Communications Team roster named "The Director,
     Legal Counsel" — a title that does not appear anywhere else in this
     project. Every Legal & Compliance Handbook policy stewarded by that
     office refers to it as "the Office of Legal Counsel" (an office, not
     a personal directorship), matching its steward name in the
     Institutional Governance Compendium's registry. Corrected for
     consistency.

All cross-references to other University documents (MKT-006's citation of
the Crisis Management Policy as WAQ-008, MKT-007's citations of the
Financial Model as OPS-001 and the Student Recruitment Plan as STU-003)
were checked against the Institutional Governance Compendium's Doc Code
registry and are correct as drafted — no phantom titles or wrong doc
codes were found in this section.

Formatting is normalized to house style (numbered outline points become
bold-numbered paragraphs, ALL-CAPS section headers become sentence case,
the two plain-text data tables in MKT-001 become proper markdown tables)
but no provision, clause, or numbered point from the source is cut,
shortened, or merged away.
"""

OUT = "/home/user/shroyalschools/work_mkt_handbook_body.md"

# ---------------------------------------------------------------------------
# Divider generator (mirrors gen_leg_handbook_body.py's divider() pattern)
# ---------------------------------------------------------------------------

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def title_size(title):
    n = len(title)
    if n <= 22:
        return 42
    if n <= 34:
        return 34
    if n <= 48:
        return 27
    return 22

def divider(num, code, title, steward, thesis, section_titles):
    tsize = title_size(title)
    rows = []
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="120"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:color w:val="8C97AB"/><w:sz w:val="19"/><w:spacing w:val="14"/></w:rPr><w:t>Marketing &amp; Communications Handbook &#183; Policy {num} of 7</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces Black" w:hAnsi="Fraunces Black"/><w:color w:val="B08625"/><w:b/><w:sz w:val="72"/></w:rPr><w:t>{code}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="120" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces Black" w:hAnsi="Fraunces Black"/><w:color w:val="FFFFFF"/><w:b/><w:sz w:val="{tsize*2}"/></w:rPr><w:t>{esc(title)}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="260"/><w:pBdr><w:bottom w:val="single" w:sz="10" w:space="8" w:color="B08625"/></w:pBdr></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:color w:val="8C97AB"/><w:sz w:val="19"/><w:spacing w:val="10"/></w:rPr><w:t>Policy Steward: {esc(steward)}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="360"/><w:ind w:right="700"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces" w:hAnsi="Fraunces"/><w:i/><w:color w:val="DCE3F0"/><w:sz w:val="24"/></w:rPr><w:t>&#8220;{esc(thesis)}&#8221;</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="140"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:b/><w:color w:val="B08625"/><w:sz w:val="18"/><w:spacing w:val="12"/></w:rPr><w:t>Contents of This Policy</w:t></w:r></w:p>''')
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
    lines.append(f"| **Policy Steward** | {steward} |")
    lines.append(f"| **Implementation Owner** | {owner} |")
    lines.append(f"| **Authority** | {authority} |")
    return "\n".join(lines)

PAGEBREAK = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'

# ---------------------------------------------------------------------------
# Policy metadata: (num, code, title, steward, owner, authority, thesis,
#  [(sec_num, sec_title), ...])
# Authority citations below are the CORRECTED versions — see the module
# docstring above for what each replaced and why.
# ---------------------------------------------------------------------------
POLICIES = [
 (1, "MKT-001", "Brand Style Guide", "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "One logo, three colors, two typefaces, and a brand voice that stays Islamic, warm, and professional across every channel.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Brand Identity"),("6.0","Brand Usage"),("7.0","Brand Protection"),
   ("8.0","Handling Brand Scenarios"),("9.0","Training Requirements"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (2, "MKT-002", "Website Content Plan", "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "Seven website sections, reviewed on a fixed schedule, so no page goes a year without a second look.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Website Structure"),("6.0","Content Governance"),("7.0","Accessibility"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (3, "MKT-003", "Content Creation Policy", "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "A plan before every piece, a review after every draft, and an approval tier that scales with the stakes.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Content Types"),("6.0","Creation Process"),
   ("7.0","Copyright and Intellectual Property"),("8.0","Enforcement"),
   ("9.0","Related Documents"),("10.0","Effective Date")]),
 (4, "MKT-004", "Social Media Policy", "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "Official accounts run by one office, personal accounts left to their owners, and a hard line against impersonation.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Official Accounts"),("6.0","Personal Accounts"),("7.0","Prohibited Conduct"),
   ("8.0","Crisis Communications"),("9.0","Enforcement"),
   ("10.0","Related Documents"),("11.0","Effective Date")]),
 (5, "MKT-005", "Media Relations Policy", "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "Every inquiry to one office, every press release through one approval chain, and one spokesperson during a crisis.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Media Inquiries"),("6.0","Press Releases"),("7.0","Crisis Media Management"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (6, "MKT-006", "Crisis Communications Plan", "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "A one-hour acknowledgment clock, a standing Crisis Communications Team, and a holding statement ready before it's needed.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Crisis Communications Team"),("6.0","Crisis Types"),
   ("7.0","Communications Protocols"),("8.0","Holding Statements"),
   ("9.0","Social Media During Crisis"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (7, "MKT-007", "Marketing Plan", "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "Five channels, five audiences, and a budget that never spends past what the Financial Model allocates.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Marketing Objectives"),("6.0","Target Audiences"),("7.0","Marketing Channels"),
   ("8.0","Budget"),("9.0","Performance Measurement"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
]

APPROVAL = {
 1: "Deputy Vice-Chancellor, Administration & Finance",
 2: "Director, Communications",
 3: "Director, Communications",
 4: "Deputy Vice-Chancellor, Administration & Finance",
 5: "Deputy Vice-Chancellor, Administration & Finance",
 6: "Deputy Vice-Chancellor, Administration & Finance",
 7: "Deputy Vice-Chancellor, Administration & Finance",
}

VERSION_EFFECTIVE_REVIEW = ("1.0", "1 January 2028", "Annual")

CONTENT = {}

CONTENT[1] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive visual identity, brand standards, and usage guidelines for Al-Mulk International University.

**1.2** This Policy serves as the binding institutional rule for all brand-related matters and ensures:

**1.2.1** Consistent and professional representation of the University across all platforms;

**1.2.2** That no person misuses the University's brand assets;

**1.2.3** That all communications reflect the University's Islamic identity and values;

**1.2.4** That the University's brand is protected and strengthened;

**1.2.5** That no person creates unauthorized brand variations.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University;

**2.1.2** All communications, including digital, print, and social media;

**2.1.3** All faculty, staff, and students;

**2.1.4** All third-party vendors creating materials for the University;

**2.1.5** All University departments and units.

**2.2 Jurisdictional Reach.** This Policy applies to all brand-related materials, regardless of medium, format, or location.

**2.3** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Brand.** The University's identity, including its name, logo, colors, typography, imagery, and voice.

**3.2 Logo.** The visual symbol representing the University.

**3.3 Brand Assets.** All elements of the University's brand, including logos, colors, fonts, and imagery.

**3.4 Brand Voice.** The tone and style of University communications.

**3.5 Brand Misuse.** Any unauthorized use or modification of brand assets.

**3.6 Visual Identity.** The visual elements that represent the University.

**3.7 Tagline.** The University's official tagline: "Knowledge Without Barriers."

## 4.0 Policy Statement

**4.1** The University shall maintain a comprehensive Brand Style Guide that defines all brand standards.

**4.2** No person shall misuse the University's brand assets.

**4.3** No person shall create unauthorized brand variations.

**4.4** No person shall use the University's brand for personal gain.

**4.5** All communications shall reflect the University's Islamic identity and values.

**4.6** The Brand Style Guide shall be reviewed annually.

## 5.0 Brand Identity

**5.1 Logo**

**5.1.1** The official logo of the University shall consist of:

**5.1.1.1** The University's name: "Al-Mulk International University";

**5.1.1.2** The acronym: "AMIU";

**5.1.1.3** The tagline: "Knowledge Without Barriers";

**5.1.1.4** The official seal or emblem.

**5.1.2** The logo shall be used in its entirety.

**5.1.3** No person shall:

**5.1.3.1** Alter the logo in any way;

**5.1.3.2** Stretch or distort the logo;

**5.1.3.3** Change the logo colors;

**5.1.3.4** Place the logo on cluttered backgrounds;

**5.1.3.5** Use unauthorized logo versions.

**5.1.4** The logo shall have clear space around it.

**5.1.5** The minimum size for the logo shall be:

**5.1.5.1** Print: 1 inch wide;

**5.1.5.2** Digital: 100 pixels wide.

**5.2 Color Palette**

**5.2.1** The University's primary colors are:

| Color Name | Hex Code | RGB Values | Usage |
|---|---|---|---|
| Royal Blue | #1A237E | (26, 35, 126) | Primary color for all materials |
| Gold | #FFD700 | (255, 215, 0) | Secondary color for accents |
| Red | #B71C1C | (183, 28, 28) | Accent color for urgency and calls to action |

**5.2.2** No person shall:

**5.2.2.1** Use colors outside the approved palette;

**5.2.2.2** Alter the approved colors;

**5.2.2.3** Use the colors in unauthorized ways.

**5.2.3** The color palette shall be used consistently in all materials.

**5.3 Typography**

**5.3.1** The University's approved fonts are:

| Usage | Font | Weight | Size |
|---|---|---|---|
| Headings | Georgia | Bold | 18-36pt |
| Subheadings | Georgia | Bold Italic | 14-18pt |
| Body Text | Times New Roman | Regular | 11-12pt |
| Captions | Times New Roman | Italic | 9-10pt |

**5.3.2** No person shall use unauthorized fonts.

**5.3.3** Font sizes shall be consistent across all materials.

**5.4 Imagery**

**5.4.1** Approved imagery shall include:

**5.4.1.1** Images of students and faculty;

**5.4.1.2** Images of Islamic architecture and calligraphy;

**5.4.1.3** Images of the University's brand elements.

**5.4.2** No person shall use images that:

**5.4.2.1** Are inconsistent with Islamic values;

**5.4.2.2** Are low quality or pixelated;

**5.4.2.3** Misrepresent the University.

**5.4.3** All images shall be high quality and professional.

**5.5 Brand Voice**

**5.5.1** The University's brand voice shall be:

**5.5.1.1** Professional and authoritative;

**5.5.1.2** Warm and welcoming;

**5.5.1.3** Islamic and values-driven;

**5.5.1.4** Clear and accessible.

**5.5.2** No person shall use language that:

**5.5.2.1** Is disrespectful or inappropriate;

**5.5.2.2** Is inconsistent with Islamic values;

**5.5.2.3** Misrepresents the University.

## 6.0 Brand Usage

**6.1 Official Communications**

**6.1.1** All official communications shall use the approved brand elements.

**6.1.2** Brand elements shall be used consistently.

**6.1.3** No person shall create unauthorized communications.

**6.2 Social Media**

**6.2.1** All official social media accounts shall use the approved brand elements.

**6.2.2** Profile pictures shall use the University logo.

**6.2.3** Cover images shall use approved imagery.

**6.2.4** No person shall create unauthorized social media accounts.

**6.3 Printed Materials**

**6.3.1** All printed materials shall use the approved brand elements.

**6.3.2** Materials shall be reviewed before printing.

**6.3.3** No person shall print unauthorized materials.

## 7.0 Brand Protection

**7.1 Trademark Protection**

**7.1.1** The University shall register its trademarks.

**7.1.2** Trademarks shall be protected from infringement.

**7.1.3** No person shall use the University's trademarks without authorization.

**7.2 Brand Misuse**

**7.2.1** Brand misuse shall be reported to the Office of Communications.

**7.2.2** Brand misuse shall be investigated.

**7.2.3** Corrective action shall be taken.

**7.2.4** No person shall misuse the University's brand.

## 8.0 Handling Brand Scenarios

**8.1 Scenario A: Logo Misuse**

**8.1.1** When a logo is misused:

**8.1.1.1** Notify the person responsible;

**8.1.1.2** Request correction;

**8.1.1.3** Escalate if necessary.

**8.1.2** No person shall ignore logo misuse.

**8.2 Scenario B: Unauthorized Brand Variation**

**8.2.1** When an unauthorized brand variation is discovered:

**8.2.1.1** Remove the variation;

**8.2.1.2** Investigate the source;

**8.2.1.3** Take corrective action.

**8.2.2** No person shall create unauthorized variations.

**8.3 Scenario C: Social Media Misrepresentation**

**8.3.1** When a social media account misrepresents the University:

**8.3.1.1** Report the account;

**8.3.1.2** Request removal;

**8.3.1.3** Notify the University community.

**8.3.2** No person shall create unauthorized accounts.

## 9.0 Training Requirements

**9.1** All personnel shall receive training on brand standards.

**9.2** Training shall include:

**9.2.1** Logo usage;

**9.2.2** Color palette;

**9.2.3** Typography;

**9.2.4** Brand voice.

**9.3** No person shall create materials without training.

## 10.0 Enforcement

**10.1** No person shall violate any provision of this Policy.

**10.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**10.3** The Director, Communications shall ensure compliance with this Policy.

## 11.0 Related Documents

**11.1** Website Content Plan (MKT-002)

**11.2** Social Media Policy (MKT-004)

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[2] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive structure, content, and governance standards for all University websites.

**1.2** This Policy ensures:

**1.2.1** Consistent and professional web presence;

**1.2.2** Accurate and up-to-date content;

**1.2.3** That no person publishes unauthorized content;

**1.2.4** That the University's brand and values are reflected online.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All University websites;

**2.1.2** All web content;

**2.1.3** All personnel managing web content.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Website.** Any web property owned or operated by the University.

**3.2 Web Content.** Any information published on University websites.

**3.3 Content Management System (CMS).** The platform used to manage web content.

## 4.0 Policy Statement

**4.1** The University shall maintain a comprehensive Website Content Plan.

**4.2** No person shall publish unauthorized content.

**4.3** No person shall publish inaccurate or misleading content.

**4.4** Content shall be reviewed and updated regularly.

## 5.0 Website Structure

**5.1 Home Page**

**5.1.1** The home page shall include:

**5.1.1.1** University name and logo;

**5.1.1.2** Mission and vision statements;

**5.1.1.3** Navigation to key sections;

**5.1.1.4** News and announcements;

**5.1.1.5** Call to action (Apply Now, Give, etc.).

**5.1.2** No person shall modify the home page without approval.

**5.2 Admissions**

**5.2.1** The admissions section shall include:

**5.2.1.1** Admission requirements;

**5.2.1.2** Application process;

**5.2.1.3** Deadlines;

**5.2.1.4** Tuition and fees;

**5.2.1.5** Scholarships.

**5.2.2** Content shall be accurate and up-to-date.

**5.3 Academic Programs**

**5.3.1** The academic programs section shall include:

**5.3.1.1** Program descriptions;

**5.3.1.2** Program requirements;

**5.3.1.3** Course listings;

**5.3.1.4** Faculty information.

**5.3.2** Content shall be reviewed annually.

**5.4 Tuition and Fees**

**5.4.1** The tuition section shall include:

**5.4.1.1** Tuition tiers;

**5.4.1.2** Fee schedules;

**5.4.1.3** Payment options;

**5.4.1.4** Refund policies.

**5.4.2** Content shall be updated annually.

**5.5 Scholarships**

**5.5.1** The scholarships section shall include:

**5.5.1.1** Waqf scholarship information;

**5.5.1.2** Application process;

**5.5.1.3** Eligibility criteria;

**5.5.1.4** Impact stories.

**5.5.2** Content shall be reviewed regularly.

**5.6 Student Portal**

**5.6.1** The student portal shall provide access to:

**5.6.1.1** Course materials;

**5.6.1.2** Grades;

**5.6.1.3** Financial information;

**5.6.1.4** Support services.

**5.6.2** No person shall deny access to the portal.

**5.7 News and Events**

**5.7.1** The news section shall include:

**5.7.1.1** University announcements;

**5.7.1.2** Events calendar;

**5.7.1.3** Student stories;

**5.7.1.4** Alumni news.

**5.7.2** Content shall be updated regularly.

## 6.0 Content Governance

**6.1 Content Creation**

**6.1.1** Content shall be created by authorized personnel.

**6.1.2** Content shall be reviewed before publication.

**6.1.3** No person shall publish unauthorized content.

**6.2 Content Review**

**6.2.1** Content shall be reviewed:

**6.2.1.1** Annually for accuracy;

**6.2.1.2** When regulations change;

**6.2.1.3** When programs change.

**6.2.2** No person shall fail to review content.

**6.3 Content Removal**

**6.3.1** Outdated content shall be removed.

**6.3.2** Inaccurate content shall be corrected.

**6.3.3** No person shall leave outdated content.

## 7.0 Accessibility

**7.1** All web content shall comply with:

**7.1.1** WCAG 2.1 standards;

**7.1.2** ADA requirements;

**7.1.3** Section 508 standards.

**7.2** No person shall create inaccessible content.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Director, Communications shall ensure compliance.

## 9.0 Related Documents

**9.1** Brand Style Guide (MKT-001)

**9.2** Content Creation Policy (MKT-003)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[3] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive content creation, review, approval, and distribution processes for all University communications.

**1.2** This Policy ensures:

**1.2.1** Consistent and high-quality content;

**1.2.2** Compliance with all applicable laws and regulations;

**1.2.3** That no person publishes unauthorized content;

**1.2.4** That content reflects the University's brand and values.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All content creators;

**2.1.2** All University communications;

**2.1.3** All platforms and media.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Content.** Any information created for University communications.

**3.2 Content Creator.** Any person creating content for the University.

**3.3 Review.** The process of checking content for accuracy and compliance.

**3.4 Approval.** Formal authorization to publish content.

## 4.0 Policy Statement

**4.1** All content shall be created in accordance with this policy.

**4.2** No person shall publish unauthorized content.

**4.3** No person shall publish inaccurate or misleading content.

**4.4** All content shall be reviewed before publication.

## 5.0 Content Types

**5.1** Content shall include:

**5.1.1** Website content;

**5.1.2** Social media posts;

**5.1.3** Press releases;

**5.1.4** Marketing materials;

**5.1.5** Newsletters;

**5.1.6** Videos;

**5.1.7** Publications.

**5.2** No person shall create unauthorized content types.

## 6.0 Creation Process

**6.1 Planning**

**6.1.1** Content shall be planned in advance.

**6.1.2** Plans shall include:

**6.1.2.1** Purpose;

**6.1.2.2** Audience;

**6.1.2.3** Format;

**6.1.2.4** Timeline.

**6.1.3** No person shall create content without a plan.

**6.2 Creation**

**6.2.1** Content shall be created in accordance with brand standards.

**6.2.2** Content shall be accurate and complete.

**6.2.3** Content shall be free of errors.

**6.2.4** No person shall create content with errors.

**6.3 Review**

**6.3.1** Content shall be reviewed by the appropriate authority.

**6.3.2** Review shall check:

**6.3.2.1** Accuracy;

**6.3.2.2** Completeness;

**6.3.2.3** Compliance;

**6.3.2.4** Brand alignment.

**6.3.3** No person shall skip review.

**6.4 Approval**

**6.4.1** Content shall be approved before publication.

**6.4.2** Approval authority:

**6.4.2.1** Routine content: Director, Communications;

**6.4.2.2** Sensitive content: DVC, Academic Affairs;

**6.4.2.3** Crisis content: President & Vice-Chancellor.

**6.4.3** No person shall publish without approval.

## 7.0 Copyright and Intellectual Property

**7.1** All content shall respect copyright laws.

**7.2** Content shall include appropriate attributions.

**7.3** No person shall use copyrighted material without permission.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Director, Communications shall ensure compliance.

## 9.0 Related Documents

**9.1** Brand Style Guide (MKT-001)

**9.2** Social Media Policy (MKT-004)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[4] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive social media use, management, and governance standards for Al-Mulk International University.

**1.2** This Policy ensures:

**1.2.1** Professional and consistent social media presence;

**1.2.2** Protection of the University's reputation;

**1.2.3** That no person misuses social media;

**1.2.4** That social media reflects the University's brand and values.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All official social media accounts;

**2.1.2** All employees;

**2.1.3** All students;

**2.1.4** All social media activities related to the University.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Social Media.** Online platforms for communication and content sharing.

**3.2 Official Account.** An account authorized by the University.

**3.3 Personal Account.** An account not authorized by the University.

**3.4 Social Media Misuse.** Inappropriate use of social media.

## 4.0 Policy Statement

**4.1** Social media shall be used responsibly and professionally.

**4.2** No person shall misuse social media.

**4.3** No person shall post inappropriate content.

**4.4** No person shall impersonate the University.

## 5.0 Official Accounts

**5.1 Account Management**

**5.1.1** Official accounts shall be managed by the Office of Communications.

**5.1.2** Account credentials shall be secure.

**5.1.3** No person shall create unauthorized accounts.

**5.2 Content Guidelines**

**5.2.1** Content shall:

**5.2.1.1** Reflect the University's brand;

**5.2.1.2** Be professional and respectful;

**5.2.1.3** Be accurate and current.

**5.2.2** No person shall post inappropriate content.

**5.3 Engagement**

**5.3.1** Engagement shall be:

**5.3.1.1** Prompt and professional;

**5.3.1.2** Respectful and courteous;

**5.3.1.3** Consistent with University values.

**5.3.2** No person shall engage in unprofessional communication.

## 6.0 Personal Accounts

**6.1** Employees and students are responsible for their personal accounts.

**6.2** Personal accounts shall not be used to represent the University.

**6.3** No person shall use personal accounts to impersonate the University.

## 7.0 Prohibited Conduct

**7.1** Social media shall not be used for:

**7.1.1** Harassment or bullying;

**7.1.2** Discrimination;

**7.1.3** Illegal activities;

**7.1.4** Sharing confidential information;

**7.1.5** Impersonation.

**7.2** No person shall engage in prohibited conduct.

## 8.0 Crisis Communications

**8.1** Crisis communications shall be handled by the Office of Communications.

**8.2** No person shall respond to crises without authorization.

**8.3** Crisis communications shall follow the Crisis Communications Plan (MKT-006).

## 9.0 Enforcement

**9.1** No person shall violate any provision of this Policy.

**9.2** Violation of this Policy shall result in disciplinary action.

**9.3** The Director, Communications shall ensure compliance.

## 10.0 Related Documents

**10.1** Brand Style Guide (MKT-001)

**10.2** Crisis Communications Plan (MKT-006)

## 11.0 Effective Date

**11.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[5] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive media relations standards, including handling inquiries, issuing press releases, and managing crisis media.

**1.2** This Policy ensures:

**1.2.1** Professional and consistent media relations;

**1.2.2** Protection of the University's reputation;

**1.2.3** That no person makes unauthorized media statements;

**1.2.4** Compliance with all applicable laws and regulations.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All media interactions;

**2.1.2** All employees;

**2.1.3** All students;

**2.1.4** All University communications.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Media.** All forms of mass communication, including print, broadcast, and digital.

**3.2 Spokesperson.** The authorized representative of the University.

**3.3 Press Release.** An official statement issued to the media.

**3.4 Media Crisis.** A situation requiring urgent media response.

## 4.0 Policy Statement

**4.1** Media relations shall be handled professionally and consistently.

**4.2** No person shall make unauthorized media statements.

**4.3** No person shall provide inaccurate information.

**4.4** All media inquiries shall be directed to the Office of Communications.

## 5.0 Media Inquiries

**5.1 Inquiry Handling**

**5.1.1** All media inquiries shall be directed to the Office of Communications.

**5.1.2** Inquiries shall be acknowledged within 24 hours.

**5.1.3** Responses shall be accurate and timely.

**5.1.4** No person shall respond to inquiries without authorization.

**5.2 Spokespersons**

**5.2.1** Authorized spokespersons shall include:

**5.2.1.1** The President & Vice-Chancellor;

**5.2.1.2** The Director, Communications;

**5.2.1.3** Designated subject matter experts.

**5.2.2** No person shall act as a spokesperson without authorization.

## 6.0 Press Releases

**6.1 Approval Process**

**6.1.1** Press releases shall be drafted by the Office of Communications.

**6.1.2** Press releases shall be reviewed and approved by:

**6.1.2.1** The Director, Communications;

**6.1.2.2** The DVC, Academic Affairs (for academic content);

**6.1.2.3** The President & Vice-Chancellor (for major announcements).

**6.1.3** No person shall issue a press release without approval.

**6.2 Content**

**6.2.1** Press releases shall be:

**6.2.1.1** Accurate and truthful;

**6.2.1.2** Clear and concise;

**6.2.1.3** Consistent with University values.

**6.2.2** No person shall issue inaccurate press releases.

## 7.0 Crisis Media Management

**7.1** Crisis media management shall follow the Crisis Communications Plan (MKT-006).

**7.2** No person shall respond to media during a crisis without authorization.

**7.3** The President & Vice-Chancellor shall be the primary spokesperson during a crisis.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Director, Communications shall ensure compliance.

## 9.0 Related Documents

**9.1** Crisis Communications Plan (MKT-006)

**9.2** Brand Style Guide (MKT-001)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[6] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive crisis communications protocols to protect the University's reputation during crises.

**1.2** This Policy ensures:

**1.2.1** Effective and consistent crisis communications;

**1.2.2** Protection of the University's reputation;

**1.2.3** That no person makes unauthorized statements;

**1.2.4** That stakeholders are informed promptly and accurately.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All University communications during crises;

**2.1.2** All employees;

**2.1.3** All students;

**2.1.4** All stakeholders.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Crisis.** An event that threatens the University's reputation, operations, or stakeholders.

**3.2 Crisis Communications.** Communications during a crisis.

**3.3 Crisis Communications Team.** The team responsible for crisis communications.

**3.4 Spokesperson.** The authorized representative of the University.

## 4.0 Policy Statement

**4.1** Crisis communications shall be managed in accordance with this plan.

**4.2** No person shall make unauthorized statements during a crisis.

**4.3** No person shall provide inaccurate information.

**4.4** All communications shall be consistent and coordinated.

## 5.0 Crisis Communications Team

**5.1** The Crisis Communications Team shall consist of:

**5.1.1** The President & Vice-Chancellor;

**5.1.2** The Director, Communications;

**5.1.3** The Office of Legal Counsel;

**5.1.4** Other relevant personnel.

**5.2** No person shall act independently during a crisis.

## 6.0 Crisis Types

**6.1** Crises may include:

**6.1.1** Natural disasters;

**6.1.2** Security incidents;

**6.1.3** Financial crises;

**6.1.4** Reputation crises;

**6.1.5** Health emergencies;

**6.1.6** Legal crises.

**6.2** No person shall fail to identify a crisis.

## 7.0 Communications Protocols

**7.1 Initial Response**

**7.1.1** Acknowledge the crisis within 1 hour.

**7.1.2** Provide initial information.

**7.1.3** Establish the facts.

**7.1.4** No person shall delay response.

**7.2 Ongoing Communications**

**7.2.1** Provide regular updates.

**7.2.2** Address stakeholder concerns.

**7.2.3** Correct misinformation.

**7.2.4** No person shall ignore misinformation.

**7.3 Post-Crisis Communications**

**7.3.1** Provide final updates.

**7.3.2** Communicate lessons learned.

**7.3.3** Rebuild trust.

**7.3.4** No person shall fail to communicate lessons.

## 8.0 Holding Statements

**8.1** Holding statements shall be prepared in advance.

**8.2** Holding statements shall include:

**8.2.1** Acknowledgment of the situation;

**8.2.2** Commitment to providing information;

**8.2.3** Contact information.

**8.3** No person shall issue unauthorized statements.

## 9.0 Social Media During Crisis

**9.1** Social media shall be monitored during a crisis.

**9.2** Social media shall be used to provide updates.

**9.3** No person shall post unauthorized content.

## 10.0 Enforcement

**10.1** No person shall violate any provision of this Policy.

**10.2** Violation of this Policy shall result in disciplinary action.

**10.3** The Director, Communications shall ensure compliance.

## 11.0 Related Documents

**11.1** Crisis Management Policy (WAQ-008)

**11.2** Media Relations Policy (MKT-005)

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[7] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive marketing strategies, channels, budgets, and performance metrics for Al-Mulk International University.

**1.2** This Policy ensures:

**1.2.1** Effective marketing and recruitment;

**1.2.2** Consistent brand representation;

**1.2.3** That no person engages in unethical marketing;

**1.2.4** That marketing efforts achieve institutional goals.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All marketing activities;

**2.1.2** All marketing personnel;

**2.1.3** All marketing materials.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Marketing.** The activities used to promote the University.

**3.2 Marketing Plan.** The strategic plan for marketing activities.

**3.3 Marketing Channel.** The medium used to reach the target audience.

**3.4 Performance Metric.** A measure of marketing effectiveness.

## 4.0 Policy Statement

**4.1** The University shall maintain a comprehensive Marketing Plan.

**4.2** No person shall engage in unethical marketing.

**4.3** No person shall make false or misleading claims.

**4.4** All marketing shall reflect the University's brand and values.

## 5.0 Marketing Objectives

**5.1** Marketing objectives shall include:

**5.1.1** Enrollment growth;

**5.1.2** Brand awareness;

**5.1.3** Student engagement;

**5.1.4** Reputation management.

**5.2** No person shall deviate from marketing objectives.

## 6.0 Target Audiences

**6.1** Target audiences shall include:

**6.1.1** Prospective students;

**6.1.2** Current students;

**6.1.3** Alumni;

**6.1.4** Donors;

**6.1.5** Partners.

**6.2** No person shall target unauthorized audiences.

## 7.0 Marketing Channels

**7.1** Marketing channels shall include:

**7.1.1** Digital marketing;

**7.1.2** Social media;

**7.1.3** Email marketing;

**7.1.4** Content marketing;

**7.1.5** Events;

**7.1.6** Public relations.

**7.2** No person shall use unauthorized channels.

## 8.0 Budget

**8.1** The marketing budget shall be allocated annually.

**8.2** Budget allocation shall follow the Financial Model (OPS-001).

**8.3** No person shall exceed the marketing budget.

## 9.0 Performance Measurement

**9.1** Marketing performance shall be measured by:

**9.1.1** Enrollment numbers;

**9.1.2** Website traffic;

**9.1.3** Social media engagement;

**9.1.4** Brand awareness metrics;

**9.1.5** Return on investment.

**9.2** No person shall fail to measure performance.

## 10.0 Enforcement

**10.1** No person shall violate any provision of this Policy.

**10.2** Violation of this Policy shall result in disciplinary action.

**10.3** The Director, Communications shall ensure compliance.

## 11.0 Related Documents

**11.1** Brand Style Guide (MKT-001)

**11.2** Student Recruitment Plan (STU-003)

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
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
