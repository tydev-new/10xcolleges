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

- **Required:** the student's `profile.md` and `conversations.md` — the
  essay is built from what is in them (read
  `${CLAUDE_PLUGIN_ROOT}/docs/voice.md` first). Thin material is not a
  reason to draft; it is a reason to interview.
- **Optional:** `research/<college>.md` (the why-us rubric wants things
  that exist only there) · the school's CDS §C7 (what they actually
  weigh).

## The loop and the sequence

The brief is written once per essay and its Fixed half never moves;
the essay is the loop. The craft — finding angles, the three draft
modes, the review moves, what good looks like: `references/patterns.md`.
File shapes: `references/schema.md`.

### The brief (a sequence)

**Runs when** an essay prompt arrives — a personal statement, a
supplement, or `college-app` routing a prompt from the tracker. **Read
`references/patterns.md § The brief — getting there`**; write `brief.md`
in its two halves: Fixed from the college (the prompt restated, 4–6
checkable criteria, the word count with its retrieval date) and Living
from the student (three or four angles honestly assessed, your pick and
why, an outline). **Show the brief and let them react before anything
is written** — they will often reject your favorite angle and be right.
Then ask, out loud, how they want to draft — they write · a sample
first · you take the first pass — with the honest cost of each; record
the choice.

**Exits** with the brief on file and the mode chosen.

### The essay (the loop)

**Runs when** a draft arrives, or the chosen mode calls for a sample or
a first pass.

- **Standard:** `brief.md § Fixed` — the rubric's criteria at the word
  count. **Budget:** 3–5 rounds, said up front so round two doesn't feel
  like failure.
- **Each round:** re-read `brief.md` in full — both halves — before
  reading the draft (reviewing from a fresh read of the draft alone is
  how coaching drifts into polishing sentences in an essay that quietly
  stopped answering the prompt); score the draft against every
  criterion, `N/M`; check the angle; write `review-NN.md` in its shape;
  the next draft is a new file.
- **Four things bind at their moment:**
  1. **A draft without its author line does not exist.** Before any
     draft is written — yours or theirs — its first line is the verbatim
     marker (`references/schema.md`); a student's rewrite of your draft
     is a new file with `STUDENT DRAFT`, never an edit to yours. The
     package refuses to build otherwise.
  2. **The rubric does not move; the angle may.** A draft never
     justifies changing a criterion — if the draft fails "specific to
     this school", the draft is wrong. The rubric changes only when the
     college changed the prompt, you transcribed it wrong, or the CDS
     §C7 turned up — and the change is dated with its reason. A drift
     in angle is named first: better (Living updated, with why) or
     easier (it stopped answering the prompt).
  3. **Point, never fix.** A review quotes the line and says what and
     why; it never rewrites their sentence. That is the difference
     between coaching and ghostwriting, and why the essay will sound
     like them.
  4. **Invent nothing.** Mode C builds only from `profile.md` and
     `conversations.md` — no event, feeling, quote, or detail they did
     not give; thin material means stop and interview. A Mode C draft
     is handed back with the instruction to rewrite from scratch with
     the file closed; line-editing it does not produce their essay.
     "Just write it and be done" gets the cost said once, plainly —
     colleges ask them to affirm it is their own work — then the answer
     respected and Mode C run properly, rewrite step intact.

**Exits** when a review scores `M/M` and the angle holds — *say so
plainly*; or at the budget; or at **the ceiling** — two reviews with the
same count: change the approach (a different angle, a different mode,
an interview for material) or bring the student the choice. Never relax
a criterion to let a draft pass.

## State

Owned: `students/<slug>/essays/` — shapes in `references/schema.md`.
Appends to `conversations.md` (new material the student gives, dated,
in their words). Reads the rest.

**Hands back:** a deadline or a new prompt → `app-tracker`; a school
fact the why-us needs → `college-research`; the finished essays → the
counselor package (it reads the author headers).

**Session close:** run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_package.py --check <student-slug>`
— the author-label check is code, not memory. No checker-subagent is
spawned — the student's words are theirs and the agent's carry their
label. **Outcomes, never narration**: say what the essay folder now
holds — the brief, the draft number, the review's count.

## Guardrails

- **Never invent an experience, an emotion, a quote, or a detail.
  Ever.**
- A student is never obligated to write their hardest experience. Ask
  once whether they want to; take the answer.

*Every reply ends with ONE next step — a sentence with its why, not a
menu.*
