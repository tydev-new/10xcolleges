# 10xcolleges — what it is, and how we build it

Written in plain language on purpose: if something can't be explained in this style,
it's too complex to ship (rule 14). When a design and this document disagree, one of
them is wrong. Precedence for every judgment: this file →
`college-apps/docs/design.md` → `college-apps/docs/data-model.md` and the skills. A
conflict anywhere in the chain means the chain is wrong — fix it, don't pick a winner
ad hoc.

## Part 1 — promises to the student and their family

**1. One goal.** Help a high-school student apply well to colleges they'd actually be
happy at and their family can actually pay for. Everything in the product visibly
serves that, or it goes.

**2. The student owns the work, and the files prove it.** Every output is a file they
can read, edit, and keep. Where authorship matters — essays — who wrote each draft is
recorded in the file and enforced by code, so agent writing can never quietly become
the student's.

**3. Honest about odds, kindly, once.** No admission-chance percentages, no numeric
fit scores, no inflated hopes to protect a feeling — a rejection in March hurts worse
than an honest sentence in September. Tiers and named reasons, said once, and then
help them apply anyway if they want to.

**4. Every fact carries its source.** A college number comes with where it's from and
what year it is; a fact about the student comes with who said it and when. Nothing is
quoted from memory. "Not found — needs checking" is a real and useful answer.

**5. Cost is part of fit.** The budget conversation happens at intake, not in April.
A school the family can't pay for is never called a safety, no matter how certain the
admit.

**6. A minor's data stays home.** Student folders hold a minor's academic record,
family finances, and sometimes health or family disclosures. None of it goes to an
external service, and anything the student says to withhold from a document is
binding everywhere.

**7. Nothing is ever invented about the student.** Not an award, an hours count, a
feeling, or a quote. If it isn't in their file or something they said, it gets asked
— and an unanswered question stays a visible `TODO:`, never a guess.

**8. Plain spoken.** The voice of a good counselor who has done this five hundred
times and still likes kids. Terms of art are defined in a clause the first time; no
admissions-industrial jargon; praise is specific or absent.

## Part 2 — rules for building it

**9. Believe the disk, not the narration.** Everything produced is a file that can be
checked, and the system trusts what's actually there — never what any component,
including the model, says it did. `check_student.py` exists because the contract was
previously binding only on the honor system.

**10. One of everything.** One profile, one criteria file, one list, one place per
fact. Duplicate representations eventually disagree, so they aren't built — and the
stray-file check catches them when they appear anyway.

**11. Facts that drift live in config; rules that compute live in code, under test.**
FAFSA's opening date is a fact (`config/calendar.json`); which aid year a January
deadline belongs to is a rule (Python, tested). Rules expressed as prose get
re-derived every run, and re-derived date arithmetic is how a nine-month error hides.

**12. Every rule is derivable or earned.** A behavior either follows from Part 1 or
carries the receipt of the real incident that earned it, with a date. Rules with
neither get deleted. When an earned rule becomes checkable, it moves to code and the
prose is deleted — the receipt moves to the commit.

**13. Evidence decides — conduct is measured, not asserted.** Described behavior is
not produced behavior. Discipline rules get conduct cases (`tests/conduct/`) that
bait the exact failure; claims of improvement come with a before and an after;
single runs are noise. A dogfooded student walked through the real arc outranks any
argument from taste.

**14. Plain language is the complexity test — for designs AND skill prose.** The
audience for a skill is the user as much as the model. Skills stay small enough to
read; a cryptic instruction is a misbehavior waiting to happen; deletion is the
default answer to complexity.

---

When Part 1 and Part 2 conflict, Part 1 wins — a simplification that breaks a promise
isn't a simplification. Which documents are current, records, or superseded:
`college-apps/docs/README.md`. How a change actually gets built and proven:
`college-apps/docs/PROCESS.md`.
