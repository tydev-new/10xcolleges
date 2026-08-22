# The conduct harness — how a case is built and judged

A skill's unit tests check structure. Its **conduct** — did the agent do
the right thing under a baited prompt — is measured here: a planted
workspace, one prompt, a real `claude -p` session with only the skills
under test, and an independent judge (a second model) scoring the reply
AND the files against a written expectation. Results are receipts
(`docs/evals/`), never assertions.

## A case

```
tests/always-on/cases/<suite>-<name>/
  prompt.md        what the candidate says — carry the bait in natural form
  expected.md      MUST / MUST NOT, each checkable from the transcript or the files
  ws-seed/         the planted workspace: the state that makes the bait real
```

Write the bait the way it arrives in life ("6 active vs 5, with the
Interested one"), not as a test instruction. Put the rule under test in
the MUSTs by its observable consequence, never by quoting the skill.

## Running

```bash
CASES="<case> ..." TRIALS=2 ./run_<suite>.sh <tag>   # targeted (default); CASES=all for the suite
./judge_<suite>.sh <tag>                             # judges whatever the tag holds
```

A fresh tag per measurement — a reused tag skips existing cases and the
runner says so. `TRIALS=2` minimum before a rule is called held;
`TRIALS=3` on a single case to separate noise from a miss.

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
