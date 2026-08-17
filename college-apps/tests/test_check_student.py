#!/usr/bin/env python3
"""Tests for the workspace contract checker.

check_student.py is the code half of docs/data-model.md — the rows of the enforcement
table that moved up from discipline. Each test plants a workspace defect the contract
names and asserts the checker sees it. The clean-workspace case runs against the shipped
template itself, so the template can never drift out of contract without a test failing.

Run:  python3 -m unittest discover -s tests -v
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_student as cs  # noqa: E402

META = {
    "slug": "test-student", "name": "Test Student", "grad_year": 2027,
    "high_school": "", "updated": "2026-08-17",
    "colleges": [], "recommenders": [], "key_dates": [],
}


class Workspace(unittest.TestCase):
    """Shared scaffold: a student folder copied from the shipped template."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.sd = Path(self.tmp.name) / "test-student"
        shutil.copytree(ROOT / "templates" / "student", self.sd)
        (self.sd / "meta.json").write_text(json.dumps(META))

    def tearDown(self):
        self.tmp.cleanup()

    def fails(self):
        return cs.check(self.sd)[0]

    def warns(self):
        return cs.check(self.sd)[1]


class CleanTemplate(Workspace):
    def test_fresh_scaffold_passes_with_no_warnings(self):
        fails, warns = cs.check(self.sd)
        self.assertEqual(fails, [])
        self.assertEqual(warns, [])


class ProfileSchema(Workspace):
    def test_missing_profile_fails(self):
        (self.sd / "profile.md").unlink()
        self.assertTrue(any("profile.md is missing" in f for f in self.fails()))

    def test_removed_section_fails(self):
        p = self.sd / "profile.md"
        p.write_text(p.read_text().replace("## Constraints", "## Limits"))
        fails = self.fails()
        self.assertTrue(any("'## Constraints'" in f for f in fails))

    def test_extra_section_warns_not_fails(self):
        p = self.sd / "profile.md"
        p.write_text(p.read_text() + "\n## Vibes\n\nchill\n")
        self.assertEqual(self.fails(), [])
        self.assertTrue(any("'## Vibes'" in w for w in self.warns()))

    def test_schema_comes_from_the_template(self):
        # The single-owner rule: the checker's required list IS the template's headings.
        tpl = (ROOT / "templates" / "student" / "profile.md").read_text()
        for section in cs.required_profile_sections():
            self.assertIn(f"## {section}", tpl)


class DraftProvenance(Workspace):
    def _draft(self, text):
        d = self.sd / "essays" / "michigan--why-us"
        d.mkdir(parents=True, exist_ok=True)
        (d / "draft-01.md").write_text(text)

    def test_unlabeled_draft_fails(self):
        self._draft("The shop smelled of cutting oil.")
        self.assertTrue(any("no provenance header" in f for f in self.fails()))

    def test_labeled_draft_passes(self):
        self._draft("> **STUDENT DRAFT**\n\nThe shop smelled of cutting oil.")
        self.assertEqual(self.fails(), [])


