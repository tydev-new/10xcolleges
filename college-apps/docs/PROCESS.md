# The working process — how a change gets built here

The ritual, scaled to this repo's size from the sibling 10xjobs project's
`docs/PROCESS.md`, where each step carries the receipt of the failure that earned it.
Steps adopted here keep those receipts by reference; steps this repo has since earned
its own receipts for say so inline.

**Precedence chain for every judgment:** `../../PRINCIPLES.md` → `design.md` →
`data-model.md` and the skills. A conflict means one of them is wrong — fix the
chain, never pick a winner ad hoc.

## The ritual, in order

1. **Design gate before building.** Destination, assumptions with falsifiers,
   tradeoffs, test plan — recorded (GitHub issue, or a dated design doc in `docs/`)
   before code or prose changes. Explicit rejections are recorded too, so bad ideas
   don't get re-imported later.
2. **Build with the enforcement split** (`design.md § Enforcement`): one right
   answer → code (checkers, build refusals, tests); judgment → skill prose bound to
   the exact moment it fires, with its reason stated.
3. **Independent review before closing.** An agent that did NOT build it reviews
   against the full precedence chain plus consumer seams, findings with file:line
   evidence. The author never grades their own build — **and the reviewer verifies
   the fixes**, never only the fixer. *(This repo's own receipt, 2026-08-17: the
   Phase 1–2 reviewer found three real defects the author's tests missed, and the
   fix-pass verification caught an incomplete fix the fixer had called done.)*
4. **Dogfood: one student through the touched arc.** Before a skill change is done,
   walk a real or fully-realistic student through the stages it touches. The live
   run is the acceptance test AND the design input for what the conduct harness
   should bait next.
5. **Conduct case(s) after the live run.** Planted workspace, the exact failure
   baited, LLM judge, multi-trial majority (`tests/conduct/README.md` — including
   the environment contract and "judge inputs are inputs"). On any failure: ONE
   moment-bound change, re-run, record before/after. Any hard fabrication blocks
   the phase.
6. **A dated record.** Eval results land in `docs/eval-*.md` and are never edited
   afterward — a record describes what was measured on a date; its subject may have
   changed since, the record doesn't.
7. **Close with receipts.** The closing statement says what was verified and how,
   not what was intended. Durable lessons go in the repo (docs, commit messages,
   this file) — never only in a session's memory.

## The non-negotiables

- **Patch, verify, and commit share one command block** — a commit that claims an
  unverified change is a lie. Grep the disk before believing any "written/fixed".
- **Author contamination:** whoever built it doesn't test or review it alone.
- **A conduct pass counts only if the environment could express the failure** — and
  a judge's verdict counts only if the judge's inputs were what you think they were.
- **New rules bind to their trigger moment and name the failure they prevent** —
  sixty lines of distance loses a rule; a rule nowhere near its moment never fires.
- **Deterministic tests before every commit:** `python3 -m unittest discover -s
  college-apps/tests`. Skill prose changes also run
  `python3 college-apps/tests/word_report.py`.
- **Real student data never enters the repo.** `students/` is gitignored; fixtures
  are synthetic; dogfooding on a real student happens in a working folder outside
  the repo.
- **Work on a feature branch; the maintainer merges to `main`.**
