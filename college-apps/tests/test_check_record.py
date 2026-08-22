import subprocess, sys, tempfile, unittest
from pathlib import Path

S = Path(__file__).resolve().parent.parent / "scripts" / "check_record.py"
PROFILE = "# Profile\n## 1. Basics\n- **Name:** Maya R. [packet]\n- **GPA (unweighted):** 3.7 [transcript]\n- TODO: test scores\n"
CRITERIA = "# List criteria\n## Hard filters\n| # | Criterion | Value | Source | Added |\n|---|---|---|---|---|\n| H1 | budget | $25k/yr · set by: parent | [parent 2026-08-22] | 2026-08-22 |\n## Retired criteria\n| # | Criterion | Retired | Why |\n|---|---|---|---|\n"

def ws(profile=PROFILE, criteria=CRITERIA, conv=None):
    sd = Path(tempfile.mkdtemp()) / "students" / "s"; sd.mkdir(parents=True)
    (sd / "profile.md").write_text(profile); (sd / "criteria.md").write_text(criteria)
    if conv is not None: (sd / "conversations.md").write_text(conv)
    return sd

def run(sd):
    r = subprocess.run([sys.executable, str(S), str(sd)], capture_output=True, text=True)
    return r.returncode, r.stdout

class CheckRecord(unittest.TestCase):
    def test_clean_record_passes(self):
        code, out = run(ws()); self.assertEqual(code, 0, out); self.assertIn("OK", out)

    def test_untagged_line_fails(self):
        code, out = run(ws(profile=PROFILE + "- Robotics team, 3 years\n"))
        self.assertEqual(code, 1); self.assertIn("no source tag", out)

    def test_untagged_table_row_fails(self):
        code, out = run(ws(criteria=CRITERIA.replace("| [parent 2026-08-22] |", "| |")))
        self.assertEqual(code, 1); self.assertIn("no source tag", out)

    def test_template_empty_row_is_not_a_claim(self):
        code, out = run(ws(criteria=CRITERIA + "## Preferences\n| # | Criterion | Weight | Source | Added |\n|---|---|---|---|---|\n| P1 | | | | |\n"))
        self.assertEqual(code, 0, out)

    def test_todo_with_a_value_fails(self):
        code, out = run(ws(profile=PROFILE + "- TODO: budget $30k\n"))
        self.assertEqual(code, 1); self.assertIn("TODO carrying a value", out)

    def test_todo_with_what_to_ask_passes(self):
        code, out = run(ws(profile=PROFILE + "- TODO: unweighted GPA — ask them to check the transcript\n"))
        self.assertEqual(code, 0, out)

    def test_gpa_without_unweighted_warns(self):
        code, out = run(ws(profile=PROFILE.replace("GPA (unweighted)", "GPA")))
        self.assertEqual(code, 0); self.assertIn("WARN", out); self.assertIn("unweighted", out)

    def test_budget_without_set_by_warns(self):
        code, out = run(ws(criteria=CRITERIA.replace(" · set by: parent", "")))
        self.assertEqual(code, 0); self.assertIn("set by", out)

    def test_conversations_going_backwards_fails(self):
        code, out = run(ws(conv="## 2026-08-22 — intake\n- \"x\" [student]\n## 2026-08-02 — earlier\n- \"y\" [student]\n"))
        self.assertEqual(code, 1); self.assertIn("backwards", out)

if __name__ == "__main__":
    unittest.main()
