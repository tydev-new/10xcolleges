# 10xcolleges — what it is, and how we build it

Written in plain language on purpose: if something can't be explained in this style, it's too complex to ship (rule 13). When a design and this document disagree, one of them is wrong. `docs/voice.md` is how we talk; this is what we promise.

## Part 1 — What 10xcolleges is

*(promises to the student — and to the parent and counselor reading over their shoulder. Every skill answers to these.)*

**1. One goal.** Help you get into a college you'll actually be glad you went to — not the highest-ranked one you can reach. Everything in the product visibly serves that, or it goes.

**2. It runs your applications as three things.** A list (balanced across safety, target, and reach, and honest about which is which), the work you carry across every school (who you are, your essays, your recommenders), and a calendar (every deadline known, every task worked backward from it). The sign it's working: nothing is due tomorrow that you're hearing about today.

**3. The essay is yours.** Words the agent wrote are labeled as the agent's, every time, and a draft without that label does not exist — the package refuses to build. You can ask for an example, a first draft to react against, or a rewrite of your own words; what gets submitted is what *you* wrote, and the record shows whose words they were. This is the line this product cannot cross, because the cost is yours: a discovered ghostwritten essay ends an application, and sometimes more than one.

**4. Honest odds, said once, kindly.** A 5% school is a lottery ticket for a valedictorian too. We say so, we don't say it twice, and then we help you apply if you love it. No admission probabilities, no numeric fit scores — tiers and named trade-offs, because a number implies a model that doesn't exist and you would sort by it.

**5. The money is known before the choice, not after.** Sticker price is not the number; the net price for *your* family is, and we find it — the school's own calculator, not the average — before a school earns a place on the list. Every list has at least one school you can afford without a scholarship you haven't won yet; merit aid is never counted before it's in writing. The aid calendar (FAFSA, CSS Profile, each school's priority deadline) sits on the same tracker as the application deadlines, worked backward the same way. And the agent goes looking for the money that doesn't come to you — outside scholarships you qualify for, each with its deadline, its source, and what it actually requires — so that the question "can we pay for this" has an answer in September, not a surprise in April. The family's ceiling is the family's to set; we never tell you what you can afford, only what each school costs against the number you gave.

**6. Every fact has a source.** A college's admit rate, cost, deadline, or program exists only with where it came from and when. Something about you exists only because you said it or a document of yours shows it. "Not found — needs checking" is a real answer; a plausible guess is not. The one thing we never hand-compute is a date: deadlines and aid years come from code under test, because a nine-month error hides in plain sight.

**7. The agent does everything that doesn't need you.** Researching, drafting the tracker, pre-filling the packet, building the package, remembering the dates, drafting the ask to a teacher. You do only what genuinely needs you: the writing, the choosing, the asking, the clicking. Nothing the agent could have prepared ever sits on your list as work.

**8. The important moments are unmissable.** Anything that leaves your hands — a recommendation request sent to a teacher, the package shared with a counselor or parent, an application submitted — follows the same steps: you see the complete thing; one plain sentence says what happens when it goes; your explicit yes; a log line. No button fires these — only your word.

**9. You own the record.** Every output is a file you can read, edit, and keep — your profile, your list and its reasons, every draft in order, every review, what you said and when. A correction is a new dated line, never a quiet rewrite, so the record stays something a counselor can trust. And the counselor and your parents get the same files, not a summary that flatters.

## Part 2 — How we build it

*(the build rules — `kit/PRINCIPLES-core.md`, adopted unchanged: believe the disk, one of everything, every rule derivable or earned, evidence decides, plain language is the complexity test.)*

When Part 1 and Part 2 conflict, Part 1 wins — a simplification that breaks a promise isn't a simplification. The designs that derive from this file: `docs/design.md` (the working design) and `docs/skill-shape.md` (the shape every skill follows), in that order of authority.
