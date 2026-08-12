# Data model — one folder per student

Everything about one student lives in `students/<slug>/`, where `<slug>` is lowercase-
hyphenated (`maya-rodriguez`). Skills read and write these files; nothing else is state.

```
students/maya-rodriguez/
├── profile.md              # THE source of truth about the student
├── conversations.md        # append-only log of what the student said
├── feedback.md             # parent + counselor input, attributed and dated
├── criteria.md             # what they're looking for — the list's rubric
├── colleges.md             # the list: tier, why, status
├── research/
│   └── <college-slug>.md   # one cited dossier per college
├── essays/
│   └── <college-slug>--<prompt-slug>/
│       ├── brief.md        # rubric + angle options + outline
│       ├── draft-01.md     # student's or agent's, labeled either way
│       ├── review-01.md    # feedback on draft-01
│       └── draft-02.md ...
├── recs/
│   ├── brag-sheet--<teacher-slug>.md
│   └── request--<teacher-slug>.md
├── out/
│   ├── tracker.xlsx
│   ├── packet.docx
│   └── package.html
└── meta.json               # small machine-readable index (see below)
```

## profile.md

Mirrors the school's Post-Secondary Options Packet, because that is what the counselor
already expects, plus an interview section the packet doesn't have. Sections, in order:

1. **Basics** — name, email, phone, grad year, high school, GPA (weighted + unweighted if
   known), test scores and test-optional intent, state of residence, citizenship status if
   relevant to aid.
2. **Senior year classes** — first and second semester.
3. **Teachers who know you well** — name, subject, grade taught, what they saw you do.
4. **School activities** — group, grades involved, hours/week, role, what actually happened.
5. **Outside activities** — same shape. Jobs and family responsibilities count and are
   often underreported; ask directly.
6. **Hobbies** — including the ones that "don't count." They frequently become the essay.
7. **Honors and awards** — with level (school / regional / state / national).
8. **Work experience** — employer, grades, position, hours.
9. **Reflections** — the packet's five questions, in the student's own words. Preserve
   their phrasing; do not smooth it out. This is essay raw material.
10. **Goals and direction** — intended major(s), career thinking, and how sure they are.
11. **What excites / what turns them off** — from the interview. Verbatim quotes.
12. **Constraints** — budget ceiling and who set it, distance from home, size preference,
    religious or cultural requirements, need for specific support services, athletics.

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

- `[packet]` — from the school packet
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
