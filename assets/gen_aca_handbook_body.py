#!/usr/bin/env python3
"""Author work_aca_handbook_body.md — the 19-policy body of the AMIU Academic
Handbook (Doc Codes ACA-001 through ACA-019), the fourth AMIU flagship
publication, in the same navy/gold editorial system as the Blueprint,
Constitution, and Institutional Governance Compendium.

Source: the 19 fully-drafted ACA policies supplied by the user, transcribed
here with the fixes found during the editorial review applied directly
(not just noted) — see the Publication Certification Statement in
assets/aca_handbook_back.md for what each fix was and why.
"""

OUT = "/home/user/shroyalschools/work_aca_handbook_body.md"

# ---------------------------------------------------------------------------
# Divider generator (mirrors gen_igc_body.py's divider() pattern)
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
      <w:r><w:rPr><w:rFonts w:ascii="Archivo" w:hAnsi="Archivo"/><w:color w:val="8C97AB"/><w:sz w:val="17"/><w:spacing w:val="26"/></w:rPr><w:t>ACADEMIC HANDBOOK &#183; POLICY {num} OF 19</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces Black" w:hAnsi="Fraunces Black"/><w:color w:val="B08625"/><w:b/><w:sz w:val="72"/></w:rPr><w:t>{code}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="120" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces Black" w:hAnsi="Fraunces Black"/><w:color w:val="FFFFFF"/><w:b/><w:sz w:val="{tsize*2}"/></w:rPr><w:t>{esc(title)}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="260"/><w:pBdr><w:bottom w:val="single" w:sz="10" w:space="8" w:color="B08625"/></w:pBdr></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Archivo" w:hAnsi="Archivo"/><w:color w:val="8C97AB"/><w:sz w:val="17"/><w:spacing w:val="14"/></w:rPr><w:t>POLICY STEWARD: {esc(steward.upper())}</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="360"/><w:ind w:right="700"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Fraunces" w:hAnsi="Fraunces"/><w:i/><w:color w:val="DCE3F0"/><w:sz w:val="24"/></w:rPr><w:t>&#8220;{esc(thesis)}&#8221;</w:t></w:r></w:p>''')
    rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="140"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Archivo" w:hAnsi="Archivo"/><w:color w:val="B08625"/><w:b/><w:sz w:val="16"/><w:spacing w:val="20"/></w:rPr><w:t>CONTENTS OF THIS POLICY</w:t></w:r></w:p>''')
    for sec_num, sec_title in section_titles:
        rows.append(f'''<w:p><w:pPr><w:spacing w:before="0" w:after="90"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Archivo SemiBold" w:hAnsi="Archivo SemiBold"/><w:color w:val="B08625"/><w:b/><w:sz w:val="17"/></w:rPr><w:t>{sec_num}&#8194;</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Archivo" w:hAnsi="Archivo"/><w:color w:val="FFFFFF"/><w:sz w:val="16"/></w:rPr><w:t>{esc(sec_title)}</w:t></w:r></w:p>''')
    body = "\n".join(rows)
    height = 10600 + min(len(section_titles), 12) * 175
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
# Policy metadata: (num, code, title, version, effective, review, approval,
#  steward, owner, authority, thesis, [(sec_num, sec_title), ...])
# Authority citations below are the CORRECTED versions — see the editorial
# review notes in assets/aca_handbook_back.md for what each replaced.
# ---------------------------------------------------------------------------
POLICIES = [
 (1, "ACA-001", "Academic Catalog", "President & Vice-Chancellor", "Office of the Registrar",
  "Constitution Article 10",
  "The Catalog in effect at enrollment is the binding contract between the University and every student it admits.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Contents of the Academic Catalog"),("6.0","Publication Process"),("7.0","Amendment Process"),
   ("8.0","Handling Catalog Issues"),("9.0","Student Responsibilities"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (2, "ACA-002", "Curriculum Development Process", "Deputy Vice-Chancellor, Academic Affairs", "Office of Academic Affairs",
  "Constitution Article 8, Section 8.1",
  "No course is taught, and no program admits a single student, before four levels of review say it is ready.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Proposal Requirements"),("6.0","Approval Process"),("7.0","Timeline"),
   ("8.0","Resource Allocation"),("9.0","Record Keeping"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (3, "ACA-003", "Program Assessment & Review Policy", "Deputy Vice-Chancellor, Academic Affairs", "Office of Institutional Research",
  "Constitution Article 8, Section 8.1",
  "Every program faces a self-study, an outside expert, and a five-year clock — or a teach-out plan when it fails to keep up.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Self-Study Requirements"),("6.0","External Review Requirements"),("7.0","Action Planning Requirements"),
   ("8.0","Program Closure and Teach-Out"),("9.0","Reporting Requirements"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (4, "ACA-004", "Course Syllabi Template", "Deputy Vice-Chancellor, Academic Affairs", "Office of Academic Affairs",
  "Constitution Article 8, Section 8.1",
  "The syllabus is a binding contract between instructor and student, not a formality — no course runs without one.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Required Syllabi Elements"),("6.0","Template"),("7.0","Submission and Approval"),
   ("8.0","Syllabus Changes"),("9.0","Student Access"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (5, "ACA-005", "Faculty Evaluation System", "Deputy Vice-Chancellor, Academic Affairs", "College Deans",
  "Constitution Article 13, Section 13.2",
  "Teaching, research, and service, weighted and documented every year — for every faculty member, with no exemption.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Evaluation Components"),("6.0","Evaluation Cycle"),("7.0","Promotion Criteria"),
   ("8.0","Part-Time and Adjunct Faculty Evaluation"),("9.0","Appeals"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (6, "ACA-006", "Course Evaluation System", "Deputy Vice-Chancellor, Academic Affairs", "Office of Institutional Research",
  "Constitution Article 8, Section 8.1",
  "Anonymous, mandatory, and analyzed every semester — student feedback that actually reaches the instructor.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Evaluation Instrument"),("6.0","Administration"),("7.0","Low Response Rates"),
   ("8.0","Analysis and Reporting"),("9.0","Use of Results"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (7, "ACA-007", "Academic Standards Committee Charter", "Chair, Academic Standards Committee", "Secretary to the Senate",
  "Constitution Article 8, Section 8.1",
  "Five faculty members hold the University's academic policy review, grade appeals, and integrity oversight in one charter.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Composition"),("6.0","Member Disqualification"),("7.0","Responsibilities"),
   ("8.0","Meetings"),("9.0","Reporting"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (8, "ACA-008", "Accreditation Preparation Plan", "Deputy Vice-Chancellor, Academic Affairs", "Office of Institutional Research",
  "Constitution Article 10",
  "A five-year roadmap from self-study to site visit — accreditation status the University discloses, never overstates.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Accreditation Goals"),("6.0","Self-Study Process"),("7.0","Site Visit Preparation"),
   ("8.0","Gap Analysis"),("9.0","Accreditation Status Disclosure"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (9, "ACA-009", "Transfer Credit Policy", "University Registrar", "Office of the Registrar",
  "Constitution Article 10",
  "Accredited source, a grade of C or better, and no more than half a program — the ceiling on what transfers in.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Evaluation Criteria"),("6.0","International Transfer Credit"),("7.0","Fraudulent Documents"),
   ("8.0","Evaluation Process"),("9.0","Appeals"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (10, "ACA-010", "Credit-Hour Definition Policy", "University Registrar", "Office of the Registrar",
  "Constitution Article 10, Section 10.1",
  "One hour of instruction, two hours of outside work, fifteen weeks — the Carnegie-standard unit every AMIU credential is built from.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","International Equivalency"),
   ("5.0","Contact Hour Verification"),("6.0","Enforcement"),("7.0","Related Documents"),
   ("8.0","Effective Date")]),
 (11, "ACA-011", "Academic Calendar Policy", "University Registrar", "Office of the Registrar",
  "Constitution Article 10",
  "Semester dates, deadlines, and the one office authorized to change them in an emergency.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Semester Dates"),
   ("5.0","Deadlines"),("6.0","Emergency Calendar Changes"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (12, "ACA-012", "Graduation Requirements Policy", "University Registrar", "Office of the Registrar",
  "Constitution Article 10, Section 10.1",
  "Credit hours, GPA, residency, and a completed application — nothing about graduation is granted by exception.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Credit Hour Requirements"),
   ("5.0","GPA Requirements"),("6.0","Residency Requirements"),("7.0","Dual Degrees"),
   ("8.0","Graduation with Honors"),("9.0","Application Process"),("10.0","Enforcement"),
   ("11.0","Related Documents"),("12.0","Effective Date")]),
 (13, "ACA-013", "Academic Integrity Policy", "Deputy Vice-Chancellor, Academic Affairs", "College Deans",
  "Constitution Article 8, Section 8.1",
  "Plagiarism, cheating, fabrication, AI misuse, and contract cheating — named explicitly, investigated, and sanctioned on an escalating scale.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Prohibited Conduct"),("6.0","Investigation Process"),("7.0","Sanctions"),
   ("8.0","Appeals"),("9.0","Enforcement"),("10.0","Related Documents"),("11.0","Effective Date")]),
 (14, "ACA-014", "Program Learning Outcomes Assessment Policy", "Deputy Vice-Chancellor, Academic Affairs", "Office of Institutional Research",
  "Constitution Article 8, Section 8.1",
  "A program that cannot show its students achieved its stated outcomes owes the Senate a remedial action plan, not an excuse.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Assessment Methods"),("6.0","Outcome Achievement Standards"),("7.0","Remedial Actions"),
   ("8.0","Reporting"),("9.0","Enforcement"),("10.0","Related Documents"),("11.0","Effective Date")]),
 (15, "ACA-015", "Online Attendance Policy", "Deputy Vice-Chancellor, Academic Affairs", "Office of Academic Affairs",
  "Constitution Article 10",
  "Seventy-five percent attendance, measured five different ways, with a real accommodation for power outages and emergencies.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Excused Absences"),("6.0","Consequences"),("7.0","Enforcement"),
   ("8.0","Related Documents"),("9.0","Effective Date")]),
 (16, "ACA-016", "Remote Proctoring & Online Examinations Policy", "Deputy Vice-Chancellor, Academic Affairs", "Office of Academic Affairs",
  "Constitution Article 8, Section 8.1",
  "A working webcam and microphone are the price of admission to an online exam; a financial-hardship waiver is the price of fairness.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Definitions"),("4.0","Policy Statement"),
   ("5.0","Prohibited Conduct"),("6.0","Proctoring Fees"),("7.0","Technical Assistance"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (17, "ACA-017", "Technology Requirements Policy", "Director, Information Technology", "Office of Information Technology",
  "Constitution Article 9, Section 9.4",
  "Minimum device and bandwidth standards, backed by grants and loaner equipment so no student is priced out by hardware.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Minimum Device Requirements"),
   ("5.0","Internet Connectivity"),("6.0","Technology Grants"),("7.0","Loaner Equipment"),
   ("8.0","Low-Bandwidth Accommodations"),("9.0","Enforcement"),("10.0","Related Documents"),
   ("11.0","Effective Date")]),
 (18, "ACA-018", "Synchronous/Asynchronous Learning Policy", "Deputy Vice-Chancellor, Academic Affairs", "Office of Academic Affairs",
  "Constitution Article 10",
  "No course is entirely live or entirely self-paced — every AMIU classroom balances both, with sessions recorded and time zones respected.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Synchronous Learning"),
   ("5.0","Asynchronous Learning"),("6.0","Recording Retention"),("7.0","Privacy of Recordings"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
 (19, "ACA-019", "Virtual Faculty & Student Support Policy", "Deputy Vice-Chancellor, Academic Affairs", "Office of Student Affairs",
  "Constitution Article 8, Section 8.1",
  "Advising, counseling, and disability services — available by video, phone, and chat, in more than one language, with crisis support every hour of the day.",
  [("1.0","Purpose"),("2.0","Scope"),("3.0","Policy Statement"),("4.0","Academic Advising"),
   ("5.0","Mental Health Support"),("6.0","Multilingual Support"),("7.0","Disability Services"),
   ("8.0","Enforcement"),("9.0","Related Documents"),("10.0","Effective Date")]),
]

