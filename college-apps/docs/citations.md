# Sourcing and citation rules

Every number about a college that reaches the student must have a source you can point
to. A student will quote your tuition figure to their parents at dinner. Be right, or be
silent.

## Source hierarchy — prefer in this order

1. **College Scorecard** (US Dept. of Education). Authoritative and consistent across
   schools for: admit rate, net price by income band, median debt, completion rate, median
   earnings, enrollment size. Use `scripts/scorecard.py`. Its numbers run about two years
   behind — always print the field year the API returns, not the current year.
2. **The college's Common Data Set (CDS).** The richest source for admissions detail:
   test score ranges by percentile, what factors they weigh ("very important / important /
   considered / not considered"), waitlist numbers, need-met percentage. Usually at
   `<college>.edu/ir/cds`, or search for `"common data set" site:<college>.edu`.
   Cite the year of the CDS, e.g. CDS 2025-26.
3. **The college's own official pages** — deadlines, required essays, program pages,
   tuition tables, net price calculator. For deadlines especially: only the college's own
   admissions page counts.
4. **Common App / Coalition** — for what the application itself requires.

## Never use as a factual source

- Ranking sites' "chance me" calculators, Niche/Unigo prediction widgets, College
  Confidential threads, Reddit, or any site that doesn't say where its admit rate came from.
- Your own memory of a number. Model training data goes stale, and admit rates have moved
  hard in the last few years. Look it up. Every time.

Ranking sites are fine for *color only* (campus vibe, student reviews), labeled as
opinion, never as fact.

## Citation format

Inline, at the end of the sentence carrying the claim:

> Admit rate 17.7% (Scorecard, 2023-24 field year)
> Middle 50% SAT 1420–1530 (Common Data Set 2025-26, §C9)
> Regular Decision deadline January 5 ([admissions.example.edu/deadlines](https://admissions.example.edu/deadlines), retrieved 2026-08-12)

Three parts, always: **the number, the source, the vintage** (the year the number is
from). A cost figure without a year is not a citation.

## When sources disagree

They will. Scorecard's and the CDS's admit rates often differ by a point or two, because
they count different applicant pools and different years. When they disagree by
more than a rounding error:

- Report the CDS figure as primary (it's the school's own count).
- Note the difference in one clause: "about 18% (CDS 2025-26; Scorecard shows 17.7% for
  an earlier year)."
- Do not average them. Do not silently pick one.

## When you cannot find it

Write `Not found — needs checking` and say where you looked. This is a real, useful output.
It tells the student to call the admissions office, which they should learn to do anyway.
Never put a likely-looking estimate in place of a missing number.

## Cost — say which cost

The most misleading number in college admissions is sticker price. Always present:

- **Sticker** (tuition + fees + room + board), labeled in-state or out-of-state
- **Average net price** for the student's likely income band, from Scorecard
- A pointer to that school's **Net Price Calculator** URL

And say plainly: almost nobody pays the sticker price at a wealthy private college, and
nearly everyone pays it at an out-of-state public. That one sentence changes lists.

## Deadlines are load-bearing

A wrong deadline is the one error here that can actually cost a student an admission. Check every deadline again against the college's own page when the tracker is
built, and again in October. Record the date you looked it up next to it.
