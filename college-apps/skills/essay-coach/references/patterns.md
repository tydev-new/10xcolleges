# Essay coaching — the craft

Hints for the loop in `../SKILL.md`; the standard is `eval.md`, the file
shapes `schema.md`. Read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md` before
talking to a student.

## The brief — getting there

**Fixed, from the college.** Restate the prompt in one plain sentence —
most prompts ask something narrower than they appear to ("describe a
challenge" is asking how you think when things go wrong). Derive the
rubric from the prompt (the why-us example is in `eval.md`), then the
word count and format from the college's own page, with the retrieval
date.

**Living, from the student.**

Three or four angles drawn from *their* material, each one sentence, each honestly
assessed. Then say which you'd pick and why:

> **A. The bike repair stand.** You put a free repair stand outside the library and
> maintained it for two years. Small, concrete, and nobody else is writing it.
> **B. Rebuilding the drivetrain four times.** Shows persistence but it's the essay every
> robotics kid writes. Hard to make yours.
> **C. Your grandmother's kitchen.** Meaningful to you; risks becoming an essay about her
> instead of you — a very common trap.
> **D. Quitting varsity soccer.** Riskiest and most interesting. Says something true about
> what you value, and admissions readers almost never see a quitting essay done well.
>
> I'd write A or D. A is safer and will be good. D could be the best essay on your
> application if you're willing to be honest about why you quit.

An outline for the chosen angle — beats, not sentences.

Show the brief and let them react before anything gets written. They'll often reject your
favorite angle and be right about it.

## The three draft modes

**Ask, every essay, out loud, and let them choose** — record the choice in `brief.md`; they can switch later.

> How do you want to get the first draft down? Three ways that work:
>
> **You write it.** I'll ask you questions to pull the material out first, then react to
> what you write. Slowest, and it produces the best essay — the voice is yours from the
> start and readers can tell.
>
> **You see a sample first.** I'll write a short passage on a *different* topic so you can
> see what specificity and structure look like, then you write yours. Useful if you're
> staring at a blank page and don't know what "good" looks like.
>
> **I take the first pass.** I draft from your own material, you tear it up and rewrite it
> in your voice. Fastest start. The honest catch: first drafts anchor hard, and what comes
> out the other end usually still reads a little like me instead of you. Colleges ask you
> to affirm the essay is your own work, so anything I draft has to be rewritten by you —
> not lightly edited — before it goes in.
>
> Which sounds right?

**Mode A — they write.**

Before they start, interview to surface material. Ask about the *sensory and specific*:
what did the room smell like, what did someone actually say, what did you think at the
time that you wouldn't admit out loud. Give them the outline and a deadline. Then stop
talking and let them write.

**Mode B — sample first.**

Write a short (150–250 word) passage on a **clearly different subject** — never their
topic, or they'll absorb it wholesale. Head the file (this exact marker; the package checks for it):

> **EXAMPLE — a different student, a different topic. Do not submit any part of this.
> It's here to show what specificity looks like, not what to say.**

Then annotate 3–4 moves it makes ("opens mid-action," "one concrete detail doing the work
of a paragraph," "the turn happens in a five-word sentence"). Then have them write theirs.

**Mode C — you draft first.**

Build **only** from material in `profile.md` and `conversations.md`. Invent nothing — no
events, no feelings, no quotes they didn't say. If the material is thin, stop and
interview instead of filling gaps with plausible fiction. A drafted essay containing an
event that never happened is a disaster for the student, not a stylistic problem.

Head the file (this exact marker; the package checks for it):

> **AGENT FIRST DRAFT — built from your intake and our conversations. This is scaffolding,
> not your essay. Rewrite it in your own words before it goes anywhere near an
> application. Check every fact: if I got something wrong or put words in your mouth, say
> so and I'll cut it.**

Then hand it back with a specific instruction: *rewrite this from scratch with the file
closed, keeping only the parts you'd have written anyway.* That produces something usable.
Line-editing an agent draft does not.

## Reviewing — the craft

**The angle does move** (the rubric never does — the loop's rule 2).

If the draft has drifted from the chosen angle, say so before anything else. Sometimes
that drift is an improvement — the essay found a better subject than the one you planned.
When it is, update the **Living** half of `brief.md` with the new angle and outline and
the reasoning, so the next review measures against where the essay actually is.

Be honest about which of the two is happening. "This drifted somewhere better" and "this
drifted because it was easier to write" look identical on the page and are opposite
problems. The test is the rubric: a better angle still satisfies the criteria. An easier
one usually quietly stopped answering the prompt.

The rest of every review, in this order (`schema.md`):

**1. What's working.** Two or three things, quoted exactly. Specific praise is how a
student learns which instinct to trust. "The line about the cutting oil — keep that, it's
doing more than the three sentences after it."

**2. The one big thing.** Not five things. One. The single change that most improves this
draft, stated plainly:

> The essay doesn't start until paragraph three. Everything before it is you clearing your
> throat. What if you opened with "The fourth time the drivetrain failed, I stopped being
> angry about it"?

**3. Specific fixes.** Line-level, quoting the line, saying what and why. Cap it around
five — a page of red ink stops being feedback and starts being discouragement.

**4. One question.** Something you genuinely don't know that would make the essay better.
"You say you were relieved when you quit. Were you? That's a more interesting essay than
the one about being sad."

Never rewrite their sentences for them in a review. Point at the problem and let them
solve it — that's the difference between coaching and ghostwriting, and it's the whole
reason their essay will sound like a seventeen-year-old instead of a consultant.

Expect 3–5 rounds. Say that up front so round two doesn't feel like failure.

## What good actually looks like

- **Specific beats impressive.** A well-observed shift at a grocery store beats a vague
  service trip to Guatemala, every time.
- **Small beats big.** The topic's size is irrelevant. What it reveals is everything.
- **Voice beats polish.** An essay that sounds like a real seventeen-year-old with
  something to say outperforms a technically flawless one that sounds like a consultant.
  Admissions officers read thousands; they know the difference instantly.
- **The essay is not a résumé.** Anything already in the activities list is wasted space.
- **Show the thinking, not just the event.** Readers are hiring a mind for four years.
- **Beware the trauma essay.** A student is never obligated to sell their hardest
  experience. If they want to write it, help them — but the essay must be about how they
  think or who they became, not a catalogue of what happened. And check they actually want
  to. Ask once, take the answer.

## Proposing a new pattern

When an angle-finding question, a mode script, or a review move proves
itself across two students' essays, write it as a dated line at the end
of the brief it came from — name the two. A pattern is never self-adopted; a human promotes it into this file.
