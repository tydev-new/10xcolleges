# Evaluation Rubric: Counselor & Review Package (`counselor-package`)

This document defines the qualitative criteria, compliance standards, and evaluation protocols for compiling the school counselor review dossier (`package.html` / `package.pdf`) and the official post-secondary options packet (`packet.docx`).

---

## 5-Dimension Qualitative Rubric

### 1. Actionable Counselor Inquiries (The 4 Asks)
- **Excellence:** The package opens immediately with `counselor-questions.md` ("Where we would most value your input") focused strictly on institutional knowledge only this counselor possesses:
  1. *Local School Scattergrams:* Historical admit trends from this high school for students with similar GPAs/test scores.
  2. *SSR Course Rigor Rating:* Ensuring the counselor has the context to rate senior coursework as "Most Demanding" and explain AP course caps.
  3. *Faculty Recommender Capacity & Steering:* Validating teacher pairings (1 STEM + 1 Hum) and checking for full queues.
  4. *School-Nominated Scholarships:* Inquiring about nomination opportunities for selective awards (e.g. Morehead-Cain, Jefferson, Trustee).
- **Failure:** Asking generic questions found on public `.edu` admissions pages (e.g. *"What is Purdue's deadline?"*), wasting the counselor's limited attention on trivia.

### 2. Secondary School Report (SSR) Context & Course Rigor Advocacy
- **Excellence:** Directly arms the counselor with the institutional facts needed to champion the student in the official Secondary School Report (SSR):
  - Documenting district AP course caps (e.g., maximum 3 APs permitted junior year) so a rigorous schedule isn't misread as average.
  - Explaining unavoidable scheduling collisions (e.g. AP Physics C scheduled against AP Literature).
  - Highlighting out-of-school family obligations (e.g. 15 hours/week working at family business or caring for siblings).
- **Failure:** Treating the counselor like an essay proofreader; failing to provide the structural context required for the counselor recommendation letter.

### 3. Authentic Adolescent Voice in Senior Packet (`packet.docx`)
- **Excellence:** Student reflection answers in `packet.json` and `packet.docx` are transcribed in authentic adolescent voice—retaining real phrasing, unvarnished intellectual curiosity, and self-aware vulnerability. The counselor can lift direct student quotes into the SSR letter.
- **Failure:** Sanitizing or rewriting student answers into stiff, corporate adult prose that sounds like an admissions consultant wrote it.

### 4. Confidential Adversity & Disciplinary Protocol
- **Excellence:** Strictly enforces the student's binding preference on sensitive disclosure. If `challenges_include` is `"No"`, medical, family, or personal struggles are completely omitted from `packet.docx` and `package.html`. If `"Yes"`, the challenge is framed through the lens of maturity, growth, and academic recovery.
- **Failure:** Disclosing private family or health information against the student's explicit choice; sharing unvetted disciplinary details without prior counsel.

### 5. Local Authority Override & Feedback Integration
- **Excellence:** Recognizes that **local counselor feedback outranks AI coach heuristics**. Counselor comments are logged into `feedback.md` with date and attribution (`[counselor YYYY-MM-DD]`). If the counselor warns that a school rarely admits students from their high school in Early Action, the list is immediately re-tiered and the tracker regenerated.
- **Failure:** Arguing with the counselor's local institutional memory; failing to update `colleges.md` and `meta.json` following the counselor conference.

---

## Division of Labor: Who Checks What

| Requirement | Python Scripts (`build_package.py` / `fill_packet.py`) | LLM Agent |
|---|---|---|
| **Draft Provenance Declaration** | **Enforces:** `build_package.py` halts with `SystemExit` if any `draft-NN.md` lacks a valid header declaration (`STUDENT DRAFT`, `AGENT FIRST DRAFT`). | Inserts truthful provenance declaration headers at the top of every draft. |
| **Safety List Warning** | **Enforces:** Injects a visible red alert banner if fewer than 2 true safeties appear on the college list. | Curates a genuinely balanced list with $\ge 2$ safeties before generating the package. |
| **Adolescent Reflection Text** | **Enforces:** Maps `packet.json` fields into Word table cells; renders `[to be completed]` for blanks. | **Evaluates:** Preserves verbatim student phrasing; forbids consultant buzzwords or adult rewriting. |
| **Sensitive Challenge Privacy** | **Enforces:** Checks `challenges_include == "Yes"`; if not, suppresses the challenge block. | **Evaluates:** Confirms the student's explicit disclosure consent before populating `packet.json`. |
| **Offline HTML Packaging** | **Enforces:** Inlines all styles, SVGs, and print stylesheets; runs headless Chrome for PDF. | Ensures all research dossiers and profile sections are populated prior to build. |
| **High-Leverage Asks Curation** | Generates default prompts if `counselor-questions.md` is absent. | **Evaluates:** Writes student-specific questions in `counselor-questions.md` addressing local high school nuances. |
| **Counselor Feedback Override** | Does not modify files post-meeting. | **Evaluates:** Transcribes counselor notes into `feedback.md` and updates `colleges.md` accordingly. |
