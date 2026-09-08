# Patterns & Sourcing Techniques for College Research

Operational blueprints for gathering verified data, evaluating admissions policies, unearthing essay hooks, and exposing friction points.

---

## 1. Sourcing Hierarchy & Investigation Sequence

Follow this sequence to build a research dossier:

```
Step 1: Federal & Institutional Numbers  (Scorecard batch + CDS Section C1, C7, C9)
Step 2: Departmental Audit              (Direct-admit vs pre-major, ABET status, labs)
Step 3: Cost & Financial Aid Engine      (Non-resident waiver matrices, need-met % in CDS §H)
Step 4: Friction & Culture Probe         (CDS B22 retention + Student forums labeled 'Impression')
```

### A. College Scorecard (`scorecard.py`)
- **Use for:** Federal net price by family income band, median student debt at graduation, median post-grad earnings, completion rate, and non-resident public COA.
- **Out-of-state public Cost of Attendance:** `scorecard.py` calculates and reports the non-resident Cost of Attendance (e.g. *Out-of-state students at this public pay roughly $43,393 [Scorecard]*). Use this verified federal figure as the canonical non-resident COA benchmark if university web pages return 404 or provide unverified room/board estimates. Against a $30k budget, ~$41k–$44k (~$43.4k) yields the true ~$11k–$14k gap.
- **Batching rule:** To respect API limits, resolve UNITIDs first and batch them:
  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" search "Purdue"
  python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" get --unitid 243780,147767
  ```
- **Fallback:** If API quota is exhausted, note it honestly and proceed immediately to the school's Common Data Set and official aid pages.

### B. Common Data Set (CDS)
Search `"common data set" site:<college>.edu` or check the university's Institutional Research page:
- **Section C1:** Exact applicant, admitted, and enrolled counts (fresh admit rate).
- **Section C7 (The Admissions Policy Matrix):** Tells you in the school's own words what factors move the needle:
  - *Demonstrated Interest:* If marked "Considered" or "Important," tell the student to open emails, attend virtual webinars, and schedule campus visits to prevent yield-protection waitlisting.
  - *Rigor, GPA, Essays, Recommendations, Talent:* Check which non-cognitive factors carry "Very Important" weight.
  - *Decision Plans (ED vs. EA vs. RD):* Note whether Early Decision provides a statistical advantage. **Golden Rule:** Never recommend Early Decision if the family needs to compare financial aid offers from multiple institutions.
- **Section C9 (Testing & Score Inflation Audit):**
  - Read SAT and ACT middle 50% percentiles (25th–75th).
  - *Audit Score Submission Rate:* Note what percentage of enrolled freshmen actually submitted test scores. If only 35% submitted, the published range is artificially inflated by high-scoring self-selectors.
  - *Testing Strategy:* Recommend submitting scores if at or above the 50th percentile (or major average); recommend test-optional if below the 25th percentile, unless scores are required by policy.
- **Section B22:** First-to-second year retention rate (the satisfaction canary).
- **Section H2:** Financial aid numbers — average percentage of need met and whether need-based loans are packaged.

### C. Academic Department Pages
Search `<college>.edu/<department>` (e.g. `purdue.edu/me`):
- Verify **exact degree title** and accreditation (e.g. ABET for engineering).
- **Major-Specific Selectivity:** Check whether the department admits directly or places students in a "First-Year Engineering" or "Pre-Major" weed-out pool. If departmental admit rates are 15%–20% while the general university admits 50%, the school must be tiered as a major-specific Reach.
- **Physical Undergraduate Facilities & Maker Spaces (Essay Hooks):** Must identify at least 2 named, physical undergraduate facilities or maker spaces where undergraduates build projects (e.g. at Purdue: Bechtel Innovation Design Center, Herrick Labs; at Rice: Oshman Engineering Design Kitchen [OEDK]; at Michigan: Wilson Student Team Project Center; at MIT: MakerLodge). Do not cite lecture formats or general course numbers as substitutes for physical maker facilities.

### D. Financial Aid & Budget Comparison (The Out-of-State Public Trap)
- **Beware the Aggregator Net Price Trap:** Never cite third-party aggregators (CollegeSimply, Niche, CollegeXpress) for financial aid or net price. They blend in-state tuition and state grants into a misleading "average net price" and mislabel it as out-of-state.
- **Public Universities & Non-Resident Need:** Public institutions (e.g. Purdue, Wisconsin, Penn State, Colorado) offer **zero to very limited institutional need-based grant aid to non-residents**. For out-of-state students, always assume the **full non-resident Cost of Attendance (COA)** from the official college bursar/financial aid page, unless an official automatic tuition waiver or guaranteed merit matrix applies.
- **Use Standard Undergraduate Living Costs:** Sourced room and board must be the standard on-campus freshman residence rate (~$10,000–$11,500/year at Big Ten/public flagships). Never use off-campus, regional, or graduate housing proxies that artificially inflate COA to $48k–$50k.
- **Calculate the True Cost Gap:** Compare the non-resident COA against the family's annual budget ceiling (from `criteria.md`). For example, Purdue's out-of-state COA is ~$41,000–$44,000/year (tuition ~$29k + housing/food ~$10k + books/fees); against a $30,000 budget, the reality is an **$11,000–$14,000 annual gap** that only large competitive merit scholarships can close. Never sugarcoat this gap or assume financial aid will cut it in half.
- Look up out-of-state scholarship matrices (guaranteed GPA/SAT tables) and state-mandated tuition waivers (e.g. Texas competitive \$1,000 waiver, Louisiana out-of-state fee exemption).

---

## 2. Four-Layer Friction Sourcing Pattern

Never write a dossier with zero drawbacks. Every real college has friction. Uncover it across four layers:

1. **Statistical Canary (CDS §B22):** Check freshman retention. If retention is below 85%, investigate why (academic weed-out culture, financial distress, or poor advising).
2. **Departmental Policy Traps:** Look for secondary gates (e.g. "Admitted to Pre-Business; must maintain 3.5 college GPA in gateway courses to enter Finance").
3. **Living & Housing Realities:** Check how many years on-campus housing is guaranteed. Note if students must lease off-campus apartments as sophomores in expensive rental markets.
4. **Student Forums (Reddit `r/<college>`, Niche, Fiske):** Read what students complain about (course registration waitlists, cold weather, large 300+ person lectures, or "suitcase school" weekends).
   - **Mandatory Guardrail:** Always label student sentiment explicitly:  
     `Impression, not data: Students report that introductory chemistry and physics act as heavy weed-out courses with harsh curves.`

---

## 3. Extracting Authentic Essay Hooks

Generic essays praise the school's *"renowned faculty and beautiful campus."* Great essays connect specific student experiences to distinctive campus programs:

- **Look for named maker spaces and design centers:** (e.g. Rice's *Oshman Engineering Design Kitchen (OEDK)*, Michigan's *Wilson Student Team Project Center*).
- **Look for distinctive student-run initiatives:** (e.g. Pomona's *Green Bikes* co-op, student-managed investment funds).
- **Look for unique curriculum structures:** (e.g. Brown's *Open Curriculum*, Columbia's *Core*, Northeastern's *Co-op*).
- Record these in `## Academics & Programs` so `essay-coach` can draw upon them for "Why Us" supplements.

