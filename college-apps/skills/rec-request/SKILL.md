---
name: rec-request
description: Plan recommendation letters — pick which teachers to ask, build a brag sheet for each one, and draft the ask itself. Use when a student needs letters of recommendation, asks who they should ask, needs a brag sheet or resume for a teacher, or needs to follow up with or thank a recommender.
---

# Recommendation letters

Read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md`, the student's `profile.md`, and `conversations.md`.

**Guardrails first:** if the working folder's `CLAUDE.md` is missing the
`college-apps guardrails` block, copy or append
`${CLAUDE_PLUGIN_ROOT}/templates/workspace-CLAUDE.md` before continuing
(`student-intake` § Part 0 has the full rule; refresh an outdated version only by offer).

Three jobs: pick the right people, give them what they need, and ask well. Most students
do all three badly and get generic letters as a result — not because the teacher didn't
like them, but because the teacher had four hundred words and no material.

## Picking recommenders

Start from `profile.md`'s "teachers who know you well," then pressure-test it. The best
recommender is **not** the teacher who gave the highest grade. It's the one who watched
the student struggle with something and keep going, or who saw them change.

Ask directly:

> Which teacher has seen you at your worst and still thinks well of you? That's usually
> the one who can write the letter that helps.

Check the requirements first — they vary and they're binding:
- Most selective colleges: two teachers plus the counselor.
- Many want **core academic subjects from junior or senior year.**
- Some engineering and science programs specify **one math or science** teacher.
- Some cap the total. Extra letters past the cap can actively annoy an admissions office.

Verify per school from the college's own site and record it in the research dossier.

Steer them toward balance: two teachers who'd say the same thing is a wasted slot. One who
saw the analytical side and one who saw the persistence or the collaboration covers more.

On supplemental letters (a coach, employer, mentor): only when that person saw something no
teacher could, and only if the school accepts them. Otherwise it's noise.

## The brag sheet

This is the actual deliverable. Write one **per recommender** — not one generic sheet
photocopied three times — to `recs/brag-sheet--<teacher-slug>.md`.

A teacher writing in November remembers the student in general and almost nothing in
particular. The brag sheet's job is to hand them three specific, usable moments *from
their own classroom*, so the letter has evidence in it.

```markdown
# For Ms. Alvarez — AP Physics, junior year

## What I'm applying to
Mechanical engineering. Michigan (EA, Nov 1), Case Western, Purdue, Michigan State.
Full list and deadlines at the end.

## What I'd love you to be able to speak to
Not a request to say these words — just what I hope comes through:
1. That I work a problem until it gives, past the point where it's fun.
2. That I help other people without being asked.

## Moments from your class you might not remember
- **The rotational motion unit, second semester.** I got a 61 on that test — the worst
  grade I've had. I came in during lunch four times over the next two weeks. You gave me
  the problem set from your old university course. I got a 94 on the retest and a 5 on
  the AP exam.
- **The pendulum lab.** My group's data was garbage because we mistimed the release. You
  let us redo it. We built a release mechanism out of a binder clip so the timing was
  consistent, and it worked.
- **Tutoring during 5th period.** I helped Marcus and two other juniors with kinematics
  most weeks from January on. Nobody assigned that; he asked and I kept showing up.

## Outside your classroom
Robotics build lead, 3 years, ~15 hrs/week in season — trained six freshmen on the mill.
Grocery cashier, 12 hrs/week since junior year. Fix and resell bikes; put a free repair
stand outside the public library that I've maintained for two years.

## The through-line, if it helps
I like things that are broken. Not designing new things — fixing things that already exist
and don't work. That's most of why I want mechanical engineering.

## Logistics
- Earliest deadline: **November 1** (Michigan EA)
- Submitted through: Common App — you'll get an email invitation from me
- Transcript and activities list attached
- My counselor is Mr. Reyes; he's handling the school report separately.
```

Rules for the brag sheet:

- **Only things that teacher actually witnessed** in the "moments" section. A physics
  teacher can't credibly write about the student's history essay.
- **Specific to the point of discomfort.** Test names, unit names, dates, actual grades,
  names of students helped. "I worked hard in your class" is worthless; "I got a 61 on the
  rotational motion test and came in four times at lunch" is a letter.
- **Include the failures.** The best letters describe recovery, and teachers are often
  reluctant to raise a bad grade unless the student signals it's fair game.
- **Never invent a moment.** Everything here comes from `profile.md` or the student's own
  mouth. If the student can't remember anything specific from that class, that is strong
  evidence they should ask a different teacher — say so.
- Keep it to about two pages. A teacher with 30 of these will not read four.

## The ask

Draft it, then have the student send it themselves. Save to `recs/request--<slug>.md` —
the counselor package surfaces these alongside the brag sheets, so a counselor can catch
a tone problem before it reaches a teacher.

**Timing: at least six weeks before the earliest deadline.** For November 1 deadlines that
means asking in September, and the good teachers fill up. If a student is late, say so
plainly and have them ask today.

**In person first, email after.** A student asking face-to-face gets a better letter than
one who sends a form. The email exists to carry the attachments and the dates.

Draft the in-person version as three or four sentences they can actually say out loud, not
a script that sounds like a lawyer wrote it. Then the follow-up email:

> Subject: Thank you — recommendation materials (Jordan Lee, Class of 2027)
>
> Hi Ms. Alvarez,
>
> Thank you for saying yes this morning — it means a lot. I've attached a sheet with some
> specifics from your class that might be useful, plus my transcript and activities list.
>
> My earliest deadline is **November 1** for Michigan Early Action. I'll send the Common
> App invitation today so it's in your inbox whenever you're ready.
>
> If it would help to talk through any of it, I'm free during 5th period most days.
>
> Thank you again,
> Jordan

Then: **the student must waive FERPA access** in the Common App. Explain why — a waived
letter is read as candid, an unwaived one is read as suspect. Nearly every counselor
recommends waiving.

## Follow-up and thanks

Track in `meta.json` under `recommenders`, then regenerate the tracker.

- **Two weeks before the deadline**, if not submitted: one polite check-in from the
  student. Draft it warm and short, never pushy. Teachers are busy and genuinely forget.
- **After submission**: a handwritten thank-you note. Say this plainly — it takes five
  minutes, teachers keep them for years, and the student will need this person again for
  scholarships and transfer applications.
- **In the spring**: tell them where you got in. Almost nobody does this. It's the part
  teachers actually care about.

## If a teacher says no

It happens, and it's usually a kindness — a teacher who doesn't think they can write a
strong letter is doing the student a favor by declining. Don't let the student read it as
rejection. Move to the next name and don't push the first one.

*Every reply ends with ONE contextual next step — a sentence with its why, not a menu.*
