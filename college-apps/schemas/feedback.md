# Schema: feedback.md

Owner: `counselor-package` (appended to by `college-app`)
Class: **Append-only**

Location: `students/<slug>/feedback.md`

`feedback.md` records external reactions, reviews, and guidance from high school counselors, independent counselors, teachers, and parents. In the counseling hierarchy, external counselor and parent feedback outranks the AI coach's automated evaluations.

---

## `feedback.md` — owned by counselor-package

### Structure & Conventions

1. **Chronological Header:** One dated header per feedback instance (`## YYYY-MM-DD — <Source Name & Role>`), moving forward in time.
2. **Explicit Attribution:** Every section must identify who provided the feedback (e.g. `Counselor read (Ms. Alvarez)`, `Parent discussion (Mr. & Mrs. Lee)`).
3. **Actionable Recommendations:** Captures specific list revisions, recommended additions, deleted schools, essay guidance, or budget ceiling adjustments.
4. **Append-Only Invariant:** Never edit or overwrite past feedback. If an earlier comment is superseded (e.g. a parent relaxes a budget limit), append a new dated section reflecting the change.

### Concrete Template:

```markdown
# Counselor & Parent Feedback — Jordan K

## 2026-08-22 — Counselor read (Ms. Alvarez)
- "The list is too top-heavy with four reaches and only one target. Add two solid in-state safeties (Michigan State and Michigan Tech) before finalizing."
- "Great essay topic on the robotics repair stand — make sure the emphasis is on student mentorship and leadership, not just fixing mechanical parts."

## 2026-08-23 — Parent budget confirmation
- "Confirmed the family's annual net price budget ceiling is $30,000 net after all grants and merit scholarships. Direct student loans up to the $5,500 federal maximum are acceptable."

## 2026-09-02 — High school counselor check-in (Mr. Reyes)
- "Approved the November 1 Early Action timeline for Michigan, Purdue, and Illinois. Transcript request submitted in high school portal."
- "Agreed that Ms. Alvarez and Mr. Davis provide a strong, balanced recommender pairing for engineering."
```
