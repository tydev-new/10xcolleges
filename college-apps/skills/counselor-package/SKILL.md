---
name: counselor-package
description: Build the interim package for a school counselor or parent to review — a self-contained HTML/PDF with the student snapshot, college list and reasoning, research, essay status, recommendation plan, and specific questions for their feedback. Also produces the filled-in school packet as .docx. Use when sharing progress with a counselor or parent, or when the student needs their completed post-secondary options packet.
---

# Counselor & Review Package

Build and maintain the formal review documents that bridge the student's independent preparation with the high school counseling office. Read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md`.

Two distinct deliverables serve two distinct audiences:

1. **`out/package.html` (+ PDF):** The comprehensive interim review dossier prepared for the school counselor or parent, opening with targeted, high-leverage institutional questions.
2. **`out/packet.docx`:** The school's official "Post-Secondary Options Packet" / Senior Questionnaire, filled in verbatim adolescent voice as raw ammunition for the counselor's Secondary School Report (SSR) letter.

```bash
# Build the review package (self-contained HTML and optional PDF)
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_package.py" students/<slug> --pdf

# Fill the school's official questionnaire (.docx)
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fill_packet.py" students/<slug>
```

- **Standards & Rubrics:** Read `${CLAUDE_PLUGIN_ROOT}/skills/counselor-package/references/eval.md`.
- **Master Counseling Protocols:** Read `${CLAUDE_PLUGIN_ROOT}/skills/counselor-package/references/patterns.md`.
- **Deliverable Schemas:** Read `${CLAUDE_PLUGIN_ROOT}/schemas/counselor.md` and `${CLAUDE_PLUGIN_ROOT}/schemas/meta.md`.

---

## Sequences & Triggers

### 1. Trigger: Preparing for the Senior Counselor Conference
Whenever the student schedules their senior conference:
1. **Curate the Asks:** Draft `students/<slug>/counselor-questions.md` following `schemas/counselor.md`. Focus strictly on the **4 high-leverage institutional questions** (Pattern § 2): Naviance scattergram trends, SSR course rigor checkmark context, teacher recommendation queues, and school-nominated scholarships.
2. **Compile the Dossier:** Run `build_package.py` to create `out/package.html` and `out/package.pdf`.
3. **Pre-Meeting Delivery (48–72 Hours Ahead):** Instruct the student to email `package.pdf` to the counselor 2–3 days in advance with a polite 3-sentence note (Pattern § 6).

### 2. Trigger: Fulfilling the School's Senior Packet Requirement
Whenever the high school counseling office requires its official questionnaire:
1. **Extract to `packet.json`:** Extract academic data, activities, honors, reflections, and parent worksheet answers from `profile.md` into `students/<slug>/packet.json` (schema in `schemas/meta.md`).
2. **Preserve Adolescent Phrasing:** Transcribe student reflection responses in verbatim adolescent voice. Never polish into consultant adult English (Pattern § 4).
3. **Verify Adversity Consent:** Confirm `challenges_include` is `"Yes"` before including sensitive family, medical, or personal challenges (Pattern § 5).
4. **Compile Word Document:** Run `fill_packet.py` to generate `out/packet.docx`. Missing fields render as grey `[to be completed]` placeholders.

### 3. Trigger: Post-Meeting Feedback Integration
Whenever the counselor provides verbal or written feedback after the conference:
1. **Log Feedback:** Append the counselor's comments into `feedback.md` with exact quotes and attribution (`[counselor YYYY-MM-DD]`).
2. **Enforce Authority Override:** Counselor feedback on local high school context (scattergram history, teacher queues, SSR rigor) outranks AI coach heuristics (Pattern § 7). Update `colleges.md` and `meta.json` immediately.
3. **Same-Day Gratitude:** Prompt the student to send a concise thank-you email confirming the agreed-upon adjustments (Pattern § 8).
4. **Regenerate Tracker:** Run `make_tracker.py` to reflect the updated college list.

---

## Operations & Execution Protocols

### 1. The 4 High-Leverage Institutional Questions
The review package opens with **"Where we'd most value your input"** (pulled from `counselor-questions.md`). Never ask questions that public search engines can answer. Focus on:
- *Local Scattergrams:* How local students with similar profiles have fared at target schools in EA vs. RD.
- *SSR Rigor Rating:* Ensuring the counselor rates coursework as "Most Demanding" and documents school AP caps.
- *Teacher Queues:* Validating the 1 STEM + 1 Hum pairing and checking teacher workload caps.
- *School Nominations:* Inquiring about school-nominated scholarships (Morehead-Cain, Jefferson, Trustee).

### 2. Secondary School Report (SSR) Division of Labor
- **Counselor SSR Letter:** Focuses on institutional context, school profile, AP limits, schedule collisions, family adversity, and character within the class cohort.
- **Teacher Letters:** Focus on daily classroom friction, lab troubleshooting, and intellectual stamina.
- Never ask the counselor to repeat classroom anecdotes from teacher brag sheets.

### 3. Draft Provenance Enforcement
`build_package.py` mechanically enforces academic integrity:
- Every `draft-NN.md` must begin with a valid provenance declaration (`STUDENT DRAFT`, `AGENT FIRST DRAFT`, or `EXAMPLE`).
- The build halts immediately on unlabeled drafts. Agent-assisted drafts render with visible transparency badges in `package.html`.

---

## State

Owns:
- `students/<slug>/counselor-questions.md` — schema in `${CLAUDE_PLUGIN_ROOT}/schemas/counselor.md`
- `students/<slug>/packet.json` — schema in `${CLAUDE_PLUGIN_ROOT}/schemas/meta.md`
- `students/<slug>/out/package.html` — schema in `${CLAUDE_PLUGIN_ROOT}/schemas/counselor.md`
- `students/<slug>/out/package.pdf` — schema in `${CLAUDE_PLUGIN_ROOT}/schemas/counselor.md`
- `students/<slug>/out/packet.docx` — schema in `${CLAUDE_PLUGIN_ROOT}/schemas/counselor.md`

Appends to `conversations.md` and `feedback.md`.

---

## Non-Negotiable Guardrails

1. **Mandatory Draft Provenance:** Never remove or bypass draft declaration headers. Presenting an agent-drafted essay without declaration damages student credibility.
2. **Safety Floor:** The college list must contain at least 2 true safeties; `build_package.py` renders a visible red alert banner if fewer than 2 exist.
3. **Adolescent Voice Integrity:** Student reflections in `packet.json` must remain authentic. Adult consultant rewrites destroy counselor credibility.
4. **Binding Adversity Consent:** If `challenges_include` is `"No"`, sensitive medical or personal adversity must never appear in `packet.docx` or `package.html`.
5. **Counselor Authority Override:** Local counselor feedback on school admissions history always overrides AI model suggestions.

---

## Session Close

Before replying to the student on EVERY turn:
1. **Compile Deliverables:** Execute:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_package.py" students/<slug>
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fill_packet.py" students/<slug>
   ```
2. **Verify Disk Output:** Confirm `out/package.html` and `out/packet.docx` exist and are current.
3. **Audit Provenance Headers:** Confirm no draft provenance errors were raised during compilation.
4. **Link Deliverables:** Provide direct, clickable markdown links to `out/package.html` and `out/packet.docx` in chat.
