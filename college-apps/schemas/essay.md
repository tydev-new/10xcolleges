# Schema: Essay Coaching Files

Owner: `essay-coach`
Location: `students/<slug>/essays/<college-slug>--<prompt-slug>/` (or `common-app--<prompt-slug>/`)

Each essay occupies its own isolated directory containing its brief, immutable drafts, and immutable reviews.

---

## `brief.md` — owned by essay-coach
- `## Fixed`
- `## Living`
- `### Rounds`

### `brief.md` Structure
- `## Fixed` (Fixed-source): Defined by the college. Only changes if prompt changes or was copied wrong.
  - Plain-language restatement of prompt.
  - 4–6 yes/no criteria, each labeled with its source tier (1: college guidance, 2: CDS §C7, 3: public reader guide, 4: derived).
  - Word count, format, and lookup date.
- `## Living` (Living): Defined by the student. Updates as the essay develops.
  - 3–4 weighed angles, chosen angle, and why.
  - Outline beats for chosen angle.
  - Chosen draft mode (A: student writes, B: sample first, C: agent first pass).
- `### Rounds` (Append-only table): Score and decision trail across all rounds.
  - Table header: `| round | date | N/M | the one big thing | student's choice |`
  - Two rows with identical `N/M` indicates the loop ceiling.

---

## `draft-NN.md` — owned by essay-coach (free-form body)

Class: **Immutable** (never edited; revisions become `draft-NN+1.md`)

Line 1 must contain exactly one author header marker:
```markdown
> **STUDENT DRAFT**
```
or
```markdown
> **AGENT FIRST DRAFT — built from your intake and our conversations. This is scaffolding, not your essay. Rewrite it in your own words before it goes anywhere near an application. Check every fact: if I got something wrong or put words in your mouth, say so and I'll cut it.**
```
or
```markdown
> **EXAMPLE — a different student, a different topic. Do not submit any part of this. It's here to show what specificity looks like, not what to say.**
```

---

## `review-NN.md` — owned by essay-coach
- `## Against the brief`
- `## Cold reader`
- `## External feedback` — optional
- `## Angle check` — optional
- `## What's working`
- `## The one big thing`
- `## Specific fixes`
- `## One question`

Class: **Immutable** (never edited; one review per draft)

### Review Template
```markdown
# Review <NN> — <College / Prompt Slug>

## Against the brief
- **Student's read:** <Their score and notes, or "—">
- **Rubric evaluation:**
  - [<Met / Not Met>] <Criterion 1 with source tier>: <Evidence / Gap>
  - [<Met / Not Met>] <Criterion 2 with source tier>: <Evidence / Gap>
- **Score:** <N/M>
- **Read gap:** <Analysis of differences between student and coach reads>

## Cold reader
- **Impression:** <One-sentence blind reader take>
- **Remembered:** <What sticks after an hour>
- **Question:** <Lingering reader question>

## External feedback
<!-- When feedback.md has teacher/counselor feedback, quote here (outranks coach) -->

## Angle check
<!-- On chosen angle, or drifted: somewhere better (Living updated) or easier -->

## What's working
- "<Exact quote 1>" — <Why it works>
- "<Exact quote 2>" — <Why it works>

## The one big thing
<The single most impactful revision to make>

## Specific fixes
1. Line <L>: "<Quote>" → <Issue and suggested fix>

## One question
<One genuine question that unlocks deeper material>
```
