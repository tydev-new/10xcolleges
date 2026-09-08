# Evaluation Rubric: Application Tracker (`app-tracker`)

This document defines the evaluation criteria for building and maintaining the college application tracker, scheduling backwards milestones, and managing campaign logistics.

---

## 5-Dimension Qualitative Rubric

### 1. Deadline Precision & Multi-Tier Rigor
- **Excellence:** Every college in `meta.json` has a verified ISO date (`YYYY-MM-DD`) anchored to official admissions source pages. The tracker explicitly accounts for the **four distinct deadline tiers**:
  1. Internal High School transcript/counselor cutoffs (often 3–4 weeks prior).
  2. Institutional scholarship & honors college priority cutoffs (e.g., USC Dec 1, Indiana Nov 1).
  3. Admissions decision plan deadlines (Nov 1 EA/ED, Jan 1–15 RD).
  4. Financial aid priority dates (FAFSA / CSS Profile).
- **Failure:** Using vague approximations ("early November"), mistyping date formats, or tracking only the Regular Decision deadline when competitive merit aid required submitting 6 weeks earlier.

### 2. Backwards Planning Horizon & Pacing
- **Excellence:** Generates a 12-week backwards operational plan from deadlines (recommenders at 9 weeks, supplements drafted at 6, revised at 4, counselor letter at 3, proofreading at 2, submission day). Respects cognitive bandwidth by sequencing the personal statement in late summer/early autumn before peak supplement load.
- **Failure:** Generating an unsequenced flat list of 40 tasks on the final deadline date, overwhelming the student and family.

### 3. The 7-Day Server Crash Buffer
- **Excellence:** Enforces an internal target submission date set to **Official Deadline − 7 Days**. Leaves the final week free for portal account generation, payment processing, transcript upload confirmations, and peace of mind.
- **Failure:** Scheduling target submission for 11:59 PM on the deadline date, exposing the student to server outages, payment gateway rejections, and time-zone errors.

### 4. Timeline Compression Realism & Cognitive Triage
- **Excellence:** When a student begins with a compressed runway (< 10 weeks), scales tasks proportionally rather than dumping a wall of impossible red overdue items. If runway is severely compressed (< 3 weeks), provides honest cognitive triage (focusing on 1 Safety + 1 Target for EA and strategically shifting remaining schools to Regular Decision).
- **Failure:** Panicking the student, generating dozens of historical overdue tasks, or pretending a student can write 14 high-quality essays in 48 hours.

### 5. Post-Submission & Rescission Auditing
- **Excellence:** Recognizes that submission is not the finish line. Schedules the **72-hour portal audit** to verify receipt of transcripts, test scores, and SRAR linkage. Explicitly includes spring senior milestones: the non-negotiable rule against unapproved course drops, the C/D proactive disclosure protocol, and the May 1 National Reply Date.
- **Failure:** Disappearing once the Common App is submitted, ignoring applicant portal incomplete notices, or failing to warn the student against dropping spring AP courses.

---

## Division of Labor: Who Checks What

| Requirement | Python Script (`make_tracker.py` / `test_dates.py`) | LLM Agent |
|---|---|---|
| **Date Syntax & ISO Format** | **Checks:** Aborts loudly on malformed strings (e.g. `11/01/2026`). | Enters clean ISO dates into `meta.json`. |
| **Aid Year Anchoring Math** | **Checks:** Computes matriculation fall anchor (tested in `test_dates.py`). | Explains aid cycle timing to family. |
| **Backwards Date Arithmetic** | **Checks:** Calculates exact due dates for all 12 backward steps. | Contextualizes current week's single priority. |
| **Proportional Compression** | **Checks:** Arithmetically scales offsets when runway < 10 weeks. | Flags tight timelines verbally in chat. |
| **Conditional Formatting & UI** | **Checks:** Injects Excel formulas, fills, and dropdown validations. | Formats Markdown Executive Dashboard in chat. |
| **Multi-Tier Deadline Trap Audit** | Cannot detect missing scholarship deadlines. | **Evaluates:** Audits `.edu` pages for earlier merit cutoffs. |
| **7-Day Crash Buffer Guidance** | Cannot alter official deadline field. | **Evaluates:** Coaches student to target submission 7 days early. |
| **72-Hour Portal Verification** | Cannot log into university applicant portals. | **Evaluates:** Prompts student to verify portal green checkmarks. |
| **Senior Spring Course Retention** | Cannot monitor high school transcripts. | **Evaluates:** Enforces written permission before any schedule drop. |
