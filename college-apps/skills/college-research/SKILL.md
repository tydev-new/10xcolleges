---
name: college-research
description: Research a specific college and write a cited dossier — admit rate, test ranges, real cost and net price, the program the student actually wants, campus culture, deadlines, and an honest fit assessment against the student's profile. Use when a student asks about a particular school, its cost or admit rate, whether it's good for their major, or what it's like there.
---

# Research a college

Read `${CLAUDE_PLUGIN_ROOT}/docs/citations.md` before you write a single number. Every fact gets a source and a
vintage, or it doesn't go in. Read the student's `profile.md` too — a dossier that isn't
evaluated against this student is a brochure.

Output goes to `students/<slug>/research/<college-slug>.md`.

**Guardrails first:** if the working folder's `CLAUDE.md` is missing the
`college-apps guardrails` block, copy or append
`${CLAUDE_PLUGIN_ROOT}/templates/workspace-CLAUDE.md` before continuing
(`student-intake` § Part 0 has the full rule; refresh an outdated version only by offer).

## Step 1 — federal data first

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" search "Northeastern"     # find the UNITID
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" get --unitid 167358
```

This gives admit rate, test ranges, enrollment, sticker cost, **net price by family income
band**, grad rate, median debt, and earnings — each tagged with the year it's actually
from. Paste it in and build around it.

### Spend the quota carefully

Without `SCORECARD_API_KEY` set, this runs on the shared DEMO_KEY at roughly **10 requests
per hour** — which a 10-school list will blow through in one sitting if you fetch schools
one at a time. So don't.

**Batch the whole list in a single request** once you have the UNITIDs:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" get --unitid 167358,170976,201645
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" quota      # check before a big session
```

Working rules under DEMO_KEY:

- **Resolve UNITIDs first, then batch.** Each `search` costs a request; each batched `get`
  costs one regardless of how many schools are in it.
- **Responses cache for 30 days.** Re-running a school you've already fetched is free, so
  never re-fetch to "double-check" — read the dossier you already wrote.
- **Common Data Sets and college websites cost nothing.** When quota runs out, that's where
  the current-year admissions detail lives anyway. Keep working.
- **If you hit the limit**, say so plainly and keep going with CDS and college sites rather
  than stalling the session. Suggest the free key — 2 minutes, no approval wait, raises the
  limit to 1,000/hour — but don't make it a blocker.

## Step 2 — the Common Data Set

Scorecard runs ~2 years behind. For current admissions detail, find the school's CDS:

- Search `"common data set" site:<college>.edu`
- Or try `<college>.edu/ir/cds` or `<college>.edu/institutional-research`

Section C is what matters: C1 (applied/admitted/enrolled), C9 (test score percentiles),
and **C7 — the table of what they actually weigh.** C7 is the most useful and least-known
document in college admissions. It tells you in the school's own words whether they care
about essays, recommendations, demonstrated interest, or legacy. When a school marks
"Interest" as *Considered* or higher, that changes what the student should do — open the
emails, attend the virtual session, mention specifics in the supplement. Say so.

## Step 3 — the college's own site

Deadlines, required essays, and program details come from the school and nowhere else.
Record the retrieval date. Verify the **exact program name** the student wants — many
schools have a general engineering admit with major declared later, and that materially
changes the application.

Also check whether the school or division **admits by major**. A 15% university rate can
hide a 7% engineering or nursing or business rate. Getting this wrong mis-tiers the school.

## Step 4 — culture, honestly labeled

Student newspapers, Reddit, Niche, YouTube tours, and the school's own subreddit are fine
for *texture* — what people complain about, what they're proud of, whether the campus
empties on weekends. Label it as impression, never as fact:

> *Impression, not data:* students describe the campus as emptying out on weekends; the
> Greek scene is the dominant social structure for a large share of students. If that's
> what you meant by "I don't want a party school," this is worth a hard look.

## The dossier

```markdown
# Northeastern University
Boston, MA — private nonprofit, large city — UNITID 167358

## The short version
Three sentences. What this school is, why it's on your list, and the one thing to know.

## Admissions
- Admit rate: 5.6% (CDS 2025-26 §C1; Scorecard shows 6.8% for an earlier year)
- Middle 50% SAT: 1490–1560 (CDS 2025-26 §C9)
- Your position: your 1480 sits just below the middle 50%.
- Admits by major? Yes — Khoury (CS) is meaningfully harder than the overall rate.
- What they weigh most (CDS §C7): rigor, GPA, essays — all "Very Important."
  Demonstrated interest: Considered. Open their emails.
- Deadlines: ED I Nov 1, ED II Jan 1, RD Jan 1 (admissions.northeastern.edu, ret. 2026-08-12)

## Cost
- Sticker: $89,536 (Scorecard, 2024-25 field year)
- Average net price, your income band: $31,204 (Scorecard, 2024-25)
- Net Price Calculator: <url>  ← run this, the average is not your number
- Meets full need? No — 65% of need met on average (CDS 2025-26 §H2)
- **Against your $25k ceiling:** likely over by ~$6k/yr without merit aid.

## The program you want
Named program, degree, accreditation, what's distinctive, what's oversold.

## Fit — against your profile
**Works because:** co-op is six months of real paid engineering work, twice. You said you
learn by doing and you're tired of school being theoretical. This is the most direct
answer to that on your whole list.
**Friction:** you also said you want a campus that feels like a community. Co-op means a
third of your friends are gone at any given time.
**Turn-offs check:** you said no huge lectures — intro classes here run 300+.

## Verdict
Reach, and the money is the harder problem than the admission. Worth applying if you love
the co-op model enough to organize four years around it.

## Still unknown
- Whether co-op counts toward the 8-semester aid cap — call admissions. [needs checking]
```

## Rules

- **Every number carries a source and a year.** No exceptions.
- **Nothing from memory.** Look it up, every time, even for schools you "know."
- **"Not found — needs checking" is a real answer.** Say where you looked. Tell the student
  to call admissions; learning to do that is worth more than the fact.
- **Always evaluate against this student.** Every dossier ends with fit and friction tied
  to specific things they said. If you can't name a friction, you haven't looked hard
  enough — every school has one.
- **Lead with cost when cost is the problem.** Don't bury a $30k gap under three paragraphs
  about the honors college.

After writing, update the school's entry in `colleges.md` and `meta.json` if the research
changed the tier, deadline, or status — then regenerate the tracker.

*Every reply ends with ONE contextual next step — a sentence with its why, not a menu.*
