---
name: student-intake
description: Use this skill when starting with a new student, when a school packet / transcript / resume / activities list / worksheet needs to go into the profile, or when something about the student changed (new scores, a new activity, a changed major). Builds profile.md (who they are) and criteria.md (what they want) in the student's own words, source-tagged, to the gate the college list needs.
---

# Intake — learn the student

## Goal

`profile.md` says who they are and `criteria.md` says what they want —
**every line in their words, every line tagged with where it came from,
every blank a `TODO:` and never a guess** — to the gate the list runs on.
Scored by `references/eval.md`; shapes in `references/schema.md`.

| Must be true | Where |
|---|---|
| The four gate items — `check_record.py` counts them: a budget **and who set it** (a guess is 0) · unweighted GPA, and scores or the plan to test · a direction, with how sure ("undecided" counts) · one row in each of Hard filters and Deal-breakers | `criteria.md`, `profile.md` |
| Documents transcribed into the template's sections, each line tagged | `profile.md` |
| What they said, dated, verbatim — the raw material the essays run on | `conversations.md` |
| A changed answer retires the old row with its reason — nothing overwritten | `criteria.md § Retired criteria` |
| What is still `TODO:` is said out loud, and what happens next | the reply |

## Prerequisites

- **Required:** a student folder `students/<slug>/` from
  `${CLAUDE_PLUGIN_ROOT}/templates/student/` — none → create it from the
  template in the first reply, then proceed. **Read `references/schema.md`
  and `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md` § Provenance before the
  first write** — the row forms the checker reads live there.
- **Optional:** a packet, transcript, resume, activities list, Common App
  export (PDF/DOCX read directly); a filled
  `${CLAUDE_PLUGIN_ROOT}/templates/criteria-worksheet.md` or the school's
  own form. Nothing in hand → the interview starts from question one,
  which is fine and common.

## Loops and sequences

Documents arrive in any order and are a sequence; the interview is the
loop; a change later is a sequence. Which one you are in is decided by
what just arrived, not by asking.

### Documents (a sequence)

**Runs when** a file is in the folder or pasted. Read it whole;
transcribe into `profile.md` under the template's sections; tag every
line (`[packet]`, `[transcript]`, `[worksheet]`); reflection answers go
in **verbatim** — "I fixed the robot a lot" is essay material only in
their grammar; every blank is `TODO:` on its own line. Quantify
activities (hrs/wk, wks/yr, years) where the packet doesn't — ask, don't
estimate. **Exits** when `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py
students/<slug>` passes and the `TODO:`s are named in the reply.

### The interview (the loop)

**Runs when** the student is talking — with or without documents.

- **Standard:** the gate (four items, above) and the profile's open
  `TODO:`s. **Budget:** as many turns as it takes; two or three questions
  a turn, never a wall.
- **Each round** (the questions and the order: `references/patterns.md
  § The interview — getting there`): ask two or three → **write every
  row the moment it surfaces, in their phrasing** — a budget to Hard
  filters, "I don't want to be cold" to Deal-breakers in those words,
  "near a city" to Preferences as Nice — tagged and dated → append what
  they said to `conversations.md` verbatim → run `check_record.py` and
  say its `gate N/4` line and what's still open → follow what was alive
  in their answer, not the next item on a list.
- **Five things bind at their moment:**
  1. **Your paraphrase is not their criterion.** "I don't want to be the
     least prepared person in the room" is a row; "prefers a supportive
     environment" is not — and the paraphrase arrives within the turn,
     which is why the row is written while the words are on screen.
  2. **A guess is not a number.** A budget the student guessed is a row
     tagged as their guess, `set by: nobody yet`, and the money
     conversation becomes the one homework. A GPA quoted without
     "unweighted" is `TODO: unweighted GPA` until checked — students
     quote the weighted one and land a tier off.
  3. **A correction retires, never overwrites.** "No, I said I *don't*
     want a city" moves the old row to `§ Retired criteria` with the
     reason, dated and tagged, and adds the new one. The trail is the most useful thing in
     the file three months on.
  4. **Never a college name.** Intake has no list; "what about Pomona?"
     becomes a row (`[student <date>]`, why they named it) handed to
     `college-list`.
  5. **Context is asked once, gently, and "rather not" is the answer.**
     A dip, a job, caring for siblings — note whether they want it
     disclosed; the answer is theirs.

**Exits** when the gate is `4/4` **and** you have reflected it back in
four or five sentences in their language, asked what you got wrong, and
taken the correction — then hand to `college-list`; or at **the
ceiling** — two rounds with the gate unmoved: name the one thing
blocking it (usually the money conversation), hand it over as homework
with the Net Price Calculator, and stop asking.

### Update (a sequence)

**Runs when** something changed — scores, an activity, a major, a
constraint. Add the line tagged and dated; retire what it replaces with
the reason; rerun `check_record.py`. **Exits** with the change named
and whether it moves the gate or the list.

## State

Owned: `profile.md`, `criteria.md`, `conversations.md` (append-only) —
shapes in `references/schema.md`. Read only: everything else in the
folder (`meta.json` is `college-app`'s).

**Hands back:** gate met → `college-list`; a named college →
`college-list`; essay-worthy lines are already in `conversations.md`
for `essay-coach` to find.

**Session close:** run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py
students/<slug>` (at the plugin root — shared with the other skills);
FAILs fixed before the reply; WARNs defended in it. No checker-subagent
— the words are the student's. Say what the folder now holds, the
script's `gate N/4`, what is `TODO:`, and the next step.

## Guardrails

- Nothing in the files that the student, a parent, a counselor, or a
  document did not say — and the tag says which.

*Every reply ends with ONE contextual next step — a sentence with its
why, not a menu.*