APPROVAL = {
    "ACA-001": "University Senate", "ACA-002": "University Senate", "ACA-003": "University Senate",
    "ACA-004": "Academic Standards Committee", "ACA-005": "University Senate", "ACA-006": "University Senate",
    "ACA-007": "University Senate", "ACA-008": "University Senate", "ACA-009": "University Senate",
    "ACA-010": "University Senate", "ACA-011": "University Senate", "ACA-012": "University Senate",
    "ACA-013": "University Senate", "ACA-014": "University Senate", "ACA-015": "University Senate",
    "ACA-016": "University Senate", "ACA-017": "Deputy Vice-Chancellor, Academic Affairs",
    "ACA-018": "University Senate", "ACA-019": "University Senate",
}

CONTENT = {}

CONTENT[1] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the Academic Catalog as the official, definitive, and legally binding source of all academic information, policies, and requirements of Al-Mulk International University.

**1.2** This Policy ensures that:

**1.2.1** All academic programs, courses, policies, and requirements are published in a single, accessible, authoritative document;

**1.2.2** Students, faculty, and staff have a clear, consistent, and reliable reference for academic matters;

**1.2.3** The University meets all accreditation and regulatory requirements for transparency and consistency;

**1.2.4** No person may claim ignorance of academic policies as a defense for non-compliance, as the Catalog is the official record;

**1.2.5** The Catalog serves as a binding contract between the University and its students;

**1.2.6** The Catalog is the final authority on all academic matters.

## 2.0 Scope

**2.1** This Policy applies to:

**2.1.1** All students, including prospective, current, and former students;

**2.1.2** All faculty members, including full-time, part-time, and adjunct;

**2.1.3** All academic advisors and administrative staff;

**2.1.4** All academic departments, colleges, and programs;

**2.1.5** Any person acting on behalf of the University in academic matters.

**2.2** Jurisdictional Reach: The Academic Catalog governs all academic programs, courses, and policies, regardless of:

**2.2.1** Mode of delivery (online, hybrid, or in-person);

**2.2.2** Geographic location of the student or program;

**2.2.3** Tuition tier classification of the student.

**2.3** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 Academic Catalog:** The official, comprehensive, annually published document of the University containing all academic programs, courses, requirements, and policies. It serves as the binding contract between the University and its students.

**3.2 Catalog Year:** The academic year for which the Catalog is published, beginning 1 August and ending 31 July. Students are bound by the Catalog in effect at the time of their initial enrollment.

**3.3 Program:** A formally recognized course of study leading to a degree, diploma, or certificate.

**3.4 Course:** A unit of instruction with defined learning outcomes, credit hours, and assessment methods.

**3.5 Program Requirements:** The specific courses, credit hours, and other conditions that must be satisfied to complete a program.

**3.6 Academic Policy:** A rule or regulation governing academic affairs, as set forth in the Catalog.

**3.7 Binding Authority:** The Catalog is the official and enforceable source of all academic policies. No person may rely on verbal representations that conflict with the Catalog.

**3.8 Catalog Applicability:** Students are subject to the Catalog in effect at the time of their initial enrollment, but must comply with any changes to University-wide policies that apply to all students.

## 4.0 Policy Statement

**4.1** The Academic Catalog is the official, binding, and authoritative source of all academic information for Al-Mulk International University.

**4.2** The University shall publish an Academic Catalog annually, no later than 1 August of each academic year.

**4.3** The Academic Catalog shall be the sole and exclusive source of academic policies and requirements.

**4.4** All students are bound by the policies, requirements, and procedures set forth in the Academic Catalog in effect at the time of their enrollment.

**4.5** No person shall make any representation, verbal or written, that is inconsistent with the Academic Catalog.

**4.6** No person shall make any change to the Academic Catalog without prior approval from the University Senate.

**4.7** No person shall offer any course or program that is not listed in the Academic Catalog.

**4.8** No person shall award any degree or certificate that is not listed in the Academic Catalog.

**4.9** No person shall deviate from the Academic Catalog without prior written approval from the University Senate.

**4.10** No person shall claim ignorance of the Catalog as a defense for non-compliance.

**4.11** No person shall use an outdated Catalog version to claim entitlement to requirements that have been changed.

## 5.0 Contents of the Academic Catalog

**5.1** The Academic Catalog shall include the following sections, each of which is a binding and enforceable component of the Catalog:

**5.1.1 Institutional Identity** — legal name, seal, tagline, and official logo; mission and vision statements; core values and the ISLAMIC framework; history and founding date; accreditation status and legal domicile; religious exemption status.

**5.1.2 Admission Information** — general and program-specific admission requirements; application procedures and deadlines; transfer credit policies; international student admission requirements; tuition and fee schedules; scholarship and financial aid information.

**5.1.3 Academic Programs** — all undergraduate programs (Diploma, Associate, Bachelor); all graduate programs (PGD, Master, Ph.D., Post-Doctoral); program descriptions, objectives, and learning outcomes; program requirements and course sequences; credit-hour requirements; time-to-completion limits; capstone, thesis, or dissertation requirements.

**5.1.4 Course Offerings** — course descriptions; course codes and titles; credit hours; prerequisites and corequisites; learning objectives and outcomes; assessment methods.

**5.1.5 Academic Policies** — academic integrity policy; grading policy and GPA calculation; attendance policy; academic probation and dismissal policy; transfer credit policy; online learning policies; course withdrawal policy; grade appeal policy.

**5.1.6 Graduation Requirements** — credit-hour requirements by program; GPA requirements; capstone/thesis/dissertation requirements; residency requirements; application process and deadlines.

**5.1.7 Student Services** — academic advising; career services; mental health support; disability services; library and research support.

**5.1.8 University Governance** — Board of Trustees; University Senate; Administration; Faculty.

**5.1.9 Catalog Applicability and Disclaimers** — statement that the Catalog is a binding contract; statement that the University reserves the right to make changes; statement that students are responsible for knowing the Catalog; statement that verbal representations are not binding.

