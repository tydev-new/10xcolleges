# Schema: feedback.md

Owner: `counselor-package` (appended to by `college-app`)
Class: **Append-only**

`feedback.md` records external reactions, reviews, and advice from school counselors, teachers, and parents. External feedback outranks the AI coach's reviews.

## `feedback.md` — owned by counselor-package (free-form body)

---

### Structure & Conventions

1. **Attribution & Date:** Every entry carries who said it and when (`## YYYY-MM-DD — <Source>`).
2. **Exact Attribution:** State whether the note comes from a counselor, teacher, or parent.
3. **Actionable Notes:** Include specific school recommendations, list feedback, or essay impressions.

```markdown
# Counselor & Parent Feedback — Jordan K

## 2026-08-22 — Counselor read (Ms. Alvarez)
- "The list is too top-heavy. Add two solid in-state safeties before finalizing."
- "Great essay topic on the robotics repair stand — make sure the emphasis is on leadership, not just fixing things."

## 2026-08-23 — Parent notes
- "Confirmed the annual budget ceiling is $30,000 net."
```
