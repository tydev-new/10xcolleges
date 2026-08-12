---
name: college-list
description: Build or rebalance a student's college list into safety, target, and reach tiers, with the reasoning for each school tied to their profile, budget, and preferences. Use when a student asks where they should apply, wants schools added or cut, questions whether a school is a reach, or when the list needs checking for balance and affordability.
---

# Build the list

Read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md`, `${CLAUDE_PLUGIN_ROOT}/docs/citations.md`, and the student's `profile.md` first. If the
profile is mostly `TODO:` — especially budget and GPA — go do `student-intake` instead.
A list built on guesses wastes everyone's fall.

## Always start from criteria.md

`students/<slug>/criteria.md` is to the college list what `brief.md` is to an essay: an
explicit, living checklist that gets re-read **in full, every time** the list is built or
rebalanced. Without it, the criteria live scattered across the profile and get reassembled
from memory on each pass — which is how a list ends up with four schools that violate
something the student said clearly in August.

**Re-read it before every list operation.** Adding a school, cutting one, re-tiering,
responding to counselor feedback — all of it starts by reading the criteria file top to
bottom. This is the same discipline as re-reading the essay brief before a review, for
the same reason.

If `criteria.md` doesn't exist yet, build it before building any list — either from the
interview (`student-intake` owns that) or by handing the student
`${CLAUDE_PLUGIN_ROOT}/templates/criteria-worksheet.md` to fill in. If they already have a
form, spreadsheet, or questionnaire from their school, read that and seed the rows from it
instead of making them answer everything twice.

### Keeping it current

The file changes constantly, and every change is an edit to the file, not a mental note:

- **Student says something new** → add a row, tagged `[student <date>]`.
- **Something turns out not to matter** → move it to **Retired** with the reason. Never
  delete. In November, when someone asks why an "in-state only" list has three
  out-of-state schools, the Retired table is the answer.
- **Student and parent disagree** → keep both rows, both tagged, and say out loud that
  they conflict. Do not average a $25k ceiling and a $40k ceiling into $32k.
- **A criterion is really two** → split it. "Not too big" usually means one thing about
  class size and another about social anonymity, and they filter differently.

### Using it to build

1. **Hard filters cut first.** A school failing any hard filter does not go on the list
   "to keep options open." That's what the filter is for.
2. **Deal-breakers are hard filters** written in the student's own words. Treat them with
   the same force.
3. **Preferences score, never eliminate.** Weight them Strong or Nice.
4. **Every school entry names the match.** One line: which criteria it satisfies and which
   it misses, by number, so the reasoning is auditable rather than vibes.

> **Michigan State** — meets H1 (net price $18k), H2 (ABET ME), H3 (90 min away).
> Strong on P1 (honors college keeps intro classes small). Misses P4 — this is a big
> school and you said you didn't want to feel anonymous.

**Never compute a numeric fit score.** "Michigan State: 82% match" is the same false
precision as an admission percentage, and it invites the student to sort by a number that
doesn't mean anything. Name what matches and what doesn't; let them weigh it.

### When the filters are too tight

If the hard filters leave fewer than about five plausible schools, stop and say so rather
than quietly returning a thin list:

> Your filters right now are under $25k, ABET mechanical engineering, within a day's
> drive, and no school over 15,000 students. Together those leave four schools, and two
> are reaches. Something has to give — my read is the size cap is the softest of the four,
> since the honors colleges at the bigger schools would solve most of what you're worried
> about. Want to try relaxing that one and see what opens up?

Propose *which* filter to relax and why. That's the counselor move — a student staring at
four criteria doesn't know which one is cheap to give up.

## What tiers actually mean

Tier by *this student's* numbers against *that school's* admitted range, not by prestige.

**Safety** — their GPA and scores sit comfortably above the school's middle 50%, admission
is close to certain, **and the family can afford it without a scholarship they haven't won
yet.** All three. A school that admits them and costs $40k they don't have is not a safety,
and calling it one is the most common and most damaging error in this whole process.

**Target** — their numbers land inside the middle 50%. Admission is plausible, not owed.
Most of the list lives here.

**Reach** — their numbers sit below the middle 50%, *or* the school admits under ~20% of
applicants regardless of numbers.

Say this part plainly, once, to every student:

> Any school admitting under about 15% is a reach for everyone. Not because you're not
> good enough — because they turn away thousands of students who are just as qualified as
> the ones they take. It stops being about merit and starts being about fit with what that
> particular class needs that particular year. Apply if you love it. Don't build a plan
> around it.

Never state a numeric admission probability for an individual. "You have a 30% shot" is
false precision dressed as expertise.

## Shape of a good list

8–12 schools. Roughly a third reach, a third target, a third safety, and **at least two
safeties the student would genuinely be happy to attend.** Test that last part directly:

> If everything else said no and this was where you were going — how do you feel?

A grimace means it's not a safety, it's a backup plan they'll resent. Find a different one.

More than 15 schools is usually a sign the list has no thesis, and it guarantees the
supplements get written badly. Fewer than 6 is fragile. Say so, then respect their choice.

## How to build it

Start from the student, never from a rankings list.

1. **Apply the hard filters and deal-breakers** from `criteria.md`. These eliminate, and
   they eliminate first. A school that violates a stated turn-off does not go on the list
   to "keep options open."
2. **Anchor on the academics.** Does the school actually have the program? A student who
   wants biomedical engineering needs the ABET-accredited BME degree, not a biology
   department with a health-professions advisor. Verify the program exists, by name.
3. **Start with in-state publics.** They are usually the affordability floor and the most
   reliable safeties. Build outward from there.
4. **Add schools for a reason you can state in one sentence.** If you can't say why this
   school and not the twenty like it, it doesn't belong on the list.
5. **Check the money on every single one** with `scripts/scorecard.py` — sticker *and* net
   price at the family's income band. Schools get cut here, and that's the system working.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" search "Case Western"          # get the UNITID
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" get --unitid 201645,170976,167358
```

