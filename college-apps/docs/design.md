# Design

How this system is put together and why. For the *data* rules — what each file is and
what may change it — see `data-model.md`, which is the binding contract.

This document deliberately does **not** restate what individual skills do. The skills are
the specification; they're what the model reads at runtime. Anything duplicated here would
drift the first time a skill changed. What lives here is what no single skill can say:
structure, cross-cutting invariants, and the reasoning behind decisions that look
arbitrary later.

---

## Principles

**1. The student owns the work, and the artifacts prove it.**
Every output is a file the student can read, edit, and keep. Nothing is hidden in a
conversation that scrolls away. Where authorship matters — essays — it's recorded and
mechanically enforced.

**2. Facts carry provenance; the system never invents one.**
Every college number carries its source and vintage. Every profile line carries who said
it and when. `Not found — needs checking` is a valid, useful output. This is the rule
most likely to be quietly violated under pressure, so it's stated in three places and
enforced where code can reach it.

**3. Facts that drift live in config; rules that compute live in code.**
FAFSA's opening date is a fact and belongs in `config/calendar.json`. "A January deadline
belongs to the aid year that opened the previous October" is a rule and belongs in Python,
under test. Rules expressed as prose get re-derived on every run, and re-derived date
arithmetic is how a nine-month error hides in plain sight.

**4. Precision is never faked.**
No admission probabilities. No numeric fit scores. Tiers and named trade-offs instead. A
number implies a model that doesn't exist, and students sort by numbers.

**5. Degrade, don't fail.**
Rate limit hit → work from Common Data Sets. No API key → shared demo key. No Chrome →
print to PDF by hand. The only hard stops are the two places where continuing would
produce something misleading: a mistyped deadline, and an unlabeled essay draft.

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
   │  profile · criteria · colleges · conversations · feedback ·         │
   │  research/ · essays/ · recs/ · meta.json                            │
   └──────────────────────────────────┬──────────────────────────────────┘
                                      │ consumed by
   ┌──────────────────────────────────▼──────────────────────────────────┐
   │  scripts/            deterministic, no judgment                     │
   │  scorecard · make_tracker · fill_packet · build_package             │
   └──────────────────────────────────┬──────────────────────────────────┘
                                      ▼
                     students/<slug>/out/  →  xlsx · docx · html · pdf


   Read-only, shipped with the plugin          External sources
   ┌────────────────────────────────┐          ┌──────────────────────────┐
   │ docs/    voice · citations ·   │          │ College Scorecard API    │
   │          data-model · design   │          │ Common Data Sets (§C7)   │
   │ config/  calendar.json         │          │ College admissions pages │
   │ templates/ student · worksheet │          │ (deadlines — sole source)│
   └────────────────────────────────┘          └──────────────────────────┘
```

**The split that matters:** skills exercise judgment, scripts do not. Anything requiring a
decision about a student lives in a skill. Anything deterministic — date arithmetic,
spreadsheet layout, HTML generation, API pagination — lives in a script and is testable.
Where they meet, the model extracts (it's good at that) and the script formats (it's
reliable at that). `packet.json` → `fill_packet.py` is the clearest instance.

---

## The arc

Stages 1–3 are mostly sequential; 4–7 run in parallel and repeat. Skipping ahead produces
worse work — an essay written before the research is generic, a list built before the
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
the list; the same read in December changes nothing. The package is built to be sent early
and repeatedly.

---

## The two iteration loops

Both work the same way, and the symmetry is deliberate: **an explicit written standard,
re-read in full before every pass, so the work can't drift off what was agreed.**

### Essay loop

```
   prompt ──▶ brief.md ┬─ FIXED   prompt · rubric · word count   ← from the college
                       └─ LIVING  angle · outline · draft mode   ← from the student
                            │
                            ▼
                  student picks a mode:  A write · B sample · C agent-drafts
                            │
                            ▼
        ┌────────▶  draft-NN.md   (declares its author — enforced)
        │                │
        │                ▼
        │        re-read brief.md IN FULL
        │                │
        │                ▼
        │        review-NN.md  ── score against FIXED rubric
        │                │      ── what works · one big thing · fixes · a question
        │                │
        └────────────────┘  3–5 rounds
```

The asymmetry is the whole design: **a draft can never justify relaxing the rubric.** A
rubric that softens to fit what was written isn't a standard, it's a rationalization. The
angle may move (the essay found a better subject); the rubric moves only when the college
changes the prompt or we misread it.

### List loop

```
   interview / worksheet ──▶ criteria.md ┬─ hard filters   (cut)
                                         ├─ deal-breakers  (cut, in their words)
                                         ├─ preferences    (score, weighted)
                                         └─ RETIRED        (kept with the reason)
                                              │
                     ┌────────────────────────┘
                     ▼
        re-read criteria.md IN FULL before every list operation
                     │
                     ▼
        colleges.md — each entry names which criteria it meets and misses
