# Essay coaching — the file shapes

One folder per essay, `students/<slug>/essays/<college-slug>--<prompt-slug>/` (`common-app--<prompt-slug>/` for the personal statement); a student's parallel essays are parallel folders, and the loop in `../SKILL.md` tracks one.
Three kinds of file, each with the mutability the data model assigns
(`${CLAUDE_PLUGIN_ROOT}/docs/data-model.md`): the brief is split, drafts
and reviews are immutable — a change is a new numbered file, and the
sequence IS the history of the essay and of who wrote it.
`${CLAUDE_PLUGIN_ROOT}/scripts/build_package.py` is the authority on the draft header: it
refuses to build a package containing a draft without one.

## `brief.md` — the standard and the angle, under separate headings

- `## Fixed` — from the college; changes only when the college changes it
  or it was transcribed wrong:
  - the prompt, restated in one plain sentence (what it is actually asking)  - **the rubric** — 4–6 criteria, each checkable yes/no, **each with its source tier** (`eval.md § The rubric`): 1 the college's own prompt guidance, verbatim + URL + date · 2 CDS §C7 (year) · 3 public reader guidance · 4 derived — labeled so
  - word count and format, from the college's own page, with the
    retrieval date
- `## Living` — from the student; changes as the essay evolves:
  - three or four angles, each one sentence, each honestly assessed, and
    which one was chosen and why
  - the outline for the chosen angle — beats, not sentences
  - the draft mode chosen (A: they write · B: sample first · C: agent
    first pass), re-asked at each new essay
  - dated lines for every change to either half, with the reason ("we
    added a criterion in October" is explainable later)

## `draft-NN.md` — immutable; the first line declares the author

The first line is one of these, verbatim (`build_package.py` checks the
marker):

```markdown
> **STUDENT DRAFT**
> **AGENT FIRST DRAFT — built from your intake and our conversations. This is scaffolding, not your essay. Rewrite it in your own words before it goes anywhere near an application. Check every fact: if I got something wrong or put words in your mouth, say so and I'll cut it.**
> **EXAMPLE — a different student, a different topic. Do not submit any part of this. It's here to show what specificity looks like, not what to say.**
```

A student's rewrite of an agent draft is a **new file** with a `STUDENT
DRAFT` header — never an edit to the agent's file. That distinction is
the whole record of whose words ended up in the application.

## `review-NN.md` — immutable; one per draft, in this shape

- **The student's read** — their own met / not met per criterion and the one thing they would change, captured BEFORE the coach's read; then **Against the brief** — one line per criterion, met or not, and the count `N/M` (the round's score); the gap between the two reads, named
- **Cold reader** — three lines from the independent pass: the impression, what it remembers, the one question it is left with (or `VOID` and why)
- **External feedback** — when `feedback.md` carries a teacher's or counselor's reaction to this draft, quoted here above the coach's read; it outranks the coach
- **Angle check** — on the chosen angle, or drifted: somewhere better
  (Living updated, with the reason) or somewhere easier (named)
- **What's working** — two or three things, quoted exactly
- **The one big thing** — one change, stated plainly; the student's choice if they pick a different one, recorded in Living
- **Specific fixes** — line-level, quoting the line, at most ~5
- **One question** — something you genuinely don't know

## What this skill reads and appends

`profile.md` and `conversations.md` — the essay is built from what is
in them, and the best material is usually a stray line from the
interview. `conversations.md` is **append-only**: anything the student
says that is new material is appended, dated, in their words.
`research/<college>.md` when it exists — for the why-us rubric.
