# Schema: criteria.md

Owner: `student-intake`
Class: **Living (with Retired table)**

`criteria.md` holds the college list's explicit requirements: hard filters, preferences, and deal-breakers in the student's own words. It is re-read in full before every list operation.

## `criteria.md` — owned by student-intake
- `## Hard filters`
- `## Preferences`
- `## Deal-breakers`
- `## Retired criteria`
- `## Open questions` — optional

---

### Table Formats & Numbering

Rows are numbered monotonically in order of entry (`H1, H2...` / `P1, P2...` / `D1, D2...`). Numbers are never reused.

#### Hard filters
A school failing any hard filter is disqualified from the list.
```markdown
| # | Criterion | Value | Source | Added |
|---|---|---|---|---|
| H1 | Budget ceiling | $25k/yr · set by: parent | [parent 2026-08-20] | 2026-08-20 |
| H2 | Budget ceiling | "$30k?" · set by: nobody yet (student guess) | [student 2026-08-22] | 2026-08-22 |
```
*Note:* The budget row Value must explicitly state who set the number.

#### Preferences
Factors that score and rank schools without eliminating them.
```markdown
| # | Criterion | Weight | Source | Added |
|---|---|---|---|---|
| P1 | Research university with engineering | Strong | [student 2026-08-20] | 2026-08-20 |
| P2 | named: Pomona — "cousin went there and loved it" | Nice | [student 2026-08-22] | 2026-08-22 |
```
*Weights:* `Strong` (high priority) or `Nice` (positive preference).
*Named colleges:* Recorded as `named: <college> — "<student reason>"`.

#### Deal-breakers
Stated student turn-offs in their exact words.
```markdown
| # | "In their words" | What it rules out | Source | Added |
|---|---|---|---|---|
| D1 | "I don't want to be freezing cold" | Midwest / Northeast rural | [student 2026-08-20] | 2026-08-20 |
```

#### Retired criteria
Criteria that changed or were replaced. Rows are never deleted; they are moved here with the date and reason.
```markdown
| # | Criterion | Why it changed | When |
|---|---|---|---|
| D1 | "no big cities" | "an hour outside a city is fine" [student 2026-08-22] | 2026-08-22 |
```
