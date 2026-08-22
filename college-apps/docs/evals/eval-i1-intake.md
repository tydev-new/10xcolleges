# Eval — i1-intake-rounds: a thin packet, then three interview turns (2026-08-22)

Issue #2. `student-intake` to the shape: Documents (sequence) · the
interview (the loop, scored `gate N/4`) · Update (sequence); the law in
`scripts/check_record.py` (source tags, dated for people; a `TODO:` never
carries a value or a hedge; GPA kind; `set by`; append-only log; and the
gate count). Case: `tests/always-on/cases/i1-intake-rounds` — Jordan K.,
half-blank packet; a simulated student mentions a job not in the packet,
a deal-breaker verbatim, guesses a budget his parents never set, asks
about his cousin's college, corrects the reflect-back. The runner
snapshots `students/` after every turn so "rows as they surface" is
visible to the judge.

| Run | Skill state | Result | What held · what missed |
|---|---|---|---|
| i1v1 | as built, before review fixes (gate self-counted) | 0/2 | held 2/2: packet transcribed and tagged, blanks `TODO:`, GPA not taken as unweighted, rows landed in the turn they surfaced, the budget guess recorded as a guess, UC Davis written down and not evaluated, the city correction retired not overwritten. Missed: **t2 counted the guessed budget → "gate 4/4"** (review finding #1, the self-reported score); t1 omitted the gate line one turn; two `TODO:`s filled by inference ("TODO: no", "implies ~11th grade") |
| i1v2 | after the review's 19 findings: `check_record.py` prints `gate N/4`; labelled `TODO: <value>` caught; dated people-tags; Retired shape = template | **1/2** | t2 pass on every MUST. Gate discipline 2/2 — the guess excluded both trials. t1: records clean but **zero questions asked in turns 2–4**; the alive thread (garden center) unpursued; no reflect-back |

What it settled:

- The score moved to code and the inflation stopped: `gate N/4` is the
  script's line, and a guessed budget is 0 in both trials.
- The record laws hold under a multi-turn intake: tags, `TODO:`
  discipline, per-turn row landing, retire-not-overwrite, no college
  evaluated — 4/4 trials across both runs.

Open (single sightings, watched):

- The interview stops interviewing (i1v2 t1): the loop's "ask two or
  three" did not fire for three rounds. If it recurs, the moment is the
  reply's close — a round with no question is not a round.
- Light rewording of quotes in rows (i1v2 t2, soft): "in their phrasing"
  is judged, not checked.
- `check_record.py` cannot see a `TODO:` filled by a non-numeric
  inference ("TODO: no"); eval.md says so.

Accepted deviations from the review: loop 415w (under the 600 hard cap);
the checker at the plugin root like essay-coach's; college-list's
receiving check unconverted (its own conversion).
