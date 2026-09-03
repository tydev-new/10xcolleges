---
name: app-tracker
description: Build and maintain the application tracker spreadsheet — deadlines, per-college task lists worked backwards from each due date, recommender status, and key dates. Use when a student asks what's due, whether they're behind, what to do next, or after the college list, deadlines, or application statuses change.
---

# Application Tracker

Build and maintain the operational command center for a student's college application campaign. Read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md`.

The tracker is `students/<slug>/out/tracker.xlsx`, compiled deterministically from `meta.json` and `${CLAUDE_PLUGIN_ROOT}/config/calendar.json`. It is strictly a **Derived** artifact — never hand-edit the `.xlsx` file directly; all updates are made to `meta.json` and regenerated.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/make_tracker.py" students/<slug>
```

- **Standards & Rubrics:** Read `${CLAUDE_PLUGIN_ROOT}/skills/app-tracker/references/eval.md`.
- **Master Counseling Protocols:** Read `${CLAUDE_PLUGIN_ROOT}/skills/app-tracker/references/patterns.md`.
- **Workbook Schema:** Read `${CLAUDE_PLUGIN_ROOT}/schemas/tracker.md`.

---

## Sequences & Triggers

### 1. Trigger: College List or Deadline Change
Whenever `colleges.md` changes or a deadline is updated:
1. Mirror updates to `meta.json` under `colleges[]` with strict ISO dates (`YYYY-MM-DD`).
2. Audit for earlier **Scholarship Priority Deadlines** (Pattern § 1) and note them in the college record.
3. Regenerate the workbook:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/make_tracker.py" students/<slug>
   ```

### 2. Trigger: Status Progress ("What's due next?", "I submitted!")
1. If an application is submitted, update `"status": "submitted"` in `meta.json`.
2. If a recommender agrees, sends, or submits, update `meta.json.recommenders`.
3. If a student asks what to do, run `make_tracker.py` and output the **Inline Executive Dashboard** in chat.
4. Schedule the **72-Hour Applicant Portal Audit** (Pattern § 3) post-submission.

---

## Operations & Execution Protocols

### 1. Multi-Tier Deadline Hierarchy
Novices look only at the final application deadline. Master counselors track four distinct tiers:
- **Tier 1: Internal High School Cutoff:** (Often 3–4 weeks prior) for requesting official transcripts.
- **Tier 2: Institutional Scholarship Cutoff:** (e.g., USC Dec 1, Indiana Univ Nov 1). Missing this forfeits merit aid.
- **Tier 3: Admissions Application Deadline:** Official Common App submission cutoff.
- **Tier 4: Financial Aid Priority Date:** FAFSA / CSS Profile institutional deadlines.

### 2. The 7-Day "Server Crash" Buffer Rule
- **Rule:** Target submission date = **Official Deadline − 7 Days**.
- Common App servers experience severe slowdowns and payment gateway failures on deadline nights. Time-zone misunderstandings (EST vs. local time) cause fatal rejections. The student finishes one week early; the final 7 days are purely for portal transmission, payment clearance, and peace of mind.

### 3. Backwards Scheduling & Compression Math
- Backwards planning steps (recommenders at 9 weeks, supplements drafted at 6, revised at 4, counselor letter at 3, proofreading at 2, submit) live in `config/calendar.json`.
- **Compression:** If runway < 10 weeks, `make_tracker.py` compresses tasks proportionally into remaining days.
- **Extreme Crunch (< 3 weeks):** Execute cognitive triage (Pattern § 5): pick 1 Safety + 1 Target for EA; move remaining schools to Regular Decision.

### 4. The 72-Hour Applicant Portal Audit
- Within 24–72 hours of submission, the student receives email credentials for the college's applicant portal.
- The student must log in and audit green checkmarks for: Transcripts, Counselor SSR, Teacher Letters, Test Scores (or test-optional flag), and SRAR account linkage.

### 5. Senior Spring Rescission Defense
- **Rule 1:** Never drop a second-semester academic course without prior written approval from every admitted university. Dropping an AP class for study hall is the #1 cause of July rescissions.
- **Rule 2 (C/D Mitigation Protocol):** Proactive disclosure in April/May for severe grade dips converts a unilateral rescission into an academic support plan.

---

## Talking About the Tracker

Don't narrate the spreadsheet rows. Present an actionable, high-clarity summary:
- **Lead with what's next, not what exists.** "What should I do today" is the only question the student has.
- **One priority at a time.** A student handed twelve tasks does none of them.
- **Never catastrophize a late start.** Compress the plan, name the immediate move, and get moving.

---

## State

Owns `students/<slug>/out/tracker.xlsx` — schema in `${CLAUDE_PLUGIN_ROOT}/schemas/tracker.md`. Generated from the student metadata index and `${CLAUDE_PLUGIN_ROOT}/config/calendar.json`.

Appends to `conversations.md`. Maintains `meta.json` (`colleges[]`, `recommenders[]`, `key_dates[]`) — schema in `${CLAUDE_PLUGIN_ROOT}/schemas/meta.md`.

---

## Non-Negotiable Guardrails

1. **Never Hand-Edit `tracker.xlsx`:** The spreadsheet is strictly a Derived artifact. Always edit `meta.json` and regenerate via `make_tracker.py`.
2. **Strict ISO Date Invariant:** All deadlines must be formatted as `YYYY-MM-DD`. Malformed dates (e.g. `11/01/2026`) abort the build immediately to prevent missing tasks.
3. **The 7-Day Crash Buffer:** Working submission targets must be scheduled 7 days prior to official deadlines.
4. **The Scholarship Priority Trap:** Never record an RD deadline without verifying whether earlier institutional merit cutoffs exist.
5. **The Senior Course Retention Rule:** Never endorse dropping an academic course in senior spring without written university consent.

---

## Session Close

Before replying to the student on EVERY turn:
1. **Regenerate Tracker:** Execute:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/make_tracker.py" students/<slug>
   ```
2. **Verify Output on Disk:** Confirm `students/<slug>/out/tracker.xlsx` was generated cleanly.
3. **Render Inline Executive Dashboard:** Output a clean Markdown table in chat summarizing:
   - Target vs. official deadlines and live days left.
   - Immediate 14-day urgent action items.
   - Recommender and applicant portal audit status.
   - Clickable link to the full `.xlsx` workbook.
