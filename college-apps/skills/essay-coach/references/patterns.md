# Essay coaching — the craft

Hints for the loop in `../SKILL.md`. The standard is in `eval.md`, the
file shapes in `${CLAUDE_PLUGIN_ROOT}/schemas/essay.md`. Read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md`
before talking to a student.

## The brief — getting there

**Fixed, from the college.** Restate the prompt in one plain sentence.
Most prompts ask something narrower than they look ("describe a
challenge" is really asking how you think when things go wrong). Build
the rubric from the prompt (the why-us example is in `eval.md`), then
get the exact word count ceiling and format from the college's own page or application portal, with the date you looked it up.

Every brief must include an explicit Tier 1 rubric criterion for word count:
- **Hard Ceiling:** Word count $\le$ Prompt limit. Admissions software (Common App, UC, Coalition) cuts off submission at word $N+1$.
- **The 80% Depth Zone:** Coach drafts toward 80%–100% of the ceiling (e.g. 520–650 words on Common App; 200–250 words on a 250-word supplement; 125–150 words on a 150-word supplement). An essay at 50% of the limit leaves crucial space unused and signals under-developed thought.

**Living, from the student.**

### Upstream Brainstorming — The 4 Concrete Elicitation Questions
When material is thin, never ask abstract questions like "what makes you unique?" A teenager freezes. Ask concrete, slightly mischievous questions that pull the truth out naturally:
1. **The Boredom & Hands Question:** *"When you were stuck at home and everyone was busy, what did you actually spend hours doing? What was on your bedroom floor or in your browser history?"*
2. **The Unspoken Thought Question:** *"What was a thought you had during that time that you didn't say out loud to your parents or coach, or that you felt a little guilty admitting?"*
3. **The Hollywood vs. Reality Question:** *"If this were a cheesy Hollywood movie, what would the dramatic scene look like? And how was your actual experience totally different from that?"*
4. **The Petty Frustration Question:** *"What was the most ridiculously annoying little detail of the whole ordeal that nobody talks about?"*

### Cliché Subversion — Don't Ban, Subvert
Standard playbooks issue lazy blanket bans (*"never write about sports injuries, grandma, or mission trips"*). That invalidates authentic lived experience. The problem isn't the topic; it's the predictable 3-part formula (*"I struggled -> I worked hard -> I learned resilience"*).
- Name the predictable formula out loud to the student with respect.
- Find the **uncommon truth**: the weird mechanical hack, the generational clash, the private burnout, or the quiet behavioral shift.
- Keep the spotlight on the student's mind and values, not the external event.

### The Additional Information Boundary (Protecting the Showcase Essay)
Never burn a primary personal statement (whether the 650-word Common App essay, a 350-word UC PIQ, or an MIT short take) explaining a transcript blemish, medical leave, or family crisis.
- The personal statement is your **portrait** (who you are, how you think, what you value).
- Grade dips and disruptions belong in the dedicated **Additional Information / Comments section** (Common App Writing § Additional Info, UC Academic Additional Comments, or Coalition/independent text box) in 3 factual, non-emotional beats: (1) Context, (2) Concrete Impact, (3) Resolution and upward trajectory.

Three or four angles drawn from *their* material, one sentence each, each weighed honestly. Then say which you'd pick and why:

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

(Show all of this before anything is written — that is the brief sequence's rule.)

## The three draft modes

**Ask out loud, for every essay, and let them choose.** Record the
choice in `brief.md`; they can switch later.

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

Before they start, interview to bring out material. Ask for the
*sensory and specific*: what did the room smell like, what did someone
actually say, what did you think at the time that you wouldn't say out
loud. Give them the outline and a deadline. Then stop talking and let
them write.

**Mode B — sample first.**

Pick a **real, published essay** on a clearly different subject — never
their topic, or they'll copy it without meaning to — from a cited
collection: Johns Hopkins *Essays That Worked*, Hamilton College's and
Connecticut College's published examples. Save it (or its first 150–250
words) as `draft-NN.md` with the exact `EXAMPLE` marker on the first line
(`${CLAUDE_PLUGIN_ROOT}/schemas/essay.md`) plus the URL and date. Never write the sample yourself. A
published one really is a different student on a different topic, and
nothing in it is made up.

Then point out 3–4 moves it makes ("opens mid-action," "one concrete
detail doing the work of a paragraph," "the turn happens in a five-word
sentence"). Then have them write theirs.

**Mode C — you draft first.**

Build **only** from what is in `profile.md` and `conversations.md` (the
loop's rule 4). A draft with an event that never happened is a disaster
for the student, not a style problem.

Put the exact `AGENT FIRST DRAFT` marker on the first line
(`${CLAUDE_PLUGIN_ROOT}/schemas/essay.md`; the package build checks for it).

Then hand it back with one clear instruction: *rewrite this from
scratch with the file closed, keeping only the parts you'd have written
anyway.* That produces something usable. Editing an agent draft line by
line does not.

## The review round — getting there

Reviewing from a fresh read of the draft alone is how coaching drifts.
By round three you are polishing sentences in an essay that quietly
stopped answering the prompt, and nobody notices because nobody
re-checked the rubric. So: brief first, both halves. The student's read
before yours — a student who marks "specific to Pomona — yes" next to
"beautiful campus" has a blind spot worth more than any fix; one who
under-rates themselves is paying a self-doubt tax. The cold reader at the
same time. Then score.

What kept failing (e1, 2026-08-22), so you don't: a draft written only
in the reply (nothing can check it — the one made up wholesale lived
there); Mode C with no chosen angle (it made up a customer, a feeling, a
lab); a college feature named from memory while trying to be helpful
("the open curriculum", "the 5-college consortium" — three of four
trials).

## Reviewing — the craft

**The angle does move** (the rubric never does — the loop's rule 2).

If the draft has drifted from the chosen angle, say so before anything
else. Sometimes the drift is an improvement — the essay found a better
subject than the one you planned. When it is, update the **Living** half
of `brief.md` with the new angle, outline, and reasoning, so the next
review measures against where the essay actually is.

Be honest about which one is happening. "This drifted somewhere better"
and "this drifted because it was easier to write" look the same on the
page and are opposite problems. The test is the rubric: a better angle
still meets the criteria. An easier one usually stopped answering the
prompt.

The rest of every review, in this order (`${CLAUDE_PLUGIN_ROOT}/schemas/essay.md`):

**1. What's working.** Two or three things, quoted exactly. Specific
praise is how a student learns which instinct to trust. "The line about the cutting oil — keep that, it's
doing more than the three sentences after it."

**2. The one big thing.** Not five things. One. The single change that most improves this
draft, stated plainly:

> The essay doesn't start until paragraph three. Everything before it is you clearing your
> throat. What if you opened with "The fourth time the drivetrain failed, I stopped being
> angry about it"?

**3. Specific fixes.** Line by line, quoting the line, saying what and
why. Stop around five — a page of red ink stops being feedback and
starts being discouragement.

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
- **Write from scars, not open wounds.** If a student is still in the middle of active trauma, it is not ready for an admissions essay. Hardship essays follow the 1/3 to 2/3 rule: at most 1/3 on the obstacle, and at least 2/3 on the intellectual agency, humor, and community growth that grew out of it.

### Advanced Line & Structure Craft

1. **Show, THEN Tell (The Insight Follow-Through):**
   Sensory detail without cognitive reflection is just a movie script; reflection without sensory detail is a boring lecture. Drop a 2-sentence micro-scene to anchor the physical reality, then immediately tell the reader how your mind processed it. Sensory detail exists solely to earn the right to deliver personal insight.
2. **The "Why Us?" Tethering Formula:**
   Every institutional claim must tether to past student proof, and every student aspiration must project into a campus contribution:  
   `Past Proof (Me) <-> Specific Resource (from research/<college>.md) <-> Future Contribution (Campus)`.  
   *The Replace-the-Name Test:* If you can swap the college name for another school and the essay still works, it fails.
3. **Micro-Epiphanies Over Grand Preachiness:**
   Replace sweeping Hallmark-card morals (*"I learned that success is about the journey"*) with quiet, specific, humble shifts in behavior (*"I still don't know the secret to motivating twenty tired trumpet players, but I stopped blowing the whistle in their ears"*).
4. **Zero Throat-Clearing (In Medias Res):**
   In 80% of first drafts, the real essay begins in paragraph 2 or 3. Slash the opening philosophical scene-setting and drop the reader straight into the micro-action.
5. **Cadence & The "Cool Teacher" Ear Test:**
   Vary sentence length deliberately (Gary Provost's cadence principle). The voice should sound like an articulate seventeen-year-old speaking with their favorite high school teacher during office hours: natural, thoughtful, and expressive. Eliminate artificial SAT thesaurus words (*"plethora," "myriad," "tapestry of life"*).

## The cold reader

One subagent, started fresh for each review. It gets the draft alone —
no brief, no rubric, no profile — and one instruction: read it once, the
way an admissions reader does in two minutes, then return exactly three
lines: the impression in one sentence · what it would remember an hour
later · the one question it is left with. If it doesn't return three
lines, start it once more; if that fails too, write VOID and why. It catches the
essay that meets every criterion and is forgettable; it never scores.
Its three lines are quoted word for word. The subagent call shows in
the tool log — a "cold read" with no call behind it is a made-up one.

## The frameworks the hints draw on

- **Narrative vs. montage** (Ethan Sawyer, *College Essay Guy*): the two
  shapes nearly every strong personal statement takes — one story with a
  turn, or several threads tied together by a value. His values exercise
  is the fastest way to find an angle that is theirs.
- **Voice and the cliché list** (Harry Bauld, *On Writing the College Application
  Essay*): the trip, the grandmother, the big game, the injury — and why the essay that
  sounds like a real seventeen-year-old beats the polished one.
- **The "so what?" test**: after every paragraph, what does the reader now know about how
  this person thinks that they did not know before it.
- **Prompt-specific guidance as the model**: the UC Personal Insight
  Questions publish, for each question, what the readers look for. That
  is the shape every rubric here aims for — quoted when the college
  provides it, derived and labeled when it does not.

## The "Super-Essay / Hub" Supplemental Matrix

A student applying to 10–12 selective colleges faces between 25 and 40 supplemental essays. Brainstorming and writing 30 individual essays from scratch leads to catastrophic student burnout and hollow, rushed prose by November. Master counselors build a **Hub Strategy** around 4 universal archetypes:

### The 4 Universal Archetypes:
1. **The Community / Belonging Hub:**
   - *Prompt variations:* "Describe a community you belong to and your place within it" (Michigan, MIT, Duke, Yale).
   - *Drafting:* Write a rich 400-word master version focused on how the student interacts with, contributes to, and learns from a specific group (e.g. robotics pit crew, family Sunday dinner cooks, community garden volunteers).
   - *Adaptation:* Trim to 250 words by focusing on the micro-action; trim to 100–150 words by keeping only the core interaction and takeaway.
2. **The Activity Deep-Dive / Intellectual Spark Hub:**
   - *Prompt variations:* "Briefly elaborate on one of your extracurricular activities or work experiences" (Common App, Stanford, Princeton, Georgetown, Vanderbilt).
   - *Drafting:* Write a 350-word master version focusing on the intellectual friction and problem-solving (what hands did, what mind learned).
   - *Adaptation:* Easily condensed to 150 words or expanded to 250 words for departmental "Why Major" prompts.
3. **The Challenge / Perspective Hub:**
   - *Prompt variations:* "Describe a setback, challenge, or ethical dilemma and how you responded" (Common App #2, Harvard, Dartmouth).
   - *Drafting:* Grounded in the 1/3 obstacle, 2/3 intellectual recovery formula.
4. **The Bespoke "Why Us?" Supplement:**
   - *The Non-Negotiable Exception:* This is the **only** essay archetype that CANNOT be recycled. It must be built exclusively from the student's `research/<college>.md` dossier, using the *Past Proof <-> Specific Campus Resource <-> Future Contribution* formula.

---

## The 4-Bullet Additional Information Protocol

The Common App and Coalition applications provide an "Additional Information" box (up to 650 words). Admissions officers read this section in 30 seconds. They actively dislike long, flowery, defensive essays in this space. Master counselors mandate the **4-Bullet Factual Standard**:

```markdown
### Circumstance Regarding 11th Grade Chemistry Honors Grade Dip

