# First wave — intake and essay-coach, made solid before user testing (2026-08-22)

The founder paused new skills to harden the two that ship first. This is
the ledger: every measurement, what moved, what is still watched. The
per-skill records (`eval-e3-essay-rounds.md`, `eval-i1-intake.md`,
`eval-e1-essay-coach-pilot.md`) hold the earlier rounds.

## The cases

| Case | Skill | What it tests |
|---|---|---|
| e4-late-read | essay-coach | two turns: review, then her per-criterion read arriving late (one wrong on purpose) — the late-read rule alone |
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
| sweep5 (×3, serial) | i2: a bare existence test is the one allowed look; wrong folder named by its path; case runs serially | — | — | **3/3** | no `find /` in any tool log; the law held 3/3; t2 first judged fail for listing the plugin's own `templates/` and the workspace it had just made — the expectation said "ours vs theirs" badly; clarified (the plugin and the created workspace are ours) and re-judged: pass |

## What is solid

- **Late read (e4): 3/3** — logged in full in her words, review untouched, every disagreement named with the score held. The student's read is optional (offered once per essay, never pressed).

- **Setup (i2): 3/3** on sweep5 after 0/3 → 0/3 → 1/3 → 0/3: four rounds of finding the real cause (no slug rule → a stalled name question → plugin-hunting with `find /` → a rule that contradicted itself → a harness collision).

- **Intake interview (i1): 3/3** on the sweep, after 0/2 → 1/2 in its own rounds. The gate is computed by `check_record.py`; a guessed budget never counts; rows land in the turn they were said; corrections retire rows; no college is ever evaluated.
- **Essay rounds (e3): 2/3 twice**, each miss a different single thing, with the two repeat misses now ruled (the coach folding to the student's read; a late read logged partially). Files, headers, the Rounds trail, the ceiling, and the cold reader have held in every trial since mt2.

## What is watched

- e3: a criterion marked met against its own quoted evidence (1 sighting, mt4).
- i1: a round that asks no question (1 sighting, i1v2).
- i2: none open — the disk-search ban held 3/3 once it named the plugin too and allowed the one existence test.

## Harness lessons earned here

- A case that writes to the real home directory runs serially (`serial` marker) — parallel trials see each other.
- The judge reads the tool log: "no search outside the session folder" is checked against calls, not claims.
- A rule that needs a fact ("say the default is taken") must allow the one look that gets it.

## From the first live exchange (Isabel T., 2026-08-22)

The founder ran intake live and called it verbose, not collecting the
profile, and "mean" (comparing her to other students). Each traced to
the skill: no reply-length rule; the interview order put the numbers
sixth and never asked for the transcript; nothing forbade "thousands of
kids write that". And the gate itself was the college list's, though
only essay-coach ships — so intake was asking for budgets and GPA kinds
the essay never needs.

| Run | Change | i1 | What held · what missed |
|---|---|---|---|
| voice1 (×3) | reply shape (≤2 questions, short, no rationale unless asked); transcript asked at Setup; gate items before the alive thread; voice rule 5 (never against other students); i1 judges tone/length/order | 0/3 (list gate still in play) | lengths 160–195 → 70–90 on turn 4 (Isabel's were ~300+); tone clean 3/3; one `find /` for the checker during the interview (ban lived only in Setup) |
| voice2 (×3) | **what comes next decides the gate**: essay gate `material N/3` (documents · an activity with what happened · the major, how sure); money/test numbers not asked unless raised; conversation recorded as it happens, never asked for | 0/3 | nothing asked the essay doesn't need 3/3; tone clean; misses: gate line paraphrased away (script ran 8×), "biology maybe, idk" filed as TODO, one turn 285w of meta-rationale, `find /` 2/3 |
| voice3 (×3) | Tier 0: nothing outside this folder, plugin at `CLAUDE_PLUGIN_ROOT`; gate line copied as printed; a hedged answer is an answer | **2/3** | `find /` 0/3; lengths 68–225; t1 slid to the list gate after he volunteered a budget (assigned GPA/budget homework) — single sighting; one reworded quote |

