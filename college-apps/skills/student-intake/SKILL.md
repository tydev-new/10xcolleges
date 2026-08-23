---
name: student-intake
description: Use this skill when starting with a new student, when a school packet / transcript / resume / activities list / worksheet needs to go into the profile, or when something about the student changed (new scores, a new activity, a changed major). Builds profile.md (who they are) and criteria.md (what they want) in the student's own words, with a source on every line, up to the point where the college list can start.
---

# Intake — learn the student

## Goal

`profile.md` says who they are and `criteria.md` says what they want —
**every line in their words, every line marked with where it came from,
every blank a `TODO:` and never a guess** — up to the gate that what
comes next needs. **What comes next decides the gate.** Today that is
the essay: `college-list` is not built yet, so money and test numbers
are not asked for unless the student raises them. Scored by
`references/eval.md`; file shapes in `references/schema.md`.

| Must be true | Where |
|---|---|
| **The essay gate** (the default) — `check_record.py` counts it as `material N/3`: documents read, or "none" recorded · at least one activity with hours and *what actually happened* · **the major they are applying for**, and how sure ("undecided" counts) | `profile.md` |
| The conversation is recorded as it happens — what they said, word for word, dated — that is what the essay is built from; it is never asked for | `conversations.md` |
| **The list gate** (when `college-list` is next) — `gate N/4`: a budget **and who set it** (a guess counts as 0) · unweighted GPA, plus scores or the plan to test · a direction · one row each in Hard filters and Deal-breakers | `criteria.md`, `profile.md` |
| Documents copied into the template's sections, each line tagged with its source | `profile.md` |
| What they said, dated, in their exact words — the raw material the essays run on | `conversations.md` |
| A changed answer moves the old row to Retired with the reason — nothing is overwritten | `criteria.md § Retired criteria` |
| The reply says what is still `TODO:` and what happens next | the reply |

## Prerequisites

- **Required:** a working folder with a `CLAUDE.md` in it — none → run
  Setup first, before any write. Then a student folder
  `students/<slug>/` made from `${CLAUDE_PLUGIN_ROOT}/templates/student/`
  — none → create it (Setup does, or the first reply does). **Read
  `references/schema.md` and `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md`
  § Provenance before the first write** — that is where the exact row
  formats the script checks are written down.
- **Optional:** a packet, transcript, resume, activities list, or
  Common App export (PDF and DOCX can be read directly); a filled-in
  `${CLAUDE_PLUGIN_ROOT}/templates/criteria-worksheet.md` or the school's
  own form. With nothing in hand, the interview starts from question
  one. That is fine and common.

## Loops and sequences

Setup runs once per folder. Documents arrive in any order and are a
sequence. The interview is the loop. A change later on is a sequence.
Which one you are in depends on what just arrived, not on asking.

### Setup — the working folder (a sequence)