## 6.0 Publication Process

**6.1 Preparation.** The Office of the Registrar shall coordinate the preparation of the Academic Catalog. Academic departments shall submit program and course information to the Registrar's Office by 1 April of each year. No department shall fail to submit required information by the deadline.

**6.2 Review.** The draft Catalog shall be reviewed by the Curriculum Committee, which shall verify that all programs and courses meet academic standards and submit recommendations to the University Senate.

**6.3 Approval.** The University Senate shall approve the Academic Catalog by a simple majority vote. No Catalog shall be published without Senate approval.

**6.4 Publication.** The Catalog shall be published by 1 August of each year, available in PDF format, searchable HTML format, accessible formats for students with disabilities, and mobile-friendly format. All students and faculty shall be notified of the publication of the new Catalog.

## 7.0 Amendment Process

**7.1** Amendments to the Catalog shall follow the same approval process as the initial publication.

**7.2** Amendments shall be effective at the start of the next academic year.

**7.3** No person shall make any change to the Catalog without Senate approval.

**7.4** No person shall implement any change to a program or course that is inconsistent with the Catalog.

**7.5** All amendments shall be communicated to the University community within 14 days of approval.

## 8.0 Handling Catalog Issues

**8.1 Outdated Information.** If the Catalog contains incorrect information, the Office of the Registrar shall publish corrections promptly, investigate the cause of errors, and implement corrective measures to prevent future errors.

**8.2 Conflicting Requirements.** If the Catalog conflicts with other policies, the University Senate shall resolve the conflict; the resolution shall be documented, published, and the Catalog updated accordingly.

**8.3 Student Confusion.** If students are confused by Catalog content, the Office of the Registrar shall provide guidance and publish clarifications; the Catalog shall be reviewed for clarity.

**8.4 Accessibility Issues.** If the Catalog is not accessible, the Office of Information Technology shall provide support; accessibility standards shall be implemented, and the Catalog reviewed for compliance with ADA and Section 508 standards.

## 9.0 Student Responsibilities

**9.1** Students are responsible for reading and understanding the Academic Catalog; complying with all policies and requirements; seeking clarification from their academic advisor when needed; planning their course of study in accordance with the Catalog; and meeting all program requirements by the time of graduation.

**9.2** No student shall claim ignorance of the Catalog as a defense for failure to meet requirements.

**9.3** No student shall rely on verbal representations that are inconsistent with the Catalog.

## 10.0 Enforcement

**10.1** No person shall violate any provision of this Policy.

**10.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**10.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance with this Policy.

**10.4** The Office of the Registrar shall maintain records of all Catalog amendments.

## 11.0 Related Documents

Constitution Article 10; Student Handbook; Faculty Handbook; Curriculum Development Process (ACA-002); Graduation Requirements Policy (ACA-012).

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[2] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive process by which all new courses, programs, and significant modifications are proposed, reviewed, and approved.

**1.2** This Policy ensures that all academic offerings meet the University's standards of quality, rigor, and Islamic values; that no course or program is offered without proper review and approval; that all curriculum decisions are transparent, documented, and accountable; that resource allocation is appropriate and sustainable; that all offerings align with the University's mission and strategic goals and comply with accreditation standards; and that a teach-out plan exists for discontinued programs.

## 2.0 Scope

**2.1** This Policy applies to all faculty members and academic departments; all proposed new courses and programs; all significant modifications to existing courses and programs; all academic units responsible for curriculum development; and any person acting on behalf of the University in curriculum matters.

**2.2** Significant modifications include, but are not limited to: changes to program learning outcomes (25% or more); changes to core curriculum requirements (25% or more); changes to credit-hour requirements (25% or more); changes to program length or structure; changes to course content that significantly affect learning outcomes; changes to prerequisite or corequisite requirements; changes to delivery mode (online to in-person, or vice versa); and changes to program name or code.

**2.3** No person is exempt from the requirements of this Policy.

## 3.0 Definitions

**3.1 New Course:** A course that has not been previously offered by the University.

**3.2 New Program:** A program that has not been previously offered by the University.

**3.3 Curriculum Committee:** The standing committee responsible for curriculum review and approval.

**3.4 Program Modification:** A significant change to an existing program, as defined in Section 2.2.

**3.5 Course Modification:** A significant change to an existing course.

**3.6 Learning Outcomes:** The knowledge, skills, and abilities students are expected to gain.

**3.7 Proposal:** A formal written submission requesting approval for a new or modified course or program.

**3.8 Teach-Out Plan:** A plan to ensure that current students can complete a program that is being discontinued.

**3.9 Approval Authority:** The body with the authority to approve proposals, as specified in this Policy.

## 4.0 Policy Statement

**4.1** No person shall offer any new course, program, or significant modification without prior approval through the process set forth in this Policy.

**4.2** No person shall teach a course that has not been approved.

**4.3** No person shall admit students to a program that has not been approved.

**4.4** No person shall award a degree or certificate for a program that has not been approved.

**4.5** The Curriculum Committee shall ensure that all proposals meet academic quality standards; align with the University's mission and values; are adequately resourced; and are consistent with accreditation standards.

**4.6** All proposals shall be reviewed through four levels of approval: department review; college review; Curriculum Committee review; and University Senate approval.

**4.7** Programs that are discontinued shall have a teach-out plan approved by the Senate.

## 5.0 Proposal Requirements

**5.1 New Course Proposal.** All new course proposals shall include: course title and code; course description (minimum 150 words); learning objectives (minimum 3, maximum 7); credit hours; prerequisites and corequisites (if any); assessment methods; required texts and materials; faculty qualifications; resource requirements; justification for the course; alignment with program learning outcomes; and estimated student demand. No proposal shall be accepted without all required elements. The proposal shall be submitted to the department head.

**5.2 New Program Proposal.** All new program proposals shall include: program title and code; program description (minimum 250 words); program learning outcomes (minimum 5, maximum 10); credit hour requirements; course list and sequence; faculty qualifications; resource requirements (faculty, facilities, technology); market analysis and demand; alignment with the University's mission; accreditation considerations; budget and financial projections (3-year projections); risk assessment and mitigation plan; and a teach-out plan (if applicable). No proposal shall be accepted without all required elements. The proposal shall be submitted to the department head.

**5.3 Program or Course Modification.** All modification proposals shall include a description of the proposed change, rationale, impact on students and programs, resource implications, and an implementation timeline. No modification shall be implemented without approval.

**5.4 Program Discontinuation.** All program discontinuation proposals shall include the rationale for discontinuation, a teach-out plan for current students, a timeline, and a notification plan for students and faculty. No program shall be discontinued without Senate approval.

## 6.0 Approval Process

**6.1 Department Review.** The proposal shall be reviewed by the relevant department, which shall provide a written recommendation to the College Dean within fifteen business days. No proposal shall proceed without department recommendation.

**6.2 College Review.** The proposal shall be reviewed by the relevant College Dean, who shall provide a written recommendation to the Curriculum Committee within fifteen business days. No proposal shall proceed without College recommendation.

**6.3 Curriculum Committee Review.** The Committee shall assess academic quality, resource requirements, alignment with the University's mission, compliance with accreditation standards, and market demand and feasibility within thirty days, then provide a written recommendation to the University Senate. No proposal shall proceed without Committee recommendation.

**6.4 University Senate Approval.** The proposal shall be presented to the University Senate, which shall vote; approval requires a simple majority. Approved proposals shall be published in the Academic Catalog. No proposal shall be implemented without Senate approval.

## 7.0 Timeline

**7.1** Proposals shall be submitted at least sixty days before the semester in which they are to be offered.

**7.2** The review process shall be completed within forty-five days of submission.

**7.3** The University Senate shall vote on proposals within thirty days of the Curriculum Committee's recommendation.

**7.4** No person shall circumvent these timelines.

## 8.0 Resource Allocation

**8.1** New programs shall be funded in accordance with the University's budget process.

**8.2** The Office of Finance shall ensure that adequate resources are available before approval.

**8.3** No program shall be approved without a confirmed budget.

**8.4** No program shall be offered without adequate resources.

## 9.0 Record Keeping

**9.1** The Office of Academic Affairs shall maintain records of all curriculum proposals, including the original proposal, department recommendations, college recommendations, Curriculum Committee recommendations, and Senate approvals.

**9.2** Records shall be retained for a period of seven years.

**9.3** No person shall destroy or alter curriculum records.

## 10.0 Enforcement

**10.1** No person shall offer a new course or program without approval, or make significant modifications without approval, or circumvent the approval process.

**10.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**10.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance with this Policy.

## 11.0 Related Documents

Constitution Article 8; Academic Catalog (ACA-001); Academic Standards Committee Charter (ACA-007); Program Assessment & Review Policy (ACA-003).

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[3] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive process for the systematic evaluation and continuous improvement of all academic programs.

