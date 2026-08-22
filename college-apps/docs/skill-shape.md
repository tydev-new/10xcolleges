# The shape of a skill

Settled on storybank and profile, 2026-08-20. Measured once: `t7` 6/6
after three fix rounds (`docs/eval-t7-storybank.md`). This is the
template for the remaining nine skills — written so the next one is
built in ONE pass. Profile took five; every extra pass is a hole this
doc failed to close.

---

## The five files

Each file answers one kind of question. When you can't decide where
something goes, ask which question it answers.

| File | The question it answers | When it loads |
|---|---|---|
| `SKILL.md` | what to reach, and when each thing runs | whenever the skill fires |
| `references/eval.md` | how to tell whether you got there, and who checks | at a loop's exit and at session close |
| `references/schema.md` | what shape the records take | before writing a record |
| `references/patterns.md` | how to do a specific task well | before the task |
| `scripts/*.py` | the checks with one right answer | executed, never read into context |

**All five, no exceptions** — with one sanctioned form of sharing: a
skill whose mechanical checks live in another skill's script (positioning
runs profile's `check_files.py`) needs no `scripts/` of its own, and its
`eval.md § Who checks what` names the script it uses. A uniform set is
what makes drift loud:
`tests/test_skill_shape.py` FAILs a converted skill missing a file or
`eval.md § Who checks what`. (Profile once skipped `eval.md` under a
sanctioned exception; the founder killed it — an exception is drift that
somebody blessed.) **A file's name states its scope**: `eval.md`
evaluates the whole skill, and content scoped narrower gets its scope in
a SECTION name (`eval.md § The résumé audit`), never a stealth-scoped
file wearing the generic name.

## SKILL.md — the sections, in this order

