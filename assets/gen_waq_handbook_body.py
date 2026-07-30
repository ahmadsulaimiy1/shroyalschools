#!/usr/bin/env python3
"""Author work_waq_handbook_body.md — the 9-policy body of the AMIU Waqf &
Research Handbook (Doc Codes WAQ-001 through WAQ-009), the ninth and final
AMIU flagship publication, in the same navy/gold editorial system as the
Blueprint, Constitution, Institutional Governance Compendium, Academic
Handbook, Student Policies Handbook, Operations Handbook, Legal &
Compliance Handbook, and Marketing & Communications Handbook. This is the
last of the seven policy sections the user supplied — together with the
prior six, it completes all 107 documents of the Institutional Governance
Compendium's original source registry (see igc_data.py's
ORIGINAL_SOURCE_COUNT).

Source: the 9 fully-drafted WAQ policies supplied by the user, transcribed
here with the fixes found during the editorial review applied directly
(not just noted) — see the Publication Certification Statement in
assets/waq_handbook_back.md for what each fix was and why:

  1. Authority citations. Unlike the Operations, Legal & Compliance, and
     Marketing & Communications Handbooks, most of this section's
     Authority citations already named the CORRECT Article — this
     section's fix is precision, not correction. The three Waqf-specific
     policies (Board Charter, Donor Stewardship, Fundraising Campaign)
     cited a bare "Article 11" (Waqf and Endowment); Article 11, Section
     11.1 (Waqf Board) is the exact provision establishing the Board "of
     not fewer than five members" the Charter itself describes, so all
     three are corrected to cite that section specifically. The three
     research policies (Research Policy, Publication & Conference Policy,
     Research Ethics Policy) cited a bare "Article 8" (University Senate);
     Section 8.7 (Responsibilities) is the subsection granting the Senate
     authority over academic standards, faculty quality, and degrees, so
     all three are corrected to cite it specifically. The three
     institutional-risk policies (Risk Register, Crisis Management,
     Business Continuity & Insurance) cited a bare "Article 15"
     (Transparency and Accountability) — a real Article, but one whose
     four subsections (Annual Report, Audit, Conflict of Interest,
     Whistleblower) do not actually address risk management. All three
     are stewarded by the Chair, Audit & Risk Committee, a Board
     committee, so all three are corrected to Article 6, Section 6.9
     (Committees) — the provision that actually establishes Board
     committees and their reporting obligation.

  2. Approval Authority assigned to the University Senate for two
     policies with no academic content: Crisis Management Policy (whose
     own Crisis Management Team is chaired by the President and staffed
     by Administration, Communications, Legal, and Facilities — no
     academic role at all) and Business Continuity & Insurance Policy
     (stewarded by the Deputy Vice-Chancellor, Administration & Finance,
     and owned by the Office of Finance). Both are reassigned to the
     Board of Trustees, matching their sibling Risk Register (WAQ-007),
     which was already correctly Board-approved — all three institutional-
     risk policies now share one approval authority, consistent with their
     shared stewardship under the Audit & Risk Committee.

  3. WAQ-006's Related Documents cited itself ("Research Ethics Policy
     (WAQ-006)") as a related document to the Research Ethics Policy —
     a self-reference that cannot be correct. Corrected to the
     Publication & Conference Policy (WAQ-005), completing the natural
     three-way cross-reference between the Research Policy, Publication &
     Conference Policy, and Research Ethics Policy that the other two
     policies already have.

  4. WAQ-008's Crisis Management Team roster named "The Director, Legal
     Counsel" — the same phantom title already found and corrected in the
     Marketing & Communications Handbook's Crisis Communications Plan
     (MKT-006). Every Legal & Compliance Handbook policy refers to that
     office as "the Office of Legal Counsel," matching its steward name
     in the Institutional Governance Compendium's registry. Corrected for
     consistency.

Formatting is normalized to house style (numbered outline points become
bold-numbered paragraphs, ALL-CAPS section headers become sentence case,
the donor-tier plain-text table in WAQ-002 becomes a proper markdown
table) but no provision, clause, or numbered point from the source is
cut, shortened, or merged away.
"""

OUT = "/home/user/shroyalschools/work_waq_handbook_body.md"

