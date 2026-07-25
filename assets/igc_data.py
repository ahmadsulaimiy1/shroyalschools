#!/usr/bin/env python3
"""Single source of truth for the AMIU Institutional Governance Compendium's
data-heavy sections (17-22). Authored as structured data, not hand-typed
markdown tables, specifically because the editorial review found that the
document's own hand-typed summary tables (Section 19.2's priority summary,
Section 22's phase-roadmap counts) had drifted out of sync with the
itemized 107-row inventory they were supposed to summarize. Every table in
Sections 17-22 is generated from this one list, so a summary number can
never again silently disagree with the rows it summarizes.

Source of the 107 rows: the user-supplied "AMIU Institutional Governance
Compendium" (AMIU-IGC-004, Version 4.0), Section 17. Category, priority,
status and steward text are transcribed verbatim from that source; only the
derived doc_code and the corrected summary/roadmap arithmetic are new.
"""

CATEGORY_ORDER = ["GOV", "ACA", "STU", "OPS", "LEG", "MKT", "WAQ"]
CATEGORY_NAMES = {
    "GOV": "Governance",
    "ACA": "Academic",
    "STU": "Student",
    "OPS": "Operations",
    "LEG": "Legal & Compliance",
    "MKT": "Marketing & Communications",
    "WAQ": "Waqf & Research",
}

