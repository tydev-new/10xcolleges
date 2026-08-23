# Intake — the shapes it writes

`SKILL.md` says where the work has to get to; this file is the exact
form of each file intake owns. `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md`
is the contract for the whole folder; this is the part intake writes.

## `profile.md`

The sections of `${CLAUDE_PLUGIN_ROOT}/templates/student/profile.md`, as
shipped — the template is the one copy of that order. Every content
line ends with a source tag (`data-model.md § Provenance` is the list):

| Tag | Means |
|---|---|
| `[packet]` | the school's packet, or any document they handed over (resume, activities list, Common App export) |
| `[transcript]` | an official document they provided |
| `[worksheet]` | the criteria worksheet or the school's own form |
| `[student YYYY-MM-DD]` | they said it, that day — the date is required |
| `[parent YYYY-MM-DD]` · `[counselor YYYY-MM-DD]` | same, for them |

A blank is `TODO:` on its own line. It may say *what to ask*
(`TODO: unweighted GPA — ask them to check the transcript`); it never
carries a value. Quotes are word for word, in their grammar, in
quotation marks.

GPA lines say which: `- **GPA (unweighted):** 3.7 [transcript]`. A GPA
whose kind is unknown is two lines: `- **GPA (kind unknown):** "my GPA is
3.9" [student 2026-08-22]` and `- TODO: unweighted GPA — have them check
the transcript`. A `TODO:` line never carries a number or a hedge like "probably".

## `criteria.md`

The template's four tables; rows are numbered `H1, H2…` / `P1…` / `D1…`
in the order they came up. `college-list` refers to them by number, so
a number is never reused.

- `## Hard filters` — `| # | Criterion | Value | Source | Added |`. The
  budget row's Value names who set it: `$25k/yr · set by: parent` or
  `"probably like 30k?" · set by: nobody yet (student's guess)`.
- `## Preferences` — `| # | Criterion | Weight | Source | Added |`,
  Weight `Strong` or `Nice`.
- `## Deal-breakers` — `| # | "In their words" | What it rules out | Source | Added |`.
- `## Retired criteria` — the template's `| # | Criterion | Why it changed | When |`;
  the row keeps its number, `Why it changed` is their reason in their
  words with its tag (`"not IN a city, an hour away is fine" [student 2026-08-22]`).

A named college is a Preferences row (`Strong` or `Nice` as they say),
Criterion `named: <college> — "<their reason>"`.

## `conversations.md`

Add at the end only. One dated `## YYYY-MM-DD — <what this was>` header
per sitting, then one bullet per thing said, word for word in quotes,
tagged `[student]` / `[parent]`. Headers never go backwards in time.

## The gate

Two gates, both listed in `SKILL.md § Goal`; `check_record.py` counts
both from these shapes and prints `material N/4` (the essay gate) and
`gate N/4` (the list gate). The reply repeats the script's line for
what comes next, never its own count. The essay gate reads: a
`documents/` folder with a file in it, or a profile line `documents:
none [student …]`; an activity row with hours and a non-empty "what
actually happened" cell; three or more quoted bullets in
`conversations.md`; the major they are applying for — a tagged,
non-`TODO:` line under Goals and direction, with how sure.
