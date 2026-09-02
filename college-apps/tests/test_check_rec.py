import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "check_rec.py")

VALID_BRAG_SHEET = """# For Ms. Alvarez — AP Physics, Junior Year

## What I'm applying to
- **Intended major:** Mechanical Engineering [student 2026-09-02]
- **Target colleges & earliest deadline:** University of Michigan (EA, Nov 1), Purdue, UIUC [student 2026-09-02]

## What I'd love you to be able to speak to
- **Core qualities:** Intellectual persistence when solving complex problems past the point where it's easy; willingness to support peers collaboratively without being asked.

## Moments from your class you might not remember
- **The rotational motion test recovery:** I scored a 61 on the initial rotational dynamics exam in second semester. Over the next two weeks, I attended four lunch review sessions with you, reworked the university-level problem sets, and earned a 94 on the retest and a 5 on the AP Physics exam.
- **The pendulum lab release mechanism:** When our lab group's timing data was inconsistent due to manual release error, you allowed us to iterate. We designed and built a mechanical release clamp out of a binder clip and dowel, which stabilized our period measurements within 1.5% of theoretical values.
- **Tutoring peers during 5th period study hall:** Starting in January, I worked with Marcus and two other juniors three days a week to review kinematics and energy conservation principles, helping them raise their exam scores.

## Outside your classroom
- **Robotics build lead:** 15 hrs/week in season; rebuilt our team's drivetrain 4 times and trained 6 freshmen on milling tools.
- **Community bike clinic:** Founder of the free public library repair stand, maintaining 20+ neighborhood bikes over two years.

## Logistics & Submission
- **Earliest deadline:** November 1 (Michigan EA)
- **Submission method:** Common App (invitation sent from student email)
- **FERPA status:** Confirmed waived in Common App (right to review recommendations is surrendered)
"""

VALID_REQUEST = """Subject: Thank you — recommendation materials (Jordan Lee, Class of 2027)

Hi Ms. Alvarez,

Thank you for saying yes this morning when we spoke after 4th period — having your support means a great deal to me.

I've attached my brag sheet with a few specific memories from our AP Physics class that might be useful, along with my current transcript and activities list.

My earliest application deadline is **November 1** for the University of Michigan Early Action. I will send the official Common App electronic invitation this afternoon so it is ready in your portal whenever you are able to write.

If it would help to talk through any of these details or my intended engineering path, I am free during 5th period study hall or after school any day this week.

Thank you again for your teaching and guidance.

Sincerely,
Jordan Lee
"""


class TestCheckRec(unittest.TestCase):
    def run_check(self, path):
        r = subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)
        return r.returncode, r.stdout, r.stderr

    def test_valid_brag_sheet_passes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", prefix="brag-sheet--", delete=False) as f:
            f.write(VALID_BRAG_SHEET)
            path = f.name
        try:
            code, out, _ = self.run_check(path)
            self.assertEqual(code, 0, out)
            self.assertIn("OK", out)
        finally:
            os.remove(path)

    def test_missing_section_fails(self):
        # Omit Logistics section
        bad = VALID_BRAG_SHEET.split("## Logistics & Submission")[0]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", prefix="brag-sheet--", delete=False) as f:
            f.write(bad)
            path = f.name
        try:
            code, out, _ = self.run_check(path)
            self.assertEqual(code, 1, out)
            self.assertIn("missing required section '## Logistics'", out)
        finally:
            os.remove(path)

    def test_fewer_than_3_moments_fails(self):
        # Only 2 moments
        lines = [l for l in VALID_BRAG_SHEET.splitlines() if not l.startswith("- **Tutoring peers")]
        bad = "\n".join(lines)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", prefix="brag-sheet--", delete=False) as f:
            f.write(bad)
            path = f.name
        try:
            code, out, _ = self.run_check(path)
            self.assertEqual(code, 1, out)
            self.assertIn("must have at least 3 moments", out)
        finally:
            os.remove(path)

    def test_moment_too_brief_fails(self):
        # Moment with only 4 words
        bad = VALID_BRAG_SHEET.replace(
            "- **Tutoring peers during 5th period study hall:** Starting in January, I worked with Marcus and two other juniors three days a week to review kinematics and energy conservation principles, helping them raise their exam scores.",
            "- **Tutoring:** I helped some students.",
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", prefix="brag-sheet--", delete=False) as f:
            f.write(bad)
            path = f.name
        try:
            code, out, _ = self.run_check(path)
            self.assertEqual(code, 1, out)
            self.assertIn("too brief", out)
        finally:
            os.remove(path)

    def test_missing_intended_major_fails(self):
        bad = VALID_BRAG_SHEET.replace("- **Intended major:** Mechanical Engineering [student 2026-09-02]", "- **Target:** Engineering")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", prefix="brag-sheet--", delete=False) as f:
            f.write(bad)
            path = f.name
        try:
            code, out, _ = self.run_check(path)
            self.assertEqual(code, 1, out)
            self.assertIn("missing or unverified '**Intended major:**'", out)
        finally:
            os.remove(path)

    def test_valid_request_passes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", prefix="request--", delete=False) as f:
            f.write(VALID_REQUEST)
            path = f.name
        try:
            code, out, _ = self.run_check(path)
            self.assertEqual(code, 0, out)
            self.assertIn("OK", out)
        finally:
            os.remove(path)

    def test_request_missing_in_person_ack_fails(self):
        bad = VALID_REQUEST.replace("Thank you for saying yes this morning when we spoke after 4th period — having your support means a great deal to me.", "Please write a letter of recommendation for me.")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", prefix="request--", delete=False) as f:
            f.write(bad)
            path = f.name
        try:
            code, out, _ = self.run_check(path)
            self.assertEqual(code, 1, out)
            self.assertIn("must acknowledge prior in-person agreement", out)
        finally:
            os.remove(path)

    def test_directory_scan_passes(self):
        with tempfile.TemporaryDirectory() as td:
            recs_dir = os.path.join(td, "recs")
            os.makedirs(recs_dir)
            with open(os.path.join(recs_dir, "brag-sheet--alvarez.md"), "w") as f:
                f.write(VALID_BRAG_SHEET)
            with open(os.path.join(recs_dir, "request--alvarez.md"), "w") as f:
                f.write(VALID_REQUEST)
            code, out, _ = self.run_check(td)
            self.assertEqual(code, 0, out)
            self.assertIn("OK", out)


if __name__ == "__main__":
    unittest.main()
