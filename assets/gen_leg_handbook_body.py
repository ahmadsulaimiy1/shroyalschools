#!/usr/bin/env python3
"""Author work_leg_handbook_body.md — the 11-policy body of the AMIU Legal
& Compliance Handbook (Doc Codes LEG-001 through LEG-011), the seventh AMIU
flagship publication, in the same navy/gold editorial system as the
Blueprint, Constitution, Institutional Governance Compendium, Academic
Handbook, Student Policies Handbook, and Operations Handbook.

Source: the 11 fully-drafted LEG policies supplied by the user, transcribed
here with the fixes found during the editorial review applied directly
(not just noted) — see the Publication Certification Statement in
assets/leg_handbook_back.md for what each fix was and why. The defects
found mirror the same two systemic patterns already found and fixed in the
Operations Handbook:

  1. Authority citations. Six of the eleven policies cited "Constitution
     Article 15, Section 15.1" (Transparency and Accountability — Annual
     Report/Audit/Conflict of Interest/Whistleblower) or a bare "Article
     13"/"Article 11" for matters those Articles do not address. FERPA and
     GDPR (records/data protection) are corrected to Article 17, Section
     17.2 (Access to Records), the one Article 17 subsection that
     explicitly names FERPA. Intellectual Property is corrected to Article
     9, Section 9.1 (Administration's general operational authority), since
     no Article addresses IP specifically and the policy is stewarded and
     enforced entirely by the Office of Legal Counsel, an Administration
     function. Non-Discrimination & Title IX is corrected to Article 12,
     Section 12.1 (Admission), the one provision that states the
     non-discrimination principle in the Constitution's own text.
     Cross-Border Payment Systems is corrected to Article 14, Section 14.2
     (Tuition), matching the Tuition Collection & Refund Policy (OPS-005)
     it is a companion to. International Faculty Recruitment is corrected
     to Article 9, Section 9.3 (Appointment), matching the domestic
     Recruitment & Hiring Policy (OPS-008) it mirrors. The three
     international-operations policies (Gambia Branch, Nigeria Campus,
     Country-Specific Regulatory Compliance) already cited Article 2,
     Section 2.3 (Legal Domicile) correctly — that section is the one that
     actually addresses branch campuses and multi-jurisdiction compliance —
     and are unchanged, as is the Texas State Regulatory Filings Policy's
     Article 2, Section 2.2 (Legal Status) citation.

  2. Approval Authority assigned to the University Senate for policies with
     no academic content (FERPA, GDPR, Intellectual Property,
     Non-Discrimination & Title IX, Country-Specific Regulatory Compliance,
     Cross-Border Payment Systems, International Faculty Recruitment) —
     the same bicameral non-interference conflict found and fixed across
     the Operations Handbook (Article 4.2: the Senate holds academic
     authority, the Board/Administration holds financial and operational
     authority). Reassigned to the Board of Trustees, or, for International
     Faculty Recruitment, to the Deputy Vice-Chancellor, Administration &
     Finance — matching the exact approval authority already assigned to
     the domestic Recruitment & Hiring Policy (OPS-008) it mirrors.
     International Student Support Policy (LEG-011) keeps the University
     Senate as its Approval Authority: its sibling policy of the same name
     in the Student Policies Handbook (STU-013) is likewise approved by the
     Senate, and consistency between the two is preferable to a change that
     would only apply to one.

  3. LEG-003's Related Documents cited "Certificate of Formation (LEG-001)"
     — but LEG-001 in this handbook is the FERPA Compliance Policy; the
     Certificate of Formation is a governance document (GOV-004 in the
     Institutional Governance Compendium's registry), not a Legal &
     Compliance one. Corrected to GOV-004.

Formatting is normalized to house style (numbered outline points become
bold-numbered paragraphs, ALL-CAPS section headers become sentence case)
but no provision, clause, or numbered point from the source is cut,
shortened, or merged away.
"""

OUT = "/home/user/shroyalschools/work_leg_handbook_body.md"

