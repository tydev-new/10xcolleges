# Data contract — one folder per student

Everything about one student lives in `students/<slug>/`. The slug is set once, at
Setup: first name and last initial, lowercase, hyphenated (`maya-r`) — or the full
surname when two students would collide (`maya-rodriguez`). It never changes after
that. Skills read and write these files; nothing else is state.

This document is binding. `design.md` explains the architecture around it.

## Layout

```
students/maya-r/
├── documents/              # what they dropped: packet, transcript, resume (read, never edited)
├── profile.md              # THE source of truth about the student
├── conversations.md        # append-only log of what the student said
├── feedback.md             # parent + counselor input, attributed and dated
├── criteria.md             # what they're looking for — the list's rubric
├── colleges.md             # the list: tier, why, status
├── research/
│   └── <college-slug>.md   # one cited dossier per college
├── essays/
│   └── <college-slug>--<prompt-slug>/
│       ├── brief.md        # FIXED rubric + LIVING angle (see below)
│       ├── draft-01.md     # student's or agent's, labeled either way
│       ├── review-01.md    # feedback on draft-01
│       └── draft-02.md ...
├── recs/
│   ├── brag-sheet--<teacher-slug>.md
│   └── request--<teacher-slug>.md
├── out/
│   ├── tracker.xlsx
│   ├── package.html
│   └── packet.docx
├── meta.json               # machine-readable index of the college list
└── packet.json             # extraction the .docx builder renders
```

## Mutability classes

Most defects in this system have been mutability errors — something treated as changeable
that wasn't, or as fixed when it moved. Every file belongs to exactly one class.

| Class | Rule | Why |
|---|---|---|
| **Append-only** | Add entries; never edit or remove an existing one. Corrections are new dated entries. | The record of what someone actually said is evidence. A tidied paraphrase isn't. |
| **Immutable** | Written once. A change means a new numbered file. | The sequence *is* the history — of improvement, and of authorship. |
| **Fixed-source** | Changes only when the external source changes, or when we transcribed it wrong. Never in response to our own work. | Something outside us defines it. Editing it to fit what we produced is rationalization. |
| **Living** | Edit freely as understanding improves; retire rather than delete where the audit trail matters. | It records a person's evolving intent, which genuinely changes. |
| **Index** | Machine-readable mirror of a Living file. Must be re-synced whenever its source changes. | Scripts can't parse prose; two representations must not disagree. |
| **Derived** | Never hand-edit. Regenerate from source. | Edits are silently destroyed on the next build. |

## Every file

One skill **owns** each file: it holds the file's exact shape in its
`references/schema.md` (linked below) and is the only skill that writes
it, except where the table says others append. A skill that needs a
change to a file it doesn't own asks the owner skill for it. Readers
take the shape from the owner's link — never from a copy. Owners not yet
converted to the skill shape keep their shape in their `SKILL.md`; the
link is filled in when they convert. `tests/test_data_model.py` checks
this table against the skills.

| Path | Class | Owner (shape) | Also written by | Changes when |
|---|---|---|---|---|
| `documents/*` | Fixed-source | the student (drops files) | — | Never edited; read by student-intake |
| `profile.md` | Living | student-intake — [schema](../skills/student-intake/references/schema.md) § `profile.md` | — | New information about the student |
| `criteria.md` | Living (Retired table) | student-intake — [schema](../skills/student-intake/references/schema.md) § `criteria.md` | college-list (retires rows; open questions) | The student's wants change |
| `colleges.md` | Living | college-list | — | Schools added, cut, or re-tiered |
| `conversations.md` | **Append-only** | student-intake — [schema](../skills/student-intake/references/schema.md) § `conversations.md` | every skill (append only) | After any substantive exchange |
| `feedback.md` | **Append-only** | counselor-package | college-app (append only) | Parent or counselor input arrives |
| `research/<college>.md` | Living | college-research | — | Re-researched, or a source updates |
| `essays/<e>/brief.md` | **Split** — see below | essay-coach — [schema](../skills/essay-coach/references/schema.md) § `brief.md` | — | Depends on which half |
| `essays/<e>/draft-NN.md` | **Immutable** | essay-coach — [schema](../skills/essay-coach/references/schema.md) § `draft-NN.md` | the student (a new numbered file) | Never. Write `draft-NN+1.md` |
| `essays/<e>/review-NN.md` | **Immutable** | essay-coach — [schema](../skills/essay-coach/references/schema.md) § `review-NN.md` | — | Never. Write `review-NN+1.md` |
| `recs/brag-sheet--<t>.md` | Living | rec-request | — | Before sending to that teacher |
| `recs/request--<t>.md` | Living | rec-request | — | Before the student sends it |
| `counselor-questions.md` | Living | counselor-package | — | Before each package send |
| `meta.json` | **Index** | college-app | — | Immediately after `colleges.md` changes |
| `packet.json` | **Index** | counselor-package | — | Before regenerating the .docx |
| `out/tracker.xlsx` | **Derived** | `make_tracker.py` | — | Regenerate; never edit |
| `out/package.html` | **Derived** | `build_package.py` | — | Regenerate; never edit |
| `out/package.pdf` | **Derived** | `build_package.py` | — | Regenerate; never edit |
| `out/packet.docx` | **Derived** | `fill_packet.py` | — | Regenerate; never edit |

Shipped with the plugin, read-only to a session:

| Path | Class | Changes when |
|---|---|---|
| `config/calendar.json` | Living (human-edited) | A real-world date moves — verify each summer |
| `templates/student/` | Fixed-source | The scaffold itself is revised |
| `templates/criteria-worksheet.md` | Fixed-source | The worksheet is revised |
| `docs/*.md` | Fixed-source | Deliberate design change |

