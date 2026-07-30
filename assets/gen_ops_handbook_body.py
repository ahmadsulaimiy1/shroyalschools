#!/usr/bin/env python3
"""Author work_ops_handbook_body.md — the 27-policy body of the AMIU
Operations Handbook (Doc Codes OPS-001 through OPS-027), the sixth AMIU
flagship publication, in the same navy/gold editorial system as the
Blueprint, Constitution, Institutional Governance Compendium, Academic
Handbook, and Student Policies Handbook.

Source: the 27 fully-drafted OPS policies supplied by the user, transcribed
here with the fixes found during the editorial review applied directly
(not just noted) — see the Publication Certification Statement in
assets/ops_handbook_back.md for what each fix was and why. The two
systemic defects were:

  1. Authority citations. Nearly every policy cited the wrong Constitution
     article: financial policies (Financial Model, Financial Operations
     Manual, Budgeting, Tuition, Payroll, Compensation) cited Article 11
     (Waqf and Endowment) instead of Article 14 (Financial Sustainability);
     general HR/administrative/IT/facilities policies cited either a bare
     "Article 13" (Faculty Rights and Responsibilities — a real Article,
     just the wrong one for policies that apply to ALL staff, not faculty)
     or "Article 15, Section 15.1" (Transparency and Accountability —
     Annual Report/Audit/Conflict of Interest/Whistleblower, unrelated to
     IT infrastructure or facilities) instead of Article 9 (Administration),
     Section 9.1 (the Administration's actual day-to-day operational
     authority). Data Privacy & Security is the one exception moved to a
     MORE specific citation than a generic Article 9 fallback: Article 17,
     Section 17.2 (Access to Records), which explicitly names FERPA and
     confidential-record protection. Two policies genuinely about faculty
     conduct (Online Pedagogy Training, Virtual Office Hours) keep or gain
     Article 13, Section 13.2 (Faculty Responsibilities) — the one case
     where that Article is the correct fit.

  2. Approval Authority assigned to the University Senate for policies with
     no academic content (Procurement, Payroll, Compensation, HR Policies
     Manual, Leave, Performance Review, Data Privacy, Acceptable Use,
     Health & Safety) — a direct conflict with the Constitution's own
     bicameral non-interference principle (Article 4.2: the Senate holds
     academic authority, the Board/Administration holds financial and
     operational authority). Reassigned to the Board of Trustees.

  3. OPS-002's banking-protocol signatory list named "the Chief Financial
     Officer" as a third authorized signer — a position that does not
     exist in the Constitution's Article 9.2 Administration roster (the
     University's financial authority is the Deputy Vice-Chancellor,
     Administration & Finance, already listed as a signatory in the same
     clause). Removed as the same phantom-title defect already corrected
     in the Institutional Governance Compendium.

  4. Restructured later, at the user's explicit direction: OPS-010's
     original Section 6.0 (Salary Structure) set rigid, mandatory dollar
     bands for every rank and role — e.g. "President & Vice-Chancellor:
     $100,000–$150,000" — with "No person shall set compensation outside
     the approved ranges." Two problems: this contradicts the
     Constitution's own Article 14, Section 14.3, which deliberately
     leaves compensation to Board discretion with no fixed figures; and
     it is financially impossible against the Strategic Implementation
     Blueprint's own Year-1 Payroll model (roughly $45,000 total across
     all payroll categories combined, per the 20%-of-gross-revenue
     Payroll allocation in the Financial Model, OPS-001) — a single
     mandatory executive salary floor would have exceeded the entire
     founding-decade payroll pool. Rewritten as a four-category personnel
     framework (Volunteer / Adjunct-Part-Time / Contract / Permanent
     Faculty, plus a parallel Senate Compensation Model distinguishing
     Volunteer, Contract, and Executive Senate Members), replacing every
     fixed salary band with Board-discretion language, and adding a
     discretionary Allowance Framework, an Awards and Recognition
     section, and a Revenue Participation Framework — all explicitly
     non-guaranteed and subject to annual Board review. This was the only
     place across all nine publications where a rigid, unfunded-liability
     compensation figure existed; the Constitution, the Payroll Policy
     (OPS-006, ratio-based), and the Blueprint's own honoraria modeling
     were already principle- or ratio-based and needed no change.

Formatting is normalized to house style (numbered outline points become
bold-numbered paragraphs, ALL-CAPS section headers become sentence case)
but no provision, clause, or numbered point from the source is cut,
shortened, or merged away.
"""

OUT = "/home/user/shroyalschools/work_ops_handbook_body.md"