class MetaSync(Workspace):
    def _meta_college(self, name="University of Michigan", tier="target", **kw):
        meta = dict(META)
        meta["colleges"] = [dict(name=name, tier=tier, status="researching", **kw)]
        (self.sd / "meta.json").write_text(json.dumps(meta))

    def _list_college(self, heading="## University of Michigan — Target"):
        p = self.sd / "colleges.md"
        p.write_text(p.read_text() + f"\n{heading}\n\n**Why it's here:** fit.\n")

    def test_in_sync_passes(self):
        self._meta_college()
        self._list_college()
        self.assertEqual(self.fails(), [])

    def test_meta_only_college_fails(self):
        self._meta_college()
        self.assertTrue(any("not in colleges.md" in f for f in self.fails()))

    def test_list_only_college_fails(self):
        self._list_college()
        self.assertTrue(any("not in meta.json" in f for f in self.fails()))

    def test_tier_mismatch_fails(self):
        self._meta_college(tier="safety")
        self._list_college("## University of Michigan — Target")
        self.assertTrue(any("tier 'safety'" in f and "'target'" in f
                            for f in self.fails()))

    def test_unknown_tier_fails(self):
        self._meta_college(tier="likely")
        self._list_college("## University of Michigan — Target")
        self.assertTrue(any("tier 'likely'" in f for f in self.fails()))

    def test_unknown_status_fails(self):
        meta = dict(META)
        meta["colleges"] = [{"name": "U", "tier": "target", "status": "vibing"}]
        (self.sd / "meta.json").write_text(json.dumps(meta))
        self.assertTrue(any("status 'vibing'" in f for f in self.fails()))

    def test_unparseable_meta_fails(self):
        (self.sd / "meta.json").write_text("{not json")
        self.assertTrue(any("does not parse" in f for f in self.fails()))

    def test_missing_meta_with_populated_list_fails(self):
        # The maximal desync: index deleted, list full — must not pass clean.
        (self.sd / "meta.json").unlink()
        self._list_college()
        self.assertTrue(any("meta.json is missing" in f for f in self.fails()))

    def test_duplicate_list_entries_fail(self):
        self._meta_college()
        self._list_college("## University of Michigan — Target")
        self._list_college("## University of Michigan — Reach")
        self.assertTrue(any("more than once" in f for f in self.fails()))

    def test_duplicate_meta_entries_fail(self):
        meta = dict(META)
        meta["colleges"] = [
            {"name": "University of Michigan", "tier": "target", "status": "researching"},
            {"name": "university of michigan", "tier": "reach", "status": "researching"},
        ]
        (self.sd / "meta.json").write_text(json.dumps(meta))
        self._list_college()
        self.assertTrue(any("more than once" in f for f in self.fails()))

    def test_off_format_heading_fails_naming_the_format(self):
        # A heading the regex can't parse must be reported as a format problem,
        # not as a phantom "not in colleges.md" mismatch pointing at meta.json.
        self._meta_college()
        self._list_college("## University of Michigan — Target (EA)")
        self.assertTrue(any("doesn't match the format" in f for f in self.fails()))

    def test_endash_in_school_name_parses(self):
        self._meta_college(name="University of Wisconsin–Madison")
        self._list_college("## University of Wisconsin–Madison — Target")
        self.assertEqual(self.fails(), [])


class Manifest(Workspace):
    def test_stray_markdown_warns(self):
        (self.sd / "colleges-v2.md").write_text("# a second list")
        self.assertTrue(any("colleges-v2.md" in w for w in self.warns()))

    def test_nested_copy_of_contract_name_warns(self):
        # Path.match is right-anchored; a naive matcher accepts backup/profile.md
        # as profile.md — the exact second-source-of-truth this check exists for.
        (self.sd / "backup").mkdir()
        (self.sd / "backup" / "profile.md").write_text("# old profile")
        self.assertTrue(any("backup/profile.md" in w for w in self.warns()))

    def test_draft_outside_essays_warns(self):
        d = self.sd / "drafts" / "essays" / "michigan--why-us"
        d.mkdir(parents=True)
        (d / "draft-01.md").write_text("unlabeled")
        self.assertTrue(any("drafts/essays" in w for w in self.warns()))

    def test_nested_out_files_are_never_stray(self):
        (self.sd / "out" / "assets").mkdir(parents=True)
        (self.sd / "out" / "assets" / "chart.png").write_text("")
        self.assertEqual(self.warns(), [])

    def test_contract_files_do_not_warn(self):
        (self.sd / "counselor-questions.md").write_text("# Questions")
        (self.sd / "research").mkdir(exist_ok=True)
        (self.sd / "research" / "michigan.md").write_text("# Michigan")
        (self.sd / "recs").mkdir(exist_ok=True)
        (self.sd / "recs" / "brag-sheet--ms-alvarez.md").write_text("# Brag")
        (self.sd / "out").mkdir(exist_ok=True)
        (self.sd / "out" / "tracker.xlsx").write_text("")
        self.assertEqual(self.warns(), [])

    def test_derived_out_dir_is_never_stray(self):
        (self.sd / "out").mkdir(exist_ok=True)
        (self.sd / "out" / "package.pdf").write_text("")
        self.assertEqual(self.warns(), [])


class DatedEntries(Workspace):
    def test_undated_entry_warns(self):
        p = self.sd / "conversations.md"
        p.write_text(p.read_text() + "\n## first chat\n\n\"quote\"\n")
        self.assertTrue(any("no ISO date" in w for w in self.warns()))

    def test_dated_entry_passes(self):
        p = self.sd / "feedback.md"
        p.write_text(p.read_text() + "\n## 2026-09-02 — Mr. Reyes\n\n\"quote\"\n")
        self.assertEqual(self.warns(), [])


if __name__ == "__main__":
    unittest.main()