**Runs when** there is no `CLAUDE.md` in the session's folder. Usually
that folder is the right place — they chose it when they opened the
session. **Name it in your first reply and move on**, as a path they
could paste into a file manager, never "here": *"everything I write
lands in `<path>` — say the word if you'd rather use a different
folder."* It becomes a real question only when the folder looks wrong —
a home directory, a code repository, a system path, a folder full of
unrelated work. Then say what it is, by its path ("`<path>` is a code
project"), and ask, in this one sentence: *"Where should your
college files live? If you already have a folder from an earlier
session, point me there — otherwise I'll set one up at
`~/college-apps/`."* Ask for their full name in the same breath. **Nothing outside the
session folder is yours to look at: no `find`, `ls`, or search beyond
it — not for an earlier workspace, not for the plugin. The one
allowed look is a bare existence test of the folder they chose
(`[ -e ]`); never list or read inside it until you have created it.**
(The plugin's own folders under `${CLAUDE_PLUGIN_ROOT}` are yours to
read.) The plugin's templates are
at `${CLAUDE_PLUGIN_ROOT}/templates/`; if that variable is unset, ask
where the plugin is installed. **Nothing is written until the folder is settled, and creating a
directory is writing.** An occupied default is not yours to read — say
the name is taken and ask for another. **The first file written is the
workspace `CLAUDE.md`**, copied from
`${CLAUDE_PLUGIN_ROOT}/templates/workspace-CLAUDE.md` — rules before
facts. Then `students/<slug>/` from the student template — the slug is
first name and last initial, lowercase (`jordan-k`); with only a first
name in hand, use it now (`jordan`) and rename when the rest comes —
and the drop path for their documents, as a path:
`<path>/students/<slug>/documents/` — **and ask for the transcript and
the packet in the same reply**; they are the fastest route to the
numbers. Never wait on the name to create the folder. **Exits** when `CLAUDE.md` and the student folder exist and
the paths have been said. A folder with a `CLAUDE.md` is settled;
re-entry never asks again.

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

- **Standard:** (what each round is measured against) the gate for
  what comes next — the essay gate unless the list is next, listed
  above — and the profile's open `TODO:`s. **Budget:** as many turns as it takes;
  **at most two questions a turn, and the reply is short: what you
  wrote down, the gate line, the questions, one next step — no reasons
  for a question unless they ask.**
- **Each round** (the questions and their order: `references/patterns.md
  § The interview — getting there`): the gate items are asked before
  anything else — for the essay gate that is the documents and what
  actually happened in their activities; for the list gate, numbers and
  money → ask at most two → **write every row the
  moment it comes up, in their phrasing** — a budget to
  Hard filters, "I don't want to be cold" to Deal-breakers in those
  words, "near a city" to Preferences as Nice — tagged and dated → add
  what they said to `conversations.md` word for word → run
  `check_record.py` and **copy its gate line into the reply as printed**
  (`material N/3 — missing: …`) → follow whatever was alive in their answer, not the next item
  on a list.
- **Seven rules — each applies at the step it names:**
  1. **Your paraphrase is not their criterion.** "I don't want to be the
     least prepared person in the room" is a row; "prefers a supportive
     environment" is not. The paraphrase creeps in within the same turn,
     which is why the row is written while their words are on screen.
  2. **A hedged answer is still an answer.** "biology maybe, idk" is
     the major with *how sure: not very* — written down, tagged; `TODO:`
     is only for a question they haven't answered.
  3. **A guess is not a number.** A budget the student guessed is a row
     marked as their guess, `set by: nobody yet`, and the money
     conversation becomes the one piece of homework. A GPA given
     without "unweighted" is `TODO: unweighted GPA` until checked —
     students quote the weighted one and land a tier off.
  4. **A correction retires the old row; it never overwrites it.** "No,
     I said I *don't* want a city" moves the old row to `§ Retired
     criteria` with the reason, dated and tagged, and adds the new row.
     That trail is the most useful thing in the file three months on.
  5. **Never name a college.** Intake has no list. "What about Pomona?"
     becomes a row (`[student <date>]`, with why they named it) handed
     to `college-list`.
  6. **Ask about context once, gently, and take "rather not" as the
     answer.** A dip in grades, a job, caring for siblings — note
     whether they want it disclosed. The answer is theirs.
  7. **Never against other students.** No "most kids", no "thousands
     write that"; a caution names the fact, not them (`voice.md` rule
     5). Praise is specific or absent.

**Exits** when the gate is full **and** you have said back what you
heard in four or five sentences in their language, asked what you got
wrong, and put the correction into the files — then hand off to what
is next (`essay-coach` today; `college-list` when it exists). Or at **the ceiling** (the sign the loop is stuck) —
two rounds with the gate unchanged: name the one thing blocking it
(usually the money conversation), hand it over as homework with the Net Price Calculator,
and stop asking.

### Update (a sequence)

**Runs when** something changed — scores, an activity, a major, a
constraint — or `conversations.md` has lines newer than `profile.md`
(another skill heard something). Add the line, tagged and dated. Retire what it replaces,
with the reason. Run `check_record.py` again. **Exits** with the change
named and whether it moves the gate or the list.

## State

Owns `profile.md`, `criteria.md`, `conversations.md` (add at the end
only) — shapes in `references/schema.md`. Reads everything else in the
folder; the shape of a file it doesn't own is the owner's, found through
`${CLAUDE_PLUGIN_ROOT}/docs/data-model.md § Every file` (`meta.json`
belongs to `college-app`).

**Passes to:** essay gate met → `essay-coach` (the material is in
`profile.md` and `conversations.md`); list gate met → `college-list`; a
named college → a criteria row for `college-list`.

**Session close:** run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py students/<slug>`
(it lives at the plugin root, shared with the other skills). Fix FAILs
before the reply; for each WARN, say in the reply why it is acceptable.
No checker-subagent — the words are the student's. Say what the folder now holds, the script's
gate line, what is `TODO:`, and the next step.

## Guardrails

- Nothing goes in the files that the student, a parent, a counselor, or
  a document did not say — and the tag says which one.

*Every reply ends with ONE next step — a sentence with its why, not a
menu.*
