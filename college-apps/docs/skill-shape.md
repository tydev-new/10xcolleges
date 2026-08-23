# The shape of a skill

Every skill here is built to one shape. It was earned in
tydev-new/10xjobs-cowork (its `docs/skill-shape.md` keeps the receipts)
and adopted here with essay-coach, then student-intake. Measured here:
e4 3/3, i1 3/3, i2 3/3, e3 2/3 twice
(`docs/evals/eval-first-wave-2026-08-22.md`). This is the template for
the six skills still to convert, written so the next one is built in
ONE pass. Every extra pass is a hole this doc failed to close.

Words used below, glossed once. A **loop** repeats rounds against
something it can re-score. A **sequence** runs once to its exit. A
loop's **standard** is the written thing each round is measured against
(essay-coach: the rubric in `brief.md § Fixed`; student-intake: the
four-item gate). Its **budget** is how many rounds it may take, said up
front. Its **ceiling** is the sign it is stuck: two rounds with the same
count. A **moment rule** binds at one step of a round and is stated at
that step. **Tier 0** is the workspace `CLAUDE.md`, loaded before any
skill fires (`templates/workspace-CLAUDE.md`). The **registry** is the
table in `docs/data-model.md § Every file`. The **vault** is the lock on
the real workspace during a harness run.

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

**All five, no exceptions** — with one allowed form of sharing. A skill
whose mechanical checks live in a script it does not host needs no
`scripts/` of its own; its `eval.md § Who checks what` names the script
it uses. Here the scripts are shared at the plugin root (essay-coach
runs `scripts/check_draft.py`, student-intake runs
`scripts/check_record.py`); the shape allows it. A uniform set is what
makes drift loud: `kit/tests/test_invariants.py` FAILs a skill missing a
file or `eval.md § Who checks what`. An exception is drift that somebody
blessed — the source repo tried one and killed it. **A file's name
states its scope.** `eval.md` evaluates the whole skill. Narrower content
gets its scope in a SECTION name (`eval.md § The rubric`), never a file
wearing the generic name with a hidden narrower scope.

## SKILL.md — the sections, in this order

1. **The goal, and what must be true when it is met.** One sentence,
   then a table. Two allowed shapes; pick by what the skill measures:
   - **Scored measures** → `Measure | Target`. Targets only: "names
     things that exist only at this school" is a criterion and belongs
     in `eval.md`.
   - **Binary destinations** → `Must be true | Where` (essay-coach,
     student-intake). One row per thing; no scores to state.
   No procedure in the cells either way: "walk the draft modes" points
   at patterns.md, it does not inline the walk.
2. **Prerequisites**, split **Required** (do not proceed without) and
   **Optional** (better with, workable without — say what degrades).
