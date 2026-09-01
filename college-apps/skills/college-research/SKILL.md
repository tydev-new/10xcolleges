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
| Evaluates the school through this student's major and residency | `students/<slug>/research/<college-slug>.md` |
| Cites at least 2 distinctive academic resources for essays | `students/<slug>/research/<college-slug>.md` |
| Names at least 2 genuine friction points / watch-outs | `students/<slug>/research/<college-slug>.md` |
| `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_research.py ...` passes | Terminal |

---

## Prerequisites

- **Required:** `students/<slug>/profile.md` (unweighted GPA, test plans, intended major) and `students/<slug>/criteria.md` (budget ceiling, residency, deal-breakers).
- Dossier destination: `students/<slug>/research/<college-slug>.md`.

---

## Sequences and loops

### The research sequence

**Runs when** asked to research a college or when list building/essay coaching requires factual grounding.

1. **Federal Scorecard:** Query `scorecard.py search` and batch `scorecard.py get --unitid` for federal net price by income, student debt, and completion rates. (If quota exhausted, proceed to CDS/institutional pages).
2. **Common Data Set (CDS):** Look up the school's latest CDS:
   - Section C1 (admit rate) and Section C9 (enrolled middle 50% SAT/ACT).
   - Section C7 (what the school weighs: rigor, GPA, essays, demonstrated interest).
   - Section B22 (freshman retention) and Section H2 (percentage of need met).
3. **Academic Department Audit:** Check `<college>.edu/<department>` for:
   - Accreditation (e.g. ABET) and exact major degree title.
   - Admission by major: Does the student enter directly or face a pre-major weed-out pool?
   - Distinctive resources for essays (named maker spaces, research centers, capstones).
4. **Cost & Financial Aid:** Calculate realistic net price for *this student's residency* (in-state vs. out-of-state), checking automatic merit grids and need-based threshold policies against the family budget ceiling.
5. **Friction & Campus Texture:** Check student forums and reviews (Reddit, Niche) for class sizes, housing shortages, and culture.
6. **Write the Dossier:** Write `students/<slug>/research/<college-slug>.md` following the schema (`schemas/research.md`).
7. **Sync:** Update `colleges.md` and `meta.json` if the research alters the school's tier, deadline, or status.

**Exits** when `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_research.py students/<slug>/research/<college-slug>.md` passes clean.

---

## Moment rules

1. **Every number carries a source and year/date:** Admit rates, percentiles, tuition figures, and deadlines must carry inline citations (e.g., `[CDS 2024-25 §C1]`).
2. **Nothing from memory:** Look it up every time. If a number cannot be found, output `Not found — needs checking` with the admissions contact info; never guess.
3. **Lead with cost when cost is the problem:** Never bury an out-of-state budget gap under paragraphs of campus praise.
4. **Two friction points mandatory:** Every real school has trade-offs (secondary major gates, large lectures, housing crunches, or weather). Name them honestly in `Watch out for`.
5. **Label student sentiment as impression:** Always prefix qualitative notes from forums with: `Impression, not data: ...`.
6. **Never ask for household income upfront:** Present institutional need-based policy thresholds (e.g. "covers full tuition under $140k") and ask if that threshold is a possibility for offline parent verification.

---

## Session close

Before replying to the student on EVERY turn:
1. Sync `colleges.md` and `meta.json` if list tiering or deadlines changed.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_research.py students/<slug>/research/<college-slug>.md` as the absolute final tool call on EVERY turn. If you edit any file, re-run `check_research.py` before speaking. Never reply without running `check_research.py` last.
3. Every reply ends with ONE next step and its reason.
