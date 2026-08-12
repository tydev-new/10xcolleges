#!/usr/bin/env python3
"""Date-logic tests for the tracker.

These pin the arithmetic that costs real money when it's wrong: which aid year a
deadline belongs to, what happens when a student starts late, and what happens when a
deadline is missing or mistyped.

Run:  .venv/bin/python -m unittest discover -s tests -v
"""

import json
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import make_tracker as mt  # noqa: E402

CFG = mt.load_config()


def colleges(*specs):
    """specs: (name, deadline, status) -> the (college, parsed_date) pairs build_tasks wants."""
    meta = {"colleges": [
        {"name": n, "deadline": d, "status": s} for n, d, s in specs
    ]}
    return mt.read_colleges(meta)


def due_for(tasks, needle):
    return [t["due"] for t in tasks if needle in t["task"]]


class AidYearAnchor(unittest.TestCase):
    """FAFSA is keyed to the fall the student matriculates, not the deadline's year."""

    def test_january_deadline_anchors_to_previous_october(self):
        # RD for fall 2027 entry -> FAFSA opened Oct 2026, not Oct 2027.
        self.assertEqual(mt.aid_year_anchor(date(2027, 1, 15), 7), 2026)

    def test_june_deadline_still_previous_cycle(self):
        self.assertEqual(mt.aid_year_anchor(date(2027, 6, 1), 7), 2026)

    def test_november_deadline_anchors_to_same_year(self):
        # EA in Nov 2026 for fall 2027 entry -> FAFSA opened Oct 2026.
        self.assertEqual(mt.aid_year_anchor(date(2026, 11, 1), 7), 2026)

    def test_july_is_the_boundary(self):
        self.assertEqual(mt.aid_year_anchor(date(2026, 7, 1), 7), 2026)
        self.assertEqual(mt.aid_year_anchor(date(2026, 6, 30), 7), 2025)


class FafsaScheduling(unittest.TestCase):
    def test_rd_only_list_puts_fafsa_before_the_deadlines(self):
        """The nine-month bug: FAFSA must not be scheduled after the applications."""
        today = date(2026, 9, 15)
        cs = colleges(("Case Western", "2027-01-15", "committed-to-apply"),
                      ("Northeastern", "2027-01-01", "committed-to-apply"))
        tasks, _, _ = mt.build_tasks(cs, today, CFG)
        fafsa = due_for(tasks, "FAFSA")[0]
        self.assertLess(fafsa, date(2027, 1, 1),
                        "FAFSA scheduled after the earliest application deadline")
        self.assertEqual(fafsa, date(2026, 10, 1))

    def test_ea_list_fafsa_same_autumn(self):
        today = date(2026, 8, 1)
        cs = colleges(("Michigan", "2026-11-01", "committed-to-apply"))
        tasks, _, _ = mt.build_tasks(cs, today, CFG)
        self.assertEqual(due_for(tasks, "FAFSA")[0], date(2026, 10, 1))


class PassedDeadlines(unittest.TestCase):
    def test_passed_deadline_gets_no_task_plan(self):
        today = date(2026, 9, 15)
        cs = colleges(("Missed U", "2026-08-01", "in-progress"))
        tasks, notices, _ = mt.build_tasks(cs, today, CFG)
        # Profile-wide tasks (FAFSA, personal statement) are independent of any one
        # college and still apply; only this college's 12-step plan should be absent.
        mine = [t for t in tasks if t["college"] == "Missed U"]
        self.assertEqual(len(mine), 1, "expected only the flag task for this college")
        self.assertIn("DEADLINE PASSED", mine[0]["task"])
        self.assertTrue(any("already passed" in n for n in notices))

    def test_no_impossible_submit_task(self):
        today = date(2026, 9, 15)
        cs = colleges(("Missed U", "2026-08-01", "in-progress"))
        tasks, _, _ = mt.build_tasks(cs, today, CFG)
        self.assertEqual(due_for(tasks, "SUBMIT Missed U"), [])

    def test_closed_statuses_generate_nothing(self):
        today = date(2026, 9, 15)
        for status in ("withdrawn", "decided", "submitted"):
            cs = colleges(("Done U", "2026-12-01", status))
            tasks, _, _ = mt.build_tasks(cs, today, CFG)
            self.assertEqual([t for t in tasks if t["college"] == "Done U"], [],
                             f"{status} should not generate tasks")