# (number, title, category, priority, status, steward)
DOCS = [
    (1, "Strategic Plan", "GOV", "Complete", "Done", "President & Vice-Chancellor"),
    (2, "Strategic Plan Implementation Roadmap", "GOV", "Critical", "To Develop", "DVC, Administration & Finance"),
    (3, "Bylaws", "GOV", "Critical", "To Develop", "Secretary to the Board"),
    (4, "Certificate of Formation", "GOV", "Complete", "Done", "Office of Legal Counsel"),
    (5, "Board of Trustees Charter", "GOV", "Critical", "To Develop", "Chair, Board of Trustees"),
    (6, "Annual Report Template", "GOV", "Important", "To Develop", "President & Vice-Chancellor"),
    (7, "Senate Standing Rules", "GOV", "Critical", "To Develop", "Secretary to the Senate"),
    (8, "Succession Planning Policy", "GOV", "Important", "To Develop", "DVC, Administration & Finance"),
    (9, "Committee Charters", "GOV", "Critical", "To Develop", "Secretary to the Senate"),
    (10, "Conflict of Interest Policy", "GOV", "Critical", "To Develop", "Office of Legal Counsel"),
    (11, "Whistleblower Policy", "GOV", "Important", "To Develop", "Chair, Audit & Risk Committee"),
    (12, "Academic Catalog", "ACA", "Complete", "Done", "DVC, Academic Affairs"),
    (13, "Curriculum Development Process", "ACA", "Critical", "To Develop", "DVC, Academic Affairs"),
    (14, "Program Assessment & Review Policy", "ACA", "Critical", "To Develop", "DVC, Academic Affairs"),
    (15, "Course Syllabi Template", "ACA", "Critical", "To Develop", "DVC, Academic Affairs"),
    (16, "Faculty Evaluation System", "ACA", "Critical", "To Develop", "DVC, Academic Affairs"),
    (17, "Course Evaluation System", "ACA", "Critical", "To Develop", "DVC, Academic Affairs"),
    (18, "Academic Standards Committee Charter", "ACA", "Critical", "To Develop", "Chair, Academic Standards Committee"),
    (19, "Accreditation Preparation Plan", "ACA", "Important", "To Develop", "DVC, Academic Affairs"),
    (20, "Transfer Credit Policy", "ACA", "Important", "To Develop", "University Registrar"),
    (21, "Credit-Hour Definition Policy", "ACA", "Important", "To Develop", "University Registrar"),
    (22, "Academic Calendar Policy", "ACA", "Important", "To Develop", "University Registrar"),
    (23, "Graduation Requirements Policy", "ACA", "Important", "To Develop", "University Registrar"),
    (24, "Academic Integrity Policy", "ACA", "Important", "To Develop", "DVC, Academic Affairs"),
    (25, "Program Learning Outcomes Assessment Policy", "ACA", "Important", "To Develop", "DVC, Academic Affairs"),
    (26, "Online Attendance Policy", "ACA", "Critical", "To Develop", "DVC, Academic Affairs"),
    (27, "Remote Proctoring & Online Examinations Policy", "ACA", "Critical", "To Develop", "DVC, Academic Affairs"),
    (28, "Technology Requirements Policy", "ACA", "Critical", "To Develop", "Director, IT"),
    (29, "Synchronous/Asynchronous Learning Policy", "ACA", "Critical", "To Develop", "DVC, Academic Affairs"),
    (30, "Virtual Faculty & Student Support Policy", "ACA", "Important", "To Develop", "DVC, Academic Affairs"),
    (31, "Student Code of Conduct", "STU", "Critical", "To Develop", "Dean of Students"),
    (32, "Student Grievance Policy", "STU", "Critical", "To Develop", "Dean of Students"),
    (33, "Student Recruitment Plan", "STU", "Important", "To Develop", "DVC, Academic Affairs"),
    (34, "Student Orientation Program", "STU", "Important", "To Develop", "Dean of Students"),
    (35, "Student Retention Strategy", "STU", "Important", "To Develop", "Dean of Students"),
    (36, "Attendance Policy", "STU", "Critical", "To Develop", "Dean of Students"),
    (37, "Academic Probation & Dismissal Policy", "STU", "Critical", "To Develop", "Dean of Students"),
    (38, "Grade Appeal Policy", "STU", "Critical", "To Develop", "Dean of Students"),
    (39, "Mental Health Support Policy", "STU", "Important", "To Develop", "Dean of Students"),
    (40, "Career Services Policy", "STU", "Important", "To Develop", "Dean of Students"),
    (41, "Disability Services Policy", "STU", "Important", "To Develop", "Dean of Students"),
    (42, "Student Activities Policy", "STU", "Important", "To Develop", "Dean of Students"),
    (43, "International Student Support Policy", "STU", "Important", "To Develop", "Dean of Students"),
    (44, "Digital Citizenship & Online Conduct Policy", "STU", "Critical", "To Develop", "Dean of Students"),
    (45, "Islamic Dress Code Policy for Online Learning", "STU", "Critical", "To Develop", "Dean of Students"),
    (46, "Online Classroom Etiquette & Noise Policy", "STU", "Critical", "To Develop", "Dean of Students"),
    (47, "International Time Zone Policy", "STU", "Important", "To Develop", "Dean of Students"),
    (48, "Virtual Campus Life Policy", "STU", "Important", "To Develop", "Dean of Students"),
    (49, "Digital Accessibility Policy", "STU", "Important", "To Develop", "Dean of Students"),
    (50, "Student ID Card Policy", "STU", "Important", "To Develop", "University Registrar"),
    (51, "Virtual Graduation Policy", "STU", "Important", "To Develop", "University Registrar"),
    (52, "Faculty-Student Relationship Policy", "STU", "Critical", "To Develop", "DVC, Academic Affairs"),
    (53, "Comprehensive Disciplinary & Negative Reinforcement Policy", "STU", "Critical", "To Develop", "Dean of Students"),
    (54, "Financial Model", "OPS", "Complete", "Done", "DVC, Administration & Finance"),
    (55, "Financial Operations Manual", "OPS", "Critical", "To Develop", "DVC, Administration & Finance"),
    (56, "Budgeting Policy", "OPS", "Important", "To Develop", "DVC, Administration & Finance"),
    (57, "Procurement Policy", "OPS", "Important", "To Develop", "DVC, Administration & Finance"),
    (58, "Tuition Collection & Refund Policy", "OPS", "Critical", "To Develop", "DVC, Administration & Finance"),
    (59, "Payroll Policy", "OPS", "Critical", "To Develop", "DVC, Administration & Finance"),
    (60, "HR Policies & Procedures Manual", "OPS", "Critical", "To Develop", "DVC, Administration & Finance"),
    (61, "Recruitment & Hiring Policy", "OPS", "Critical", "To Develop", "Director, Human Resources"),
    (62, "Employee Contract Template", "OPS", "Important", "To Develop", "Director, Human Resources"),
    (63, "Compensation Policy", "OPS", "Important", "To Develop", "Director, Human Resources"),
    (64, "Leave Policy", "OPS", "Important", "To Develop", "Director, Human Resources"),
    (65, "Performance Review Policy", "OPS", "Important", "To Develop", "Director, Human Resources"),
    (66, "Termination Policy", "OPS", "Important", "To Develop", "Director, Human Resources"),
    (67, "IT Infrastructure Plan", "OPS", "Important", "To Develop", "Director, Information Technology"),
    (68, "LMS Technical Specifications", "OPS", "Important", "To Develop", "Director, Information Technology"),
    (69, "Data Privacy & Security Policy", "OPS", "Critical", "To Develop", "Director, Information Technology"),
    (70, "Backup & Disaster Recovery Plan", "OPS", "Important", "To Develop", "Director, Information Technology"),
    (71, "IT Support Policy", "OPS", "Important", "To Develop", "Director, Information Technology"),
    (72, "Acceptable Use Policy", "OPS", "Important", "To Develop", "Director, Information Technology"),
    (73, "Facilities Management Policy", "OPS", "Important", "To Develop", "Director, Facilities"),
    (74, "Health & Safety Policy", "OPS", "Important", "To Develop", "Director, Facilities"),
    (75, "Emergency Response Plan", "OPS", "Important", "To Develop", "Director, Facilities"),
    (76, "Learning Management System (LMS) Policy", "OPS", "Critical", "To Develop", "Director, Information Technology"),
    (77, "Online Pedagogy Training Policy", "OPS", "Critical", "To Develop", "DVC, Academic Affairs"),
    (78, "Virtual Office Hours Policy", "OPS", "Important", "To Develop", "DVC, Academic Affairs"),
    (79, "Digital Resources & Library Policy", "OPS", "Important", "To Develop", "University Librarian"),
    (80, "Social Media & Student Communication Policy", "OPS", "Important", "To Develop", "Director, Communications"),
    (81, "FERPA Compliance Policy", "LEG", "Critical", "To Develop", "University Registrar"),
    (82, "GDPR Compliance Policy", "LEG", "Critical", "To Develop", "Director, Information Technology"),
    (83, "Texas State Regulatory Filings Policy", "LEG", "Critical", "To Develop", "Office of Legal Counsel"),
    (84, "Intellectual Property Policy", "LEG", "Critical", "To Develop", "Office of Legal Counsel"),
    (85, "Non-Discrimination & Title IX Policy", "LEG", "Important", "To Develop", "DVC, Administration & Finance"),
    (86, "Gambia Branch Operational Plan", "LEG", "Critical", "To Develop", "DVC, Administration & Finance"),
    (87, "Nigeria Campus Development Plan", "LEG", "Critical", "To Develop", "DVC, Administration & Finance"),
    (88, "Country-Specific Regulatory Compliance", "LEG", "Critical", "To Develop", "Office of Legal Counsel"),
    (89, "Cross-Border Payment Systems Policy", "LEG", "Critical", "To Develop", "DVC, Administration & Finance"),
    (90, "International Faculty Recruitment Policy", "LEG", "Important", "To Develop", "Director, Human Resources"),
    (91, "International Student Support Policy", "LEG", "Important", "To Develop", "Dean of Students"),
    (92, "Brand Style Guide", "MKT", "Critical", "To Develop", "Director, Communications"),
    (93, "Website Content Plan", "MKT", "Critical", "To Develop", "Director, Communications"),
    (94, "Content Creation Policy", "MKT", "Important", "To Develop", "Director, Communications"),
    (95, "Social Media Policy", "MKT", "Important", "To Develop", "Director, Communications"),
    (96, "Media Relations Policy", "MKT", "Important", "To Develop", "Director, Communications"),
    (97, "Crisis Communications Plan", "MKT", "Important", "To Develop", "Director, Communications"),
    (98, "Marketing Plan", "MKT", "Critical", "To Develop", "Director, Communications"),
    (99, "Waqf & Endowment Board Charter", "WAQ", "Critical", "To Develop", "Chair, Waqf & Endowment Board"),
    (100, "Donor Stewardship Plan", "WAQ", "Critical", "To Develop", "Chair, Waqf & Endowment Board"),
    (101, "Fundraising Campaign Plan", "WAQ", "Critical", "To Develop", "Chair, Waqf & Endowment Board"),
    (102, "Research Policy", "WAQ", "Important", "To Develop", "DVC, Academic Affairs"),
    (103, "Publication & Conference Policy", "WAQ", "Important", "To Develop", "DVC, Academic Affairs"),
    (104, "Research Ethics Policy", "WAQ", "Important", "To Develop", "DVC, Academic Affairs"),
    (105, "Risk Register", "WAQ", "Complete", "Done", "Chair, Audit & Risk Committee"),
    (106, "Crisis Management Policy", "WAQ", "Critical", "To Develop", "Chair, Audit & Risk Committee"),
    (107, "Business Continuity & Insurance Policy", "WAQ", "Important", "To Develop", "DVC, Administration & Finance"),
]

