# Design

How this system is put together and why. The *data* rules — what each file is and what
may change it — are in `data-model.md`, the binding contract.

This document does **not** restate what individual skills do. The skills are the
specification; they are what the model reads at runtime. Anything copied here would drift
the first time a skill changed. What lives here is what no single skill can say:
structure, rules that cut across skills, and the reasoning behind decisions that look
arbitrary later.

---

## Principles

The promises are in `PRINCIPLES.md` — nine to the student and family, plus the core every
skill is built to. They top the precedence chain (`PRINCIPLES.md` → `design.md` →
`skill-shape.md`). Nothing here restates them. Two stances follow from them and are easy
to lose:

- **Facts that drift live in config; rules that compute live in code.** FAFSA's opening
  date is a fact and belongs in `config/calendar.json`. "A January deadline belongs to
  the aid year that opened the previous October" is a rule and belongs in Python, under
  test. A rule in prose is re-derived on every run, and re-derived date arithmetic is
  how a nine-month error hides in plain sight.
- **Degrade, don't fail.** Rate limit hit → work from Common Data Sets. No API key → the
  shared demo key. No Chrome → print to PDF by hand. The only hard stops are where
  continuing would produce something misleading: a mistyped deadline, an unlabeled essay
  draft, a student draft with no review.

---

## Components

```
                        ┌───────────────────────────────┐
                        │   Student · parent · school   │
                        │          counselor            │
                        └───────────────┬───────────────┘
                                        │  plain conversation
                        ┌───────────────▼───────────────┐
                        │         college-app           │   orchestrator:
                        │   locate → diagnose → route   │   finds the student,
                        └───────────────┬───────────────┘   sees what's missing
                                        │
      ┌────────────┬────────────┬───────┴────┬────────────┬──────────────┐
      ▼            ▼            ▼            ▼            ▼              ▼
 student-     college-     college-      essay-        rec-      app-tracker
  intake        list       research       coach       request   counselor-package
      │            │            │            │            │              │
      └────────────┴────────────┴─────┬──────┴────────────┴──────────────┘
                                      │ read / write
   ┌──────────────────────────────────▼──────────────────────────────────┐
   │  students/<slug>/          ← in the USER's working directory        │
   │  documents/ · profile · criteria · conversations · colleges ·        │
   │  feedback · research/ · essays/ · recs/ · meta.json                  │
   └──────────────────────────────────┬──────────────────────────────────┘
                                      │ consumed by
   ┌──────────────────────────────────▼──────────────────────────────────┐
   │  scripts/            deterministic, no judgment                     │
   │  check_record · check_draft  (the laws, run every round)            │
   │  scorecard · make_tracker · fill_packet · build_package             │
   └──────────────────────────────────┬──────────────────────────────────┘
                                      ▼
                     students/<slug>/out/  →  xlsx · docx · html · pdf


    Read-only, shipped with the plugin          External sources
    ┌────────────────────────────────┐          ┌──────────────────────────┐
    │ schemas/ profile · criteria ·  │          │ College Scorecard API    │
    │          conversations · essay │          │ Common Data Sets (§C7)   │
    │ docs/    voice · citations ·   │          │ College admissions pages │
    │          data-model · design   │          │ (deadlines — sole source)│
    │ config/  calendar.json         │          │                          │
    │ templates/ student · worksheet │          │                          │
    └────────────────────────────────┘          └──────────────────────────┘
```

**The split that matters:** skills exercise judgment, scripts do not. Any decision about
a student lives in a skill. Anything deterministic — date arithmetic, spreadsheet layout,
HTML generation, API pagination — lives in a script and is testable. Where they meet, the
model extracts (it is good at that) and the script formats (it is reliable at that).
`packet.json` → `fill_packet.py` is the clearest example.

---

## The arc

Stages 1–3 are mostly in order; 4–7 run in parallel and repeat. Skipping ahead produces
worse work: an essay written before the research is generic, and a list built before the
interview is a rankings printout.

