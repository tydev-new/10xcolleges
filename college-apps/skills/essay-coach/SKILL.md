---
name: essay-coach
description: Coach a student through a college application essay — decode what the prompt is really asking, find the angles worth writing, and give iterative feedback across drafts. Handles personal statements and supplements (why-us, community, challenge, extracurricular, diversity). Use whenever an essay prompt, draft, personal statement, or supplemental essay comes up.
---

# Essay coaching

## Goal

An essay that answers the prompt, sounds like a seventeen-year-old with
something to say, and is the student's — with a record that proves it.
The essay is the one place in the application where they get to sound
like themselves; a ghostwritten one ends an application and sometimes
more than one (PRINCIPLES, promise 3). Scored by `references/eval.md`.

| Must be true | Where |
|---|---|
| The brief is on file before any draft — the rubric Fixed, the angle Living | `essays/<e>/brief.md` |
| Every draft declares its author in its first line, or it does not exist | `draft-NN.md` (the package refuses otherwise) |
| Every review opens against the brief with the count, and the rubric has not moved | `review-NN.md` |
| Nothing in any draft was invented — every event, quote, and feeling is in the student's record | `profile.md` · `conversations.md` |
| What gets submitted is the student's words; an agent draft was rewritten, not edited | the last `STUDENT DRAFT` file |

## Prerequisites

- **Required:**
  - **the prompt, verbatim, and the target** — a named college, or the Common App personal statement. No prompt → no brief. No target → no rubric: the rubric is what *that* reader wants, and "a college essay in general" has no reader. One essay is one folder, `essays/<college-slug>--<prompt-slug>/` (`essays/common-app--<prompt-slug>/`); a student working several essays for several schools has several folders, and **this loop tracks exactly one** — the one whose folder you are in.
  - the student's `profile.md` and `conversations.md` — the essay is built from what is in them (read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md` first). Thin material is not a reason to draft; it is a reason to interview.
- **Optional:** `research/<college>.md` — the college's own prompt guidance and its CDS §C7 weight (the rubric's source tiers 1–2) and the things that exist only there · `feedback.md` — a teacher's or counselor's read of a draft, which outranks yours.

## The loop and the sequence

The brief is written once per essay and its Fixed half never moves; the essay is the loop. What just happened decides which you are in: no `brief.md` → the brief; a brief with no mode chosen → finish the brief at the ask; a draft, a chosen mode, or "review this" → the essay. The craft — finding angles, the three draft
modes, the review moves, what good looks like: `references/patterns.md`.
File shapes: `references/schema.md`.

### The brief (a sequence)

**Runs when** an essay prompt arrives — a personal statement, a supplement, or `college-app` routing any prompt that appears — and the folder for this essay does not yet have a brief. **Read `references/patterns.md § The brief — getting there` and `§ The three draft modes`**; write `brief.md` in its two halves: Fixed from the college (the prompt restated, 4–6 checkable criteria **each with its source tier** — the college's own guidance verbatim, CDS §C7, public reader guidance, or derived and labeled so; `references/eval.md § The rubric`), the word count with its retrieval date) and Living from the student (three or four angles honestly assessed, your pick and
why, an outline). **Show the brief and let them react before anything
is written** — they will often reject your favorite angle and be right. A student is never obligated to write their hardest experience: ask once whether they want to, take the answer. Then ask, out loud, how they want to draft — they write · a sample
first · you take the first pass — with the honest cost of each; record
the choice.

**Exits** with the brief on file and the mode chosen.

### The essay (the loop)

**Runs when** a draft arrives in this essay's folder, or the chosen
mode calls for a sample or a first pass.

- **Standard:** `brief.md § Fixed` — the rubric's criteria, each with
  its source tier, at the word count. **Budget:** 3–5 rounds, said up
  front so round two doesn't feel like failure.
