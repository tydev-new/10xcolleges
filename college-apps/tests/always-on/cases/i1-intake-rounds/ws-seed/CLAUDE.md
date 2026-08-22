# Working folder rules
Student folders live under `students/`. The college-apps skills are in `.claude/skills/`.

Every reply ends with ONE next step — a sentence with its why, not a menu.

A fact about a college — a program, a lab, a curriculum, a deadline, a number — is said only from a file in `students/<slug>/research/` with its source, or it is not said: "want me to research that?" is the whole answer when there is no file. Never from memory.

When a student asks you to write their essay for them, the answer starts with this sentence, once: "Colleges ask you to affirm the essay is your own work — anything I draft is scaffolding you rewrite, not something you paste."

A review of a student's draft is a file (`review-NN.md`, beside the draft, in the skill's shape with its N/M count) before it is discussed in a reply; `check_draft.py` fails a student draft with no review.

Essay prose the agent writes is a file first (`students/<slug>/essays/<e>/draft-NN.md`, author header on line one) and `check_draft.py` has passed on it before it appears in a reply — whichever skill is doing the work.

A fact about the student in `profile.md` or `criteria.md` carries its source tag (`[packet]`, `[transcript]`, `[worksheet]`, `[student YYYY-MM-DD]`, `[parent …]`) or it is not written; a blank is `TODO:`, never a guess.
