# Schema: counselor-package Deliverables

Owner: `counselor-package`
Class: **Living** (`counselor-questions.md`), **Derived** (`package.html`, `package.pdf`, `packet.docx`)

This schema defines the specifications for both student-counselor deliverables: the holistic review package (`package.html` / `package.pdf`) and the school's official questionnaire (`packet.docx`), alongside the student's targeted inquiry document (`counselor-questions.md`).

---

## `counselor-questions.md` — owned by counselor-package

Location: `students/<slug>/counselor-questions.md`  
Class: **Living**

`counselor-questions.md` contains targeted, student-specific questions prepared for the high school counselor. When present, it directly populates the opening *"Where we'd most value your input"* section of `out/package.html`.

### Concrete Template:

```markdown
# Where We Would Most Value Your Input — Jordan K

## 1. List Balance & Local High School History
- **Safeties & In-State Targets:** Does our list tiering match how applicants from our high school with similar GPAs have fared at Michigan and Purdue over the past three cycles? Are there specific regional target schools where our students consistently thrive that we have overlooked?
- **Restricted Early Action / Early Decision:** Given our intended major in Mechanical Engineering, does an Early Action submission to Michigan carry meaningful historical leverage from our school, or should we consider an ED I binding commitment?

## 2. Counselor Recommendation Letter & School Profile Context
- **Coursework & Enrollment Caps:** Our school limits students to a maximum of 3 AP courses in junior year. Will the Secondary School Report (SSR) profile explicitly note this cap so admissions readers know Jordan took the maximum rigor permitted?
- **Schedule Conflict:** In junior year, Jordan had to choose between AP Computer Science A and AP Physics C due to period scheduling collisions. Could this constraint be briefly referenced in the counselor letter?
- **Family Responsibilities & Job:** Jordan works 12 hours a week at Trader Joe's to contribute to household expenses while captaining the robotics build team. We would be grateful if this longitudinal responsibility was highlighted in your overall character assessment.

## 3. Teacher Recommender Steering
- **Recommender Pair:** We have asked Ms. Alvarez (AP Physics C, 11th) and Mr. Davis (AP English Language, 11th). Do you think this pair provides balanced coverage across quantitative rigor and classroom seminar engagement, or would you advise a different pairing?
- **Capacity Check:** Are you aware of any submission deadlines or capacity caps for either teacher that we need to account for in our timeline?

## 4. Timeline & Workload Sanity Check
- **Submission Horizon:** Jordan is planning on three November 1 Early Action deadlines (Michigan, Purdue, Illinois). Does this timeline look realistic given our high school's internal transcript request deadlines (October 1)?
```

---

## `package.html` — owned by counselor-package

Location: `students/<slug>/out/package.html`  
Class: **Derived**  
Generator: `scripts/build_package.py students/<slug>`

`package.html` is the comprehensive, single-file interim review dossier prepared for the school counselor or parent. It synthesizes the entire student file into a self-contained document.

### Structure & Sections:

1. **Header & Student Snapshot:** Name, High School, Grad Year, GPA (UW/W), SAT/ACT, Intended Major, and generation timestamp.
2. **Where We Would Most Value Your Input:** Placed at the very top of the dossier. Pulled directly from `counselor-questions.md` (or generated defaults). Focuses the counselor's attention immediately on actionable local questions.
3. **Application Roster & Tiering:** Color-coded table of colleges grouped by Tier (Reach, Target, Safety) with verified deadlines, admit rates, net price estimates, and primary selection rationale.
   - *Safety Warning:* Flags in red if fewer than 2 true safeties are present.
4. **College Research Dossiers:** In-depth breakdown for each school pulled from `research/<college>.md` (academic fit, culture, programs).
5. **Essay Inventory & Draft Provenance:** Complete text of all current essay drafts with mandatory provenance labels (`STUDENT DRAFT`, `AGENT FIRST DRAFT`, or `EXAMPLE`). Agent-assisted drafts render with visible transparency badges.
6. **Recommendation Matrix:** Faculty recommenders, subjects, asked dates, agreement status, and earliest deadlines.

### Technical Invariants:
- **Zero External Dependencies:** All styles (`CSS`), SVG icons, and layouts are inlined. It renders identically offline, inside an email attachment, or on Google Drive.
- **Print Stylesheet:** Includes dedicated `@media print` rules removing navigation chrome so standard browser printing produces a pristine multi-page document.
- **Strict Provenance Enforcement:** `build_package.py` halts immediately if any `draft-NN.md` lacks a valid provenance declaration header.

---

## `package.pdf` — owned by counselor-package

Location: `students/<slug>/out/package.pdf`  
Class: **Derived**  
Generator: `scripts/build_package.py students/<slug> --pdf`

`package.pdf` is the compiled PDF representation of `package.html`. When headless Chrome is installed (`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`), `build_package.py --pdf` runs headless print rendering to generate this file automatically. When headless Chrome is absent, users generate the identical PDF via browser `Cmd-P` / `Print to PDF`.

---

## `packet.docx` — owned by counselor-package

Location: `students/<slug>/out/packet.docx`  
Class: **Derived**  
Generator: `scripts/fill_packet.py students/<slug>`

`packet.docx` is the school's official "Post-Secondary Options Packet" / Senior Questionnaire. It formats student and parent background data into the exact Word document layout expected by high school counseling departments.

### Input Source:
Compiled from `students/<slug>/packet.json` (schema in [`schemas/meta.md`](./meta.md)) using the template at `templates/packet-template.docx`.

### Sections Formatted:
1. **Student Contact & Academics:** Name, email, phone, high school, grad year, senior year courses (Semester 1 & 2).
2. **Faculty Recommenders:** List of teachers and subjects asked.
3. **Activities & Employment:** School clubs, outside activities, hobbies, honors, and work history.
4. **Narrative Reflections:**
   - 3 core personal qualities with concrete examples.
   - Academic growth moments.
   - Intellectual curiosity experiences outside the classroom.
   - Campus and community impact.
5. **Sensitive Challenges & Disciplinary Context:** Personal or family challenges, strictly conditioned on `challenges_include: "Yes"`.
6. **Target Colleges:** Synced from `meta.json`.
7. **Parent Worksheet:** Transcribed parent responses to questions 1–7.

### Formatting Invariants:
- **Adolescent Voice Preservation:** Student reflection answers are transcribed verbatim. No consultant jargon or corporate adult polishing is permitted.
- **Explicit Incomplete Badging:** Any unpopulated field renders in styled grey text as `[to be completed]` so incomplete sections are immediately visible.
- **Binding Adversity Consent:** If `challenges_include` is `"No"`, the challenge text is strictly omitted from the generated document.