### brief.md is deliberately split

The only file with two classes, because its halves answer to different authorities:

| Half | Class | Contains | May change when |
|---|---|---|---|
| **Fixed** | Fixed-source | Prompt, rubric, word count, format | The college revises it, we misread it, or we learn what the reader weighs (CDS §C7) |
| **Living** | Living | Angle, outline, draft mode | The essay evolves |

**A draft never justifies changing the rubric.** If a draft fails a criterion, the draft is
wrong. A rubric that relaxes to fit what was written has stopped being a standard.

Contrast `criteria.md`, which is fully Living: a college prompt is external and fixed,
while a student's preferences are their own and legitimately change. Same mechanic —
written down, re-read in full before every pass — different mutability, because the
sources differ.

## profile.md

Mirrors the school's Post-Secondary Options Packet, because that is what the counselor
already expects, plus the interview sections the packet doesn't have. **The section list
is `templates/student/profile.md`, as shipped — the one copy.** Briefly: basics (GPA
weighted *and* unweighted, scores and testing intent, residency if it affects aid), senior
classes, teachers who know you, school and outside activities (hours and what actually
happened — jobs and family responsibilities count and are underreported), hobbies, honors,
work, the packet's reflections verbatim, goals and direction, what excites / what turns
them off (quotes), constraints, and context that shows up nowhere else.

Mark anything unknown as `TODO:` on its own line. Skills scan for `TODO:` to know what to
ask next. Never fill a `TODO:` with a guess.

## criteria.md

The college list's equivalent of an essay brief: hard filters, deal-breakers in the
student's own words, weighted preferences, and a Retired table for criteria that stopped
applying. `college-list` re-reads it in full before every list operation, which is what
keeps a growing list from drifting off what the student actually asked for.

Rows are never deleted — they move to Retired with a reason. When a student and a parent
disagree, both rows stay, both tagged. Never merge them into an invented compromise.

Seed it from the interview, or from `templates/criteria-worksheet.md`, or from whatever
form the student's school already gave them.

## Provenance

Every non-obvious claim in `profile.md` carries a source tag at the end of the line:

- `[packet]` — from the school packet, or any other document the student handed over (resume, activities list, Common App export)
- `[worksheet]` — from the criteria worksheet or the school's own questionnaire
- `[student 2026-08-14]` — student said it, in conversation, on that date
- `[parent 2026-08-20]` — from the parent worksheet or a parent conversation
- `[counselor 2026-09-02]` — from the counselor
- `[transcript]` — from an official document the student provided

This matters. When a parent and a student disagree about how much the student liked
their internship, both versions belong in the file, tagged, and the essay skill needs to
know which one came from the student.

## meta.json

A small index so scripts don't have to parse Markdown:

```json
{
  "slug": "maya-rodriguez",
  "name": "Maya Rodriguez",
  "grad_year": 2027,
  "updated": "2026-08-12",
  "colleges": [
    {
      "name": "University of Michigan",
      "slug": "university-of-michigan",
      "unitid": 170976,
      "tier": "target",
      "decision_plan": "EA",
      "deadline": "2026-11-01",
      "app_type": "Common App",
      "counselor_letter": true,
      "status": "researching"
    }
  ]
}
```

`tier` is one of `safety | target | reach`. `status` is one of
`considering | researching | committed-to-apply | in-progress | submitted | decided | withdrawn`.

Scripts (`scripts/make_tracker.py`, `scripts/build_package.py`) read `meta.json`.
Keep it in sync whenever `colleges.md` changes — the orchestrator is responsible for this.

## Conventions

- Dates are ISO: `2026-11-01`. Deadlines are the college's stated date, not "early November."
- Money is annual USD, and always labeled: sticker vs net vs in-state.
- Never delete from `conversations.md` or `feedback.md`. Append. If something is wrong,
  append a correction with today's date.
- Drafts are never overwritten. `draft-02.md` is a new file. The student needs to be able
  to see that draft 4 is better than draft 1 — that is most of the motivation.

## Draft provenance is mandatory

Every `draft-NN.md` opens with exactly one of these, in its first few lines:

```markdown
> **STUDENT DRAFT**
> **AGENT FIRST DRAFT — …**
> **EXAMPLE — … Do not submit any part of this.**
```

`build_package.py` refuses to build if any draft lacks one. This is enforced rather than
trusted because an unlabeled agent draft is byte-for-byte indistinguishable from a
student's, and the counselor package would present it as the student's own work.

A student rewriting an agent draft creates a **new file** with a `STUDENT DRAFT` header
rather than editing the agent's. The sequence of files is the record of whose words
actually ended up in the application.

## What the counselor package reads

Improving the package means improving these files — it has no content of its own:

| Path | Appears as |
|---|---|
| `profile.md` | Student snapshot (with a `TODO:` count) |
| `criteria.md` | What they're looking for, before the list itself |
| `meta.json` → `colleges[]` | The list, with tier balance warnings |
| `research/*.md` | Collapsible dossier per school |
| `essays/*/brief.md` | The rubric and chosen angle — what a counselor can still change |
| `essays/*/draft-*.md` | Latest draft, with a provenance badge |
| `essays/*/review-*.md` | Counted as rounds (contents stay between coach and student) |
| `recs/brag-sheet--*.md` | Full text |
| `recs/request--*.md` | Full text, so tone can be caught before it reaches a teacher |
| `counselor-questions.md` | Overrides the generated "Where we'd value your input" |
