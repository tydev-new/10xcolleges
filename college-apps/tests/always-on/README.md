# The conduct harness — how a case is built and judged

A skill's unit tests check structure. Its **conduct** — did the agent do
the right thing under a baited prompt — is measured here: a planted
workspace, one prompt, a real `claude -p` session with only the skills
under test, and an independent judge (a second model) scoring the reply
AND the files against a written expectation. Results are receipts
(`docs/evals/`), never assertions.

## The suite: e3 — multi-turn, the persona driver

One case carries the essay loop: `cases/e3-review-rounds/`. A second
model plays the student from `persona.md` (TRUE FACTS + a beat script by
message number); the agent's reply is fed back with `--continue`; the
judge grades only the Agent turns against `expected.md`, with the files
after the run and the tool log beside them. e1 (the "just write it"
bait) and e2 (one review round) are retired — e3's first turn is e2, and
the ghostwriting bait is a beat to add to a persona when it is wanted.

```
tests/always-on/cases/e3-review-rounds/
  persona.md       who she is, TRUE FACTS, BEHAVIOR SCRIPT by message, what she never says
  opener.txt       message 1           turns.txt   how many messages
  skills.txt       the skills planted  ws-seed/    the planted student folder
  expected.md      MUST / MUST NOT, each checkable from the transcript or the files
```

Write the bait the way it arrives in life, not as a test instruction.
Put the rule under test in the MUSTs by its observable consequence,
never by quoting the skill.

## Running

```bash
CASES=all TRIALS=2 ./run_e3.sh <tag>     # or CASES="<case> ..."
./judge_e3.sh <tag>
```

A fresh tag per measurement — a reused tag skips existing cases and the
runner says so. `TRIALS=2` minimum before a rule is called held;
`TRIALS=3` on a single case to separate noise from a miss. A run is ~15
minutes (four turns, sequential by nature); trials run concurrently.

## What the kit supplies, what the host fills

The runner template carries the parts that were earned by incident: the
**vault** (the real workspace is locked for the run — a harness session
once wrote into the founder's real files), **targeted by default**,
**bounded concurrency** (cases are independent processes), the
**reused-tag warning**, and `extract_text.py` / `dump_tools.py` (the
reply text and the tool log, the two things a judge and a debugger
read). The host fills four blocks: the real workspace path, the suite's
cases, how a workspace is planted, and what the judge sees afterward.

## Reading a result

```bash
for v in results/<suite>-<tag>/*.verdict.json; do python3 -c "
import json; d=json.load(open('$v')); print(d['case'], d['overall'], [c['item'] for c in d['criteria'] if c['verdict']=='fail'])"; done
```

Then read the fails' `evidence` before touching a skill. The lesson of
the rollout: a one-trial miss is a sighting, not a rule; a rule that
fails twenty trials under rewording is a design or stratum problem, not
a wording one — change the mechanism (a script, a placement, a
structure), never the sentence again.
