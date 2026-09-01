# Evaluating a college list

A college list is evaluated against five dimensions. Every round of list building or rebalancing checks all five.

---

## The rubric

| Dimension | Target | Failure looks like |
|---|---|---|
| **Balance** | 8–12 schools total: 2–3 Safeties, 3–5 Targets, 2–4 Reaches | All reaches ("lottery ticket list"); zero safeties; >15 schools without focus. |
| **Affordability** | Every Safety is provably within the family's annual net price budget ceiling without unearned scholarships | Calling a $50k school a "safety" when the family ceiling is $25k because "they might get merit aid." |
| **Hard Filter Compliance** | Zero schools violate any Hard Filter (`[H]`) or Deal-breaker (`[D]`) in `criteria.md` | Putting a cold-climate school on a list where D1 is "no cold weather," or an out-of-state school when budget requires in-state. |
| **Plain-English Matches** | Every school entry explicitly describes what criteria it satisfies and misses in human words | Shorthand like `Meets H1, H2; Misses P3` without explaining what H1 or P3 actually are. |
| **Derivation Transparency** | The list states how it was derived and proactively offers to walk through the logic | Delivering a list of names with no explanation of how filters and tiers were computed. |

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
