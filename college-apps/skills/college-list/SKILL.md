---
name: college-list
description: Build or rebalance a student's college list into safety, target, and reach tiers, with the reasoning for each school tied to their profile, budget, and preferences. Use when a student asks where they should apply, wants schools added or cut, questions whether a school is a reach, or when the list needs checking for balance and affordability.
---

# Build and balance the college list

Build or rebalance an 8–12 school college list across Safety, Target, and Reach tiers, grounded in the student's factual record and personal criteria.

| Must be true | Where |
|---|---|
| List is balanced across Safeties (2–3), Targets (3–5), and Reaches (2–4) | `students/<slug>/colleges.md` |
| Every school cites criteria matches in human-readable plain words | `students/<slug>/colleges.md` |
| Safeties are affordable within verified family budget ceiling | `students/<slug>/colleges.md` |
| Hard filters and deal-breakers are strictly respected | `students/<slug>/colleges.md` |
| Derivation explanation and walkthrough offered in chat | Conversation |
| `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_list.py students/<slug>` passes | Terminal |

---

## Prerequisites

- **Required:** `students/<slug>/profile.md` (unweighted GPA, test plans) and `students/<slug>/criteria.md` (budget ceiling, hard filters, deal-breakers). The list gate (`gate 4/4`) in `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py` must be met before building.
- **Optional:** `documents/` (counselor packet, school questionnaires).

---

## Sequences and loops

### The list gate (a sequence)

**Runs when** asked to build or rebalance a list.

1. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_record.py students/<slug>`.
2. Check `gate N/4`:
   - If `gate 4/4`: proceed to list building.
   - If `gate < 4`: halt. Never guess missing numbers or budgets. Route to `student-intake` to clarify unweighted GPA, test plans, deal-breakers, or budget.

**Exits** when `gate 4/4` is confirmed or handoff to `student-intake` is delivered.

### Build the list (a sequence)

**Runs when** `gate 4/4` is met and an initial list is requested.

1. Read `students/<slug>/criteria.md` completely.
2. Cut candidate schools immediately on any failed Hard Filter (`[H]`) or Deal-breaker (`[D]`). Never place a school that violates a hard filter on the list.
3. If filters leave fewer than 5 eligible schools: do not paper over violations by adding unaffordable schools to `colleges.md`. Stop and name the bottleneck in chat (e.g. out-of-state costs vs. budget vs. weather), show the near-misses and their cost gaps, and propose which constraint to relax (e.g. in-state options fit budget; or a budget bump opens specific schools).
4. Assign tiers based on verified academic ranges, major-specific selectivity, and net price:
   - **Safety (2–3):** GPA/test above 75th percentile for this major, net price strictly within family budget ceiling without unearned aid, AND matches at least 1–2 key student preferences ("Love Your Safeties"). A school over budget is NEVER a safety.
   - **Target (3–5):** GPA/test in middle 50% for this major AND strictly within budget.
   - **Reach (2–4):** GPA/test below 25th percentile, admit rate $< 15\text{--}20\%$, OR major-specific admit gate under 20% (e.g. engineering/CS), with plausible aid pathway.
5. Write `students/<slug>/colleges.md` following `schemas/colleges.md` with an upfront derivation summary and plain-English criteria descriptions. When `research/<college>.md` exists, pull numbers, net prices, and watch-outs directly from the dossier.
6. Synchronize `meta.json`.

**Exits** when `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_list.py students/<slug>` passes.

### Rebalance and adjust (the loop)

**Runs when** the student requests additions, cuts, or re-tiering, or when counselor feedback arrives.

- **Standard:** The 5-dimension rubric in `references/eval.md`.
- **Budget:** 3 rounds of adjustment per session.
- **Each round:**
  1. Re-read `criteria.md` top to bottom.
  2. Evaluate requested adjustments against hard filters and tier balance. If a school violates a deal-breaker or budget ceiling, explain why before rejecting it.
  3. Update `colleges.md` and sync `meta.json`.
  4. Run `check_list.py`.
  5. Ceilings: If two consecutive rounds leave the list unbalanced or under 5 schools due to tight filters, halt, identify the bottleneck constraint, and offer which filter to relax.

**Exits** when `check_list.py` passes clean and the student confirms the updated list.

---

## Moment rules

1. **Always re-read criteria.md first:** Re-read the criteria file completely before adding, removing, or re-tiering any school.
2. **Affordability is required for a safety:** A school that costs more than the family's annual net price budget is never a safety. Never call a school over budget a safety.
3. **Never place a violating school in colleges.md:** If a school fails a hard budget filter or deal-breaker, do not put it in `colleges.md`. Discuss it in chat as a near-miss.
4. **Plain words over cryptic codes:** In `Why it's here`, describe the actual criteria in human words, never raw row numbers alone (`H1, P2`).
5. **Always offer a derivation walkthrough:** In EVERY reply discussing or presenting the list, explain the derivation and explicitly ask: *"Would you like me to walk through how any of these schools were matched, or why specific schools were filtered out?"*
6. **No made-up probabilities or match percentages:** Never state individual admission chances (*"you have a 30% shot"*) or arbitrary fit scores (*"82% match"*).
7. **Never cite college numbers from memory:** Admit rates, test ranges, net prices, and campus enrollment figures must come directly from `research/` files or Scorecard queries. If a number is not in the dossier, do not guess or state a specific figure from memory.
8. **Never ask for household income upfront:** Present institutional need-based policy thresholds (e.g. "covers full tuition for typical assets under $140k income") and ask if that threshold is a possibility for them to verify privately with parents via the school's Net Price Calculator.
9. **Index tiering to the major:** If engineering or business admits through a separate, highly competitive pool, tier based on the major's selectivity, not general university stats.
10. **Never recommend Early Decision if comparing aid:** If the family must compare net prices across colleges, steer toward Early Action or Regular Decision.
11. **Pull verified numbers from research dossiers:** When `research/<college>.md` exists, the entry in `colleges.md` must pull its numbers, costs, and watch-outs directly from the dossier.

---

## Session close

Before replying to the student on EVERY turn:
1. Sync `meta.json` if schools were added or removed.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_list.py students/<slug>` as the final tool call on EVERY turn — whether files were edited or you are merely answering questions, explaining tiers, or discussing colleges. Never reply without running `check_list.py` first.
3. Every reply offers the derivation walkthrough and ends with ONE next step and its reason.
