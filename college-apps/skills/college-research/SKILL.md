---
name: college-research
description: Research a specific college and write a cited dossier — admit rate, test ranges, real cost and net price, the program the student actually wants, campus culture, deadlines, and an honest fit assessment against the student's profile. Use when a student asks about a particular school, its cost or admit rate, whether it's good for their major, or what it's like there.
---

# Research a college

Build an investigative, cited research dossier on a single college, evaluating its academic programs, true costs, admissions policies, and friction points against this student's profile.

| Must be true | Where |
|---|---|
| Dossier covers Admissions, Academics, Cost, Deadlines, and Fit | `students/<slug>/research/<college-slug>.md` |
| Every number carries an inline citation with source and year/date | `students/<slug>/research/<college-slug>.md` |
| Evaluates major-specific selectivity (direct-admit vs. pre-major pool) | `students/<slug>/research/<college-slug>.md` |
| Net price compared to family budget ceiling with gap/surplus calculated | `students/<slug>/research/<college-slug>.md` |
| Cites at least 2 distinctive academic resources for essays | `students/<slug>/research/<college-slug>.md` |
| Names at least 2 genuine friction points / watch-outs | `students/<slug>/research/<college-slug>.md` |
| `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_research.py ...` passes | Terminal |

---

## Prerequisites

- **Required Student Context:** Inspect `students/` to locate the existing student folder (e.g. `students/<slug>/`). Always read `students/<slug>/profile.md` (unweighted GPA, test scores, intended major, state of residency) and `students/<slug>/criteria.md` (budget ceiling, hard filters, deal-breakers like D1 cold weather). If state of residence or intended major is `TODO:`, ask the student in-stride or apply graceful degradation per `schemas/requirements.md` (e.g. evaluate out-of-state COA if state unknown). Never invent a new student identity when an existing student folder is present.
- Dossier destination: `students/<slug>/research/<college-slug>.md`.

---

## Sequences and loops

### The research sequence

**Runs when** asked to research a college or when list building/essay coaching requires factual grounding.

1. **Federal Scorecard:** Query `scorecard.py search` and batch `scorecard.py get --unitid` for federal net price by income, student debt, and completion rates. (If quota exhausted, proceed to CDS/institutional pages).
2. **Common Data Set (CDS):** Look up the school's latest CDS:
   - Section C1 (admit rate) and Section C9 (enrolled middle 50% SAT/ACT and % submitting scores).
   - Section C7 (what the school weighs: rigor, GPA, essays, demonstrated interest, and decision plan leverage).
   - Section B22 (freshman retention) and Section H2 (percentage of need met).
3. **Academic Department Audit:** Check `<college>.edu/<department>` for:
   - Accreditation (e.g. ABET) and exact major degree title.
   - Admission by major: Does the student enter directly or face a pre-major weed-out pool?
   - Distinctive physical undergraduate facilities for essays (named maker spaces, research centers, design hubs like Bechtel Center, Herrick Labs, OEDK, Wilson Center).
4. **Cost & Financial Aid:** Calculate realistic net price for *this student's residency* (in-state vs. out-of-state):
   - Use standard freshman on-campus housing and food (~$10k–$11.5k) to compute the official non-resident COA (~$41k–$44k at Big Ten flagships).
   - Compute the true cost gap against the student's family budget ceiling (e.g. ~$11k–$14k gap vs $30k budget).
5. **Friction & Campus Texture:** Check student forums and reviews (Reddit, Niche) for class sizes, housing shortages, and culture:
   - Cross-check against the student's deal-breakers in `criteria.md` (e.g. flagging freezing/grey Midwestern winter if student has a warm-weather deal-breaker).
6. **Write the Dossier:** Write `students/<slug>/research/<college-slug>.md` following the schema (`schemas/research.md`).
7. **Sync:** Update `colleges.md` and `meta.json` if the research alters the school's tier, deadline, or status.

**Exits** when `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_research.py students/<slug>/research/<college-slug>.md` passes clean.

---

## Moment rules

1. **Every number carries a source and year/date:** Admit rates, percentiles, tuition figures, and deadlines must carry inline citations (e.g., `[CDS 2024-25 §C1]`).
2. **Nothing from memory:** Look it up every time. If a number cannot be found, output `Not found — needs checking` with the admissions contact info; never guess.
3. **Lead with cost when cost is the problem:** Never bury an out-of-state budget gap under paragraphs of campus praise. Calculate the cost gap explicitly.
4. **Two friction points mandatory:** Every real school has trade-offs (secondary major gates, large lectures, housing crunches, or weather). Name them honestly in `Watch out for`.
5. **Label student sentiment as impression:** Always prefix qualitative notes from forums with: `Impression, not data: ...`.
6. **Never ask for household income upfront:** Present institutional need-based policy thresholds (e.g. "covers full tuition under $140k") and ask if that threshold is a possibility for offline parent verification.
7. **Index selectivity to the major:** If engineering or business admits through a restricted pool or has a 15% admit rate, evaluate the school through the major's selectivity, not general university averages.
8. **Never recommend Early Decision if comparing aid:** If the family must compare out-of-pocket costs, steer toward Early Action or Regular Decision.
9. **The Out-of-State Public Net Price Trap:** Never cite third-party aggregators (CollegeSimply, Niche) or blended IPEDS averages for out-of-state net price. Public universities rarely meet need for non-residents. Assume the full non-resident sticker COA unless an official guaranteed waiver or published merit grid applies. Calculate the true cost gap explicitly.
10. **Primary sources only for admissions numbers:** Always cite official Common Data Sets ([CDS YYYY-YY §C1/C7/C9]), College Scorecard ([Scorecard]), or official university pages (.edu). Never cite third-party commercial consulting blogs or aggregators (Empowerly, PrepScholar, CollegeShortcuts, CollegeSimply) for admissions or cost statistics.
11. **Named physical undergraduate facilities for essay hooks:** When identifying essay hooks for STEM/maker students, always name physical facilities or maker spaces where undergraduates build projects (e.g. Bechtel Center, Herrick Labs, OEDK, Wilson Center). Course numbers or lecture formats alone do not fulfill this requirement.
12. **Out-of-state public COA sourcing:** Sourced non-resident Cost of Attendance must use standard freshman on-campus housing (~$10,000–$11,500/year) yielding ~$41k–$44k/year (e.g. ~$43,393 reported by Scorecard for Purdue). Never use unverified search snippets or off-campus housing proxies to inflate the COA to $48k–$50k and distort the cost gap.

---

## Session close

Before replying to the student on EVERY turn:
1. Sync `colleges.md` and `meta.json` if list tiering or deadlines changed.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_research.py students/<slug>/research/<college-slug>.md` as the absolute final tool call on EVERY turn. If you edit any file, re-run `check_research.py` before speaking. Never reply without running `check_research.py` last.
3. Every reply ends with ONE next step and its reason.
