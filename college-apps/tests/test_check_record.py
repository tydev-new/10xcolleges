import subprocess, sys, tempfile, unittest
from pathlib import Path

S = Path(__file__).resolve().parent.parent / "scripts" / "check_record.py"
PROFILE = "# Profile\n## Basics\n- **Name:** Maya R. [packet]\n- **GPA (unweighted):** 3.7 [transcript]\n- **Test scores:** none yet; SAT in October [student 2026-08-22]\n- **State of residence:** California [packet]\n## Goals and direction\n- **Intended major:** \"biology maybe, something with plants\" — not sure [student 2026-08-22]\n"
CRITERIA = "# List criteria\n## Hard filters\n| # | Criterion | Value | Source | Added |\n|---|---|---|---|---|\n| H1 | budget | $25k/yr · set by: parent | [parent 2026-08-22] | 2026-08-22 |\n## Deal-breakers\n| # | \"In their words\" | What it rules out | Source | Added |\n|---|---|---|---|---|\n| D1 | \"I don't want to be somewhere cold\" | cold climates | [student 2026-08-22] | 2026-08-22 |\n## Retired criteria\n| # | Criterion | Why it changed | When |\n|---|---|---|---|\n"

def ws(profile=PROFILE, criteria=CRITERIA, conv=None):
    sd = Path(tempfile.mkdtemp()) / "students" / "s"; sd.mkdir(parents=True)
    (sd / "profile.md").write_text(profile); (sd / "criteria.md").write_text(criteria)
    if conv is not None: (sd / "conversations.md").write_text(conv)
    return sd

def run(sd):
    r = subprocess.run([sys.executable, str(S), str(sd)], capture_output=True, text=True)
    return r.returncode, r.stdout

class CheckRecord(unittest.TestCase):
    def test_clean_record_passes_and_gate_is_full(self):
        code, out = run(ws()); self.assertEqual(code, 0, out); self.assertIn("OK", out); self.assertIn("gate 4/4", out)

    def test_material_gate_counts_the_essay_needs(self):
        sd = ws()
        code, out = run(sd); self.assertIn("material 1/3", out)  # direction only
        (sd / "documents").mkdir(); (sd / "documents" / "packet.md").write_text("x")
        (sd / "profile.md").write_text(PROFILE + "## School activities\n| Group | Grades | Hrs/wk | Role | What actually happened |\n|---|---|---|---|---|\n| Robotics | 10-12 | 8 | drivetrain lead | rebuilt the drivetrain four times last season [student 2026-08-22] |\n")
        code, out = run(sd); self.assertEqual(code, 0, out); self.assertIn("material 3/3", out); self.assertIn("the essay can start", out)

    def test_empty_conversations_warns_not_gates(self):
        sd = ws(conv="# Conversations\n")
        code, out = run(sd); self.assertEqual(code, 0); self.assertIn("WARN conversations.md: no dated entry", out)

    def test_documents_none_counts(self):
        sd = ws(profile=PROFILE + "- documents: none [student 2026-08-22]\n")
        code, out = run(sd); self.assertNotIn("documents read", out)

    def test_guessed_budget_counts_zero(self):
        code, out = run(ws(criteria=CRITERIA.replace("$25k/yr · set by: parent", "\"probably like 30k?\" · set by: nobody yet (student's guess)")))
        self.assertEqual(code, 0, out); self.assertIn("gate 3/4", out); self.assertIn("budget", out)

    def test_gpa_without_unweighted_is_not_the_gate(self):
        code, out = run(ws(profile=PROFILE.replace("- **GPA (unweighted):** 3.7 [transcript]", "- **GPA (kind unknown):** \"my GPA is 3.9\" [student 2026-08-22]\n- TODO: unweighted GPA — have them check the transcript")))
        self.assertEqual(code, 0, out); self.assertIn("gate 3/4", out); self.assertIn("unweighted GPA", out)

    def test_missing_state_of_residence_gates(self):
        code, out = run(ws(profile=PROFILE.replace("- **State of residence:** California [packet]\n", "")))
        self.assertEqual(code, 0, out); self.assertIn("gate 3/4", out); self.assertIn("state of residence", out)

    def test_undated_person_tag_fails(self):
        code, out = run(ws(profile=PROFILE + "- works at a garden center [student]\n"))
        self.assertEqual(code, 1); self.assertIn("needs its date", out)

    def test_todo_with_a_hedge_fails(self):
        code, out = run(ws(profile=PROFILE + "- TODO: budget — probably engineering money\n"))
        self.assertEqual(code, 1); self.assertIn("TODO carrying a value", out)

    def test_labelled_todo_with_a_value_fails(self):
        code, out = run(ws(profile=PROFILE + "- **Intended major:** TODO: probably engineering\n- **Class rank:** TODO: 12\n"))
        self.assertEqual(code, 1); self.assertEqual(out.count("TODO carrying a value"), 2, out)

    def test_retired_row_in_template_shape_passes(self):
        code, out = run(ws(criteria=CRITERIA + "| P1 | near a city | \"not IN a city, an hour away is fine\" [student 2026-08-22] | 2026-08-22 |\n"))
        self.assertEqual(code, 0, out)

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