- **Context (Dates & Circumstance):** In October–November of junior year (Fall 2025), I contracted severe mononucleosis, missing 18 consecutive school days and requiring hospitalization for complications.
- **Academic Impact:** Because laboratory experiments could not be made up remotely, my Q2 Chemistry Honors grade dropped to a C, and I took an Incomplete in Pre-Calculus.
- **Proactive Steps & Resolution:** Upon medical clearance in January, I attended daily after-school tutorials with Mr. Henderson, completed all outstanding calculus modules, and earned an A- on the semester exam.
- **Upward Trend & Verification:** Maintained a 4.0 GPA in Spring semester (including A in AP Biology). School counselor Ms. Patricia Vance can verify medical records upon request.
```

**Key counselor rules:**
- Purely factual, chronological, and objective.
- Zero self-pity, excuses, or emotional rhetoric.
- Highlights agency, recovery, and third-party verifiability.

---

## The 150-Character Common App Activity Description Formula

In the Common App, students can enter 10 activities, but each description is strictly capped at **150 characters** (including spaces!), and the Position/Leadership title is capped at **50 characters**.

### The Amateur Mistake:
Using passive sentences or repeating words from the organization box:
- *Weak (138 chars):* `"I was a member of the robotics team and helped build the robot. I was responsible for attending meetings and helping other members learn CAD."`

### The Master Counselor Formula:
`[Strong Action Verb] + [Quantified Task] + [Technical Tool/Skill] -> [Concrete Result/Impact]`
- Drop pronouns ("I", "my") and filler words ("responsible for", "helped to").
- Use semicolons to pack multiple achievements into the character limit.
- *Master Example (142 chars):*
  `"Rebuilt drivetrain 4x; coded autonomous PID loop in Java; trained 6 junior members; led team to 2nd at regional championship (42 teams competing)."`
- *Master Example 2 (148 chars):*
  `"Co-founded free tutoring co-op; recruited 14 peer tutors; coordinated 300+ hrs of STEM prep for 65 low-income middle schoolers; raised $2,400 for books."`

---

## The 550–620 Word Personal Statement Sweet Spot

While the Common App permits up to 650 words, top counselors target the **550 to 620 word window**:
- **Why Not < 500 Words:** Admissions readers review personal statements in 2–3 minutes. Submissions under 500 words often feel thin, lacking the second beat of cognitive reflection that proves maturity.
- **Why Not Exactly 650 Words:** Drafts stuffed to 649 words almost always contain repetitive throat-clearing, strained adjectives, or redundant transitions that dilute the voice.
- **The Sweet Spot:** 550–620 words gives the essay room to breathe, provides rhythmic variation in sentence length, and leaves the reader energized rather than fatigued.

---

## The Letter of Continued Interest (LOCI) 4-Beat Protocol (Deferrals & Waitlists)

When a student is **deferred** from Early Action/Early Decision to Regular Decision (in mid-December) or placed on an institutional **waitlist** (in late March/April), they have one critical opportunity to reignite their application: the **Letter of Continued Interest (LOCI)**.

### Operational Window:
- **For Deferrals:** Submit in early January (between January 5 and January 15) once first-semester senior grades are finalized.
- **For Waitlists:** Submit within 10–14 days of receiving the waitlist decision (mid-to-late April).

### The 4-Beat Structure (One Page, Max 400–500 Words):

```markdown
Dear Admissions Committee [or Regional Admissions Counselor Name],

