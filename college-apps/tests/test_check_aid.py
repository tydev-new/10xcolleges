#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_aid.py"

VALID_PLAN = """# Financial Aid & Scholarship Plan — Jordan K

## Strategy & Budget Target
- **Primary Strategy Archetype:** Merit-seeking (income above need-based thresholds; targeting out-of-state tuition waivers and merit matrices).
- **Annual Net Price Budget Ceiling:** $30,000/year [parent 2026-08-20].
- **Net Price Calculator Status:** Parent verified offline for in-state benchmarks.

## Form Checklist & Priority Deadlines
| School | FAFSA Priority | CSS Profile | Notes |
|---|---|---|---|
| Louisiana Tech | 2027-01-15 | Not Required | Needed for state grant consideration |
| Texas Tech | 2027-01-15 | Not Required | Priority for institutional scholarships |
| Rice University | 2026-11-15 (ED) | Required | Rice Investment initiative |

## Institutional Merit & Deadlines
| School | Scholarship Name | Potential Value | Requirements / Cutoffs | Deadline | Status |
|---|---|---|---|---|---|
| Louisiana Tech | Bulldog Out-of-State Exemption | ~$10,000/yr | 3.0+ GPA & 1230+ SAT | Automatic | Qualified |
| Texas Tech | Presidential Merit Scholarship | $4,000/yr + in-state waiver | 3.8 GPA & 1380 SAT | Automatic | Qualified |
| UT Dallas | Academic Excellence Scholarship (AES) | $3,000–$10,000/yr | Comprehensive review | 2026-12-01 | Planning |

## Outside & Local Scholarships
| Priority Tier | Award Name | Organization | Potential Value | Deadline | Status |
|---|---|---|---|---|---|
| Tier 1: High School | Roosevelt Alumni Scholarship | Roosevelt HS Counseling Bulletin | $1,500 | 2027-03-01 | Researched |
| Tier 2: Community | Rotary Club of Wyandotte | Local Rotary District 6400 | $2,500 | 2027-02-15 | Identified |
| Tier 3: Association | SME Education Foundation | Society of Manufacturing Engineers | $2,000 | 2027-02-01 | Drafting |

## Award Letter Audit
*(Pending spring admissions decisions)*
"""


def run_check(target):
    r = subprocess.run([sys.executable, str(SCRIPT), str(target)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


class TestCheckAid(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_clean_financial_aid(self):
        p = os.path.join(self.tmp, "financial-aid.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(VALID_PLAN)
        code, out, _ = run_check(p)
        self.assertEqual(code, 0, f"Expected 0 exit, got {code} with output: {out}")
        self.assertIn("OK", out)
        self.assertIn("Merit-Seeking", out)

    def test_missing_file(self):
        code, out, _ = run_check(os.path.join(self.tmp, "nonexistent.md"))
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)

    def test_missing_archetype(self):
        content = """# Financial Aid & Scholarship Plan

## Strategy & Budget Target
- Budget: $25,000.

## Form Checklist & Priority Deadlines
- FAFSA: 2026-11-01.
"""
        p = os.path.join(self.tmp, "no_arch.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        code, out, _ = run_check(p)
        self.assertEqual(code, 1)
        self.assertIn("missing Strategy Archetype", out)

    def test_missing_budget(self):
        content = """# Financial Aid & Scholarship Plan

## Strategy & Budget Target
- Strategy: Need-based path.

## Form Checklist & Priority Deadlines
- FAFSA: 2026-11-01.
"""
        p = os.path.join(self.tmp, "no_budget.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        code, out, _ = run_check(p)
        self.assertEqual(code, 1)
        self.assertIn("missing annual budget ceiling figure", out)

    def test_loans_as_aid_fails(self):
        content = VALID_PLAN + """
## Award Letter Audit
- Total COA: $50,000
- Grants: $10,000
- Net price after loans: $25,000 (subtracting Parent PLUS loan of $15,000)
"""
        p = os.path.join(self.tmp, "bad_loans.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        code, out, _ = run_check(p)
        self.assertEqual(code, 1)
        self.assertIn("loans (Direct, PLUS) cannot be subtracted", out)

    def test_lottery_without_local_warns(self):
        bad_lottery = VALID_PLAN.replace("Roosevelt Alumni Scholarship", "Taco Bell Live Mas Scholarship").replace("Rotary Club of Wyandotte", "Coca-Cola Scholars")
        bad_lottery = bad_lottery.replace("Roosevelt HS Counseling Bulletin", "National Sweepstakes").replace("Local Rotary District 6400", "National Foundation")
        bad_lottery = bad_lottery.replace("Tier 1: High School", "National Sweepstake").replace("Tier 2: Community", "National Sweepstake")
        p = os.path.join(self.tmp, "lottery.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(bad_lottery)
        code, out, _ = run_check(p)
        self.assertEqual(code, 0)
        self.assertIn("WARN", out)
        self.assertIn("only national lottery scholarships listed", out)


if __name__ == "__main__":
    unittest.main()
