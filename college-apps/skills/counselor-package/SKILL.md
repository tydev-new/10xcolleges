---
name: counselor-package
description: Build the interim package for a school counselor or parent to review — a self-contained HTML/PDF with the student snapshot, college list and reasoning, research, essay status, recommendation plan, and specific questions for their feedback. Also produces the filled-in school packet as .docx. Use when sharing progress with a counselor or parent, or when the student needs their completed post-secondary options packet.
---

# The counselor package

Read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md`. Two deliverables, different audiences:

- **`out/package.html`** (+ PDF) — the interim review document. For the counselor.
- **`out/packet.docx`** — the school's own Post-Secondary Options Packet, filled in. For
  submitting to the school.

**Guardrails first:** if the working folder's `CLAUDE.md` is missing the
`college-apps guardrails` block, copy or append
`${CLAUDE_PLUGIN_ROOT}/templates/workspace-CLAUDE.md` before continuing
(`student-intake` § Part 0 has the full rule; refresh an outdated version only by offer).

## The review package

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_package.py" students/<slug> --pdf
```

Self-contained HTML — no external CSS, fonts, or scripts — so it survives email, Drive,
and being opened offline. Prints cleanly to PDF (`--pdf` uses headless Chrome if present;
otherwise Cmd-P). It pulls from `profile.md`, `meta.json`, `research/`, `essays/`, and
`recs/` automatically, so the way to improve the package is to improve those files.

### The part that matters: the asks

The package opens with **"Where we'd value your input."** This is the whole point of
sending it. A counselor with 300 students will not read eleven pages and free-associate
feedback — they'll answer specific questions.

The script generates sensible defaults, but write your own to
`students/<slug>/counselor-questions.md` whenever there's something real to ask. Good asks
are ones only this counselor can answer:

> 1. We have Case Western as a target based on the CDS ranges. You'd know better than the
>    data does — how have our students actually fared there the last few years?
> 2. Jordan's sophomore-year dip was the semester their mom was in treatment. They'd
>    rather not write about it in the essay. Is that context you'd normally include in the
>    school report, and do you want anything from us for it?
> 3. Ms. Alvarez and Mr. Chen are our two teacher recommenders. Any reason to steer
>    differently?
> 4. Northeastern's net price still runs about $6k/yr over the family's ceiling. Are there
>    school-based or local scholarships worth applying for that we wouldn't know about?

Bad asks are ones the internet can answer ("what's Michigan's deadline?"). Don't waste
their attention on those.

### Before you send

Check the package for these, because the counselor certainly will:

- **Fewer than two safeties** — the script flags this in red. Fix the list before sending,
  or name it in the asks as a known open problem. Don't send it unmentioned.
- **`TODO:` count in the profile** — the script surfaces it. A few open items is honest.
  Twenty means intake isn't finished.
- **Uncited numbers** — every fact in the research files needs its source and vintage. The
  counselor is exactly the reader who will notice an unsourced admit rate.
- **Essay drafts** — the build now *enforces* this: `build_package.py` refuses to run if
  any `draft-NN.md` lacks a provenance header, and agent-written drafts render with a
  visible warning in the package. If the build stops here, add the missing header rather
  than working around it — presenting a Mode C draft as the student's own work damages
  their credibility with the one reader who will later see the submitted essay.

### After you send

Log everything the counselor says to `feedback.md`, attributed and dated, in their words.
Then actually act on it: re-tier the schools they questioned, add the ones they suggested,
update the tracker. Tell the student what changed and why.

Counselor feedback outranks yours on anything local — how this school's students have
actually done at a given college, what the school report will say, which teachers write
well. They have information the data doesn't.

## The school packet

The school wants their own form back. Build `packet.json` from `profile.md` first — you do
the extraction, the script does the layout. The shape is documented in the header of
`${CLAUDE_PLUGIN_ROOT}/scripts/fill_packet.py`.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fill_packet.py" students/<slug>
```

Colleges are pulled from `meta.json` automatically. Anything missing renders as
`[to be completed]` in grey, so the student can see exactly what's left rather than
receiving a document that looks finished and isn't.

Rules:

- **The student's reflection answers go in verbatim.** Do not polish them into consultant
  prose. The counselor is reading these to find material for a letter that sounds like a
  real kid, and a packet that reads like it was written by an adult is worse than useless.
- **Never fill a blank with a guess.** `[to be completed]` is the correct output for
  anything you don't actually know.
- **The parent worksheet is the parent's.** Transcribe what they wrote. Don't improve it.
- **Question 4 is sensitive** — personal challenges, and whether to include them in the
  letter. Whatever the student said about disclosure is binding. If they said no, it does
  not go in the packet, and it does not go in the package either.

Then have the student check it before it goes to the counselor. It's their document and
their name on it.

## Timing

Send the first package **early** — September, when the list is drafted but before the
essays are locked. Feedback in September changes the list; feedback in December changes
nothing. Send an updated one after the list settles and once more before the earliest
deadline.

Say what changed since last time at the top. A counselor re-reading eleven pages to find
three differences will stop opening them.

*Every reply ends with ONE contextual next step — a sentence with its why, not a menu.*
