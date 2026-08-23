# First wave — intake and essay-coach, made solid before user testing (2026-08-22)

The founder paused new skills to harden the two that ship first. This is
the ledger: every measurement, what moved, what is still watched. The
per-skill records (`eval-e3-essay-rounds.md`, `eval-i1-intake.md`,
`eval-e1-essay-coach-pilot.md`) hold the earlier rounds.

## The cases

| Case | Skill | What it tests |
|---|---|---|
| e3-review-rounds | essay-coach | four turns with a simulated student: review → her own read (one criterion wrong on purpose) + a new fact → draft-02 → draft-03 that changes nothing (the ceiling) |
| i1-intake-rounds | student-intake | a half-blank packet, then three interview turns: a job not in the packet, a deal-breaker verbatim, a guessed budget, a cousin's college, a correction at reflect-back |
| i2-setup-in-a-repo | student-intake (Setup) | the session opened inside a code repo with no `CLAUDE.md`; two turns |

## The sweeps

| Run | Skill state | e3 | i1 | i2 | What moved |
|---|---|---|---|---|---|
| sweep1 (×3) | after the plain-language pass; Setup new | 2/3 | **3/3** | 0/3 | e3: coach agreed with her wrong "specific to Pomona — yes" (3rd sighting → rule). i2: the law held 3/3 (ask, write nothing, `CLAUDE.md` first); every fail was the slug `jordan` — no slug rule existed |
| sweep2 (×3) | e3: "their read never moves yours"; i2: slug rule | 2/3 | — | 0/3 | e3: the new rule held 3/3; t2 logged her read partially (2nd sighting → "every criterion they scored"). i2: stalled waiting for a last name the persona never gave (case bug); **`find /` across the disk in 2/3** |
| sweep3 (×3) | i2: fixed folder question, disk-search ban, slug never blocks, persona gives her name | — | — | 1/3 | `find / -iname student-intake` in 2/3 — hunting for the **plugin**, not a workspace, with the variable set; the ban was written only against workspace hunting |
| sweep4 (×3) | i2: ban widened to "nothing outside the session folder, not for the plugin either" | — | — | 0/3 | **harness bug**: three parallel trials shared the real `~/college-apps`; t1 found it occupied (t2 made it) and read the other trial's files. Also: agents `ls` the default to see if it is occupied — which my own rule requires knowing and forbids checking |
| sweep5 (×3, serial) | i2: a bare existence test is the one allowed look; wrong folder named by its path; case runs serially | — | — | _pending_ | |

## What is solid

- **Intake interview (i1): 3/3** on the sweep, after 0/2 → 1/2 in its own rounds. The gate is computed by `check_record.py`; a guessed budget never counts; rows land in the turn they were said; corrections retire rows; no college is ever evaluated.
- **Essay rounds (e3): 2/3 twice**, each miss a different single thing, with the two repeat misses now ruled (the coach folding to the student's read; a late read logged partially). Files, headers, the Rounds trail, the ceiling, and the cold reader have held in every trial since mt2.

## What is watched

- e3: a criterion marked met against its own quoted evidence (1 sighting, mt4).
- i1: a round that asks no question (1 sighting, i1v2).
- i2: see sweep5.

## Harness lessons earned here

- A case that writes to the real home directory runs serially (`serial` marker) — parallel trials see each other.
- The judge reads the tool log: "no search outside the session folder" is checked against calls, not claims.
- A rule that needs a fact ("say the default is taken") must allow the one look that gets it.
