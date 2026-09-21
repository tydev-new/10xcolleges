---
name: feedback
description: Pass along what the user thinks of 10xcolleges — what worked, what didn't, a rating, a bug — to the people building it. Use when the user offers an opinion about the tool itself ("this was helpful", "that list made no sense", "it keeps asking me the same thing"), asks how to give feedback, or answers the one-line check-in another skill asked after a big deliverable. Never sends anything about the student; only the user's own words about the tool, and only after they see it and say yes.
---

# Feedback — hearing how it's going

> **Shared kit.** Scripts, schemas, templates, and reference docs live in the `core` skill: `${CLAUDE_PLUGIN_ROOT}/skills/core` in Claude Code, or the `core` folder installed next to this skill in any other agent. Read every `${CLAUDE_PLUGIN_ROOT}/skills/core/...` path below as that folder. Scripts need `pip install -r core/requirements.txt`.


## Goal

Get one honest, user-written note about the tool to the team, with the user's explicit
yes, and nothing else attached — scored by `references/eval.md`.

| Must be true | Where |
|---|---|
| **Their words, not ours:** The comment is what the user typed for this purpose, unedited except for redaction | payload |
| **Nothing about the student:** No name, no file contents, no conversation text, no numbers from the workspace | payload |
| **Seen before sent:** The user sees the exact payload and says yes | the turn |
| **Once, lightly:** At most one unprompted ask per session, one line, after a big deliverable | the session |
| **Plain if it fails:** A send that fails gets one plain sentence, no jargon, and the work continues | the turn |

---

## Prerequisites

- None. Works without a student workspace; nothing is read from `students/`.
- Script: `${CLAUDE_PLUGIN_ROOT}/skills/core/scripts/feedback.py` (needs `requests`).

---

## Sequences and loops

### Taking feedback the user offers (a sequence)

**Runs when** the user says something about the tool — praise, a complaint, a bug, a
suggestion — or answers another skill's one-line check-in.

1. Reflect it back in one sentence so they know you heard it as feedback about the tool,
   not as a change to the student's plan.
2. Build the payload with `--dry-run` and show it verbatim:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/core/scripts/feedback.py" --skill <skill> --stage <stage> [--rating N] --comment "<their words>" --dry-run
   ```
   `<skill>` and `<stage>` are whatever just ran (`college-list`, `2`); if nothing ran,
   leave them empty. Rating only if they gave one.
3. Ask, in one line: "Send this? Only what's shown goes." If the answer is anything but a
   clear yes, drop it without comment and continue.
4. On yes, run the same command without `--dry-run`, and relay the script's one-line result.

**Exits** after one send or one decline. Don't circle back.

### The check-in after a big deliverable (the loop, run by other skills)

**Runs when** a skill has just handed over something substantial — a college list, a
research dossier, a counselor package, an essay after a review round — and no check-in
has happened yet this session.

- **Budget:** one ask per session, ever. If the user skipped it, it's done.
- **Each round:**
  1. End the deliverable's turn with one plain line, after the single next step:
     > One quick thing, if you have it: did this help? A word or a sentence and I'll pass it along. Or skip.
  2. If they answer with anything about the tool, run *Taking feedback the user offers*.
  3. If they answer with anything else, treat it as their next request and move on.
- **Seven moment rules:**
  1. **One line, once.** No menus, no rating scales pushed at them, no "on a scale of 1 to 5".
     If they volunteer a number, keep it.
  2. **Never attach the workspace.** Not the student's name, not a quote from `conversations.md`,
     not a number from `colleges.md`. If the user's comment itself names the student, keep
     it — it's their sentence — but never add anything.
  3. **Show before send, every time.** The dry-run output is what goes. Nothing is sent
     that the user hasn't seen on screen in that turn.
  4. **A no is a no.** "Skip", silence, a new question — all mean no. Don't ask why.
  5. **Don't fish.** Never ask leading questions ("wasn't the list great?"). Ask if it
     helped; take what comes.
  6. **Failure is one plain sentence.** If the script can't send, say so in its words and
     keep working. No talk of servers, endpoints, or errors.
  7. **Complaints about the plan are not feedback.** "That school is too expensive" is a
     criterion change — route to the right skill. "The tool keeps ignoring my budget" is
     feedback — take it, then also fix the budget.

---

## Handoffs

- After a send or a decline, return to whatever the user was doing; the orchestrator's
  single next step still stands.
- A bug report the user wants fixed in their own workspace is also a task: take the
  feedback, then do the task.
