# Evaluation Rubric: Meta-Orchestrator & Session Router (`college-app`)

This document defines the qualitative criteria, compliance standards, and evaluation protocols for managing the student lifecycle, routing across the 8 specialist skills, and maintaining campaign-wide state integrity.

---

## 5-Dimension Qualitative Rubric

### 1. Intelligent Pipeline Routing & Next-Step Proactivity
- **Excellence:** Accurately routes student prompts to the appropriate specialist skill without friction. When a student is vague or open-ended (*"I don't know what to do next"*), the orchestrator inspects the workspace, identifies the single most critical bottleneck (e.g., intake incomplete, no safeties, essays unstarted, recommenders unasked), and recommends **one clear, high-leverage next action**—never overwhelming the student with a multi-stage menu.
- **Failure:** Dumping an overwhelming 7-stage options list; routing to the wrong skill (e.g., trying to write an essay before discovering the student's profile); failing to guide an uncertain student forward.

### 2. Workspace Discovery & Session Continuity
- **Excellence:** On session launch, checks `students/`:
  - If a student workspace exists, reads `profile.md` and `meta.json` to immediately greet the student with an executive summary of current progress and pending deadlines. Never re-interviews a student whose data is already recorded.
  - If no workspace exists, prompts for the student's name and seeds `students/<slug>/` from `templates/student/`.
  - If multiple workspaces exist, asks which student to load without guessing.
- **Failure:** Re-asking previously recorded intake questions; failing to load existing workspace context; hallucinating or creating redundant directories.

### 3. Dependency-First Multi-Intent Execution
- **Excellence:** When a student provides new information alongside an analytical request (*"I scored 1420 on my SAT, rebalance my college list"*, or *"I want to add UIUC for Mechanical Engineering and see my deadlines"*):
  1. *Phase 1 (State Commit First):* Immediately commits the volunteered facts/criteria to `profile.md` or `criteria.md` with source attribution (`[student YYYY-MM-DD]`) and logs verbatim to `conversations.md`.
  2. *Phase 2 (Specialist Analysis Second):* Executes the specialist skill (`college-list`, `college-research`, `app-tracker`) using the freshly updated state.
  3. *Phase 3 (Deterministic Validation Third):* Runs the relevant validator script as the final tool call before responding.
- **Failure:** Telling the student to ask again next turn; executing downstream analysis with stale profile data; omitting validator scripts.

### 4. State Synchronization & Single Source of Truth
- **Excellence:** Maintains rigorous consistency across the application state:
  - Whenever a college is added, removed, or re-tiered, updates BOTH `colleges.md` AND `meta.json`.
  - Regenerates `out/tracker.xlsx` via `make_tracker.py` immediately upon list or deadline updates.
  - Preserves verbatim notes in `conversations.md` and attributed feedback in `feedback.md`.
- **Failure:** Updating `colleges.md` while leaving `meta.json` stale; letting `tracker.xlsx` fall out of sync with actual deadlines.

### 5. Counseling Ethics & Non-Negotiable Guardrails
- **Excellence:**
  - Enforces the **2-Safety Floor Invariant**: Insists on at least 2 schools that are both academically reliable and financially viable.
  - Treats **affordability as a core dimension of fit**, actively prompting for budget ceilings early.
  - Upholds strict **anti-fabrication standards**: Zero tolerance for invented deadlines, admit rates, or artificial essay ideas.
  - Handles high-stakes ambiguity with nuance, laying out tradeoffs while directing institutional/financial policy questions to school counselors.
- **Failure:** Endorsing an unbalanced "all reach" list; ignoring financial constraints; inventing deadlines or program requirements.

---

## Division of Labor: Who Checks What

| Requirement | Deterministic Validators (`check_*.py`, `make_tracker.py`) | Meta-Orchestrator LLM Agent |
|---|---|---|
| **Intake Completeness** | `check_record.py` checks TODO counts, source citations, and section completeness in `profile.md`. | Synthesizes profile status into a warm, encouraging executive greeting. |
| **List Balance & Safeties** | `check_list.py` verifies $\ge 2$ safeties, 8–12 total schools, and source citations in `colleges.md`. | Detects list gaps and routes to `college-list` with specific tactical advice. |
| **Tracker Synchronization** | `make_tracker.py` validates `meta.json` schema and regenerates `out/tracker.xlsx`. | Keeps `meta.json` perfectly synchronized with `colleges.md` changes. |
| **Essay Integrity & Provenance** | `check_draft.py` and `build_package.py` halt on missing provenance headers (`STUDENT DRAFT`). | Routes essay prompts to `essay-coach` and prevents ghostwriting. |
| **Recommender Logistics** | `check_rec.py` verifies brag sheet friction moments and letter request formatting. | Flags approaching recommender deadlines and monitors faculty queue capacity. |
| **Pipeline Navigation** | N/A | Evaluates whole-campaign state and recommends the single most impactful next action. |
| **Multi-Intent Ordering** | N/A | Enforces Phase 1 (State Commit) $\to$ Phase 2 (Specialist Analysis) $\to$ Phase 3 (Validator). |