```
 1  INTAKE                                        student-intake
    school packet ─┐
    transcript ────┼──▶  profile.md      (who they are)
    worksheet  ────┤
    interview  ────┴──▶  criteria.md     (what they want)
         │
         │  gate: budget + numbers + rough direction + criteria rows
         ▼
 2  LIST                                          college-list
    criteria.md ──hard filters──▶ cut
                └─preferences──▶ score
                                  └──▶ colleges.md  +  meta.json
         │
         ▼
 3  RESEARCH                                      college-research
    Scorecard ──┐
    CDS §C7 ────┼──▶ research/<college>.md   (cited, with fit + friction)
    .edu site ──┘         │
         │                └──▶ may re-tier a school, or cut it ──┐
         ▼                                                       │
 ┌───────────────────── these repeat ────────────────────────┐   │
 │                                                            │   │
 │  4 ESSAYS      essay-coach       essays/…                  │   │
 │  5 RECS        rec-request       recs/…                    │   │
 │  6 TRACKER     app-tracker       out/tracker.xlsx          │   │
 │  7 PACKAGE     counselor-package out/package.html + .docx  │   │
 │                        │                                   │   │
 └────────────────────────┼───────────────────────────────────┘   │
                          │                                       │
                          ▼                                       │
              counselor feedback → feedback.md ───────────────────┘
                                    (re-tier, add schools, redo tracker)
```

Feedback loops are the point, not an exception. A counselor's read in September changes
the list; the same read in December changes nothing. So the package is built to be sent
early and often.

---

## First release — intake and the essay loop

Two skills give students value before anything else exists: `student-intake` (who they
are and what they want, each line tagged with its source) and `essay-coach` (one essay
at a time, to a standard the college set). Everything else in the arc — the list,
research, the tracker, recs, the package, the aid plan — builds on those two files and
those two habits. Both are built to the shape in `skill-shape.md`, independently
reviewed, and measured with a simulated student (`tests/always-on/`, receipts in
`docs/evals/eval-first-wave-2026-08-22.md`). Intake also owns Setup — where the files
live — because it is the front door; `college-app` routes to it. The rest follow in the
order their laws suggest, each through the same process before it is called ready.

## The iteration loops

A loop repeats rounds against an explicit written standard. Three loops do this; everything else in
the arc runs once to an exit or a gate. The loops share one shape: **an explicit written standard,
owned by the student or set by the college, re-read in full before every pass; a record
of each round that is append-only or never edited; a score that is a count; and a
ceiling — the sign the loop is stuck — that hands the decision to the student instead of
bending the standard.**

### The essay loop

One loop per essay. A student works several essays for several schools at once. Each has
its own folder, brief, and draft/review sequence, and the loop tracks exactly one.
Nothing crosses folders except the student's record (`profile.md`, `conversations.md`)
and the college's research file.

**Prerequisites, before the loop opens:** the prompt, word for word, and the target — a
named college, or the Common App personal statement
(`essays/common-app--<prompt-slug>/`). No prompt, no brief. No target, no rubric: the
rubric comes from what *that* reader wants, and "a college essay in general" has no reader.

```
   prompt + target ──▶ brief.md ┬─ FIXED   prompt, restated · rubric (each criterion with
                                │          its SOURCE tier) · word count + retrieval date
                                └─ LIVING  angles · chosen · outline · draft mode
                                     │
                                     ▼
                      student chooses the mode:  A write · B sample · C first pass
                                     │
           ┌────────────▶  draft-NN.md  ── author on line one (code-enforced)
           │                    │        ── check_draft.py passed BEFORE it is shown
           │                    ▼
           │            student's read: their own N/M + the one thing they'd change
           │                    │
           │                    ▼
           │            re-read brief.md IN FULL — both halves
           │                    │
           │                    ▼
           │            review-NN.md  ── their read beside yours: N/M against FIXED
           │                          ── and a row in brief.md § Rounds: round · date · N/M · big thing · their choice
           │                          ── the cold reader's three lines (an independent pass)
           │                          ── external feedback, when feedback.md has any (outranks ours)
           │                          ── what works · ONE big thing · fixes (≤5) · one question
           │                    │             (the answer → conversations.md, in their words)
           └────────────────────┘   3–5 rounds, said up front
                                     ceiling: two reviews with the same count →
                                     a different angle, mode, or an interview — never a relaxed criterion
```

**The rubric has sources, like every other fact.** Most colleges publish no scoring rubric
for an essay. What exists is used word for word and cited; the rest is derived, and says
so:

| Tier | Source | Example |
|---|---|---|
| 1 | the college's own guidance for the prompt — "what we're looking for", word for word, with URL and date | the UC Personal Insight Questions' per-question guidance; MIT's and the Common App's prompt notes |
| 2 | the Common Data Set § C7 — how much the essay weighs at that school | "Application Essay: Very Important" (CDS 2024-25) |
| 3 | reader-training material that became public | the reader guidelines surfaced in the Harvard SFFA case |
| 4 | derived — our reading of what a strong answer to this prompt does | the why-us table in `essay-coach/references/eval.md` |