1. **The goal, and what must be true when it is met.** One sentence,
   then a table — two sanctioned shapes, pick by what the skill measures:
   - **Scored measures** → `Measure | Target` (storybank: Strong = "4 or
     better"). Targets only — "carries STAR, stakes and an earned
     secret" is a criterion and belongs in `eval.md`.
   - **Binary destinations** → `Must be true at the end | Where it
     lives` (profile). One row per thing; no scores to state.
   No procedure in the cells either way: "walk the hazard table" points
   at patterns.md, it doesn't inline the walk.
2. **Prerequisites**, split **Required** (do not proceed without) and
   **Optional** (better with, workable without — say what degrades).
3. **The loops and sequences**, with a short intro that says how you
   know which one you are in — what just happened decides, not asking.
   **A `###` section is a loop or sequence the skill runs; a procedure that is only technique gets a row in the table (rule 4).** A section is not a place for steps — see the skeleton below. A section that repeats rounds against a
   re-scorable measure is a **loop** and additionally carries the exits
   below; a section that runs once to its exit (profile's Setup, its
   Direction change) is a **sequence** — same layout, no round budget, no
   ceiling. Each section states, in this order:
   - **Runs when** — the trigger, first line. It names cross-skill
     callers too: grep the other skills for routes into this one, and say
     what a routed entry changes — a caller usually arrives WITH a
     diagnosis (positioning: a routed entry starts with the diagnostic
     against the existing pitch, not a fresh build).   - **The skeleton — and nothing else (founder, 2026-08-21):**
     *Runs when* · *Standard* (where it is written, what counts as an
     item) · *Budget* (said up front) · *Each round* — three to five
     lines: read the record, draft, check, score, deliver · *the
     measured rules that bind at a moment* — each one sentence, phrased
     as an **action** ("propose it now, in this reply", never "that is
     a proposal, not a write" — a classification is satisfied by doing
     nothing, and one trial did exactly that) · *Exits*. Soft cap ~300
     words per loop. **Everything that is HOW to get there — the read
     order, the audit block's contents, classify-then-select, where to
     place a word, the panel's lenses — is a hint and lives in
     `patterns.md § <loop> — getting there`**, with its receipts. Apply
     grew to ten numbered steps by earning "a sentence at the moment"
     per measured miss; measured 2026-08-21, the loop skeleton held the
     same cases (8/8) at a third the length.
   - **The placement test, both directions.** A line belongs in the
     loop only if it is *what must be true* or a *measured rule that
     binds at a moment*. The converse is also earned: **a measured
     moment rule stays in the loop however short the loop is** — the
     reshape moved two to references ("a fact needs a yes on the exact
     line"; "the panel is spawned subagents") and both failed in the
     next run, then passed the round they came back.
   - **A measured miss earns one of three things** — a moment rule in
     the loop (if it binds at a moment), a hint in patterns (if it is
     how), or a script (if a checker can see it) — never a step.
   - Any read the loop's RULES depend on is a **step that says
     "read X"** — a parenthetical citation is how storybank's improve
     loop ran without its rules. A parenthetical is allowed only as a
     lookup pointer (a scale, a row format) into a file the skill's head
     already requires reading.
   - **Exit** — the three ways out for a bounded loop: clears the
     standard (say so plainly), budget spent (said up front), or the
     ceiling — two rows with the same count and tiers → change strata or hand the
     candidate a DECISION; never relax the standard.
   - A loop with a history file **reads it before scoring** — the
     ceiling is a fact about earlier rounds, and a fresh session
     remembers none of them.
4. **Anything whose procedure lives in `patterns.md`** goes in ONE
   table: what it is · runs when · threshold · exits with. (Storybank's
   find gaps, drill and narrative identity are the reference; profile
   has no table because every one of its modes keeps steps inline.)
5. **State** — what the skill owns and what it explicitly does NOT own;
   who else may write which columns; when the skill hands back; and
   **Session close**, which must say all three of:
   - which scripts run;
   - whether the checker-subagent runs, over which files, with which
     rule sources;
   - **how the candidate sees the results**: outcomes, never narration.
     Clean = one line. Script FAILs = fixed, then named as fixed.
     Language flags = the verdict table shown, fix or defence beside
     each row. Never announce a check is about to run; report what it
     found. A checker reply that is not the JSON table is a VOID check —
     say it could not run, never deliver as if it passed.
6. **A moment-critical rule** may take its own section when it is too
   long to inline — and every moment that triggers it still names it in
   its step (see rule 3 on actions).
7. **Guardrails** — only rules that must hold before the model judges
   anything relevant (fabrication guards, the door guard). A rule that
   fires inside one loop lives in that loop.

## eval.md — three parts

1. **§ Who checks what** — the READ-split applied to this skill:
   structure and counts → the script · language against written rules →
   the checker-subagent (name the rule sources) · semantic judgment →
   the model at the moment, plus the candidate. Storybank shipped
   without this section and a struck claim could enter a story file
   unchecked; it is not optional.
2. **The criteria** — for each target in SKILL.md, what to look at when
   deciding whether it is met. Binary things are judged, not scored:
   forcing a score on "the map exists" invents precision. A skill whose
   round-scoring standard lives in a candidate file (profile's § FIXED)
   still has an eval.md — it says where the standard lives and how the
   round is judged against it.
3. **Boundaries** — bars that belong to a consumer (prep's 8–12,
   practice's 8+) are named as theirs and NOT restated. The skill's own
   bars are the targets in `SKILL.md`'s goal table; they are not
   duplicated here. Omit the part entirely when no consumer bar exists —
   an empty section is noise, not conformance.

## schema.md — and the parser's three rules

Holds every record shape: index rows, file templates, status grammars,
history rows, lifecycle. `check_files.py` **parses schema declarations
out of this file** (and out of `SKILL.md`), so the format is load-bearing:

- A file is declared by `## `name.md` — role` (heading form) or
  `**`name.md`**` (inline form). Section bullets — `` - `## Section` `` —
  must follow the declaring line **directly**: a prose line ends the
  block, and the sections after it are silently lost. Prose goes after
  the bullets.
- The `free-form body` marker must sit **on the declaring line**.
- After ANY schema edit, run the checker and **compare the printed
  schema count against what you expect**. The count is what caught both
  parser breaks; nothing else did.

Every history file also states its **lifecycle**: created when, written
by whom, **read by whom before scoring**, never pruned.

## patterns.md — technique, plus two fixed sections

How-to guidance the loops reach for. Two sections are required:

- **Antipatterns** — only for failure modes NOT already stated as rules
  elsewhere in this file. If the rule exists above, do not restate it as
  an antipattern (that duplication class was cut seven times in one day).
  If that leaves nothing, skip the section.
- **Proposing a new pattern** — a pattern is never self-adopted. Propose
  it with the evidence from the history file; it lands in the
  candidate's workspace, and a human promotes it to the skill through
  the normal ritual.

## Shared references — the fourth kind

Some references are **cross-skill contracts**, not this skill's
technique: profile hosts `candidate-voice.md` and `language-check.md`,
but their readers are apply, outreach,
positioning and storybank (which spawns the language checker at its own
session close). A hosted contract is labeled as such at the top; it never
folds into the host's `patterns.md`, and it moves only with all its
consumers rewired in the same commit.

## Converting a skill — the procedure

Profile took five passes; this list is what they taught.

1. **Map before moving**: every section of every old file → its new
   home. Anything without a home is a finding, not leftovers.
2. Build the new files. Watch the three assembly traps that all
   happened: a leftover H1 inside a section, glue fragments (`— -`),
   the same offer or rule landing twice.
3. **Rewire every inbound pointer** — grep the old filenames across
   `skills/`, `tests/` (including `expected.md` files AND judge scripts:
   `judge_t19.sh` fed a deleted file to the judge), and `docs/` — except
   dated records (`eval-*.md`, `*-trace.md`), which describe what WAS and
   are never rewired. Then sweep **section names too**: `§` pointers and
   "below" references break without any filename changing, and
   `workspace-CLAUDE.md` points at one section by its exact title.
4. **Token-preservation check, mechanical**: every backticked token,
   ALL-CAPS word, and quoted phrase from the old files, grepped against
   the new — **whitespace-flexible**, because a phrase wrapped across a
   line break is still present (overclaim #14 was a flat pattern
   inventing a loss). Judge each miss; "casing changed" is an answer,
   "probably fine" is not.
5. **Plain-language pass** (rule 13) — relocated prose keeps its old
   density unless someone reads it. Scan for ·-chained run-ons,
   semicolon chains, and multi-clause parentheticals; unpack them into
   lists or sentences. The force of every rule survives the unpacking —
   this pass rewrites shape, never strength — and the token check
   re-runs after it.
6. Run `tests/run.py` AND `check_files.py` against the live workspace;
   **compare the printed schema count against what you expect**. Run
   `python3 tests/word_report.py` and report the tier-2 delta — growth
   into the loaded tier is the shape's known cost, and it is reported,
   never discovered.
7. If the conversion touched `templates/workspace-CLAUDE.md`, **bump its
   version marker** — the refresh-by-offer mechanism keys on it.
8. Regenerate `docs/loading-map.md`'s counts — a conversion moves words
   between tiers by design.
9. Deploy (`cp -r skills/* ~/.claude/skills/`) and **remove dissolved
   files by hand** — cp never deletes.
10. **Measure before calling it done**: the skill's harness cases,
   TRIALS=2, against the recorded baseline. A restructure that scores
   worse reverts. Storybank needed three rounds to return to its own
   baseline — parity is the expected outcome, not improvement.
11. Independent review. The builder does not review their own
    conversion.

## What this shape costs — decided with eyes open

- **A loop whose deliverable persists scores as a count and keeps a
  round record** (founder, 2026-08-21, the loop-alignment design —
  applied to profile's base résumé, positioning's pitch, and apply's
  tailoring; **not yet aligned, by decision**: apply's answers loop and
  outreach's draft loop — short-lived drafts whose rubric line is their
  record; a round table per question or message would be ceremony —
  revisit if a measured miss traces to it. **Learn, by decision**: an ordinal status per topic with its own per-topic log — the honest-result cell carries the coverage count; its ceiling is two reps at the same count. **Coach — aligned**: the mirror's weekly `plan-log.md` entry carries `planned N · happened K`; the ceiling is two entries with the same K). The standard is written to a file before the draft (a brief for a
  deliverable that outlives jobs; a `## Standard` block inside the
  deliverable's own file otherwise), as bullets, one item per bullet —
  M is the bullet count.
  Each round appends a row with the columns `date · round · driver ·
  scored · what changed` (the column is named `scored vs FIXED` in the
  brief-backed history files; header and cells checker-enforced), and
  `scored` is
  `N/M held; unmet: <items>` over the standard's items plus any tier
  words — never a sentence. The loop reads the earlier rows before it
  scores. The ceiling is then mechanical: two rows with the same count
  and tiers. A reviewer panel, where one exists, returns `lens · finding` rows;
  the author adds the outcome (`fixed` / `discarded — why`); the bar is
  no undischarged finding; a lens that returns prose twice is a VOID
  row. Scores stay counts and
  tiers, not 0–100 judgments, a skill's own ordinal rubric rides beside the count where it exists
  (positioning's 1–5 diagnostic) or replaces it where the deliverable
  is per-story (storybank's 1–5 strength, its own history columns);
  evaluate's fit score is a different object.
- **A skill's loops are specified in its own `SKILL.md` — never in a
  shared reference** (founder's ruling, #36). A conversion that finds
  the skill's loop described in a shared reference INLINES it; that is
  not optional. Done (2026-08-21): apply and outreach were the last
  consumers of `improvement-loop.md`; it is REMOVED, and its tier-2
  contract (enter / execute / exit / self-loop / the ceiling / record
  where the work lives) is stated inline as each loop's own text. The
  standard-does-not-bend law is stated **verbatim at each
  loop's exit, unmarked** — the door-guard pattern: short, identical
  copies guarded by the shape test, no echo bookkeeping. The one-copy
  pattern governs facts that drift; a one-sentence law at its firing
  moments is the sanctioned-duplication class.

- **When a loop detaches from a shared reference**, two things travel
  with it or the detach is incomplete: the shared LAW ("cutting a
  claim's supporting evidence to fit a limit IS relaxing it: a
  claim-name without its number is not the claim") lands **unmarked at
  the loop's exit**, guarded by `tests/test_skill_shape.py` — t13
  measured that a pointer alone does not carry it — and the residual
  file is **trimmed in the same commit** (and removed when its last
  consumer leaves): a tier row, a budget, or a known-gap line left
  behind becomes a second authoritative copy the moment the skill
  states its own.

- **Dated records are never rewired** — and the list is wider than
  `eval-*.md` and `*-trace.md`: superseded/shipped design docs
  (banner-marked) and everything under `tests/always-on/results/` also
  describe what WAS.

- **Session close states its checker-subagent fact inline** — "none is
  wired" is a statement, a pointer to eval.md is not.

- **It grows a skill.** Storybank 3,256 → 4,801 words (measured at
  6e40f3c; +47%); profile roughly flat only because trims offset the
  growth. Loops living in `SKILL.md`
  puts their full text in the loaded tier — profile's is ~2,500 words
  against a ~700 soft target.
- **It is parity, not improvement.** The old storybank also scored 6/6.
  The shape buys structure — a place for everything, so drift is
  findable — not measured behaviour gains.
- **The loop shape is stated per skill** (storybank's improve, profile's
  Loop A, positioning's pitch loop, apply's tailoring and answers,
  outreach's draft) — the sanctioned duplication, guarded by the shape
  test's law check; #35's invariants test is the broader guard still
  to design.
