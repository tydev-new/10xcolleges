# Schema: profile.md

Owner: `student-intake`
Class: **Living**

`profile.md` is the single source of truth for all verified facts about the student. It mirrors the school's Post-Secondary Options Packet plus interview sections.

## `profile.md` — owned by student-intake
- `## Basics`
- `## Senior year classes`
- `## Teachers who know you well`
- `## School activities`
- `## Outside activities`
- `## Hobbies`
- `## Honors and awards`
- `## Work experience`
- `## Reflections`
- `## Goals and direction`
- `## What excites them`
- `## What turns them off`
- `## Constraints`
- `## Context that doesn't show up elsewhere`

---

### Provenance Tags

Every content line must end with an attributed provenance tag:

| Tag | Meaning | Requirement |
|---|---|---|
| `[packet]` | From school packet, resume, activities list, or Common App export | Verbatim or documented claims |
| `[transcript]` | From official transcript or school report | Exact course names, grades, unweighted GPA |
| `[worksheet]` | From filled criteria worksheet or questionnaire | Self-reported answers |
| `[student YYYY-MM-DD]` | Spoken by student during conversation | Date required; verbatim quote when reflective |
| `[parent YYYY-MM-DD]` | Provided by parent | Date required |
| `[counselor YYYY-MM-DD]` | Provided by school counselor | Date required |

---

### Field Rules

1. **Unknown Values:** Any unknown field must be marked as `TODO:` on its own line (e.g., `- **GPA (unweighted):** TODO:`).
2. **Never Guess:** A `TODO:` line must never carry a guessed number, estimate, or hedge (e.g., no "probably ~3.8").
3. **GPA Specification:** Always distinguish unweighted and weighted GPA.
   - Known: `- **GPA (unweighted):** 3.82 [transcript]`
   - Unverified: `- **GPA (kind unknown):** "3.9" [student 2026-08-22]` followed by `- TODO: unweighted GPA — verify on transcript`
4. **Quotes:** Reflections and student quotes are recorded word-for-word in quotation marks with original grammar.
