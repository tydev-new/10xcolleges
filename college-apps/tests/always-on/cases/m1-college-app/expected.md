# Expected — m1-college-app: meta-orchestrator front door, triage, and multi-intent execution for Jordan K

Jordan asks where to begin with college applications, followed by providing major/budget criteria and requesting to add two safety schools (Michigan State and Purdue) to check the 2-safety floor.

## MUST
- **Workspace Discovery & Greeting:** In Turn 1, reads `students/jordan-k/profile.md` and greets Jordan with a concise status summary based on existing facts (GPA, SAT, school).
- **Single Next Step Principle:** In Turn 1, identifies what is missing (criteria and college list) and recommends ONE clear next action (defining criteria / building the college list) rather than dumping an overwhelming 7-stage menu.
- **Multi-Intent Fact Ingestion First:** In Turn 2, commits the budget ceiling ($30k/yr) and mechanical engineering preference to `students/jordan-k/criteria.md` with source attribution (`[student YYYY-MM-DD]` or `[parent YYYY-MM-DD]`), and appends to `conversations.md`.
- **List & Meta Synchronization:** In Turn 2, adds Michigan State and Purdue to `students/jordan-k/colleges.md` AND updates `students/jordan-k/meta.json` concurrently.
- **Safety Floor Verification:** In Turn 2, explicitly evaluates whether MSU and Purdue qualify as true safeties (both academically and financially under the $30k ceiling).
- **Deterministic Validation:** Runs `check_list.py` and `make_tracker.py` during Turn 2.

## MUST NOT
- MUST NOT: Re-interview Jordan on facts already present in `profile.md` (e.g. asking for GPA or test scores again).
- MUST NOT: Overwhelm the student with a multi-stage menu of all 8 application phases in Turn 1.
- MUST NOT: Execute list additions without syncing `meta.json`.
- MUST NOT: Classify a school as a safety if its estimated net price exceeds the $30k budget ceiling.
