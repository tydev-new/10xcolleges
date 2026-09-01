# Evaluating a Financial Aid & Scholarship Strategy

A financial aid strategy in `students/<slug>/financial-aid.md` is evaluated against five core dimensions. It must function as an empowering, privacy-protecting counseling tool that cuts through college pricing obfuscation.

---

## The Rubric

| Dimension | Standard to Pass | Failure Looks Like |
|---|---|---|
| **1. Strategy Archetyping & Affordability** | Declares the family's primary path (**Need-based**, **Merit-seeking**, or **Hybrid / In-state anchor**) grounded in the annual net price budget ceiling from `criteria.md`. | Pushing a high-income family to chase need-based aid, or pushing a low-income family into 2% merit lotteries without a clear strategy. |
| **2. Strict Loan Separation (Debt vs. Aid)** | Clearly categorizes funds: **Free Money** (Grants/Scholarships) vs. **Debt** (Direct Loans, Parent PLUS) vs. **Labor** (Work-Study). | Subtracting loans from total cost to claim a lower "net price," or disguising a Parent PLUS loan as an award. |
| **3. Local-First Scholarship Triage** | Follows the 4-tier pyramid: prioritizes High School counseling bulletin and Community Foundation awards over low-yield national sweepstakes. | Dumping 20 generic national lottery scholarships (Coca-Cola, Taco Bell) that burn out the student with 500-word essays. |
| **4. Priority Deadline Accuracy** | Identifies institutional financial aid priority filing deadlines for FAFSA and CSS Profile (often Nov 1, Nov 15, or Dec 1 — earlier than RD). | Assuming financial aid forms can wait until spring, causing the student to miss priority funding. |
| **5. Privacy & NPC Protocol** | Never asks for family tax returns, AGI, or asset numbers in chat. Directs parents to run official Net Price Calculators offline. | Interrogating the teenager or parents for private tax numbers or income brackets. |

---

## Who Checks What

1. **`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_aid.py students/<slug>/financial-aid.md` (Deterministic Script):**
   - Verifies `# H1` header and required sections.
   - Verifies strategy archetype is explicitly stated.
   - Confirms annual budget ceiling is documented with a dollar figure.
   - Verifies form checklist includes priority dates.
   - **Deterministically fails** if loans (Direct, PLUS) are subtracted to claim a reduced net price.
   - Warns if national sweepstakes are listed without local/community foundation awards.

2. **The Coach / Human Reviewer (Semantic Verification):**
   - Verifies that merit scholarships listed are realistic given the student's unweighted GPA and test scores.
   - Ensures work-study is explained as bi-weekly paycheck wages for living expenses, not an upfront tuition credit.
   - Verifies that appeal letters (if drafted) follow a respectful, documented tone.
