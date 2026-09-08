#!/usr/bin/env python3
"""check_major.py — validates students/<slug>/academic-direction.md.

Usage:
    python3 scripts/check_major.py students/<slug>/academic-direction.md

Checks:
    FAIL  file missing or empty
    FAIL  missing any of the 5 required H2 sections
    FAIL  primary intended major missing or blank
    FAIL  adjacent majors table has fewer than 2 rows
    FAIL  content line without a valid source tag
    FAIL  institutional admissions reality has no transfer or direct-admit note
    FAIL  intellectual red thread is missing or empty
"""
import os
import re
import sys

TAG = re.compile(r"\[(packet|transcript|worksheet|(?:student|parent|counselor) \d{4}-\d{2}-\d{2})\]")

REQUIRED_SECTIONS = [
    "overview & primary direction",
    "coursework stamina & transcript evidence",
    "high-leverage adjacent majors",
    "institutional admissions reality",
    "intellectual red thread",
]


def check(path):
    findings = []
    if not os.path.isfile(path):
        return [("FAIL", f"{path}: file does not exist")]

    text = open(path, encoding="utf-8").read()
    if not text.strip():
        return [("FAIL", f"{path}: file is empty")]

    # Check sections
    h2_matches = re.findall(r"^##\s+([^\n]+)", text, re.M)
    lower_h2 = [h.strip().lower() for h in h2_matches]

    for req in REQUIRED_SECTIONS:
        if not any(req in h for h in lower_h2):
            findings.append(("FAIL", f"missing required section: '## {req.title()}'"))

    # Check primary major
    m_major = re.search(r"\*\*Primary intended major:\*\*\s*(.+)", text, re.I)
    if not m_major or not m_major.group(1).strip() or "TODO:" in m_major.group(1):
        findings.append(("FAIL", "missing or unverified '**Primary intended major:**'"))

    # Check adjacent majors table
    sec_adj = re.search(r"##\s+High-Leverage Adjacent Majors(.*?)(?=^## |\Z)", text, re.S | re.M | re.I)
    if sec_adj:
        table_lines = [l.strip() for l in sec_adj.group(1).splitlines() if l.strip().startswith("|")]
        data_rows = [l for l in table_lines if not re.match(r"^\|(\s*:?-+:?\s*\|)+$", l) and not "Adjacent Major" in l]
        if len(data_rows) < 2:
            findings.append(("FAIL", f"adjacent majors table must contain at least 2 options (found {len(data_rows)})"))
    else:
        findings.append(("FAIL", "missing '## High-Leverage Adjacent Majors' section"))

    # Check source tags on content bullets
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#") or s == "---":
            continue
        if s.startswith("|"):
            continue  # table rows have columns
        if s.startswith("-") or s.startswith("*"):
            body = s.lstrip("-* ").strip()
            if not TAG.search(s) and not "TODO:" in body:
                findings.append(("FAIL", f"line {n}: no source tag — [transcript], [packet], or [student YYYY-MM-DD]: `{s[:80]}`"))

    # Check institutional transfer warnings
    sec_inst = re.search(r"##\s+Institutional Admissions Reality(.*?)(?=^## |\Z)", text, re.S | re.M | re.I)
    if sec_inst:
        body = sec_inst.group(1).lower()
        if not any(w in body for w in ("transfer", "direct-admit", "gate", "pool", "arts & sciences", "un-siloed", "lockout")):
            findings.append(("WARN", "institutional admissions reality should note direct-admit or transfer lockout gates"))
    else:
        findings.append(("FAIL", "missing '## Institutional Admissions Reality' section"))

    # Check intellectual red thread
    sec_thread = re.search(r"##\s+Intellectual Red Thread(.*?)(?=^## |\Z)", text, re.S | re.M | re.I)
    if sec_thread:
        bullets = [l for l in sec_thread.group(1).splitlines() if l.strip().startswith(("-", "*"))]
        if len(bullets) < 2:
            findings.append(("FAIL", "intellectual red thread must contain at least 2 hooks (e.g. The Spark, The Friction, The Open Question)"))

    return findings


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)

    path = sys.argv[1]
    findings = check(path)
    for level, msg in findings:
        print(f"{level} {msg}")

    if not any(level == "FAIL" for level, _ in findings):
        if not findings:
            print("OK")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