# ---------------------------------------------------------------------------
# Divider generator (mirrors gen_ops_handbook_body.py's divider() pattern)
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
      <w:r><w:rPr><w:rFonts w:ascii="Source Serif 4" w:hAnsi="Source Serif 4"/><w:i/><w:smallCaps/><w:color w:val="8C97AB"/><w:sz w:val="19"/><w:spacing w:val="14"/></w:rPr><w:t>Legal &amp; Compliance Handbook &#183; Policy {num} of 11</w:t></w:r></w:p>''')
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
 (1, "LEG-001", "FERPA Compliance Policy", "University Registrar", "Office of the Registrar",
  "Constitution Article 17, Section 17.2",
  "Forty-five days to inspect, written consent before disclosure, and a logged record of every release of a student's education record.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Student Rights Under FERPA"),("6.0","Access to Education Records"),
   ("7.0","Disclosure of Education Records"),("8.0","Amendment of Records"),
   ("9.0","Training Requirements"),("10.0","Handling FERPA Scenarios"),("11.0","Enforcement"),
   ("12.0","Related Documents"),("13.0","Effective Date")]),
 (2, "LEG-002", "GDPR Compliance Policy", "Director, Information Technology", "Office of Information Technology",
  "Constitution Article 17, Section 17.2",
  "Six lawful bases for processing, seven data-subject rights, and a seventy-two-hour clock on every reportable breach.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Data Protection Principles"),("6.0","Lawful Basis for Processing"),
   ("7.0","Data Subject Rights"),("8.0","Data Breach Response"),("9.0","Enforcement"),
   ("10.0","Related Documents"),("11.0","Effective Date")]),
 (3, "LEG-003", "Texas State Regulatory Filings Policy", "Office of Legal Counsel", "Office of Legal Counsel",
  "Constitution Article 2, Section 2.2",
  "Every certificate, exemption, and annual report the State of Texas requires, tracked to a deadline no one is allowed to miss.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Required Filings"),("6.0","Deadlines"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (4, "LEG-004", "Intellectual Property Policy", "Office of Legal Counsel", "Office of Legal Counsel",
  "Constitution Article 9, Section 9.1",
  "Work created on the University's time belongs to the University; scholarship belongs to its author, licensed back for teaching.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Ownership"),("6.0","Use and Protection"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (5, "LEG-005", "Non-Discrimination & Title IX Policy", "Deputy Vice-Chancellor, Administration & Finance", "Office of Human Resources",
  "Constitution Article 12, Section 12.1",
  "A single standard against discrimination and harassment, one Title IX Coordinator, and a promise that no complaint goes uninvestigated.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Prohibited Conduct"),("6.0","Title IX Compliance"),
   ("7.0","Handling Discrimination Scenarios"),("8.0","Enforcement"),
   ("9.0","Related Documents"),("10.0","Effective Date")]),
 (6, "LEG-006", "Gambia Branch Operational Plan", "Deputy Vice-Chancellor, Administration & Finance", "Office of International Operations",
  "Constitution Article 2, Section 2.3",
  "Registered with NAQAA, licensed with the Registrar of Companies, and answerable to the Senate for its academic quality.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Registration and Licensing"),("6.0","Accreditation"),("7.0","Operations"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (7, "LEG-007", "Nigeria Campus Development Plan", "Deputy Vice-Chancellor, Administration & Finance", "Office of International Operations",
  "Constitution Article 2, Section 2.3",
  "A Mega-University campus built to Nigerian law, from Corporate Affairs Commission registration to an NUC charter by Year 10.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Registration and Licensing"),("6.0","NUC Charter Application"),
   ("7.0","Site Acquisition and Construction"),("8.0","Enforcement"),
   ("9.0","Related Documents"),("10.0","Effective Date")]),
 (8, "LEG-008", "Country-Specific Regulatory Compliance", "Office of Legal Counsel", "Office of International Operations",
  "Constitution Article 2, Section 2.3",
  "One legal review before entering any jurisdiction, and a standing watch for the regulatory change that follows.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Compliance Requirements"),("6.0","Handling Compliance Scenarios"),
   ("7.0","Enforcement"),("8.0","Related Documents"),("9.0","Effective Date")]),
 (9, "LEG-009", "Cross-Border Payment Systems Policy", "Deputy Vice-Chancellor, Administration & Finance", "Office of Finance",
  "Constitution Article 14, Section 14.2",
  "Four payment rails, one settlement currency, and a sanctions screen no transaction is allowed to skip.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Payment Gateways"),("6.0","Currency Conversion"),("7.0","Sanctions Compliance"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (10, "LEG-010", "International Faculty Recruitment Policy", "Director, Human Resources", "Office of Human Resources",
  "Constitution Article 9, Section 9.3",
  "Visa sponsorship, relocation support, and a hiring process that never outruns its own immigration paperwork.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Recruitment Process"),("6.0","Visa and Work Authorization"),
   ("7.0","Relocation and Support"),("8.0","Enforcement"),
   ("9.0","Related Documents"),("10.0","Effective Date")]),
 (11, "LEG-011", "International Student Support Policy", "Dean of Students", "Office of Student Affairs",
  "Constitution Article 12, Section 12.2",
  "Pre-arrival guidance, SEVIS compliance, and a standing commitment that no international student is left to navigate alone.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Support Services"),("6.0","Visa and SEVIS Compliance"),
   ("7.0","Handling International Student Scenarios"),("8.0","Enforcement"),
   ("9.0","Related Documents"),("10.0","Effective Date")]),
]

APPROVAL = {
 1: "Board of Trustees", 2: "Board of Trustees", 3: "Board of Trustees",
 4: "Board of Trustees", 5: "Board of Trustees", 6: "Board of Trustees",
 7: "Board of Trustees", 8: "Board of Trustees", 9: "Board of Trustees",
 10: "Deputy Vice-Chancellor, Administration & Finance", 11: "University Senate",
}

VERSION_EFFECTIVE_REVIEW = ("1.0", "1 January 2028", "Annual")

CONTENT = {}

CONTENT[1] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to ensure full, definitive, and binding compliance with the Family Educational Rights and Privacy Act (FERPA) regarding all student education records maintained by Al-Mulk International University.

**1.2** This Policy serves as the binding institutional rule for all FERPA-related matters and ensures:

**1.2.1** That all student education records are protected in accordance with federal law;

**1.2.2** That no person discloses student records without proper authorization;

**1.2.3** That students are informed of their rights under FERPA;

**1.2.4** That the University maintains accurate and complete records of all disclosures;

