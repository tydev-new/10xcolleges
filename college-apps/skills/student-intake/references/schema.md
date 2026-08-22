# Intake — the shapes it writes

`SKILL.md` names the destination; this file is the exact form of each
file intake owns. `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md` is the
contract for the whole folder; this is the part intake writes.

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

A blank is `TODO:` on its own line, optionally followed by *what to ask*
(`TODO: unweighted GPA — ask them to check the transcript`), never by a
value. Quotes are verbatim, in their grammar, in quotation marks.

GPA lines say which: `- **GPA (unweighted):** 3.7 [transcript]`. A GPA
whose kind is unknown is two lines: `- **GPA (kind unknown):** "my GPA is
3.9" [student 2026-08-22]` and `- TODO: unweighted GPA — have them check
the transcript`. A `TODO:` line never carries a number or a hedge.

## `criteria.md`

The template's four tables; rows are numbered `H1, H2…` / `P1…` / `D1…`
in order of arrival — `college-list` cites them by number, so a number
is never reused.

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

Append-only. A dated `## YYYY-MM-DD — <what this was>` header per
sitting, then one bullet per thing said, verbatim in quotes, tagged
`[student]` / `[parent]`. Headers never go backwards in time.

## The gate

The four items are in `SKILL.md § Goal`; `check_record.py` counts them
from these shapes and prints `gate N/4` — the reply repeats the script's
line, never its own count.
