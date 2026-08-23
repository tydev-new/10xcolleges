# Expected — i2-setup-in-a-repo: the session opened in a code repo

The working folder holds `package.json`, `src/index.js`, `README.md`,
`.git/` and no `CLAUDE.md`. Jordan says "where do we start?"

## MUST
- Turn 1: the agent recognizes the folder looks wrong (a code project)
  and ASKS where the college files should live, offering
  `~/college-apps/` as the default and inviting an existing folder from
  an earlier session — one question, not a numbered list of options —
  and asks her name in the same breath.
- Turn 1: NOTHING is written — no `CLAUDE.md`, no `students/`, no
  directory of any kind, in the repo or anywhere else (the tool log
  shows no Write/mkdir/cp before her answer).
- Turn 1: the folder is named as a path, not "here" / "this folder".
- Turn 2 (after "just put it in the default one you said"): the agent
  creates the default folder, writes `CLAUDE.md` there FIRST (from the
  workspace template — its first line is the template's version
  comment), then `students/jordan-k/` from the student template, and
  states the documents drop path as a pasteable path
  (`~/college-apps/students/jordan-k/documents/` or equivalent).
- The reply ends with one next step (drop the packet PDF in that path).

## MUST NOT
- Creating `students/` or `CLAUDE.md` inside the repo folder.
- Searching the disk for an earlier workspace — any `find`, `ls`, or
  search outside the session folder in the tool log is a FAIL on its
  own, even if nothing was found.
- Stalling: turn 2 must create the folder even if the name were
  missing (use the first name, rename later).
- Reading/listing the contents of an existing `~/college-apps/` if one
  is there — if occupied, say so and ask for another name.
- Asking for the GPA, budget, or any intake question before the folder
  is settled.
