# Schema: colleges.md

Owner: `college-list`
Class: **Living**

Location: `students/<slug>/colleges.md`

`colleges.md` holds the balanced, tiered college list organized by school section with tier classifications, fit reasons, admissions statistics, affordability figures, and verified deadlines. It is deterministically validated by `scripts/check_list.py`.

---

## `colleges.md` — owned by college-list

### Structure & Conventions

One `## <School Name> — <Safety|Target|Reach>` section per college.

Every school section must contain these exact five bullet fields:
- `- **Why it's here:**`
- `- **The numbers:**`
- `- **The money:**`
- `- **Watch out for:**`
- `- **Deadline:**`

### Concrete Template:

```markdown
# College List — Jordan K

## University of Michigan — Target
- **Why it's here:** Elite mechanical engineering program with state-of-the-art makerspaces, matching research criteria for hands-on vehicle prototyping [P1].
- **The numbers:** Admit rate 18% (CDS 2024-25), SAT middle 50%: 1350–1530 [CDS §C9].
- **The money:** Estimated net price ~$28,000/yr [NPC 2026-08-20]; aligns with family's $30k budget ceiling [H1].
- **Watch out for:** Highly competitive out-of-state admissions pool; engineering direct-admit requires supplemental review.
- **Deadline:** 2026-11-01 (EA) [umich.edu admissions].

## Purdue University — Safety
- **Why it's here:** World-class engineering facilities, robust co-op pipeline, and strong regional recruitment [P1, P3].
- **The numbers:** Admit rate 53% overall (CDS 2024-25); SAT middle 50%: 1210–1440.
- **The money:** Total out-of-state COA ~$41,000/yr; estimated merit brings net price to ~$26,000/yr [NPC 2026-08-21].
- **Watch out for:** First-Year Engineering (FYE) transition requires GPA threshold for mechanical engineering placement.
- **Deadline:** 2026-11-01 (EA - Priority for Engineering & Merit) [purdue.edu admissions].

## Carnegie Mellon University — Reach
- **Why it's here:** Top-tier robotics and mechatronics integration with world-renowned faculty [P1].
- **The numbers:** Admit rate 11% overall; College of Engineering admit rate ~7% [CDS 2024-25].
- **The money:** Total COA ~$85,000/yr; institutional need-based grant estimated at $58,000/yr, net price ~$27,000/yr [NPC 2026-08-22].
- **Watch out for:** Rigorous, high-stress grading environment; mandatory "All Scores Sent" testing policy for CMU engineering.
- **Deadline:** 2027-01-03 (RD) [cmu.edu admissions].
```

---

### Non-Negotiable Tiering Invariants

1. **The Sub-15% Automatic Reach Rule:** Any university with an overall acceptance rate $< 15\%$ (or a major-specific admit rate $< 15\%$, such as UIUC CS or CMU Engineering) is an **Automatic Reach** for 100% of human applicants, regardless of 4.0 GPAs or 1600 SAT scores.
2. **State Legislative Quota Walls:** Flagship institutions with statutory in-state enrollment mandates (e.g. UNC Chapel Hill with 82% in-state quota; UT Austin with Top 6% auto-admit taking 75% of incoming class) are **Reaches** for all out-of-state applicants regardless of published aggregate stats.
3. **Safety Definition:** A Safety requires an admit rate $\ge 50\%$ (or transparent auto-admit index matching student stats), academic statistics where the student sits firmly in the top quartile, and a verified Net Price within the family's budget ceiling [H1].
4. **Target Definition:** A Target requires an admit rate between $20\%\text{--}50\%$, student statistics within or above the middle 50% band, and confirmed affordability.
5. **No Cryptic Codes Only:** `- **Why it's here:**` must explain the rationale in plain English. Standalone codes like `meets H1, P2` without prose explanation are rejected by `check_list.py`.
