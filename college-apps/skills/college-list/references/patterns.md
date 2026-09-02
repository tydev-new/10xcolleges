# Patterns & Techniques for Building College Lists

Techniques for sourcing schools, classifying tiers honestly, matching criteria in plain English, and explaining derivations.

---

## 1. Sourcing Schools (Scorecard & Common Data Set)

- **Use the Scorecard script for verified data:**
  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" search "<State/Name>"
  python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" get --unitid <id1,id2,...>
  ```
  Batch queries together; responses are cached for 30 days.
- **Section C7 of the Common Data Set:** When available in `research/<college>.md`, check how heavily the institution weighs GPA, rigor, test scores, and demonstrated interest.
- **Never guess numbers:** If admit rates or costs are unverified, mark them `Not found — needs checking` instead of citing figures from memory.

---

## 2. Honest Tiering

Tier by *this student's* academic profile against *that school's* admitted class statistics, adjusted for major and residency:

- **Safety (2–3 schools):**
  - Academic numbers (unweighted GPA, SAT/ACT) sit comfortably in the school's top 25% (above the 75th percentile).
  - High probability of admission for this specific major.
  - **Affordability:** Net price is confirmed within the family's annual budget ceiling without relying on unearned merit scholarships. If it costs $40k against a $25k budget, it is **never** a safety.
  - **"Love Your Safeties" Rule:** Must actively match at least 1–2 key student preferences (`[P]`)—such as an honors college, maker space, or campus community—so the student would genuinely be excited to attend if all reaches say no.
- **Target (3–5 schools):**
  - Academic numbers land squarely within the middle 50% (25th–75th percentile).
  - Realistic, competitive chance of admission for the student's major. Forms the solid core of the list.
- **Reach (2–4 schools):**
  - Academic numbers sit below the 25th percentile, **OR**
  - The school admits under 15–20% of applicants overall (all sub-15% schools are lottery reaches for everyone), **OR**
  - **Major-Specific Reach:** The specific department or college (e.g. Engineering, CS, Nursing, Business) has an admit rate under 20% or uses a competitive pre-major weed-out pool, even if the general university admit rate is 50%+.

### A. The Out-of-State Public Flagship Trap
Warn families early about out-of-state public flagships (e.g., Colorado, Wisconsin, Penn State, Washington). They almost never meet out-of-state need and cost $55k–$70k/year. Unless an automatic out-of-state tuition waiver or massive merit grid applies, they break middle-class budgets and should not displace affordable targets.

### B. Decision Plan Timing & Aid Alignment
- Prioritize non-binding **Early Action (EA)** for schools offering automatic merit grids, honors college consideration, or priority scholarship deadlines (typically Nov 1 or Dec 1).
- **Golden Rule on Early Decision (ED):** Never recommend binding Early Decision if the family needs to compare financial aid packages across colleges before committing.

### C. Synchronizing with Research Dossiers
When a research dossier exists in `research/<college>.md`, the entry in `colleges.md` must pull its numbers, net price estimates, and watch-outs directly from the dossier rather than generic estimates.

---

## 3. Plain-English Criteria Matches

Do not use raw codes like `Meets H1, H2; Misses P3`. Always write the actual human criteria:

### Pattern:
```markdown
- **Why it's here:** Meets: under $25k net price ($18k) [H1], ABET-accredited mechanical engineering [H2], within 90 minutes of home [H3]. Strong on: honors college keeps intro classes small [P1]. Misses: prefers small campus; MSU has 50,000+ students [P4].
```

- State the concrete requirement first.
- Note any strong alignments with student hobbies or learning preferences.
- Be honest about misses: every school has trade-offs; naming them builds trust with the student.

---

## 4. When Hard Filters are Too Tight

If hard filters leave fewer than ~5 plausible schools:
1. Stop before returning an empty or artificially narrow list.
2. Identify the bottleneck constraint (e.g. strict geographic radius, small campus size, or niche program).
3. Offer an actionable recommendation on which filter to relax:
   > *"Your current filters (under $25k, ABET mechanical engineering, within 2 hours of home, and under 5,000 students) leave only two schools. The size cap is the tightest constraint here. If we relax the campus size to include mid-sized universities with honors colleges, six strong, affordable engineering options open up. Want to try that?"*

---

## 5. Explaining Derivations in Conversation

Deliver the list with transparency into how it was constructed:

> *"Here's your initial balanced college list. I built it by first applying your non-negotiable filters (in-state tuition under $25k, ABET-accredited engineering), and then balancing schools where your 3.8 GPA sits above the 75th percentile (Safeties), within the middle 50% (Targets), and selective programs admitting under 20% (Reaches).
>
> Would you like me to walk through how any specific school was matched, or why other schools you've heard about were filtered out?"*

---

## 6. Need-Based Aid: Presenting Opportunities Without Asking for Income

Never interrogate a student or family for their tax returns or household income upfront. It is private, intrusive, and turns people off. Instead, present institutional aid policy thresholds as opportunities and ask if they are a possibility for the family:

### Conversational Pattern:
> *"Schools like Rice or Stanford have special initiatives for middle- and working-class families. For example, the Rice Investment covers 100% of tuition for families with typical assets earning under $140,000/year (and full tuition, room, and board under $75,000).
>
> If you think your family might fall under that $140k threshold, Rice could be well within your $30k budget as a reach. Is that a possibility worth keeping on the table for you to check privately with your parents?"*

### Artifact Pattern in `colleges.md`:
In `colleges.md`, record the policy threshold clearly so the student and parents can review it privately together:
```markdown
- **Watch out for:** Need-based eligibility should be verified privately with your parents using Rice's official Net Price Calculator (NPC).
```

---

## 7. In-Stride Resolution & Graceful Degradation Patterns

When `gate < 4` or open `TODO:` items exist in the student record, never halt or refuse to help. Apply the 3-beat protocol:

### A. Missing State of Residence
- **Prompt:** *"Before we pick public universities, what state do you live in? That determines whether schools like Purdue or Michigan count as in-state ($10k–$18k) or out-of-state ($30k–$60k) tuition."*
- **If Answered:** Write `- **State of residence:** <State> [student YYYY-MM-DD]` to `profile.md` and log to `conversations.md`.
- **If Skipped/Deferred:** Tag `- **State of residence:** TODO: deferred by student on YYYY-MM-DD [student YYYY-MM-DD]`. Degrade gracefully by assuming non-resident public COA and prioritizing private colleges that charge uniform tuition to all US residents. In `colleges.md`, write:
  `- **Watch out for:** In-state status unverified; estimated at non-resident rates.`

### B. Missing Budget Ceiling
- **Prompt:** *"Have your parents set an annual budget ceiling for college costs (e.g. $25k/year, $40k/year, or need-based aid)?"*
- **If Answered:** Write `| H1 | Budget | $XXk/yr · set by: parent | [student YYYY-MM-DD] | YYYY-MM-DD |` to `criteria.md`.
- **If Skipped/Deferred:** Tag `| H1 | Budget | TODO: deferred by student on YYYY-MM-DD · set by: nobody yet | [student YYYY-MM-DD] | YYYY-MM-DD |`. Degrade gracefully by tiering schools purely by academic match (GPA and test percentiles). For every school, display the estimated Net Price from Scorecard and note:
  `- **The money:** Estimated Net Price ~$XX,XXX [Scorecard]. Affordability unverified — family budget ceiling not yet set. Review Net Price Calculator with parents before applying.`

### C. Missing Major ("Undecided")
- **Prompt:** *"What major or academic field are you thinking about? (If you're not sure, 'undecided' is completely fine — just tell me what subjects you enjoy)."*
- **If Answered:** Record major or record `"undecided" [student YYYY-MM-DD]` in `profile.md § Goals and direction`.
- **If Undecided:** Degrade gracefully by evaluating schools on general university admission rates, but add an explicit watch-out for restricted STEM/business programs:
  `- **Watch out for:** Applying undecided; changing into Engineering, CS, Nursing, or Business later often requires a separate, highly competitive internal transfer gate.`

---

## 8. The Sub-15% "Automatic Reach" Rule (Regardless of Stats)

A student with a 4.0 unweighted GPA and 1580 SAT will have stats at or above the 75th percentile of Ivy League, Stanford, Duke, and Northwestern. Students (and novice counselors) often mistakenly tier these as "Targets".

### The Master Counselor Law:
**Any institution or program with an acceptance rate below 15% is an Automatic Reach for 100% of human applicants.**
- *Why:* At $< 15\%$ admit rates, schools reject thousands of 4.0/1600 applicants every year. Institutional institutional priorities (recruited athletes, legacy, development, geographic diversity, underrepresented talents) occupy 30%–50% of the admitted class, making general unhooked admission statistical lotteries.
- *Tiering Rule:* Never label a sub-15% school as a Target or Safety. `check_list.py` strictly enforces this.

---

## 9. The Per-College Test-Optional Submission Strategy

Never make a blanket global decision to submit or withhold SAT/ACT scores. Counselors evaluate score submission **college by college** against the institution's enrolled middle 50% (from CDS Section C9):

1. **Submit Confidently:** If the student's score is at or above the college's **enrolled 50th percentile**.
2. **Submit Strategically:** If the score is between the **25th and 50th percentile AND** the student brings a geographic hook, first-generation status, or intended major in a non-STEM field where the score is competitive.
3. **Withhold (Apply Test-Optional):** If the score is below the college's **enrolled 25th percentile**. Submitting a 1380 to an institution where the 25th percentile is 1490 converts a strong GPA into a questionable profile. Applying test-optional allows admissions officers to focus entirely on course rigor and grades.

---

## 10. Early Decision (ED) Leverage & The Financial Guardrail

Early Decision (ED I / ED II) often provides a 1.5x–2.5x statistical boost in acceptance rates at selective private universities (e.g. Northwestern, WashU, Duke, Emory, Tulane, Boston College).

### The Non-Negotiable Financial Prerequisite:
**Never allow a student to submit a binding Early Decision agreement without written confirmation that parents have run the college's Net Price Calculator (NPC) and confirmed the estimated cost is affordable.**
- *Why:* An ED acceptance is a binding contract. If admitted, the student must withdraw all other applications immediately. The student cannot compare financial aid offers from other schools in April.
- *Chat & Dossier Standard:* When a student proposes an ED school, always ask:
  > *"Because Early Decision is legally binding, have you and your parents run [College]'s official Net Price Calculator? We need to verify that their estimated net price is within your family's budget before locking in an ED commitment."*
