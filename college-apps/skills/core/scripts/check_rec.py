#!/usr/bin/env python3
"""check_rec.py — validates brag-sheet--<teacher>.md and request--<teacher>.md files.

Usage:
    python3 scripts/check_rec.py students/<slug>/recs/brag-sheet--<teacher>.md
    python3 scripts/check_rec.py students/<slug>/recs/request--<teacher>.md
    python3 scripts/check_rec.py students/<slug>/recs/
    python3 scripts/check_rec.py students/<slug>

Checks for brag-sheet:
    FAIL  file missing or empty
    FAIL  missing any required H2 section
    FAIL  intended major missing or unverified
    FAIL  moments section contains fewer than 3 bullet points
    FAIL  any classroom moment has fewer than 15 words
    FAIL  earliest deadline missing
    WARN  FERPA waiver status unconfirmed

Checks for request:
    FAIL  file missing or empty
    FAIL  missing Subject: line
    FAIL  missing in-person agreement acknowledgment
    FAIL  missing deadline mention
    FAIL  missing submission method / Common App mention

Exit 1 on any FAIL, else 0.
"""
import os
import re
import sys

REQUIRED_BRAG_SECTIONS = [
    "what i'm applying to",
    "what i'd love you to be able to speak to",
    "moments from your class",
    "outside your classroom",
    "logistics",
]

DATE_PATTERN = re.compile(
    r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
    r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}\b|"
    r"\b\d{4}-\d{2}-\d{2}\b",
    re.I,
)


def check_brag_sheet(path):
    findings = []
    if not os.path.isfile(path):
        return [("FAIL", f"{path}: file does not exist")]

    text = open(path, encoding="utf-8").read()
    if not text.strip():
        return [("FAIL", f"{path}: file is empty")]

    # Check required H2 sections
    h2_matches = re.findall(r"^##\s+([^\n]+)", text, re.M)
    lower_h2 = [h.strip().lower() for h in h2_matches]

    for req in REQUIRED_BRAG_SECTIONS:
        if not any(req in h for h in lower_h2):
            findings.append(("FAIL", f"{os.path.basename(path)}: missing required section '## {req.title()}'"))

    # Check intended major
    m_major = re.search(r"\*\*Intended major:\*\*\s*(.+)", text, re.I)
    if not m_major or not m_major.group(1).strip() or "TODO:" in m_major.group(1):
        findings.append(("FAIL", f"{os.path.basename(path)}: missing or unverified '**Intended major:**'"))

    # Check earliest deadline
    if not DATE_PATTERN.search(text):
        findings.append(("FAIL", f"{os.path.basename(path)}: missing earliest deadline date (e.g. 'Nov 1' or 'YYYY-MM-DD')"))

    # Check classroom moments
    sec_moments = re.search(r"##\s+Moments from your class.*?(?=^## |\Z)", text, re.S | re.M | re.I)
    if sec_moments:
        # Extract bullet items under moments
        raw_bullets = [
            l.strip()
            for l in sec_moments.group(0).splitlines()
            if l.strip().startswith("-") or l.strip().startswith("*")
        ]
        if len(raw_bullets) < 3:
            findings.append(
                ("FAIL", f"{os.path.basename(path)}: 'Moments from your class' must have at least 3 moments (found {len(raw_bullets)})")
            )
        for i, bullet in enumerate(raw_bullets, 1):
            words = re.findall(r"\b[A-Za-z0-9'-]+\b", bullet)
            if len(words) < 15:
                findings.append(
                    ("FAIL", f"{os.path.basename(path)}: classroom moment #{i} is too brief ({len(words)} words; min 15 required for concrete evidence)")
                )
    else:
        findings.append(("FAIL", f"{os.path.basename(path)}: missing 'Moments from your class' section"))

    # Check FERPA status
    sec_logistics = re.search(r"##\s+Logistics.*?(?=^## |\Z)", text, re.S | re.M | re.I)
    if sec_logistics:
        if not re.search(r"FERPA", sec_logistics.group(0), re.I):
            findings.append(("WARN", f"{os.path.basename(path)}: FERPA waiver status not mentioned in Logistics section"))
    else:
        findings.append(("WARN", f"{os.path.basename(path)}: missing Logistics section for FERPA and submission details"))

    return findings


def check_request(path):
    findings = []
    if not os.path.isfile(path):
        return [("FAIL", f"{path}: file does not exist")]

    text = open(path, encoding="utf-8").read()
    if not text.strip():
        return [("FAIL", f"{path}: file is empty")]

    # Check Subject line
    if not re.search(r"^Subject:\s*\S+", text, re.M | re.I):
        findings.append(("FAIL", f"{os.path.basename(path)}: missing 'Subject:' line"))

    # Check in-person acknowledgment
    in_person_keywords = re.search(
        r"\b(saying yes|spoke|spoke with you|talked|met with you|after class|this morning|yesterday|in person|agreed to write)\b",
        text,
        re.I,
    )
    if not in_person_keywords:
        findings.append(
            ("FAIL", f"{os.path.basename(path)}: request must acknowledge prior in-person agreement (e.g. 'Thank you for saying yes this morning...')")
        )

    # Check earliest deadline
    if not DATE_PATTERN.search(text):
        findings.append(("FAIL", f"{os.path.basename(path)}: missing earliest deadline date in request letter"))

    # Check submission method
    if not re.search(r"\b(Common App|Coalition|portal|electronic invitation|invite)\b", text, re.I):
        findings.append(("FAIL", f"{os.path.basename(path)}: missing submission portal notice (e.g. Common App invitation)"))

    return findings


def check_path(target):
    findings = []
    if os.path.isdir(target):
        recs_dir = os.path.join(target, "recs") if os.path.isdir(os.path.join(target, "recs")) else target
        files = [f for f in os.listdir(recs_dir) if f.endswith(".md")]
        if not files:
            return [("WARN", f"no recommendation files found in {recs_dir}")]
        for f in sorted(files):
            p = os.path.join(recs_dir, f)
            if f.startswith("brag-sheet--"):
                findings.extend(check_brag_sheet(p))
            elif f.startswith("request--"):
                findings.extend(check_request(p))
    elif os.path.isfile(target):
        base = os.path.basename(target)
        if base.startswith("brag-sheet--"):
            findings.extend(check_brag_sheet(target))
        elif base.startswith("request--"):
            findings.extend(check_request(target))
        else:
            findings.append(("FAIL", f"unrecognized recommendation file name: {base} (must start with brag-sheet-- or request--)"))
    else:
        findings.append(("FAIL", f"target does not exist: {target}"))
    return findings


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    target = sys.argv[1]
    findings = check_path(target)

    fails = [f for f in findings if f[0] == "FAIL"]
    warns = [f for f in findings if f[0] == "WARN"]

    for level, msg in findings:
        print(f"{level} {msg}")

    if not fails and not warns:
        print(f"OK {target}: recommendation materials meet all standards")
    elif not fails:
        print(f"OK {target} (with {len(warns)} warnings)")

    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