`college-research` fetches tiers 1–2 into the dossier so the brief can cite them. A
criterion with no tier above 4 is legitimate, and labeled.

**The student is in the loop, not at the end of it.** They choose the angle (and often
overrule ours, rightly). They choose the mode. When present, they score their own draft
against the rubric *before* seeing the review — the gap between their read and ours is
the coaching, not the fixes. The review is written either way, with their read marked
pending if they haven't given it; the loop never blocks on the student. They decide which
"one big thing" to act on. Their answer to the review's question is new material,
appended in their words. A draft says who wrote it on its first line, and the package
refuses to build without that line — the student's ownership made mechanical.

**Feedback comes from three places, ranked.** A teacher's or counselor's reaction in
`feedback.md` outranks the coach's review. Next is an independent **cold reader**: a
subagent that reads the draft as an admissions reader does, in two minutes, without the
brief. It returns three lines (the impression, what it remembers, the one question it is
left with) and catches what a rubric cannot: an essay that meets every criterion and is
forgettable. The coach's review is the third tier and the only one that scores.

**Mode B samples are real, published essays, cited** — the *Essays That Worked*
collections (Johns Hopkins, Hamilton, Connecticut College) — never ones the agent writes.
"A different student, a different topic" is then literally true, nothing is made up, and
the EXAMPLE header carries its URL.

**The frameworks the hints draw on** are named in `essay-coach/references/patterns.md`
with attribution: narrative vs. montage structure and the values exercise (Ethan Sawyer),
voice and the cliché list (Harry Bauld), the "so what?" test, and the UC guidance as the
model of prompt-specific criteria.

**What code holds** — `check_draft.py`: the author header, and every name, number, and
quoted phrase in an agent draft present in the student's record or a research file. What
code cannot see — a made-up feeling, a sensory detail — stays with the coach. That is why
the draft is a file *before* it is shown: a draft that exists only in a reply is
can be pasted straight into an application, and nothing can check it. Measured (e1, 2026-08-22): four
prose rules held the law 2/2; more rules under deadline pressure broke it 0/2 and 0/3;
the file-first rule and the script held it 3/3.

### The list loop

`criteria.md` holds the hard filters, the deal-breakers in the student's words, the
weighted preferences, the family's ceiling (what the family says it can spend), and a Retired table
that keeps every dropped row with its reason. It is re-read in full before every list
operation. `colleges.md` names, per school, which criteria it meets and misses, dated. A
safety is all three: numbers above the range, admission near-certain, affordable without
a scholarship not yet won. If two passes at the list change nothing, the criteria contradict
each other and the student decides (a $25k ceiling and a $40k one are never averaged). Where the two
standards differ: an essay rubric is external and fixed — the college wrote
the prompt — while list criteria are the student's own and really do change. So
`criteria.md` is fully living with an audit trail, and `brief.md` is only half living.

### The aid loop *(not built; promise 5)*

The family's ceiling against each school's net price from its own calculator, the aid
calendar on the tracker, outside scholarships found and dated, merit never counted before
it is in writing. Its record is `aid.md`. Its ceiling: two revisions with the same gap
between the family's ceiling and the cheapest school → the family's decision.

---

## Where facts come from

```
  admit rate · net price      ┌──────────────────┐
  grad rate · earnings   ◀────│ College Scorecard│  federal, ~2yr lag,
                              │ scorecard.py     │  per-metric vintage probing
                              └──────────────────┘
  test ranges · what they     ┌──────────────────┐
  actually weigh (§C7)   ◀────│ Common Data Set  │  the school's own count,
                              │ (agent reads)    │  current year, costs no quota
                              └──────────────────┘
  deadlines · required        ┌──────────────────┐
  essays · programs      ◀────│ College's site   │  SOLE valid source for a
                              │ (agent reads)    │  deadline. Nothing else counts.
                              └──────────────────┘
  campus texture         ◀────  reviews/forums — labeled impression, never fact
```

Precedence when sources disagree is in `citations.md`. In short: CDS wins on admissions
counts, the college's own page on deadlines, Scorecard on comparing schools. Never
average two sources.

---

## Enforcement: what's guaranteed vs. what's asked for

Honesty here beats pretending everything is guaranteed. Each skill's
`references/eval.md § Who checks what` says which of its rules are code and which are
judgment. This is the cross-skill view.