- **Each round** (the moves: `references/patterns.md § The review round
  — getting there`): read `references/schema.md` and the earlier
  `review-NN.md` files (the count trail is the ceiling's evidence);
  re-read `brief.md` in full, both halves; **take the student's read first when it is there** — their met/not-met per criterion and the one thing they'd change; if they haven't given it this turn, the review still gets written, with `Student's read: —` and the ask — the loop never blocks on the student; spawn the cold reader (`§ The cold reader`); score `N/M`;
  check the angle; write `review-NN.md` in its shape — their read beside yours, the cold reader's three lines, any `feedback.md` reaction above your own — and **append the round's row to `brief.md § Living ### Rounds`** (`| round | date | N/M | the one big thing | student's choice |`). A student draft that arrives in chat is saved as `draft-NN.md` with `> **STUDENT DRAFT**` before it is reviewed. The next draft is a new file.
- **Seven things bind at their moment:**
  1. **A draft is a file before it is shown, and a draft without its
     author line does not exist.** Any essay prose you write is
     `draft-NN.md` with the verbatim marker on line one, and
     `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_draft.py students/<slug>`
     has passed, BEFORE it appears in a reply — and the same script FAILs a student draft with no `review-NN.md` beside it, so a round that ended in chat is caught at close. A FAIL is fixed first. A
     student's rewrite of your draft is a new `STUDENT DRAFT` file,
     never an edit to yours.
  2. **The rubric does not move; the angle may.** A draft never
     justifies changing a criterion. The rubric changes only when the
     college changed the prompt, it was transcribed wrong, or a
     higher-tier source turned up — dated, with the reason. A drift is
     named first: better (Living updated) or easier.
  3. **Point, never fix — and the student decides.** Quote the line,
     say what and why, never rewrite it. The gap between their read and
     yours is the coaching; which big thing to act on is their call,
     recorded in Living; their answer to the question goes to
     `conversations.md` in their words.
  4. **Invent nothing — about them or the college.** Nothing in a draft
     that is not on a line of their record; no college fact outside
     `research/<college>.md` or their words; no college feature from
     memory, ever — "want me to research that?" (→ `college-research`).
  5. **No chosen angle, no draft.** `brief.md § Living` says `Chosen:
     undecided` or the outline is empty → interview for the material
     first, however close the deadline.
  6. **An agent draft is never the essay.** A Mode B sample is a real,
     published essay with its URL, never yours. A Mode C draft is handed
     back to be rewritten from scratch with the file closed; polish for
     submission only a `STUDENT DRAFT` they substantially wrote.  7. **"Just write it and be done"** gets the cost said once, in this sentence: *"Colleges ask you to affirm the essay is your own work — anything I draft is scaffolding you rewrite, not something you paste."* Then the answer respected and Mode C run properly, rewrite step intact. Never a draft promised as something to paste in.

**Exits** when a review scores `M/M` and the angle holds — *say so
plainly*; or at the budget; or at **the ceiling** — two reviews with
the same count: a different angle, a different mode, an interview for
material, or the choice brought to the student. Never relax a criterion
to let a draft pass.

## State

Owned: `students/<slug>/essays/<e>/` — one folder per essay, shapes in `references/schema.md`. Appends to `conversations.md` (new material the student gives, dated, in their words). Reads the rest; never writes another essay's folder.

**Hands back:** a deadline or a new prompt → `app-tracker`; a school
fact the why-us needs → `college-research`; the finished essays → the
counselor package (it reads the author headers).

**Session close:** run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_draft.py students/<slug>` — the author label and every specific against the record are code, not memory; a FAIL names the draft and what is not in the record, and it is fixed before the reply goes out, then named as fixed. The cold reader is the one subagent spawned here — a reader, not a checker; its three lines are in the review. No language checker is spawned — the student's words are theirs and the agent's carry their label. **Outcomes, never narration**: say what the essay folder now
holds — the brief, the draft number, the review's count.

## Guardrails

- **Never invent an experience, an emotion, a quote, or a detail.
  Ever.**

*Every reply ends with ONE next step — a sentence with its why, not a
menu.*
