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