assert len(DOCS) == 107, f"expected 107 documents, got {len(DOCS)}"
assert [d[0] for d in DOCS] == list(range(1, 108)), "document numbers must be a contiguous 1-107 sequence"

# ---------------------------------------------------------------------------
# Derived: category-relative Doc Code (e.g. GOV-001), matching the format
# Section 1.5 defines and Section 21's Cross-Reference Matrix already uses
# for most (but, before this fix, not all) documents.
# ---------------------------------------------------------------------------
_cat_counters = {c: 0 for c in CATEGORY_ORDER}
DOC_CODES = {}
for num, title, cat, priority, status, steward in DOCS:
    _cat_counters[cat] += 1
    DOC_CODES[num] = f"{cat}-{_cat_counters[cat]:03d}"

CATEGORY_TOTALS = {c: _cat_counters[c] for c in CATEGORY_ORDER}
assert sum(CATEGORY_TOTALS.values()) == 107

# ---------------------------------------------------------------------------
# Priority tallies — the authoritative numbers. The source document's own
# Section 19.2 ("Critical 62/58%, Important 38/35%, Complete 7/7%") does not
# match a row-by-row tally of Section 17 and is corrected here.
# ---------------------------------------------------------------------------
PRIORITY_COUNTS = {"Critical": 0, "Important": 0, "Complete": 0}
for num, title, cat, priority, status, steward in DOCS:
    PRIORITY_COUNTS[priority] += 1