Batch the whole candidate list into one `get` — on the shared DEMO_KEY you have roughly
10 requests an hour, and fetching schools one at a time will exhaust it mid-list. Check
`scorecard.py quota` before a long session.

Use Scorecard for the numbers and the school's Common Data Set for the current-year
admitted ranges. Cite both, with vintages. Never tier a school from memory of its admit
rate — those numbers have moved hard in recent years.

## Write it to colleges.md

One entry per school:

```markdown
## University of Michigan — Reach

**Against your criteria:** Meets H1 (net price $10.9k, under your $20k ceiling), H2
(ABET mechanical engineering), H3 (90 min from home). Strong on P2 (hands-on shop
culture). Misses P4 — 34,000 undergrads, and you said you didn't want to feel anonymous.

**Why it's here:** Top-5 mechanical engineering with a machine shop culture that matches
how you actually like to work. You said you want out of the house but not out of the
Midwest — this is 90 minutes away.

**The numbers:** Admit rate 15.6% (Scorecard, 2024-25 field year). Middle 50% ACT 31–34
(Scorecard, 2024). Your 30 sits below that, which is why this is a reach and not a target.

**The money:** In-state COA $34,654 (Scorecard, 2024-25). Average net price at your family's
income band $10,869. Under your $20k ceiling — this one works financially if you get in.

**Watch out for:** Engineering admits separately and is harder than the university rate.
Confirm the CoE-specific number before you decide on EA. [needs checking]

**Deadline:** EA November 1 (admissions.umich.edu, retrieved 2026-08-12)
```

Then mirror every school into `meta.json` — name, slug, unitid, tier, decision_plan,
deadline, app_type, counselor_letter, status, and a one-line `rationale` (the package and
tracker both read it). Regenerate the tracker:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/make_tracker.py" students/<slug>
```

## Present it like a counselor, not a spreadsheet

Lead with the shape of the list and the honest headline, then the schools:

> Here's a list of ten. Three are genuine long shots, four are real possibilities, and
> three you'll almost certainly get into — and I want to flag that two of those three are
> ones you sounded actually excited about, which is the part most lists get wrong.
>
> The thing I'd push back on: you have four schools in the reach column and only one is
> affordable at full price. If the money doesn't come through at Michigan, what's the plan?

Then invite the fight. Students and parents both have opinions about lists and they should
— it's their life and their money. Ask what feels wrong, what's missing, what they'd cut.
Expect to revise two or three times before it settles, and say that up front so revision
feels like progress instead of failure.

## Common failure modes to name out loud

- **All reaches, one safety.** The most common list a strong student brings in. Name the
  math: eight reaches at 8% each is not a plan.
- **A safety nobody wants to attend.** Covered above. Fix it.
- **Prestige-tiering.** Parents especially will tier by ranking. Redirect to fit and net
  price without making anyone feel dumb about it.
- **No financial safety.** Every list needs at least one school affordable *without* merit
  aid, since merit aid is not knowable in advance.
- **ED without a budget conversation.** Early Decision is binding. Never let a student
  file ED before the family has run that school's Net Price Calculator and agreed on the
  number. Say this every time it comes up.