**1.2.5** That all University personnel are trained on FERPA compliance;

**1.2.6** That the University complies with all applicable state and federal privacy laws.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All students of Al-Mulk International University;

**2.1.2** All education records maintained by the University;

**2.1.3** All faculty, staff, and administrators;

**2.1.4** All third-party vendors who have access to student records;

**2.1.5** Any person acting on behalf of the University in handling student records.

**2.2 Jurisdictional Reach.** This Policy applies to all student records, regardless of the medium in which they are stored or the location of the student.

**2.3** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 FERPA.** The Family Educational Rights and Privacy Act of 1974 (20 U.S.C. § 1232g), as amended.

**3.2 Education Record.** Any record, file, document, or other material that contains information directly related to a student and is maintained by the University. This includes, but is not limited to:

**3.2.1** Admissions records;

**3.2.2** Academic records (transcripts, grades, class schedules);

**3.2.3** Disciplinary records;

**3.2.4** Financial aid records;

**3.2.5** Medical records maintained by the University;

**3.2.6** Personal notes about students made by faculty or staff.

**3.3 Directory Information.** Information that may be disclosed without consent, including:

**3.3.1** Student's name;

**3.3.2** Address;

**3.3.3** Telephone number;

**3.3.4** Email address;

**3.3.5** Dates of attendance;

**3.3.6** Program of study;

**3.3.7** Degrees and awards received;

**3.3.8** Student ID number (not Social Security number).

**3.4 Eligible Student.** A student who has reached eighteen years of age or is attending a postsecondary institution.

**3.5 Legitimate Educational Interest.** The need to review an education record in order to fulfill a professional responsibility.

**3.6 Disclosure.** The release of information from an education record.

**3.7 Consent.** Written permission from the eligible student to disclose education records.

**3.8 FERPA Violation.** Any unauthorized disclosure of student education records.

## 4.0 Policy Statement

**4.1** The University shall comply fully with FERPA in all matters relating to student education records.

**4.2** No person shall disclose any student education record without proper authorization.

**4.3** No person shall access any student education record without a legitimate educational interest.

**4.4** No person shall use student education records for any purpose other than the legitimate educational purpose for which access was granted.

**4.5** No person shall share student education records with unauthorized individuals or entities.

**4.6** No person shall fail to report a suspected FERPA violation.

**4.7** No person shall destroy or alter student education records without authorization.

**4.8** No person shall knowingly provide false or misleading information regarding student records.

## 5.0 Student Rights Under FERPA

**5.1** Students have the right to:

**5.1.1** Inspect and review their education records within 45 days of the request;

**5.1.2** Request amendment of their education records if they believe records are inaccurate or misleading;

**5.1.3** Consent to disclosures of personally identifiable information contained in their education records;

**5.1.4** File a complaint with the U.S. Department of Education concerning alleged failures by the University to comply with FERPA.

**5.2** No person shall deny a student the right to inspect their records.

**5.3** No person shall prevent a student from filing a complaint.

## 6.0 Access to Education Records

**6.1 Who May Access**

**6.1.1** The following persons may access student education records without consent:

**6.1.1.1** University officials with a legitimate educational interest;

**6.1.1.2** The student themselves;

**6.1.1.3** Authorized representatives of the U.S. Department of Education;

**6.1.1.4** In connection with financial aid for which the student has applied;

**6.1.1.5** Accrediting organizations;

**6.1.1.6** Compliance with a judicial order or lawfully issued subpoena;

**6.1.1.7** Health and safety emergencies;

**6.1.1.8** Parents of dependent students as defined by the IRS.

**6.1.2** No person shall access student records without authorization.

**6.2 Legitimate Educational Interest**

**6.2.1** A legitimate educational interest exists when:

**6.2.1.1** The information is necessary for the performance of the person's job duties;

**6.2.1.2** The information is needed to provide services to the student;

**6.2.1.3** The information is needed to fulfill the person's professional responsibilities.

**6.2.2** No person shall claim a legitimate educational interest without proper justification.

## 7.0 Disclosure of Education Records

**7.1 Directory Information**

**7.1.1** The University may disclose directory information without consent.

**7.1.2** Students may opt out of the disclosure of directory information by notifying the Registrar in writing.

**7.1.3** No person shall disclose directory information after a student has opted out.

**7.2 Consent Requirements**

**7.2.1** Written consent is required for the disclosure of non-directory information.

**7.2.2** The consent shall:

**7.2.2.1** Specify the records to be disclosed;

**7.2.2.2** State the purpose of the disclosure;

**7.2.2.3** Identify the party to whom the disclosure is to be made.

**7.2.3** No person shall disclose non-directory information without proper consent.

**7.3 Record of Disclosures**

**7.3.1** The University shall maintain a record of all disclosures of education records.

**7.3.2** The record shall include:

**7.3.2.1** The date of the disclosure;

**7.3.2.2** The reason for the disclosure;

**7.3.2.3** The identity of the person to whom the disclosure was made.

**7.3.3** No person shall fail to document a disclosure.

## 8.0 Amendment of Records

**8.1** Students may request amendment of their education records if they believe records are inaccurate or misleading.

**8.2** The request shall be submitted in writing to the Registrar.

**8.3** If the University denies the request, the student has the right to:

**8.3.1** A hearing;

