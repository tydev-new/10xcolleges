# Essay coaching — how to judge the work

`SKILL.md` names the destination; this file is how to tell it is
reached, and who checks.

## Who checks what

- **Structure → `${CLAUDE_PLUGIN_ROOT}/scripts/build_package.py`** (`check_draft_labels`):
  every draft declares its author in its first line, or the package
  refuses to build — the one hard stop in this product, because an
  unlabeled agent draft is indistinguishable from the student's.
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
- **No sentence of the student's was rewritten in a review** — pointed
  at, never fixed.
- **A Mode C draft was never treated as submit-ready**: the cost was
  said once, the draft labeled, the rewrite-from-scratch instruction
  given, and the student's rewrite is a new `STUDENT DRAFT` file.
- **Nothing was invented** — no event, emotion, quote, or detail that is
  not in `profile.md` or `conversations.md`; thin material led to an
  interview, not to plausible fiction.

## The rubric — what a criterion must be

Checkable yes/no, derived from the prompt (and the school's CDS §C7
weighting when known), never from generic essay advice. A criterion you
can't answer yes or no about is decoration. The round's score is the
count of criteria met; the ceiling is two reviews with the same count.

For a why-us supplement, the criteria that tend to be right:

| Criterion | What it looks like |
|---|---|
| Specific to this school | Names things that exist only here — a lab, a course number, a professor's actual work. Not "strong academics" or "beautiful campus." |
| Specific to this student | Connects to something they've actually done, not something they aspire to |
| Two-way | Says what they'd contribute, not just what they'd receive |
| Fits the length | 150 words means ~3 sentences of setup, tops |
| Not swappable | If you could paste the school's name out and another in, it fails |

## The angle, judged

The rubric does not move; the angle may. A drift is *better* when the
new angle still satisfies the criteria — update Living with the reason.
A drift is *easier* when it quietly stopped answering the prompt — name
it before anything else in the review.