---

## 4. Need-Based Aid: Threshold Pattern (Income Privacy)

Never ask the student or family for their tax returns or household income upfront. When researching schools with generous endowments (e.g. Rice, Stanford, Ivy League):
- Note the published institutional promise:
  > *"The Rice Investment covers full tuition for families with typical assets earning under $140,000/year (and full tuition, room, and board under $75,000)."*
- In conversation, present this as a threshold opportunity:
  > *"If you think your family might fall under that $140k threshold, Rice could be well within your budget as a reach. Is that a possibility worth checking privately with your parents using their Net Price Calculator?"*

---

## 5. The Housing Guarantee Horizon & Upperclassman Rental Shock

Never assume a freshman room and board rate applies for four years:

### The Housing Guarantee Cliff:
- **4-Year Guarantee:** Schools like Notre Dame, Princeton, Vanderbilt, and Williams guarantee undergraduate housing for all four years, ensuring predictable living costs.
- **1-Year or 2-Year Guarantee Cliffs:** At institutions like UC Berkeley, UC Santa Cruz, NYU, Northeastern, and Colorado Boulder, housing is strictly capped after freshman or sophomore year.
- **The Financial Impact:** Students must sign 12-month private leases in competitive rental markets where rents range from $1,800 to $2,800/month per student. Adding 12 months of rent, utilities, and groceries often inflates upperclassman Cost of Attendance by **$8,000 to $15,000/year** above freshman sticker projections.
- **Dossier Rule:** In `students/<slug>/research/<college>.md § Cost & Financial Aid`, always state:
  `- **Housing guarantee:** Guaranteed for [N] years; off-campus leasing required as [sophomores/juniors].`