**8.3.2** Place a statement in the record explaining the student's position.

**8.4** No person shall deny a student the right to request amendment.

## 9.0 Training Requirements

**9.1** All faculty, staff, and administrators shall receive training on FERPA compliance annually.

**9.2** Training shall include:

**9.2.1** FERPA requirements;

**9.2.2** Student rights;

**9.2.3** Proper handling of education records;

**9.2.4** Consequences of violations.

**9.3** No person shall handle student records without training.

## 10.0 Handling FERPA Scenarios

**10.1 Scenario A: Parent Request for Records**

**10.1.1** When a parent requests a student's education records:

**10.1.1.1** Verify that the parent has the student's consent;

**10.1.1.2** If the student is a dependent for tax purposes, the parent may have access;

**10.1.1.3** If not, the request shall be denied.

**10.1.2** No person shall disclose records without proper verification.

**10.2 Scenario B: Subpoena for Records**

**10.2.1** When a subpoena is received:

**10.2.1.1** Forward to the Office of Legal Counsel immediately;

**10.2.1.2** Comply only with a valid subpoena;

**10.2.1.3** Notify the student before compliance if possible.

**10.2.2** No person shall respond to a subpoena without legal review.

**10.3 Scenario C: Directory Information Request**

**10.3.1** When a third party requests directory information:

**10.3.1.1** Verify that the student has not opted out;

**10.3.1.2** Provide only directory information;

**10.3.1.3** No person shall disclose non-directory information.

**10.4 Scenario D: Student Inspection Request**

**10.4.1** When a student requests to inspect their records:

**10.4.1.1** Schedule an inspection within 45 days;

**10.4.1.2** Provide access to the records;

**10.4.1.3** Allow the student to make copies if requested.

**10.4.2** No person shall deny a student's right to inspect records.

## 11.0 Enforcement

**11.1** No person shall violate any provision of this Policy.

**11.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**11.3** The University Registrar shall ensure compliance with this Policy.

**11.4** Students may file complaints with the U.S. Department of Education.

## 12.0 Related Documents

**12.1** Data Privacy & Security Policy (OPS-016)

**12.2** GDPR Compliance Policy (LEG-002)

**12.3** Student Policies Handbook

## 13.0 Effective Date

**13.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[2] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to ensure full, definitive, and binding compliance with the General Data Protection Regulation (GDPR) for all personal data of EU citizens processed by Al-Mulk International University.

**1.2** This Policy serves as the binding institutional rule for all GDPR-related matters and ensures:

**1.2.1** That all personal data of EU citizens is protected in accordance with GDPR requirements;

**1.2.2** That no person processes personal data without proper legal basis;

**1.2.3** That data subjects are informed of their rights under GDPR;

**1.2.4** That the University maintains accurate records of all data processing activities;

**1.2.5** That data breaches are reported in accordance with GDPR requirements;

**1.2.6** That the University complies with all applicable data protection laws.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All personal data of EU citizens processed by the University;

**2.1.2** All faculty, staff, and administrators;

**2.1.3** All third-party vendors who process personal data on behalf of the University;

**2.1.4** Any person acting on behalf of the University in processing personal data.

**2.2 Jurisdictional Reach.** This Policy applies to all personal data of EU citizens, regardless of where the data is processed or stored.

**2.3** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 GDPR.** The General Data Protection Regulation (Regulation (EU) 2016/679).

**3.2 Personal Data.** Any information relating to an identified or identifiable natural person.

**3.3 Data Subject.** The individual to whom personal data relates.

**3.4 Data Controller.** The entity that determines the purposes and means of processing personal data.

**3.5 Data Processor.** The entity that processes personal data on behalf of the controller.

**3.6 Processing.** Any operation performed on personal data.

**3.7 Data Breach.** A breach of security leading to accidental or unlawful destruction, loss, alteration, unauthorized disclosure of, or access to personal data.

**3.8 Consent.** Freely given, specific, informed, and unambiguous indication of the data subject's wishes.

**3.9 DPO.** Data Protection Officer, appointed to oversee GDPR compliance.

## 4.0 Policy Statement

**4.1** The University shall comply fully with GDPR in all matters relating to personal data of EU citizens.

**4.2** No person shall process personal data without a proper legal basis.

**4.3** No person shall disclose personal data without proper authorization.

**4.4** No person shall fail to report a data breach.

**4.5** No person shall destroy or alter personal data without authorization.

**4.6** No person shall knowingly provide false or misleading information regarding personal data.

## 5.0 Data Protection Principles

**5.1** The University shall process personal data in accordance with the following principles:

**5.1.1 Lawfulness, Fairness, and Transparency.** Data shall be processed lawfully, fairly, and transparently;

**5.1.2 Purpose Limitation.** Data shall be collected for specified, explicit, and legitimate purposes;

**5.1.3 Data Minimization.** Data shall be adequate, relevant, and limited to what is necessary;

**5.1.4 Accuracy.** Data shall be accurate and kept up to date;

**5.1.5 Storage Limitation.** Data shall be kept in a form that permits identification for no longer than necessary;

**5.1.6 Integrity and Confidentiality.** Data shall be processed in a manner that ensures appropriate security.

## 6.0 Lawful Basis for Processing

**6.1** Processing shall be lawful only if one of the following applies:

**6.1.1** The data subject has given consent;

**6.1.2** Processing is necessary for the performance of a contract;

**6.1.3** Processing is necessary for compliance with a legal obligation;

**6.1.4** Processing is necessary to protect vital interests;

**6.1.5** Processing is necessary for the performance of a task carried out in the public interest;

**6.1.6** Processing is necessary for legitimate interests pursued by the controller.

**6.2** No person shall process personal data without a lawful basis.

## 7.0 Data Subject Rights

**7.1** Data subjects have the following rights:

**7.1.1 Right to be Informed.** The right to know how their data is being processed;

**7.1.2 Right of Access.** The right to access their personal data;

**7.1.3 Right to Rectification.** The right to have inaccurate data corrected;

**7.1.4 Right to Erasure.** The right to have data deleted in certain circumstances;

**7.1.5 Right to Restrict Processing.** The right to restrict processing in certain circumstances;

**7.1.6 Right to Data Portability.** The right to receive data in a portable format;

**7.1.7 Right to Object.** The right to object to processing in certain circumstances.

**7.2** No person shall deny a data subject their rights.

## 8.0 Data Breach Response

**8.1** When a data breach is suspected:

**8.1.1** Report to the DPO immediately;

**8.1.2** Contain the breach;

**8.1.3** Investigate the cause;

**8.1.4** Notify affected data subjects if there is a high risk;

**8.1.5** Report to the supervisory authority within 72 hours.

**8.2** No person shall fail to report a data breach.

## 9.0 Enforcement

**9.1** No person shall violate any provision of this Policy.

**9.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**9.3** The Director, Information Technology shall ensure compliance with this Policy.

## 10.0 Related Documents

**10.1** Data Privacy & Security Policy (OPS-016)

**10.2** FERPA Compliance Policy (LEG-001)

## 11.0 Effective Date

**11.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[3] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for all required state filings, deadlines, and compliance procedures.

**1.2** This Policy ensures:

**1.2.1** That all required state filings are submitted on time;

**1.2.2** That the University maintains good standing with the State of Texas;

**1.2.3** That no person fails to file required documents;

**1.2.4** That the University complies with all applicable state laws and regulations.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University;

**2.1.2** All required state filings;

**2.1.3** All personnel responsible for filings.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 State Filing.** Any document required to be filed with the State of Texas.

**3.2 Good Standing.** The status of the University as a compliant entity.

**3.3 Registered Agent.** The individual or entity authorized to accept legal service.

## 4.0 Policy Statement

**4.1** The University shall file all required state documents on time.

**4.2** No person shall fail to file required documents.

**4.3** No person shall submit inaccurate filings.

**4.4** The Office of Legal Counsel shall ensure compliance.

## 5.0 Required Filings

**5.1 Certificate of Formation**

**5.1.1** The Certificate of Formation establishes the University as a Texas Nonprofit Religious Educational Corporation.

**5.1.2** Amendments shall be filed as needed.

**5.1.3** No person shall make changes without Board approval.

**5.2 Texas State Tax-Exemption Application**

**5.2.1** Form AP-204 shall be filed after federal 501(c)(3) approval.

**5.2.2** No person shall fail to file the exemption application.

**5.3 TWC Chapter 132 Religious Exemption**

**5.3.1** The religious exemption registration shall be maintained.

**5.3.2** No person shall fail to maintain the exemption.

**5.4 THECB Certificate of Authorization**

**5.4.1** The Certificate of Authorization shall be obtained before offering degrees.

**5.4.2** No person shall offer degrees without authorization.

**5.5 Annual Filings**

**5.5.1** Annual Texas nonprofit filings shall be submitted.

**5.5.2** Public Information Reports shall be filed.

**5.5.3** No person shall fail to file annual reports.

## 6.0 Deadlines

**6.1** Deadlines shall be tracked by the Office of Legal Counsel.

**6.2** Reminders shall be sent at least 30 days before deadlines.

**6.3** No person shall miss a filing deadline.

## 7.0 Enforcement

**7.1** No person shall fail to comply with this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Office of Legal Counsel shall ensure compliance.

## 8.0 Related Documents

**8.1** Certificate of Formation (GOV-004)

**8.2** Bylaws (GOV-003)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[4] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for the ownership, use, and protection of intellectual property created within the University.

**1.2** This Policy ensures:

**1.2.1** Clear ownership of intellectual property;

**1.2.2** Protection of the University's intellectual property rights;

**1.2.3** Compliance with applicable intellectual property laws;

**1.2.4** That no person infringes on intellectual property rights.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University;

**2.1.2** All intellectual property created by University personnel;

**2.1.3** All intellectual property used by the University.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Intellectual Property.** Creations of the mind, including copyrights, trademarks, patents, and trade secrets.

**3.2 Copyright.** The exclusive right to reproduce, distribute, and display a work.

**3.3 Trademark.** A word, symbol, or design that identifies goods or services.

**3.4 Patent.** The exclusive right to make, use, or sell an invention.

**3.5 Work Made for Hire.** Work created by an employee within the scope of employment.

## 4.0 Policy Statement

**4.1** The University shall protect its intellectual property rights.

**4.2** No person shall infringe on intellectual property rights.

**4.3** No person shall use University intellectual property without authorization.

## 5.0 Ownership