```

**Where the two loops differ, and why:** an essay rubric is external and fixed — the
college wrote the prompt and doesn't care how it's going. List criteria are the student's
own and genuinely mutable — a student is allowed to decide they'd move further from home.
So `criteria.md` is fully living (with a Retired table for the audit trail) while
`brief.md` is only half living. Same mechanic, different mutability, because the sources
differ.

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

Precedence when sources disagree is in `citations.md`. Summary: CDS wins on admissions
counts, the college's own page wins on deadlines, Scorecard wins on cross-school
comparability. Never average two sources.

---

## Enforcement: what's guaranteed vs. what's asked for

Being honest about this is more useful than pretending everything is guaranteed.

| Invariant | How | Where |
|---|---|---|
| Every essay draft declares its author | **Code** — build refuses | `build_package.py` |
| Deadlines parse as ISO | **Code** — build refuses, names the school | `make_tracker.py` |
| Batch lookups don't silently lose schools | **Code** — warns by UNITID | `scorecard.py` |
| >100 UNITIDs refuses rather than truncating | **Code** | `scorecard.py` |
| Cost estimates don't mix field years | **Code** — flags the mismatch | `scorecard.py` |
| Probe years track the calendar | **Code** + test | `scorecard.py` |
| Aid year maps to matriculation, not deadline year | **Code** + test | `make_tracker.py` |
| Config shape matches what code expects | **Test** | `test_dates.py` |
| Required profile sections exist (unknowns are `TODO:`, not absences) | **Code** — check fails | `check_student.py` |
| Draft provenance present at session close, not only at package build | **Code** — check fails | `check_student.py` |
| `meta.json` in sync with `colleges.md` | **Code** — check fails | `check_student.py` |
| Stray files flagged before they become a second source of truth | **Code** — warns | `check_student.py` |
| Append-only log entries carry dates | **Code** — warns | `check_student.py` |
| Guardrails present before any skill loads | *Discipline* — every skill repairs it | `templates/workspace-CLAUDE.md` |
| Never invent a fact about a college or student | *Discipline* | every skill + workspace `CLAUDE.md` |
| Citations carry source + vintage | *Discipline* | `citations.md` |
| Append-only files are never rewritten | *Discipline* | `data-model.md` |
| criteria.md / brief.md re-read before each pass | *Discipline* | the two skills |
| No numeric fit or admission scores | *Discipline* | `voice.md` + workspace `CLAUDE.md` |

The *Discipline* rows are where the real risk sits. Each is stated in the skill that would
violate it, at the point of violation, with the reason — instructions with a stated reason
survive paraphrase better than bare rules. Anything on that list that later becomes
checkable should move up to Code.

**Where the discipline lives matters.** A skill's body loads only when its description
matches what the user said — so a guardrail that lives only in a skill fires only when
the model already judged that skill relevant. The rules that must hold *before any skill
loads* — never invent a fact about the student or a college, no chance percentages,
authorship, privacy — therefore also live in a ~300-word guardrails block that intake
copies into the user's own `CLAUDE.md` at setup (`templates/workspace-CLAUDE.md`, version-
marked, refreshed only by offer since the file is theirs). Every skill treats a missing
block as the first thing to repair. Open assumption, to verify on-platform: that an
installed plugin's own `CLAUDE.md` is *not* in an end user's context — the sibling
10xjobs project measured exactly that on Cowork, which is why the copy-at-setup
mechanism exists at all.

---

## Decisions worth remembering

**One data format (JSON), everywhere.** `tomllib` is read-only in the standard library and
`meta.json` is rewritten constantly, so TOML would have meant a dependency or two formats.
Rationale that would have been a TOML comment goes in `_note` fields instead — which is
strictly better, since a comment is invisible to the parser while a `_note` can be read
and surfaced at runtime.

**Student data never enters the plugin directory.** `students/` is created in the user's
working directory; the plugin holds only read-only resources; the Scorecard cache lives
under `~/.cache/`. An installed plugin may be read-only, and Cowork warns when plugin
files change beneath it. It also keeps a hard line visible: this system holds minors'
academic records and family finances, and none of it goes anywhere it isn't needed.

**Probe explicit years instead of Scorecard's `latest` alias.** `latest` hides which year a
number is from, making honest citation impossible. Depth is per-metric because debt and
earnings lag far behind admit rates, and because every extra year costs ~28 query fields
against an ~8KB URL ceiling.

**Compress a late start rather than reporting it overdue.** The first version generated
fifteen already-late tasks for a student starting in September. A wall of red is
discouraging and tells them nothing; the same sequence squeezed into the runway that
remains tells them what to do first.

---

## Extending it

- **A new stage** → a new skill in `skills/`, plus a routing line in `college-app`.
- **A new calendar fact** → `config/calendar.json`, with a `_note` saying why.
- **A new date rule** → Python plus a test in `tests/test_dates.py`. Never prose.
- **A new student file** → add it to the contract table in `data-model.md` with its
  mutability class, to the manifest in `check_student.py` (or the checker will flag it
  as stray), and to `build_package.py` if a counselor should see it.
- **A new external source** → add its precedence to `citations.md` first.