# ---------------------------------------------------------------------------
# Divider generator (mirrors gen_mkt_handbook_body.py's divider() pattern)
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
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:color w:val="8C97AB"/><w:sz w:val="19"/><w:spacing w:val="14"/></w:rPr><w:t>Waqf &amp; Research Handbook &#183; Policy {num} of 9</w:t></w:r></w:p>''')
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
# docstring above for what each replaced and why. Note WAQ-007's Review
# Date is "Quarterly", not "Annual" — carried over from the source as-is.
# ---------------------------------------------------------------------------
POLICIES = [
 (1, "WAQ-001", "Waqf & Endowment Board Charter", "Chair, Waqf & Endowment Board", "Secretary, Waqf & Endowment Board",
  "Constitution Article 11, Section 11.1",
  "Five Board members, no fewer, each a practicing Muslim with real expertise — halal investments only, and no deviation from a donor's intent.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Composition"),("6.0","Qualifications"),("7.0","Responsibilities"),
   ("8.0","Meetings"),("9.0","Reporting"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (2, "WAQ-002", "Donor Stewardship Plan", "Chair, Waqf & Endowment Board", "Office of Waqf & Philanthropy",
  "Constitution Article 11, Section 11.1",
  "Eight recognition tiers, quarterly contact for major donors, and an annual impact report for every giver.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Donor Tiers"),("6.0","Stewardship Activities"),("7.0","Donor Communication"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (3, "WAQ-003", "Fundraising Campaign Plan", "Chair, Waqf & Endowment Board", "Office of Waqf & Philanthropy",
  "Constitution Article 11, Section 11.1",
  "Five campaign types, an ethical solicitation standard, and a budget that answers for every dollar it spends to raise a dollar.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Campaign Types"),("6.0","Campaign Planning"),("7.0","Donor Solicitation"),
   ("8.0","Campaign Evaluation"),("9.0","Enforcement"),
   ("10.0","Related Documents"),("11.0","Effective Date")]),
 (4, "WAQ-004", "Research Policy", "Deputy Vice-Chancellor, Academic Affairs", "Office of Research",
  "Constitution Article 8, Section 8.7",
  "One peer-reviewed contribution a year, grounded in Islamic principles, with zero tolerance for fabrication, falsification, or plagiarism.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Research Expectations"),("6.0","Research Support"),("7.0","Research Misconduct"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (5, "WAQ-005", "Publication & Conference Policy", "Deputy Vice-Chancellor, Academic Affairs", "Office of Research",
  "Constitution Article 8, Section 8.7",
  "At least one peer-reviewed article a year, conference funding to back it, and no name on a paper without real contribution.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Publication Expectations"),("6.0","Conference Participation"),("7.0","Support"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (6, "WAQ-006", "Research Ethics Policy", "Deputy Vice-Chancellor, Academic Affairs", "Office of Research",
  "Constitution Article 8, Section 8.7",
  "No human subject without informed consent, no study without IRB approval, no animal harmed beyond what the research requires.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Human Subjects"),("6.0","Animal Research"),("7.0","Data Management"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (7, "WAQ-007", "Risk Register", "Chair, Audit & Risk Committee", "Office of Internal Audit",
  "Constitution Article 6, Section 6.9",
  "Six risk categories, scored as likelihood times impact, reviewed by the Board every quarter without exception.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Risk Categories"),("6.0","Risk Assessment"),("7.0","Risk Register Contents"),
   ("8.0","Risk Scenarios"),("9.0","Reporting"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (8, "WAQ-008", "Crisis Management Policy", "Chair, Audit & Risk Committee", "Office of Internal Audit",
  "Constitution Article 6, Section 6.9",
  "One Crisis Management Team, one chain of command, and a standing rule that no person acts alone during a crisis.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Crisis Types"),("6.0","Crisis Management Team"),("7.0","Crisis Response"),
   ("8.0","Crisis Scenarios"),("9.0","Enforcement"),
   ("10.0","Related Documents"),("11.0","Effective Date")]),
 (9, "WAQ-009", "Business Continuity & Insurance Policy", "Deputy Vice-Chancellor, Administration & Finance", "Office of Finance",
  "Constitution Article 6, Section 6.9",
  "Four critical functions kept running through any disruption, and four lines of insurance that never lapse.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Business Continuity"),("6.0","Insurance"),("7.0","Scenarios"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
]

APPROVAL = {
 1: "Board of Trustees",
 2: "Waqf & Endowment Board",
 3: "Waqf & Endowment Board",
 4: "University Senate",
 5: "Deputy Vice-Chancellor, Academic Affairs",
 6: "University Senate",
 7: "Board of Trustees",
 8: "Board of Trustees",
 9: "Board of Trustees",
}

VERSION_EFFECTIVE_REVIEW = ("1.0", "1 January 2028", "Annual")
REVIEW_OVERRIDE = {7: "Quarterly"}

CONTENT = {}

CONTENT[1] = '''
## 1.0 Purpose

**1.1** The purpose of this Charter is to establish the definitive, binding, and comprehensive framework for the governance, management, and oversight of the University's Waqf and endowment funds.

**1.2** This Charter serves as the binding institutional rule for all Waqf-related matters and ensures:

**1.2.1** That all Waqf funds are managed in accordance with Islamic principles;

**1.2.2** That no person misuses or misappropriates Waqf funds;

**1.2.3** That Waqf funds are used exclusively for charitable and educational purposes;

**1.2.4** That donors' intentions are honored and respected;

**1.2.5** That the Waqf & Endowment Board exercises proper fiduciary oversight;

**1.2.6** That all Waqf activities comply with applicable laws and regulations.

## 2.0 Scope

**2.1** This Charter applies to:

**2.1.1** All Waqf and endowment funds of the University;

**2.1.2** All members of the Waqf & Endowment Board;

**2.1.3** All personnel involved in managing Waqf funds;

**2.1.4** All donors and beneficiaries of Waqf funds.

**2.2 Jurisdictional Reach.** This Charter applies to all Waqf funds, regardless of location, donor origin, or beneficiary location.

**2.3** No person is exempt from the requirements of this Charter.

## 3.0 Definitions

**3.1 Waqf.** An Islamic charitable endowment established for educational, religious, or humanitarian purposes.

**3.2 Endowment.** Funds established for the long-term support of the University.

**3.3 Waqf & Endowment Board.** The Board responsible for overseeing Waqf and endowment funds.

**3.4 Donor.** A person or entity that contributes to the Waqf.

**3.5 Beneficiary.** The person or entity that benefits from the Waqf.

**3.6 Waqf Fund.** The principal and income of the Waqf.

**3.7 Fiduciary Duty.** The legal obligation to act in the best interests of the Waqf.

**3.8 Sadaqah Jariyah.** Continuous charity that benefits others beyond the donor's lifetime.

## 4.0 Policy Statement

**4.1** The Waqf & Endowment Board shall operate in accordance with this Charter.

**4.2** No person shall misuse or misappropriate Waqf funds.

**4.3** No person shall use Waqf funds for unauthorized purposes.

**4.4** All Waqf funds shall be managed in accordance with Islamic principles.

**4.5** No person shall engage in riba (interest), gharar (excessive uncertainty), or haram (prohibited) activities.

**4.6** Donors' intentions shall be honored and respected.

**4.7** No person shall deviate from donor instructions.

## 5.0 Composition

**5.1** The Waqf & Endowment Board shall consist of not fewer than five members.

**5.2** Members shall be appointed by the Board of Trustees.

**5.3** Members shall have expertise in:

**5.3.1** Islamic finance;

**5.3.2** Investment management;

**5.3.3** Legal and compliance;

**5.3.4** Philanthropy and fundraising.

**5.4** The Chairperson shall be appointed by the Board of Trustees.

**5.5** No person shall serve on the Board without proper qualifications.

## 6.0 Qualifications

**6.1** Board members must:

**6.1.1** Be practicing Muslims;

**6.1.2** Have expertise in at least one relevant area;

**6.1.3** Be of high moral character and integrity;

**6.1.4** Have no conflict of interest;

**6.1.5** Be committed to the University's Islamic mission.

**6.2** No person shall be appointed without meeting qualifications.

## 7.0 Responsibilities

**7.1 Governance**

**7.1.1** The Board shall:

**7.1.1.1** Oversee the management of Waqf funds;

**7.1.1.2** Ensure compliance with Islamic principles;

**7.1.1.3** Approve investment policies;

**7.1.1.4** Approve distributions;

**7.1.1.5** Report to the Board of Trustees.

**7.1.2** No person shall make unauthorized decisions.

**7.2 Investment Management**

**7.2.1** The Board shall ensure that Waqf funds are invested in:

**7.2.1.1** Halal (permissible) investments;

**7.2.1.2** Low-risk instruments;

**7.2.1.3** Ethical investments.

**7.2.2** No person shall invest in haram investments.

**7.3 Distribution**

**7.3.1** Waqf funds shall be distributed for:

**7.3.1.1** Scholarships;

**7.3.1.2** Support for schools and mosques;

**7.3.1.3** Support for widows and orphans;

**7.3.1.4** The Nigeria Mega-University Initiative;

**7.3.1.5** Other charitable purposes.

**7.3.2** No person shall distribute funds without authorization.

**7.4 Donor Stewardship**

**7.4.1** The Board shall ensure:

**7.4.1.1** Donor intentions are honored;

**7.4.1.2** Donors are recognized appropriately;

**7.4.1.3** Donors are informed of impact.

**7.4.2** No person shall ignore donor instructions.

## 8.0 Meetings

**8.1** The Board shall meet at least quarterly.

**8.2** Special meetings may be called by the Chairperson.

**8.3** A quorum shall consist of three members.

**8.4** Minutes shall be maintained and submitted to the Board of Trustees.

## 9.0 Reporting

**9.1** The Board shall submit annual reports to the Board of Trustees.

**9.2** Reports shall include:

**9.2.1** Financial statements;

**9.2.2** Investment performance;

**9.2.3** Distribution summary;

**9.2.4** Donor acknowledgment.

## 10.0 Enforcement

**10.1** No person shall violate any provision of this Charter.

**10.2** Violation of this Charter shall result in disciplinary action.

**10.3** The Chairperson shall ensure compliance.

## 11.0 Related Documents

**11.1** Constitution Article 11 (Waqf and Endowment)

**11.2** Donor Stewardship Plan (WAQ-002)

**11.3** Fundraising Campaign Plan (WAQ-003)

## 12.0 Effective Date

**12.1** This Charter is effective as of 1 January 2028.
'''

CONTENT[2] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for cultivating, recognizing, and engaging donors to the University.

**1.2** This Policy ensures:

**1.2.1** Donors are cultivated and engaged effectively;

**1.2.2** Donors are recognized appropriately;

**1.2.3** Donors are informed of the impact of their gifts;

**1.2.4** That no person misuses donor relationships;

**1.2.5** That donor trust is maintained and strengthened.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All donors to the University;

**2.1.2** All personnel involved in donor relations;

**2.1.3** All donor-related activities.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Donor.** A person or entity that contributes to the University.

**3.2 Stewardship.** The cultivation, recognition, and engagement of donors.

**3.3 Recognition.** Acknowledgment of donor contributions.

**3.4 Donor Tier.** A category of donor based on contribution level.

## 4.0 Policy Statement

**4.1** The University shall maintain a comprehensive Donor Stewardship Plan.

**4.2** No person shall misuse donor relationships.

**4.3** No person shall ignore donor instructions.

**4.4** Donors shall be recognized appropriately.

## 5.0 Donor Tiers

**5.1** Donor tiers shall be:

| Tier | Contribution | Recognition |
|---|---|---|
| Sponsor a Student (Tier 4) | $500 | Certificate of Appreciation |
| Sponsor a Diploma Seat | $250 | Certificate of Appreciation |
| Sponsor an Undergraduate Seat | $600 | Certificate of Appreciation |
| Sponsor a Graduate Seat | $900 | Certificate of Appreciation |
| Sponsor a Mosque Partnership | $2,500 | Plaque |
| Sponsor a Physical Islamic School | $5,000/year | Plaque |
| Named Endowed Scholarship | $25,000 | Named Scholarship |
| Nigeria Mega-University Founding Patron | $10,000 | Named Plaque |

**5.2** No person shall recognize donors improperly.

## 6.0 Stewardship Activities

**6.1 Cultivation**

**6.1.1** Cultivation shall include:

**6.1.1.1** Personal communication;

**6.1.1.2** Invitations to events;

**6.1.1.3** Impact reports;

**6.1.1.4** Regular updates.

**6.1.2** No person shall neglect donors.

**6.2 Recognition**

**6.2.1** Recognition shall include:

**6.2.1.1** Acknowledgment letters;

**6.2.1.2** Public recognition;

**6.2.1.3** Plaques and certificates;

**6.2.1.4** Named scholarships.

**6.2.2** No person shall fail to recognize donors.

**6.3 Communication**

**6.3.1** Communication shall include:

**6.3.1.1** Annual impact reports;

**6.3.1.2** Newsletters;

**6.3.1.3** Personal updates.

**6.3.2** No person shall fail to communicate with donors.

## 7.0 Donor Communication

**7.1 Frequency**

**7.1.1** Major donors shall be contacted at least quarterly.

**7.1.2** All donors shall receive annual impact reports.

**7.1.3** No person shall neglect donor communication.

**7.2 Content**

**7.2.1** Communications shall include:

**7.2.1.1** Impact of contributions;

**7.2.1.2** University updates;

**7.2.1.3** Upcoming initiatives.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Chair, Waqf & Endowment Board shall ensure compliance.

## 9.0 Related Documents

**9.1** Waqf & Endowment Board Charter (WAQ-001)

**9.2** Fundraising Campaign Plan (WAQ-003)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[3] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for fundraising strategies, campaigns, and targets.

**1.2** This Policy ensures:

**1.2.1** Effective fundraising to support the University's mission;

**1.2.2** Ethical and transparent fundraising practices;

**1.2.3** That no person engages in unethical fundraising;

**1.2.4** That fundraising targets are achieved.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All fundraising activities;

**2.1.2** All fundraising personnel;

**2.1.3** All fundraising communications.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Fundraising.** The process of soliciting and collecting donations.

**3.2 Campaign.** A coordinated fundraising effort.

**3.3 Target.** The fundraising goal.

**3.4 Donor.** A person or entity that contributes.

## 4.0 Policy Statement

**4.1** The University shall maintain a comprehensive Fundraising Campaign Plan.

**4.2** No person shall engage in unethical fundraising.

**4.3** No person shall make false or misleading representations.

**4.4** All fundraising shall be transparent and accountable.

## 5.0 Campaign Types

**5.1** Campaigns shall include:

**5.1.1** Annual giving campaigns;

**5.1.2** Capital campaigns;

**5.1.3** Endowment campaigns;

**5.1.4** Waqf campaigns;

**5.1.5** Emergency campaigns.

**5.2** No person shall conduct unauthorized campaigns.

## 6.0 Campaign Planning

**6.1 Objectives**

**6.1.1** Campaign objectives shall include:

**6.1.1.1** Fundraising targets;

**6.1.1.2** Donor acquisition;

**6.1.1.3** Donor retention;

**6.1.1.4** Brand awareness.

**6.2 Strategy**

**6.2.1** Strategies shall include:

**6.2.1.1** Donor segmentation;

**6.2.1.2** Communication channels;

**6.2.1.3** Solicitation methods;

**6.2.1.4** Recognition plans.

**6.3 Budget**

**6.3.1** Fundraising budgets shall include:

**6.3.1.1** Staff costs;

**6.3.1.2** Materials;

**6.3.1.3** Events;

**6.3.1.4** Marketing.

**6.3.2** No person shall exceed the fundraising budget.

## 7.0 Donor Solicitation

**7.1 Methods**

**7.1.1** Solicitation methods shall include:

**7.1.1.1** Direct mail;

**7.1.1.2** Email;

**7.1.1.3** Events;

**7.1.1.4** Personal visits;

**7.1.1.5** Digital platforms.

**7.1.2** No person shall use unethical solicitation methods.

**7.2 Ethical Standards**

**7.2.1** Solicitation shall be:

**7.2.1.1** Honest and transparent;

**7.2.1.2** Respectful of donors;

**7.2.1.3** Consistent with Islamic values.

**7.2.2** No person shall engage in unethical solicitation.

## 8.0 Campaign Evaluation

**8.1** Campaigns shall be evaluated based on:

**8.1.1** Funds raised;

**8.1.2** Donor acquisition;

**8.1.3** Donor retention;

**8.1.4** Return on investment.

**8.2** No person shall fail to evaluate campaigns.

## 9.0 Enforcement

**9.1** No person shall violate any provision of this Policy.

**9.2** Violation of this Policy shall result in disciplinary action.

**9.3** The Chair, Waqf & Endowment Board shall ensure compliance.

## 10.0 Related Documents

**10.1** Donor Stewardship Plan (WAQ-002)

**10.2** Waqf & Endowment Board Charter (WAQ-001)

## 11.0 Effective Date

**11.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[4] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for research expectations, support resources, and integrity standards.

**1.2** This Policy ensures:

**1.2.1** That research is conducted to the highest standards;

**1.2.2** That no person engages in research misconduct;

**1.2.3** That research aligns with the University's Islamic mission;

**1.2.4** That researchers receive appropriate support.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All faculty and researchers;

**2.1.2** All research activities;

**2.1.3** All research outputs.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Research.** Systematic investigation to establish facts or principles.

**3.2 Research Misconduct.** Fabrication, falsification, or plagiarism in research.

**3.3 Research Output.** Any product of research, including publications and presentations.

## 4.0 Policy Statement

**4.1** Research shall be conducted to the highest standards.

**4.2** No person shall engage in research misconduct.

**4.3** No person shall falsify or fabricate research data.

**4.4** All research shall be conducted ethically.

## 5.0 Research Expectations

**5.1 Faculty Expectations**

**5.1.1** Faculty are expected to:

**5.1.1.1** Conduct research;

**5.1.1.2** Publish in peer-reviewed journals;

**5.1.1.3** Present at conferences;

**5.1.1.4** Contribute to knowledge.

**5.1.2** No faculty member shall neglect research.

**5.2 Research Quality**

**5.2.1** Research shall:

**5.2.1.1** Be rigorous and systematic;

**5.2.1.2** Use appropriate methods;

**5.2.1.3** Be grounded in Islamic principles;

**5.2.1.4** Contribute to the Ummah.

**5.2.2** No person shall conduct substandard research.

## 6.0 Research Support

**6.1 Resources**

**6.1.1** The University shall provide:

**6.1.1.1** Research facilities;

**6.1.1.2** Library resources;

**6.1.1.3** Research funding;

**6.1.1.4** Administrative support.

**6.1.2** No researcher shall be denied support.

**6.2 Training**

**6.2.1** Training shall include:

**6.2.1.1** Research methods;

**6.2.1.2** Research ethics;

**6.2.1.3** Publication skills;

**6.2.1.4** Grant writing.

## 7.0 Research Misconduct

**7.1 Prohibited Conduct**

**7.1.1** Research misconduct includes:

**7.1.1.1 Fabrication.** Making up data;

**7.1.1.2 Falsification.** Manipulating data;

**7.1.1.3 Plagiarism.** Using others' work without attribution.

**7.1.2** No person shall engage in research misconduct.

**7.2 Investigation**

**7.2.1** Allegations of misconduct shall be investigated.

**7.2.2** The investigation shall be:

**7.2.2.1** Prompt;

**7.2.2.2** Fair;

**7.2.2.3** Confidential.

**7.2.3** No person shall interfere with investigations.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance.

## 9.0 Related Documents

**9.1** Publication & Conference Policy (WAQ-005)

**9.2** Research Ethics Policy (WAQ-006)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[5] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for publication expectations, conference participation, and support.

**1.2** This Policy ensures:

**1.2.1** That faculty publish and present their research;

**1.2.2** That no person engages in publication misconduct;

**1.2.3** That research is disseminated to the academic community;

**1.2.4** That faculty receive support for conferences.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All faculty and researchers;

**2.1.2** All publications;

**2.1.3** All conference participation.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Publication.** A scholarly work published in a peer-reviewed journal, book, or other venue.

**3.2 Conference.** An academic gathering for presenting research.

**3.3 Authorship.** The acknowledgment of contribution to a publication.

## 4.0 Policy Statement

**4.1** Faculty shall publish and present their research.

**4.2** No person shall engage in publication misconduct.

**4.3** No person shall claim authorship without contribution.

**4.4** All publications shall be ethically sound.

## 5.0 Publication Expectations

**5.1** Faculty are expected to publish:

**5.1.1** At least one peer-reviewed article per year;

**5.1.2** Other scholarly works as appropriate.

**5.2** No faculty member shall fail to publish.

## 6.0 Conference Participation

**6.1** Faculty are expected to:

**6.1.1** Present at conferences;

**6.1.2** Attend conferences;

**6.1.3** Network with peers.

**6.2** No faculty member shall neglect conferences.

## 7.0 Support

**7.1** The University shall provide:

**7.1.1** Conference funding;

**7.1.2** Publication support;

**7.1.3** Editing services.

**7.2** No faculty member shall be denied support.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance.

## 9.0 Related Documents

**9.1** Research Policy (WAQ-004)

**9.2** Research Ethics Policy (WAQ-006)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[6] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for ethical standards in research involving human subjects, animals, and data.

**1.2** This Policy ensures:

**1.2.1** That all research is conducted ethically;

**1.2.2** That no person engages in unethical research;

**1.2.3** That human subjects are protected;

**1.2.4** That research aligns with Islamic values.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All research activities;

**2.1.2** All researchers;

**2.1.3** All research involving human subjects, animals, or data.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Research Ethics.** The principles governing research conduct.

**3.2 Human Subjects.** Living individuals about whom researchers obtain data.

**3.3 Informed Consent.** Voluntary agreement to participate in research.

**3.4 IRB.** Institutional Review Board, which reviews research involving human subjects.

## 4.0 Policy Statement

**4.1** All research shall be conducted ethically.

**4.2** No person shall engage in unethical research.

**4.3** No person shall harm human subjects.

**4.4** All research shall respect human dignity.

## 5.0 Human Subjects

**5.1 Protection**

**5.1.1** Human subjects shall be protected from harm.

**5.1.2** Informed consent shall be obtained.

**5.1.3** Confidentiality shall be maintained.

**5.1.4** No person shall research without consent.

**5.2 IRB Review**

**5.2.1** Research involving human subjects shall be reviewed by the IRB.

**5.2.2** IRB approval shall be obtained before research.

**5.2.3** No person shall research without IRB approval.

## 6.0 Animal Research

**6.1** Animal research shall:

**6.1.1** Respect animal welfare;

**6.1.2** Minimize suffering;

**6.1.3** Follow ethical guidelines.

**6.2** No person shall harm animals unnecessarily.

## 7.0 Data Management

**7.1** Data shall be:

**7.1.1** Stored securely;

**7.1.2** Protected from unauthorized access;

**7.1.3** Retained as required.

**7.2** No person shall misuse data.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance.

## 9.0 Related Documents

**9.1** Research Policy (WAQ-004)

**9.2** Publication & Conference Policy (WAQ-005)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[7] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for identifying, assessing, and mitigating institutional risks.

**1.2** This Policy ensures:

**1.2.1** That all institutional risks are identified and managed;

**1.2.2** That no person ignores institutional risks;

**1.2.3** That the University maintains a robust risk management framework;

**1.2.4** That risks are reported to the Board of Trustees.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University;

**2.1.2** All operations and activities;

**2.1.3** All personnel.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Risk.** The potential for loss or harm.

**3.2 Risk Register.** A comprehensive inventory of institutional risks.

**3.3 Risk Assessment.** The process of identifying and evaluating risks.

**3.4 Risk Mitigation.** Actions to reduce risks.

## 4.0 Policy Statement

**4.1** The University shall maintain a comprehensive Risk Register.

**4.2** No person shall ignore institutional risks.

**4.3** No person shall fail to report risks.

**4.4** Risks shall be reviewed quarterly.

## 5.0 Risk Categories

**5.1** Risks shall include:

**5.1.1** Financial risks;

**5.1.2** Operational risks;

**5.1.3** Reputational risks;

**5.1.4** Compliance risks;

**5.1.5** Strategic risks;

**5.1.6** Cybersecurity risks.

## 6.0 Risk Assessment

**6.1 Likelihood**

**6.1.1** Likelihood shall be rated:

**6.1.1.1 Low.** Unlikely to occur;

**6.1.1.2 Medium.** May occur;

**6.1.1.3 High.** Likely to occur.

**6.2 Impact**

**6.2.1** Impact shall be rated:

**6.2.1.1 Low.** Minor impact;

**6.2.1.2 Medium.** Significant impact;

**6.2.1.3 High.** Major impact.

**6.3 Risk Score**

**6.3.1** Risk score = Likelihood &#215; Impact.

**6.3.2** High scores require immediate attention.

## 7.0 Risk Register Contents

**7.1** The Risk Register shall include:

**7.1.1** Risk description;

**7.1.2** Likelihood;

**7.1.3** Impact;

**7.1.4** Risk score;

**7.1.5** Mitigation actions;

**7.1.6** Responsible party;

**7.1.7** Status.

## 8.0 Risk Scenarios

**8.1 Scenario A: Financial Risk**

**8.1.1** When financial risks are identified:

**8.1.1.1** Assess the risk;

**8.1.1.2** Develop mitigation;

**8.1.1.3** Monitor regularly.

**8.1.2** No person shall ignore financial risks.

**8.2 Scenario B: Cybersecurity Risk**

**8.2.1** When cybersecurity risks are identified:

**8.2.1.1** Assess the risk;

**8.2.1.2** Implement security measures;

**8.2.1.3** Monitor threats.

**8.2.2** No person shall ignore cybersecurity risks.

## 9.0 Reporting

**9.1** The Risk Register shall be reviewed quarterly.

**9.2** Reports shall be submitted to:

**9.2.1** The Audit & Risk Committee;

**9.2.2** The Board of Trustees.

## 10.0 Enforcement

**10.1** No person shall violate any provision of this Policy.

**10.2** Violation of this Policy shall result in disciplinary action.

**10.3** The Chair, Audit & Risk Committee shall ensure compliance.

## 11.0 Related Documents

**11.1** Crisis Management Policy (WAQ-008)

**11.2** Business Continuity & Insurance Policy (WAQ-009)

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[8] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for managing institutional crises.

**1.2** This Policy ensures:

**1.2.1** Effective crisis management;

**1.2.2** Protection of the University community;

**1.2.3** Business continuity;

**1.2.4** That no person fails to respond to crises.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University;

**2.1.2** All crisis situations;

**2.1.3** All personnel.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Crisis.** An event threatening the University's operations, reputation, or stakeholders.

**3.2 Crisis Management Team.** The team responsible for managing crises.

**3.3 Crisis Response.** Actions taken during a crisis.

**3.4 Recovery.** Actions taken after a crisis.

## 4.0 Policy Statement

**4.1** The University shall maintain a comprehensive Crisis Management Policy.

**4.2** No person shall fail to respond to crises.

**4.3** No person shall make unauthorized decisions during crises.

**4.4** All crises shall be managed effectively.

## 5.0 Crisis Types

**5.1** Crises may include:

**5.1.1** Natural disasters;

**5.1.2** Health emergencies;

**5.1.3** Security incidents;

**5.1.4** Financial crises;

**5.1.5** Reputational crises;

**5.1.6** Legal crises.

## 6.0 Crisis Management Team

**6.1** The Crisis Management Team shall consist of:

**6.1.1** The President & Vice-Chancellor;

**6.1.2** The Deputy Vice-Chancellor, Administration & Finance;

**6.1.3** The Director, Communications;

**6.1.4** The Office of Legal Counsel;

**6.1.5** The Director, Facilities;

**6.1.6** Other relevant personnel.

**6.2** No person shall act independently.

## 7.0 Crisis Response

**7.1 Initial Response**

**7.1.1** Acknowledge the crisis immediately.

**7.1.2** Activate the Crisis Management Team.

**7.1.3** Assess the situation.

**7.1.4** No person shall delay response.

**7.2 Ongoing Response**

**7.2.1** Communicate with stakeholders.

**7.2.2** Coordinate actions.

**7.2.3** Monitor the situation.

**7.2.4** No person shall fail to communicate.

**7.3 Post-Crisis**

**7.3.1** Assess the response.

**7.3.2** Communicate lessons learned.

**7.3.3** Update plans.

**7.3.4** No person shall fail to learn.

## 8.0 Crisis Scenarios

**8.1 Scenario A: Natural Disaster**

**8.1.1** When a natural disaster occurs:

**8.1.1.1** Ensure safety of personnel;

**8.1.1.2** Activate emergency procedures;

**8.1.1.3** Communicate with stakeholders.

**8.1.2** No person shall ignore safety.

**8.2 Scenario B: Cybersecurity Incident**

**8.2.1** When a cybersecurity incident occurs:

**8.2.1.1** Contain the incident;

**8.2.1.2** Notify affected parties;

**8.2.1.3** Investigate the cause.

**8.2.2** No person shall ignore cybersecurity.

## 9.0 Enforcement

**9.1** No person shall violate any provision of this Policy.

**9.2** Violation of this Policy shall result in disciplinary action.

**9.3** The Chair, Audit & Risk Committee shall ensure compliance.

## 10.0 Related Documents

**10.1** Risk Register (WAQ-007)

**10.2** Crisis Communications Plan (MKT-006)

**10.3** Business Continuity & Insurance Policy (WAQ-009)

## 11.0 Effective Date

**11.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[9] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for business continuity and insurance requirements.

**1.2** This Policy ensures:

**1.2.1** Business continuity during disruptions;

**1.2.2** Adequate insurance coverage;

**1.2.3** Protection of University assets;

**1.2.4** That no person fails to maintain business continuity.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University;

**2.1.2** All operations;

**2.1.3** All personnel.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Business Continuity.** The ability to continue operations during disruptions.

**3.2 Critical Function.** A function essential to University operations.

**3.3 Insurance.** Coverage against losses.

## 4.0 Policy Statement

**4.1** The University shall maintain business continuity and adequate insurance.

**4.2** No person shall fail to maintain business continuity.

**4.3** No person shall fail to maintain insurance.

**4.4** All critical functions shall be protected.

## 5.0 Business Continuity

**5.1 Critical Functions**

**5.1.1** Critical functions shall include:

**5.1.1.1** Academic operations;

**5.1.1.2** Financial operations;

**5.1.1.3** IT operations;

**5.1.1.4** Student services.

**5.1.2** No person shall neglect critical functions.

**5.2 Continuity Plan**

**5.2.1** The Continuity Plan shall include:

**5.2.1.1** Critical functions identification;

**5.2.1.2** Alternative arrangements;

**5.2.1.3** Recovery procedures;

**5.2.1.4** Communication plans.

**5.2.2** No person shall fail to develop a continuity plan.

## 6.0 Insurance

**6.1 Coverage**

**6.1.1** Insurance shall include:

**6.1.1.1** General liability;

**6.1.1.2** Property insurance;

**6.1.1.3** Cyber insurance;

**6.1.1.4** Professional liability.

**6.1.2** No person shall fail to maintain insurance.

**6.2 Claims**

**6.2.1** Claims shall be reported promptly.

**6.2.2** Claims shall be documented.

**6.2.3** No person shall fail to report claims.

## 7.0 Scenarios

**7.1 Scenario A: Disruption**

**7.1.1** When operations are disrupted:

**7.1.1.1** Activate continuity plan;

**7.1.1.2** Communicate with stakeholders;

**7.1.1.3** Document actions.

**7.1.2** No person shall fail to respond.

**7.2 Scenario B: Insurance Claim**

**7.2.1** When an insurance claim is needed:

**7.2.1.1** Document the loss;

**7.2.1.2** Submit the claim;

**7.2.1.3** Follow up.

**7.2.2** No person shall fail to submit claims.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance.

## 9.0 Related Documents

**9.1** Risk Register (WAQ-007)

**9.2** Crisis Management Policy (WAQ-008)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

def main():
    out = []
    for (num, code, title, steward, owner, authority, thesis, sections) in POLICIES:
        out.append(divider(num, code, title, steward, thesis, sections))
        out.append(f"## {code}: {title} {{.unnumbered}}\n")
        review = REVIEW_OVERRIDE.get(num, VERSION_EFFECTIVE_REVIEW[2])
        out.append(header_block(code, VERSION_EFFECTIVE_REVIEW[0], VERSION_EFFECTIVE_REVIEW[1],
                                 review, APPROVAL[num], steward, owner, authority))
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
