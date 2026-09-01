# Evaluating a College Research Dossier

A research dossier in `students/<slug>/research/<college-slug>.md` is evaluated against five core dimensions. Every dossier must function as an investigative counseling asset, not a university marketing brochure.

---

## The Rubric

| Dimension | Standard to Pass | Failure Looks Like |
|---|---|---|
| **1. Multi-Source Sourcing with Dates** | Every admit rate, test range, tuition figure, and deadline carries an inline source and year/date (`[CDS 2024-25 §C1]`, `[Scorecard 2023]`, `[retrieved YYYY-MM-DD]`). | Citing unverified numbers from memory; using third-party "chance me" widgets; missing years or dates. |
| **2. Student-Specific Lens** | Evaluates the school through *this student's* academic major, out-of-state vs. in-state residency, and family budget ceiling. | Quoting in-state averages for an out-of-state applicant; evaluating an engineering applicant using general university liberal arts stats. |
| **3. Essay-Actionable Specificity** | Identifies at least 2 distinctive academic resources (specific labs, maker spaces, capstones, student-run initiatives, or specialized clinics) for "Why Us" essays. | Generic platitudes like *"renowned faculty, state-of-the-art facilities, and great school spirit."* |
| **4. Honest Friction Reporting** | Details at least 2 genuine, unvarnished watch-outs (secondary major gatekeeping, large weed-out classes, housing shortages, weather, or cost traps). | Zero drawbacks noted; reads like an admissions viewbook. |
| **5. Admissions Policy & Decision Strategy** | Notes how the school evaluates applicants (CDS Section C7 weights: rigor, GPA, essays, demonstrated interest) and decision plan leverage (ED vs. EA vs. RD). | Failing to flag that demonstrated interest is tracked, or ignoring that Early Decision gives a 3x statistical advantage. |

---

## Who Checks What

1. **`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_research.py students/<slug>/research/<college-slug>.md` (Deterministic Script):**
   - Verifies `# H1 College Name` title on line 1.
   - Verifies required sections/fields exist (Admissions, Academics, Cost/Aid, Deadlines).
   - Verifies deadlines cite a specific calendar date (`YYYY-MM-DD`) or `Rolling`.
   - Confirms presence of inline citations and at least one explicit watch-out / friction tag.

2. **The Coach / Human Reviewer (Semantic Verification):**
   - Confirms that academic resources cited (labs, maker spaces) actually offer undergraduate access.
   - Verifies that net price estimates properly account for non-resident tuition and automatic scholarship thresholds.
   - Checks that qualitative cultural notes from Reddit/Niche are labeled `Impression, not data`.
