# The build rules — domain-neutral core

*(Extracted verbatim from `../PRINCIPLES.md` Part 2. That file is the
source; `kit/tests/test_kit.py` fails if this copy drifts. A host writes
its own Part 1 — the promises to its user — and adopts this Part 2 as
is.)*

## Part 2 — How we build it

*(rules for ourselves — how the promises stay true as the system grows)*

**9. Believe the disk, not the narration.** Everything produced is a file (or a database row) that can be checked. The system trusts what's actually there — never what any component, including the model, *says* it did. Learned the hard way on 2026-07-17, when work the model described did not match what had actually been saved; now it's the architecture.

**10. One of everything.** One board, one plan, one set of files, one conversation, one place per fact. Duplicate representations will eventually disagree — so they aren't built, and when found, they're deleted.

**11. Every rule is derivable or earned.** A behavior must either follow from Part 1, or carry the receipt of the real incident that earned it. Rules with neither get deleted. When we simplify by deleting a rule the model should be able to derive, we test that it really does handle the cases the deleted rule spelled out — and running our own job searches on the product is that test.

**12. Evidence decides.** Usage data, incident history, and our own live use of the product outrank taste. Two independent groups of users saying the same thing beat any argument; a caveat about the data travels with every conclusion drawn from it.

**13. Plain language is the complexity test — for designs AND for skill prose.** If a design can't be explained in this document's register, it's too complex to ship. And the skills themselves — the instructions the agent derives behavior from — follow the same rule: no metaphors that need decoding, no invented shorthand; a technical term is allowed only when it's precise and defined where it first appears. A cryptic instruction is a misbehavior waiting to happen. Deletion is the default answer to complexity.
