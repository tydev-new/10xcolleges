---
name: rec-request
description: Plan recommendation letters — pick which teachers to ask, audit faculty writing habits, build personalized brag sheets with classroom friction moments, draft in-person scripts and email requests, and track submission etiquette. Produces brag-sheet--<teacher>.md and request--<teacher>.md.
---

# Recommendation Letters — Strategy, Brag Sheets & Requests

## Goal

Build `students/<slug>/recs/brag-sheet--<teacher-slug>.md` and `request--<teacher-slug>.md` for each recommender — **every brag sheet equipped with three concrete classroom moments from that teacher's room, every request grounded in an in-person conversation, every deadline verified, and FERPA access irrevocably waived** — validated deterministically by `scripts/check_rec.py`, evaluated qualitatively by `references/eval.md`, with schema in `${CLAUDE_PLUGIN_ROOT}/schemas/recs.md`.

| Must be true | Where |
|---|---|
| **Recommender balance:** 1 STEM + 1 Humanities/Social Science junior-year teachers prioritized | `profile.md § Teachers who know you well`, `recs/` |
| **Classroom specificity:** At least 3 concrete moments (friction, dialogue, initiative) from that teacher's room | `brag-sheet--<teacher-slug>.md` |
| **Declared major & deadlines:** Intended major and earliest application deadline date explicitly stated | `brag-sheet--<teacher-slug>.md`, `request--<teacher-slug>.md` |
| **Two-step ask dance:** Written request acknowledges prior face-to-face agreement | `request--<teacher-slug>.md` |
| **FERPA waiver status:** Confirmed waived in Common App | `brag-sheet--<teacher-slug>.md § Logistics` |
| **Deterministic validation:** `check_rec.py` passes with zero FAILs | CLI |

---

## Prerequisites

- **Required:** `students/<slug>/profile.md` (coursework, teachers who know you well, activities), `conversations.md`, and `criteria.md` / `colleges.md` (for deadlines).
- **Synchronizes with:** `academic-direction.md` (intended major alignment) and `meta.json` / `tracker.xlsx` (recommender statuses).
- **Outputs:**
  - `students/<slug>/recs/brag-sheet--<teacher-slug>.md`
  - `students/<slug>/recs/request--<teacher-slug>.md`

---

## Sequences and Loops

### Phase 1: Recommender Selection & Faculty Audit (Sequence)

**Runs when** planning who to ask, or when a student is uncertain which teachers will write strong letters.

1. **Verify College List Rules:** Audit target institutions on `colleges.md` for specific recommender requirements (e.g. MIT, Caltech, and Harvey Mudd mandate 1 STEM + 1 Humanities).
2. **Prioritize Junior Year (11th Grade):** Focus on 11th-grade teachers in core academic subjects who taught advanced rigor (AP, IB, DE, Honors).
3. **Conduct the Faculty Audit (Pattern § 2):**
   - *The Feedback Test:* Does this teacher write detailed narrative comments on papers/labs, or just assign numbers?
   - *The Vulnerability Test:* Has this teacher seen the student struggle, fail an assessment, seek help, and recover?
   - *The Capacity Test:* Does this teacher cap their letter list (e.g. max 15 students)? Ask early in September.
4. **Steer Toward Balance:** Never pick two teachers who say the exact same thing. Pair an analytical/experimental teacher with a discussion/humanities teacher.

### Phase 2: Brag Sheet & In-Person Script Drafting (The Loop)

**Runs for each agreed recommender.**

- **Standard:** The 5-dimension rubric in `references/eval.md`.
- **Each recommender:**
  1. *Extract Classroom Moments:* Sift `profile.md` and interview the student for **three narrative bricks** that occurred inside that specific teacher's room:
     - *Moment 1 (Friction & Recovery):* An exam dip, lab failure, or critical essay revision where the student worked through difficulty to mastery.
     - *Moment 2 (Classroom Dialogue):* A seminar debate, provocative question, or intellectual risk.
     - *Moment 3 (Peer Generosity / Build):* Voluntary peer tutoring or lab apparatus iteration.
  2. *Draft the In-Person Script:* Write a natural, 3-sentence spoken script for the student to ask the teacher face-to-face at 3:15 PM, giving them a gracious out.
  3. *Draft `brag-sheet--<teacher>.md`:* Format strictly according to `schemas/recs.md`.
  4. *Draft `request--<teacher>.md`:* Follow-up email sent within 2 hours of the in-person agreement, confirming deadlines, Common App invitation, and attachments.
  5. *Validate:* Run `check_rec.py`.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_rec.py" students/<slug>/recs/
```

### Phase 3: Relational Lifecycle & Accountability (Sequence)

**Runs across the autumn and spring application cycle.**

1. **Record in Meta:** Add recommenders to `meta.json` under `recommenders` (`asked`, `agreed`, `brag_sheet_sent`, `submitted`, `thanked`) and regenerate the tracker:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/make_tracker.py" students/<slug>
   ```
2. **2 Weeks Before Deadline:** If unsubmitted, draft a gentle, appreciative check-in note (Pattern § 7). Never push or badger.
3. **Post-Submission Gratitude:** Prompt the student to deliver a **handwritten thank-you card** to the teacher's classroom.
4. **Spring Outcome Reveal (April/May):** Prompt the student to visit the teacher in person to share their final college decision.

---

## State

Owns `students/<slug>/recs/brag-sheet--<t>.md` and `students/<slug>/recs/request--<t>.md` — schema in `${CLAUDE_PLUGIN_ROOT}/schemas/recs.md`. Appends to `conversations.md`.

---

## Non-Negotiable Guardrails

1. **Never Invent Classroom Moments:** Every project, grade recovery, or peer tutoring event must be drawn from `profile.md` or student testimony in `conversations.md`.
2. **The In-Person Ask Invariant:** Never send a cold email or Common App invitation before having a face-to-face conversation with the teacher.
3. **The Strict FERPA Rights Waiver:** The student must confirm they have waived their right to inspect recommendations. An unwaved letter destroys evaluative credibility.
4. **Division of Labor:** Teacher brag sheets focus exclusively on classroom curiosity and academic stamina. School context, family adversity, and AP caps belong exclusively to the School Counselor letter (`counselor-package`).
