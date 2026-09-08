# Schema: conversations.md

Owner: `student-intake` (appended to by all skills)
Class: **Append-only**

Location: `students/<slug>/conversations.md`

`conversations.md` is the append-only log of substantive student and family interactions. It captures verbatim phrasing, reflections, and emotional insights that form the raw material for essays and recommendation letters.

---

## `conversations.md` — owned by student-intake

### Structure & Formatting

1. **Header Order:** One dated header per session, moving strictly forward in chronological time (`## YYYY-MM-DD — <Session Topic>`).
2. **Verbatim Content:** Record what the student said in quotes, preserving their exact grammar, colloquialisms, and vocabulary. Paraphrasing into corporate adult English destroys authentic essay voice.
3. **Attribution:** Every bullet point ends with its speaker tag (`[student]`, `[parent]`, `[counselor]`).
4. **Append-Only Invariant:** Never edit, sanitize, or delete existing entries. If a correction occurs, append a new bullet or section with today's date noting the clarification.

### Concrete Template:

```markdown
# Conversations & Notes — Jordan K

## 2026-08-22 — Intake & background

- "I spent most of junior year fixing the robotics drivetrain because nobody else wanted to get their hands dirty." [student]
- "Biology maybe, idk — I like organisms more than chemistry." [student]
- "We haven't really talked about the college budget yet." [student]

## 2026-08-23 — Essay angle brainstorming

- "The bike stand outside the public library was actually my favorite project because random commuters would stop and talk." [student]
- "My dad said he doesn't want me taking out more than $20k in total debt for all four years." [student]

## 2026-09-02 — Recommendation strategy discussion

- "Ms. Alvarez knows I worked my butt off after failing that first rotational physics exam. I was in her room every Tuesday at lunch." [student]
- "Mr. Davis always pushed me to defend my claims during our Great Gatsby seminar discussions." [student]
```
