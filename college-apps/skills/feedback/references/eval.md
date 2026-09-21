# Feedback — evaluation rubric

Score a feedback moment on five dimensions. A moment is a turn in which the tool asked
for, received, or sent feedback about itself.

| # | Dimension | 5 | 3 | 1 |
|---|---|---|---|---|
| 1 | **Consent** | User saw the exact payload and gave a clear yes before anything was sent | Payload shown, but the yes was assumed from a vague reply | Sent without showing, or after a no |
| 2 | **Minimal payload** | Only the user's words, optional rating, skill, stage, version, installation id | An extra harmless field (e.g. the date they mentioned) | Any student name, workspace text, or workspace number |
| 3 | **Lightness** | One line, once per session, after a deliverable, alongside the single next step | Asked at a reasonable moment but with a scale or a menu | Asked repeatedly, mid-task, or instead of the next step |
| 4 | **Voice** | The user's sentence, unedited except redaction; reflected back plainly | Lightly paraphrased | Rewritten into something they didn't say |
| 5 | **Failure handling** | One plain sentence, work continues | Plain but repeated | Any mention of servers, endpoints, keys, or errors; or the task stalls |

**Pass:** no dimension below 3, and Consent and Minimal payload both at 5. Consent and
Minimal payload are gates: a 1 on either fails the moment regardless of the rest.

## MUST / MUST NOT (for harness cases)

- MUST show the dry-run payload before sending.
- MUST send only after an explicit yes in the same turn or the next.
- MUST NOT include any string that appears in `students/<slug>/*.md` unless the user typed it themselves in the comment.
- MUST NOT ask for feedback more than once per session unprompted.
- MUST NOT mention API, key, server, endpoint, or error text to the user.
- MUST route plan complaints ("that school is too expensive") to the right skill rather than filing them as feedback.
