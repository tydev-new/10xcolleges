# kit/ — the skill shape, portable

Everything about how these skills are built that is not about job
search, in one place, so a second product (10xcolleges is the first)
adopts the same principles, shape, checker, and harness without
copying them by hand — and so a fix lands once.

## What is in the kit, and where the one authoritative copy lives

| Piece | Lives at | In the kit as |
|---|---|---|
| The build rules (Part 2 of the principles: believe the disk, one of everything, every rule derivable or earned, evidence decides, plain language) | `../PRINCIPLES.md § Part 2` | `PRINCIPLES-core.md` — a verbatim extract, guarded by `tests/test_kit.py` |
| The shape — five files, the loop skeleton, the alignment rules, how to convert a skill | `../docs/skill-shape.md` | not copied; read it there |
| The process — design gate → review → dogfood → harness → closing review | `../docs/PROCESS.md` | not copied; read it there |
| The checker core — schema parser, section check, declared tables, round-record check, the link rung | `../skills/profile/scripts/check_files.py` | `shapecheck.py` — the domain-neutral functions, guarded byte-identical by `tests/test_kit.py` |
| The invariants — what must be true of every skill in a `skills/` directory | — | `tests/test_invariants.py`, parameterized by `SKILLS_ROOT` |
| The conduct harness — runner, judge, the two helpers, how to write a case | `../tests/always-on/` (the live suites) | `harness/` — templates with four host blocks to fill |

## What a host writes itself

- **Part 1 of its principles** — the promises to its user. For job
  search: nothing enters the résumé unruled, the human fires every
  gate, honest numbers. For colleges the law is the ghostwriting
  boundary and the counselor package; write it before converting a
  skill, because every skill's `eval.md` answers to it.
- **The checker's host constants** — the workspace manifest (which
  files may exist, who owns each), the history-table headers, any
  declared tables — in its own `check_files.py` that imports or copies
  `shapecheck.py`.
- **One conduct case per skill**, with the bait that skill's law
  forbids, and the host blocks of the runner/judge.
- **The close-out contract at Tier 0** — whatever must hold on every
  reply regardless of which skill did the work goes in the workspace
  rules file every skill loads, not in one skill (earned 2026-08-22:
  three rounds of 0/2 until it moved).

## Adopting it in a new repo

1. Vendor `kit/` (a one-way copy; record the source commit).
2. Write Part 1; adopt `PRINCIPLES-core.md` as Part 2 unchanged.
3. Pilot ONE skill to the shape (the one with a loop and a record
   already — for colleges, essay-coach: its brief is already
   FIXED/LIVING, its drafts are already a round record). Independent
   review, then its first conduct case, then measure.
4. Point `SKILLS_ROOT` at the repo's `skills/` and run
   `tests/test_invariants.py`; it is red until every skill is in, and
   it names where.
5. Convert the rest skeleton-first; each gets a review and a case.

## Running the kit's tests here

```bash
python3 tests/run.py            # the host suite includes kit/tests via its runner
SKILLS_ROOT=/path/to/other/skills python3 -c "import sys; sys.path.insert(0,'kit/tests'); import test_invariants as t; [getattr(t,n)() for n in dir(t) if n.startswith('test_')]"
```
