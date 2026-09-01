# 10xcolleges

A Claude plugin that coaches high school students through college application essays the way a great counselor would — uncovering authentic personal stories, breaking down prompts, and giving honest feedback draft by draft without ghostwriting.

Plain-spoken, encouraging, and focused on helping students sound like themselves.

---

## Part of the 10xJobs family

10xcolleges is a project of [10xjobs.co](https://10xjobs.co), built by the same team.

10xjobs.co helps job seekers navigate an application process that's opaque, high-stakes, and full of jargon nobody explains to you. 10xcolleges applies that same thinking (plain language, honest feedback, no ghostwriting or shortcuts) to a different high-stakes, opaque process: getting into college. Same product philosophy, different audience and problem.

---

## What's ready now — Essay Coaching

The core essay coaching experience is fully built, reviewed, and measured:

| Skill | What it does for you | How it's kept honest |
|---|---|---|
| **student-intake** | Gets to know you through a short conversation or by reading whatever your school gave you (a counselor packet or activities list). It draws out your favorite activities, hobbies, and stories in your own words. It leaves blanks blank and never asks for sensitive personal info like family finances. | A verification script checks the files after every turn: no untagged facts, no blanks filled with guesses, and your words are never altered or summarized into buzzwords. |
| **essay-coach** | Guides you through one essay at a time (your Common App personal statement or any college supplement). It breaks down what the prompt really asks, builds a scoring checklist (rubric) from college guidance, and explores 3–4 angles from things you've actually done. Then it reviews draft by draft: what's working, the one big thing to change, and specific line notes. | Every draft clearly states its author on line one. The coach points at issues and explains why, but never rewrites your sentences for you. A blind cold reader checks every draft to see what real admissions readers will remember. |

Both skills are tested and verified with simulated multi-turn student conversations (conduct harness in `college-apps/tests/always-on/`). What they will never do: write your essay, invent details, or look outside the folder you chose.

---

## Install

### In Claude Cowork

1. Open **Customize** in the sidebar, then **Plugins**.
2. Select **Add marketplace** and enter:
   ```
   tydev-new/10xcolleges
   ```
3. **College Applications** appears in the list. Click **Install**.

The skills load automatically and activate whenever you talk about college essays.

### In Claude Code

```bash
/plugin marketplace add tydev-new/10xcolleges
/plugin install college-apps@10xcolleges
```

---

## Using it

Just say what you need in natural language. The coach meets you where you are.

### 1. Getting Started
Hand it whatever your school gave you, or just introduce yourself:

> "Help me get started on my college essays. Here's my school's senior packet: `~/Downloads/Senior_Packet.pdf`"

First it confirms where your files will live (usually a dedicated folder). Then it reads your packet and asks a couple of relaxed questions to understand what you care about — what you like to study, what you do when nobody's making you, and what experiences you'd gladly repeat.

### 2. Exploring Angles & Creating the Brief
Name the essay you want to work on:

> "I want to work on the Pomona supplement: 'What at Pomona would you use, and what would you bring?'"

The coach restates the prompt in plain English, creates a 4–6 point checklist based on what that college values, and weighs 3–4 angles drawn directly from your life:

- **Angle A:** The weekend bike repair job → joining the campus bike co-op (shows community contribution and hands-on persistence).
- **Angle B:** Rebuilding the robotics drivetrain four times (shows grit, but common among STEM applicants).
- **Angle C:** Quitting varsity soccer (risky and interesting; reveals true values).

You choose the angle that feels right to you.

### 3. Drafting Your Way
The coach asks how you want to get the first words on the page:

- **You write it:** Slowest start, best result — your authentic voice shines from the first sentence.
- **See a sample first:** Read a published essay on a completely different topic to see what specific, vivid structure looks like before you write.
- **First pass scaffold:** The coach drafts a structural outline from your notes. You rewrite it from scratch with the file closed so the final words remain 100% your own.

### 4. Reviewing Draft by Draft
Paste your draft or save it in your essay folder:

> "Here's my first draft of the Pomona essay, it's in my folder. What do you think?"

Each review gives you:
1. **The Score:** A clear checklist score against the prompt rubric (e.g. `3/5`).
2. **What's Working:** Specific lines quoted with why they are effective.
3. **The One Big Thing:** The single most impactful structural change to focus on next.
4. **Line Fixes & Questions:** Clear notes on sentences that feel generic or need more detail.

If two rounds get the same score, the coach pauses and changes strategy rather than nagging you on the same line.

---

## What you get

Your workspace is kept neat and readable in plain markdown files you can open and edit anytime:

| File | What it holds |
|---|---|
| `students/<name>/profile.md` | Your background, activities, roles, and reflections — every line tagged by source |
| `students/<name>/conversations.md` | Notes and ideas captured during coaching in your exact words |
| `students/<name>/essays/<college>--<prompt>/brief.md` | The prompt breakdown, scoring rubric, chosen angle, and outline |
| `students/<name>/essays/<college>--<prompt>/draft-NN.md` | Every draft version preserved in order, labeled by author |
| `students/<name>/essays/<college>--<prompt>/review-NN.md` | Structured reviews with scores, praise, and specific edits |

---

## What it will never do

- **Never ghostwrite:** Colleges require students to affirm that their essays are their own work. The coach teaches and guides, but never writes the essay for you.
- **Never invent facts:** No made-up awards, exaggerated hours, or fictional emotions. Everything in your essay traces back to your real experiences.
- **Never probe sensitive finances:** Essay coaching is about your voice and stories; it never asks for personal family financial details.
- **Never overwrite history:** Every draft and review is preserved as a separate file so you can always see how your writing evolved.

---

## Development & Testing

```bash
git clone https://github.com/tydev-new/10xcolleges.git
cd 10xcolleges
python3 -m unittest discover college-apps/kit/tests
python3 -m unittest discover college-apps/tests
```

**Architecture & Principles:**
- [`design.md`](college-apps/docs/design.md): System architecture, multi-turn conduct loop, and file boundaries.
- [`data-model.md`](college-apps/docs/data-model.md): Data contracts and file schemas.
- [`skill-shape.md`](college-apps/docs/skill-shape.md): Skill structure, invariants, and evaluation guidelines.

---

## License

MIT — see [LICENSE](LICENSE).