assert PRIORITY_COUNTS == {"Critical": 49, "Important": 53, "Complete": 5}, PRIORITY_COUNTS

def pct(n):
    return round(100 * n / 107, 1)

PRIORITY_PERCENTAGES = {k: pct(v) for k, v in PRIORITY_COUNTS.items()}

# ---------------------------------------------------------------------------
# Phase roadmap. Phase 1 (Pre-Launch Essentials) is a fixed, hand-selected
# 9-document subset — all 9 happen to be Critical-priority documents. Phase 2
# is every other Critical document. Phase 3 is every Important document NOT
# already placed in Phase 4. Phase 4 is a fixed, hand-selected 7-document
# subset of Important documents (facilities/IT items deliberately deferred
# to Year 3+). The source document's own Section 22 numbered Phase 2 "53"
# and Phase 3 "38" — the reverse of the correct 40/46 split below — and
# separately double-booked documents 70-72 into both Phase 3 and Phase 4
# while never scheduling document 68 (LMS Technical Specifications) into
# any phase at all. Both defects are corrected here structurally: Phase 3
# is *computed* as "Important minus Phase 1 minus Phase 4", so a document
# can never again be double-booked or dropped.
# ---------------------------------------------------------------------------
PHASE1_NUMS = [3, 5, 10, 55, 60, 69, 31, 36, 58]
PHASE4_NUMS = [73, 74, 75, 70, 71, 72, 67]

_by_num = {d[0]: d for d in DOCS}
for n in PHASE1_NUMS:
    assert _by_num[n][3] == "Critical", f"Phase 1 doc {n} is not Critical"
for n in PHASE4_NUMS:
    assert _by_num[n][3] == "Important", f"Phase 4 doc {n} is not Important"

CRITICAL_NUMS = [d[0] for d in DOCS if d[3] == "Critical"]
IMPORTANT_NUMS = [d[0] for d in DOCS if d[3] == "Important"]
COMPLETE_NUMS = [d[0] for d in DOCS if d[3] == "Complete"]

PHASE2_NUMS = [n for n in CRITICAL_NUMS if n not in PHASE1_NUMS]
PHASE3_NUMS = [n for n in IMPORTANT_NUMS if n not in PHASE4_NUMS]

assert len(PHASE1_NUMS) == 9
assert len(PHASE2_NUMS) == 40, len(PHASE2_NUMS)
assert len(PHASE3_NUMS) == 46, len(PHASE3_NUMS)
assert len(PHASE4_NUMS) == 7
assert len(PHASE1_NUMS) + len(PHASE2_NUMS) + len(PHASE3_NUMS) + len(PHASE4_NUMS) == 102  # 107 - 5 Complete