**5.1 University-Owned Works**

**5.1.1** Works created by employees within the scope of employment are owned by the University.

**5.1.2** Works created using University resources may be owned by the University.

**5.1.3** No person shall claim ownership of University-owned works.

**5.2 Faculty-Owned Works**

**5.2.1** Scholarly works, including publications, are owned by the faculty member.

**5.2.2** However, the University has a license to use such works.

**5.2.3** No person shall prevent the University from using scholarly works.

**5.3 Student-Owned Works**

**5.3.1** Works created by students are owned by the student.

**5.3.2** However, the University has a license to use such works for educational purposes.

**5.3.3** No person shall prevent the University from using student works for educational purposes.

## 6.0 Use and Protection

**6.1** University intellectual property shall be protected by:

**6.1.1** Copyright registration;

**6.1.2** Trademark registration;

**6.1.3** Patent filing;

**6.1.4** Confidentiality agreements.

**6.2** No person shall disclose confidential intellectual property.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Office of Legal Counsel shall ensure compliance.

## 8.0 Related Documents

**8.1** Employee Contract Template (OPS-009)

**8.2** Research Policy (WAQ-004)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[5] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to ensure full, definitive, and binding compliance with non-discrimination laws and Title IX requirements.

**1.2** This Policy ensures:

**1.2.1** That no person is discriminated against on the basis of protected status;

**1.2.2** That no person engages in harassment or sexual misconduct;

**1.2.3** That all complaints are investigated promptly and fairly;

**1.2.4** That the University complies with all applicable laws.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All students, faculty, and staff;

**2.1.2** All programs and activities;

**2.1.3** All visitors and third parties.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Discrimination.** Unfavorable treatment based on protected status.

**3.2 Harassment.** Unwelcome conduct based on protected status.

**3.3 Sexual Harassment.** Unwelcome sexual advances, requests for sexual favors, and other verbal or physical conduct of a sexual nature.

**3.4 Title IX.** Federal law prohibiting sex discrimination in education.

**3.5 Protected Status.** Race, color, national origin, sex, disability, age, religion, or other protected categories.

## 4.0 Policy Statement

**4.1** The University shall not discriminate on the basis of protected status.

**4.2** No person shall discriminate against any person.

**4.3** No person shall engage in harassment or sexual misconduct.

**4.4** All complaints shall be investigated promptly and fairly.

## 5.0 Prohibited Conduct

**5.1** Discrimination is prohibited in:

**5.1.1** Admissions;

**5.1.2** Employment;

**5.1.3** Academic programs;

**5.1.4** Activities.

**5.2** Harassment is prohibited, including:

**5.2.1** Verbal harassment;

**5.2.2** Physical harassment;

**5.2.3** Sexual harassment;

**5.2.4** Cyber harassment.

**5.3** Retaliation is prohibited.

## 6.0 Title IX Compliance

**6.1** The University shall comply with Title IX requirements.

**6.2** The University shall appoint a Title IX Coordinator.

**6.3** The Title IX Coordinator shall:

**6.3.1** Receive and investigate complaints;

**6.3.2** Provide training;

**6.3.3** Ensure compliance.

**6.4** No person shall interfere with the Title IX Coordinator.

## 7.0 Handling Discrimination Scenarios

**7.1 Scenario A: Discrimination Complaint**

**7.1.1** When a complaint is received:

**7.1.1.1** Acknowledge receipt within 5 days;

**7.1.1.2** Investigate within 30 days;

**7.1.1.3** Provide a written decision;

**7.1.1.4** Notify the complainant of appeal rights.

**7.1.2** No person shall fail to investigate a complaint.

**7.2 Scenario B: Sexual Harassment Complaint**

**7.2.1** When a sexual harassment complaint is received:

**7.2.1.1** Notify the Title IX Coordinator immediately;

**7.2.1.2** Provide supportive measures;

**7.2.1.3** Investigate promptly;

**7.2.1.4** Provide a written decision.

**7.2.2** No person shall retaliate against a complainant.

**7.3 Scenario C: Retaliation Complaint**

**7.3.1** When a retaliation complaint is received:

**7.3.1.1** Investigate promptly;

**7.3.1.2** Take corrective action;

**7.3.1.3** Protect the complainant.

**7.3.2** No person shall engage in retaliation.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance.

## 9.0 Related Documents

**9.1** Student Code of Conduct (STU-001)

**9.2** HR Policies & Procedures Manual (OPS-007)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[6] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for the establishment and operation of the Gambia branch campus.

**1.2** This Policy ensures:

**1.2.1** Legal compliance with Gambian laws and regulations;

**1.2.2** Successful establishment of the branch campus;

**1.2.3** That no person operates outside the legal framework;

**1.2.4** That the branch campus maintains academic quality and integrity.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The Gambia branch campus;

**2.1.2** All personnel at the branch campus;

**2.1.3** All activities of the branch campus.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Gambia Branch Campus.** The University's branch campus in The Gambia.

**3.2 NAQAA.** The National Accreditation and Quality Assurance Authority of The Gambia.

**3.3 GNQF.** The Gambia National Qualifications Framework.

## 4.0 Policy Statement

**4.1** The Gambia branch campus shall operate in compliance with Gambian law.

**4.2** No person shall operate outside the legal framework.

