# Schema: Core Student Requirements & Graceful Degradation Contract

Owner: Shared contract across all skills
Class: **Contract**

Location: `schemas/requirements.md`

This single document defines all required student fields, their source locations, the skills that depend on them, the exact in-stride prompt to ask the student if a field is `TODO:`, and the graceful degradation behavior if the student skips or defers.

---

## The Contract Table

| Field Name | File & Section | Required By | In-Stride Prompt (if `TODO:`) | Graceful Degradation (if skipped/deferred) | Deferral Tag |
|---|---|---|---|---|---|
| **State of Residence** | `profile.md § Basics` (`State of residence`) | `college-list`, `college-research`, `financial-aid` | *"What state do you live in? (Needed to know which public colleges count as in-state vs. out-of-state for tuition and state grants)."* | Assume out-of-state public Cost of Attendance (conservative financial posture); prioritize private colleges; flag in `colleges.md`: `Watch out for: In-state status unverified; estimated at non-resident rates.` | `- **State of residence:** TODO: deferred by student on YYYY-MM-DD [student YYYY-MM-DD]` |
| **Intended Major** | `profile.md § Goals and direction` (`Intended major`) | `college-list`, `college-research`, `essay-coach` | *"What major or field of study are you thinking about? (If you're not sure, 'undecided' is completely fine)."* | Record as `"undecided" [student YYYY-MM-DD]`; evaluate based on general university admission; explicitly flag that secondary gates for Engineering, CS, Business, or Nursing have separate, lower admit rates. | `- **Intended major:** "undecided" [student YYYY-MM-DD]` |
| **Budget Ceiling** | `criteria.md § Hard filters` (`Budget`) | `college-list`, `college-research`, `financial-aid` | *"Have your parents set an annual budget ceiling for college? (e.g. $25k/year, $40k/year, or need-based aid)?"* | Build list based on academic match; display estimated Net Price for each school; mark every tier as `Affordability unverified — family budget ceiling not yet set; review Net Price Calculator with parents.` | `\| H1 \| Budget \| TODO: deferred by student on YYYY-MM-DD · set by: nobody yet \| [student YYYY-MM-DD] \| YYYY-MM-DD \|` |
| **Unweighted GPA** | `profile.md § Basics` (`GPA (unweighted)`) | `college-list`, `college-research` | *"What is your unweighted GPA on a 4.0 scale? (If you only know your weighted GPA, that's fine to start)."* | If weighted GPA is known (e.g. 4.1), use a conservative estimated band (unweighted ~3.6–3.8); mark tiering as `Tentative — pending unweighted GPA transcript confirmation.` | `- **GPA (unweighted):** TODO: deferred by student on YYYY-MM-DD [student YYYY-MM-DD]` |
| **Testing Plan** | `profile.md § Basics` (`Testing plan`) | `college-list`, `college-research` | *"Are you planning to submit SAT/ACT scores, or applying test-optional?"* | Default to a Test-Optional strategy; exclude or flag schools requiring mandatory test scores (e.g. MIT, Purdue, Georgetown, Florida public universities). | `- **Testing plan:** test-optional (defaulted) [student YYYY-MM-DD]` |
| **Deal-Breakers** | `criteria.md § Deal-breakers` | `college-list` | *"Are there any absolute deal-breakers for you? (e.g. no freezing winters, must be within driving distance)?"* | Proceed with open geography and campus size; proactively showcase a variety of campus environments (urban vs. suburban, large flagship vs. small college). | `\| D1 \| "no preference stated yet" \| none \| [student YYYY-MM-DD] \| YYYY-MM-DD \|` |
| **Core Activity Detail** | `profile.md § School activities` / `§ Outside activities` | `essay-coach` | *"What is one activity or hobby you've spent the most time on, and what did you actually do there?"* | Pivot to the 4 behavioral brainstorming questions (Hands/Boredom, Unspoken Thought, Hollywood vs. Reality, Petty Frustration) before drafting. | Active interview in `conversations.md` |

---

## The Invariant Rules

1. **Deterministic `TODO:` Invariant:**
   In `profile.md` and `criteria.md`, any required field above that is not yet verified from documents or student conversation **MUST** be explicitly labeled with `TODO:`. Empty, unlabeled blanks (e.g. `- **State of residence:**` with nothing after it) are strictly forbidden.

2. **The 3-Beat Downstream Protocol (Prompt $\to$ Record $\to$ Degrade):**
   When any downstream skill starts:
   - **Beat 1 (Detect):** Scan `profile.md` and `criteria.md` for required fields. If any are marked `TODO:`, do NOT halt.
   - **Beat 2 (Prompt In-Stride):** Ask the student directly in chat using the canonical prompt (at most 2 questions per turn).
   - **Beat 3 (Record or Degrade):**
     - If the student provides the information: Record it immediately with `[student YYYY-MM-DD]` in `profile.md` or `criteria.md`, append to `conversations.md`, and proceed.
     - If the student skips, hedges, or defers: Record the deferral tag, apply the **Graceful Degradation** rule, disclose the limitation to the student, and proceed without blocking.

3. **Turn-Level Order of Operations (Dependency-First Protocol):**
   When a user's prompt combines new student facts or criteria changes with an analytical or research request (e.g. *"Research SUNY Stony Brook and set my residence to New York"*, or *"I got a 1450 on the SAT, rebalance my list"*):
   - **Phase 1: State Updates First (Intake):** Always commit the new student facts to `profile.md` or `criteria.md` with provenance attribution (`[student YYYY-MM-DD]`), and append the verbatim statement to `conversations.md` before doing downstream work.
   - **Phase 2: Downstream Analysis Second (Research / List / Aid / Essay):** Execute the analytical sequence using the freshly committed state. This guarantees downstream operations consume accurate facts (e.g. evaluating in-state tuition for NY, or re-tiering against 1450 SAT) and prevents stale reads.
   - **Phase 3: Final Validation Check:** Run the required validator script (`check_research.py`, `check_list.py`, `check_aid.py`, etc.) as the final tool call before responding to the student.