def ranges(nums):
    """Render a sorted list of document numbers as comma-joined ranges, e.g. [2,7,9,13,14,15] -> '2, 7, 9, 13-15'."""
    nums = sorted(nums)
    out = []
    i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j+1] == nums[j] + 1:
            j += 1
        out.append(str(nums[i]) if i == j else f"{nums[i]}-{nums[j]}")
        i = j + 1
    return ", ".join(out)

# ---------------------------------------------------------------------------
# Markdown table generators
# ---------------------------------------------------------------------------

def md_escape(s):
    return s.replace("|", "\\|")

def table_17_full_inventory():
    lines = ["| # | Doc Code | Document | Category | Priority | Status | Policy Steward |",
             "|---:|---|---|---|---|---|---|"]
    for num, title, cat, priority, status, steward in DOCS:
        lines.append(f"| {num} | {DOC_CODES[num]} | {md_escape(title)} | {cat} | {priority} | {status} | {md_escape(steward)} |")
    return "\n".join(lines)

def table_18_category(cat):
    lines = ["| # | Doc Code | Document | Priority | Status | Policy Steward |",
             "|---:|---|---|---|---|---|"]
    for num, title, c, priority, status, steward in DOCS:
        if c == cat:
            lines.append(f"| {num} | {DOC_CODES[num]} | {md_escape(title)} | {priority} | {status} | {md_escape(steward)} |")
    return "\n".join(lines)

def table_19_2_summary():
    lines = ["| Priority | Count | Percentage |", "|---|---:|---:|"]
    for k in ("Critical", "Important", "Complete"):
        lines.append(f"| {k} | {PRIORITY_COUNTS[k]} | {PRIORITY_PERCENTAGES[k]}% |")
    lines.append(f"| **TOTAL** | **107** | **100.0%** |")
    return "\n".join(lines)

