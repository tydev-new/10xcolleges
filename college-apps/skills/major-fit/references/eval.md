# Evaluation Rubric: `major-fit`

This rubric evaluates the strategic depth, intellectual honesty, and institutional realism of `academic-direction.md`.

---

## The 5-Dimension Rubric

| Dimension | Target (Pass) | Defect (Fail) |
|---|---|---|
| **1. Intellectual Flow & Authenticity** | Grounded in student's demonstrated curiosity, Sunday night flow test, and stamina during friction (debugging, rebuilding, writing). | Chooses a major purely based on parent pressure, salary rankings, or generic prestige without evidence of student flow. |
| **2. Transcript & Rigor Alignment** | Coursework prerequisites (e.g. Calculus for engineering/CS/business; chemistry/biology for pre-med) verified on transcript. | Validates a selective STEM or business major where student lacks required math/science foundational coursework. |
| **3. Strategic Adjacent Alternatives** | Maps at least two high-leverage adjacent majors that lead to identical career/graduate outcomes with higher admit rates or broader interdisciplinary training. | Suggests only one major, or offers zero alternatives to hyper-crowded single-digit admit pools (e.g. only CS). |
| **4. Institutional Admissions Reality** | Clearly distinguishes direct-admit siloed colleges from un-siloed liberal arts colleges; warns against internal transfer lockouts for high-demand programs. | Endorses a "backdoor gimmick major" to sneak into a university with the plan to transfer into a locked major (e.g. UIUC CS). |
| **5. Intellectual Red Thread (Essay Hooks)** | Captures three distinct narrative beats: an authentic origin spark, a moment of troubleshooting/friction, and an open question outside the syllabus. | Relies on generic clichés ("I've loved computers since I was 5", "I want to help people") without specific classroom or project moments. |

---

## Who checks what

| Artifact / Behavior | Checked by | When | Standard |
|---|---|---|---|
| 5 required H2 sections present | `check_major.py` | End of turn | `academic-direction.md` schema |
| Primary major + confidence declared | `check_major.py` | End of turn | Label and value non-empty |
| $\ge 2$ adjacent majors mapped in table | `check_major.py` | End of turn | Table rows $\ge 2$ |
| Source tags on content lines | `check_major.py` | End of turn | `[packet]`, `[transcript]`, `[student YYYY-MM-DD]` |
| Institutional transfer lockout note | `check_major.py` | End of turn | Mentions direct-admit or transfer lockout gates |
| Red Thread essay hooks ($\ge 2$) | `check_major.py` | End of turn | Spark, friction, or open question present |
| Intellectual flow & stamina depth | Counselor / Judge | Review | Dimension 1 |
| Transcript prerequisite alignment | Counselor / Judge | Review | Dimension 2 |
| Gimmick major avoidance | Counselor / Judge | Review | Dimension 4 |

---

## Boundaries

The consumer bar — what downstream skills require from `academic-direction.md`:

- **For `college-list`:** Must state primary major and at least one viable adjacent major so the list can index tiering to major-specific departmental selectivity.
- **For `college-research`:** Must specify the degree target (e.g. BSME vs. BA Physics) so the research dossier can audit departmental accreditation (ABET) and pre-major gates (FYE).
- **For `essay-coach`:** Must provide the origin spark, troubleshooting moment, and open question so the coach can construct the "Why Major" essay brief.
