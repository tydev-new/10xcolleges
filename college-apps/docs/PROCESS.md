# The working process — how a skill gets built here

The ritual that produced profile, search, evaluate, storybank, and
positioning. Each step exists because skipping it failed, measurably;
the receipt is named so the step can be re-litigated if the evidence
changes (P2.11 — every rule derivable or earned).

**Precedence chain for every judgment:** `PRINCIPLES.md` →
`docs/design.md` → `docs/skill-shape.md`.
A conflict means one of them is wrong — fix the chain, never pick a
winner ad hoc.

## The ritual, in order

1. **Design gate before building.** Destination, assumptions with
   falsifiers, tradeoffs, test plan — discussed in session, conclusions
   recorded in the phase's GitHub issue before code or prose changes.
   *(Receipt: standing instruction 2026-08-13; every phase since.)*
2. **Track via GitHub issues.** One issue per phase with checkboxes;
   closed with receipts, never silently. Explicit rejections are recorded
   too, so bad ideas don't get re-imported later (#20's rejected list).
3. **Cross-check prior art** — career-ops (vendored, MIT) and the Noam
   docs — for proven frameworks to port and cautionary tales to name.
   Port knowledge, not choreography; record what was deliberately NOT
   taken and why. *(Receipt: search's SimHash/liveness ports; evaluate's
   rejected scoring formula.)*
4. **Build with the enforcement split** (goals doc, goal 2): one right
   answer → code (schemas in the owning SKILL § State, checkers,
   loud-fail duplicates); judgment → skill prose bound to its moment.
5. **Independent drift review before closing.** A subagent that did NOT
   build it reviews against the full chain plus consumer seams, findings
   with file:line evidence. The author never grades their own build.
   *(Receipt: caught the draft-guardrail-where-it-can't-fire DRIFT and
   the document-confirmation DRIFT — both invisible to the author.)*
   **And the reviewer verifies the fixes** — findings are confirmed
   resolved by the agent that found them, never only by the fixer's own
   greps. *(Receipt 2026-08-15: the apply fix-pass shipped a corrupted
   file and two dangling sentences; the fixer's verification missed all
   three, the reviewer's caught all three.)*
6. **Dogfood on the founder's real data — live-first.** The live run is
   the acceptance test AND the design input for what the harness should
   bait. *(Receipt: the S002 "most left"→"about half" catch; the pitch
   anti-pattern catch; every t6/t7 case came from a live lesson.)*
7. **Conduct harness (tN) after the live run.** Planted workspaces, ~3
   cases per failure mode, Sonnet runner + Opus judge; the judge sees
   the written files, the skill text, and a deterministic check output;
   multi-trial gates (majority; single runs are noise). Fix-and-remeasure
   on any failure — one moment-bound change, re-run, record before/after.
   Eval record lands in `docs/eval-*.md`. Environment contract:
   `tests/always-on/README.md` — including "judge inputs are inputs."
8. **Closing drift review, then declare done.** Same chain, whole
   implementation including what the acceptance actually produced
   (described vs produced behavior).
9. **Memory + transcripts.** Durable lessons → the repo (docs, commit
   messages, this file) — never only in an agent's session memory.
   Session transcripts archive OUTSIDE the repo (they carry the
   founder's personal data).

## The non-negotiables (earned the hard way)

- **Patch, grep, and commit share one command block, or the message
  lies.** *(Three commits once claimed unapplied patches.)*
- **Verify disk, not narration** — before believing any "I wrote/fixed
  X", grep the file. *(t1's narration slip; the t7 base-resume check.)*
- **Bind rules to their trigger moment and measure.** Described behavior
  ≠ produced behavior — measured six times (hazard list 1/7→7/7,
  transition list, plan gate 0/2→2/2, track naming 1/3→2/2, both-writes
  0/2→2/2, the Raskin check). **Co-located obligations must be
  co-named** — sixty lines of distance loses a rule.
- **A conduct pass counts only if the environment could express the
  failure** — and a judge's verdict counts only if the judge's inputs
  were what you think they were.
- **Author contamination:** whoever built it doesn't test or review it
  alone.
- **Files are records; chat is the interface.** Anything needing the
  candidate's judgment is shown and answered in conversation — never
  routed through file-editing homework.
- **No half measures:** delete cleanly, with the deletion adjudicated
  (earned rules keep receipts; deadweight goes).
