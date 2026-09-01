#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_list.py"

VALID_COLLEGES_MD = """# College list

## Michigan State University — Safety
- **Why it's here:** Meets: under $25k net price ($18k) [H1], ABET-accredited mechanical engineering [H2], within driving distance [H3].
- **The numbers:** Admit rate 88% (Scorecard 2023), GPA middle 50%: 3.5–4.0.
- **The money:** Net price estimate ~$18,000/yr [Scorecard 2023].
- **Watch out for:** Large campus size (50k students).
- **Deadline:** 2026-11-01 (EA) [admissions.msu.edu].

## Purdue University — Target
- **Why it's here:** Strong engineering reputation, meets ABET ME [H2], strong on research focus [P1].
- **The numbers:** Admit rate 53% (Scorecard 2023), SAT middle 50%: 1210–1450.
- **The money:** Net price estimate ~$22,000/yr [Scorecard 2023].
- **Watch out for:** Engineering direct-admit is much more competitive than overall rate.
- **Deadline:** 2026-11-01 (EA) [purdue.edu].

## University of Illinois Urbana-Champaign — Target
- **Why it's here:** Top 5 mechanical engineering program [H2], excellent career placement [P2].
- **The numbers:** Admit rate 45% (Scorecard 2023), SAT middle 50%: 1340–1530.
- **The money:** Net price estimate ~$24,500/yr [Scorecard 2023].
- **Watch out for:** Large lecture halls for introductory classes.
- **Deadline:** 2026-11-01 (EA) [illinois.edu].

## University of Wisconsin-Madison — Target
- **Why it's here:** Renowned engineering college [H2], great college town feel [P3].
- **The numbers:** Admit rate 49% (Scorecard 2023), ACT middle 50%: 28–33.
- **The money:** Net price estimate ~$23,000/yr [Scorecard 2023].
- **Watch out for:** Harsh winter weather.
- **Deadline:** 2026-11-01 (EA) [wisc.edu].

## Ohio State University — Safety
- **Why it's here:** Solid ABET mechanical engineering [H2], affordable honors program [H1].
- **The numbers:** Admit rate 53% (Scorecard 2023), SAT middle 50%: 1250–1460.
- **The money:** Net price estimate ~$19,500/yr [Scorecard 2023].
- **Watch out for:** Must apply by early deadline for merit scholarships.
- **Deadline:** 2026-11-01 (EA) [osu.edu].

## Northwestern University — Reach
- **Why it's here:** World-class engineering, close to Chicago [H3], unmatched alumni network [P1].
- **The numbers:** Admit rate 7% (CDS 2024), SAT middle 50%: 1500–1560.
- **The money:** Generous need-based aid, net price ~$21,000/yr [NPC 2026-08].
- **Watch out for:** Sub-10% admit rate makes it a lottery ticket for everyone.
- **Deadline:** 2026-11-01 (ED) [northwestern.edu].

## University of Michigan — Reach
- **Why it's here:** Top-tier public engineering [H2], school spirit and research funding [P1].
- **The numbers:** Admit rate 18% (Scorecard 2023), SAT middle 50%: 1350–1530.
- **The money:** Net price estimate ~$24,000/yr [NPC 2026-08].
- **Watch out for:** Out-of-state pool is fiercely competitive.
- **Deadline:** 2026-11-01 (EA) [umich.edu].

## Case Western Reserve University — Target
- **Why it's here:** Hands-on maker space, strong engineering [H2], great co-op program [P2].
- **The numbers:** Admit rate 27% (Scorecard 2023), SAT middle 50%: 1420–1520.
- **The money:** Net price estimate ~$24,000/yr [Scorecard 2023].
- **Watch out for:** Heavy workload and rigorous grading.
- **Deadline:** 2026-11-01 (EA) [case.edu].
"""


def run_check(sd):
    r = subprocess.run([sys.executable, str(SCRIPT), str(sd)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


class TestCheckList(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_clean_list(self):
        with open(os.path.join(self.tmp, "colleges.md"), "w", encoding="utf-8") as f:
            f.write(VALID_COLLEGES_MD)
        code, out, _ = run_check(self.tmp)
        self.assertEqual(code, 0, f"Expected 0 exit, got {code} with output: {out}")
        self.assertIn("OK", out)
        self.assertIn("list balance: 2 safeties, 4 targets, 2 reaches (total 8)", out)

    def test_missing_colleges_file(self):
        code, out, _ = run_check(self.tmp)
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        self.assertIn("colleges.md not found", out)

    def test_missing_field(self):
        content = """# College list

## Michigan State University — Safety
- **Why it's here:** Solid program in state.
- **The numbers:** Admit rate 88%.
- **The money:** Net price $18k.
- **Deadline:** 2026-11-01.
"""
        with open(os.path.join(self.tmp, "colleges.md"), "w", encoding="utf-8") as f:
            f.write(content)
        code, out, _ = run_check(self.tmp)
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        self.assertIn("Watch out for", out)

    def test_cryptic_code_fails(self):
        content = """# College list

## Michigan State University — Safety
- **Why it's here:** Meets H1, H2.
- **The numbers:** Admit rate 88%.
- **The money:** Net price $18k.
- **Watch out for:** Big campus.
- **Deadline:** 2026-11-01.
"""
        with open(os.path.join(self.tmp, "colleges.md"), "w", encoding="utf-8") as f:
            f.write(content)
        code, out, _ = run_check(self.tmp)
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        self.assertIn("plain words, not just codes", out)

    def test_over_budget_school_fails(self):
        criteria_content = """# List criteria
## Hard filters
| # | Criterion | Value | Source | Added |
|---|---|---|---|---|
| H1 | Budget | Under $30,000 net price/year, set by: parents | [parent 2026-08-20] | 2026-08-20 |
"""
        with open(os.path.join(self.tmp, "criteria.md"), "w", encoding="utf-8") as f:
            f.write(criteria_content)

        colleges_content = """# College list

## UT Arlington — Target
- **Why it's here:** Strong engineering program in Texas.
- **The numbers:** Admit rate 80%.
- **The money:** Net price estimate ~$39,476/yr [Scorecard].
- **Watch out for:** Commuter school.
- **Deadline:** 2026-12-01.
"""
        with open(os.path.join(self.tmp, "colleges.md"), "w", encoding="utf-8") as f:
            f.write(colleges_content)

        code, out, _ = run_check(self.tmp)
        self.assertEqual(code, 1)
        self.assertIn("exceeds budget ceiling", out)


if __name__ == "__main__":
    unittest.main()
