---
name: student-intake
description: Use this skill when starting with a new student, when a school packet / transcript / resume / activities list / worksheet needs to go into the profile, or when something about the student changed (new scores, a new activity, a changed major). Builds profile.md (who they are) and criteria.md (what they want) in the student's own words, with a source on every line, up to the point where the college list can start.
---

# Intake — learn the student

## Goal

Build `profile.md` (who they are) and `criteria.md` (what they want) — **every line in the student's words, every line marked with its source tag, every blank an explicit `TODO:` without guessing** — up to the gate required by the next stage. Scored by `references/eval.md`; file schemas in `${CLAUDE_PLUGIN_ROOT}/schemas/`.

| Must be true | Where |
|---|---|
| **The essay gate** (default) — `check_record.py` reports `material N/3`: documents read (or "none"), ≥1 activity with hours and real details, target major + confidence level | `profile.md` |
| **The list gate** (when `college-list` is next) — `check_record.py` reports `gate N/4`: budget + who set it, unweighted GPA / test plan / state of residence, academic direction, hard filters & deal-breakers | `criteria.md`, `profile.md` |
| **Verbatim conversation log:** What the student said, dated and quoted word-for-word in quotes — the raw material essays are built from | `conversations.md` |
| **Source attribution:** Every profile claim and criteria row tagged with provenance (`[packet]`, `[transcript]`, `[student YYYY-MM-DD]`) | `profile.md`, `criteria.md` |
| **Audit trail:** Changed criteria moved to `## Retired criteria` with reasons; never overwritten | `criteria.md` |
| **Transparent status:** Reply explicitly states open `TODO:` items and the single next step | The reply |

## Prerequisites

- **Required:**
  - A working folder with a `CLAUDE.md` — none → run Setup first before any write.
  - A student folder `students/<slug>/` created from `${CLAUDE_PLUGIN_ROOT}/templates/student/`.
  - Read `${CLAUDE_PLUGIN_ROOT}/schemas/requirements.md`, `${CLAUDE_PLUGIN_ROOT}/schemas/profile.md`, `${CLAUDE_PLUGIN_ROOT}/schemas/criteria.md`, and `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md § Provenance` before the first write.
- **Optional:**
  - A school packet, transcript, resume, activities list, or Common App export (PDF and DOCX supported).
  - A completed `${CLAUDE_PLUGIN_ROOT}/templates/criteria-worksheet.md` or school questionnaire. Without documents, start directly with the interview.

## Loops and sequences

Setup runs once per folder. Documents are processed in sequence. The interview is the loop. Changes are handled via Update. What just arrived determines the mode.

### Setup — the working folder (a sequence)

**Runs when** there is no `CLAUDE.md` in the session's folder.

1. **Confirm the folder:**
   - *Normal folder:* State the path directly in your first reply: *"Everything I write lands in `<path>` — say the word if you'd rather use a different folder."*
   - *Suspicious folder* (home directory, code repository, system path, or unrelated files): Name the path ("`<path>` is a code project") and ask: *"Where should your college files live? If you already have a folder from an earlier session, point me there — otherwise I'll set one up at `~/college-apps/`."* Ask for their full name in the same breath.
2. **Check existence safely:**
   - Only perform a bare existence test (`[ -e <path> ]`). Never run `find`, `ls`, or recursive searches outside the session folder. The plugin directory at `${CLAUDE_PLUGIN_ROOT}` is always safe to read.
3. **Initialize rules & student scaffold:**
   - Copy `${CLAUDE_PLUGIN_ROOT}/templates/workspace-CLAUDE.md` to `CLAUDE.md` (rules before facts).
   - Create `students/<slug>/` from `${CLAUDE_PLUGIN_ROOT}/templates/student/` (`<slug>` is first name and last initial, e.g. `jordan-k`, or `jordan` if surname is unknown; rename when provided).
4. **Provide document drop path:**
   - Tell the student `<path>/students/<slug>/documents/` and ask for their transcript and packet in the same reply.

**Exits** when `CLAUDE.md` and the student folder exist and paths are communicated. Re-entry never asks again once `CLAUDE.md` is present.

### Documents (a sequence)

**Runs when** a document is placed in `documents/` or pasted into chat.

