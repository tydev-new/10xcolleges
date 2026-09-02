# Schema: academic-direction.md

Owner: `major-fit`
Class: **Living**

Location: `students/<slug>/academic-direction.md`

`academic-direction.md` is the single source of truth for the student's chosen major, evaluated adjacent fields, coursework stamina evidence, institutional admission realities, and intellectual narrative ("Red Thread") for essays.

---

## `academic-direction.md` — owned by major-fit

The file must contain these exact five sections in order:

- `## Overview & Primary Direction`
- `## Coursework Stamina & Transcript Evidence`
- `## High-Leverage Adjacent Majors`
- `## Institutional Admissions Reality`
- `## Intellectual Red Thread (Why Major Essay Hooks)`

---

## Concrete Template

```markdown
# Academic Direction & Major Strategy — [Student Name]

## Overview & Primary Direction

- **Primary intended major:** Mechanical Engineering [student 2026-09-02]
- **Confidence level:** High / Exploring / Undecided [student 2026-09-02]
- **Strategic alternate major:** Materials Science & Engineering (for Common App / UC alternate major choice) [student 2026-09-02]
- **One-sentence intellectual core:** "Fixing physical things that are broken and designing assistive hardware." [student 2026-09-02]

## Coursework Stamina & Transcript Evidence

- **Flow & stamina subjects:** AP Physics C (loves mechanics), Pre-Calculus [transcript]
- **Friction tolerated:** Rebuilt robotics drivetrain 4 times last season without giving up [packet]
- **Prerequisite check:** Calculus pathway confirmed for STEM admission [transcript]

## High-Leverage Adjacent Majors

| Adjacent Major | Focus & Differentiation | Career / Grad Pathway | Admissions Advantage |
|---|---|---|---|
| Materials Science & Engineering | Focus on advanced composites, metallurgy, and failure analysis | Hardware tech, aerospace, materials R&D | Higher admit rate than ME at large engineering flagships |
| Industrial & Systems Engineering | Optimizing complex physical systems and manufacturing processes | Operations, manufacturing, tech consulting | Flexible entry, strong corporate recruitment |

## Institutional Admissions Reality

- **Direct-admit institutions:** Purdue (First-Year Engineering pre-major pool, 3.2 T2M), UIUC (Grainger direct-admit).
- **Internal transfer lockouts:** UIUC and Washington lock popular engineering and CS majors; never apply to an alternative major at these schools intending to switch.
- **Un-siloed / Open exploration:** At liberal arts colleges and non-siloed universities (Rice, Amherst), applying undecided or declaring sophomore year is fully supported.

## Intellectual Red Thread (Why Major Essay Hooks)

- **The Spark:** Tinkering with broken lawnmower engines in the garage with a neighbor [student 2026-09-02]
- **The Friction / Troubleshooting:** Spending 14 hours debugging gear backlash on the robotics arm [student 2026-09-02]
- **The Open Question:** How to design affordable prosthetic limbs using off-the-shelf compliant mechanisms [student 2026-09-02]
```

---

### Field & Provenance Rules

1. **Attributed Source Tags:** Every content bullet and row must carry an attributed source tag (`[packet]`, `[transcript]`, `[worksheet]`, `[student YYYY-MM-DD]`, `[parent …]`, `[counselor …]`).
2. **At Least Two Adjacent Majors:** The table in `## High-Leverage Adjacent Majors` must contain at least two concrete, viable alternative or interdisciplinary majors that bypass hyper-competitive single-digit admit pools while leading to equivalent career or graduate outcomes.
3. **Institutional Realities Required:** The `## Institutional Admissions Reality` section must explicitly distinguish direct-admit institutions from open exploration schools, and document internal transfer lockouts for high-demand majors.
4. **Synchronization with Profile:** Whenever the primary major or confidence changes, immediately sync `- **Intended major:**` and `- **How sure are they?**` in `profile.md § Goals and direction` and append the student's verbatim words to `conversations.md`.
