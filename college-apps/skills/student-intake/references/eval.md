# Intake — how to judge the work

`SKILL.md` says where the work has to get to; this file says how to
tell it got there, and who checks what.

## Who checks what

- **Structure → `${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py students/<slug>`**
  every round and at close: every content line in `profile.md` and
  `criteria.md` carries a source tag (dated, for people); no `TODO:`
  carries a value (a number, a dollar amount, a hedge like "probably");
  the GPA says unweighted or is a `TODO:`; the budget row says who set
  it; `conversations.md` headers are in date order; **and it counts the
  gate** — `gate N/4` with what's missing. What it cannot see stays with
  you: whether a line is in their words or yours; whether a GPA labeled
  unweighted really is; whether a `TODO:` hides a guess in prose.
- **Language → no checker-subagent.** The words are the student's; the
  only language rule is that you did not tidy them.
- **Everything that needs judgment → you, as it comes up:** whether a
  throwaway line is the alive one, whether a preference is real or
  untested, whether a correction changes a row or retires it.

## The destination, judged

- **The gate in the reply is the script's line**, not a count of your
  own — a guessed budget is not a budget; a GPA without "unweighted" is
  not the GPA; "undecided, pretty sure" is a direction.
- **Rows were written in the turn they came up** — a turn-by-turn look
  at `criteria.md` shows each row appearing in the turn the student said
  it, not all at the end; and the row is their phrasing, not a
  paraphrase.
- **Every line tagged; no `TODO:` filled in by guessing** — a blank in
  the packet stayed a `TODO:`, with what to ask.
- **A correction retired the old row** with the reason, dated, and the
  number was not reused.
- **No college was named by the agent**; a college the student named is
  a row with their reason.
- **Context asked once**; a "rather not" recorded as that and not
  pursued.
- **What you heard was said back in their language**, and the
  correction that drew was written down.
- **The reply said what is `TODO:` and the next step** — one, with its
  why.

## Scoring

`gate N/4` is the score, printed by the script. The ceiling is two
rounds with the gate unchanged; the move then is homework (the Net
Price Calculator; checking the transcript), not another round of the
same question.
