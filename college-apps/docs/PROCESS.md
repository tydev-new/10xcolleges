# The working process — how a skill gets built here

The ritual that produced student-intake and essay-coach, ported from
tydev-new/10xjobs-cowork where it was earned (that repo's `docs/PROCESS.md`
keeps the original receipts). Each step exists because skipping it
failed, measurably. The receipt is named so the step can be argued again
if the evidence changes.

**Precedence chain for every judgment:** `PRINCIPLES.md` →
`docs/design.md` → `docs/skill-shape.md`.
A conflict means one of them is wrong. Fix the chain; never pick a
winner case by case.

## The ritual, in order

1. **Design gate before building.** Discuss in session the destination,
   the assumptions and what would disprove them, the tradeoffs, and the
   test plan. Record the conclusions in the skill's GitHub issue before
   any code or prose changes. *(Receipt: issue #2,
   student-intake.)*
2. **Track via GitHub issues.** One issue per skill, with checkboxes.
   Close it with receipts, never silently. Record explicit rejections
   too, so bad ideas are not re-imported later.
3. **Cross-check prior art** — the 10xjobs skills (the same shape, a
   year ahead) and the published essay-coaching frameworks
   (`essay-coach/references/patterns.md § The frameworks`). Port
   knowledge, not choreography. Record what was deliberately NOT taken
   and why. *(Receipt: intake ported source tags and the `TODO:`
   discipline, not the propose-then-confirm write — design.md says rows
   land in the moment.)*
4. **Build with the enforcement split** (`design.md § Enforcement`). A
   check with one right answer goes in code (the owner's
   `references/schema.md`, a checker script, the registry test). A
   judgment goes in skill prose, bound to the step where it applies.
5. **Independent drift review before closing.** A subagent that did NOT
   build it reviews against the full chain plus consumer seams, with
   file:line evidence per finding. The author never grades their own
   build. *(Receipt: intake's review found 19 — the
   self-reported gate count, a Retired-row shape its own checker
   rejected, `meta.json` claimed against the data model — all invisible
   to the author.)*
   **And the reviewer verifies the fixes.** The agent that found a
   finding confirms it is resolved — never only the fixer's own greps.
   *(Receipt: the re-verify caught a labelled `TODO: <value>` the fix
   had claimed to catch and didn't.)*
6. **Dogfood on a real student — live-first.** The live run is the
   acceptance test AND the design input for what the harness should
   bait. Student data is real personal data: dogfood deliberately, never
   plant test data in a real folder, and run the harness in temp
   workspaces with the real one locked. *(Pending for the first wave.)*
7. **Conduct harness after the live run.** Planted workspaces, a
   simulated student for multi-turn cases, Sonnet runner + Opus judge.
   The judge sees the written files, the skill text, the tool log, and
   the expectations — never the agent's summary of any of them.
   Multi-trial gates (`TRIALS=2` minimum, 3 to separate noise from a
   miss). On a repeat miss: one change at the step it applies, re-run,
   record before and after. Records land in
   `docs/evals/`. Environment contract: `tests/always-on/README.md`.
   *(Receipt: `eval-first-wave-2026-08-22.md` — five rounds to make
   Setup hold, each round a different real cause.)*
8. **Closing drift review, then declare done.** Same chain, whole
   implementation, including what the acceptance run actually produced
   (described vs produced behavior).
9. **Memory + transcripts.** Durable lessons go in the repo (docs, commit
   messages, this file) — never only in an agent's session memory.
   Session transcripts archive OUTSIDE the repo (they carry students'
   personal data).

## The non-negotiables (earned the hard way)

- **Patch, grep, and commit share one command block, or the message
  lies.** A number in a commit message comes from the command that
  measured it. *(Receipt: a commit here claimed "598 words" while the
  edit had not applied; the loop was 601.)*
- **Verify disk, not narration.** Before believing any "I wrote/fixed
  X", grep the file. *(Receipt: `run_e1.sh` planted no skill for three
  measurements; the tool log showed the agent searching an empty
  `.claude/skills/`.)*
- **Bind rules to the step where they apply, and measure.** Described
  behavior ≠ produced behavior. *(Receipts: the late read 0/4 → 3/3 once
  the rule named the turn it arrives in; the disk-search ban 0/3 → 3/3
  once it named the plugin too.)*
- **A conduct pass counts only if the environment could express the
  failure.** A judge's verdict counts only if the judge's inputs were
  what you think they were. *(Receipt: the judge grading a transcript
  copy with no workspace beside it reported "no files written".)*
- **Author contamination:** whoever built it doesn't test or review it
  alone.
- **Files are records; chat is the interface.** Anything that needs the
  student's judgment is shown and answered in conversation — never sent
  off as file-editing homework.
- **No half measures:** delete cleanly, and decide each deletion on its
  merits (earned rules keep receipts; deadweight goes).