# ---------------------------------------------------------------------------
# Divider generator (mirrors gen_stu_handbook_body.py's divider() pattern)
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
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:color w:val="8C97AB"/><w:sz w:val="19"/><w:spacing w:val="14"/></w:rPr><w:t>Operations Handbook &#183; Policy {num} of 27</w:t></w:r></w:p>''')
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
 (1, "OPS-001", "Financial Model", "Deputy Vice-Chancellor, Administration & Finance", "Office of Finance",
  "Constitution Article 14, Section 14.1",
  "A ten-year, zero-deficit financial framework in which every dollar of gross revenue has an approved home before it is spent.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Revenue Model"),("6.0","Expense Allocation"),("7.0","Reserve Management"),
   ("8.0","Zero-Deficit Operations"),("9.0","Handling Financial Scenarios"),
   ("10.0","Financial Reporting"),("11.0","Enforcement"),("12.0","Related Documents"),
   ("13.0","Effective Date")]),
 (2, "OPS-002", "Financial Operations Manual", "Deputy Vice-Chancellor, Administration & Finance", "Office of Finance",
  "Constitution Article 14, Section 14.1",
  "Accrual accounting, two signatures on every wire, and a monthly reconciliation that catches discrepancies before they become losses.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Accounting Policies"),("6.0","Banking Protocols"),("7.0","Accounts Payable"),
   ("8.0","Accounts Receivable"),("9.0","Financial Reporting"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (3, "OPS-003", "Budgeting Policy", "Deputy Vice-Chancellor, Administration & Finance", "Office of Finance",
  "Constitution Article 14, Section 14.1",
  "A six-month planning cycle, from department requests in August to Board approval in December, so no fiscal year starts without a budget.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Budget Process"),("6.0","Budget Monitoring"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (4, "OPS-004", "Procurement Policy", "Deputy Vice-Chancellor, Administration & Finance", "Office of Procurement",
  "Constitution Article 9, Section 9.1",
  "Three quotes above $1,000, formal bidding above $25,000, and no contract signed by anyone without proper authority.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Purchasing Methods"),("6.0","Vendor Selection"),("7.0","Contract Management"),
   ("8.0","Conflict of Interest"),("9.0","Enforcement"),("10.0","Related Documents"),
   ("11.0","Effective Date")]),
 (5, "OPS-005", "Tuition Collection & Refund Policy", "Deputy Vice-Chancellor, Administration & Finance", "Office of Finance",
  "Constitution Article 14, Section 14.2",
  "Five payment plans from full upfront to weekly, a published refund schedule, and hardship review before any student is turned away.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Billing"),("6.0","Payment Options"),("7.0","Refund Schedule"),
   ("8.0","Financial Hardship"),("9.0","Enforcement"),("10.0","Related Documents"),
   ("11.0","Effective Date")]),
 (6, "OPS-006", "Payroll Policy", "Deputy Vice-Chancellor, Administration & Finance", "Office of Human Resources",
  "Constitution Article 14, Section 14.3",
  "Monthly payroll, disbursed on the last working day, calculated against the Constitution's own fixed honoraria ratios.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Payroll Schedule"),("6.0","Compensation Administration"),("7.0","Record Keeping"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (7, "OPS-007", "HR Policies & Procedures Manual", "Deputy Vice-Chancellor, Administration & Finance", "Office of Human Resources",
  "Constitution Article 9, Section 9.1",
  "One comprehensive, annually reviewed reference for every employment matter the University's Administration governs.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Contents"),
   ("5.0","Enforcement"),("6.0","Related Documents"),("7.0","Effective Date")]),
 (8, "OPS-008", "Recruitment & Hiring Policy", "Director, Human Resources", "Office of Human Resources",
  "Constitution Article 9, Section 9.3",
  "Position authorization, a diverse candidate pool, and a background check completed before any offer becomes final.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Hiring Process"),
   ("5.0","Enforcement"),("6.0","Related Documents"),("7.0","Effective Date")]),
 (9, "OPS-009", "Employee Contract Template", "Director, Human Resources", "Office of Human Resources",
  "Constitution Article 9, Section 9.3",
  "One standard contract format for every employee category, so no one is employed on undocumented terms.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Contract Template"),("6.0","Contract Provisions"),("7.0","Contract Amendment"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (10, "OPS-010", "Compensation Policy", "Director, Human Resources", "Office of Human Resources",
  "Constitution Article 14, Section 14.3",
  "Four categories of service, Board-determined compensation within each, and a discretionary allowance and recognition framework that never becomes a fixed liability.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Personnel Categories"),("6.0","Compensation Principles"),("7.0","Allowance Framework"),
   ("8.0","Awards and Recognition"),("9.0","Revenue Participation Framework"),
   ("10.0","Market Benchmarking"),("11.0","Merit Increases"),("12.0","Enforcement"),
   ("13.0","Related Documents"),("14.0","Effective Date")]),
 (11, "OPS-011", "Leave Policy", "Director, Human Resources", "Office of Human Resources",
  "Constitution Article 9, Section 9.1",
  "Fifteen days of annual leave, ten of sick leave, and unpaid religious and parental leave that no employee is denied.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Leave Types"),("6.0","Leave Approval"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (12, "OPS-012", "Performance Review Policy", "Director, Human Resources", "Office of Human Resources",
  "Constitution Article 9, Section 9.1",
  "Self-assessment, supervisory evaluation, and an improvement plan before any performance issue becomes a termination.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Review Process"),("6.0","Enforcement"),("7.0","Related Documents"),
   ("8.0","Effective Date")]),
 (13, "OPS-013", "Termination Policy", "Director, Human Resources", "Office of Human Resources",
  "Constitution Article 9, Section 9.1",
  "Written notice, a right to appeal, and an exit interview for every employee who leaves, however the separation began.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Termination Types"),("6.0","Termination Process"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (14, "OPS-014", "IT Infrastructure Plan", "Director, Information Technology", "Office of Information Technology",
  "Constitution Article 9, Section 9.1",
  "A scalable, redundant, and secured technology architecture that grows with the University without ever being redesigned from zero.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Infrastructure Components"),("6.0","Security"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (15, "OPS-015", "LMS Technical Specifications", "Director, Information Technology", "Office of Information Technology",
  "Constitution Article 9, Section 9.1",
  "A single accessible platform, WCAG-compliant and available on any device, for every course the University delivers.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Technical Specifications"),("6.0","Accessibility"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (16, "OPS-016", "Data Privacy & Security Policy", "Director, Information Technology", "Office of Information Technology",
  "Constitution Article 17, Section 17.2",
  "Every record classified, every breach reported immediately, and no data disclosed outside the classification it was given.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Data Classification"),("6.0","Data Protection"),("7.0","Data Breach Response"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (17, "OPS-017", "Backup & Disaster Recovery Plan", "Director, Information Technology", "Office of Information Technology",
  "Constitution Article 9, Section 9.1",
  "Daily backups, a four-hour recovery objective, and an off-site copy of everything the University cannot afford to lose.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Backup Procedures"),("6.0","Recovery Objectives"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (18, "OPS-018", "IT Support Policy", "Director, Information Technology", "Office of Information Technology",
  "Constitution Article 9, Section 9.1",
  "A one-hour response to a critical outage, a published service-level table for everything else, and a clear escalation path.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Services"),("6.0","Service Levels"),("7.0","Escalation"),("8.0","Enforcement"),
   ("9.0","Related Documents"),("10.0","Effective Date")]),
 (19, "OPS-019", "Acceptable Use Policy", "Director, Information Technology", "Office of Information Technology",
  "Constitution Article 9, Section 9.1",
  "University technology serves academic work, research, and University business — never harassment, hacking, or personal gain.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Acceptable Use"),("6.0","Prohibited Use"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (20, "OPS-020", "Facilities Management Policy", "Director, Facilities", "Office of Facilities",
  "Constitution Article 9, Section 9.1",
  "Preventive, corrective, and emergency maintenance, and space allocated by need and function, never by informal claim.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Maintenance"),("6.0","Space Allocation"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (21, "OPS-021", "Health & Safety Policy", "Director, Facilities", "Office of Facilities",
  "Constitution Article 9, Section 9.1",
  "Fire safety, emergency evacuation, and first aid standards that protect every employee, student, and visitor without exception.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Safety Standards"),("6.0","Incident Reporting"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (22, "OPS-022", "Emergency Response Plan", "Director, Facilities", "Office of Facilities",
  "Constitution Article 9, Section 9.1",
  "A single response sequence — call, notify, evacuate, account for everyone — for fire, medical, and active-threat emergencies alike.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Emergency Types"),("6.0","Response Procedures"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (23, "OPS-023", "Learning Management System (LMS) Policy", "Director, Information Technology", "Office of Information Technology",
  "Constitution Article 9, Section 9.1",
  "Every course lives in one platform, with one role-based permission structure, so no instructor improvises delivery elsewhere.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Course Structure"),("6.0","User Roles"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (24, "OPS-024", "Online Pedagogy Training Policy", "Deputy Vice-Chancellor, Academic Affairs", "Office of Academic Affairs",
  "Constitution Article 13, Section 13.2",
  "No faculty member teaches online without first completing training in pedagogy, the LMS, and proctored assessment.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Training Requirements"),
   ("5.0","Ongoing Development"),("6.0","Evaluation"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (25, "OPS-025", "Virtual Office Hours Policy", "Deputy Vice-Chancellor, Academic Affairs", "College Deans",
  "Constitution Article 13, Section 13.2",
  "Two hours of virtual office hours a week, scheduled across time zones, with a 48-hour reply guarantee on every email.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Requirements"),
   ("5.0","Communication"),("6.0","Enforcement"),("7.0","Related Documents"),
   ("8.0","Effective Date")]),
 (26, "OPS-026", "Digital Resources & Library Policy", "University Librarian", "Library",
  "Constitution Article 9, Section 9.1",
  "A digital library open twenty-four hours a day, so distance from a campus is never distance from a book.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Resources"),
   ("5.0","Access"),("6.0","Research Support"),("7.0","Enforcement"),
   ("8.0","Effective Date")]),
 (27, "OPS-027", "Social Media & Student Communication Policy", "Director, Communications", "Office of Communications",
  "Constitution Article 9, Section 9.1",
  "Official channels for the University's voice, and a Digital Citizenship standard for every student who represents it online.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Official Social Media"),
   ("5.0","Student Use"),("6.0","Prohibited Use"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
]

APPROVAL = {
 1: "Board of Trustees", 2: "Deputy Vice-Chancellor, Administration & Finance",
 3: "Board of Trustees", 4: "Board of Trustees", 5: "Board of Trustees",
 6: "Board of Trustees", 7: "Board of Trustees",
 8: "Deputy Vice-Chancellor, Administration & Finance", 9: "Deputy Vice-Chancellor, Administration & Finance",
 10: "Board of Trustees", 11: "Board of Trustees", 12: "Board of Trustees", 13: "Board of Trustees",
 14: "Deputy Vice-Chancellor, Administration & Finance", 15: "Deputy Vice-Chancellor, Academic Affairs",
 16: "Board of Trustees", 17: "Director, Information Technology", 18: "Director, Information Technology",
 19: "Board of Trustees", 20: "Deputy Vice-Chancellor, Administration & Finance", 21: "Board of Trustees",
 22: "Deputy Vice-Chancellor, Administration & Finance", 23: "Deputy Vice-Chancellor, Academic Affairs",
 24: "University Senate", 25: "Deputy Vice-Chancellor, Academic Affairs",
 26: "Deputy Vice-Chancellor, Academic Affairs", 27: "Deputy Vice-Chancellor, Academic Affairs",
}

VERSION_EFFECTIVE_REVIEW = ("1.0", "1 January 2028", "Annual")

CONTENT = {}

CONTENT[1] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive financial framework for Al-Mulk International University, governing all aspects of its financial planning, revenue generation, expense allocation, reserve management, and fiscal sustainability.

**1.2** This Policy serves as the binding institutional rule for all financial matters and ensures:

**1.2.1** That the University maintains long-term financial sustainability and operational viability;

**1.2.2** That all financial decisions are made transparently, accountably, and in alignment with the University's mission and Islamic values;

**1.2.3** That no person makes unauthorized financial commitments or expenditures;

**1.2.4** That the University operates on a zero-deficit basis, with all revenue allocated to approved categories;

**1.2.5** That the University's financial practices comply with all applicable laws, regulations, and accreditation standards;

**1.2.6** That Waqf and endowment funds are managed in accordance with Islamic principles;

**1.2.7** That financial resources are allocated in accordance with strategic priorities and institutional goals.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University, including all academic and administrative units;

**2.1.2** All financial transactions, commitments, and expenditures;

**2.1.3** All revenue sources, including tuition, Waqf, grants, donations, and other income;

**2.1.4** All expense categories, including payroll, operations, technology, and reserves;

**2.1.5** All officers, faculty, staff, and any person authorized to make financial commitments on behalf of the University;

**2.1.6** All financial planning, budgeting, reporting, and auditing activities;

**2.1.7** All reserve and endowment funds, including the Liquidity Reserve and the Waqf Reserve.

**2.2 Jurisdictional Reach.** This Policy governs all financial activities, regardless of funding source, geographic location, or currency.

**2.3** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Financial Model.** The University's ten-year financial framework that includes revenue projections, expense allocations, reserve targets, and sustainability metrics.

**3.2 Gross Revenue.** All revenue generated by the University, including tuition, fees, Waqf income, grants, donations, ancillary services, investment income, and any other lawful sources.

**3.3 Zero-Deficit.** A financial state in which all revenue is allocated to approved categories and no deficit exists. The University shall not operate with a deficit in any fiscal year.

**3.4 Liquidity Reserve.** Funds retained on the University's balance sheet for institutional resilience, operational continuity, future capital deployment, and emergency needs. This reserve is distinct from the Waqf Reserve.

**3.5 Waqf Reserve.** Funds allocated for charitable and endowment purposes, including scholarships, support for schools and mosques, support for widows and orphans, and the Nigeria Mega-University Initiative. This reserve is managed in accordance with Islamic Waqf principles.

**3.6 Tuition Tier.** The regional pricing classification assigned to each student based on the World Bank income classification of their home country. Tiers are: Tier 1 (Very Developed), Tier 2 (Developed), Tier 3 (Developing), and Tier 4 (Underdeveloped/Conflict-Affected).

**3.7 Financial Emergency.** A situation where the University's financial viability is at risk, including significant revenue shortfalls, unexpected large expenses, or other circumstances that threaten the University's ability to meet its obligations.

**3.8 Budget.** The annual financial plan approved by the Board of Trustees, detailing expected revenue and authorized expenditures for the fiscal year.

**3.9 Fiscal Year.** The University's fiscal year shall begin on 1 January and end on 31 December of each year.

**3.10 Audit.** An independent examination of the University's financial records and practices by a certified public accountant.

## 4.0 Policy Statement

**4.1** The University shall maintain a ten-year financial model that ensures sustainability and zero-deficit operations. The Financial Model shall be reviewed annually and updated as necessary.

**4.2** No person shall make financial commitments that exceed approved budgets or available funds.

**4.3** No person shall commit University resources without proper authorization from the appropriate authority.

**4.4** No person shall engage in financial practices that are inconsistent with Islamic values, including the prohibition of riba (interest), gharar (excessive uncertainty), and haram (prohibited) activities.

**4.5** All financial decisions shall be made in accordance with the University's mission, strategic priorities, and the ISLAMIC framework.

**4.6** No person shall manipulate or misrepresent financial information for any purpose.

**4.7** No person shall use University funds for personal gain or unauthorized purposes.

**4.8** The University shall maintain accurate, complete, and transparent financial records in accordance with generally accepted accounting principles (GAAP).

**4.9** No person shall operate any bank account or financial account on behalf of the University without proper authorization.

## 5.0 Revenue Model

**5.1 Revenue Sources**

**5.1.1** The University's revenue shall come from:

**5.1.1.1** Tuition and fees collected from students;

**5.1.1.2** Waqf and endowment income;

**5.1.1.3** Grants from governmental and non-governmental organizations;

**5.1.1.4** Donations from individuals, organizations, and foundations;

**5.1.1.5** Ancillary services and activities;

**5.1.1.6** Investment income from University funds;

**5.1.1.7** Other lawful sources of income.

**5.1.2** No person shall generate revenue in a manner inconsistent with University values or applicable law.

**5.1.3** No person shall accept funds from sources that would compromise the University's mission or reputation.

**5.2 Tuition Tiers**

**5.2.1** Tuition shall be priced according to regional tiers, reflecting the economic circumstances of the student's home country:

**5.2.1.1** Tier 1 — Very Developed (Premium Rate): high-income economies;

**5.2.1.2** Tier 2 — Developed (Standard Global Rate): upper-middle-income economies;

**5.2.1.3** Tier 3 — Developing (Accessible Rate): lower-middle-income economies;

**5.2.1.4** Tier 4 — Underdeveloped/Conflict-Affected (Sponsored Rate): least-developed and conflict-affected nations.

**5.2.2** The tier classification shall be based on the most recent World Bank income classifications and shall be reviewed annually.

**5.2.3** Students may appeal their tier classification by submitting a written request to the Office of Admissions, with supporting documentation.

**5.2.4** No person shall charge tuition inconsistent with the published tier structure.

**5.2.5** No person shall misrepresent a student's tier classification.

**5.3 Revenue Allocation**

**5.3.1** Gross revenue shall be allocated as follows, and no person shall deviate from these allocations without Board approval:

| Category | Percentage | Purpose |
|---|---|---|
| Marketing & Student Acquisition | 10% | Digital acquisition, referral commissions, marketing campaigns, brand development |
| Payroll | 20% | Faculty honoraria, founders' compensation, Senate stipends, core administration |
| Operating Expenses | 5% | Legal, compliance, licenses, filings, audits, overhead |
| LMS & Technology | 5% | Platform hosting, verification systems, technical support, upgrades |
| Da'wah Fund | 5% | Mission activities, outreach programs, community engagement |
| Liquidity Reserve | 35% | Institutional resilience, future capital deployment, emergency needs |
| Waqf Reserve | 20% | Scholarships, schools/mosques, widows/orphans, Nigeria Mega-University |

**5.3.2** No person shall reallocate funds from one category to another without approval from the Board of Trustees.

**5.3.3** All reallocations shall be documented and reported.

**5.3.4** The Board of Trustees may adjust these percentages upon recommendation of the Finance Committee.

## 6.0 Expense Allocation

**6.1 Marketing & Student Acquisition (10%)**

**6.1.1** Funds allocated to this category shall be used for:

**6.1.1.1** Digital marketing and online advertising;

**6.1.1.2** Referral commissions to partners and individuals;

**6.1.1.3** Marketing campaigns and materials;

**6.1.1.4** Brand development and maintenance;

**6.1.1.5** Recruitment events and activities;

**6.1.1.6** Website and social media promotion.

**6.1.2** No person shall use marketing funds for unauthorized purposes.

**6.1.3** No person shall make false or misleading representations in marketing materials.

**6.1.4** All marketing activities shall comply with the University's Marketing Plan.

**6.2 Payroll (20%)**

**6.2.1** Funds allocated to this category shall be allocated as follows:

**6.2.1.1** Faculty Honoraria: 40% of payroll;

**6.2.1.2** Founders' Compensation: 24% of payroll;

**6.2.1.3** Senate Stipends: 18% of payroll;

**6.2.1.4** Core Administration: 18% of payroll.

**6.2.2** Payroll shall be administered in accordance with the Payroll Policy (OPS-006).

**6.2.3** No person shall receive unauthorized compensation.

**6.2.4** No person shall inflate payroll records.

**6.2.5** All compensation shall be reasonable and consistent with the University's mission of service.

**6.3 Operating Expenses (5%)**

**6.3.1** Funds allocated to this category shall be used for:

**6.3.1.1** Legal and compliance costs;

**6.3.1.2** Licenses and regulatory filings;

**6.3.1.3** Audits and financial reviews;

**6.3.1.4** General overhead and administrative costs;

**6.3.1.5** Office supplies and equipment;

**6.3.1.6** Insurance premiums.

**6.3.2** No person shall use operating funds for unauthorized purposes.

**6.3.3** All expenditures shall be properly documented and approved.

**6.4 LMS & Technology (5%)**

**6.4.1** Funds allocated to this category shall be used for:

**6.4.1.1** Learning Management System (LMS) hosting and maintenance;

**6.4.1.2** Verification and security systems;

**6.4.1.3** Technical support and help desk services;

**6.4.1.4** Technology upgrades and improvements;

**6.4.1.5** Software licenses and subscriptions;

**6.4.1.6** Hardware and infrastructure.

**6.4.2** No person shall use technology funds for unauthorized purposes.

**6.4.3** All technology expenditures shall be approved by the Director, Information Technology.

**6.5 Da'wah Fund (5%)**

**6.5.1** Funds allocated to this category shall be used for:

**6.5.1.1** Mission activities and outreach programs;

**6.5.1.2** Community engagement and education;

**6.5.1.3** Da'wah publications and materials;

**6.5.1.4** Programs that advance the University's Islamic mission.

**6.5.2** No person shall use Da'wah funds for unauthorized purposes.

**6.5.3** All Da'wah expenditures shall be approved by the President & Vice-Chancellor.

**6.6 Liquidity Reserve (35%)**

**6.6.1** Funds allocated to this category shall be retained on the University's balance sheet for:

**6.6.1.1** Institutional resilience and operational continuity;

**6.6.1.2** Future capital deployment and growth;

**6.6.1.3** Emergency needs and unforeseen circumstances;

**6.6.1.4** Economic downturns or revenue shortfalls.

**6.6.2** No person shall access Liquidity Reserve funds without approval from the Board of Trustees.

**6.6.3** Funds shall be held in low-risk, liquid instruments.

**6.6.4** Investment decisions shall be made in accordance with the University's investment policy.

**6.7 Waqf Reserve (20%)**

**6.7.1** Funds allocated to this category shall be used for:

**6.7.1.1** Scholarships for deserving students;

**6.7.1.2** Support for schools and mosques;

**6.7.1.3** Support for widows and orphans;

**6.7.1.4** The Nigeria Mega-University Initiative;

**6.7.1.5** Other charitable purposes approved by the Waqf & Endowment Board.

**6.7.2** No person shall use Waqf funds for unauthorized purposes.

**6.7.3** Waqf funds shall be managed in accordance with Islamic principles.

**6.7.4** All Waqf expenditures shall be approved by the Waqf & Endowment Board.

## 7.0 Reserve Management

**7.1 Liquidity Reserve**

**7.1.1** The Liquidity Reserve shall be maintained at a minimum of 35% of annual gross revenue.

**7.1.2** Funds shall be held in low-risk, liquid instruments, such as:

**7.1.2.1** Bank deposits;

**7.1.2.2** Money market funds;

**7.1.2.3** Government securities;

**7.1.2.4** Other low-risk investments approved by the Finance Committee.

**7.1.3** No person shall use Liquidity Reserve funds for operational expenses.

**7.1.4** No person shall make withdrawals from the Liquidity Reserve without Board approval.

**7.1.5** Withdrawals shall be documented and reported to the Board.

**7.2 Waqf Reserve**

**7.2.1** The Waqf Reserve shall be maintained at a minimum of 20% of annual gross revenue.

**7.2.2** Funds shall be managed in accordance with Islamic Waqf principles, including:

**7.2.2.1** Preservation of principal;

**7.2.2.2** Ethical investment;

**7.2.2.3** Charitable distribution of income.

**7.2.3** No person shall use Waqf funds for unauthorized purposes.

**7.2.4** The Waqf & Endowment Board shall oversee the management of Waqf funds.

## 8.0 Zero-Deficit Operations

**8.1** The University shall operate on a zero-deficit basis in all fiscal years.

**8.2** No person shall approve expenditures that exceed available funds.

**8.3** No person shall create a deficit without Board approval.

**8.4** If a deficit is projected, the Deputy Vice-Chancellor, Administration & Finance shall:

**8.4.1** Identify cost-saving measures within 10 business days;

**8.4.2** Recommend budget adjustments;

**8.4.3** Report to the Board of Trustees.

**8.5** No person shall fail to report a projected deficit.

## 9.0 Handling Financial Scenarios

**9.1 Budget Shortfalls**

**9.1.1** When revenue falls short of projections, the Deputy Vice-Chancellor, Administration & Finance shall:

**9.1.1.1** Identify cost-saving measures within 10 business days;

**9.1.1.2** Recommend budget adjustments to the President;

**9.1.1.3** Report to the Board of Trustees at the next meeting.

**9.1.2** Cost-saving measures may include:

**9.1.2.1** Hiring freezes;

**9.1.2.2** Travel restrictions;

**9.1.2.3** Deferral of non-essential expenditures;

**9.1.2.4** Reallocation of funds from lower-priority areas.

**9.1.3** No person shall exceed the budget without authorization.

**9.1.4** No person shall ignore a budget shortfall.

**9.2 Financial Crisis**

**9.2.1** During a financial crisis, the University shall:

**9.2.1.1** Prioritize essential operations;

**9.2.1.2** Activate contingency plans;

**9.2.1.3** Consult the Board of Trustees within 5 business days;

**9.2.1.4** Communicate with stakeholders as appropriate.

**9.2.2** No person shall take unilateral action during a financial crisis.

**9.2.3** No person shall make decisions that jeopardize the University's viability.

**9.3 Fraud**

**9.3.1** When fraud is suspected, the following steps shall be taken:

**9.3.1.1** The matter shall be reported to the Office of Internal Audit immediately;

**9.3.1.2** An investigation shall be initiated within 5 business days;

**9.3.1.3** The person responsible shall be subject to disciplinary action;

**9.3.1.4** Legal action may be pursued.

**9.3.2** No person shall engage in fraud or financial misconduct.

**9.3.3** No person shall destroy evidence related to fraud.

**9.3.4** No person shall retaliate against whistleblowers.

**9.4 Disputes with Vendors**

**9.4.1** When disputes with vendors arise, the Office of Procurement shall:

**9.4.1.1** Document the dispute;

**9.4.1.2** Attempt to resolve the dispute amicably;

**9.4.1.3** Escalate to legal counsel if necessary.

**9.4.2** No person shall enter into unauthorized agreements to settle disputes.

## 10.0 Financial Reporting

**10.1 Monthly Reporting**

**10.1.1** The Office of Finance shall prepare monthly financial reports, including:

**10.1.1.1** Income statement;

**10.1.1.2** Balance sheet;

**10.1.1.3** Cash flow statement;

**10.1.1.4** Budget variance analysis;

**10.1.1.5** Reserve status report.

**10.1.2** Monthly reports shall be submitted to:

**10.1.2.1** The Deputy Vice-Chancellor, Administration & Finance;

**10.1.2.2** The President & Vice-Chancellor.

**10.1.3** No person shall submit inaccurate financial reports.

**10.2 Quarterly Reporting**

**10.2.1** Quarterly financial reports shall be submitted to the Board of Trustees.

**10.2.2** Reports shall include:

**10.2.2.1** Financial statements;

**10.2.2.2** Budget variance analysis;

**10.2.2.3** Reserve status report;

**10.2.2.4** Significant financial developments.

**10.2.3** No person shall omit material information.

**10.3 Annual Reporting**

**10.3.1** Annual financial reports shall be prepared for:

**10.3.1.1** The Board of Trustees;

**10.3.1.2** The University Senate;

**10.3.1.3** External auditors;

**10.3.1.4** Regulatory bodies;

**10.3.1.5** Donors and stakeholders.

**10.3.2** No person shall submit inaccurate annual reports.

**10.4 Audit**

**10.4.1** The University shall undergo an independent financial audit annually.

**10.4.2** The audit shall be conducted by a certified public accountant.

**10.4.3** The audit report shall be presented to the Board of Trustees.

**10.4.4** No person shall interfere with the audit process.

## 11.0 Enforcement

**11.1** No person shall violate any provision of this Policy.

**11.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies, up to and including termination and legal action.

**11.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance with this Policy.

**11.4** The Office of Internal Audit shall conduct periodic reviews of financial compliance.

## 12.0 Related Documents

**12.1** Constitution Article 14 (Financial Sustainability)

**12.2** Strategic Implementation Blueprint 2028–2050 (AMIU-SB-002)

**12.3** Budgeting Policy (OPS-003)

**12.4** Financial Operations Manual (OPS-002)

**12.5** Waqf & Endowment Board Charter

## 13.0 Effective Date

**13.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[2] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to define the definitive, binding, and comprehensive daily financial procedures of Al-Mulk International University, including accounting policies, banking protocols, financial reporting standards, and internal controls.

**1.2** This Policy serves as the binding institutional rule for all financial operations and ensures:

**1.2.1** Financial integrity and accountability in all transactions;

**1.2.2** Compliance with all applicable laws, regulations, and accounting standards;

**1.2.3** Efficient, transparent, and ethical financial operations;

**1.2.4** Strong internal controls to safeguard assets and prevent fraud;

**1.2.5** Accurate and timely financial reporting;

**1.2.6** That no person engages in unauthorized financial transactions.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The Office of Finance and all financial personnel;

**2.1.2** All financial transactions, including revenue, expenditures, and transfers;

**2.1.3** All bank accounts and financial accounts maintained by the University;

**2.1.4** All personnel authorized to handle financial matters;

**2.1.5** Any person acting on behalf of the University in financial matters.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Financial Operations Manual.** The comprehensive guide to all financial procedures, maintained by the Office of Finance.

**3.2 Chart of Accounts.** The classification system for all financial transactions, approved by the Deputy Vice-Chancellor, Administration & Finance.

**3.3 Accounts Payable.** Money owed by the University to vendors, suppliers, and other creditors.

**3.4 Accounts Receivable.** Money owed to the University by students, donors, and other debtors.

**3.5 Internal Control.** Procedures and policies designed to safeguard assets, ensure accuracy, and prevent fraud.

**3.6 Segregation of Duties.** The practice of dividing financial responsibilities among different individuals to prevent fraud and errors.

**3.7 Authorization.** Formal approval of a financial transaction by the appropriate authority.

**3.8 Reconciliation.** The process of comparing financial records to bank statements to ensure accuracy.

**3.9 Fiscal Year.** The University's fiscal year shall begin on 1 January and end on 31 December.

## 4.0 Policy Statement

**4.1** The University shall maintain a Financial Operations Manual that documents all financial procedures.

**4.2** No person shall engage in financial transactions outside the approved procedures documented in the Manual.

**4.3** No person shall make unauthorized financial commitments or expenditures.

**4.4** No person shall circumvent internal controls.

**4.5** The Manual shall be reviewed annually and updated as necessary.

**4.6** No person shall destroy or alter financial records without authorization.

## 5.0 Accounting Policies

**5.1 Accounting Framework**

**5.1.1** The University shall use the accrual basis of accounting in accordance with Generally Accepted Accounting Principles (GAAP).

**5.1.2** All financial transactions shall be recorded in the University's accounting system.

**5.1.3** No person shall record inaccurate or incomplete financial transactions.

**5.2 Chart of Accounts**

**5.2.1** The Chart of Accounts shall be maintained by the Office of Finance.

**5.2.2** All transactions shall be coded to the appropriate account.

**5.2.3** No person shall use incorrect account codes.

**5.2.4** Changes to the Chart of Accounts require approval by the Deputy Vice-Chancellor, Administration & Finance.

**5.3 Internal Controls**

**5.3.1** The University shall maintain strong internal controls, including:

**5.3.1.1 Segregation of duties.** No single person shall have control over all aspects of a financial transaction;

**5.3.1.2 Authorization requirements.** All transactions require approval by the appropriate authority;

**5.3.1.3 Reconciliation procedures.** Bank accounts and financial records shall be reconciled monthly;

**5.3.1.4 Access controls.** Financial systems shall be protected by passwords and access restrictions.

**5.3.2** No person shall circumvent internal controls.

**5.3.3** No person shall have unauthorized access to financial systems.

## 6.0 Banking Protocols

**6.1 Bank Accounts**

**6.1.1** The University shall maintain bank accounts for:

**6.1.1.1** Operating funds;

**6.1.1.2** Liquidity Reserve;

**6.1.1.3** Waqf Reserve.

**6.1.2** All bank accounts shall be in the name of the University.

**6.1.3** No person shall open bank accounts without authorization.

**6.2 Signatory Authority**

**6.2.1** Signatory authority shall be limited to:

**6.2.1.1** The President & Vice-Chancellor;

**6.2.1.2** The Deputy Vice-Chancellor, Administration & Finance.

**6.2.2** All checks and wire transfers shall require two signatures from the persons listed in Section 6.2.1.

**6.2.3** No person shall make unauthorized withdrawals.

**6.3 Reconciliation**

**6.3.1** Bank accounts shall be reconciled monthly.

**6.3.2** Discrepancies shall be investigated immediately.

**6.3.3** No person shall fail to report discrepancies.

## 7.0 Accounts Payable

**7.1 Invoice Processing**

**7.1.1** All invoices shall be submitted to the Office of Finance.

**7.1.2** Invoices shall be verified before payment:

**7.1.2.1** Goods/services were received;

**7.1.2.2** Prices match the purchase order;

**7.1.2.3** Invoices are mathematically accurate.

**7.1.3** No person shall process unauthorized payments.

**7.2 Payment Approval**

**7.2.1** Payments shall be approved by the appropriate authority:

**7.2.1.1** Under $5,000: Finance Manager;

**7.2.1.2** $5,000–$25,000: DVC, Administration & Finance;

**7.2.1.3** Over $25,000: President & Vice-Chancellor.

**7.2.2** No person shall approve payments without proper authority.

**7.3 Vendor Management**

**7.3.1** Vendors shall be vetted before payment.

**7.3.2** Vendor records shall be maintained.

**7.3.3** No person shall pay unauthorized vendors.

## 8.0 Accounts Receivable

**8.1 Invoicing**

**8.1.1** Invoices shall be issued promptly.

**8.1.2** Invoices shall include:

**8.1.2.1** Invoice number;

**8.1.2.2** Date;

**8.1.2.3** Description of goods/services;

**8.1.2.4** Amount due;

**8.1.2.5** Payment terms and deadline.

**8.1.3** No person shall fail to issue invoices.

**8.2 Collections**

**8.2.1** Overdue accounts shall be followed up promptly.

**8.2.2** Collection procedures:

**8.2.2.1** 30 days overdue: first reminder;

**8.2.2.2** 60 days overdue: second reminder;

**8.2.2.3** 90 days overdue: final notice;

**8.2.2.4** 120 days overdue: collection action.

**8.2.3** No person shall write off accounts without authorization.

## 9.0 Financial Reporting

**9.1 Monthly Reports**

**9.1.1** Monthly financial reports shall include:

**9.1.1.1** Income statement;

**9.1.1.2** Balance sheet;

**9.1.1.3** Cash flow statement;

**9.1.1.4** Budget variance analysis.

**9.1.2** Reports shall be submitted by the 15th of the following month.

**9.1.3** No person shall submit inaccurate reports.

**9.2 Annual Reports**

**9.2.1** Annual financial reports shall be prepared for:

**9.2.1.1** The Board of Trustees;

**9.2.1.2** The University Senate;

**9.2.1.3** External auditors;

**9.2.1.4** Regulatory bodies.

**9.2.2** No person shall submit inaccurate annual reports.

## 10.0 Enforcement

**10.1** No person shall violate any provision of this Policy.

**10.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**10.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance with this Policy.

## 11.0 Related Documents

**11.1** Budgeting Policy (OPS-003)

**11.2** Procurement Policy (OPS-004)

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[3] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive budget development, approval, monitoring, and reporting process for Al-Mulk International University.

**1.2** This Policy ensures:

**1.2.1** Fiscal accountability and transparency in all budgetary matters;

**1.2.2** Resource allocation aligned with the University's strategic priorities and mission;

**1.2.3** That no person makes unauthorized budget decisions or expenditures;

**1.2.4** That all expenditures are within approved budgets;

**1.2.5** That budget variances are identified and addressed promptly.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University, including all academic and administrative units;

**2.1.2** All budget decisions and allocations;

**2.1.3** All personnel authorized to manage budgets;

**2.1.4** Any person acting on behalf of the University in budget matters.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Budget.** The financial plan for the fiscal year, detailing expected revenue and authorized expenditures.

**3.2 Fiscal Year.** The period from 1 January to 31 December.

**3.3 Budget Variance.** The difference between budgeted and actual amounts.

**3.4 Budget Adjustment.** A change to the approved budget.

**3.5 Operating Budget.** The budget for day-to-day operations.

**3.6 Capital Budget.** The budget for capital expenditures.

## 4.0 Policy Statement

**4.1** The University shall maintain a formal budgeting process.

**4.2** No person shall spend funds outside the approved budget.

**4.3** No person shall make unauthorized budget adjustments.

**4.4** All budget decisions shall align with the University's strategic priorities.

## 5.0 Budget Process

**5.1 Budget Planning Cycle**

**5.1.1** The budget cycle shall begin six months before the fiscal year (1 July).

**5.1.2** Departments shall submit budget requests by 1 August.

**5.1.3** The Office of Finance shall consolidate requests by 1 September.

**5.1.4** The draft budget shall be presented to the Board by 1 November.

**5.1.5** The budget shall be approved by 1 December.

**5.1.6** The budget shall take effect on 1 January.

**5.2 Budget Development**

**5.2.1** The Deputy Vice-Chancellor, Administration & Finance shall oversee budget development.

**5.2.2** Department heads shall submit budget requests, including:

**5.2.2.1** Prior year actuals;

**5.2.2.2** Current year projections;

**5.2.2.3** Justification for requested amounts;

**5.2.2.4** Strategic priorities and goals.

**5.2.3** The Office of Finance shall review requests for completeness.

**5.2.4** No person shall submit incomplete budget requests.

**5.3 Budget Approval**

**5.3.1** The President & Vice-Chancellor shall review the draft budget.

**5.3.2** The budget shall be presented to the Board of Trustees.

**5.3.3** The Board shall approve the budget by a majority vote.

**5.3.4** No budget shall be implemented without Board approval.

## 6.0 Budget Monitoring

**6.1 Monthly Monitoring**

**6.1.1** Department heads shall monitor their budgets monthly.

**6.1.2** The Office of Finance shall prepare variance reports.

**6.1.3** Significant variances shall be investigated.

**6.1.4** No person shall ignore budget variances.

**6.2 Budget Adjustments**

**6.2.1** Budget adjustments shall be submitted to the Office of Finance.

**6.2.2** Adjustments under $10,000: department head approval.

**6.2.3** Adjustments $10,000–$50,000: DVC, Administration & Finance approval.

**6.2.4** Adjustments over $50,000: President & Vice-Chancellor approval.

**6.2.5** No person shall make unauthorized budget adjustments.

**6.3 Year-End Close**

**6.3.1** The fiscal year shall close on 31 December.

**6.3.2** Unused budget funds shall revert to the University's general fund.

**6.3.3** No person shall make unauthorized expenditures at year-end.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**7.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance with this Policy.

## 8.0 Related Documents

**8.1** Financial Model (OPS-001)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[4] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive purchasing procedures, bidding requirements, contract management, and vendor selection standards for Al-Mulk International University.

**1.2** This Policy ensures:

**1.2.1** Ethical, transparent, and cost-effective procurement;

**1.2.2** Compliance with all applicable laws and regulations;

**1.2.3** That no person engages in fraudulent or unethical procurement practices;

**1.2.4** That all procurement decisions are documented and accountable.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University;

**2.1.2** All procurement activities, regardless of funding source;

**2.1.3** All vendors and suppliers;

**2.1.4** Any person authorized to make purchases.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Procurement.** The process of acquiring goods and services.

**3.2 Competitive Bidding.** The process of soliciting bids from multiple vendors.

**3.3 Vendor.** A supplier of goods or services.

**3.4 Contract.** A legally binding agreement with a vendor.

**3.5 Purchase Order.** A document authorizing a purchase.

**3.6 Sole-Source Procurement.** Procurement from a single vendor without competitive bidding.

## 4.0 Policy Statement

**4.1** All procurement shall follow the procedures defined in this policy.

**4.2** No person shall make unauthorized purchases.

**4.3** No person shall engage in fraudulent procurement practices.

**4.4** All procurement shall be ethical, transparent, and cost-effective.

## 5.0 Purchasing Methods

**5.1 Small Purchases**

**5.1.1** Purchases under $1,000: direct purchase, subject to budget availability.

**5.1.2** Purchases $1,000–$5,000: quotes from three vendors.

**5.1.3** No person shall split purchases to avoid thresholds.

**5.2 Medium Purchases**

**5.2.1** Purchases $5,000–$25,000: formal quotes from three vendors.

**5.2.2** Evaluation criteria shall include price, quality, and service.

**5.2.3** No person shall award contracts without proper evaluation.

**5.3 Large Purchases**

**5.3.1** Purchases over $25,000: formal bidding process.

**5.3.2** Bids shall be advertised publicly.

**5.3.3** Evaluation criteria shall be published.

**5.3.4** No person shall award contracts without competitive bidding.

## 6.0 Vendor Selection

**6.1 Vendor Evaluation**

**6.1.1** Vendors shall be evaluated on:

**6.1.1.1** Price;

**6.1.1.2** Quality;

**6.1.1.3** Reliability;

**6.1.1.4** Ethical standards;

**6.1.1.5** Past performance.

**6.1.2** No person shall select vendors based on personal relationships.

**6.2 Vendor Approval**

**6.2.1** All vendors shall be approved by the Office of Procurement.

**6.2.2** Vendor records shall be maintained.

**6.2.3** No person shall use unapproved vendors.

## 7.0 Contract Management

**7.1 Contract Approval**

**7.1.1** Contracts shall be reviewed by the Office of Legal Counsel.

**7.1.2** Contracts shall be signed by authorized personnel:

**7.1.2.1** Under $25,000: DVC, Administration & Finance;

**7.1.2.2** Over $25,000: President & Vice-Chancellor.

**7.1.3** No person shall sign contracts without proper authority.

**7.2 Contract Monitoring**

**7.2.1** Contracts shall be monitored for performance.

**7.2.2** Non-compliance shall be addressed promptly.

**7.2.3** No person shall ignore contract violations.

## 8.0 Conflict of Interest

**8.1** No person shall participate in procurement where they have a conflict of interest.

**8.2** Conflicts shall be disclosed immediately.

**8.3** Persons with conflicts shall recuse themselves.

## 9.0 Enforcement

**9.1** No person shall violate any provision of this Policy.

**9.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**9.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance with this Policy.

## 10.0 Related Documents

**10.1** Financial Operations Manual (OPS-002)

## 11.0 Effective Date

**11.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[5] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive tuition billing, payment plan options, and refund procedures for all students.

**1.2** This Policy ensures:

**1.2.1** Financial clarity and transparency for all students;

**1.2.2** Student support and flexibility in meeting financial obligations;

**1.2.3** Fiscal accountability for the University;

**1.2.4** That no student is unaware of their financial obligations;

**1.2.5** That no student is denied access due to financial hardship without first being offered assistance.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All students enrolled in any program;

**2.1.2** All tuition and fee payments;

**2.1.3** All refund requests.

**2.2** No student is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Grand Total.** The sum of all mandatory fees payable by a student, including tuition, registration, assessment, digital certificate, and project/thesis/dissertation fees.

**3.2 Payment Plan.** An arrangement for paying the Grand Total in installments rather than a single payment.

**3.3 Refund.** The return of tuition and fees paid to the University.

**3.4 Financial Hardship.** A condition in which a student is unable to pay the Grand Total due to circumstances beyond their control.

**3.5 Withdrawal.** The formal process by which a student discontinues enrollment in a program or course.

## 4.0 Policy Statement

**4.1** Tuition shall be billed, collected, and refunded in accordance with this policy.

**4.2** No student shall be denied enrollment due to inability to pay without first being offered assistance.

**4.3** No student shall receive unauthorized refunds.

**4.4** All students shall be informed of their financial obligations at the time of enrollment.

## 5.0 Billing

**5.1 Billing Cycle**

**5.1.1** Invoices shall be issued at the beginning of each semester.

**5.1.2** Invoices shall be sent electronically through the Student Portal.

**5.1.3** Invoices shall include:

**5.1.3.1** The Grand Total;

**5.1.3.2** Payment options;

**5.1.3.3** Payment deadlines;

**5.1.3.4** Late payment penalties;

**5.1.3.5** Contact information for financial assistance.

**5.1.4** No person shall fail to issue invoices.

**5.2 Payment Deadlines**

**5.2.1** Payment shall be due 30 days from the invoice date.

**5.2.2** Late payments shall be subject to penalties as defined in this Policy.

**5.2.3** No student shall fail to pay by the deadline without authorization.

## 6.0 Payment Options

**6.1 Full Upfront Payment**

**6.1.1** Students may pay the full Grand Total at enrollment.

**6.1.2** A 15% discount shall be applied.

**6.1.3** Payment shall be due at the time of enrollment.

**6.2 Annual Payment**

**6.2.1** Students may pay annually.

**6.2.2** A 10% discount shall be applied.

**6.2.3** Payment shall be due at the start of the academic year.

**6.3 Semester Payment**

**6.3.1** Students may pay per semester.

**6.3.2** A 5% discount shall be applied.

**6.3.3** Payment shall be due at the start of each semester.

**6.4 Monthly Payment**

**6.4.1** Students may pay monthly.

**6.4.2** No discount shall be applied.

**6.4.3** A 3.9% servicing fee shall be charged.

**6.4.4** Payments shall be due on the 1st of each month.

**6.5 Sub-Monthly Payment**

**6.5.1** Students may pay bi-weekly or weekly.

**6.5.2** No discount shall be applied.

**6.5.3** A 3.9% servicing fee shall be charged.

**6.5.4** Payments shall be due on schedule.

## 7.0 Refund Schedule

**7.1 Withdrawal Timeline**

| Withdrawal Time | Refund Percentage |
|---|---|
| Before the semester starts | 100% |
| During the first week | 75% |
| During the second week | 50% |
| During the third week | 25% |
| After the third week | 0% |

**7.2 Refund Process**

**7.2.1** Students must formally withdraw to receive a refund.

**7.2.2** Refund requests shall be submitted in writing.

**7.2.3** Refunds shall be processed within 30 days.

**7.2.4** No student shall receive unauthorized refunds.

## 8.0 Financial Hardship

**8.1** Students experiencing financial hardship may request:

**8.1.1** Payment extensions;

**8.1.2** Alternative payment plans;

**8.1.3** Waqf scholarship review.

**8.2** Requests shall be submitted in writing to the Office of Finance.

**8.3** Supporting documentation may be required.

**8.4** No student shall be denied consideration for financial hardship.

## 9.0 Enforcement

**9.1** No person shall violate any provision of this Policy.

**9.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**9.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance with this Policy.

## 10.0 Related Documents

**10.1** Constitution Article 14 (Financial Sustainability)

**10.2** Academic Catalog (ACA-001)

**10.3** Student Policies Handbook

## 11.0 Effective Date

**11.1** This Policy is effective as of 1 January 2028.
'''


CONTENT[6] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive payroll procedures, compensation administration, and statutory compliance standards for Al-Mulk International University.

**1.2** This Policy ensures:

**1.2.1** Accurate and timely payment to all employees;

**1.2.2** Legal compliance with all applicable tax and labor laws;

**1.2.3** Employee satisfaction and trust;

**1.2.4** That no employee receives unauthorized compensation;

**1.2.5** That all compensation is consistent with the University's mission of service.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All employees of the University;

**2.1.2** All compensation payments;

**2.1.3** All payroll-related activities.

**2.2** No employee is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Payroll.** The process of calculating and distributing employee compensation.

**3.2 Honorarium.** Compensation for services rendered.

**3.3 Deductions.** Amounts withheld from employee pay for taxes, benefits, and other purposes.

**3.4 Payroll Schedule.** The frequency of payroll processing and distribution.

**3.5 Payroll Record.** Documentation of employee compensation and deductions.

## 4.0 Policy Statement

**4.1** Payroll shall be administered in accordance with this policy.

**4.2** No person shall receive unauthorized compensation.

**4.3** No person shall alter payroll records without authorization.

**4.4** All payroll records shall be maintained in accordance with applicable law.

## 5.0 Payroll Schedule

**5.1** Payroll shall be processed monthly.

**5.2** Payroll shall be disbursed on the last working day of each month.

**5.3** If the last working day falls on a weekend or holiday, payroll shall be disbursed on the preceding working day.

**5.4** No person shall fail to process payroll on time.

## 6.0 Compensation Administration

**6.1 Honorarium Calculation**

**6.1.1** Honoraria shall be calculated as defined in the Constitution:

**6.1.1.1** Faculty Honoraria: 40% of payroll;

**6.1.1.2** Founders' Compensation: 24% of payroll;

**6.1.1.3** Senate Stipends: 18% of payroll;

**6.1.1.4** Core Administration: 18% of payroll.

**6.1.2** No person shall receive unauthorized honoraria.

**6.2 Deductions**

**6.2.1** Deductions shall be made as required by law.

**6.2.2** Voluntary deductions shall be authorized by the employee.

**6.2.3** No person shall make unauthorized deductions.

**6.3 Payroll Reconciliation**

**6.3.1** Payroll records shall be reconciled monthly.

**6.3.2** Discrepancies shall be investigated immediately.

**6.3.3** No person shall ignore payroll discrepancies.

## 7.0 Record Keeping

**7.1** Payroll records shall be maintained for seven years.

**7.2** Records shall include:

**7.2.1** Employee information;

**7.2.2** Compensation details;

**7.2.3** Deductions;

**7.2.4** Tax information;

**7.2.5** Payroll history.

**7.3** No person shall destroy or alter payroll records.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**8.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance with this Policy.

## 9.0 Related Documents

**9.1** Constitution Article 14 (Financial Sustainability)

**9.2** HR Policies & Procedures Manual (OPS-007)

**9.3** Compensation Policy (OPS-010)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[7] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive guide to all human resources policies, procedures, and standards for Al-Mulk International University.

**1.2** This Policy ensures:

**1.2.1** Fair and consistent treatment of all employees;

**1.2.2** Legal compliance with all applicable employment laws;

**1.2.3** Employee satisfaction and professional development;

**1.2.4** That no person engages in discrimination or harassment.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All employees of the University;

**2.1.2** All employment-related activities;

**2.1.3** All employment records.

**2.2** No employee is exempt from the requirements of this Policy.

## 3.0 Policy Statement

**3.1** The University shall maintain a comprehensive HR Policies and Procedures Manual.

**3.2** No person shall engage in discrimination or harassment.

**3.3** No person shall violate any HR policy.

**3.4** The Manual shall be reviewed annually.

## 4.0 Contents

**4.1** The Manual shall include:

**4.1.1** Equal Employment Opportunity;

**4.1.2** Employment Categories;

**4.1.3** Records;

**4.1.4** Compensation;

**4.1.5** Benefits;

**4.1.6** Conduct and Discipline;

**4.1.7** Grievance Procedures;

**4.1.8** Termination Procedures.

## 5.0 Enforcement

**5.1** No person shall violate any provision of this Policy.

**5.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**5.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance with this Policy.

## 6.0 Related Documents

**6.1** Constitution Article 9 (Administration)

**6.2** Bylaws (GOV-003)

**6.3** Recruitment & Hiring Policy (OPS-008)

## 7.0 Effective Date

**7.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[8] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive recruitment, selection, and hiring process for all positions.

**1.2** This Policy ensures:

**1.2.1** Fair and consistent hiring practices;

**1.2.2** Legal compliance with all applicable employment laws;

**1.2.3** Quality recruitment of qualified personnel.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All hiring processes;

**2.1.2** All positions.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Policy Statement

**3.1** All recruitment and hiring shall follow the process defined in this policy.

**3.2** All hiring shall be non-discriminatory.

**3.3** No person shall engage in discriminatory hiring practices.

## 4.0 Hiring Process

**4.1 Position Authorization.**

**4.1.1** All new positions require authorization.

**4.1.2** Authorization shall be obtained from the appropriate authority.

**4.2 Position Description.**

**4.2.1** A position description shall be prepared.

**4.2.2** The description shall include qualifications and responsibilities.

**4.3 Recruitment.**

**4.3.1** Positions shall be advertised appropriately.

**4.3.2** Recruitment sources shall be diverse.

**4.4 Selection.**

**4.4.1** A selection committee shall be formed.

**4.4.2** Candidates shall be evaluated based on qualifications.

**4.5 Background Checks.**

**4.5.1** Background checks shall be conducted.

**4.5.2** Results shall be reviewed before hiring.

## 5.0 Enforcement

**5.1** No person shall violate any provision of this Policy.

**5.2** Violation of this Policy shall result in disciplinary action.

**5.3** The Director, Human Resources shall ensure compliance.

## 6.0 Related Documents

**6.1** HR Policies & Procedures Manual (OPS-007)

## 7.0 Effective Date

**7.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[9] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive standard employment contract format for all employee categories at Al-Mulk International University.

**1.2** This Policy ensures:

**1.2.1** Consistency and clarity in all employment agreements;

**1.2.2** Legal compliance with all applicable employment laws;

**1.2.3** That no employee is employed without a properly executed contract;

**1.2.4** That all employment terms are clearly documented and understood.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All employees of the University, including full-time, part-time, and adjunct;

**2.1.2** All employment contracts and agreements;

**2.1.3** All contract renewals and amendments.

**2.2** No employee is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Employment Contract.** A legally binding agreement between the University and an employee.

**3.2 Term of Appointment.** The duration of the employment relationship.

**3.3 Compensation.** The total remuneration paid to the employee.

**3.4 Probationary Period.** The initial period of employment during which the employee's performance is evaluated.

**3.5 Confidentiality.** The obligation to protect University information.

## 4.0 Policy Statement

**4.1** All employment contracts shall follow the standard template provided in this policy.

**4.2** No person shall employ any individual without a properly executed contract.

**4.3** No person shall deviate from the standard template without approval from the Office of Legal Counsel.

**4.4** All contracts shall be reviewed by the Office of Human Resources.

## 5.0 Contract Template

**5.1** Every employment contract shall contain, at minimum, the following sections in this order: employee information; position; term of appointment; compensation; duties and responsibilities; performance expectations; termination; confidentiality; code of conduct; and a signed acknowledgment by both the employee and an authorized University representative.

**5.2** The Office of Human Resources shall maintain the current standard-form template implementing Section 5.1 and shall issue every new contract from that template without ad hoc alteration to its structure.

## 6.0 Contract Provisions

**6.1 Term of Appointment**

**6.1.1** The term of appointment shall be specified in the contract.

**6.1.2** Appointments shall be for a fixed term, renewable at the University's discretion.

**6.1.3** No person shall be employed without a specified term.

**6.2 Probationary Period**

**6.2.1** All new employees shall serve a probationary period of three to six months.

**6.2.2** During the probationary period, the employee's performance shall be evaluated.

**6.2.3** The University may terminate the employee during the probationary period without cause.

**6.3 Confidentiality**

**6.3.1** All employees shall maintain confidentiality of:

**6.3.1.1** Student records;

**6.3.1.2** Financial information;

**6.3.1.3** Strategic plans;

**6.3.1.4** Proprietary information;

**6.3.1.5** Personnel records.

**6.3.2** No employee shall disclose confidential information without authorization.

**6.3.3** Violation of confidentiality shall result in disciplinary action.

## 7.0 Contract Amendment

**7.1** Amendments to contracts require approval by:

**7.1.1** The Office of Human Resources;

**7.1.2** The Office of Legal Counsel.

**7.2** Amendments shall be in writing and signed by both parties.

**7.3** No person shall make unauthorized amendments.

## 8.0 Enforcement

**8.1** No person shall employ any individual without a properly executed contract.

**8.2** No person shall deviate from the standard template without approval.

**8.3** Violation of this Policy shall result in disciplinary action.

## 9.0 Related Documents

**9.1** HR Policies & Procedures Manual (OPS-007)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[10] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive compensation philosophy, personnel categories, and discretionary allowance and recognition framework for every person who serves the University in any capacity.

**1.2** This Policy ensures:

**1.2.1** That compensation reflects the University's identity as a religious, mission-driven, non-profit, Waqf-oriented institution serving the Ummah;

**1.2.2** That no provision of this Policy creates a guaranteed salary obligation the University cannot sustain if enrollment, donations, grants, or Waqf income fluctuate;

**1.2.3** That the Board of Trustees retains full discretion over every compensation decision, consistent with Constitution Article 14, Section 14.3;

**1.2.4** Fair, transparent, and mission-aligned treatment of every person who serves the University, whether as a volunteer, on a part-time or contract basis, or as permanent staff or faculty;

**1.2.5** Legal compliance with all applicable wage and hour laws;

**1.2.6** That no person receives unauthorized compensation.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All employees of the University;

**2.1.2** All volunteers serving the University in any capacity;

**2.1.3** All faculty, regardless of category;

**2.1.4** All members of University governance bodies who receive compensation, honoraria, allowances, or stipends for their service.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Compensation.** Any base salary, honorarium, stipend, fee, allowance, award, or revenue-participation payment provided in exchange for service to the University.

**3.2 Volunteer.** A person serving the University primarily for religious service, da'wah, community contribution, or charitable participation, without an employment relationship or guarantee of payment.

**3.3 Adjunct/Part-Time Faculty.** Faculty compensated through teaching stipends, course-delivery payments, supervision fees, examination fees, project fees, research grants, or approved allowances, whose compensation may vary significantly by assignment.

**3.4 Contract Faculty.** Faculty compensated according to a fixed-term contract that specifies duration, workload, responsibilities, qualifications, and available institutional resources.

**3.5 Permanent Faculty.** Faculty holding an indefinite appointment, eligible for base salary, performance incentives, allowances, grants, revenue participation, and research support, each as determined under this Policy.

**3.6 Allowance.** A discretionary, policy-based payment made to offset a specific category of expense incurred in service to the University, not a component of base salary.

**3.7 Honorarium.** A discretionary payment made in recognition of service, distinct from a salary and carrying no expectation of continuation or increase.

**3.8 Revenue Participation.** A discretionary, Board-approved share of programme surplus, executive education revenue, research revenue, or approved grants awarded to a selected permanent academic leader in recognition of performance.

**3.9 Market Benchmarking.** The process of comparing compensation to market rates at peer institutions, used to inform, not bind, the Board's compensation decisions.

**3.10 Merit Increase.** A discretionary compensation increase based on performance, awarded from a pool the Board determines is affordable each year.

## 4.0 Policy Statement

**4.1** Compensation for every category of person described in this Policy shall be determined by the Board of Trustees upon recommendation of the President and the Finance Committee, consistent with Constitution Article 14, Section 14.3.

**4.2** No provision of this Policy shall be construed to guarantee any person a fixed salary, allowance, award, or revenue-participation payment irrespective of the University's financial condition.

**4.3** No person shall receive unauthorized compensation.

**4.4** No person shall set compensation levels without proper authority.

**4.5** All compensation decisions shall take into account institutional resources, financial sustainability, workload, qualifications, responsibilities, performance, market conditions, and mission alignment.

**4.6** No person shall represent any category of service described in this Policy as an employment relationship where it is not one.

## 5.0 Personnel Categories

**5.1 Category A — Volunteers.**

**5.1.1** Volunteers serve primarily for religious service, da'wah, community contribution, or charitable participation and are not employees of the University.

**5.1.2** A Volunteer may receive no compensation, occasional gifts, discretionary stipends, approved allowances, and awards and recognition under Section 8.0.

**5.1.3** No guarantee of salary shall exist for a Volunteer, and no person shall represent a Volunteer as an employee.

**5.2 Category B — Adjunct/Part-Time Faculty.**

**5.2.1** Adjunct and part-time faculty are compensated through teaching stipends, course-delivery payments, supervision fees, examination fees, project fees, research grants, and approved allowances.

**5.2.2** Compensation for Adjunct/Part-Time Faculty may vary significantly by course load, subject area, and assignment, as determined under Section 6.0.

**5.3 Category C — Contract Faculty.**

**5.3.1** Contract Faculty are compensated according to their contract's duration, workload, responsibilities, qualifications, performance, and available institutional resources.

**5.3.2** No provision of this Policy or any other University policy shall lock the University into a compensation commitment beyond what a Contract Faculty member's contract specifies.

**5.4 Category D — Permanent Faculty.**

**5.4.1** Permanent Faculty may receive base salary, performance incentives, allowances, grants, revenue participation, leadership stipends, and research support, each subject to the Board's discretion under this Policy.

**5.5 Senate Compensation Model.**

**5.5.1** Membership in the University Senate does not, by itself, imply any salary.

**5.5.2** A Volunteer Senate Member shall receive no salary, but may receive meeting honoraria where approved and approved allowances.

**5.5.3** A Contract Senate Member's compensation shall be based on the actual duties the member performs for the University, under that member's contract.

**5.5.4** An Executive Senate Member (a Senate seat held by virtue of an executive administrative appointment, such as the President & Vice-Chancellor or a Deputy Vice-Chancellor) shall be compensated according to that member's employment contract, not according to Senate membership itself.

## 6.0 Compensation Principles

**6.1** The University's compensation philosophy is based on:

**6.1.1 Mission-Driven Service.** Compensation is framed first as acknowledgment of service to the University's mission and to the Ummah;

**6.1.2 Board Discretion.** Every compensation decision preserves the Board of Trustees' discretion and is never a self-executing entitlement;

**6.1.3 Fairness and Transparency.** Compensation decisions are made consistently and are transparent to the persons affected by them;

**6.1.4 Sustainability.** No compensation commitment may be made that could render the University unable to meet its obligations if enrollment, donations, grants, or Waqf income decline;

**6.1.5 Mission-Aligned Competitiveness.** Compensation, taken together with the opportunities described in Section 8.0, is designed to attract qualified personnel without competing on salary alone.

**6.2** Compensation for each Category described in Section 5.0 shall be determined by the Board of Trustees upon recommendation of the President and the Finance Committee, taking into consideration:

**6.2.1** Institutional resources and financial sustainability;

**6.2.2** Workload, qualifications, and responsibilities;

**6.2.3** Performance;

**6.2.4** Market conditions, informed by the benchmarking described in Section 10.0;

**6.2.5** Mission alignment.

**6.3** No Constitution provision, University policy, or contract shall state a fixed minimum or maximum compensation figure for any rank or role as a binding, self-executing entitlement; compensation figures the Board adopts from time to time under this Section are administrative guidance, not contractual guarantees, and remain subject to annual review and Board discretion.

**6.4** No person shall set compensation without the authority this Policy grants.

## 7.0 Allowance Framework

**7.1** Allowances are discretionary, policy-based payments approved by the Board of Trustees upon recommendation of the President and the Finance Committee, subject to available institutional resources. No allowance described in this Section creates a guaranteed entitlement.

**7.2 Connectivity Allowance.** For internet and digital-teaching expenses incurred by faculty and staff delivering instruction or performing duties online.

**7.3 Communication Allowance.** For institutional calls and communications incurred in the course of University service.

**7.4 Research & Publication Allowance.** For books, journal-publication fees, conference participation, and academic projects.

**7.5 Healthcare Support Allowance.** Subject to this Policy and to available institutional resources.

**7.6 Professional Development Allowance.** For certifications, training, workshops, and seminars.

**7.7 Technology Allowance.** For laptops, devices, software, and teaching equipment.

**7.8** The Board of Trustees shall set and periodically revise the amount or range of each allowance described in this Section, published in the HR Policies & Procedures Manual (OPS-007).

**7.9** No person shall claim an allowance described in this Section without proper authorization.

## 8.0 Awards and Recognition

**8.1 Academic Excellence Award.** For exceptional academic contribution. May include a cash award, a research grant, conference sponsorship, or honorary recognition, as the Board of Trustees determines.

**8.2 Service to the Ummah Award.** For exceptional religious service. May include recognition, grant support, travel sponsorship, or institutional honor, as the Board of Trustees determines.

**8.3** No award described in this Section is a recurring entitlement; each award is granted at the Board's discretion for the specific contribution it recognizes.

**8.4** The University's value proposition to prospective and current scholars includes a global teaching platform, international student reach, academic freedom within the University's mission, research opportunities, publication support, recognition, an opportunity for Islamic service, leadership opportunities, grants, stipends, awards, flexible contracts, and remote-participation options, in addition to any compensation described elsewhere in this Policy.

**8.5** No person shall represent any award described in this Section as a guaranteed or recurring payment.

## 9.0 Revenue Participation Framework

**9.1** The Board of Trustees may, at its discretion, approve a revenue-participation arrangement for a selected Permanent Faculty member holding an academic leadership role, drawn from:

**9.1.1** A percentage of programme surplus;

**9.1.2** A percentage of executive education revenue;

**9.1.3** A percentage of research revenue;

**9.1.4** A percentage of approved grants;

**9.1.5** A performance-incentive pool.

**9.2** Every revenue-participation arrangement shall be:

**9.2.1** Transparent, and disclosed to the Board of Trustees in full;

**9.2.2** Approved by the Board of Trustees before it takes effect;

**9.2.3** Legally compliant with the University's non-profit status;

**9.2.4** Financially sustainable, assessed against the same zero-deficit standard as the Financial Model (OPS-001).

**9.3** No revenue-participation arrangement shall guarantee a fixed percentage in perpetuity; every arrangement remains subject to annual Board review and may be adjusted or discontinued at the Board's discretion.

**9.4** No person shall enter into or represent a revenue-participation arrangement without Board approval.

## 10.0 Market Benchmarking

**10.1** The University shall conduct market benchmarking annually to inform, not bind, the Board's compensation decisions under Section 6.0.

**10.2** Benchmarking shall compare compensation to:

**10.2.1** Similar positions at peer institutions;

**10.2.2** Regional market rates;

**10.2.3** The compensation practices of comparable religious and mission-driven non-profit institutions.

**10.3** No person shall set compensation without reference to the benchmarking described in this Section, and no benchmarking result binds the Board beyond the discretion described in Section 6.0.

## 11.0 Merit Increases

**11.1** Merit increases shall be based on performance reviews.

**11.2** The annual merit-increase pool, if any, shall be determined by the Board of Trustees based on institutional resources and financial sustainability.

**11.3** No person shall receive an unauthorized merit increase.

## 12.0 Enforcement

**12.1** No person shall violate any provision of this Policy.

**12.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**12.3** The Director, Human Resources shall ensure compliance with this Policy.

## 13.0 Related Documents

**13.1** Constitution Article 14, Section 14.3 (Compensation)

**13.2** Financial Model (OPS-001)

**13.3** Payroll Policy (OPS-006)

**13.4** HR Policies & Procedures Manual (OPS-007)

## 14.0 Effective Date

**14.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[11] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive employee leave entitlements, accrual rates, and approval procedures.

**1.2** This Policy ensures:

**1.2.1** Fair and consistent leave administration;

**1.2.2** Legal compliance with all applicable leave laws;

**1.2.3** Employee wellbeing and work-life balance;

**1.2.4** That no employee abuses leave privileges.

## 2.0 Scope

**2.1** This Policy applies to all employees.

## 3.0 Definitions

**3.1 Leave.** Time off from work with or without pay.

**3.2 Annual Leave.** Paid time off for personal use.

**3.3 Sick Leave.** Paid time off for illness or injury.

**3.4 Religious Leave.** Time off for religious observances.

**3.5 Parental Leave.** Time off for the birth or adoption of a child.

**3.6 Leave Accrual.** The accumulation of leave over time.

## 4.0 Policy Statement

**4.1** Employee leave shall be administered in accordance with this policy.

**4.2** No person shall abuse leave privileges.

**4.3** No person shall take unauthorized leave.

**4.4** All leave requests shall be properly documented.

## 5.0 Leave Types

**5.1 Annual Leave**

**5.1.1** Full-time employees shall accrue annual leave.

**5.1.2** Accrual rate: 15 days per year.

**5.1.3** Unused annual leave may be carried over to the next year (maximum 30 days).

**5.1.4** Annual leave requests shall be submitted in advance.

**5.2 Sick Leave**

**5.2.1** Full-time employees shall accrue sick leave.

**5.2.2** Accrual rate: 10 days per year.

**5.2.3** Sick leave requests shall be supported by documentation.

**5.2.4** Sick leave may be used for personal illness or family illness.

**5.3 Religious Leave**

**5.3.1** Employees may take leave for religious observances.

**5.3.2** Advance notice is required.

**5.3.3** Religious leave shall be unpaid unless annual leave is used.

**5.4 Parental Leave**

**5.4.1** Employees may take parental leave for:

**5.4.1.1** Birth of a child;

**5.4.1.2** Adoption of a child.

**5.4.2** Duration: as per applicable law.

**5.4.3** No employee shall be denied parental leave.

**5.5 Professional Development Leave**

**5.5.1** Employees may take leave for professional development.

**5.5.2** Requests shall be submitted in writing.

**5.5.3** Approval shall be based on:

**5.5.3.1** Relevance to the employee's role;

**5.5.3.2** Budget availability.

## 6.0 Leave Approval

**6.1** Leave requests shall be submitted to the supervisor.

**6.2** Approval shall be based on:

**6.2.1** Staffing requirements;

**6.2.2** Leave balance;

**6.2.3** Timing.

**6.3** No person shall take leave without approval.

## 7.0 Enforcement

**7.1** No person shall abuse leave privileges.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Human Resources shall ensure compliance.

## 8.0 Related Documents

**8.1** HR Policies & Procedures Manual (OPS-007)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[12] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive performance review process and standards for employee evaluation.

**1.2** This Policy ensures:

**1.2.1** Fair and consistent employee evaluation;

**1.2.2** Employee development and growth;

**1.2.3** Accountability and performance improvement;

**1.2.4** That no employee is exempt from performance review.

## 2.0 Scope

**2.1** This Policy applies to all employees.

## 3.0 Definitions

**3.1 Performance Review.** The systematic evaluation of employee performance.

**3.2 Self-Assessment.** The employee's own evaluation of their performance.

**3.3 Supervisory Evaluation.** The evaluation of the employee by their supervisor.

**3.4 Performance Improvement Plan.** A plan to address performance deficiencies.

## 4.0 Policy Statement

**4.1** All employees shall undergo annual performance reviews.

**4.2** No employee shall be exempt from performance review.

**4.3** All performance reviews shall be documented.

## 5.0 Review Process

**5.1 Self-Assessment**

**5.1.1** Employees shall complete a self-assessment annually.

**5.1.2** The assessment shall include:

**5.1.2.1** Achievements;

**5.1.2.2** Challenges;

**5.1.2.3** Goals;

**5.1.2.4** Development needs.

**5.1.3** No employee shall fail to submit a self-assessment.

**5.2 Supervisory Evaluation**

**5.2.1** Supervisors shall evaluate employees based on:

**5.2.1.1** Performance against goals;

**5.2.1.2** Quality of work;

**5.2.1.3** Professionalism;

**5.2.1.4** Teamwork;

**5.2.1.5** Attendance.

**5.2.2** No supervisor shall fail to evaluate employees.

**5.3 Review Meeting**

**5.3.1** A review meeting shall be conducted.

**5.3.2** Feedback shall be provided.

**5.3.3** Goals shall be set for the next period.

**5.4 Performance Improvement Plan**

**5.4.1** If performance is unsatisfactory, a Performance Improvement Plan shall be developed.

**5.4.2** The plan shall include:

**5.4.2.1** Specific improvement actions;

**5.4.2.2** Timelines;

**5.4.2.3** Success indicators.

**5.4.3** Failure to improve may result in disciplinary action.

## 6.0 Enforcement

**6.1** No person shall fail to participate in performance reviews.

**6.2** Violation of this Policy shall result in disciplinary action.

**6.3** The Director, Human Resources shall ensure compliance.

## 7.0 Related Documents

**7.1** HR Policies & Procedures Manual (OPS-007)

## 8.0 Effective Date

**8.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[13] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive process and standards for employee separation.

**1.2** This Policy ensures:

**1.2.1** Fair and consistent termination decisions;

**1.2.2** Legal compliance with all applicable employment laws;

**1.2.3** Protection of employee rights;

**1.2.4** That no employee is terminated without due process.

## 2.0 Scope

**2.1** This Policy applies to all employees.

## 3.0 Definitions

**3.1 Termination.** The end of employment.

**3.2 Voluntary Resignation.** Termination initiated by the employee.

**3.3 Non-Renewal.** Termination at the end of a contract term.

**3.4 Termination for Cause.** Termination for misconduct or poor performance.

**3.5 Reduction in Force.** Termination due to budget constraints or reorganization.

## 4.0 Policy Statement

**4.1** All terminations shall follow the process defined in this policy.

**4.2** No employee shall be terminated without due process.

**4.3** No employee shall be terminated in a discriminatory manner.

## 5.0 Termination Types

**5.1 Voluntary Resignation**

**5.1.1** Employees may resign by providing 30 days' written notice.

**5.1.2** The supervisor shall acknowledge the resignation.

**5.1.3** The employee shall complete an exit interview.

**5.1.4** No employee shall resign without proper notice.

**5.2 Non-Renewal**

**5.2.1** Non-renewal shall be communicated at least 60 days before the end of the contract.

**5.2.2** Reasons for non-renewal shall be documented.

**5.2.3** No employee shall be non-renewed without proper notice.

**5.3 Termination for Cause**

**5.3.1** Cause for termination includes:

**5.3.1.1** Gross misconduct;

**5.3.1.2** Theft or fraud;

**5.3.1.3** Harassment or discrimination;

**5.3.1.4** Violation of University policies;

**5.3.1.5** Poor performance after a Performance Improvement Plan.

**5.3.2** No employee shall be terminated for cause without investigation.

**5.4 Reduction in Force**

**5.4.1** Reduction in force shall be based on:

**5.4.1.1** Budget constraints;

**5.4.1.2** Reorganization;

**5.4.1.3** Program closure.

**5.4.2** Selection criteria shall be documented.

**5.4.3** No employee shall be terminated in a discriminatory manner.

## 6.0 Termination Process

**6.1 Notice**

**6.1.1** Written notice of termination shall be provided.

**6.1.2** The notice shall include:

**6.1.2.1** Effective date;

**6.1.2.2** Reason for termination;

**6.1.2.3** Appeal rights.

**6.1.3** No employee shall be terminated without notice.

**6.2 Appeal**

**6.2.1** Employees have the right to appeal termination decisions.

**6.2.2** Appeals shall be submitted in writing within 14 days.

**6.2.3** Appeals shall be heard by the Grievance Committee.

**6.3 Exit Interview**

**6.3.1** Employees shall participate in an exit interview.

**6.3.2** The interview shall document:

**6.3.2.1** Reasons for leaving;

**6.3.2.2** Suggestions for improvement.

**6.3.3** No employee shall be exempt from exit interview.

## 7.0 Enforcement

**7.1** No person shall terminate an employee without due process.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Human Resources shall ensure compliance.

## 8.0 Related Documents

**8.1** HR Policies & Procedures Manual (OPS-007)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[14] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive technology infrastructure strategy, architecture, and management standards for the University.

**1.2** This Policy ensures:

**1.2.1** Reliable, secure, and scalable technology infrastructure;

**1.2.2** Alignment with the University's strategic goals;

**1.2.3** Effective use of technology resources;

**1.2.4** That no person compromises the University's technology infrastructure.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University;

**2.1.2** All technology infrastructure;

**2.1.3** All users of technology resources.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 IT Infrastructure.** The hardware, software, networks, and systems that support University operations.

**3.2 Cloud Infrastructure.** Off-site computing resources accessed over the internet.

**3.3 Network.** The communication system connecting University systems.

**3.4 Security Infrastructure.** Measures to protect systems and data.

## 4.0 Policy Statement

**4.1** The University shall maintain a comprehensive IT Infrastructure Plan.

**4.2** No person shall compromise the University's technology infrastructure.

**4.3** No person shall use technology resources for unauthorized purposes.

## 5.0 Infrastructure Components

**5.1 Architecture**

**5.1.1** The University shall maintain a scalable technology architecture.

**5.1.2** Architecture shall include:

**5.1.2.1** Cloud-based services;

**5.1.2.2** On-premise systems;

**5.1.2.3** Hybrid solutions.

**5.2 Network**

**5.2.1** The University shall maintain:

**5.2.1.1** Reliable internet connectivity;

**5.2.1.2** Redundant network paths;

**5.2.1.3** Secure access.

**5.2.2** No person shall disrupt network operations.

**5.3 Servers**

**5.3.1** The University shall maintain:

**5.3.1.1** Reliable server infrastructure;

**5.3.1.2** Redundant systems;

**5.3.1.3** Regular maintenance.

**5.3.2** No person shall compromise server security.

## 6.0 Security

**6.1** Security measures shall include:

**6.1.1** Firewalls;

**6.1.2** Intrusion detection;

**6.1.3** Data encryption;

**6.1.4** Access controls;

**6.1.5** Regular security audits.

**6.2** No person shall compromise security measures.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Information Technology shall ensure compliance.

## 8.0 Related Documents

**8.1** Constitution Article 9 (Administration)

**8.2** Data Privacy & Security Policy (OPS-016)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[15] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive technical requirements, architecture, and specifications for the Learning Management System (LMS).

**1.2** This Policy ensures:

**1.2.1** A reliable, secure, and accessible LMS;

**1.2.2** Effective delivery of online education;

**1.2.3** Compliance with accessibility standards;

**1.2.4** That no person compromises the LMS.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The LMS platform;

**2.1.2** All users of the LMS;

**2.1.3** All courses delivered through the LMS.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 LMS.** Learning Management System, the platform for online education.

**3.2 User Roles.** The permissions assigned to different types of users.

**3.3 Accessibility.** The ability of all users to access LMS features.

## 4.0 Policy Statement

**4.1** The LMS shall meet the technical specifications defined in this policy.

**4.2** No person shall compromise the LMS.

**4.3** No person shall use the LMS for unauthorized purposes.

## 5.0 Technical Specifications

**5.1 Platform Requirements**

**5.1.1** The LMS shall be accessible via:

**5.1.1.1** Web browsers;

**5.1.1.2** Mobile devices;

**5.1.1.3** Tablets.

**5.1.2** The LMS shall support:

**5.1.2.1** Video streaming;

**5.1.2.2** File uploads;

**5.1.2.3** Discussion forums;

**5.1.2.4** Assessments;

**5.1.2.5** Gradebooks.

**5.2 Hosting Requirements**

**5.2.1** The LMS shall be hosted on reliable infrastructure.

**5.2.2** Hosting shall provide:

**5.2.2.1** 99.9% uptime;

**5.2.2.2** Scalability;

**5.2.2.3** Security.

**5.3 User Roles**

**5.3.1** The LMS shall support:

**5.3.1.1** Student roles;

**5.3.1.2** Faculty roles;

**5.3.1.3** Administrator roles;

**5.3.1.4** Guest roles.

## 6.0 Accessibility

**6.1** The LMS shall comply with:

**6.1.1** WCAG 2.1 standards;

**6.1.2** ADA requirements;

**6.1.3** Section 508 standards.

**6.2** No person shall create inaccessible content.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Information Technology shall ensure compliance.

## 8.0 Related Documents

**8.1** IT Infrastructure Plan (OPS-014)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[16] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive data protection standards, privacy compliance, and incident response protocols.

**1.2** This Policy ensures:

**1.2.1** Protection of all University data;

**1.2.2** Compliance with applicable privacy laws;

**1.2.3** Effective response to data incidents;

**1.2.4** That no person compromises data privacy or security.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University;

**2.1.2** All data processed by the University;

**2.1.3** All personnel who handle data;

**2.1.4** All systems that store data.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Data.** Any information processed by the University.

**3.2 Personal Data.** Data that identifies or can identify an individual.

**3.3 Data Breach.** An incident in which data is accessed without authorization.

**3.4 Data Classification.** The categorization of data based on sensitivity.

## 4.0 Policy Statement

**4.1** All data shall be protected in accordance with this policy.

**4.2** No person shall compromise data privacy or security.

**4.3** No person shall access data without authorization.

**4.4** Data breaches shall be reported immediately.

## 5.0 Data Classification

**5.1** Data shall be classified as:

**5.1.1 Public.** Information that may be shared publicly;

**5.1.2 Internal.** Information for internal use only;

**5.1.3 Confidential.** Information requiring protection;

**5.1.4 Restricted.** Information requiring strict protection (e.g., student records, financial data).

**5.2** No person shall disclose data outside its classification.

## 6.0 Data Protection

**6.1** Protection measures shall include:

**6.1.1** Encryption;

**6.1.2** Access controls;

**6.1.3** Regular backups;

**6.1.4** Security audits.

**6.2** No person shall disable security measures.

## 7.0 Data Breach Response

**7.1** When a breach is suspected:

**7.1.1** Report to the Director, Information Technology immediately;

**7.1.2** Contain the breach;

**7.1.3** Investigate the cause;

**7.1.4** Notify affected individuals;

**7.1.5** Report to regulatory bodies if required.

**7.2** No person shall fail to report a breach.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Director, Information Technology shall ensure compliance.

## 9.0 Related Documents

**9.1** Constitution Article 17 (Records and Archives)

**9.2** FERPA Compliance Policy (LEG-001)

**9.3** GDPR Compliance Policy (LEG-002)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[17] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive backup procedures, recovery objectives, and disaster recovery protocols.

**1.2** This Policy ensures:

**1.2.1** Data protection and recovery capability;

**1.2.2** Business continuity;

**1.2.3** That no person fails to follow backup procedures.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All University data;

**2.1.2** All systems and applications.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Backup.** A copy of data for recovery purposes.

**3.2 RTO (Recovery Time Objective).** The maximum acceptable downtime.

**3.3 RPO (Recovery Point Objective).** The maximum acceptable data loss.

## 4.0 Policy Statement

**4.1** The University shall maintain a comprehensive Backup and Disaster Recovery Plan.

**4.2** No person shall fail to follow backup procedures.

**4.3** No person shall compromise recovery capability.

## 5.0 Backup Procedures

**5.1** Backups shall be performed:

**5.1.1** Daily for critical systems;

**5.1.2** Weekly for non-critical systems.

**5.2** Backups shall be stored:

**5.2.1** On-site for quick recovery;

**5.2.2** Off-site for disaster recovery.

## 6.0 Recovery Objectives

**6.1** RTO: 4 hours for critical systems.

**6.2** RPO: 24 hours for critical data.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Information Technology shall ensure compliance.

## 8.0 Related Documents

**8.1** Data Privacy & Security Policy (OPS-016)

**8.2** Emergency Response Plan (OPS-022)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[18] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive IT support services, response standards, and escalation procedures.

**1.2** This Policy ensures:

**1.2.1** Effective IT support for all users;

**1.2.2** Consistent service delivery;

**1.2.3** Timely resolution of issues.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All users;

**2.1.2** All IT support services.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 IT Support.** Services provided by the Office of Information Technology.

**3.2 Service Level.** The expected response and resolution times.

**3.3 Escalation.** The process of escalating issues to higher-level support.

## 4.0 Policy Statement

**4.1** IT support shall be provided in accordance with this policy.

**4.2** No person shall fail to respond to support requests.

**4.3** No person shall provide unauthorized IT support.

## 5.0 Services

**5.1** Services shall include:

**5.1.1** Help desk support;

**5.1.2** Technical troubleshooting;

**5.1.3** Account management;

**5.1.4** Training and guidance.

## 6.0 Service Levels

**6.1 Response Times**

| Priority | Response Time | Resolution Time |
|---|---|---|
| Critical | 1 hour | 4 hours |
| High | 4 hours | 24 hours |
| Medium | 24 hours | 72 hours |
| Low | 72 hours | 1 week |

## 7.0 Escalation

**7.1** Escalation shall occur when:

**7.1.1** Issues are not resolved within SLA;

**7.1.2** Issues require higher-level expertise.

**7.2** Escalation levels:

**7.2.1** Level 1: Help Desk;

**7.2.2** Level 2: IT Support Specialist;

**7.2.3** Level 3: Director, IT.

## 8.0 Enforcement

**8.1** No person shall fail to follow this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Director, Information Technology shall ensure compliance.

## 9.0 Related Documents

**9.1** IT Infrastructure Plan (OPS-014)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[19] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive standards for acceptable use of University technology resources.

**1.2** This Policy ensures:

**1.2.1** Responsible use of technology resources;

**1.2.2** Security and integrity of systems;

**1.2.3** That no person misuses technology resources.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All users of University technology resources;

**2.1.2** All technology resources.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Technology Resources.** All hardware, software, networks, and systems.

**3.2 Acceptable Use.** Use that is consistent with University policies and values.

**3.3 Prohibited Use.** Use that is unauthorized or harmful.

## 4.0 Policy Statement

**4.1** All users shall use technology resources responsibly.

**4.2** No person shall misuse technology resources.

**4.3** No person shall use technology resources for illegal purposes.

## 5.0 Acceptable Use

**5.1** Technology resources may be used for:

**5.1.1** Academic activities;

**5.1.2** Research;

**5.1.3** University business;

**5.1.4** Personal use (limited).

## 6.0 Prohibited Use

**6.1** Technology resources shall not be used for:

**6.1.1** Illegal activities;

**6.1.2** Harassment or bullying;

**6.1.3** Personal gain;

**6.1.4** Unauthorized access;

**6.1.5** Malware or hacking.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Information Technology shall ensure compliance.

## 8.0 Related Documents

**8.1** Data Privacy & Security Policy (OPS-016)

**8.2** Student Code of Conduct (STU-001)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[20] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive operations, maintenance, planning, and management standards for University facilities.

**1.2** This Policy ensures:

**1.2.1** Safe and well-maintained facilities;

**1.2.2** Effective use of space;

**1.2.3** Compliance with health and safety regulations.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All University facilities;

**2.1.2** All users of facilities.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Facilities.** All University buildings, grounds, and infrastructure.

**3.2 Maintenance.** The upkeep of facilities.

**3.3 Space Allocation.** The assignment of space to users.

## 4.0 Policy Statement

**4.1** All facilities shall be maintained in accordance with this policy.

**4.2** No person shall misuse facilities.

**4.3** No person shall damage facilities.

## 5.0 Maintenance

**5.1** Regular maintenance shall be performed:

**5.1.1** Preventive maintenance;

**5.1.2** Corrective maintenance;

**5.1.3** Emergency repairs.

**5.2** No person shall fail to report maintenance issues.

## 6.0 Space Allocation

**6.1** Space shall be allocated based on:

**6.1.1** Need;

**6.1.2** Function;

**6.1.3** Priority.

**6.2** No person shall occupy space without authorization.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Facilities shall ensure compliance.

## 8.0 Related Documents

**8.1** Health & Safety Policy (OPS-021)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[21] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive occupational health and safety standards, procedures, and responsibilities.

**1.2** This Policy ensures:

**1.2.1** A safe environment for all members of the University community;

**1.2.2** Compliance with all health and safety regulations;

**1.2.3** That no person engages in unsafe practices.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All employees, students, and visitors;

**2.1.2** All University facilities and activities.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Health and Safety.** The protection of people from harm.

**3.2 Hazard.** Any source of potential harm.

**3.3 Incident.** Any event that causes or could cause harm.

## 4.0 Policy Statement

**4.1** The University shall maintain a safe and healthy environment.

**4.2** No person shall engage in unsafe practices.

**4.3** No person shall fail to report hazards or incidents.

## 5.0 Safety Standards

**5.1** Safety standards shall include:

**5.1.1** Fire safety;

**5.1.2** Emergency evacuation;

**5.1.3** First aid;

**5.1.4** Hazard identification and control.

## 6.0 Incident Reporting

**6.1** All incidents shall be reported:

**6.1.1** Immediately for serious incidents;

**6.1.2** Within 24 hours for minor incidents.

**6.2** No person shall fail to report an incident.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Facilities shall ensure compliance.

## 8.0 Related Documents

**8.1** Emergency Response Plan (OPS-022)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[22] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive response procedures for all types of emergencies affecting the University.

**1.2** This Policy ensures:

**1.2.1** Effective and coordinated emergency response;

**1.2.2** Protection of life and property;

**1.2.3** Continuity of University operations through and beyond an emergency.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All employees, students, and visitors;

**2.1.2** All emergency situations affecting the University, wherever they occur.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Emergency.** A situation requiring immediate response to protect life, property, or University operations.

**3.2 Emergency Response Team.** The personnel designated by the Director, Facilities to coordinate the University's response to an emergency.

**3.3 Evacuation.** The organized movement of people away from a location of danger to a safe location.

## 4.0 Policy Statement

**4.1** The University shall maintain a comprehensive Emergency Response Plan covering all foreseeable categories of emergency.

**4.2** No person shall fail to follow emergency procedures during a declared emergency.

**4.3** No person shall interfere with emergency response personnel or operations.

## 5.0 Emergency Types

**5.1** The Emergency Response Plan shall address, at minimum:

**5.1.1** Natural disasters;

**5.1.2** Medical emergencies;

**5.1.3** Fires;

**5.1.4** Active threats;

**5.1.5** Cyber incidents affecting University systems or data.

## 6.0 Response Procedures

**6.1 General**

**6.1.1** For any emergency, personnel shall, in order:

**6.1.1.1** Call emergency services;

**6.1.1.2** Notify the Emergency Response Team;

**6.1.1.3** Follow published evacuation procedures;

**6.1.1.4** Account for all personnel at the designated assembly point.

**6.2 Fire**

**6.2.1** Activate the nearest fire alarm;

**6.2.2** Evacuate the building by the nearest safe route;

**6.2.3** Call the local emergency number from a position of safety.

**6.3 Medical Emergency**

**6.3.1** Call emergency services immediately;

**6.3.2** Administer first aid only if trained to do so;

**6.3.3** Notify the Emergency Response Team.

**6.4 Active Threat**

**6.4.1** Run if a safe route exists; hide if it does not; fight only as a last resort;

**6.4.2** Call emergency services as soon as it is safe to do so;

**6.4.3** Notify the Emergency Response Team.

## 7.0 Enforcement

**7.1** No person shall interfere with emergency response.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Facilities shall ensure compliance with this Policy.

## 8.0 Related Documents

**8.1** Health & Safety Policy (OPS-021)

**8.2** Crisis Management Policy (WAQ-008)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[23] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive usage, requirements, and support standards for the University's Learning Management System (LMS).

**1.2** This Policy ensures:

**1.2.1** Consistent and effective use of the LMS across every course;

**1.2.2** Academic integrity in online learning;

**1.2.3** Accessibility of the LMS for all students.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All users of the LMS;

**2.1.2** All courses delivered through the LMS.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 LMS.** The University's Learning Management System, the single authorized platform for online course delivery.

**3.2 Course Structure.** The required organization of course materials within the LMS.

**3.3 User Roles.** The permissions assigned to students, faculty, and administrators within the LMS.

## 4.0 Policy Statement

**4.1** The LMS shall be the sole and exclusive platform for online education at the University.

**4.2** No person shall use an unauthorized platform for course delivery.

**4.3** No person shall compromise the security or integrity of the LMS.

## 5.0 Course Structure

**5.1** Every course shall be structured in the LMS with:

**5.1.1** A course syllabus;

**5.1.2** Weekly modules;

**5.1.3** Assignments;

**5.1.4** Discussion forums;

**5.1.5** Lecture recordings.

## 6.0 User Roles

**6.1** Users shall have role-based permissions:

**6.1.1 Students.** View course materials, submit assignments, and participate in discussion forums;

**6.1.2 Faculty.** Create and manage courses, grade assignments, and moderate discussion forums;

**6.1.3 Administrators.** Manage all technical and administrative aspects of the LMS.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Information Technology shall ensure compliance with this Policy.

## 8.0 Related Documents

**8.1** LMS Technical Specifications (OPS-015)

**8.2** IT Support Policy (OPS-018)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[24] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive training requirements for faculty who teach online.

**1.2** This Policy ensures:

**1.2.1** Effective online teaching;

**1.2.2** Consistent quality across every online course;

**1.2.3** That no faculty member teaches online without completing the required training.

## 2.0 Scope

**2.1** This Policy applies to all faculty who teach, or intend to teach, an online course.

## 3.0 Policy Statement

**3.1** All faculty shall complete the required training in online pedagogy before teaching an online course.

**3.2** No faculty member shall teach an online course without completing the required training.

## 4.0 Training Requirements

**4.1** All faculty shall complete:

**4.1.1** Online Pedagogy Training: Principles and Practices;

**4.1.2** LMS Proficiency Training: Course Management;

**4.1.3** Online Assessment Training: Proctoring and Grading.

## 5.0 Ongoing Development

**5.1** Faculty shall participate in annual professional development in online teaching.

**5.2** Faculty shall have access to resources on:

**5.2.1** Current best practices in online pedagogy;

**5.2.2** Emerging educational technologies;

**5.2.3** Student engagement strategies.

## 6.0 Evaluation

**6.1** Faculty online teaching shall be evaluated annually.

**6.2** Evaluation shall include:

**6.2.1** Student evaluations of teaching;

**6.2.2** Peer review of online course design;

**6.2.3** Self-assessment.

## 7.0 Enforcement

**7.1** No faculty member shall teach an online course without completing the required training.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance with this Policy.

## 8.0 Related Documents

**8.1** Faculty Evaluation System (ACA-005)

**8.2** LMS Technical Specifications (OPS-015)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[25] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive virtual office hours requirements for faculty.

**1.2** This Policy ensures:

**1.2.1** Reliable student access to faculty;

**1.2.2** Effective student support across time zones;

**1.2.3** That no faculty member fails to hold the required office hours.

## 2.0 Scope

**2.1** This Policy applies to all faculty.

## 3.0 Policy Statement

**3.1** All faculty shall maintain virtual office hours in accordance with this Policy.

**3.2** No faculty member shall fail to hold the required office hours.

## 4.0 Requirements

**4.1** Faculty shall hold at least two hours of virtual office hours per week.

**4.2** Office hours shall be scheduled at times that reasonably accommodate students in different time zones.

**4.3** Office hours shall be accessible via:

**4.3.1** Video conferencing;

**4.3.2** Chat;

**4.3.3** Email.

## 5.0 Communication

**5.1** Faculty shall respond to student emails within 48 hours.

**5.2** Faculty shall respond to urgent student inquiries within 24 hours.

## 6.0 Enforcement

**6.1** No faculty member shall fail to hold the required office hours.

**6.2** Violation of this Policy shall result in disciplinary action.

**6.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance with this Policy.

## 7.0 Related Documents

**7.1** Virtual Faculty & Student Support Policy (ACA-019)

## 8.0 Effective Date

**8.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[26] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive standards for access to online library resources and digital materials.

**1.2** This Policy ensures:

**1.2.1** Access to quality research and learning resources;

**1.2.2** Support for research and scholarship across every program;

**1.2.3** That no student or faculty member is denied access to the digital library.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All students, faculty, and staff;

**2.1.2** All digital library resources maintained or licensed by the University.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Policy Statement

**3.1** The University shall provide access to digital library resources to every student, faculty member, and staff member.

**3.2** No student or faculty member shall be denied access to the digital library.

## 4.0 Resources

**4.1** The digital library's resources shall include:

**4.1.1** E-books;

**4.1.2** Academic journals;

**4.1.3** Research databases;

**4.1.4** Primary texts in Arabic;

**4.1.5** Lecture archives.

## 5.0 Access

**5.1** The digital library shall be accessible online twenty-four hours a day, seven days a week.

**5.2** Access shall be available via:

**5.2.1** The University website;

**5.2.2** The Student Portal.

## 6.0 Research Support

**6.1** Research support shall be available via:

**6.1.1** Email;

**6.1.2** Chat;

**6.1.3** Virtual consultation.

## 7.0 Enforcement

**7.1** No person shall deny access to library resources in violation of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The University Librarian shall ensure compliance with this Policy.

## 8.0 Effective Date

**8.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[27] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive standards for the use of social media for student communication and learning.

**1.2** This Policy ensures:

**1.2.1** Effective institutional and student communication;

**1.2.2** Professional conduct across every social media platform used for University purposes;

**1.2.3** Protection of the University's reputation.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All students;

**2.1.2** All social media platforms used for University communication.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Policy Statement

**3.1** Social media shall be used responsibly for University-related communication.

**3.2** No person shall misuse social media in a manner inconsistent with this Policy.

**3.3** No person shall post inappropriate content under the University's name or on an official University account.

## 4.0 Official Social Media

**4.1** Official University social media accounts shall be managed exclusively by the Office of Communications.

**4.2** Official accounts shall be used for:

**4.2.1** University announcements;

**4.2.2** Student engagement;

**4.2.3** Recruitment.

## 5.0 Student Use

**5.1** Students may use social media for:

**5.1.1** Study groups;

**5.1.2** Discussion forums;

**5.1.3** Community engagement.

**5.2** Students shall adhere to the Digital Citizenship & Online Conduct Policy (STU-014) in all social media use.

## 6.0 Prohibited Use

**6.1** Social media shall not be used for:

**6.1.1** Harassment or bullying;

**6.1.2** Sharing inappropriate content;

**6.1.3** Misrepresentation of the University or its programs.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Director, Communications shall ensure compliance with this Policy.

## 8.0 Related Documents

**8.1** Digital Citizenship & Online Conduct Policy (STU-014)

**8.2** Social Media Policy (MKT-004)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
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