| Invariant | How | Where |
|---|---|---|
| Every essay draft says who wrote it on line one | **Code** — build refuses; the checker FAILs | `build_package.py`, `check_draft.py` |
| An agent draft names nothing not in the student's record or a cited research line | **Code** | `check_draft.py` |
| A student draft has a review beside it, and the review has its Rounds row | **Code** | `check_draft.py` |
| Every profile/criteria line carries a source tag; no `TODO:` carries a value | **Code** | `check_record.py` |
| The intake gate is counted from the files, not by the agent | **Code** — prints `gate N/4` | `check_record.py` |
| One owner per student file; the owner's schema has the shape; nobody else claims it | **Test** | `tests/test_data_model.py` |
| Every skill keeps the five-file shape; loops stay under the word cap | **Test** | `kit/tests/test_invariants.py` |
| Deadlines parse as ISO | **Code** — build refuses, names the school | `make_tracker.py` |
| Batch lookups don't silently lose schools; >100 UNITIDs refuses | **Code** | `scorecard.py` |
| Cost estimates don't mix field years; probe years track the calendar | **Code** + test | `scorecard.py` |
| Aid year maps to matriculation, not deadline year | **Code** + test | `make_tracker.py` |
| The coach's score never moves to match the student's read | *Measured conduct* | essay-coach loop; e3/e4 |
| Nothing outside the chosen folder is read during setup | *Measured conduct* — the judge reads the tool log | student-intake Setup; i2 |
| No college named or evaluated during intake | *Measured conduct* | student-intake; i1 |
| Never make up a fact about a college or student (the part code can't see) | *Discipline* | every skill, Tier 0 |
| Citations carry source + vintage | *Discipline* | `citations.md` |
| Append-only files are never rewritten | *Discipline* | `data-model.md` |
| No numeric fit or admission scores | *Discipline* | `voice.md` |

*Measured conduct* means a rule in a skill, bound to the step where it applies, that held
across multiple harness trials (`docs/evals/`). *Discipline* rows are where the real risk
sits: each is stated in the skill that would violate it, at the point of violation, with
the reason. Anything there that later becomes checkable moves up to Code — that is how
the gate count and the draft checks got there. (Tier 0 is the workspace `CLAUDE.md`,
loaded before any skill fires.)

---

## Decisions worth remembering

**One data format (JSON), everywhere.** `tomllib` is read-only in the standard library and
`meta.json` is rewritten constantly, so TOML would have meant a dependency or two formats.
Reasoning that would have been a TOML comment goes in `_note` fields instead — strictly
better, since a comment is invisible to the parser while a `_note` can be read and
surfaced at runtime.

**Student data never enters the plugin directory.** `students/` is created in the user's
working directory; the plugin holds only read-only resources; the Scorecard cache lives
under `~/.cache/`. An installed plugin may be read-only, and Cowork warns when plugin
files change beneath it. It also keeps a hard line visible: this system holds minors'
academic records and family finances, and none of it goes anywhere it isn't needed.

**Probe explicit years instead of Scorecard's `latest` alias.** `latest` hides which year a
number is from, so honest citation is impossible. Depth is per-metric because debt and
earnings lag far behind admit rates, and because every extra year costs ~28 query fields
against an ~8KB URL ceiling.

**Compress a late start rather than reporting it overdue.** The first version generated
fifteen already-late tasks for a student starting in September. A wall of red is
discouraging and tells them nothing; the same tasks squeezed into the runway that remains
tell them what to do first.

---

## Extending it

- **A new skill, or converting an existing one** → `docs/skill-shape.md` for the shape
  and `docs/PROCESS.md` for the ritual: design gate in an issue, build, independent
  review, harness measurement with receipts in `docs/evals/`.
- **A new student file** → a row in `data-model.md § Every file` naming its owner and
  change class, the shape in the owner's `references/schema.md` (linked from the row),
  and `build_package.py` if a counselor should see it. `tests/test_data_model.py` fails
  until the row, the section, and the claim agree.
- **A new calendar fact** → `config/calendar.json`, with a `_note` saying why.
- **A new date rule** → Python plus a test in `tests/test_dates.py`. Never prose.
- **A new external source** → add its precedence to `citations.md` first.
- **A new rule for a skill** → only after a measured miss, at the step where it applies,
  and measured again (`skill-shape.md`). A rule nobody measured is a wish.