**1.2** This Policy ensures that all academic programs are regularly reviewed and assessed for quality, effectiveness, and relevance; that no program continues without periodic review; that findings result in actionable improvements; that the University meets accreditation and regulatory requirements; that student learning outcomes are achieved and continuously improved; and that a teach-out plan exists for programs identified for closure.

## 2.0 Scope

**2.1** This Policy applies to all academic programs offered by the University, including undergraduate, graduate, and professional programs; all faculty and staff involved in program delivery; all academic departments and colleges; and any person acting on behalf of the University in program review matters.

**2.2** No program is exempt from assessment and review.

## 3.0 Definitions

**3.1 Program Assessment:** The systematic collection and analysis of data on program performance, including student learning outcomes, enrollment, graduation rates, employment outcomes, and student satisfaction.

**3.2 Program Review:** The comprehensive evaluation of an academic program, including self-study, external review, and action planning.

**3.3 Self-Study:** The program's own evaluation conducted by program faculty, analyzing strengths, weaknesses, opportunities, and threats.

**3.4 External Reviewer:** An expert from outside the University who evaluates the program and provides an independent assessment.

**3.5 Action Plan:** A detailed plan developed by program faculty to address recommendations and improve program quality.

**3.6 Assessment Cycle:** The recurring period for program assessment and review, established as five years.

**3.7 Teach-Out Plan:** A plan to ensure that current students can complete a program that is being closed.

**3.8 Program Closure:** The permanent discontinuation of an academic program.

## 4.0 Policy Statement

**4.1** All academic programs shall undergo a comprehensive review on a five-year cycle.

**4.2** No program shall fail to participate in the assessment and review process.

**4.3** Program reviews shall include Self-Study conducted by program faculty; External Review by an independent expert; and Action Planning to address findings.

**4.4** Programs identified for closure shall have a teach-out plan approved by the Senate.

**4.5** The Academic Standards Committee shall oversee the program review process.

**4.6** Results of program reviews shall be reported to the University Senate.

## 5.0 Self-Study Requirements

**5.1** Program faculty shall conduct a self-study addressing: program mission and goals; program learning outcomes and their assessment; curriculum and instruction; student performance and achievement; faculty qualifications and development; resources and facilities; strengths and weaknesses; opportunities and threats; recommendations for improvement; and student satisfaction and engagement. The self-study shall be comprehensive and evidence-based, and submitted to the Academic Standards Committee. No program shall fail to submit a self-study.

**5.2** The self-study shall be completed within six months of the review cycle initiation. The Academic Standards Committee shall provide guidelines and support.

## 6.0 External Review Requirements

**6.1 External Reviewer Selection.** An external reviewer shall be appointed to evaluate the program. The reviewer shall be an expert in the field, shall not be affiliated with the University, and shall be approved by the Academic Standards Committee.

**6.2 External Review Process.** The external reviewer shall review the self-study, conduct a site visit (virtual or in-person), interview faculty, students, and staff, and provide an evaluation report, all within three months of the self-study. The report shall be submitted to the Academic Standards Committee. No program shall fail to cooperate with the external reviewer.

## 7.0 Action Planning Requirements

**7.1** Program faculty shall develop an action plan based on self-study findings, external reviewer recommendations, and Academic Standards Committee feedback. The plan shall include specific improvement actions, responsible parties, timelines for implementation, and success indicators, and shall be submitted to the Academic Standards Committee. No program shall fail to submit an action plan.

**7.2** Program faculty shall implement the action plan; the Academic Standards Committee shall monitor implementation, and progress reports shall be submitted annually.

## 8.0 Program Closure and Teach-Out

**8.1** Programs that fail to meet standards may be recommended for closure.

**8.2** The program closure proposal shall include the rationale for closure, a teach-out plan for current students, a timeline for closure, and a notification plan for students and faculty.

**8.3** The teach-out plan shall ensure that current students can complete the program.

**8.4** No program shall be closed without Senate approval.

## 9.0 Reporting Requirements

**9.1** The Academic Standards Committee shall submit a summary of program reviews to the University Senate, including overall program quality, recommendations for improvement, and the status of action plans.

**9.2** Reports shall be submitted annually.

## 10.0 Enforcement

**10.1** No program shall fail to participate in the assessment and review process, or fail to submit a self-study, cooperate with an external reviewer, or submit an action plan.

**10.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**10.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance with this Policy.

## 11.0 Related Documents

Constitution Article 8; Academic Standards Committee Charter (ACA-007); Program Learning Outcomes Assessment Policy (ACA-014).

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[4] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive standard for all course syllabi.

**1.2** This Policy ensures that all courses have a complete, accurate, and accessible syllabus; that all syllabi contain the required elements specified in this Policy; that students have clear and consistent information about course expectations; that no faculty member teaches a course without an approved syllabus; that the syllabus serves as a binding contract between the instructor and the student; and that the University meets accreditation and regulatory requirements for course documentation.

## 2.0 Scope

**2.1** This Policy applies to all faculty members teaching any course offered by the University; all courses, regardless of level, credit hours, or mode of delivery; and all departments and academic units.

**2.2** No course is exempt from this Policy.

## 3.0 Definitions

**3.1 Syllabus:** The official document that outlines course expectations, requirements, and policies. It serves as a binding contract between the instructor and the student.

**3.2 Significant Change:** A change that affects grading, assignments, or major course requirements.

**3.3 Catalog Year:** The academic year for which the Catalog is published.

## 4.0 Policy Statement

**4.1** All course syllabi shall follow the standard template and include all required elements specified in this Policy.

**4.2** No faculty member shall teach a course without an approved syllabus.

**4.3** Syllabi shall be submitted to the Office of Academic Affairs for approval.

**4.4** Syllabi shall be available to students before the start of the course.

**4.5** No faculty member shall make significant changes to the syllabus without approval.

**4.6** The syllabus is a binding document between the instructor and the student.

**4.7** No student may claim ignorance of syllabus policies as a defense for non-compliance.

**4.8** No instructor may deviate from the syllabus without proper notification and approval.

## 5.0 Required Syllabi Elements

Syllabi shall include, at a minimum:

**5.1 Course Identification** — course code and title; credit hours; semester and year.

**5.2 Instructor Information** — instructor name; instructor email; office hours (virtual, with time zone); contact information and response time (within 48 hours).

**5.3 Course Information** — course description; learning objectives; required texts and materials; recommended texts and materials.

**5.4 Assessment and Grading** — grading policy and components; weighting of each component; assignment descriptions and deadlines; assessment methods and rubrics.

**5.5 Course Schedule** — weekly schedule of topics; reading assignments; assignment deadlines; examination dates.

**5.6 Course Policies** — attendance policy; late submission policy; academic integrity policy; accessibility statement; accommodation for religious observances.

## 6.0 Template

Every syllabus shall follow the University's standard template, reproduced in full as **Exhibit A1** (following this policy). The template captures, in order: course and instructor identification; course description and learning objectives; required texts; the grading policy with weighted components; the week-by-week course schedule; course policies (attendance, academic integrity, accessibility); instructor contact and response-time commitment; and a signature block recording the approving authority and date.

## 7.0 Submission and Approval

**7.1** Syllabi shall be submitted to the Office of Academic Affairs at least two weeks before the start of the semester.

**7.2** Syllabi shall be reviewed by the department head.

**7.3** Approved syllabi shall be published in the LMS.

**7.4** No faculty member shall teach a course without an approved syllabus.

## 8.0 Syllabus Changes

**8.1** Significant changes to the syllabus require approval by the department head.

**8.2** Students shall be notified of changes in writing.

**8.3** Changes shall be made at least one week before they take effect.

**8.4** No instructor shall make changes after the semester has started without approval.

## 9.0 Student Access

**9.1** Students shall have access to syllabi before the start of the course.

**9.2** Syllabi shall be available in the LMS.

**9.3** Students shall be notified of any changes to the syllabus.

## 10.0 Enforcement

**10.1** No faculty member shall teach a course without an approved syllabus, or significantly deviate from the approved syllabus.

**10.2** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**10.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance with this Policy.

## 11.0 Related Documents

Academic Catalog (ACA-001).

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
<w:tbl>
  <w:tblPr>
    <w:tblW w:w="9350" w:type="dxa"/>
    <w:tblBorders>
      <w:top w:val="single" w:sz="8" w:space="0" w:color="B08625"/>
      <w:bottom w:val="single" w:sz="8" w:space="0" w:color="B08625"/>
    </w:tblBorders>
  </w:tblPr>
  <w:tblGrid><w:gridCol w:w="9350"/></w:tblGrid>
  <w:tr><w:tc><w:tcPr><w:tcW w:w="9350" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="122A4E"/><w:tcMar><w:top w:w="200" w:type="dxa"/><w:bottom w:w="200" w:type="dxa"/><w:left w:w="260" w:type="dxa"/></w:tcMar></w:tcPr>
    <w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Archivo SemiBold" w:hAnsi="Archivo SemiBold"/><w:color w:val="FFFFFF"/><w:b/><w:sz w:val="19"/><w:spacing w:val="16"/></w:rPr><w:t>EXHIBIT A1 &#8212; STANDARD COURSE SYLLABUS TEMPLATE</w:t></w:r></w:p>
  </w:tc></w:tr>
