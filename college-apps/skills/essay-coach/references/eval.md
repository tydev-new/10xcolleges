# Essay coaching — how to judge the work

`SKILL.md` names the destination; this file is how to tell it is
reached, and who checks.

## Who checks what

- **Structure → `${CLAUDE_PLUGIN_ROOT}/scripts/check_draft.py`** at every draft and at close: the author header on the first line, and every name, number, and quoted phrase in an agent draft present in `profile.md`, `conversations.md`, or `research/` — the checkable half of "invent nothing". `build_package.py` refuses to build on a missing header — the one hard stop in this product. What code cannot see — an invented feeling, a sensory detail, a role — stays with you.
- **Language against written rules → no checker-subagent.** The
  student's words are the student's; the agent's drafts carry their
  label. Nothing here is checked against a never-say list.
- **Everything semantic → you, at the moment**: whether a criterion is
  actually met, whether a drift is better or easier, whether the
  material is thin enough that drafting would mean inventing.

## The destination, judged

- **The brief is on file before any draft**, split Fixed / Living, the
  rubric 4–6 checkable criteria with the word count and its retrieval
  date; the angles shown and the student's reaction taken before
  anything was written.
- **Every draft declares its author**, verbatim marker, first line; a
  student rewrite is a new file.
- **Every review opens against the brief** with the count, and the
  rubric is byte-identical to the previous review's unless the college
  changed the prompt, it was transcribed wrong, or the CDS §C7 turned
  up — with the reason recorded.
- **No sentence of the student's was rewritten in a review** — pointed at, never fixed; the student's read was taken BEFORE the coach's and both appear; the review's question was answered into `conversations.md`.
- **The cold reader ran** — three lines in the review, or VOID and why.
- **A Mode C draft was never treated as submit-ready**: the cost was said once, the draft labeled, the rewrite-from-scratch instruction given, and the student's rewrite is a new `STUDENT DRAFT` file. Nothing was polished for submission that the student had not substantially written.
- **Every college fact in a draft or a prompt carried its source**, from `research/<college>.md` or the student's own words — no uncited feature, program, or campus detail.
- **Nothing was invented** — no event, emotion, quote, or detail that is
  not in `profile.md` or `conversations.md`; thin material led to an
  interview, not to plausible fiction.

## The rubric — what a criterion must be, and where it comes from

Checkable yes/no, never from generic essay advice; a criterion you can't answer yes or no about is decoration. **Every criterion carries its source tier**, like every other fact in this product — most colleges publish no scoring rubric, so what exists is used verbatim and the rest is derived and says so:

| Tier | Source |
|---|---|
| 1 | the college's own guidance for this prompt, verbatim — URL and retrieval date (the UC Personal Insight Questions' per-question guidance is the model) |
| 2 | the Common Data Set § C7 — how much the essay weighs at this school, with the year |
| 3 | reader-training material that became public (e.g. the reader guidelines from the Harvard SFFA case) |
| 4 | derived — our reading of what a strong answer to this prompt does; labeled "derived" |

The round's score is the count of criteria met; the ceiling is two reviews with the same count.

## The three reads, ranked

A teacher's or counselor's reaction in `feedback.md` outranks the coach's review — map it to a criterion lightly, quote it above your own. The cold reader's three lines are judged for what the rubric cannot see (an essay that meets every criterion and is forgettable). The coach's read is the only one that scores. The student's own read comes first and is compared, never corrected — the gap is the coaching.

For a why-us supplement, the criteria that tend to be right:

| Criterion | What it looks like |
|---|---|
| Specific to this school | Names things that exist only here — a lab, a course number, a professor's actual work. Not "strong academics" or "beautiful campus." |
| Specific to this student | Connects to something they've actually done, not something they aspire to |
| Two-way | Says what they'd contribute, not just what they'd receive |
| Fits the length | 150 words means ~3 sentences of setup, tops |
| Not swappable | If you could paste the school's name out and another in, it fails |

## The angle, judged

Judge against the loop's rule 2: was a drift named first, and was "better" shown by the criteria still being met rather than asserted?
