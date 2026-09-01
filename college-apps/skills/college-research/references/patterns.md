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
- **Use for:** Federal net price by family income band, median student debt at graduation, median post-grad earnings, completion rate.
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
  - *Demonstrated Interest:* If marked "Considered" or "Important," tell the student to open emails, attend virtual webinars, and schedule campus visits.
  - *Rigor, GPA, Essays, Recommendations, Talent:* Check which non-cognitive factors carry "Very Important" weight.
- **Section C9:** SAT and ACT middle 50% percentiles (25th–75th).
- **Section B22:** First-to-second year retention rate (the satisfaction canary).
- **Section H2:** Financial aid numbers — average percentage of need met and whether need-based loans are packaged.

### C. Academic Department Pages
Search `<college>.edu/<department>` (e.g. `purdue.edu/me`):
- Verify **exact degree title** and accreditation (e.g. ABET for engineering).
- Check **admission by major**: Does the student enter the major directly as a freshman, or must they compete in a "First-Year Engineering" or "Pre-Major" pool to declare later?
- Identify **specific undergraduate resources**: Named maker spaces, design project centers, undergraduate research fellowships (e.g. SURF), or cooperative education (co-op) tracks.

### D. Financial Aid Pages
- Look up out-of-state scholarship matrices (guaranteed GPA/SAT tables).
- Check for state-mandated tuition waivers (e.g. Texas competitive \$1,000 waiver, Louisiana out-of-state fee exemption).
- Note renewal requirements (e.g. maintaining a 3.0 or 3.5 college GPA).

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
