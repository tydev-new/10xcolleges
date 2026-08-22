# Eval — e3-review-rounds: three rounds with the student in the loop (2026-08-22)

The multi-turn case (`tests/always-on/cases/e3-review-rounds`): a second
model plays Maya R. from `persona.md`; four agent turns — review of
draft-01 → her own read (one criterion wrong on purpose) + a new fact →
draft-02 pasted → draft-03 pasted, same essay reordered. It replaces e2,
which was its first turn. Judge: opus, against `expected.md`, Agent turns
only; what was built for it: `brief.md § Living ### Rounds` (one row per
review — the count trail the ceiling reads), `check_draft.py` FAILs a
review without its row.

| Run | Change | Result | What the misses were |
|---|---|---|---|
| mt1 | the case, the Rounds table | 0/2 | **the simulator re-sent message 3 at turn 4** (both trials) — the agent rightly declined to re-review identical text; turns 1–3 clean on files, counts, headers, Rounds, conversations.md; her late read of draft-01 (arrives after review-01) vanished in both — the skill said nothing about a read that arrives after its review; t2 dodged naming the wrong criterion |
| mt2 | the sim is told which beat is due by number (kit 221a8d2); run on the pre-clause skill | 0/2 | draft-03 arrived; **the ceiling named in both trials** ("tied at 4/5 with round 2 … bring you the actual choice"); Rounds trail 3 rows; late read still lost (t1 claimed it was appended — hard fab), t2 **back-edited review-01.md** to insert it and said "your reads matched mine" on the wrong criterion |
| mt3 | loop clause: a read arriving after its review → `conversations.md` in their words, reply names each differing criterion, the review stays as written; loop trimmed 691→596w | **1/2** | t2 pass, all four turns; t1 logged only two of her lines (weather, Green Bikes), not the per-criterion read; soft: attributed the brief's "the essay everyone writes" to her |

What it settled:

- The loop's instruments work end to end: the rubric sits fixed in the
  brief, every review leaves a Rounds row, the count moves only when the
  draft moves, and two equal rows produce the ceiling move — a choice
  brought to the student, never a relaxed criterion.
- A pasted draft is saved under her header before review (4/4 trials
  from mt2 on); no agent draft appeared anywhere.
- The late read was a real hole: the skill bound "take their read first"
  to the turn it arrives in and said nothing about the next turn. One
  clause at the moment moved it 0/4 → 1/2 (+ a half).

Open:

- The late read logged partially (mt3 t1) — watched; one sighting under
  the rule.
- The cold reader still has no trace beyond the three lines in the
  review; mt3 t1's "both cold reads named that image" is unverifiable
  (soft fab).
- Harness note: `run_e1.sh` planted no skill from 4ca6182 until fixed
  today — see the pilot record's correction.
