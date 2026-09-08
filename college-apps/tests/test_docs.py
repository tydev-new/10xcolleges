#!/usr/bin/env python3
"""Keep the data contract honest.

A design doc that nothing checks will drift the first time the code changes, and a stale
contract is worse than none — it looks authoritative while lying. These tests bind
`docs/data-model.md` to what the repo actually ships and what the scripts actually write.

Run:  python3 -m unittest discover -s tests -v
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

DATA_MODEL = (ROOT / "docs" / "data-model.md").read_text()
DESIGN = (ROOT / "docs" / "design.md").read_text()

# The region declaring per-file mutability: the two "Every file" tables. Other tables in
# the doc (e.g. what the package reads) use column 2 for prose, not a class.
_start = DATA_MODEL.index("## Every file")
_end = DATA_MODEL.index("### brief.md is deliberately split")
CONTRACT = DATA_MODEL[_start:_end]

# First cell of every contract row, when it's a `backticked/path`.
TABLE_PATHS = set(re.findall(r"^\|\s*`([^`]+)`\s*\|", CONTRACT, re.M))

VALID_CLASSES = {"Append-only", "Immutable", "Fixed-source", "Living", "Index", "Derived",
                 "Split"}


class ContractCoversWhatWeShip(unittest.TestCase):
    def test_every_template_file_is_in_the_contract(self):
        """A file students receive but the contract omits has undefined mutability."""
        template = ROOT / "templates" / "student"
        shipped = {
            p.name for p in template.iterdir()
            if p.is_file() and p.suffix in (".md", ".json")
        }
        missing = [f for f in shipped if f not in TABLE_PATHS]
        self.assertEqual(missing, [],
                         f"template ships {missing} but data-model.md doesn't list them")

    def test_generated_outputs_are_in_the_contract(self):
        for out in ("out/tracker.xlsx", "out/packet.docx"):
            self.assertIn(out, TABLE_PATHS, f"{out} missing from the contract")
        self.assertTrue(
            any(p.startswith("out/package.") for p in TABLE_PATHS),
            "the counselor package output is missing from the contract",
        )

    def test_index_files_are_listed(self):
        for f in ("meta.json", "packet.json"):
            self.assertIn(f, TABLE_PATHS)

    def test_only_known_mutability_classes_are_used(self):
        """Catches a typo'd or invented class in the table."""
        rows = re.findall(r"^\|\s*`[^`]+`\s*\|\s*\*{0,2}([A-Za-z-]+)", CONTRACT, re.M)
        unknown = sorted({c for c in rows if c not in VALID_CLASSES})
        self.assertEqual(unknown, [], f"unknown mutability class(es): {unknown}")


class ContractMatchesCode(unittest.TestCase):
    def test_derived_outputs_match_the_scripts_defaults(self):
        """If a script's default output path moves, the contract must move with it."""
        for script, expected in [
            ("make_tracker.py", "tracker.xlsx"),
            ("fill_packet.py", "packet.docx"),
            ("build_package.py", "package.html"),
        ]:
            src = (ROOT / "scripts" / script).read_text()
            self.assertIn(expected, src, f"{script} no longer writes {expected}")
            self.assertTrue(any(expected in p for p in TABLE_PATHS),
                            f"{expected} written by {script} but absent from the contract")

    def test_config_path_referenced_by_docs_exists(self):
        self.assertTrue((ROOT / "config" / "calendar.json").exists())
        self.assertIn("config/calendar.json", DATA_MODEL)

    def test_docs_referenced_by_design_all_exist(self):
        for name in re.findall(r"`((?:docs/)?[a-z-]+\.md)`", DESIGN):
            base = name.split("/")[-1]
            if base in ("data-model.md", "citations.md", "voice.md", "design.md"):
                self.assertTrue((ROOT / "docs" / base).exists(), f"missing docs/{base}")


class SkillsAndDocsAgree(unittest.TestCase):
    def test_every_skill_in_the_component_diagram_exists(self):
        skills = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        for name in skills:
            self.assertIn(name, DESIGN,
                          f"skill '{name}' is not shown anywhere in design.md")

    def test_design_names_no_skill_that_does_not_exist(self):
        skills = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        # Skill-shaped tokens used in the diagrams and routing prose.
        named = set(re.findall(r"\b(college-app|college-list|college-research|"
                               r"student-intake|essay-coach|rec-request|app-tracker|"
                               r"counselor-package|financial-aid|major-fit)\b", DESIGN))
        self.assertEqual(named - skills, set(),
                         "design.md references skills that don't exist")

    def test_enforced_invariants_table_matches_reality(self):
        """Anything the design doc claims is code-enforced must actually be in code."""
        bp = (ROOT / "scripts" / "build_package.py").read_text()
        mt = (ROOT / "scripts" / "make_tracker.py").read_text()
        sc = (ROOT / "scripts" / "scorecard.py").read_text()
        self.assertIn("check_draft_labels", bp, "draft-label enforcement claimed, absent")
        self.assertIn("Unparseable deadline", mt, "deadline enforcement claimed, absent")
        self.assertIn("no Scorecard match for UNITID", sc, "batch warning claimed, absent")
        self.assertIn("mixes field years", sc, "vintage-mismatch flag claimed, absent")


class FencesAreBalanced(unittest.TestCase):
    def test_code_fences_close(self):
        """An unbalanced fence swallows the rest of the document when rendered."""
        for doc in (ROOT / "docs").glob("*.md"):
            with self.subTest(doc=doc.name):
                self.assertEqual(doc.read_text().count("```") % 2, 0,
                                 f"{doc.name} has an unclosed code fence")


if __name__ == "__main__":
    unittest.main(verbosity=2)
