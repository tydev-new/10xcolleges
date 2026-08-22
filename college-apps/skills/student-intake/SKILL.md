---
name: student-intake
description: Use this skill when starting with a new student, when a school packet / transcript / resume / activities list / worksheet needs to go into the profile, or when something about the student changed (new scores, a new activity, a changed major). Builds profile.md (who they are) and criteria.md (what they want) in the student's own words, with a source on every line, up to the point where the college list can start.
---

# Intake — learn the student

## Goal

`profile.md` says who they are and `criteria.md` says what they want —
**every line in their words, every line marked with where it came from,
every blank a `TODO:` and never a guess** — up to the gate the list
needs. Scored by `references/eval.md`; file shapes in
`references/schema.md`.

| Must be true | Where |
|---|---|
| The four gate items — `check_record.py` counts them: a budget **and who set it** (a guess counts as 0) · unweighted GPA, plus test scores or the plan to test · a direction, with how sure ("undecided" counts) · one row each in Hard filters and Deal-breakers | `criteria.md`, `profile.md` |
| Documents copied into the template's sections, each line tagged with its source | `profile.md` |
| What they said, dated, in their exact words — the raw material the essays run on | `conversations.md` |
| A changed answer moves the old row to Retired with the reason — nothing is overwritten | `criteria.md § Retired criteria` |
| The reply says what is still `TODO:` and what happens next | the reply |

## Prerequisites

- **Required:** a student folder `students/<slug>/` made from
  `${CLAUDE_PLUGIN_ROOT}/templates/student/`. If there is none, create
  it from the template in the first reply, then carry on. **Read
  `references/schema.md` and `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md`
  § Provenance before the first write** — that is where the row forms
  the checker reads are.
- **Optional:** a packet, transcript, resume, activities list, or
  Common App export (PDF and DOCX can be read directly); a filled-in
  `${CLAUDE_PLUGIN_ROOT}/templates/criteria-worksheet.md` or the school's
  own form. With nothing in hand, the interview starts from question
  one. That is fine and common.

## Loops and sequences

Documents arrive in any order and are a sequence. The interview is the
loop. A change later on is a sequence. Which one you are in depends on
what just arrived, not on asking.

### Documents (a sequence)

**Runs when** a file is in the folder or pasted into chat. Read the
whole thing. Copy it into `profile.md` under the template's sections and
tag every line (`[packet]`, `[transcript]`, `[worksheet]`). Reflection
answers go in **word for word** — "I fixed the robot a lot" is essay
material only in their grammar. Every blank becomes a `TODO:` on its
own line. Put numbers on activities (hours a week, weeks a year, years)
where the packet doesn't — ask, don't estimate. **Exits** when
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py students/<slug>`
passes and the `TODO:`s are named in the reply.

### The interview (the loop)

**Runs when** the student is talking — with or without documents.

- **Standard:** the gate (four items, above) and the profile's open
  `TODO:`s. **Budget:** as many turns as it takes; two or three
  questions a turn, never a wall of them.
- **Each round** (the questions and their order: `references/patterns.md
  § The interview — getting there`): ask two or three questions → **write
  every row the moment it comes up, in their phrasing** — a budget to
  Hard filters, "I don't want to be cold" to Deal-breakers in those
  words, "near a city" to Preferences as Nice — tagged and dated → add
  what they said to `conversations.md` word for word → run
  `check_record.py` and repeat its `gate N/4` line and what is still
  open → follow whatever was alive in their answer, not the next item
  on a list.
- **Five rules, each at its moment:**
  1. **Your paraphrase is not their criterion.** "I don't want to be the
     least prepared person in the room" is a row; "prefers a supportive
     environment" is not. The paraphrase creeps in within the same turn,
     which is why the row is written while their words are on screen.
  2. **A guess is not a number.** A budget the student guessed is a row
     marked as their guess, `set by: nobody yet`, and the money
     conversation becomes the one piece of homework. A GPA given
     without "unweighted" is `TODO: unweighted GPA` until checked —
     students quote the weighted one and land a tier off.
  3. **A correction retires the old row; it never overwrites it.** "No,
     I said I *don't* want a city" moves the old row to `§ Retired
     criteria` with the reason, dated and tagged, and adds the new row.
     That trail is the most useful thing in the file three months on.
  4. **Never name a college.** Intake has no list. "What about Pomona?"
     becomes a row (`[student <date>]`, with why they named it) handed
     to `college-list`.
  5. **Ask about context once, gently, and take "rather not" as the
     answer.** A dip in grades, a job, caring for siblings — note
     whether they want it disclosed. The answer is theirs.

**Exits** when the gate is `4/4` **and** you have said back what you
heard in four or five sentences in their language, asked what you got
wrong, and written down the correction — then hand off to
`college-list`. Or at **the ceiling** — two rounds with the gate
unchanged: name the one thing blocking it (usually the money
conversation), hand it over as homework with the Net Price Calculator,
and stop asking.

### Update (a sequence)

**Runs when** something changed — scores, an activity, a major, a
constraint. Add the line, tagged and dated. Retire what it replaces,
with the reason. Run `check_record.py` again. **Exits** with the change
named and whether it moves the gate or the list.

## State

Owns `profile.md`, `criteria.md`, `conversations.md` (append-only) —
shapes in `references/schema.md`. Reads everything else in the folder
(`meta.json` belongs to `college-app`).

**Hands off:** gate met → `college-list`; a named college →
`college-list`; essay-worthy lines are already in `conversations.md`
for `essay-coach` to find.

**Session close:** run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py students/<slug>`
(it lives at the plugin root, shared with the other skills). Fix FAILs
before the reply; explain WARNs in it. No checker-subagent — the words
are the student's. Say what the folder now holds, the script's
`gate N/4`, what is `TODO:`, and the next step.

## Guardrails

- Nothing goes in the files that the student, a parent, a counselor, or
  a document did not say — and the tag says which one.

*Every reply ends with ONE next step — a sentence with its why, not a
menu.*
