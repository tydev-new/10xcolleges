# Intake — the shapes it writes

`SKILL.md` names the destination; this file is the exact form of each
file intake owns. `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md` is the
contract for the whole folder; this is the part intake writes.

## `profile.md`

The twelve sections of `data-model.md § profile.md`, in that order,
headed `## 1. Basics` … `## 12. Constraints`. Every content line ends
with a source tag:

| Tag | Means |
|---|---|
| `[packet]` | the school's packet |
| `[transcript]` | an official document they provided |
| `[worksheet]` | the criteria worksheet or the school's own form |
| `[student YYYY-MM-DD]` | they said it, that day |
| `[parent YYYY-MM-DD]` · `[counselor YYYY-MM-DD]` | same, for them |

A blank is `TODO:` on its own line, optionally followed by *what to ask*
(`TODO: unweighted GPA — ask them to check the transcript`), never by a
value. Quotes are verbatim, in their grammar, in quotation marks.

GPA lines say which: `- **GPA (unweighted):** 3.7 [transcript]`. A GPA
whose kind is unknown is `TODO: unweighted GPA` plus the quoted number
as what they said (`"my GPA is 3.9" [student 2026-08-22] — likely weighted`).

## `criteria.md`

The template's four tables, rows numbered in order of arrival:

- `## Hard filters` — `| # | Criterion | Value | Source | Added |`. The
  budget row's Value names who set it: `$25k/yr · set by: parent` or
  `"probably like 30k?" · set by: nobody yet (student's guess)`.
- `## Preferences` — `| # | Criterion | Weight | Source | Added |`,
  Weight `Strong` or `Nice`.
- `## Deal-breakers` — `| # | "In their words" | What it rules out | Source | Added |`.
- `## Retired criteria` — `| # | Criterion | Retired | Why |` — a row
  moves here with the date and the reason in their words; its number is
  never reused.

A named college is a Preferences row (`Strong` or `Nice` as they say),
Criterion `named: <college> — "<their reason>"`.

## `conversations.md`

Append-only. A dated `## YYYY-MM-DD — <what this was>` header per
sitting, then one bullet per thing said, verbatim in quotes, tagged
`[student]` / `[parent]`. Headers never go backwards in time.

## `meta.json`

Only the `basics` block: name, grad year, high school, state — from the
packet or the student, nothing else here.

## The gate

Four items, counted in the reply as `gate N/4`:

1. budget **with who set it** — a guess counts as `0` here, and is the
   homework;
2. unweighted GPA;
3. a rough direction with how sure ("undecided" is a valid answer);
4. one row in Hard filters **and** one in Deal-breakers.
