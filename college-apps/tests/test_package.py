#!/usr/bin/env python3
"""Tests for the counselor package: draft provenance and content escaping.

The provenance check is an integrity guarantee, not a formatting nicety — it is the only
mechanical thing standing between an agent-written draft and a counselor reading it as
the student's own work. Treat a failure here as a real defect.

Run:  .venv/bin/python -m unittest discover -s tests -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_package as bp  # noqa: E402


class DraftProvenance(unittest.TestCase):
    def test_recognises_each_marker(self):
        cases = [
            ("> **STUDENT DRAFT**\n\nThe shop smelled of oil.", "student"),
            ("> **AGENT FIRST DRAFT — built from your intake.**\n\nText.", "agent"),
            ("> **EXAMPLE — a different student. Do not submit.**\n\nText.", "example"),
        ]
        for text, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(bp.draft_provenance(text)[0], expected)

    def test_unlabeled_draft_is_not_guessed(self):
        self.assertEqual(bp.draft_provenance("The shop smelled of oil.")[0], None)

    def test_marker_must_be_near_the_top(self):
        buried = "\n".join(["filler"] * 20 + ["> **AGENT FIRST DRAFT**"])
        self.assertIsNone(bp.draft_provenance(buried)[0],
                          "a marker buried mid-document isn't a visible declaration")

    def test_agent_marker_wins_over_incidental_student_mention(self):
        text = "> **AGENT FIRST DRAFT — scaffolding.**\n\nThe STUDENT DRAFT process..."
        self.assertEqual(bp.draft_provenance(text)[0], "agent")


class LabelEnforcement(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.sd = Path(self.tmp.name)
        self.essay = self.sd / "essays" / "michigan--why-us"
        self.essay.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_unlabeled_draft_blocks_the_build(self):
        (self.essay / "draft-01.md").write_text("No header here.")
        with self.assertRaises(SystemExit) as cm:
            bp.check_draft_labels(self.sd)
        self.assertIn("draft-01.md", str(cm.exception))

    def test_labeled_drafts_pass(self):
        (self.essay / "draft-01.md").write_text("> **AGENT FIRST DRAFT**\n\nText.")
        (self.essay / "draft-02.md").write_text("> **STUDENT DRAFT**\n\nMy rewrite.")
        bp.check_draft_labels(self.sd)  # must not raise

    def test_every_offender_is_named_not_just_the_first(self):
        (self.essay / "draft-01.md").write_text("bare")
        second = self.sd / "essays" / "rice--community"
        second.mkdir(parents=True)
        (second / "draft-01.md").write_text("also bare")
        with self.assertRaises(SystemExit) as cm:
            bp.check_draft_labels(self.sd)
        msg = str(cm.exception)
        self.assertIn("michigan--why-us", msg)
        self.assertIn("rice--community", msg)

    def test_no_essays_directory_is_fine(self):
        bp.check_draft_labels(Path(self.tmp.name) / "nonexistent")


class ContentEscaping(unittest.TestCase):
    def test_prose_angle_brackets_survive(self):
        out = bp.md("I thought <I could do better> and stopped.")
        self.assertIn("&lt;I could do better&gt;", out)

    def test_script_tags_are_neutralised(self):
        out = bp.md("<script>alert(1)</script>")
        self.assertNotIn("<script>", out)

    def test_markdown_structure_still_renders(self):
        out = bp.md("## Heading\n\n- one\n- two\n")
        self.assertIn("<h2>", out)
        self.assertIn("<li>", out)

    def test_tables_still_render(self):
        out = bp.md("| A | B |\n|---|---|\n| 1 | 2 |\n")
        self.assertIn("<table>", out)


class HeadingDemotion(unittest.TestCase):
    def test_embedded_headings_drop_below_section_level(self):
        self.assertEqual(bp.demote("## Fit\n"), "#### Fit\n")

    def test_never_exceeds_h6(self):
        self.assertEqual(bp.demote("###### Deep\n"), "###### Deep\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TodoDetection(unittest.TestCase):
    """Templates write TODOs both bare and as list items; both must count."""

    def test_counts_bare_and_bulleted_forms(self):
        for line in ("TODO: confirm budget",
                     "- TODO: confirm budget",
                     "  * TODO: confirm budget",
                     "1. TODO: confirm budget"):
            with self.subTest(line=line):
                self.assertEqual(len(bp.TODO_RE.findall(line)), 1)

    def test_does_not_match_prose_mentioning_todo(self):
        self.assertEqual(bp.TODO_RE.findall("we should TODO: nothing here"), [])


class CriteriaSection(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.sd = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_criteria_prompts_rather_than_failing(self):
        out = bp.section_criteria(self.sd)
        self.assertIn("criteria worksheet", out)

    def test_criteria_content_and_open_questions_surface(self):
        (self.sd / "criteria.md").write_text(
            "# List criteria\n\n## Hard filters\n\n"
            "| # | Criterion | Value |\n|---|---|---|\n"
            "| H1 | Net price | under $25k |\n\n"
            "## Open questions\n\n- TODO: confirm car needed\n"
        )
        out = bp.section_criteria(self.sd)
        self.assertIn("under $25k", out)
        self.assertIn("open question(s)", out)


class CheckFlag(unittest.TestCase):
    """--check runs the label gate alone and builds nothing (the essay skill's close)."""

    def test_check_passes_and_writes_no_package(self):
        import subprocess, sys as _sys, tempfile
        from pathlib import Path
        sd = Path(tempfile.mkdtemp()); (sd / "essays" / "x").mkdir(parents=True)
        (sd / "essays" / "x" / "draft-01.md").write_text("> **STUDENT DRAFT**\n\nhello\n")
        r = subprocess.run([_sys.executable, str(Path(__file__).parent.parent / "scripts" / "build_package.py"), str(sd), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("clean", r.stdout)
        self.assertFalse((sd / "out").exists())

    def test_check_fails_on_an_unlabeled_draft(self):
        import subprocess, sys as _sys, tempfile
        from pathlib import Path
        sd = Path(tempfile.mkdtemp()); (sd / "essays" / "x").mkdir(parents=True)
        (sd / "essays" / "x" / "draft-01.md").write_text("hello\n")
        r = subprocess.run([_sys.executable, str(Path(__file__).parent.parent / "scripts" / "build_package.py"), str(sd), "--check"],
                           capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)


class HeaderIsTheFirstLine(unittest.TestCase):
    """A keyword in the opening lines is not a declaration (review M7, 2026-08-22)."""

    def test_for_example_in_a_student_draft_is_not_an_example(self):
        kind, _ = bp.draft_provenance("> **STUDENT DRAFT**\n\nFor example, the first time I …")
        self.assertEqual(kind, "student")

    def test_unlabeled_draft_with_the_word_example_is_unlabeled(self):
        kind, _ = bp.draft_provenance("For example, the first time I …\n\nmore text")
        self.assertIsNone(kind)

    def test_blank_lines_before_the_header_are_fine(self):
        kind, _ = bp.draft_provenance("\n\n> **AGENT FIRST DRAFT — built from …**\n")
        self.assertEqual(kind, "agent")

