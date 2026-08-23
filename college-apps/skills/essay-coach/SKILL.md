---
name: essay-coach
description: Coach a student through a college application essay — work out what the prompt is really asking, find the angles worth writing, and give feedback draft by draft. Handles personal statements and supplements (why-us, community, challenge, extracurricular, diversity). Use whenever an essay prompt, draft, personal statement, or supplemental essay comes up.
---

# Essay coaching

## Goal

An essay that answers the prompt, sounds like a seventeen-year-old with
something to say, and is the student's own — with a file trail that
proves it. The essay is the one place in the application where they get
to sound like themselves. A ghostwritten essay can end an application,
sometimes more than one (PRINCIPLES, promise 3). Scored by
`references/eval.md`.

| Must be true | Where |
|---|---|
| The brief is on file before any draft: the rubric under Fixed, the angle under Living | `essays/<e>/brief.md` |
| Every draft says who wrote it on its first line. Without that line it does not count as a draft | `draft-NN.md` (the package build refuses it otherwise) |
| Every review starts by scoring the draft against the brief, and the rubric has not changed | `review-NN.md` |
| Nothing in any draft was made up. Every event, quote, and feeling is in the student's record | `profile.md` · `conversations.md` |
| What gets submitted is the student's words. An agent draft was rewritten, not edited | the last `STUDENT DRAFT` file |

## Prerequisites