**4.3** No person shall offer programs without accreditation.

## 5.0 Registration and Licensing

**5.1** The Gambia branch campus shall be registered with:

**5.1.1** The Registrar of Companies, Banjul;

**5.1.2** NAQAA;

**5.1.3** Other relevant regulatory bodies.

**5.2** No person shall operate without proper registration.

## 6.0 Accreditation

**6.1** The branch campus shall pursue NAQAA accreditation.

**6.2** Accreditation shall be maintained.

**6.3** No person shall offer programs without accreditation.

## 7.0 Operations

**7.1** The branch campus shall:

**7.1.1** Maintain academic quality;

**7.1.2** Comply with local laws;

**7.1.3** Report to the University Senate.

**7.2** No person shall compromise academic quality.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance.

## 9.0 Related Documents

**9.1** Country-Specific Regulatory Compliance (LEG-008)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[7] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for the establishment of the Nigeria Mega-University campus.

**1.2** This Policy ensures:

**1.2.1** Legal compliance with Nigerian laws and regulations;

**1.2.2** Successful establishment of the campus;

**1.2.3** That no person operates outside the legal framework.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The Nigeria campus;

**2.1.2** All personnel at the campus;

**2.1.3** All activities of the campus.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Nigeria Campus.** The University's Mega-University campus in Nigeria.

**3.2 CAMA.** The Companies and Allied Matters Act of Nigeria.

**3.3 CAC.** The Corporate Affairs Commission of Nigeria.

**3.4 NUC.** The National Universities Commission of Nigeria.

## 4.0 Policy Statement

**4.1** The Nigeria campus shall operate in compliance with Nigerian law.

**4.2** No person shall operate outside the legal framework.

**4.3** No person shall offer programs without NUC approval.

## 5.0 Registration and Licensing

**5.1** The Nigeria campus shall be registered with:

**5.1.1** The Corporate Affairs Commission (CAC);

**5.1.2** The National Universities Commission (NUC);

**5.1.3** Other relevant regulatory bodies.

**5.2** No person shall operate without proper registration.

## 6.0 NUC Charter Application

**6.1** The University shall apply for a charter from the NUC.

**6.2** The application shall be submitted by Year 10 (2037).

**6.3** No person shall submit incomplete applications.

## 7.0 Site Acquisition and Construction

**7.1** Site acquisition shall begin in Year 7.

**7.2** Construction shall follow Nigerian regulations.

**7.3** No person shall acquire land without proper documentation.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance.

## 9.0 Related Documents

**9.1** Country-Specific Regulatory Compliance (LEG-008)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[8] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for compliance with the laws of all countries in which the University operates.

**1.2** This Policy ensures:

**1.2.1** Legal compliance in all jurisdictions;

**1.2.2** That no person violates international laws;

**1.2.3** That the University maintains its reputation and integrity.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** The entire University;

**2.1.2** All international operations;

**2.1.3** All personnel.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Country-Specific Compliance.** Compliance with the laws of each country of operation.

**3.2 Sanctions.** Economic or trade restrictions imposed by governments.

**3.3 Anti-Corruption.** Laws prohibiting bribery and corruption.

## 4.0 Policy Statement

**4.1** The University shall comply with the laws of all countries of operation.

**4.2** No person shall violate international laws.

**4.3** No person shall engage in corrupt practices.

## 5.0 Compliance Requirements

**5.1** Compliance shall include:

**5.1.1** Registration and licensing;

**5.1.2** Tax compliance;

**5.1.3** Employment law compliance;

**5.1.4** Data protection compliance;

**5.1.5** Anti-corruption compliance.

**5.2** No person shall fail to comply with local laws.

## 6.0 Handling Compliance Scenarios

**6.1 Scenario A: New Jurisdiction**

**6.1.1** When entering a new jurisdiction:

**6.1.1.1** Conduct a legal review;

**6.1.1.2** Identify all requirements;

**6.1.1.3** Obtain necessary approvals.

**6.1.2** No person shall operate without legal review.

**6.2 Scenario B: Regulatory Change**

**6.2.1** When regulations change:

**6.2.1.1** Monitor changes;

**6.2.1.2** Assess impact;

**6.2.1.3** Implement changes.

**6.2.2** No person shall ignore regulatory changes.

**6.3 Scenario C: Sanctions**

**6.3.1** When sanctions apply:

**6.3.1.1** Identify affected activities;

**6.3.1.2** Cease prohibited activities;

**6.3.1.3** Report to authorities.

**6.3.2** No person shall violate sanctions.

## 7.0 Enforcement

**7.1** No person shall violate any provision of this Policy.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Office of Legal Counsel shall ensure compliance.

## 8.0 Related Documents

**8.1** Gambia Branch Operational Plan (LEG-006)

**8.2** Nigeria Campus Development Plan (LEG-007)

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[9] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for cross-border payment processing, currency conversion, and compliance for international students.

**1.2** This Policy ensures:

**1.2.1** Efficient and secure cross-border payments;

**1.2.2** Compliance with all applicable laws and regulations;

**1.2.3** That no person engages in fraudulent payment activities;

**1.2.4** That students have convenient payment options.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All international payments;

**2.1.2** All students;

**2.1.3** All personnel handling payments.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Cross-Border Payment.** A payment made from one country to another.

