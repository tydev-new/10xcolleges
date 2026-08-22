"""scripts/check_draft.py — the essay law's checkable half."""
import os, subprocess, sys, tempfile, unittest
from pathlib import Path
S = Path(__file__).resolve().parent.parent / "scripts" / "check_draft.py"
HDR = "> **AGENT FIRST DRAFT — built from your intake and our conversations. This is scaffolding, not your essay. Rewrite it in your own words before it goes anywhere near an application. Check every fact: if I got something wrong or put words in your mouth, say so and I'll cut it.**\n\n"

def ws(drafts, profile="- Robotics team; drivetrain lead [packet]\n- Bike shop summers [student]\n", research=None):
    sd = Path(tempfile.mkdtemp()) / "students" / "s"; e = sd / "essays" / "x"; e.mkdir(parents=True)
    (sd / "profile.md").write_text(profile); (sd / "conversations.md").write_text("- 'I fix flats' [student]\n")
    if research:
        (sd / "research").mkdir(); (sd / "research" / "pomona.md").write_text(research)
    for i, t in enumerate(drafts, 1):
        (e / f"draft-{i:02d}.md").write_text(t)
    return sd

def run(sd, *args):
    r = subprocess.run([sys.executable, str(S), str(sd), *args], capture_output=True, text=True)
    return r.returncode, r.stdout

class CheckDraft(unittest.TestCase):
    def test_clean_agent_draft_from_the_record(self):
        code, out = run(ws([HDR + "On the robotics team I was the drivetrain lead. I fix flats at the bike shop.\n"]))
        self.assertEqual(code, 0, out); self.assertIn("clean", out)

    def test_invented_name_and_number_fail(self):
        code, out = run(ws([HDR + "Pomona's Estella Laboratory, where I'd spend 4 years.\n"]))
        self.assertEqual(code, 1); self.assertIn("Estella", out); self.assertIn("'4'", out)

    def test_a_college_fact_with_a_research_file_passes(self):
        code, out = run(ws([HDR + "Pomona's Estella Laboratory machine shop.\n"], research="Estella Laboratory — student machine shop (pomona.edu, 2026-08-10)\n"))
        self.assertEqual(code, 0, out)

    def test_student_draft_only_warns_on_specifics(self):
        sd = ws(["> **STUDENT DRAFT**\n\nMy cousin Teresa taught me.\n"])
        (sd / "essays" / "x" / "review-01.md").write_text("## Against the brief — 2/5\n## The one big thing\nx\n## One question\ny\n")
        code, out = run(sd)
        self.assertEqual(code, 0); self.assertIn("WARN", out); self.assertIn("Teresa", out)

    def test_student_draft_without_its_review_fails(self):
        code, out = run(ws(["> **STUDENT DRAFT**\n\nI fix flats.\n"]))
        self.assertEqual(code, 1); self.assertIn("no review-01.md", out)

    def test_review_missing_the_count_fails(self):
        sd = ws(["> **STUDENT DRAFT**\n\nI fix flats.\n"])
        (sd / "essays" / "x" / "review-01.md").write_text("nice essay, one big thing: more detail. question: why?\n")
        code, out = run(sd)
        self.assertEqual(code, 1); self.assertIn("N/M", out)

    def test_missing_header_fails(self):
        code, out = run(ws(["Just text.\n"]))
        self.assertEqual(code, 1); self.assertIn("no author header", out)

if __name__ == "__main__":
    unittest.main()
