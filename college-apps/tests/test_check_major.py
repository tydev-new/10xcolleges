import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_major.py"

VALID_DOSSIER = """# Academic Direction & Major Strategy — Jordan K

## Overview & Primary Direction

- **Primary intended major:** Mechanical Engineering [student 2026-09-02]
- **Confidence level:** High [student 2026-09-02]
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

- **Direct-admit institutions:** Purdue (First-Year Engineering pre-major pool, 3.2 T2M), UIUC (Grainger direct-admit) [packet]
- **Internal transfer lockouts:** UIUC and Washington lock popular engineering and CS majors; never apply to an alternative major at these schools intending to switch [packet]

## Intellectual Red Thread (Why Major Essay Hooks)

- **The Spark:** Tinkering with broken lawnmower engines in the garage with a neighbor [student 2026-09-02]
- **The Friction / Troubleshooting:** Spending 14 hours debugging gear backlash on the robotics arm [student 2026-09-02]
- **The Open Question:** How to design affordable prosthetic limbs using off-the-shelf compliant mechanisms [student 2026-09-02]
"""


def run_check(content):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(content)
        path = f.name
    r = subprocess.run([sys.executable, str(SCRIPT), path], capture_output=True, text=True)
    Path(path).unlink(missing_ok=True)
    return r.returncode, r.stdout


class TestCheckMajor(unittest.TestCase):
    def test_clean_dossier_passes(self):
        code, out = run_check(VALID_DOSSIER)
        self.assertEqual(code, 0, out)
        self.assertIn("OK", out)

    def test_missing_section_fails(self):
        bad = VALID_DOSSIER.replace("## High-Leverage Adjacent Majors", "## Random Section")
        code, out = run_check(bad)
        self.assertEqual(code, 1, out)
        self.assertIn("missing required section", out)

    def test_missing_primary_major_fails(self):
        bad = VALID_DOSSIER.replace("- **Primary intended major:** Mechanical Engineering [student 2026-09-02]", "- **Primary intended major:** TODO:")
        code, out = run_check(bad)
        self.assertEqual(code, 1, out)
        self.assertIn("missing or unverified", out)

    def test_fewer_than_two_adjacent_majors_fails(self):
        bad = VALID_DOSSIER.replace("| Industrial & Systems Engineering | Optimizing complex physical systems and manufacturing processes | Operations, manufacturing, tech consulting | Flexible entry, strong corporate recruitment |\n", "")
        code, out = run_check(bad)
        self.assertEqual(code, 1, out)
        self.assertIn("must contain at least 2 options", out)

    def test_missing_source_tag_fails(self):
        bad = VALID_DOSSIER.replace("- **The Spark:** Tinkering with broken lawnmower engines in the garage with a neighbor [student 2026-09-02]", "- **The Spark:** Tinkering with broken lawnmower engines in the garage with a neighbor")
        code, out = run_check(bad)
        self.assertEqual(code, 1, out)
        self.assertIn("no source tag", out)

    def test_missing_red_thread_fails(self):
        bad = VALID_DOSSIER.split("## Intellectual Red Thread")[0] + "## Intellectual Red Thread (Why Major Essay Hooks)\n\nNone yet.\n"
        code, out = run_check(bad)
        self.assertEqual(code, 1, out)
        self.assertIn("intellectual red thread must contain at least 2 hooks", out)


if __name__ == "__main__":
    unittest.main()
