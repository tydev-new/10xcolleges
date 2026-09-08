---
name: major-fit
description: Discover, validate, and strategically select college majors and adjacent alternatives. Use when a student is undecided, exploring options, wondering if a major like CS or Pre-Med is too competitive, or looking for adjacent majors with strong career paths and better admit rates. Produces academic-direction.md and updates profile.md.
---

# Major Fit — intellectual direction & strategy

## Goal

Build `students/<slug>/academic-direction.md` and sync `profile.md § Goals and direction` — **every claim grounded in transcript coursework and student flow, every alternative evaluated against institutional transfer reality, every insight tagged with its source** — scored by `references/eval.md`; file schema in `${CLAUDE_PLUGIN_ROOT}/schemas/academic-direction.md`.

| Must be true | Where |
|---|---|
| **Primary major + confidence:** Primary direction declared with authentic intellectual core | `academic-direction.md`, `profile.md` |
| **Coursework stamina:** Demonstrated flow and friction tolerance cited from courses and projects | `academic-direction.md` |
| **At least 2 adjacent majors:** Viable alternatives mapped with career outcomes and admissions advantage | `academic-direction.md` |
| **Institutional transfer realities:** Direct-admit gates and transfer lockouts explicitly noted | `academic-direction.md` |
| **Essay "Red Thread":** Concrete origin spark, troubleshooting moment, and open question for essays | `academic-direction.md` |
| **Verbatim conversation log:** Student statements quoted word-for-word in quotes with dates | `conversations.md` |

---

## Prerequisites

- **Required:** `students/<slug>/profile.md` (coursework, grades, activities, reflections) and `conversations.md`.
- Output: `students/<slug>/academic-direction.md` following `schemas/academic-direction.md`.
- Synchronizes with: `profile.md § Goals and direction` (`Intended major`, `How sure are they?`).

---

## Sequences and loops

### The coursework & flow audit (a sequence)

**Runs when** a student is undecided, expresses uncertainty about their major, or asks what else fits their strengths.

1. Review `profile.md`'s senior year classes, school activities, and "What excites them" / "What turns them off".
2. Audit coursework stamina using the Sunday night flow test: Which classes or projects does the student do first? Where do they tolerate friction (debugging, revisions, lab troubleshooting) without quitting?
3. Verify prerequisite coursework on the transcript (e.g., Calculus pathway for engineering, economics, or CS; lab chemistry and biology for pre-med).

**Exits** when the student's core intellectual flow and verified academic foundations are identified.

### Strategy & adjacent mapping (the loop)

**Runs when** evaluating candidate majors against admissions selectivity and career trajectories.

- **Standard:** The 5-dimension rubric in `references/eval.md`.
- **Budget:** 3 rounds of exploration per session.
- **Each round:**
  1. *Identify Primary & Adjacent Majors:* Map the core flow to a primary major, plus at least two high-leverage adjacent majors (e.g. Cognitive Science or Informatics for CS; Operations Research or Applied Economics for Finance; Public Health or Neuroscience for Pre-Med).
  2. *Audit Institutional Realities:* Flag direct-admit pre-major gates (e.g. Purdue FYE) and transfer lockouts (e.g. UIUC/Washington CS/Engineering) where backdoor major transfers are impossible.
  3. *Capture the Essay Red Thread:* Elicit the student's authentic origin spark, a memorable friction moment, and an unresolved question for upcoming "Why Major" supplemental essays.
  4. *Write/Update Dossier:* Write `students/<slug>/academic-direction.md` following `schemas/academic-direction.md`.
  5. *Sync Profile:* Update `- **Intended major:**` and `- **How sure are they?**` in `profile.md § Goals and direction` with `[student YYYY-MM-DD]`.
- **Seven moment rules:**
  1. **Never ask "What do you want to be when you grow up?":** Ask the Sunday night flow test instead — which subject absorbs them when no one is grading them?
  2. **The transcript must earn the major:** Do not validate a STEM or business major without checking the math and science prerequisites on the transcript.
  3. **Never recommend a backdoor gimmick major:** Warn against applying to an unrelated low-admit major (e.g. Classics or Forestry) with the secret intent to transfer into a locked department.
  4. **Always provide at least two adjacent majors:** Introduce high-value, lower-crowded alternatives that lead to identical career or graduate outcomes.
  5. **Respect genuine undecidedness:** If a student is undecided, focus on un-siloed liberal arts colleges and universities (where exploring is built-in) rather than siloed technical flagships.
  6. **Sync profile and conversations immediately:** Keep `profile.md` and `conversations.md` aligned with the student's latest stated direction.
  7. **Run `check_major.py` last:** Execute `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_major.py students/<slug>/academic-direction.md` as the absolute final tool call before replying.
- **Exits** when `academic-direction.md` passes `check_major.py`, primary and adjacent majors are agreed upon, and `profile.md` is updated. Ceiling: two rounds with unchanged adjacent recommendations.

---

## State

Owns `students/<slug>/academic-direction.md` — schema in `${CLAUDE_PLUGIN_ROOT}/schemas/academic-direction.md`. Appends to `conversations.md` and updates `profile.md § Goals and direction`.

**Passes to:**
- Primary and adjacent majors → `college-list` for departmental selectivity tiering
- Major requirements & transfer lockouts → `college-research` for departmental audits
- Intellectual Red Thread & essay hooks → `essay-coach` for "Why Major" supplements

---

## Session close

Before replying to the student on EVERY turn:
1. Sync `profile.md` and `conversations.md`.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_major.py students/<slug>/academic-direction.md` as the absolute final tool call. Fix any script FAILs before replying. Never reply without running `check_major.py` last.
3. Every reply ends with ONE next step and its why. No checker subagent runs because intellectual direction belongs to the student.
