# Evaluation Rubric: Recommendation Strategy & Materials

Every recommendation plan, brag sheet (`recs/brag-sheet--<teacher>.md`), and request draft (`recs/request--<teacher>.md`) is evaluated across five critical dimensions to ensure letters provide distinctive, credible evidence for holistic admissions committees.

---

## 1. Five-Dimension Evaluation Rubric

### 1. Recommender Balance & Eligibility
- **Core Academic Disciplines:** Recommenders must teach core academic disciplines (English, Mathematics, Lab Science, Social Studies, Foreign Language). Elective teachers (PE, Art, Choir) may only serve as optional supplemental recommenders where explicitly permitted.
- **Cross-Disciplinary Balance:** For colleges requiring two letters, aim for **one STEM teacher and one Humanities/Social Science teacher**. This satisfies strict institutional mandates (e.g., MIT, Caltech) and proves cognitive versatility across both quantitative and analytical domains.
- **Junior-Year Priority:** Letters must come from 11th-grade teachers who taught the student through advanced rigor for a full academic year, rather than 9th/10th-grade teachers (too distant) or 12th-grade teachers (barely 6 weeks together by early deadlines).
- **Admissions Cap Compliance:** Strict adherence to each college's maximum letter ceiling; never submit uninvited supplemental letters that clutter the admissions file.

### 2. Classroom Specificity & Concrete Evidence
- **Narrative Bricks from Their Classroom:** Brag sheets must feature at least three concrete, micro-level memories from that teacher's classroom (named units, specific lab numbers, book titles, debate topics).
- **Anti-Resume Standard:** The brag sheet must **not** be a cut-and-paste resume. It exists solely to remind the teacher of shared experiences that occurred within their four walls.
- **Named Collaborators & Details:** References specific project teammates, equipment built, or lunch review sessions attended.

### 3. Intellectual Friction & Academic Stamina
- **Vulnerability & Recovery:** The brag sheet must highlight at least one moment where the student struggled, failed an initial assessment, received critical feedback, and persevered to mastery.
- **Intellectual Risk-Taking:** Highlights moments where the student asked a provocative question, argued an unconventional perspective in seminar, or pursued an unassigned research rabbit hole.
- **Peer Generosity:** Shows how the student elevated the classroom environment (e.g. voluntary peer tutoring, troubleshooting lab equipment for others).

### 4. Major & Intellectual Alignment
- **Through-Line to Declared Direction:** The qualities demonstrated in the classroom must support the student's declared major in `academic-direction.md` (e.g. troubleshooting and mechanical patience for Mechanical Engineering; textual rigor for History).
- **Synchronized Logistics:** Lists the student's primary intended major, target college list, and earliest verified application deadline.

### 5. Interpersonal Diplomacy, Tone & FERPA Rights
- **Two-Step In-Person Protocol:** The written request email (`request--<teacher>.md`) must follow a personal, face-to-face conversation after class, giving the teacher an easy out.
- **Tone:** Humble, appreciative, and considerate of the teacher's heavy autumn grading workload.
- **FERPA Waiver Invariant:** Confirmation that the student has irrevocably waived their right to inspect recommendations in the Common App.

---

## 2. Who Checks What

| Requirement | Checked By | Method |
|---|---|---|
| All 5 H2 sections present in brag sheet | `scripts/check_rec.py` | Deterministic header check |
| At least 3 classroom moments present | `scripts/check_rec.py` | Bullet count check ($\ge 3$) |
| Minimum substance / word density per moment | `scripts/check_rec.py` | Word count threshold ($\ge 15$ words) |
| Declared intended major & earliest deadline date | `scripts/check_rec.py` | Regex pattern matching |
| `request--*.md` has Subject & in-person acknowledgment | `scripts/check_rec.py` | Keyword & regex matching |
| Recommender cross-disciplinary balance (1 STEM + 1 Hum) | Agent / Counselor | Qualitative audit against college list |
| Genuine intellectual friction vs. empty bragging | Agent / Counselor | Rubric Dimension 3 |
| Authentic 17-year-old voice (no corporate jargon) | Agent / Counselor | Rubric Dimension 5 |
| Teacher letter vs. Counselor letter division of labor | Agent / Counselor | Cross-file audit against `counselor-questions.md` |