- **Required:**
  - A working folder with a `CLAUDE.md` — none → the folder isn't set
    up; run `student-intake`'s Setup before any write.
  - **The prompt, word for word, and the target** — a named college, or
    the Common App personal statement. No prompt, no brief. No target,
    no rubric: the rubric is what *that* reader wants, and "a college
    essay in general" has no reader. One essay is one folder,
    `essays/<college-slug>--<prompt-slug>/` (or
    `essays/common-app--<prompt-slug>/`). A student working on several
    essays has several folders, and **this loop tracks exactly one: the
    essay the student names** ("the Pomona one", "my Common App
    essay"). New name → new folder. No name and several folders in
    progress → ask which, once, listing them by name with their last
    score from `brief.md § Rounds`. Naming another essay switches.
  - The student's `profile.md` and `conversations.md`. The essay is
    built from what is in them (read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md`
    first). Thin material is a reason to interview, not a reason to
    draft.
- **Optional:** `research/<college>.md` — the college's own guidance
  for the prompt and its CDS §C7 weight (the two best rubric sources —
  `references/eval.md § The rubric`), and the things that exist only at
  that school · `feedback.md` — a teacher's or
  counselor's read of a draft, which outranks yours.

## The loop and the sequence

The brief is a sequence (it runs once per essay) and its Fixed half
never changes. The essay is the loop (it repeats until it exits). What just happened tells you which you are
in: no `brief.md` → write the brief; a brief with no draft mode chosen →
finish the brief at the question; a draft, a chosen mode, or "review
this" → the essay loop. The craft — finding angles, the three draft
modes, how to review, what good looks like — is in
`references/patterns.md`. File shapes are in `references/schema.md`.

### The brief (a sequence)

**Runs when** an essay prompt arrives (a personal statement, a
supplement, or `college-app` passing one along) and this essay's folder
has no brief yet. **Read `references/patterns.md § The brief — getting
there` and `§ The three draft modes`.** Write `brief.md` in two halves.
Fixed comes from the college: the prompt restated in plain words; 4–6
yes/no criteria, **each with its source tier** (the college's own
guidance quoted, CDS §C7, public reader guidance, or derived and
labeled so — `references/eval.md § The rubric`); the word count with
the date you looked it up. Living comes from the student: three or four
angles, honestly weighed, your pick and why, and an outline. **Show the
brief and let them react before anything is written** — they will often
reject your favorite angle, and be right. A student never has to write
about their hardest experience: ask once whether they want to, and take
the answer. Then ask out loud how they want to draft — they write, a
sample first, or you take the first pass — with the honest cost of each.
Record the choice.

**Exits** with the brief on file and the mode chosen.

### The essay (the loop)

**Runs when** a draft arrives in this essay's folder, or the chosen
mode calls for a sample or first pass.

- **Standard:** `brief.md § Fixed` — the rubric with its source tiers,
  at the word count. **Budget:** 3–5 rounds, said up front.
- **Each round** (the moves: `references/patterns.md § The review round
  — getting there`): read `references/schema.md` and the earlier
  `review-NN.md` files (the score trail). Re-read `brief.md`, both
  halves. **Take the student's own read first when they give it** —
  met or not per criterion, and the one thing they'd change. Not
  given this turn → write the review anyway, `Student's read: —`, and
  ask; the loop never waits on the student. **A read that arrives
  after its review goes into `conversations.md` in their words, every
  criterion they scored, and
  your reply names each criterion where you disagree and why. Their
  read never moves yours: a criterion the review scored not-met stays
  not-met in the reply; say the gap, don't close it.** Spawn the cold reader (`§ The cold
  reader`); score `N/M`; check the angle; write `review-NN.md` in its
  shape. **Add the round's row to `brief.md § Living ### Rounds`.** A
  draft pasted in chat is saved as `draft-NN.md` under
  `> **STUDENT DRAFT**` before review; each draft is a new file.
- **Seven rules, each at the step it names:**
  1. **A draft is a file before anyone sees it, and a draft without its
     author line does not exist.** Essay prose you write goes into
     `draft-NN.md`, exact marker on line one, and
     `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_draft.py students/<slug>`
     has passed, BEFORE it appears in a reply; the same script fails a
     student draft with no review beside it. Fix a FAIL first. A
     student's rewrite of your draft is a new `STUDENT DRAFT` file.
  2. **The rubric does not change; the angle may.** A draft is never a
     reason to change a criterion — only the college changing the
     prompt, a copying error, or a higher-tier source (`eval.md § The
     rubric`), dated with the reason.
  3. **Point, never fix — and the student decides.** Quote the line, say
     what's wrong and why, never rewrite it. The gap between their read
     and yours is the coaching; what to act on is their call, recorded
     under Living; their answers go in `conversations.md`, verbatim.
  4. **Make nothing up — about them or the college.** Nothing in a
     draft not on a line of their record; no college fact
     outside `research/<college>.md` or their own words; never a college
     feature from memory — "want me to research that?" (→
     `college-research`).
  5. **No chosen angle, no draft.** `Chosen: undecided` or an empty
     outline in `brief.md § Living` → interview first, whatever the
     deadline.
  6. **An agent draft is never the essay.** A Mode B sample is a real,
     published essay with its URL, never yours. A Mode C draft is
     rewritten from scratch, file closed. Polish for submission only a
     `STUDENT DRAFT` they substantially wrote.
  7. **"Just write it and be done"** gets the cost said once, in this exact sentence: *"Colleges ask you to affirm the essay is your own work — anything I draft is scaffolding you rewrite, not something you paste."* Then respect the answer; run Mode C properly, rewrite included.

**Exits** when a review scores `M/M` and the angle holds — *say so
plainly*; or at the budget; or at **the ceiling** (the loop is stuck) —
two reviews with the same score: change the move — another angle,
mode, or interview, or bring the choice to the student. Never loosen a
criterion to let a draft pass.

## State

Owns `students/<slug>/essays/<e>/` — one folder per essay: `brief.md`,
`draft-NN.md`, `review-NN.md`, shapes in `references/schema.md`. Appends to `conversations.md` (new material the
student gives, dated, in their words; the shape is intake's). Reads
everything else — the shape of a file it doesn't own is the owner's,
found through `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md § Every file`.
Never writes into another essay's folder.

**Passes to:** a deadline or a new prompt → `app-tracker`; a school fact
the why-us needs → `college-research`; a new fact about the student
that came up while writing (a job, a dip, a change of major) → it is in
`conversations.md` already; `student-intake`'s Update moves it into the
profile; the finished essays → the counselor package (it reads the
author headers).

**Session close:** run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_draft.py students/<slug>`.
The author label and every specific detail against the record are
checked by code, not memory. A FAIL names the draft and what is not in
the record; fix it before the reply goes out, then say it was fixed. The
cold reader is the only subagent used here — a reader, not a checker;
its three lines go in the review. No language checker runs: the
student's words are theirs, and the agent's carry their label. **Report
outcomes, not activity**: say what the essay folder now holds — the
brief, the draft number, the review's score.

## Guardrails

- **Never make up an experience, an emotion, a quote, or a detail.
  Ever.**

*Every reply ends with ONE next step — a sentence with its why, not a
menu.*