3. **The loops and sequences**, with a short intro that says how you
   know which one you are in — what just happened decides, not asking.
   **A `###` section is a loop or sequence the skill runs. A procedure
   that is only technique gets a row in the table (rule 4).** A section
   is not a place for steps — see the skeleton below. A loop carries the
   exits below. A sequence (intake's Setup, Documents and Update;
   essay-coach's brief) has the same layout, no round budget, no
   ceiling. Each section states, in this order:
   - **Runs when** — the trigger, first line. It names cross-skill
     callers too: grep the other skills for routes into this one, and
     say what a routed entry changes. A caller usually arrives WITH
     something (`college-app` hands essay-coach the prompt and the
     target; the brief starts there).
   - **The skeleton — and nothing else.** *Runs when*. *Standard*
     (where it is written, what counts as an item). *Budget* (said up
     front). *Each round* — three to five lines: read the record,
     draft, check, score, deliver. *The measured rules that bind at a
     moment* — each one sentence, phrased as an **action** ("write the
     row now, while their words are on screen", never "that is a
     paraphrase, not a criterion" — a classification is satisfied by
     doing nothing, and one trial did exactly that). *Exits*. Soft cap
     ~300 words per loop; `kit/tests/test_invariants.py` FAILs a loop
     over 600. **Everything that is HOW to get there — the read order,
     the question order, where to look for an angle — is a hint and
     lives in `patterns.md § <loop> — getting there`**, with its
     receipts. A ten-step loop held the same cases at a third the
     length as a skeleton (source repo, measured).
   - **The placement test, both directions.** A line belongs in the
     loop only if it is *what must be true* or a *measured rule that
     binds at a moment*. The reverse is also earned: **a measured
     moment rule stays in the loop however short the loop is**. The
     source repo moved two to references; both failed in the next run
     and passed the round they came back. Here, "their read never moves
     yours" earned its place on the third sighting and held 3/3.
   - **A measured miss earns one of three things** — a moment rule in
     the loop (if it binds at a moment), a hint in patterns (if it is
     how), or a script (if a checker can see it). Never a step. A rule
     that keeps failing under rewording is a mechanism problem: i2 went
     0/3 → 0/3 → 1/3 → 0/3 → 3/3 by changing what the rule allowed and
     how the harness ran, never the sentence.
   - Any read the loop's RULES depend on is a **step that says "read
     X"** — a citation in parentheses is how a source-repo loop ran
     without its rules. A parenthetical is only a lookup pointer (a
     scale, a row format) into a file the skill's head already requires
     reading.
   - **Exit** — the three ways out for a bounded loop: clears the
     standard (say so plainly), budget spent (said up front), or the
     ceiling — two rounds with the same count → change the move (another
     angle, mode, or interview; homework) or hand the student a
     DECISION. Never relax the standard.
   - A loop with a history file **reads it before scoring** — the
     ceiling is a fact about earlier rounds, and a fresh session
     remembers none of them (essay-coach reads `brief.md § Rounds`).
4. **Anything whose procedure lives in `patterns.md`** goes in ONE
   table: what it is · runs when · threshold · exits with. (Neither
   converted skill needs one yet.)
5. **State** — what the skill owns and what it explicitly does NOT own;
   who else may append to which file; when the skill hands back; and
   **Session close**, which must say all three of:
   - which scripts run;
   - whether the checker-subagent runs, over which files, with which
     rule sources — "none runs, the words are the student's" is a
     statement; a pointer to eval.md is not;
   - **how the student sees the results**: outcomes, never narration.
     Clean = one line. Script FAILs = fixed, then named as fixed. WARNs
     = each named with why it is acceptable. Never announce a check is
     about to run; report what it found. A checker reply that is not the
     expected table is a VOID check — say it could not run, never
     deliver as if it passed.
6. **A moment-critical rule** may take its own section when it is too
   long to inline; every moment that triggers it still names it in its
   step (see rule 3 on actions).
7. **Guardrails** — only rules that must hold before the model judges
   anything relevant (the never-make-it-up guard, the source-tag
   guard). A rule that fires inside one loop lives in that loop.

## eval.md — three parts

1. **§ Who checks what** — the READ-split applied to this skill.
   Structure and counts → the script. Language against written rules →
   the checker-subagent (name the rule sources, or say none runs and
   why). Semantic judgment → the model at the moment, plus the student.
   Without it an unruled claim can enter a record unchecked (source
   repo); it is not optional.
2. **The criteria** — for each target in SKILL.md, what to look at when
   deciding whether it is met. Binary things are judged, not scored:
   forcing a score on "the brief exists" invents precision. A skill
   whose round-scoring standard lives in a student file (essay-coach's
   `brief.md § Fixed`) still has an eval.md — it says where the standard
   lives and how the round is judged against it.
3. **Boundaries** — bars that belong to a consumer (the counselor
   package's author-header refusal is `build_package.py`'s bar) are
   named as theirs and NOT restated. The skill's own bars are the
   targets in `SKILL.md`'s goal table; they are not duplicated here.
   Omit the part entirely when no consumer bar exists — an empty section
   is noise, not conformance.

## schema.md — and the parser's three rules

Holds every record shape: file templates, row formats, header markers,
history rows, lifecycle. `kit/shapecheck.py` (run by
`kit/tests/test_invariants.py`) **parses schema declarations out of this
file** (and out of `SKILL.md`), so the format is load-bearing:

- A file is declared by `## `name.md` — role` (heading form) or
  `**`name.md`**` (inline form). Section bullets — `` - `## Section` ``
  — must follow the declaring line **directly**: a prose line ends the
  block, and the sections after it are silently lost. Prose goes after
  the bullets.
- The `free-form body` marker must sit **on the declaring line**.
- After ANY schema edit, **count the schemas the parser returns and
  compare against what you expect** (`kit/shapecheck.load_schemas` —
  nothing here prints the count yet; call it). The count is what caught
  both parser breaks in the source repo; nothing else did.

Every history file also states its **lifecycle**: created when, written
by whom, **read by whom before scoring**, never pruned (essay-coach's
`brief.md § Rounds`).

**The data-model registry.** `docs/data-model.md § Every file` names one
owner per student file and links the section of the owner's `schema.md`
that holds its shape. Readers take the shape from that link, never from
a copy. `tests/test_data_model.py` FAILs a converted owner's row without
the link, a link that does not resolve, a schema with no section for
the file, and a second skill claiming the file under § State. An
unconverted owner keeps its shape in `SKILL.md` until it converts.

## patterns.md — technique, plus two fixed sections

How-to guidance the loops reach for. Two sections are required:

- **Antipatterns** — only for failure modes NOT already stated as rules
  elsewhere in this file. If the rule exists above, do not restate it as
  an antipattern (that duplication class was cut seven times in one day
  in the source repo). If that leaves nothing, skip the section.
- **Proposing a new pattern** — a pattern is never self-adopted. Propose
  it with the evidence from the history file; it lands in the student's
  workspace, and a human promotes it to the skill through the normal
  ritual. `kit/tests/test_invariants.py` checks the words are there.

## Shared references — the fourth kind

Some references are **cross-skill contracts**, not one skill's
technique. Here they live at the plugin root — `docs/voice.md`,
`docs/citations.md`, `docs/data-model.md` — read by every skill. A
hosted contract is labeled as such at the top; it never folds into a
host's `patterns.md`, and it moves only with all its consumers rewired
in the same commit.

**Tier 0.** Whatever must hold on every reply, whichever skill did the
work — the own-work sentence, college facts only from `research/`, a
draft is a file before it is shown — goes in the workspace `CLAUDE.md`,
not in one skill. Earned here: three rounds of 0/2 on e1 until the
lines moved there. The template is `templates/workspace-CLAUDE.md`, v1;
nothing yet refreshes a copy already in a user's folder.

## Converting a skill — the procedure

The source repo's first conversion took five passes; this list is what
they taught.

1. **Map before moving**: every section of every old file → its new
   home. Anything without a home is a finding, not leftovers.
2. Build the new files. Watch the three assembly traps that all
   happened: a leftover H1 inside a section, glue fragments (`— -`),
   the same offer or rule landing twice.
3. **Rewire every inbound pointer.** Grep the old filenames across
   `skills/`, `tests/` (including `expected.md` files AND `judge_e3.sh`:
   a judge script once fed a deleted file to the judge), `kit/`, and
   `docs/`. Skip dated records (`docs/evals/*.md`, everything under
   `tests/always-on/results/`, superseded design docs, banner-marked):
   they describe what WAS and are never rewired. Then sweep **section
   names too**: `§` pointers and "below" references break without any
   filename changing, and `docs/data-model.md` links to schema sections
   by exact name.
4. **Token-preservation check, mechanical**: every backticked token,
   ALL-CAPS word, and quoted phrase from the old files, grepped against
   the new — **whitespace-flexible**: a phrase wrapped across a line
   break is still present (a flat pattern once invented a loss). Judge
   each miss; "casing changed" is an answer, "probably fine" is not.
5. **Plain-language pass** (rule 13 of `kit/PRINCIPLES-core.md`) —
   relocated prose keeps its old density unless someone reads it. Scan
   for ·-chained run-ons, semicolon chains, and multi-clause
   parentheticals; unpack them into lists or sentences. The force of
   every rule survives the unpacking — this pass rewrites shape, never
   strength — and the token check re-runs after it.
6. Run `python3 -m unittest discover tests`, the kit invariants
   (`kit/tests/test_invariants.py`, as `kit/README.md` shows), and the
   skill's script against a planted workspace; **compare the schema
   count against what you expect** (§ schema.md above). Growth into the
   loaded tier is the shape's known cost — reported, never discovered.
7. Add or update the registry row in `docs/data-model.md § Every file`
   for every file the skill owns — owner, schema link — and confirm
   `tests/test_data_model.py` is green.
8. If the conversion touched `templates/workspace-CLAUDE.md`, say so in
   the commit; copies already in users' folders do not refresh.
9. **Measure before calling it done**: the skill's harness cases,
   TRIALS=2, against the recorded baseline. A restructure that scores
   worse reverts. The source repo's first conversion needed three
   rounds to return to its own baseline — parity is the expected
   outcome, not improvement.
10. Independent review. The builder does not review their own
    conversion.

## Measuring conduct — the harness

Tests check structure. **Conduct** — did the agent do the right thing
under a baited prompt — is measured by `tests/always-on/` (`run_e3.sh`,
`judge_e3.sh`, from `kit/harness/run_multiturn_template.sh`). A case is
a planted student folder, a persona, and `expected.md`: MUST / MUST NOT
lines, each checkable from the transcript or the files.

- **The persona driver.** A second model plays the student from
  `persona.md`: who they are, the TRUE FACTS they may use and nothing
  else, and a BEHAVIOR SCRIPT of beats by message number. Each reply is
  fed back with `--continue` for `turns.txt` turns.
- **Per-turn snapshots.** `students/` is copied after every turn, so the
  judge sees a row land in the turn it was said, not only at the end.
- **The judge reads the tool log.** Every call the agent made is in
  `.tools.txt`; "no search outside the session folder" is checked
  against calls, and a claim with no call is only a claim.
- **A `serial` marker** in a case directory runs it alone — for cases
  that touch the real home (Setup): parallel trials once saw each
  other's folders.
- **The vault.** The real workspace is locked for the run; runs use
  fresh temp folders. Never plant test data in a real student folder.

`TRIALS=2` minimum before a rule is called held; a one-trial miss is a
sighting. Results are receipts in `docs/evals/`, never assertions.

## What this shape costs — decided with eyes open

- **A loop whose deliverable persists scores as a count and keeps a
  round record.** The standard is written to a file before the draft
  (`brief.md § Fixed` for an essay; the gate `check_record.py` counts,
  for intake), one item per bullet — M is the bullet count. Each round
  appends a row (essay-coach: `round · date · N/M · the one big thing ·
  student's choice` in `brief.md § Rounds`; header and cells checked),
  and the score is `N/M` over the standard's items — never a sentence,
  never 0–100. The loop reads the earlier rows before it scores; the
  ceiling is then mechanical: two rows with the same count. A reviewer
  panel, where one exists, returns `lens · finding` rows. The author
  adds the outcome (`fixed` / `discarded — why`). The bar is no
  undischarged finding. A lens that returns prose twice is a VOID row.
  The cold reader is a reader, not a panel: three lines, or `VOID` and
  why. A skill's own ordinal rubric may ride beside the count; tiers and
  named trade-offs replace numeric fit (PRINCIPLES, promise 4).
- **A skill's loops are specified in its own `SKILL.md` — never in a
  shared reference.** A conversion that finds the skill's loop described
  in a shared reference INLINES it; that is not optional (`docs/design.md
  § The iteration loops` describes; each `SKILL.md` is the authority on
  its own). The standard-does-not-bend law is stated
  **word for word at each loop's exit, unmarked** — short, identical
  copies guarded by the invariants test, no echo bookkeeping. The
  one-copy pattern governs facts that drift; a one-sentence law at its
  firing moments is the allowed-duplication class.
- **When a loop detaches from a shared reference**, two things travel
  with it or the detach is incomplete. First, the shared LAW ("a draft
  never justifies changing the rubric; a criterion relaxed to fit what
  was written has stopped being a standard") lands **unmarked at the
  loop's exit** — the source repo measured that a pointer alone does not
  carry it. Second, the leftover text is **trimmed in the same commit**
  (and removed when its last consumer leaves): a tier row, a budget, or
  a known-gap line left behind becomes a second authoritative copy the
  moment the skill states its own.
- **It grows a skill.** Loops living in `SKILL.md` put their full text
  in the loaded tier (+47% on the source repo's first conversion).
  Report the growth; the 600-word cap bounds it.
- **It is parity, not improvement.** The shape buys structure — a place
  for everything, so drift is findable — not measured behaviour gains.
  The gains here came from mechanisms: a script, a Tier-0 line, a file
  before a reply.
- **The loop shape is stated per skill** (essay-coach's essay loop,
  student-intake's interview) — the allowed duplication, guarded by
  `kit/tests/test_invariants.py`, which also holds the rest of the
  shape: the five files, Runs when and Exits, Standard · Budget ·
  ceiling, the 600-word cap, one schema owner, resolving links, the
  Session close facts, `§ Who checks what`, "never self-adopted", and
  no loop sentence restated in a reference.
