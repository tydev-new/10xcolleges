# Evaluating a college list

A college list is evaluated against five dimensions. Every round of list building or rebalancing checks all five.

---

## The rubric

| Dimension | Target | Failure looks like |
|---|---|---|
| **Balance & Major Selectivity** | 8–12 schools: 2–3 Safeties, 3–5 Targets, 2–4 Reaches; tiers indexed to the student's *specific major* (e.g. engineering admit rate vs. general university stats). | All reaches; treating an ultra-selective engineering/CS major as a general target because university admit rate is 50%. |
| **Affordability** | Every Safety is provably within the family's annual net price budget ceiling without unearned scholarships; OOS public tuition traps flagged early. | Calling a $50k school a "safety" when the family ceiling is $25k because "they might get merit aid." |
| **Love Your Safeties** | Every Safety school actively aligns with at least 1–2 key student preferences (`[P]`) so the student would genuinely be excited to attend. | Recommending sterile safeties that meet numbers but that the student dreads attending. |
| **Hard Filter Compliance** | Zero schools violate any Hard Filter (`[H]`) or Deal-breaker (`[D]`) in `criteria.md`. | Putting a cold-climate school on a list where D1 is "no cold weather," or an out-of-state school when budget requires in-state. |
| **Plain-English Matches** | Every school entry explicitly describes what criteria it satisfies and misses in human words. | Shorthand like `Meets H1, H2; Misses P3` without explaining what H1 or P3 actually are. |
| **Decision Plan Alignment** | Deadlines prioritize Early Action for scholarship and honors consideration; never recommends Early Decision if the family needs to compare aid offers. | Recommending binding Early Decision to a student who needs to compare competing aid packages. |
| **Derivation Transparency** | The list states how it was derived and proactively offers to walk through the logic. | Delivering a list of names with no explanation of how filters and tiers were computed. |

---

## Who checks what

1. **`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_list.py students/<slug>` (Deterministic Script):**
   - Verifies `colleges.md` structure, headers, and standard fields (`Why it's here`, `The numbers`, `The money`, `Watch out for`, `Deadline`).
   - Verifies that "Why it's here" uses descriptive human words rather than cryptic codes alone.
   - Computes tier counts and warns if Safeties or Targets are zero, or if total count is outside 6–15.
   - Checks synchronization with `meta.json`.

2. **The Coach (Semantic Verification):**
   - Re-reads `criteria.md` in full before touching `colleges.md`.
   - Confirms that every Safety is affordable based on net price data, not sticker price or speculative aid.
   - Explains the derivation of the list in conversation and offers to walk through the choices.