**3.2 Currency Conversion.** The exchange of one currency for another.

**3.3 Payment Gateway.** A service that processes payments.

**3.4 Sanctions.** Government-imposed restrictions on financial transactions.

## 4.0 Policy Statement

**4.1** Cross-border payments shall be processed securely and efficiently.

**4.2** No person shall engage in fraudulent payment activities.

**4.3** No person shall violate sanctions.

## 5.0 Payment Gateways

**5.1** The University shall maintain multiple payment gateways:

**5.1.1** Credit and debit cards (Visa, Mastercard);

**5.1.2** Digital payment platforms (PayPal, Flutterwave, Paystack);

**5.1.3** Mobile money services (M-Pesa);

**5.1.4** Bank transfers and wire transfers.

**5.2** No person shall process payments through unauthorized gateways.

## 6.0 Currency Conversion

**6.1** Payments shall be made in United States Dollars (USD).

**6.2** Currency conversion shall be at the prevailing exchange rate.

**6.3** No person shall manipulate exchange rates.

## 7.0 Sanctions Compliance

**7.1** Payments shall comply with all applicable sanctions.

**7.2** No person shall process payments from sanctioned countries.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Deputy Vice-Chancellor, Administration & Finance shall ensure compliance.

## 9.0 Related Documents

**9.1** Tuition Collection & Refund Policy (OPS-005)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[10] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for the recruitment and support of international faculty.

**1.2** This Policy ensures:

**1.2.1** Legal compliance with immigration laws;

**1.2.2** Fair and equitable recruitment;

**1.2.3** Successful integration of international faculty;

**1.2.4** That no person violates immigration laws.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All international faculty recruitment;

**2.1.2** All international faculty;

**2.1.3** All personnel involved in recruitment.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 International Faculty.** Faculty members who are not citizens or permanent residents of the United States.

**3.2 Visa.** Authorization to enter and work in a country.

**3.3 Work Authorization.** Permission to work in a country.

## 4.0 Policy Statement

**4.1** International faculty recruitment shall comply with all applicable laws.

**4.2** No person shall violate immigration laws.

**4.3** No person shall engage in discriminatory recruitment.

## 5.0 Recruitment Process

**5.1** The recruitment process shall include:

**5.1.1** Job posting;

**5.1.2** Application review;

**5.1.3** Interviews;

**5.1.4** Background checks;

**5.1.5** Visa sponsorship.

**5.2** No person shall hire without proper authorization.

## 6.0 Visa and Work Authorization

**6.1** The University shall sponsor work visas for international faculty.

**6.2** Compliance with immigration laws is mandatory.

**6.3** No person shall work without proper authorization.

## 7.0 Relocation and Support

**7.1** Relocation support shall include:

**7.1.1** Visa assistance;

**7.1.2** Housing assistance;

**7.1.3** Cultural orientation.

**7.2** No person shall be denied relocation support.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Director, Human Resources shall ensure compliance.

## 9.0 Related Documents

**9.1** Recruitment & Hiring Policy (OPS-008)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[11] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive framework for the support of international students.

**1.2** This Policy ensures:

**1.2.1** Legal compliance with immigration laws;

**1.2.2** Successful integration of international students;

**1.2.3** Academic success;

**1.2.4** That no student is denied support.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All international students;

**2.1.2** All personnel supporting international students.

**2.2** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 International Student.** A student who is not a citizen or permanent resident of the United States.

**3.2 Visa.** Authorization to enter and study in a country.

**3.3 SEVIS.** Student and Exchange Visitor Information System.

## 4.0 Policy Statement

**4.1** The University shall provide support services to international students.

**4.2** No student shall be denied support.

**4.3** No person shall violate immigration laws.

## 5.0 Support Services

**5.1** Support services shall include:

**5.1.1** Visa assistance;

**5.1.2** Pre-arrival information;

**5.1.3** Cultural adjustment support;

**5.1.4** Academic support;

**5.1.5** Financial support.

**5.2** No student shall be denied support.

## 6.0 Visa and SEVIS Compliance

**6.1** The University shall comply with SEVIS requirements.

**6.2** No person shall violate immigration laws.

## 7.0 Handling International Student Scenarios

**7.1 Scenario A: Visa Issues**

**7.1.1** When a student has visa issues:

**7.1.1.1** Provide support;

**7.1.1.2** Refer to appropriate resources;

**7.1.1.3** Advocate for the student.

**7.1.2** No student shall be abandoned.

**7.2 Scenario B: Cultural Adjustment**

**7.2.1** When a student struggles with cultural adjustment:

**7.2.1.1** Provide counseling;

**7.2.1.2** Offer support groups;

**7.2.1.3** Organize cultural events.

**7.2.2** No student shall be ignored.

**7.3 Scenario C: Discrimination**

**7.3.1** When a student alleges discrimination:

**7.3.1.1** Investigate;

**7.3.1.2** Take corrective action;

**7.3.1.3** Support the student.

**7.3.2** No person shall engage in discrimination.

## 8.0 Enforcement

**8.1** No person shall violate any provision of this Policy.

**8.2** Violation of this Policy shall result in disciplinary action.

**8.3** The Dean of Students shall ensure compliance.

## 9.0 Related Documents

**9.1** International Student Support Policy (STU-013)

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
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
