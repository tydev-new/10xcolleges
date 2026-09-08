# Evaluating a College Research Dossier

A research dossier in `students/<slug>/research/<college-slug>.md` is evaluated against five core dimensions. Every dossier must function as an investigative counseling asset, not a university marketing brochure.

---

## The Rubric

| Dimension | Standard to Pass | Failure Looks Like |
|---|---|---|
| **1. Multi-Source Sourcing with Dates** | Every admit rate, test range, tuition figure, and deadline carries an inline source and year/date (`[CDS 2024-25 §C1]`, `[Scorecard 2023]`, `[retrieved YYYY-MM-DD]`). | Citing unverified numbers from memory; using third-party "chance me" widgets; missing years or dates. |
| **2. Major-Specific Selectivity & Lens** | Evaluates the school through *this student's* academic major, residency, and direct-admit vs pre-major weed-out status. | Quoting in-state averages for an out-of-state applicant; treating a competitive engineering/business major as a general-admit program. |
| **3. Essay-Actionable Specificity** | Identifies at least 2 distinctive academic resources (specific labs, maker spaces, capstones, student-run initiatives, or specialized clinics) for "Why Us" essays. | Generic platitudes like *"renowned faculty, state-of-the-art facilities, and great school spirit."* |
| **4. Honest Friction Reporting** | Details at least 2 genuine, unvarnished watch-outs (secondary major gatekeeping, large weed-out classes, housing shortages, weather, or cost traps). | Zero drawbacks noted; reads like an admissions viewbook. |
| **5. Admissions Policy & Testing Strategy** | Notes CDS §C7 factor weights (rigor, GPA, essays, demonstrated interest), CDS §C9 score-submission percentage (auditing test-optional inflation), and decision plan leverage. | Failing to flag that demonstrated interest is tracked; ignoring that Early Decision gives 3x statistical advantage; ignoring test-optional score inflation. |
| **6. Budget Ceiling Comparison** | Explicitly compares estimated net price to the student's family budget ceiling from `criteria.md`, calculating surplus or cost gap. | Reporting a $50k cost without evaluating whether it breaks the family's annual budget. |

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
