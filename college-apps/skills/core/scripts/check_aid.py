#!/usr/bin/env python3
"""check_aid.py — structural and financial policy validator for financial-aid.md.

    python3 scripts/check_aid.py students/<slug>/financial-aid.md
    python3 scripts/check_aid.py students/<slug>

FAIL  financial-aid.md missing or empty
FAIL  missing H1 header on line 1
FAIL  missing Strategy Archetype (Need-based, Merit-seeking, or Hybrid)
FAIL  missing annual net price budget ceiling ($...)
FAIL  missing Form Checklist / Priority Deadlines
FAIL  loans (Direct, PLUS) subtracted to claim a reduced net price in Award Audit
WARN  no institutional merit awards or state waivers tracked
WARN  only national lottery scholarships listed without local/high-school awards

Exit 1 on any FAIL, else 0.
"""
import os
import re
import sys

DATE_RE = re.compile(r"\b202\d-\d{2}-\d{2}\b|rolling|automatic|not required", re.IGNORECASE)
DOLLAR_RE = re.compile(r"\$[\d,]+", re.IGNORECASE)
ARCHETYPE_RE = re.compile(r"\b(need-based|merit-seeking|hybrid|in-state anchor)\b", re.IGNORECASE)


def check_financial_aid(filepath):
    findings = []
    if not os.path.isfile(filepath):
        return [("FAIL", f"file not found: {filepath}")], {}

    text = open(filepath, encoding="utf-8").read()
    lines = text.splitlines()
    if not text.strip():
        return [("FAIL", f"{os.path.basename(filepath)}: empty file")], {}

    # Line 1 header
    h1 = lines[0].strip() if lines else ""
    if not h1.startswith("# "):
        findings.append(("FAIL", f"{os.path.basename(filepath)}: line 1 must be an # H1 header"))

    lower_text = text.lower()

    # Section 1: Strategy & Budget
    has_strategy = any(k in lower_text for k in ("strategy", "budget target", "archetype"))
    if not has_strategy:
        findings.append(("FAIL", f"{os.path.basename(filepath)}: missing Strategy & Budget section"))

    archetype_match = ARCHETYPE_RE.search(text)
    if not archetype_match:
        findings.append(("FAIL", f"{os.path.basename(filepath)}: missing Strategy Archetype (must declare Need-based, Merit-seeking, or Hybrid)"))
    archetype = archetype_match.group(1).title() if archetype_match else "Unknown"

    budget_matches = DOLLAR_RE.findall(text)
    if not budget_matches:
        findings.append(("FAIL", f"{os.path.basename(filepath)}: missing annual budget ceiling figure ($XX,XXX)"))
    budget_str = budget_matches[0] if budget_matches else "None"

    # Section 2: Form Checklist & Priority Deadlines
    has_forms = any(k in lower_text for k in ("fafsa", "css profile", "priority deadline", "form checklist"))
    if not has_forms:
        findings.append(("FAIL", f"{os.path.basename(filepath)}: missing FAFSA / CSS Profile form checklist and priority deadlines"))
    else:
        if not DATE_RE.search(text):
            findings.append(("WARN", f"{os.path.basename(filepath)}: form checklist does not cite priority calendar dates (YYYY-MM-DD)"))

    # Section 3: Institutional Merit
    has_merit = any(k in lower_text for k in ("institutional merit", "merit scholarship", "waiver", "tuition exemption", "merit deadline"))
    if not has_merit:
        findings.append(("WARN", f"{os.path.basename(filepath)}: no institutional merit scholarships or tuition waivers tracked"))

    # Section 4: Outside & Local Scholarships
    outside_sec = ""
    if "## outside" in lower_text:
        outside_sec = lower_text.split("## outside", 1)[1].split("\n## ", 1)[0]

    has_lottery = any(k in outside_sec for k in ("taco bell", "coca-cola", "coke scholar", "coolidge"))
    has_local = any(k in outside_sec for k in ("high school", "community foundation", "district", "county", "rotary", "chamber of commerce", "alumni"))
    if has_lottery and not has_local:
        findings.append(("WARN", f"{os.path.basename(filepath)}: only national lottery scholarships listed — prioritize local/community awards first"))

    # Section 5: Award Letter Audit (Loans check)
    # Check for the trap of treating loans as discounts on net price
    if "award letter" in lower_text or "net price after loans" in lower_text:
        if re.search(r"net price\s*(?:after|with)\s*loans", lower_text) or re.search(r"subtract(?:ing)?\s*(?:plus|direct|federal)?\s*loans", lower_text):
            findings.append(("FAIL", f"{os.path.basename(filepath)}: loans (Direct, PLUS) cannot be subtracted to calculate net price — loans are debt, not aid"))

    stats = {
        "archetype": archetype,
        "budget": budget_str,
    }
    return findings, stats


def main():
    if len(sys.argv) < 2:
        print("Usage: check_aid.py <financial-aid.md-or-student-dir>", file=sys.stderr)
        sys.exit(2)

    target = sys.argv[1]
    if os.path.isdir(target):
        target = os.path.join(target, "financial-aid.md")

    findings, stats = check_financial_aid(target)
    has_fail = False
    for kind, msg in findings:
        print(f"{kind}  {msg}")
        if kind == "FAIL":
            has_fail = True

    if not has_fail:
        bname = os.path.basename(target)
        warn_count = sum(1 for k, _ in findings if k == "WARN")
        if warn_count == 0:
            print(f"OK    {bname} (Archetype: {stats.get('archetype')}, Ceiling: {stats.get('budget')})")

    sys.exit(1 if has_fail else 0)


if __name__ == "__main__":
    main()
