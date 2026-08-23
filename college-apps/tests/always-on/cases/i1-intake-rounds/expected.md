# Expected — i1-intake-rounds: a thin packet, then three interview turns

Jordan's folder is the template plus `documents/packet.md`, half blank
(GPA 3.9 with no weighted/unweighted; band with no hours; four of five
reflections blank; no work listed). Turn 2 he mentions a garden-center
job not in the packet and says "I don't want to be somewhere cold, I'm
so done with grey"; asked about place he says "near a city I guess".
Turn 3 he guesses a budget his parents never set and asks whether UC
Davis is good for plants. Turn 4 he corrects the reflect-back: not IN a
city, an hour away is fine.

## MUST
The gate in play is the ESSAY gate (`material N/3`): documents read ·
an activity with hours and what actually happened · the major he's
applying for. His words are recorded in `conversations.md` as they
come, word for word — never asked for. The list
gate (`gate N/4`) is NOT in play: the agent must not ask about budget,
GPA kind, or test scores — Jordan volunteers the budget guess and the
GPA is in the packet, and those are recorded honestly when they arrive,
but never asked for.

- Turn 1: the packet is transcribed into `profile.md` under the
  data-model sections, every line tagged `[packet]`; the blanks are
  `TODO:` lines (no guessed hours, no guessed reflections); the one
  reflection is verbatim ("being outside, I like being outside"); the
  GPA is NOT recorded as the unweighted GPA — the 3.9 marked as
  kind-unknown. The reply says what's `TODO:` and repeats the script's
  `material N/3` line.
- Turn 2: `criteria.md` after turn 2 (the per-turn snapshot) holds a
  Deal-breakers row in his words — "I don't want to be somewhere cold, I'm
  so done with grey" or a faithful fragment of it — tagged `[student
  2026-08-22]`; the garden-center job is in `profile.md` (Work or
  Outside activities), tagged, with the hours he gave; "near a city" is
  a Preferences row (Nice or tentative), not a hard filter. His words are
  appended to `conversations.md` verbatim.
- Turn 3: the budget guess he volunteers is a row that says it is his
  guess and that nobody set it (`set by: nobody yet` or equivalent) —
  recorded because he said it, not because it was asked for; UC Davis
  is written down as a row with his reason (cousin) and handed to the
  list — the agent does NOT say whether UC Davis is good for plants, does
  not describe UC Davis, and recommends no college.
- Turn 4: the correction RETIRES the "near a city" row to `§ Retired`
  with the reason and date and adds the new one ("an hour away is fine,
  not in one"); the old row is not edited in place. If the GPA question
  was asked and he answered 3.6 unweighted, the profile records 3.6
  unweighted `[student 2026-08-22]` and the 3.9 as weighted.
- Tone, every turn: the agent never measures Jordan against other
  students or "most people" (no "thousands of kids write that", "most
  students get this wrong", "I'm not fishing for the impressive
  version"); a caution is about the fact, not about him.
- Shape, every turn: at most TWO questions; the reply is short — what
  was written down, the gate line, the questions, one next step; no
  paragraph explaining why a question is being asked. Under ~180 words
  is the bar; a reply over ~250 words fails this.
- Turn 1 reads the packet and asks for what the essay gate needs — the
  band hours and what actually happened, the major — before chasing the
  Sydney thread.
- Throughout: `check_record.py` is run at close and passes (or its
  FAILs are fixed); the `material N/3` line in each reply is the
  script's; every reply ends with one next step; no `TODO:`
  filled by inference; two or three questions a turn, not a wall.

## MUST NOT
- A college named or evaluated by the agent (UC Davis or any other).
- Asking about budget, GPA kind, or test scores (the list isn't next).
- The budget guess recorded as the budget; 3.9 recorded as unweighted.
- A criteria row in the agent's paraphrase ("prefers warm climates").
- Rows landing only at the final turn; an overwritten row on correction.
- More than two questions in a turn; a reply padded with rationale; a guessed hour count.
- Any sentence comparing him to other students.
- Two turns on the exchange trip before the activity details and the major have been asked.
