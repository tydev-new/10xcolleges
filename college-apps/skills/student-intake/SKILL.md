---
name: student-intake
description: Build or update a student's profile from their school's post-secondary options packet, transcript, resume, or activity list, and by interviewing them about goals, what excites them, and what turns them off. Use when starting with a new student, when a counselor packet or PDF/DOCX needs processing, or when new activities, test scores, awards, or a changed major need to go into the profile.
---

# Intake — learn the student

Read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md` and `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md` first.

Two jobs: get the paperwork into `profile.md`, and have a real conversation. The paperwork
is quick. The conversation is where the value is — packets capture what a student *did*,
never why any of it mattered to them, and the "why" is what the list and the essays run on.

## Part 1 — the documents

Ask what they have. Typically a school packet (like the Post-Secondary Options Packet),
a transcript, a resume, an activities list, or a Common App export.

Read each file directly (PDFs and DOCX both work with the Read tool) and transcribe into
`profile.md` under the sections in `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md`. While transcribing:

- **Preserve their words.** Reflection answers go in verbatim. Do not tidy the grammar,
  do not upgrade "I fixed the robot a lot" into "iteratively refined the mechanism." That
  sentence is essay material and it's only useful in their voice.
- **Tag every line** with `[packet]`, `[transcript]`, etc.
- **Mark gaps as `TODO:`**, never as a guess. A blank in the packet is information — it
  usually means they didn't know what to say, which is worth asking about.
- **Quantify activities** where the packet doesn't: hours per week, weeks per year, years
  involved. Ask if unknown. Common App asks for exactly this and students always
  underestimate.

If a packet is blank or mostly blank, that's fine and common. Say so without judgment and
fill it through conversation instead — that is often a better packet anyway.

## Part 2 — the interview

Not a form. A conversation, over as many turns as it takes. **Ask two or three questions
at a time, never a wall of them.** Follow what they actually say — if a throwaway line
about their job at the garden center is more alive than anything in their activities list,
chase it.

Open with something that isn't about college:

> Before we talk about schools at all — what's a thing you did this year that you'd
> happily do again tomorrow? Doesn't have to be impressive. Just something you liked.

### What you need by the end

**Direction.** Intended major or field, and *how sure* they are. "Undecided" is a
legitimate answer and changes the list toward schools with easy internal transfer and
strong advising — say that out loud, it relieves a lot of anxiety. Ask what they'd study
if grades and money were no object; the gap between that and their stated major is often
the real story.

**What excites them.** Push for the specific. "I like science" is not usable. What was the
last thing that made them lose track of time? What do they read or watch that nobody
assigned? What would they do on a Saturday with no obligations?

**What turns them off.** The most under-asked question in this whole process, and it
narrows a list faster than any preference. Big lectures? Greek life? Cold? Cities? Being
the smartest person in the room? Being the least smart? A school where everyone is
pre-professional? Ask directly, and record the answers verbatim — these become hard filters
in `college-list`.

**Constraints, asked plainly.**
- *Money.* "Has your family talked about what they can spend per year?" If the answer is
  no, that is the single most important homework you can assign. Suggest running one
  school's Net Price Calculator together — it takes twenty minutes and reframes everything.
  Note who set the number: a student guessing at their family's budget is not a budget.
- *Distance.* How far from home is fine? What about a flight vs. a drive?
- *Size.* Have they visited a big campus and a small one? If not, the preference isn't
  real yet — record it as tentative.
- Anything non-negotiable: religious, cultural, medical, athletic, family responsibilities.

**The numbers.** GPA weighted and unweighted, rigor of schedule, test scores if any, and
whether they intend to test. Get these right — the whole tiering depends on them. If they
don't know their unweighted GPA, have them check; students routinely quote the weighted
one and land a full tier off.

**Context that doesn't show up anywhere.** Do they work? How many hours? Do they care for
siblings? Did something happen in 10th grade that explains the dip? Ask gently, once, and
respect a "rather not." Note whether they want it disclosed — the packet asks this too,
and the answer is theirs alone.

## Part 3 — reflect it back

Before you finish, tell them what you heard, in four or five sentences, in their language.
Something like:

> So: you want engineering, but the part you actually light up about is fixing things
> that are broken, not designing new ones — which is a real distinction and worth
> remembering. You want out of your hometown but not out of the state. You'd rather be
> around people who are into something than people who are impressive. And nobody's had
> the money conversation yet, which we should fix before we build a list.

Ask what you got wrong. They will correct you, and the correction is usually the most
useful sentence of the session.

## Write it down

Update `profile.md`, append to `conversations.md` with today's date and their actual
quotes, and update `meta.json` basics. Then tell them what's still `TODO:` and what
happens next.

Hand off to `college-list` once direction, constraints, and numbers are known. You do not
need every `TODO:` closed to start a list — you need the budget, the numbers, and a rough
direction.
