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

(Shown before anything is written — the sequence's rule.)

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

Pick a **real, published essay** on a clearly different subject — never their topic, or
they'll absorb it wholesale — from a cited collection: Johns Hopkins *Essays That
Worked*, Hamilton College's and Connecticut College's published examples. Save it (or
its first 150–250 words) as `draft-NN.md` headed with the verbatim `EXAMPLE` marker
(`schema.md`) plus the URL and date. Never write the sample yourself — a published one
is literally a different student on a different topic, and nothing in it is invented.

Then annotate 3–4 moves it makes ("opens mid-action," "one concrete detail doing the work
of a paragraph," "the turn happens in a five-word sentence"). Then have them write theirs.

**Mode C — you draft first.**

Build **only** from material in `profile.md` and `conversations.md` (the loop's rule 4). A drafted essay containing an event that never happened is a disaster for the student, not a stylistic problem.

Head the file with the verbatim `AGENT FIRST DRAFT` marker (`schema.md`; the package checks for it).

Then hand it back with a specific instruction: *rewrite this from scratch with the file
closed, keeping only the parts you'd have written anyway.* That produces something usable.
Line-editing an agent draft does not.

## The review round — getting there

Reviewing from a fresh read of the draft alone is how coaching drifts — by round three
you are polishing sentences in an essay that quietly stopped answering the prompt, and
nobody notices because nobody re-checked the rubric. So: brief first, both halves; the
student's read before yours (a student who marks "specific to Pomona — yes" under
"beautiful campus" has a blind spot worth more than any fix; one who under-rates is paying
a self-doubt tax); the cold reader in parallel; then score.

What kept failing (e1, 2026-08-22), so you don't: a draft written only in the reply
(nothing can check it — the one invented wholesale lived there); Mode C against an
empty angle (it invented a customer, a feeling, a lab); a college feature named from
memory while being helpful ("the open curriculum", "the 5-college consortium" — three of
four trials).

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

(Point, never fix — the loop's rule 3. The budget and the ceiling are the loop's.)

## What good actually looks like

- **Specific beats impressive.** A well-observed shift at a grocery store beats a vague
  service trip to Guatemala, every time.
- **Small beats big.** The topic's size is irrelevant. What it reveals is everything.
- **Voice beats polish.** An essay that sounds like a real seventeen-year-old with
  something to say outperforms a technically flawless one that sounds like a consultant.
  Admissions officers read thousands; they know the difference instantly.
- **The essay is not a résumé.** Anything already in the activities list is wasted space.
- **Show the thinking, not just the event.** Readers are hiring a mind for four years.
- **Beware the trauma essay.** If they choose to write it (the brief sequence asks once), the essay must be about how they think or who they became, not a catalogue of what happened.

## The cold reader

One subagent, spawned per review: it gets the draft alone — no brief, no rubric, no
profile — and the instruction to read it once, the way an admissions reader does in two
minutes, then return exactly three lines: the impression in one sentence · what it would
remember an hour later · the one question it is left with. Rows, or it is re-spawned
once and then recorded VOID. It catches the essay that meets every criterion and is
forgettable; it never scores.

## The frameworks the hints draw on

- **Narrative vs. montage** (Ethan Sawyer, *College Essay Guy*): the two shapes nearly
  every strong personal statement takes — one story with a turn, or several threads tied
  by a value; his values exercise is the fastest way to find an angle that is theirs.
- **Voice and the cliché list** (Harry Bauld, *On Writing the College Application
  Essay*): the trip, the grandmother, the big game, the injury — and why the essay that
  sounds like a real seventeen-year-old beats the polished one.
- **The "so what?" test**: after every paragraph, what does the reader now know about how
  this person thinks that they did not know before it.
- **Prompt-specific guidance as the model**: the UC Personal Insight Questions publish,
  per question, what the readers are looking for — the shape every rubric here aims for,
  cited when the college provides it, derived and labeled when it does not.

## Proposing a new pattern

When an angle-finding question, a mode script, or a review move proves
itself across two students' essays, write it as a dated line at the end
of the brief it came from — name the two. A pattern is never self-adopted; a human promotes it into this file.
