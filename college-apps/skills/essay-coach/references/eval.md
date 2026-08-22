# Essay coaching — how to judge the work

`SKILL.md` says where the work has to get to; this file says how to tell
it got there, and who checks what.

## Who checks what

- **Structure → `${CLAUDE_PLUGIN_ROOT}/scripts/check_draft.py`** at
  every draft and at close: the author header on the first line, and
  every name, number, and quoted phrase in an agent draft found in
  `profile.md`, `conversations.md`, or `research/`. That is the half of
  "make nothing up" a script can check. `build_package.py` refuses to
  build on a missing header — the one hard stop in this product. What
  code cannot see — an invented feeling, a sensory detail, a role — is
  yours to catch.
- **Language → no checker-subagent.** The student's words are the
  student's; the agent's drafts carry their label. Nothing here is
  checked against a never-say list.
- **Everything that needs judgment → you, at the moment:** whether a
  criterion is really met, whether a drift is better or just easier,
  whether the material is so thin that drafting would mean making
  things up.

## The destination, judged

- **The brief was on file before any draft**, split Fixed / Living; the
  rubric has 4–6 yes/no criteria, the word count, and the date it was
  looked up; the angles were shown and the student reacted before
  anything was written.
- **Every draft says who wrote it**, exact marker, first line; a
  student rewrite is a new file.
- **Every review opens against the brief** with the score, and the
  rubric is identical to the previous review's unless the college
  changed the prompt, it was copied wrong, or the CDS §C7 turned up —
  with the reason written down.
- **No sentence of the student's was rewritten in a review** — pointed
  at, never fixed. The student's read was taken BEFORE the coach's and
  both appear. The review's question was answered into
  `conversations.md`.
- **The cold reader ran** — three lines in the review, or VOID and why.
- **A Mode C draft was never treated as ready to submit**: the cost was
  said once, the draft was labeled, the rewrite-from-scratch instruction
  was given, and the student's rewrite is a new `STUDENT DRAFT` file.
  Nothing was polished for submission that the student had not mostly
  written.
- **Every college fact in a draft or a prompt had its source** —
  `research/<college>.md` or the student's own words. No uncited
  feature, program, or campus detail.
- **Nothing was made up** — no event, emotion, quote, or detail that is
  not in `profile.md` or `conversations.md`. Thin material led to an
  interview, not to plausible fiction.

## The rubric — what a criterion must be, and where it comes from

A criterion is a yes/no question, never generic essay advice. A
criterion you can't answer yes or no about is decoration. **Every
criterion carries its source tier**, like every other fact in this
product. Most colleges publish no scoring rubric, so what exists is
quoted and the rest is derived and says so:

| Tier | Source |
|---|---|
| 1 | the college's own guidance for this prompt, quoted — URL and date (the UC Personal Insight Questions' per-question guidance is the model) |
| 2 | the Common Data Set § C7 — how much the essay counts at this school, with the year |
| 3 | reader-training material that became public (for example the reader guidelines from the Harvard SFFA case) |
| 4 | derived — our reading of what a strong answer to this prompt does; labeled "derived" |

The round's score is the number of criteria met. The ceiling is two
reviews with the same score.

## The three reads, ranked

A teacher's or counselor's reaction in `feedback.md` outranks the
coach's review — connect it to a criterion lightly and quote it above
your own. The cold reader's three lines are judged for what the rubric
cannot see (an essay that meets every criterion and is forgettable).
The coach's read is the only one that scores. The student's own read
comes first and is compared, never corrected — the gap is the coaching.

For a why-us supplement, the criteria that tend to be right:

| Criterion | What it looks like |
|---|---|
| Specific to this school | Names things that exist only here — a lab, a course number, a professor's actual work. Not "strong academics" or "beautiful campus." |
| Specific to this student | Connects to something they have actually done, not something they hope to do |
| Two-way | Says what they would contribute, not just what they would get |
| Fits the length | 150 words means about 3 sentences of setup, at most |
| Not swappable | If you could swap in another school's name and it still reads fine, it fails |

## The angle, judged

Judge against the loop's rule 2: was a drift named first, and was
"better" shown by the criteria still being met, rather than just
claimed?