# 20.x: Responsibility Assignment Matrix needs Implementation Owner / Approval
# Authority columns, which are not derivable from DOCS alone — transcribed
# verbatim per-category from Section 20 of the source document.
RESPONSIBILITY = {
    1: ("President & Vice-Chancellor", "Office of Institutional Planning", "Board of Trustees"),
    2: ("DVC, Administration & Finance", "Office of Institutional Planning", "University Senate"),
    3: ("Secretary to the Board", "Office of Legal Counsel", "Board of Trustees"),
    4: ("Office of Legal Counsel", "Office of Legal Counsel", "Board of Trustees"),
    5: ("Chair, Board of Trustees", "Secretary to the Board", "Board of Trustees"),
    6: ("President & Vice-Chancellor", "Office of Communications", "Board of Trustees"),
    7: ("Secretary to the Senate", "Secretary to the Senate", "University Senate"),
    8: ("DVC, Administration & Finance", "Office of Human Resources", "Board of Trustees"),
    9: ("Secretary to the Senate", "Secretary to the Senate", "University Senate"),
    10: ("Office of Legal Counsel", "Office of Legal Counsel", "Board of Trustees"),
    11: ("Chair, Audit & Risk Committee", "Office of Internal Audit", "Board of Trustees"),
    12: ("DVC, Academic Affairs", "Office of the Registrar", "University Senate"),
    13: ("DVC, Academic Affairs", "Office of Academic Affairs", "University Senate"),
    14: ("DVC, Academic Affairs", "Office of Institutional Research", "University Senate"),
    15: ("DVC, Academic Affairs", "Office of Academic Affairs", "Academic Standards Committee"),
    16: ("DVC, Academic Affairs", "College Deans", "University Senate"),
    17: ("DVC, Academic Affairs", "Office of Institutional Research", "University Senate"),
    18: ("Chair, Academic Standards Committee", "Secretary to the Senate", "University Senate"),
    19: ("DVC, Academic Affairs", "Office of Institutional Research", "University Senate"),
    20: ("University Registrar", "Office of the Registrar", "University Senate"),
    21: ("University Registrar", "Office of the Registrar", "University Senate"),
    22: ("University Registrar", "Office of the Registrar", "University Senate"),
    23: ("University Registrar", "Office of the Registrar", "University Senate"),
    24: ("DVC, Academic Affairs", "College Deans", "University Senate"),
    25: ("DVC, Academic Affairs", "Office of Institutional Research", "University Senate"),
    26: ("DVC, Academic Affairs", "Office of Academic Affairs", "University Senate"),
    27: ("DVC, Academic Affairs", "Office of Academic Affairs", "University Senate"),
    28: ("Director, IT", "Office of IT", "DVC, Academic Affairs"),
    29: ("DVC, Academic Affairs", "Office of Academic Affairs", "University Senate"),
    30: ("DVC, Academic Affairs", "Office of Student Affairs", "University Senate"),
    31: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    32: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    33: ("DVC, Academic Affairs", "Office of Admissions", "University Senate"),
    34: ("Dean of Students", "Office of Student Affairs", "DVC, Academic Affairs"),
    35: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    36: ("Dean of Students", "Office of the Registrar", "University Senate"),
    37: ("Dean of Students", "Office of the Registrar", "University Senate"),
    38: ("Dean of Students", "Office of the Registrar", "University Senate"),
    39: ("Dean of Students", "Office of Student Affairs", "DVC, Administration & Finance"),
    40: ("Dean of Students", "Office of Career Services", "University Senate"),
    41: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    42: ("Dean of Students", "Office of Student Affairs", "DVC, Academic Affairs"),
    43: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    44: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    45: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    46: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    47: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    48: ("Dean of Students", "Office of Student Affairs", "DVC, Academic Affairs"),
    49: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    50: ("University Registrar", "Office of the Registrar", "DVC, Academic Affairs"),
    51: ("University Registrar", "Office of Communications", "University Senate"),
    52: ("DVC, Academic Affairs", "Office of Human Resources", "University Senate"),
    53: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    54: ("DVC, Administration & Finance", "Office of Finance", "Board of Trustees"),
    55: ("DVC, Administration & Finance", "Office of Finance", "DVC, Administration & Finance"),
    56: ("DVC, Administration & Finance", "Office of Finance", "Board of Trustees"),
    57: ("DVC, Administration & Finance", "Office of Procurement", "University Senate"),
    58: ("DVC, Administration & Finance", "Office of Finance", "University Senate"),
    59: ("DVC, Administration & Finance", "Office of Human Resources", "University Senate"),
    60: ("DVC, Administration & Finance", "Office of Human Resources", "University Senate"),
    61: ("Director, Human Resources", "Office of Human Resources", "DVC, Administration & Finance"),
    62: ("Director, Human Resources", "Office of Human Resources", "DVC, Administration & Finance"),
    63: ("Director, Human Resources", "Office of Human Resources", "University Senate"),
    64: ("Director, Human Resources", "Office of Human Resources", "University Senate"),
    65: ("Director, Human Resources", "Office of Human Resources", "University Senate"),
    66: ("Director, Human Resources", "Office of Human Resources", "University Senate"),
    67: ("Director, Information Technology", "Office of Information Technology", "DVC, Administration & Finance"),
    68: ("Director, Information Technology", "Office of Information Technology", "DVC, Academic Affairs"),
    69: ("Director, Information Technology", "Office of Information Technology", "University Senate"),
    70: ("Director, Information Technology", "Office of Information Technology", "Director, Information Technology"),
    71: ("Director, Information Technology", "Office of Information Technology", "Director, Information Technology"),
    72: ("Director, Information Technology", "Office of Information Technology", "University Senate"),
    73: ("Director, Facilities", "Office of Facilities", "DVC, Administration & Finance"),
    74: ("Director, Facilities", "Office of Facilities", "University Senate"),
    75: ("Director, Facilities", "Office of Facilities", "DVC, Administration & Finance"),
    76: ("Director, Information Technology", "Office of Information Technology", "DVC, Academic Affairs"),
    77: ("DVC, Academic Affairs", "Office of Academic Affairs", "University Senate"),
    78: ("DVC, Academic Affairs", "College Deans", "DVC, Academic Affairs"),
    79: ("University Librarian", "Library", "DVC, Academic Affairs"),
    80: ("Director, Communications", "Office of Communications", "DVC, Academic Affairs"),
    81: ("University Registrar", "Office of the Registrar", "University Senate"),
    82: ("Director, Information Technology", "Office of Information Technology", "University Senate"),
    83: ("Office of Legal Counsel", "Office of Legal Counsel", "Board of Trustees"),
    84: ("Office of Legal Counsel", "Office of Legal Counsel", "University Senate"),
    85: ("DVC, Administration & Finance", "Office of Human Resources", "University Senate"),
    86: ("DVC, Administration & Finance", "Office of International Operations", "Board of Trustees"),
    87: ("DVC, Administration & Finance", "Office of International Operations", "Board of Trustees"),
    88: ("Office of Legal Counsel", "Office of International Operations", "University Senate"),
    89: ("DVC, Administration & Finance", "Office of Finance", "University Senate"),
    90: ("Director, Human Resources", "Office of Human Resources", "University Senate"),
    91: ("Dean of Students", "Office of Student Affairs", "University Senate"),
    92: ("Director, Communications", "Office of Communications", "DVC, Academic Affairs"),
    93: ("Director, Communications", "Office of Communications", "Director, Communications"),
    94: ("Director, Communications", "Office of Communications", "DVC, Academic Affairs"),
    95: ("Director, Communications", "Office of Communications", "DVC, Academic Affairs"),
    96: ("Director, Communications", "Office of Communications", "DVC, Academic Affairs"),
    97: ("Director, Communications", "Office of Communications", "DVC, Academic Affairs"),
    98: ("Director, Communications", "Office of Communications", "DVC, Academic Affairs"),
    99: ("Chair, Waqf & Endowment Board", "Secretary, Waqf & Endowment Board", "Board of Trustees"),
    100: ("Chair, Waqf & Endowment Board", "Office of Waqf & Philanthropy", "Waqf & Endowment Board"),
    101: ("Chair, Waqf & Endowment Board", "Office of Waqf & Philanthropy", "Waqf & Endowment Board"),
    102: ("DVC, Academic Affairs", "Office of Research", "University Senate"),
    103: ("DVC, Academic Affairs", "Office of Research", "DVC, Academic Affairs"),
    104: ("DVC, Academic Affairs", "Office of Research", "University Senate"),
    105: ("Chair, Audit & Risk Committee", "Office of Internal Audit", "Board of Trustees"),
    106: ("Chair, Audit & Risk Committee", "Office of Internal Audit", "University Senate"),
    107: ("DVC, Administration & Finance", "Office of Finance", "University Senate"),
}
assert set(RESPONSIBILITY.keys()) == set(range(1, 108))