---

## 6. Executing Actionable Demonstrated Interest (CDS §C7)

When Common Data Set Section C7 lists **"Level of applicant's interest"** as `Important` or `Considered` (e.g., American University, Tulane, Case Western, Boston College, Syracuse, Lehigh, SMU):

### Institutional Mechanism:
These colleges use CRM platforms (such as Slate) that assign every applicant an engagement score based on digital and physical touchpoints. Failing to demonstrate interest often triggers **yield protection** (waitlisting or rejecting a high-stats applicant who appears unlikely to enroll).

### The Actionable Checklist for Students:
1. **Join the Mailing List Early:** Register on the admissions site using the exact same email address used for the Common App.
2. **Attend 1–2 Virtual Events:** Attend an official virtual admissions session and a departmental student panel. Attendance is automatically timestamped in the university's database.
3. **Open Admissions Emails and Click Links:** Admissions CRMs track email open rates and link clicks. Counselors instruct students to regularly open official emails and click through to academic department pages.
4. **Sign Up for the Optional Interview:** If the college offers optional alumni or senior interviews, always opt in; opting out signals low commitment.
5. **Campus Visits (If Feasible):** If traveling to campus, always register for the official admissions tour so attendance is recorded.

---

## 7. Cooperative Education (Co-op) Systems (Northeastern, Drexel, Cincinnati)

Certain universities center their undergraduate model around **Cooperative Education (Co-op)** rather than traditional summer internships:

### The Operating Model:
- Students alternate 4-to-6-month academic study semesters with **4-to-6-month full-time, paid professional employment** at corporate partners.
- During co-op rotations, students do not pay tuition and earn competitive market salaries (\$15,000–\$30,000 per co-op).

### Counseling Nuance (Pros vs. Cons):
- *The Massive Advantage:* Students graduate with 12 to 18 months of verified professional experience, a robust industry network, and frequently receive return offers before graduation.
- *The Hidden Cost:* It often extends degree completion to 5 years, disrupts 4-year cohort friendships (as friends cycle in and out of the city on alternating co-op schedules), and eliminates traditional summer vacations.
- *Dossier Rule:* State explicitly in `## Academics & Programs` whether co-op is mandatory, optional, or unavailable.

---

## 8. Grade Deflation vs. Inflation: The Pre-Med & Pre-Law Guardrail

For students targeting medical school (where a 3.75+ science GPA is near-mandatory) or top law schools (where a 3.8+ GPA dominates admissions), **undergraduate grading culture is a make-or-break factor**:

### A. Grade-Deflating Flagships & Universities:
- Campuses like UC Berkeley, Purdue, Johns Hopkins, Cornell, Boston University, and Georgia Tech are renowned for **rigorous downward curving** in introductory STEM weed-out sequences (General Chemistry, Organic Chemistry, Multivariable Calculus).
- Median grades in 300-person lecture halls are frequently curved to a C+ or B-. A high-performing high school student can quickly end up with a 3.1 science GPA, severely compromising medical school admission.

### B. Grade-Inflating & Flexible Campuses:
- Institutions like Brown University (no plus/minus grades, no failing grades recorded on transcript, open curriculum), Harvard, Yale, and smaller liberal arts colleges (Amherst, Williams) provide significantly higher grade medians and supportive faculty grading distributions.

### Counselor Action:
When evaluating a pre-med student considering a grade-deflating public flagship vs. a supportive private college or honors college, explicitly present the GPA trade-off:
> *"Purdue has an incredible engineering and biology program, but introductory chemistry and biology classes curve strictly to a B-/C+ median. If your ultimate goal is medical school, you must be prepared for fierce grading curves, or consider an honors college where advising and lab access protect your GPA."*

---

## 9. Score Choice vs. "All Scores Sent" Policies (Georgetown, CMU)

While most universities permit College Board's "Score Choice" (sending only your best single sitting), notable exceptions require complete disclosure:

### The "All Scores Sent" Mandate:
- **Georgetown University** and **Carnegie Mellon University** explicitly require applicants to report the **complete testing history of every SAT and ACT sitting taken**.
- *The Danger:* If a student took the SAT four or five times starting in 9th or 10th grade, every mediocre or fluctuating test score will be scrutinized by the admissions committee.
- *Counselor Action:* Identify these schools early in list building and advise students to limit official SAT/ACT test sittings to 2 or 3 attempts maximum.

---

## 10. Self-Reported Academic Record (SRAR / SSAR) Mandatory Systems

Do not assume submitting the Common App completes the academic record. Several major state universities **refuse high school transcripts sent by school counselors**:

### The SRAR Requirement:
- **Campuses:** Penn State, Rutgers, University of Pittsburgh, Virginia Tech, Texas A&M, Florida, Florida State.
- **The Process:** The student must create a separate external **SRAR (Self-Reported Academic Record)** or **SSAR (Student Self-Reported Academic Record)** account, manually transcribe all 9th–12th grade coursework, credits, and grades exactly matching the official transcript, and link the SRAR ID to their university applicant portal.
- *The Trap:* Students submit their Common App on deadline day and assume their application is complete. Without the linked SRAR, the file sits in "Incomplete" status and misses early action and merit scholarship evaluation deadlines.
- *Dossier Rule:* Note in `research/<college>.md § Academic Requirements` if SRAR/SSAR is required.

---

## 11. Official Score Send Latency Buffer (10–14 Business Days)

For universities that do **not** allow self-reported test scores on the Common App and require official electronic score transmissions directly from College Board or ACT:
- Electronic transmission and matching to the student's applicant file takes **10 to 14 business days**.
- Ordering official test scores on deadline day (e.g., November 1) results in late scores that may void Early Action consideration.
- *Counselor Rule:* Mandate that students order official score sends at least 3 weeks before the target application deadline.

---

## 12. Mastering Evaluative Admissions Interviews (The 3 Core Archetypes)

While alumni interviews at Ivy+ institutions rarely transform a clear denial into an admit, an awkward, arrogant, or ill-prepared interview can sink an applicant in committee. At institutions like Wake Forest, Georgetown, and Hamilton, evaluative interviews carry substantial evaluative weight.

Master counselors train students across **three universal interview archetypes**:

### 1. Archetype 1: "Tell Me About Yourself" (The 90-Second Trajectory Pitch)
- *The Trap:* Reciting the high school resume chronologically ("I was born in Dallas, then in 9th grade I did soccer...").
- *The Formula:* Deliver a tight, 90-second intellectual arc:  
  `Childhood Spark / Curiosity Hook -> Evolution into High School Hands-on Projects -> What I Spend a Free Sunday Doing -> Why I Am Here Today`.
- *Example:* *"I've always been fascinated by why physical machines fail. As a kid, I spent weekends taking apart broken weed-whackers with my neighbor. In high school, that curiosity turned into rebuilding our robotics team's drivetrain four times after mechanical failures. Outside of school, you'll find me repairing vintage bicycles for our community library stand. That hands-on friction is what drew me to [College]'s maker-centered engineering curriculum."*

### 2. Archetype 2: "Why This College?" (The Micro-Resource Formula)
- *The Trap:* Vague flattery about campus beauty, prestige, location, or "world-renowned faculty."
- *The Master Response:* Name **two specific academic micro-resources** (sourced directly from `research/<college>.md`) and **one campus community contribution**:
  - Micro-Resource 1: A specific professor's research or specialized course (e.g. *"Professor Miller's work on compliant mechanisms"*).
  - Micro-Resource 2: A distinctive facility or curriculum structure (e.g. *"The open machine shop at the Oshman Engineering Design Kitchen"*).
  - Campus Contribution: A student initiative or tradition the applicant will actively lead or join.

### 3. Archetype 3: "Do You Have Any Questions for Me?" (The Reverse Culture Interview)
- *The Trap:* Asking logistical questions easily found on Google ("What is your student-to-faculty ratio?", "Do you have a pre-med track?").
- *The Master Response:* Ask reflective, culture-probing questions that honor the interviewer's lived alumni experience:
  - *"When you look back on your four years at [College], what is one intellectual tradition or experience that shaped how you think today?"*
  - *"How did the collaborative culture between students play out during stressful midterm or project periods?"*
  - *"What kind of student genuinely thrives at [College], and who struggles?"*