1. Read the document completely.
2. Copy facts into `profile.md` under matching template sections and tag every line (`[packet]`, `[transcript]`, `[worksheet]`). If a GPA does not say "unweighted", leave `- **GPA (unweighted):** TODO: packet lists 3.9 without stating whether weighted or unweighted [packet]` (never put the number on the unweighted line as its value).
3. Copy reflection answers **word for word** in quotes with original grammar.
4. Mark every missing detail or unstated column (like hours/weeks) as a standalone `TODO:` line; never infer or guess "one-time" or "not recurring".
5. Put concrete numbers on activities (hours/week, weeks/year, years); ask rather than estimate.

**Exits** when `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py students/<slug>` passes and open `TODO:` items are named in the reply.

### The interview (the loop)

**Runs when** interacting with the student in conversation.

- **Standard:** The gate for the next stage (the essay gate by default) and open `TODO:` items in `profile.md`.
- **Budget:** As many turns as needed. **At most two questions per turn.** Keep replies short and strictly student-facing: state what was recorded, the gate line, the questions, and one next step. Never output internal planning thoughts or process narration in chat.
- **Each round:**
  1. *Ask gate items first:* For the essay gate, focus on documents, target major, and concrete activity details. For the list gate, focus on state of residence (for in-state tuition), unweighted GPA, test plans, and budget.
  2. *Write rows immediately:* Record rows in the student's exact words the moment they arise. Tag and date every row.
  3. *Log conversation:* Append student statements to `conversations.md` verbatim in quotes with date headers.
  4. *Run verification script:* Execute `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py students/<slug>` and copy its gate line into the reply as printed (`material N/3 — missing: ...`).
  5. *Follow the alive thread:* Pursue what the student showed genuine interest in, rather than reading a static list.
- **Seven moment rules:**
  1. **Your paraphrase is not their criterion:** Write their exact words while on screen; never substitute interpretive summaries (e.g. write "I don't want to be the least prepared person in the room", not "prefers supportive environment"). When putting text in quotation marks or logging a student reason, copy their exact words without any alteration.
  2. **A hedged answer is still an answer:** Record "biology maybe, idk" as the major with confidence noted; `TODO:` is reserved only for unasked/unanswered questions.
  3. **A guess is not a number:** Mark student budget estimates as unverified (`set by: nobody yet`) and assign family budget discussion as homework. Require verification for GPA without "unweighted".
  4. **A correction retires the old row:** Move replaced criteria to `## Retired criteria` with date, source tag, and student reason; never overwrite in place.
  5. **Never name a college:** Intake does not evaluate schools. Record student-mentioned colleges as Preferences rows (`named: <college> — "<reason>"`) with their exact verbatim reason, for `college-list`.
  6. **Ask about context once, gently:** For grade dips, jobs, or caregiving, ask once if they want it disclosed and accept "rather not" without pressing.
  7. **Never compare against other students:** Avoid "most kids" or "thousands write that"; focus strictly on facts.
- **Exits:**
  - *Gate full:* Reflect back the student's profile in 4–5 sentences in their language, ask what was misunderstood, record corrections, and hand off to the next stage (`essay-coach` today; `college-list` when active).
  - *Ceiling:* If two rounds pass with the gate score unchanged, name the blocking item (typically the family budget conversation), assign it as homework with the Net Price Calculator, and stop asking.

### Update (a sequence)

**Runs when** student information changes (new test scores, updated activity, changed major) or `conversations.md` has newer entries than `profile.md`.

1. Add the new information, tagged and dated.
2. Retire replaced rows with reasons.
3. Run `check_record.py` to verify consistency.

**Exits** with the change summarized and whether it updates the gate or the college list.

## State

Owns `profile.md`, `criteria.md`, `conversations.md` (append-only) — schemas in `${CLAUDE_PLUGIN_ROOT}/schemas/`. Reads other workspace files via `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md § Every file`.

**Passes to:**
- Essay gate met → `essay-coach`
- List gate met → `college-list`
- Named college → criteria row for `college-list`

**Session close:**
Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py students/<slug>`. Fix any script FAILs before replying; explain why any WARN is acceptable. No checker-subagent runs because words belong to the student. State what the folder now holds, the script's gate line, open `TODO:` items, and the single next step.

## Guardrails

- Nothing enters the files that the student, parent, counselor, or a verified document did not state.
- Every content line carries its attributed source tag.

*Every reply ends with ONE next step — a sentence with its why, not a menu.*
