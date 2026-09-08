---
name: financial-aid
description: Develop a financial aid and scholarship strategy — classify strategy archetypes (need vs. merit), track FAFSA/CSS Profile priority deadlines, identify institutional merit grids, source local scholarships, and audit spring award letters. Use when a student or parent asks about paying for college, scholarships, financial aid forms, or reviewing an award letter.
---

# Financial aid and scholarships

Build and execute an actionable financial aid and scholarship plan that bridges the family's annual budget ceiling with institutional merit, need-based aid, and local awards.

| Must be true | Where |
|---|---|
| Strategy archetype declared against family budget ceiling | `students/<slug>/financial-aid.md` |
| Priority filing dates recorded for FAFSA and CSS Profile | `students/<slug>/financial-aid.md` |
| Institutional merit awards distinguish automatic from competitive | `students/<slug>/financial-aid.md` |
| Outside scholarships prioritize local/school awards over lotteries | `students/<slug>/financial-aid.md` |
| Loans strictly categorized as debt, never subtracted from net price | `students/<slug>/financial-aid.md` |
| `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_aid.py ...` passes | Terminal |

---

## Prerequisites

- **Required:** `students/<slug>/profile.md` (unweighted GPA, test scores, state residency) and `students/<slug>/criteria.md` (H1 annual net price budget ceiling). If state or budget is `TODO:`, ask the student in-stride or apply graceful degradation per `schemas/requirements.md`.
- Output file: `students/<slug>/financial-aid.md` following `schemas/financial-aid.md`.

---

## Sequences and loops

### The financial aid sequence

**Runs when** a student or parent asks about affordability, scholarships, financial aid deadlines, or reviewing award letters.

1. **Strategy Archetyping:** Review the budget ceiling in `criteria.md` and designate the primary path:
   - *Need-Based:* Focus on 100% need-met institutions and threshold promises.
   - *Merit-Seeking:* Focus on out-of-state tuition waivers and automatic GPA/SAT grids.
   - *Hybrid / In-State Anchor:* In-state tuition safety paired with selective reach targets.
2. **Form Priority Calendar:** Record institutional priority deadlines for FAFSA and CSS Profile (which frequently fall on Nov 1 or Dec 1, ahead of regular admission deadlines).
3. **Institutional Merit Hunt:** Map the student's unweighted GPA and test scores against automatic out-of-state tuition waivers and merit grids. Flag separate scholarship essay deadlines.
4. **Local Scholarship Sourcing:** Guide the student through the Local-First Pyramid (High school counseling bulletin → Community foundation pooled funds → Professional associations).
5. **Write `financial-aid.md`:** Populate the living plan following the schema.
6. **Award Audit (Spring):** When offers arrive, translate letters into True Net Price (Sticker COA minus Grants/Scholarships). Categorize loans as debt and work-study as wages. Draft appeal letters if valid triggers exist.

**Exits** when `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_aid.py students/<slug>/financial-aid.md` passes clean.

---

## Moment rules

1. **Privacy first:** Never ask for tax returns or household income in chat. Direct parents to run official Net Price Calculators (NPC) offline.
2. **Loans are debt, not aid:** Federal Direct Loans and Parent PLUS Loans finance the bill; they do not reduce it. Never subtract loans to claim a lower net price.
3. **Work-study is labor, not a discount:** Work-study requires finding an on-campus job and is paid in bi-weekly paychecks for pocket money. It is not credited upfront on tuition bills.
4. **Local over national:** Prioritize high school and community foundation awards with high yield; discourage burning time on national 50,000-applicant lotteries.
5. **Never count competitive aid as guaranteed:** Only guaranteed, automatic matrix scholarships can be used to justify safety tier affordability.

---

## Session close

Before replying to the student on EVERY turn:
1. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_aid.py students/<slug>/financial-aid.md` as the absolute final tool call on EVERY turn — whether files were edited or you are merely answering questions, explaining forms, or discussing scholarships. Never reply without running `check_aid.py` first.
2. Every reply ends with ONE next step and its reason.
