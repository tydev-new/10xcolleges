# Intake — how to judge the work

`SKILL.md` names the destination; this file is how to tell it is
reached, and who checks.

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
- **Everything semantic → you, at the moment:** whether a throwaway line
  is the alive one, whether a preference is real or untested, whether a
  correction changes a row or retires it.

## The destination, judged

- **The gate in the reply is the script's line**, not a count of your
  own — a guessed budget is not a budget; a GPA without "unweighted" is
  not the GPA; "undecided, pretty sure" is a direction.
- **Rows landed during the turn they surfaced in** — a per-turn look at
  `criteria.md` shows the row the student's words appeared in, not a
  batch at the end; and the row is their phrasing, not a paraphrase.
- **Every line tagged; no `TODO:` filled by inference** — a blank in the
  packet stayed a `TODO:`, with what to ask.
- **A correction retired the old row** with the reason, dated, and the
  number was not reused.
- **No college was named by the agent**; a college the student named is
  a row with their reason.
- **Context asked once**; a "rather not" recorded as that and not
  pursued.
- **The reflect-back happened in their language** and the correction it
  drew was written down.
- **The reply said what is `TODO:` and the next step** — one, with its
  why.

## Scoring

`gate N/4` is the count, printed by the script. The ceiling is two rounds with the gate
unmoved; the move is homework (the Net Price Calculator; checking the
transcript), not a fifth round of the same question.