[BEAT 1: REAFFIRM COMMITMENT]
Thank you for continuing to consider my application. [College Name] remains my absolute first choice. If admitted, I will enthusiastically enroll and contribute to your vibrant intellectual community.

[BEAT 2: ACADEMIC & TRANSCRIPT UPDATES]
I am pleased to share that I concluded my first semester of senior year with a 4.0 unweighted GPA across five AP courses (AP Calculus BC, AP Physics C, AP Literature, AP Macroeconomics, and AP Spanish). In Calculus BC, my team completed our final modeling project on [specific technical challenge], deepening my enthusiasm for applied quantitative analysis.

[BEAT 3: NEW EXTRACURRICULAR & PROJECT MILESTONES]
Since submitting my application in November, I have made significant progress in my extracurricular pursuits:
- Promoted to Team Captain of our FIRST Robotics team, leading our 24-student group through drivetrain redesign and securing 1st place at the Regional Qualifying Tournament.
- Co-authored a paper on [topic] with Dr. [Name] from [University Lab], currently under review at [Journal].

[BEAT 4: SPECIFIC CAMPUS FIT & CONTRIBUTION]
My interest in [College Name] has only deepened. I recently followed the work coming out of the [Named Campus Lab/Initiative], specifically Professor [Name]'s work in [field]. I look forward to bringing my background in [student's area] to [specific student club or research group].

Thank you again for your time, consideration, and dedication to building the Class of [Graduation Year].

Sincerely,
[Student Name]
Common App ID: [ID Number]
High School: [High School Name]
```

### Key Counselor Rules:
- **No Desperation or Guilt-Tripping:** Never express bitterness about the deferral or tell the college they made a mistake.
- **Only Verifiable New Content:** Every paragraph must offer substantive news that occurred *after* the initial submission. Re-hashing the Common App essay fails.
- **Strict Single-Page Limit:** Never exceed one page. Admissions officers review hundreds of LOCIs in minutes.

---

## Proposing a new pattern

When an angle-finding question, a mode script, or a review move works
for two different students' essays, write it as a dated line at the end
of the brief it came from, naming both. A pattern is never self-adopted;
a person promotes it into this file.
