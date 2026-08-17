---
name: college-list
description: Build or rebalance a student's college list into safety, target, and reach tiers, with the reasoning for each school tied to their profile, budget, and preferences. Use when a student asks where they should apply, wants schools added or cut, questions whether a school is a reach, or when the list needs checking for balance and affordability.
---

# Build the list

Read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md`, `${CLAUDE_PLUGIN_ROOT}/docs/citations.md`,
and the student's `profile.md` first. If the profile is mostly `TODO:` — especially
budget and GPA — go do `student-intake` instead. A list built on guesses wastes
everyone's fall.

**Guardrails first:** if the working folder's `CLAUDE.md` is missing the
`college-apps guardrails` block, copy or append
`${CLAUDE_PLUGIN_ROOT}/templates/workspace-CLAUDE.md` before continuing
(`student-intake` § Part 0 has the full rule; refresh an outdated version only by offer).

## Always start from criteria.md

**Re-read `students/<slug>/criteria.md` in full before every list operation** —
adding a school, cutting one, re-tiering, responding to counselor feedback. It is to
the list what `brief.md` is to an essay: the explicit standard, re-read so the list
can't quietly drift from what the student said in August. If it doesn't exist, build
it before any list — from the interview (`student-intake` owns that) or from
`${CLAUDE_PLUGIN_ROOT}/templates/criteria-worksheet.md`.

Hard filters and deal-breakers **cut** — a school failing one does not go on the list
"to keep options open." Preferences **score**, never eliminate. Every entry names
which criteria it meets and misses, by number. Editing rules (retire, never delete;
conflicting parent/student rows both stay; splitting compound criteria) and what to
do when the filters leave too few schools: `references/criteria-coaching.md`.

**Never compute a numeric fit score.** "82% match" is the same false precision as an
admission percentage, and it invites sorting by a number that means nothing.

## What tiers actually mean

Tier by *this student's* numbers against *that school's* admitted range, not by
prestige.

- **Safety** — numbers comfortably above the middle 50%, admission close to certain,
  **and the family can afford it without a scholarship they haven't won yet.** All
  three. An affordable-only-with-unwon-aid school is not a safety, and calling it one
  is the most damaging error in this whole process.
- **Target** — numbers inside the middle 50%. Plausible, not owed.
- **Reach** — numbers below the middle 50%, *or* the school admits under ~20%
  regardless of numbers. Every sub-15% school is a reach for everyone — give the
  reach speech (`references/presenting.md`) once, kindly.

Never state a numeric admission probability for an individual.

## Shape, then build

**8–12 schools; roughly a third each tier; at least two safeties the student would
genuinely be happy to attend.** Test that directly — "if this was where you were
going, how do you feel?" A grimace means it's a backup they'll resent; find another.
More than 15 schools usually means the list has no thesis (and guarantees bad
supplements); fewer than 6 is fragile. Say so, then respect their choice.

1. Apply the hard filters and deal-breakers from `criteria.md`. They eliminate first.
2. Anchor on the academics — verify the actual program exists, by name (ABET
   accreditation where it applies).
3. Start with in-state publics — the affordability floor and the most reliable
   safeties.
4. Add each school for a reason you can state in one sentence.
5. Check the money on every single one — sticker *and* net price at the family's
   income band. Schools get cut here; that's the system working.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" search "Case Western"   # UNITID
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" get --unitid 201645,170976,167358
```

Batch every candidate into one `get` — the shared DEMO_KEY allows ~10 requests/hour;
check `scorecard.py quota` first. Scorecard for cross-school numbers, the school's
CDS for current-year admitted ranges — cite both with vintages, and never tier from a
remembered admit rate.

## Write it down, keep it in sync

One entry per school in `colleges.md` (`## School Name — Reach|Target|Safety`), with
the criteria match, the why, the cited numbers, the money, the friction, and the
deadline from the college's own page — worked example, how to present the list to
the family, and the failure modes to name out loud: `references/presenting.md`.

Mirror every school into `meta.json` (tier, plan, deadline, status, rationale), then:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/make_tracker.py" students/<slug>
```

*Every reply ends with ONE contextual next step — a sentence with its why, not a menu.*