</w:tbl>
```

| | | | |
|---|---|---|---|
| Course Code | _____________________ | Course Title | _____________________ |
| Credit Hours | _____________________ | Semester | _____________________ |
| Instructor | _____________________ | Email | _____________________ |

| Section | Contents |
|---|---|
| 1. Course Description | Full narrative description of the course |
| 2. Learning Objectives | Numbered list, 3-7 objectives |
| 3. Required Texts | Full citations of required and recommended materials |
| 4. Grading Policy | Assignments / Quizzes / Midterm / Final / Participation, each with a weighting percentage summing to 100% |
| 5. Course Schedule | Week-by-week topics, readings, and deadlines |
| 6. Course Policies | Attendance, academic integrity, accessibility, and religious-observance accommodation statements |
| 7. Instructor Contact | Email and committed response time |

*Approved By: _________________________  Date: ___________*
'''

CONTENT[5] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive process for the annual evaluation of all faculty members.

**1.2** This Policy ensures that all faculty are evaluated annually across teaching, research, and service; that evaluations are fair, transparent, and consistent; that evaluation results inform reappointment, promotion, and professional development; that no faculty member is exempt from evaluation; that the University meets accreditation and regulatory requirements; and that part-time and adjunct faculty are also evaluated.

## 2.0 Scope

**2.1** This Policy applies to all faculty members, including full-time, part-time, and adjunct; all faculty with teaching, research, and administrative responsibilities; and all academic departments and colleges.

**2.2** No faculty member is exempt from evaluation.

## 3.0 Definitions

**3.1 Faculty Evaluation:** The systematic assessment of faculty performance across teaching, research, and service.

**3.2 Student Evaluation of Teaching:** The assessment of teaching by students.

**3.3 Peer Observation:** The observation of teaching by a colleague.

**3.4 Self-Assessment:** The faculty member's own evaluation of their performance.

**3.5 Supervisor Review:** The evaluation of faculty by their supervisor.

**3.6 Promotion:** Advancement through academic ranks (e.g., Assistant Professor to Associate Professor).

**3.7 Reappointment:** Renewal of a faculty member's contract.

## 4.0 Policy Statement

**4.1** All faculty members shall be evaluated annually on teaching, research, and service.

**4.2** No faculty member shall be exempt from evaluation.

**4.3** Evaluations shall include Student Evaluations of Teaching; Peer Observation; Self-Assessment; Supervisor Review; and Scholarship and Research.

**4.4** Results shall inform reappointment, promotion, and professional development.

**4.5** No evaluator shall engage in biased or unfair evaluation.

## 5.0 Evaluation Components

The teaching evaluation is a weighted composite of four components, summing to 100%:

| Component | Weight | Description |
|---|---:|---|
| Student Evaluations of Teaching | 40% | Collected at the end of each course via an instrument approved by the Senate; results are shared with faculty and kept confidential. |
| Peer Observation | 30% | At least one classroom observation per year by a colleague, documented on a standardized form, with feedback provided to the faculty member. |
| Supervisor Review | 20% | An annual review by the College Dean, covering evaluation data, performance feedback, and improvement recommendations. |
| Self-Assessment | 10% | An annual submission covering teaching accomplishments and challenges, research and scholarship activities, service contributions, and professional development. |

Scholarship and research are evaluated separately from teaching, based on publications (peer-reviewed journals, books, chapters), conference presentations, research grants and funding, and other scholarly activities (editorial work, peer review).

## 6.0 Evaluation Cycle

**6.1** The evaluation cycle shall be annual, beginning at the start of the academic year.

**6.2** Student evaluations shall be conducted at the end of each semester.

**6.3** Peer observations shall be conducted during the academic year.

**6.4** Self-assessments shall be submitted by the end of the spring semester.

**6.5** Supervisor reviews shall be completed by the end of the academic year.

**6.6** Results shall be communicated to faculty by 1 July.

## 7.0 Promotion Criteria

**7.1** Promotion shall be based on teaching effectiveness, research and scholarship, service contributions, and professional development.

**7.2** Promotion shall be recommended by the College Dean.

**7.3** Promotion shall be approved by the University Senate.

**7.4** No faculty member shall be promoted without demonstrating excellence.

## 8.0 Part-Time and Adjunct Faculty Evaluation

**8.1** Part-time and adjunct faculty shall be evaluated annually.

**8.2** Evaluation shall include student evaluations and supervisor review.

**8.3** Results shall inform reappointment decisions.

**8.4** No part-time or adjunct faculty member shall be exempt from evaluation.

## 9.0 Appeals

**9.1** Faculty may appeal evaluation decisions.

**9.2** Appeals shall be submitted in writing to the Deputy Vice-Chancellor, Academic Affairs within fourteen days.

**9.3** Appeals shall be heard by the Faculty Affairs Committee, which shall make a recommendation to the Deputy Vice-Chancellor.

**9.4** The Deputy Vice-Chancellor shall make the final decision.

## 10.0 Enforcement

**10.1** No faculty member shall be exempt from evaluation.

**10.2** No evaluator shall engage in biased or unfair evaluation.

**10.3** Violation of this Policy shall result in disciplinary action in accordance with applicable University policies.

**10.4** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance with this Policy.

## 11.0 Related Documents

Constitution Article 13; Faculty Handbook; Course Evaluation System (ACA-006).

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[6] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive process for collecting, analyzing, and utilizing student feedback on courses.

**1.2** This Policy ensures that all courses are evaluated by students at the end of each semester; that evaluation results are used to improve course quality and teaching effectiveness; that no course is exempt from evaluation; that student feedback is collected in a consistent, anonymous, and reliable manner; and that response rates are monitored and addressed.

## 2.0 Scope

**2.1** This Policy applies to all courses offered by the University; all faculty members and instructors; and all students enrolled in courses.

**2.2** No course is exempt from evaluation.

## 3.0 Definitions

**3.1 Course Evaluation:** The systematic collection of student feedback on a course and instructor.

**3.2 Response Rate:** The percentage of enrolled students who complete the evaluation.

**3.3 Evaluation Instrument:** The standardized form used to collect student feedback.

## 4.0 Policy Statement

**4.1** All courses shall be evaluated by students at the end of each semester.

**4.2** No faculty member shall be exempt from course evaluations.

**4.3** No student shall be prevented from completing course evaluations.

**4.4** Evaluations shall be administered through the LMS.

**4.5** Evaluations shall be anonymous.

**4.6** Results shall be shared with faculty and used for improvement.

## 5.0 Evaluation Instrument

**5.1** The evaluation instrument shall include course organization and design; instructor effectiveness; learning outcomes achieved; student engagement; and overall satisfaction.

**5.2** The instrument shall be reviewed and updated annually.

## 6.0 Administration

**6.1** Evaluations shall be administered online through the LMS.

**6.2** Students shall be given sufficient time to complete evaluations.

**6.3** Evaluations shall be anonymous.

**6.4** Response rates shall be monitored.

**6.5** Students with low response rates shall be reminded to complete evaluations.

## 7.0 Low Response Rates

**7.1** If a course has a response rate below 50%, the evaluation may be considered invalid.

**7.2** The instructor shall be notified of the low response rate.

**7.3** The course evaluation may be repeated or supplemented.

**7.4** No instructor shall be penalized for low response rates beyond their control.

## 8.0 Analysis and Reporting

**8.1** The Office of Institutional Research shall analyze evaluation results.

**8.2** Summary reports shall be provided to faculty members, College Deans, and the Deputy Vice-Chancellor, Academic Affairs.

## 9.0 Use of Results

**9.1** Faculty shall use evaluation results for course improvement.

**9.2** Deans shall use evaluation results for faculty development.

**9.3** The University Senate shall review aggregate results annually.

## 10.0 Enforcement

**10.1** No person shall prevent students from completing course evaluations, or tamper with evaluation results.

**10.2** Violation of this Policy shall result in disciplinary action.

**10.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance.

## 11.0 Related Documents

Faculty Evaluation System (ACA-005).

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[7] = '''
## 1.0 Purpose

**1.1** The purpose of this Charter is to define the composition, authority, and responsibilities of the Academic Standards Committee.

**1.2** This Charter ensures that academic quality and standards are maintained; that academic policies are fair and consistently applied; that student academic standing is monitored; that grade appeals and academic integrity cases are properly reviewed; and that committee members are qualified and impartial.

## 2.0 Scope

**2.1** This Charter applies to all members of the Academic Standards Committee.

## 3.0 Definitions

**3.1 Academic Standards Committee:** The standing committee responsible for academic standards and policies.

**3.2 Academic Standing:** The status of a student's academic performance.

**3.3 Committee Member Disqualification:** The removal of a member who is unable to serve.

## 4.0 Policy Statement

**4.1** The Academic Standards Committee shall operate in accordance with this Charter.

**4.2** The Committee shall consist of five faculty members.

**4.3** The Committee shall review academic policies; monitor student academic standing; review grade appeals; and oversee academic integrity cases.

**4.4** The Committee shall report to the University Senate.

## 5.0 Composition

**5.1** The Committee shall consist of five faculty members.

**5.2** Members shall be appointed by the University Senate.

**5.3** The Chair shall be elected by the Committee.

**5.4** Members shall serve a term of two years, renewable.

**5.5** Members shall be qualified in academic affairs.

## 6.0 Member Disqualification

**6.1** A member may be disqualified if unable to serve due to illness or incapacity; if they have a conflict of interest; or if they fail to attend three consecutive meetings.

**6.2** Disqualification shall be approved by the University Senate.

**6.3** A replacement shall be appointed within thirty days.

## 7.0 Responsibilities

**7.1 Academic Policy Review** — review proposed academic policies; recommend policy changes; ensure policy consistency.

**7.2 Student Academic Standing** — monitor student academic performance; review probation and dismissal decisions; recommend academic interventions.

**7.3 Grade Appeals** — review grade appeals; ensure fair and consistent grading; make final decisions on grade disputes.

**7.4 Academic Integrity** — oversee academic integrity cases; recommend sanctions; ensure due process.

## 8.0 Meetings

**8.1** The Committee shall meet monthly during the academic semester.

**8.2** Special meetings may be called by the Chair.

**8.3** A quorum shall consist of three members.

**8.4** Minutes shall be maintained by the Secretary to the Senate.

## 9.0 Reporting

**9.1** The Committee shall submit annual reports to the University Senate, including academic policy recommendations, a summary of grade appeals, academic integrity cases, and student academic standing.

## 10.0 Enforcement

**10.1** No person shall fail to comply with this Charter.

**10.2** Violation of this Charter shall result in disciplinary action.

## 11.0 Related Documents

Constitution Article 8; Senate Standing Rules (GOV-007).

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[8] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive roadmap for achieving and maintaining institutional accreditation.

**1.2** This Policy ensures that the University meets all accreditation standards and requirements; that accreditation activities are coordinated and systematic; that no program operates without appropriate accreditation; that the University maintains its credibility and reputation; and that accreditation status is properly disclosed.

## 2.0 Scope

**2.1** This Policy applies to the entire University; all academic programs and administrative units; and all faculty, staff, and administrators.

## 3.0 Definitions

**3.1 Accreditation:** Formal recognition by a recognized accrediting body.

**3.2 Self-Study:** The comprehensive institutional assessment required for accreditation.

**3.3 Site Visit:** The on-site evaluation by accrediting body representatives.

**3.4 Accreditation Status:** The current accreditation status of the University.

## 4.0 Policy Statement

**4.1** The University shall pursue and maintain institutional accreditation through a formal preparation plan.

**4.2** The Plan shall include accreditation goals and timeline; the self-study process; site visit preparation; gap analysis; and costs and budget allocation.

**4.3** Progress shall be reported to the University Senate annually.

**4.4** Accreditation status shall be publicly disclosed.

## 5.0 Accreditation Goals

**5.1** The University shall seek accreditation from recognized accrediting bodies.

**5.2** Timeline: Years 1-3, preparation and self-study; Years 3-5, application and site visit; Year 5, accreditation decision.

## 6.0 Self-Study Process

**6.1** The Office of Institutional Research shall coordinate the self-study.

**6.2** The self-study shall address mission and goals; academic programs; faculty qualifications; student services; facilities and resources; financial stability; and institutional effectiveness.

## 7.0 Site Visit Preparation

**7.1** The University shall prepare for the site visit by reviewing accreditation standards, gathering required documentation, preparing faculty and staff, and conducting mock visits.

## 8.0 Gap Analysis

**8.1** The University shall conduct a gap analysis to identify areas for improvement, addressing policy gaps, resource gaps, and quality gaps.

## 9.0 Accreditation Status Disclosure

**9.1** The University shall publicly disclose its accreditation status, including the accrediting body, status (candidate, accredited, etc.), and date of last review.

**9.2** No person shall misrepresent the University's accreditation status.

## 10.0 Enforcement

**10.1** No person shall fail to participate in accreditation activities, or misrepresent accreditation status.

**10.2** Violation of this Policy shall result in disciplinary action.

**10.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance.

## 11.0 Related Documents

Constitution Article 10; Strategic Plan (GOV-001).

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[9] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive criteria and process for evaluating and accepting transfer credits.

**1.2** This Policy ensures that transfer credits are evaluated fairly and consistently; that academic quality is maintained; that no student receives credit for courses that do not meet University standards; that transfer credit decisions are transparent and appealable; and that international transfer credits are properly evaluated.

## 2.0 Scope

**2.1** This Policy applies to all incoming and current students; all transfer credit requests; and all academic programs.

## 3.0 Definitions

**3.1 Transfer Credit:** Academic credit awarded for coursework completed at another institution.

**3.2 Source Institution:** The institution where the coursework was completed.

**3.3 International Transfer Credit:** Credit from an institution outside the United States.

## 4.0 Policy Statement

**4.1** Transfer credits shall be evaluated and accepted in accordance with this Policy.

**4.2** No student shall be awarded transfer credit for courses not meeting these requirements.

**4.3** The University Registrar shall evaluate all transfer credit requests.

**4.4** Credits must be from an accredited institution.

**4.5** A minimum grade of "C" is required.

**4.6** Maximum transfer credit shall be 50% of the program.

## 5.0 Evaluation Criteria

**5.1** Credits shall be evaluated based on the accreditation of the source institution; the grade earned; relevance to the program; and credit hour equivalency.

## 6.0 International Transfer Credit

**6.1** International transfer credits shall be evaluated by a recognized credential evaluation service.

**6.2** The evaluation shall include equivalency to U.S. credit hours; grade equivalency; and accreditation of the source institution.

**6.3** No student shall receive international transfer credit without proper evaluation.

## 7.0 Fraudulent Documents

**7.1** If fraudulent documents are discovered, the student shall be subject to disciplinary action.

**7.2** The student shall be notified of the discovery.

**7.3** The University may revoke admission or credit.

## 8.0 Evaluation Process

**8.1** Students shall submit official transcripts to the Registrar's Office.

**8.2** The Registrar shall evaluate transcripts for transfer credit.

**8.3** Students shall be notified of the evaluation within thirty days.

## 9.0 Appeals

**9.1** Students may appeal transfer credit decisions.

**9.2** Appeals shall be submitted in writing to the Registrar.

**9.3** Appeals shall be reviewed by the Academic Standards Committee.

## 10.0 Enforcement

**10.1** No person shall award transfer credit without proper evaluation.

**10.2** Violation of this Policy shall result in disciplinary action.

**10.3** The University Registrar shall ensure compliance.

## 11.0 Related Documents

Constitution Article 10; Academic Catalog (ACA-001).

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[10] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to define the AMIU credit hour in accordance with U.S. Carnegie standards and international equivalency frameworks.

**1.2** This Policy ensures that academic quality and consistency are maintained; that the University meets accreditation standards; that credit hours are transferable and recognized internationally; and that credit hours are verified for compliance.

## 2.0 Scope

**2.1** This Policy applies to all programs and courses offered by the University; all faculty and academic staff; and all students.

## 3.0 Policy Statement

**3.1** The AMIU credit hour shall be defined in accordance with U.S. Carnegie standards.

**3.2** One credit hour shall represent one hour of direct instruction per week, plus two hours of out-of-class work per week, over a 15-week semester.

**3.3** No person shall assign credit hours inconsistent with this definition.

## 4.0 International Equivalency

*The table below spans the full seven-tier Academic Ladder established in Constitution Article X, Section 10.1 — every credit-bearing tier is listed, including the Postgraduate Diploma, which the equivalency table did not previously carry.*

| AMIU Credit Hours | Approx. ECTS Equivalent |
|---|---|
| 45 CH (Undergraduate Diploma) | 22-24 ECTS |
| 60 CH (Associate Degree) | 30 ECTS |
| 120 CH (Bachelor of Arts) | 60 ECTS |
| 30 CH (Postgraduate Diploma) | 15 ECTS |
| 45 CH (Master of Arts) | 22-24 ECTS |
| 60 CH (Doctor of Philosophy) | Not directly comparable |
| Post-Doctoral Fellowship | Non-credit; no ECTS equivalent |

## 5.0 Contact Hour Verification

**5.1** The Office of the Registrar shall verify contact hours for all courses.

**5.2** Verification shall ensure compliance with the credit-hour definition.

**5.3** No course shall be approved with incorrect credit hours.

## 6.0 Enforcement

**6.1** No person shall assign credit hours inconsistent with this definition.

**6.2** Violation of this Policy shall result in disciplinary action.

**6.3** The University Registrar shall ensure compliance.

## 7.0 Related Documents

Constitution Article 10; Academic Catalog (ACA-001).

## 8.0 Effective Date

**8.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[11] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the academic calendar including semester dates, registration deadlines, and holidays.

**1.2** This Policy ensures clarity and consistency; effective planning; student success; and a defined process for emergency calendar changes.

## 2.0 Scope

**2.1** This Policy applies to the entire University community.

## 3.0 Policy Statement

**3.1** The University shall maintain an academic calendar that establishes semester dates and deadlines.

**3.2** No person shall deviate from the Academic Calendar without Senate approval.

## 4.0 Semester Dates

**4.1** Fall Semester: mid-August to mid-December.

**4.2** Spring Semester: mid-January to mid-May.

**4.3** Summer Semester: mid-May to mid-August.

## 5.0 Deadlines

**5.1** Add/drop deadlines; withdrawal deadlines; examination periods; grade submission deadlines; and graduation deadlines.

## 6.0 Emergency Calendar Changes

**6.1** In case of emergency, the President may adjust the calendar.

**6.2** The President shall notify the University community promptly.

**6.3** The Senate shall be informed of any changes.

## 7.0 Enforcement

**7.1** No person shall deviate from the Academic Calendar without Senate approval.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The University Registrar shall ensure compliance.

## 8.0 Related Documents

Academic Catalog (ACA-001).

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[12] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to define the definitive, binding, and comprehensive academic, residency, and administrative requirements for degree conferral.

**1.2** This Policy ensures that all students meet the same rigorous standards for graduation; that no student graduates without meeting all requirements; that graduation requirements are transparent and consistently applied; and that dual degrees and honors are properly awarded.

## 2.0 Scope

**2.1** This Policy applies to all students.

## 3.0 Policy Statement

**3.1** All degree requirements must be satisfied before degree conferral.

**3.2** No student shall graduate without meeting all requirements.

**3.3** The Senate shall ratify all degrees.

## 4.0 Credit Hour Requirements

| Level | Credit Hours |
|---|---|
| Undergraduate Diploma | 45 CH |
| Associate Degree | 60 CH |
| Bachelor of Arts | 120 CH |
| Postgraduate Diploma | 30 CH |
| Master of Arts | 45 CH |
| Doctor of Philosophy | 60 CH |
| Post-Doctoral Fellowship | Non-credit |

## 5.0 GPA Requirements

**5.1** Students must maintain a minimum cumulative GPA of 2.0.

**5.2** No student shall graduate with a GPA below 2.0.

## 6.0 Residency Requirements

**6.1** Students must complete a minimum number of credit hours at AMIU.

**6.2** The residency requirement is 50% of the program.

**6.3** No student shall graduate without meeting residency requirements.

## 7.0 Dual Degrees

**7.1** Students may pursue dual degrees with approval.

**7.2** Dual degrees require approval of both programs.

**7.3** No student shall be awarded dual degrees without approval.

## 8.0 Graduation with Honors

*The GPA bands below are stated as non-overlapping ranges — the source draft's "3.5-3.7 / 3.7-3.9 / 3.9-4.0" placed a GPA of exactly 3.7 or 3.9 in two honors tiers at once. Corrected to a single unambiguous tier per GPA value.*

**8.1** Honors shall be awarded based on GPA:

**8.1.1** Cum Laude: GPA 3.50-3.69;

**8.1.2** Magna Cum Laude: GPA 3.70-3.89;

**8.1.3** Summa Cum Laude: GPA 3.90-4.00.

**8.2** No student shall receive honors without meeting GPA requirements.

## 9.0 Application Process

**9.1** Students must apply for graduation by the deadline.

**9.2** No student shall graduate without submitting a graduation application.

## 10.0 Enforcement

**10.1** No student shall graduate without meeting all requirements.

**10.2** Violation of this Policy shall result in disciplinary action.

## 11.0 Related Documents

Constitution Article 10; Academic Catalog (ACA-001).

## 12.0 Effective Date

**12.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[13] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive standards of academic honesty and consequences for violations.

**1.2** This Policy ensures that academic integrity is upheld; that violations are investigated and sanctioned consistently; that no student engages in academic dishonesty without consequence; and that AI-generated work and third-party submissions are addressed.

## 2.0 Scope

**2.1** This Policy applies to all students, and to all academic work submitted for assessment.

## 3.0 Definitions

**3.1 Academic Dishonesty:** Any act that violates academic integrity.

**3.2 Plagiarism:** Presenting another's work as one's own.

**3.3 Cheating:** Using unauthorized materials or assistance.

**3.4 Fabrication:** Falsifying data or information.

**3.5 Unauthorized Collaboration:** Working with others without permission.

**3.6 AI Misuse:** Using AI to generate academic work without permission.

**3.7 Third-Party Submission:** Submitting work prepared by another person.

## 4.0 Policy Statement

**4.1** All students shall uphold the highest standards of academic honesty.

**4.2** Academic dishonesty, in any form, is strictly prohibited.

**4.3** No student shall engage in academic dishonesty, assist another in academic dishonesty, use AI to generate academic work without permission, or submit work prepared by a third party.

## 5.0 Prohibited Conduct

**5.1 Plagiarism.** Students shall not present the work of another as their own; copy text without quotation marks and citation; paraphrase without attribution; submit work previously submitted for another course without permission; submit purchased or obtained work; or use AI-generated content without attribution.

**5.2 Cheating.** Students shall not copy from another student's work; use unauthorized materials during examinations; obtain or distribute examination materials without authorization; impersonate or permit impersonation; or use unauthorized technology during examinations.

**5.3 Fabrication.** Students shall not falsify research data or results; invent sources or citations; or alter or falsify academic records.

**5.4 Unauthorized Collaboration.** Students shall not work with others without permission, or submit collaborative work as individual work.

**5.5 AI and Technology Misuse.** Students shall not use AI to generate assignments without permission; use AI to complete examinations; use translation software without permission; or use any unauthorized technology during assessments.

**5.6 Third-Party Submissions.** Students shall not submit work prepared by another person, use essay mills or similar services, or use any form of contract cheating.

## 6.0 Investigation Process

**6.1 Reporting.** Suspected violations shall be reported to the Office of Student Affairs in writing within 14 days of discovery.

**6.2 Preliminary Review.** The Office of Student Affairs shall conduct a preliminary review within 10 business days. If sufficient evidence exists, the matter shall be referred to the Academic Standards Committee.

**6.3 Investigation.** The Academic Standards Committee shall conduct an investigation; the student shall be notified and given 10 business days to respond.

**6.4 Decision.** The Academic Standards Committee shall issue a written decision within 15 business days, including sanctions imposed.

## 7.0 Sanctions

| Offense Category | First Offense | Second Offense | Third Offense |
|---|---|---|---|
| Minor (e.g., poor citation) | Zero on assignment, written warning | Zero on assignment, probation | Failing grade (F) in course |
| Moderate (e.g., copying) | Failing grade (F) in course | Failing grade (F) in course, suspension (1 semester) | Expulsion |
| Severe (e.g., impersonation, third-party submission) | Expulsion | Expulsion | Expulsion |

## 8.0 Appeals

**8.1** Students may appeal decisions within 14 days.

**8.2** Appeals shall be heard by the Academic Standards Committee.

**8.3** The Committee's decision shall be final.

## 9.0 Enforcement

**9.1** No student shall engage in academic dishonesty.

**9.2** Violation of this Policy shall result in disciplinary action.

**9.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance.

## 10.0 Related Documents

Student Code of Conduct (STU-001).

## 11.0 Effective Date

**11.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[14] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to define the definitive, binding, and comprehensive process for assessing program-level learning outcomes.

**1.2** This Policy ensures that all programs demonstrate that students achieve learning outcomes; that assessment results are used for continuous improvement; that no program operates without demonstrating learning outcomes; that accreditation standards are met; and that remedial actions are taken when outcomes are not achieved.

## 2.0 Scope

**2.1** This Policy applies to all academic programs.

## 3.0 Definitions

**3.1 Program Learning Outcomes:** The knowledge, skills, and abilities students are expected to gain.

**3.2 Assessment:** The systematic collection and analysis of evidence.

**3.3 Outcome Achievement:** The extent to which students achieve learning outcomes.

## 4.0 Policy Statement

**4.1** Program learning outcomes shall be assessed and reported annually.

**4.2** No program shall fail to conduct learning outcomes assessment.

**4.3** Assessment methods shall be approved by the Senate.

**4.4** Results shall be used for program improvement.

**4.5** Remedial actions shall be taken when outcomes are not achieved.

## 5.0 Assessment Methods

**5.1** Direct measures (exams, projects, portfolios); indirect measures (surveys, interviews); and program-level assessments.

## 6.0 Outcome Achievement Standards

**6.1** Programs shall set achievement standards for each outcome.

**6.2** Standards shall be approved by the Academic Standards Committee.

**6.3** No program shall set standards below acceptable levels.

## 7.0 Remedial Actions

**7.1** If outcomes are not achieved, programs shall implement remedial actions, including curriculum revision, instructional improvement, and student support.

**7.2** Remedial actions shall be reported to the Academic Standards Committee.

## 8.0 Reporting

**8.1** Program faculty shall submit assessment reports annually, including assessment methods, findings, and recommendations for improvement.

## 9.0 Enforcement

**9.1** No program shall fail to conduct learning outcomes assessment.

**9.2** Violation of this Policy shall result in disciplinary action.

**9.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance.

## 10.0 Related Documents

Program Assessment & Review Policy (ACA-003).

## 11.0 Effective Date

**11.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[15] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive attendance requirements for online courses.

**1.2** This Policy ensures student engagement and accountability; that no student fails to participate without consequence; that online attendance is measured consistently; and that excused absences for power outages and emergencies are addressed.

## 2.0 Scope

**2.1** This Policy applies to all students enrolled in online courses and programs.

## 3.0 Definitions

**3.1 Attendance:** Participation in course activities.

**3.2 LMS:** Learning Management System.

**3.3 Absence:** Failure to participate in course activities.

**3.4 Excused Absence:** An absence for a valid reason.

## 4.0 Policy Statement

**4.1** All students shall maintain 75% attendance in each course.

**4.2** No student shall fail to maintain the minimum attendance requirement.

**4.3** Attendance shall be measured through LMS login frequency (minimum 2 logins per week); participation in discussion forums; submission of assignments; viewing of recorded lectures; and attendance at synchronous sessions.

## 5.0 Excused Absences

**5.1** Excused absences include documented medical emergencies; documented family emergencies; religious observances; natural disasters or internet outages; and power outages affecting the student's region.

**5.2** Students must notify their instructor within 48 hours.

## 6.0 Consequences

**6.1** Students who fall below 75% attendance will receive a warning.

**6.2** Students who fail to meet the 75% attendance requirement may receive a failing grade (F).

**6.3** Students with excused absences shall be allowed make-up work.

## 7.0 Enforcement

**7.1** No student shall fail to maintain the minimum attendance requirement.

**7.2** Violation of this Policy shall result in disciplinary action.

**7.3** The Deputy Vice-Chancellor, Academic Affairs shall ensure compliance.

## 8.0 Related Documents

LMS Technical Specifications (OPS-015); Academic Calendar Policy (ACA-011).

## 9.0 Effective Date

**9.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[16] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive standards for online examinations and remote proctoring.

**1.2** This Policy ensures academic integrity in online assessments; fair and consistent application; accessibility and accommodation; and technical assistance for students.

## 2.0 Scope

**2.1** This Policy applies to all students enrolled in online courses and programs.

## 3.0 Definitions

**3.1 Online Examination:** An assessment conducted online through the LMS.

**3.2 Remote Proctoring:** The monitoring of examinations using technology.

**3.3 AI Proctoring:** Automated proctoring using artificial intelligence.

**3.4 Live Proctoring:** Real-time human proctoring.

## 4.0 Policy Statement

**4.1** Online examinations shall be conducted in a manner that preserves academic integrity.

**4.2** No student shall engage in academic dishonesty during examinations.

**4.3** Students must have a functional webcam, a working microphone, and a stable internet connection.

**4.4** Students whose webcam is off for more than 5 minutes may be subject to disciplinary action.

## 5.0 Prohibited Conduct

**5.1** Students shall not consult unauthorized materials; communicate with others during the examination; use unauthorized devices or software; attempt to circumvent proctoring technology; or engage in any other form of academic dishonesty.

## 6.0 Proctoring Fees

**6.1** Proctoring fees shall be disclosed to students in advance.

**6.2** Students may request financial hardship waivers.

**6.3** No student shall be denied access due to proctoring fees.

## 7.0 Technical Assistance

**7.1** Students experiencing technical difficulties shall receive support.

**7.2** Technical assistance shall be available during examinations.

**7.3** Students shall be given make-up opportunities for technical failures.

## 8.0 Enforcement

**8.1** No student shall engage in academic dishonesty during examinations.

**8.2** Violation of this Policy shall result in disciplinary action.

## 9.0 Related Documents

Academic Integrity Policy (ACA-013); LMS Technical Specifications (OPS-015).

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[17] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to define the definitive, binding, and comprehensive minimum technology requirements for students, faculty, and staff.

**1.2** This Policy ensures technical readiness; equitable access; academic success; and technology grants and loaner equipment for students.

## 2.0 Scope

**2.1** This Policy applies to all students, faculty, and staff.

## 3.0 Policy Statement

**3.1** All participants shall meet the minimum technology requirements.

**3.2** No person shall participate in online programs without meeting these requirements.

## 4.0 Minimum Device Requirements

**4.1** Students must have access to a computer with a processor of at least 1.6 GHz; at least 4 GB of RAM; at least 10 GB of available storage; a screen resolution of at least 1024 x 768; and a functioning webcam and microphone.

## 5.0 Internet Connectivity

**5.1** Students must have internet access with a minimum download speed of 1 Mbps (recommended: 5 Mbps) and a minimum upload speed of 0.5 Mbps.

## 6.0 Technology Grants

**6.1** Students in financial need may apply for technology grants.

**6.2** Grants shall cover technology costs.

**6.3** No student shall be denied access due to technology costs.

## 7.0 Loaner Equipment

**7.1** Students may request loaner equipment, available on a first-come, first-served basis.

**7.2** No student shall be denied access due to equipment unavailability.

## 8.0 Low-Bandwidth Accommodations

**8.1** Students without reliable internet may request low-bandwidth alternatives: text-based course materials; audio-only lectures; offline assignment submission; and extended time for coursework.

## 9.0 Enforcement

**9.1** No person shall participate in online programs without meeting technology requirements.

**9.2** Violation of this Policy shall result in disciplinary action.

## 10.0 Related Documents

LMS Technical Specifications (OPS-015); IT Infrastructure Plan (OPS-014).

## 11.0 Effective Date

**11.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[18] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to establish the definitive, binding, and comprehensive standards for the balance between synchronous and asynchronous learning.

**1.2** This Policy ensures flexibility, quality, and accommodation of diverse time zones.

## 2.0 Scope

**2.1** This Policy applies to all online courses and programs.

## 3.0 Policy Statement

**3.1** Courses shall offer a balance of synchronous and asynchronous learning.

**3.2** No course shall be entirely synchronous or entirely asynchronous.

## 4.0 Synchronous Learning

**4.1** Live sessions shall be recorded and made available for later viewing.

**4.2** A minimum of 50% of live sessions shall be scheduled to accommodate international students.

## 5.0 Asynchronous Learning

**5.1** Asynchronous learning shall include recorded lectures; discussion forums; self-paced activities; and assigned readings.

## 6.0 Recording Retention

**6.1** Recordings shall be retained for the duration of the course.

**6.2** Recordings shall be accessible to students who miss live sessions.

**6.3** No person shall share recordings outside the course.

## 7.0 Privacy of Recordings

**7.1** Recordings shall not be shared outside the course.

**7.2** Students shall not record live sessions without permission.

**7.3** No person shall violate the privacy of recorded sessions.

## 8.0 Enforcement

**8.1** No course shall be entirely synchronous or asynchronous.

**8.2** Violation of this Policy shall result in disciplinary action.

## 9.0 Related Documents

Online Attendance Policy (ACA-015); LMS Technical Specifications (OPS-015).

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

CONTENT[19] = '''
## 1.0 Purpose

**1.1** The purpose of this Policy is to define the definitive, binding, and comprehensive support services available to students and faculty in the online environment.

**1.2** This Policy ensures student wellbeing, faculty support, and academic success.

## 2.0 Scope

**2.1** This Policy applies to all students and faculty.

## 3.0 Policy Statement

**3.1** The University shall provide comprehensive virtual support services.

**3.2** No student or faculty member shall be denied access to support services.

## 4.0 Academic Advising

**4.1** Academic advisors shall be available via video conferencing, email, phone, and chat during office hours.

## 5.0 Mental Health Support

**5.1** Counseling services shall be available via video conferencing, phone, email, and online resources.

**5.2** Crisis intervention shall be available 24/7.

## 6.0 Multilingual Support

**6.1** Support services shall be available in multiple languages, including English, Arabic, and other languages as needed.

**6.2** No person shall be denied support due to language barriers.

## 7.0 Disability Services

**7.1** Reasonable accommodations shall be provided, including extended time for coursework, accessible course materials, and additional support for online participation.

## 8.0 Enforcement

**8.1** No student or faculty member shall be denied access to support services.

**8.2** Violation of this Policy shall result in disciplinary action.

## 9.0 Related Documents

Mental Health Support Policy (STU-009); Career Services Policy (STU-010).

## 10.0 Effective Date

**10.1** This Policy is effective as of 1 January 2028.
'''

def main():
    parts = []
    for (num, code, title, steward, owner, authority, thesis, sections) in POLICIES:
        parts.append(divider(num, code, title, steward, thesis, sections))
        kicker = f'::: {{custom-style="SectionKicker"}}\n{code} &#183; {title}\n:::\n'
        parts.append(kicker)
        parts.append(header_block(code, "1.0", "1 January 2028", "Annual", APPROVAL[code], steward, owner, authority))
        parts.append("")
        parts.append(CONTENT[num])
        parts.append(PAGEBREAK)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Wrote {OUT} ({sum(len(p) for p in parts)} chars)")

if __name__ == "__main__":
    main()