class Compression(unittest.TestCase):
    def test_short_runway_compresses_instead_of_overdue(self):
        today = date(2026, 9, 15)
        cs = colleges(("Soon State", "2026-10-01", "committed-to-apply"))
        tasks, notices, catch_up = mt.build_tasks(cs, today, CFG)
        college_tasks = [t for t in tasks if t["college"] == "Soon State"]
        self.assertEqual(len(college_tasks), len(CFG["backward_plan"]))
        self.assertTrue(all(t["due"] >= today for t in college_tasks))
        self.assertTrue(any("compressed" in n for n in notices))

    def test_compression_preserves_order(self):
        today = date(2026, 9, 15)
        cs = colleges(("Soon State", "2026-10-01", "committed-to-apply"))
        tasks, _, _ = mt.build_tasks(cs, today, CFG)
        ask = due_for(tasks, "Ask recommenders")[0]
        submit = due_for(tasks, "SUBMIT Soon State")[0]
        self.assertLess(ask, submit, "asking recommenders must precede submitting")

    def test_full_runway_is_not_compressed(self):
        today = date(2026, 1, 1)
        cs = colleges(("Roomy U", "2026-11-01", "committed-to-apply"))
        tasks, notices, _ = mt.build_tasks(cs, today, CFG)
        submit = due_for(tasks, "SUBMIT Roomy U")[0]
        self.assertEqual(submit, date(2026, 11, 1))
        self.assertFalse(any("compressed" in n for n in notices))

    def test_no_task_is_ever_scheduled_before_today(self):
        today = date(2026, 12, 1)
        cs = colleges(("Late Start", "2026-12-20", "committed-to-apply"))
        tasks, _, _ = mt.build_tasks(cs, today, CFG)
        self.assertTrue(all(t["due"] >= today for t in tasks))


class DeadlineParsing(unittest.TestCase):
    def test_blank_deadline_is_tolerated(self):
        for blank in (None, "", "   "):
            meta = {"colleges": [{"name": "TBD U", "deadline": blank}]}
            cs = mt.read_colleges(meta)
            self.assertIsNone(cs[0][1])

    def test_missing_deadline_produces_a_notice_not_silence(self):
        today = date(2026, 9, 15)
        cs = mt.read_colleges({"colleges": [{"name": "TBD U", "deadline": None}]})
        tasks, notices, _ = mt.build_tasks(cs, today, CFG)
        self.assertEqual(tasks, [])
        self.assertTrue(any("no deadline set" in n for n in notices))

    def test_malformed_deadline_is_a_hard_error(self):
        """Silently dropping a school's whole task plan is the dangerous outcome."""
        for bad in ("11/01/2026", "Nov 1", "2026-13-01", "2026-11-31"):
            with self.subTest(bad=bad):
                meta = {"colleges": [{"name": "Typo U", "deadline": bad}]}
                with self.assertRaises(SystemExit) as cm:
                    mt.read_colleges(meta)
                self.assertIn("Typo U", str(cm.exception))


class ConfigContract(unittest.TestCase):
    """The config is editable by hand, so verify the shape the code depends on."""

    def test_backward_plan_has_required_keys_and_a_submit_step(self):
        for step in CFG["backward_plan"]:
            for key in ("weeks_before", "task", "category", "owner"):
                self.assertIn(key, step)
        self.assertEqual(min(s["weeks_before"] for s in CFG["backward_plan"]), 0,
                         "plan needs a step on the deadline itself")

    def test_runway_matches_longest_plan_step(self):
        self.assertEqual(CFG["rules"]["plan_runway_weeks"],
                         max(s["weeks_before"] for s in CFG["backward_plan"]),
                         "compression scales by plan_runway_weeks; a mismatch skews "
                         "every compressed date")

    def test_aid_dates_are_month_day(self):
        for key in ("fafsa_opens", "css_profile_opens", "css_suggested_by"):
            m, d = CFG["aid"][key].split("-")
            date(2026, int(m), int(d))


if __name__ == "__main__":
    unittest.main(verbosity=2)
