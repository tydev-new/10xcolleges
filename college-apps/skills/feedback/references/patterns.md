# Feedback — patterns

## 1. When to ask

After the user has something in hand: the first college list, a research dossier, the
counselor package, an essay after review round two or later. Not after intake (they've
just given a lot and received little), not mid-loop, never on an error.

Once per session. The orchestrator tracks whether the check-in happened; skills don't
need to remember, they just don't ask if it's already been asked.

## 2. How to ask

The line goes *after* the single next step, so the next step stays the headline:

> Next: research Purdue and Michigan first — they carry the two nearest deadlines.
>
> One quick thing, if you have it: did this help? A word or a sentence and I'll pass it along. Or skip.

No scale. No "1 to 5". No "how would you rate". If they say "4 out of 5", keep the 4.

## 3. Turning an answer into a payload

| They say | Payload |
|---|---|
| "yeah that was useful" | `--comment "yeah that was useful"` |
| "4/5, the safeties felt like a stretch" | `--rating 4 --comment "the safeties felt like a stretch"` |
| "skip" / silence / a new question | nothing; move on |
| "the essay coach keeps rewriting my sentences" | `--skill essay-coach --comment "the essay coach keeps rewriting my sentences"` — and also stop rewriting their sentences |

`--skill` and `--stage` come from what just ran. Never guess; empty is fine.

## 4. The show-then-send exchange

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/core/scripts/feedback.py" --skill college-list --stage 2 --rating 4 --comment "the safeties felt like a stretch" --dry-run
```
```json
{
  "comment": "the safeties felt like a stretch",
  "rating": 4,
  "skill": "college-list",
  "stage": "2",
  "version": "1.0.0",
  "client_id": "…"
}
```
> Send this? Only what's shown goes.

Yes → same command without `--dry-run` → relay: "Sent. Thank you — this goes straight to
the people building 10xcolleges."

## 5. What the installation id is, if they ask

A random string made once on this computer so the team can tell "one person said this
five times" from "five people said it". It isn't tied to a name, an email, or the machine.

## 6. Redaction

The script blanks emails and phone numbers as a safety net. It does not read the
workspace, so it cannot leak it; the only way student information reaches the payload is
if the skill puts it there — which is why rule 2 exists.

## 7. Feedback vs. a task vs. a criterion

- *"This was helpful"* → feedback.
- *"Can you redo the list with a bigger budget?"* → a task; the budget is a criterion
  change (`student-intake` / `college-list`). Not feedback.
- *"It keeps forgetting my budget"* → both: file the feedback, then fix the state so it
  stops happening.
