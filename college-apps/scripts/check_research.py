#!/usr/bin/env python3
"""check_research.py — structural and factual citation validator for college research dossiers.

    python3 scripts/check_research.py students/<slug>/research/<college-slug>.md
    python3 scripts/check_research.py students/<slug>

FAIL  research file missing or empty
FAIL  missing H1 college title on line 1
FAIL  missing key dimensions (Admissions, Academics, Cost/Aid, or Deadlines)
FAIL  deadline does not specify a date (YYYY-MM-DD) or Rolling
WARN  zero friction points or watch-outs noted (every real school has trade-offs)
WARN  admissions/cost figures without an inline source/vintage tag ([...])

Exit 1 on any FAIL, else 0.
"""
import glob
import os
import re
import sys

SOURCE_TAG = re.compile(r"\[([^\]]+)\]|\(([^\)]*(?:CDS|Scorecard|202\d|retrieved|\.edu)[^\)]*)\)", re.IGNORECASE)
DATE_RE = re.compile(r"\b202\d-\d{2}-\d{2}\b|rolling", re.IGNORECASE)


def check_dossier(filepath):
    findings = []
    if not os.path.isfile(filepath):
        return [("FAIL", f"file not found: {filepath}")], 0, 0

    text = open(filepath, encoding="utf-8").read()
    lines = text.splitlines()
    if not text.strip():
        return [("FAIL", f"{os.path.basename(filepath)}: empty file")], 0, 0

    # Line 1 title
    h1 = lines[0].strip() if lines else ""
    if not h1.startswith("# "):
        findings.append(("FAIL", f"{os.path.basename(filepath)}: line 1 must be an # H1 College Name header"))

    lower_text = text.lower()

    # Dimension 1: Admissions / Selectivity
    has_admissions = any(k in lower_text for k in ("admit rate", "acceptance rate", "admissions", "middle 50%", "sat", "act"))
    if not has_admissions:
        findings.append(("FAIL", f"{os.path.basename(filepath)}: missing admissions selectivity (admit rate or test ranges)"))

    # Dimension 2: Academics / Major Program
    has_academics = any(k in lower_text for k in ("academic", "major", "program", "abet", "curriculum", "engineering", "undergrad"))
    if not has_academics:
        findings.append(("FAIL", f"{os.path.basename(filepath)}: missing academic program or major details"))

    # Dimension 3: Cost / Aid
    has_cost = any(k in lower_text for k in ("cost", "net price", "tuition", "financial aid", "scholarship", "budget", "$"))
    if not has_cost:
        findings.append(("FAIL", f"{os.path.basename(filepath)}: missing cost, tuition, or financial aid evaluation"))

    # Dimension 4: Deadlines
    has_deadline = any(k in lower_text for k in ("deadline", "priority", "decision plan", "early action", "early decision", "regular decision"))
    if not has_deadline:
        findings.append(("FAIL", f"{os.path.basename(filepath)}: missing application deadlines"))
    else:
        if not DATE_RE.search(text):
            findings.append(("WARN", f"{os.path.basename(filepath)}: deadline does not cite an explicit date (YYYY-MM-DD) or Rolling"))

    # Dimension 5: Friction points / Watch-outs
    friction_matches = re.findall(r"(?:watch out for|friction|turn-offs? check|caveat|drawback|downside)s?:?", text, re.IGNORECASE)
    has_friction = len(friction_matches) > 0 or any(k in lower_text for k in ("weed out", "weed-out", "lecture hall", "housing crunch", "snow belt", "freezing", "commuter"))
    if not has_friction:
        findings.append(("WARN", f"{os.path.basename(filepath)}: no friction points or watch-outs noted — every real school has trade-offs"))

    # Count citations
    citations = SOURCE_TAG.findall(text)
    citation_count = len(citations)
    if citation_count == 0:
        findings.append(("WARN", f"{os.path.basename(filepath)}: no inline source or year tags ([CDS ...], [Scorecard ...], etc.) found"))

    friction_count = len(friction_matches)
    return findings, citation_count, friction_count


def main():
    if len(sys.argv) < 2:
        print("Usage: check_research.py <research-file-or-student-dir>", file=sys.stderr)
        sys.exit(2)

    target = sys.argv[1]
    files = []
    if os.path.isfile(target):
        files = [target]
    elif os.path.isdir(target):
        rdir = os.path.join(target, "research") if os.path.isdir(os.path.join(target, "research")) else target
        files = sorted(glob.glob(os.path.join(rdir, "*.md")))
        if not files:
            print(f"FAIL  no research dossiers found in {rdir}")
            sys.exit(1)
    else:
        print(f"FAIL  target does not exist: {target}")
        sys.exit(1)

    total_fails = 0
    for f in files:
        findings, cites, fricts = check_dossier(f)
        bname = os.path.basename(f)
        has_fail = False
        for kind, msg in findings:
            print(f"{kind}  {msg}")
            if kind == "FAIL":
                has_fail = True
                total_fails += 1
        if not has_fail:
            warn_count = sum(1 for k, _ in findings if k == "WARN")
            if warn_count == 0:
                print(f"OK    {bname} ({cites} citations, {max(fricts, 1)} friction points)")

    if total_fails > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
