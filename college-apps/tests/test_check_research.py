#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_research.py"

VALID_DOSSIER = """# Purdue University — research (retrieved 2026-08-20)

## Overview & Admissions
- **Admit rate:** 53% overall (CDS 2024-25 §C1); College of Engineering is more selective (~35%).
- **Testing:** SAT middle 50%: 1210–1450 (CDS 2024-25 §C9).
- **Admissions factors (CDS §C7):** Rigor, GPA, test scores are "Very Important." Demonstrated interest is "Not Considered."

## Academics & Programs
- **Program:** BS in Mechanical Engineering, ABET-accredited (purdue.edu/me).
- **Facilities:** Herrick Laboratories and Bechtel Innovation Design Center (maker space).
- **Undergraduate priority:** Active undergraduate research via SURF and EPICS programs.

## Costs & Financial Aid
- **Out-of-state COA:** ~$42,000/year sticker price [purdue.edu 2026-08].
- **Aid:** Limited need-based aid for non-residents; Trustees and Presidential scholarships require applying by early deadline.
- **Against budget:** Over the $30,000 ceiling by ~$12,000 unless significant outside merit is won.

## Deadlines & Requirements
- **Early Action:** 2026-11-01 (Priority for engineering and merit aid) [admissions.purdue.edu].
- **Regular Decision:** 2027-01-15.

## Fit & Campus Texture
- **Campus:** Large Big Ten campus in West Lafayette, IN (~38,000 undergrads).
- **Watch out for:**
  - *Secondary Admission:* Admits to "First-Year Engineering" (FYE) — requires completing entry coursework with a competitive GPA before transitioning to Mechanical Engineering.
  - *Climate:* Freezing, grey Midwestern winters [violates warm climate criteria].
  - *Large Lectures:* Introductory physics and chemistry lectures frequently exceed 350 students.
"""


def run_check(target):
    r = subprocess.run([sys.executable, str(SCRIPT), str(target)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


class TestCheckResearch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_clean_dossier(self):
        p = os.path.join(self.tmp, "purdue.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(VALID_DOSSIER)
        code, out, _ = run_check(p)
        self.assertEqual(code, 0, f"Expected 0 exit, got {code} with output: {out}")
        self.assertIn("OK", out)

    def test_missing_file(self):
        code, out, _ = run_check(os.path.join(self.tmp, "nonexistent.md"))
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)

    def test_missing_h1_title(self):
        p = os.path.join(self.tmp, "bad.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write("Just some text without a title\n- Admit rate 20%\n")
        code, out, _ = run_check(p)
        self.assertEqual(code, 1)
        self.assertIn("line 1 must be an # H1", out)

    def test_missing_admissions(self):
        content = """# Some University

## Academics
- Mechanical Engineering ABET.

## Cost
- $20,000 net price.

## Deadlines
- 2026-11-01.

## Fit
- Watch out for: cold winters.
"""
        p = os.path.join(self.tmp, "no_adm.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        code, out, _ = run_check(p)
        self.assertEqual(code, 1)
        self.assertIn("missing admissions selectivity", out)

    def test_missing_friction_warns(self):
        content = """# Some University

## Admissions
- Admit rate: 45% (CDS 2024).

## Academics
- Mechanical Engineering ABET.

## Cost
- $20,000 net price.

## Deadlines
- 2026-11-01.
"""
        p = os.path.join(self.tmp, "no_friction.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        code, out, _ = run_check(p)
        self.assertEqual(code, 0)
        self.assertIn("WARN", out)
        self.assertIn("no friction points", out)


if __name__ == "__main__":
    unittest.main()
