# Essay coaching — the file shapes

One folder per essay: `students/<slug>/essays/<college-slug>--<prompt-slug>/`
(`common-app--<prompt-slug>/` for the personal statement). A student's
other essays are other folders; the loop in `../SKILL.md` tracks one.

Three kinds of file, each with the change rules the data model gives it
(`${CLAUDE_PLUGIN_ROOT}/docs/data-model.md`): the brief has a fixed half
and a living half; drafts and reviews never change once written — a
change is a new numbered file. The numbered sequence IS the history of
the essay and of who wrote each part.
`${CLAUDE_PLUGIN_ROOT}/scripts/build_package.py` is the authority on the
draft header: it refuses to build a package that contains a draft
without one.

## `brief.md` — the standard and the angle, under separate headings

- `## Fixed` — from the college. Changes only when the college changes
  it or it was copied wrong:
  - the prompt, restated in one plain sentence (what it is really asking)
  - **the rubric** — 4–6 criteria, each answerable yes/no, **each with
    its source tier** (`eval.md § The rubric`): 1 the college's own
    guidance for the prompt, quoted, with URL and date · 2 CDS §C7 (with
    the year) · 3 public reader guidance · 4 derived — labeled "derived"
  - word count and format, from the college's own page, with the date
    you looked it up
- `## Living` — from the student. Changes as the essay develops:
  - three or four angles, one sentence each, honestly weighed, and which
    one was chosen and why
  - the outline for the chosen angle — beats, not sentences
  - the draft mode chosen (A: they write · B: sample first · C: agent
    first pass), asked again for each new essay
  - a dated line for every change to either half, with the reason ("we
    added a criterion in October" can be explained later)
  - **`### Rounds`** — the score trail, one row per review, added the
    turn the review is written: `| round | date | N/M | the one big thing | student's choice |`
    (`student's choice` is what they decided to act on, or `—` until
    they say). The ceiling is two rows with the same `N/M`. This table
    is where the ceiling is read from, so a new session can see it
    without opening every review.

## `draft-NN.md` — never edited; the first line says who wrote it

The first line is one of these, exactly (`build_package.py` checks the
marker):

```markdown
> **STUDENT DRAFT**
> **AGENT FIRST DRAFT — built from your intake and our conversations. This is scaffolding, not your essay. Rewrite it in your own words before it goes anywhere near an application. Check every fact: if I got something wrong or put words in your mouth, say so and I'll cut it.**
> **EXAMPLE — a different student, a different topic. Do not submit any part of this. It's here to show what specificity looks like, not what to say.**
```

A student's rewrite of an agent draft is a **new file** with a
`STUDENT DRAFT` header — never an edit to the agent's file. That is the
whole record of whose words ended up in the application.

## `review-NN.md` — never edited; one per draft, in this shape

- **The student's read** — their own met / not met per criterion and
  the one thing they would change, written down BEFORE the coach's read
  when they gave it this turn; otherwise `—` and the ask. Then
  **Against the brief** — one line per criterion, met or not, and the
  score `N/M`; then the gap between the two reads, named.
- **Cold reader** — three lines from the blind read: the impression,
  what it remembers, the one question it is left with (or `VOID` and
  why).
- **External feedback** — when `feedback.md` has a teacher's or
  counselor's reaction to this draft, quoted here above the coach's
  read; it outranks the coach.
- **Angle check** — on the chosen angle, or drifted: somewhere better
  (Living updated, with the reason) or somewhere easier (named).
- **What's working** — two or three things, quoted exactly.
- **The one big thing** — one change, said plainly. If the student picks
  a different one, record their choice under Living.
- **Specific fixes** — line by line, quoting the line, about five at most.
- **One question** — something you genuinely don't know.

## What this skill reads and appends

`profile.md` and `conversations.md` — the essay is built from what is in
them, and the best material is usually a stray line from the interview.
`conversations.md` is **append-only**: anything new the student says is
added at the end, dated, in their words. `research/<college>.md` when it
exists — for the why-us rubric.