def table_20_category(cat):
    lines = ["| # | Doc Code | Document | Policy Steward | Implementation Owner | Approval Authority |",
             "|---:|---|---|---|---|---|"]
    for num, title, c, priority, status, steward in DOCS:
        if c == cat:
            owner, impl, approval = RESPONSIBILITY[num]
            lines.append(f"| {num} | {DOC_CODES[num]} | {md_escape(title)} | {md_escape(owner)} | {md_escape(impl)} | {md_escape(approval)} |")
    return "\n".join(lines)

def table_22_1_roadmap():
    lines = ["| Phase | Description | Documents | Timeline |", "|---|---|---:|---|"]
    lines.append(f"| Phase 1 | Pre-Launch Essentials | {len(PHASE1_NUMS)} | 4-6 Weeks |")
    lines.append(f"| Phase 2 | Year 1 Critical Documents | {len(PHASE2_NUMS)} | 3-4 Months |")
    lines.append(f"| Phase 3 | Year 2 Important Documents | {len(PHASE3_NUMS)} | 4-5 Months |")
    lines.append(f"| Phase 4 | Year 3+ Documents | {len(PHASE4_NUMS)} | 6-8 Months |")
    lines.append(f"| **TOTAL requiring development** | | **102** | **18-24 Months** |")
    return "\n".join(lines)

if __name__ == "__main__":
    print("Category totals:", CATEGORY_TOTALS)
    print("Priority counts:", PRIORITY_COUNTS)
    print("Priority pct:", PRIORITY_PERCENTAGES)
    print("Phase sizes:", len(PHASE1_NUMS), len(PHASE2_NUMS), len(PHASE3_NUMS), len(PHASE4_NUMS))
    print("Phase 2 ranges:", ranges(PHASE2_NUMS))
    print("Phase 3 ranges:", ranges(PHASE3_NUMS))
    print("Phase 4 ranges:", ranges(PHASE4_NUMS))
    print("All checks passed.")
