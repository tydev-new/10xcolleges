#!/usr/bin/env python3
"""check_list.py — structural and balance validator for colleges.md.

    python3 scripts/check_list.py students/<slug>

FAIL  colleges.md does not exist or has no schools
FAIL  a school header does not declare a tier (Safety, Target, or Reach)
FAIL  a school missing one of the required fields (Why it's here, The numbers, The money, Watch out for, Deadline)
FAIL  a "Why it's here" that uses only cryptic codes without human words
WARN  zero safeties on the list
WARN  zero targets on the list
WARN  total schools under 6 or over 15 (target is 8-12)
WARN  schools in meta.json out of sync with colleges.md

Always prints the balance line: `list balance: S safeties, T targets, R reaches (total N)`.
Exit 1 on any FAIL, else 0.
"""
import json
import os
import re
import sys

TIER_RE = re.compile(r"^##\s+(.+?)\s+[—–-]\s*(Safety|Target|Reach)\s*$", re.IGNORECASE)
RAW_CODE_ONLY = re.compile(r"^(?:(?:meets|misses)\s+)?[HPD]\d+(?:\s*,\s*[HPD]\d+)*\s*[\.!]?$", re.IGNORECASE)


def check_list(student_dir):
    findings = []
    colleges_file = os.path.join(student_dir, "colleges.md")
    if not os.path.isfile(colleges_file):
        return [("FAIL", "colleges.md not found")], 0, 0, 0, 0

    text = open(colleges_file, encoding="utf-8").read()
    lines = text.splitlines()

    schools = []
    current_school = None

    for idx, line in enumerate(lines, 1):
        m = TIER_RE.match(line.strip())
        if m:
            if current_school:
                schools.append(current_school)
            name, tier = m.group(1).strip(), m.group(2).capitalize()
            current_school = {
                "line": idx,
                "name": name,
                "tier": tier,
                "fields": {},
                "body": []
            }
        elif current_school:
            s = line.strip()
            # Check for standard field bullets
            for field in ("Why it's here", "The numbers", "The money", "Watch out for", "Deadline"):
                prefix = f"- **{field}:**"
                if s.startswith(prefix) or s.startswith(f"**{field}:**"):
                    val = s[s.find(":**") + 3:].strip()
                    current_school["fields"][field] = val
                    break
            current_school["body"].append(s)

    if current_school:
        schools.append(current_school)

    if not schools:
        findings.append(("FAIL", "no schools found in colleges.md (format: ## School Name — Safety|Target|Reach)"))
        return findings, 0, 0, 0, 0

    safeties = sum(1 for s in schools if s["tier"] == "Safety")
    targets = sum(1 for s in schools if s["tier"] == "Target")
    reaches = sum(1 for s in schools if s["tier"] == "Reach")
    total = len(schools)

    # Parse budget ceiling from criteria.md if present
    crit_file = os.path.join(student_dir, "criteria.md")
    budget_ceiling = None
    if os.path.isfile(crit_file):
        crit_text = open(crit_file, encoding="utf-8").read()
        bm = re.search(r"\|\s*H\d+\s*\|\s*Budget\s*\|\s*[^|]*?\$([\d,]+)", crit_text, re.IGNORECASE)
        if bm:
            try:
                budget_ceiling = int(bm.group(1).replace(",", ""))
            except ValueError:
                pass

    for s in schools:
        missing = []
        for f in ("Why it's here", "The numbers", "The money", "Watch out for", "Deadline"):
            if f not in s["fields"] or not s["fields"][f]:
                missing.append(f)
        if missing:
            findings.append(("FAIL", f"{s['name']}: missing required field(s): {', '.join(missing)}"))

        # Check for plain words in "Why it's here"
        why = s["fields"].get("Why it's here", "")
        if why:
            words = [w for w in re.findall(r"[a-zA-Z]+", why) if w.lower() not in ("meets", "misses", "h", "p", "d")]
            if len(words) < 3 or RAW_CODE_ONLY.match(why.strip()):
                findings.append(("FAIL", f"{s['name']}: 'Why it's here' must describe criteria in plain words, not just codes ({why})"))

        # Enforce budget ceiling against The money
        money = s["fields"].get("The money", "")
        if budget_ceiling and money:
            # Look for 4-6 digit dollar amounts, e.g. $32,148 or $39476
            dollar_vals = [int(x.replace(",", "")) for x in re.findall(r"\$(\d{1,3}(?:,\d{3})+|\d{4,6})", money)]
            if dollar_vals:
                min_cost = min(dollar_vals)
                # If even the minimum cost estimate exceeds budget ceiling by more than $500
                if min_cost > budget_ceiling + 500:
                    findings.append(("FAIL", f"{s['name']}: cost (${min_cost:,}) exceeds budget ceiling (${budget_ceiling:,}) — over-budget schools must stay in chat, not in colleges.md"))

    if safeties == 0:
        findings.append(("WARN", "0 safeties on the list — every list needs at least one affordable, academically solid safety"))
    if targets == 0:
        findings.append(("WARN", "0 targets on the list — targets should form the core of the list"))
    if total < 6:
        findings.append(("WARN", f"list has only {total} schools — recommended target is 8–12 schools"))
    elif total > 15:
        findings.append(("WARN", f"list has {total} schools — consider narrowing to a focused 8–12 schools"))

    # Check meta.json sync if present
    meta_file = os.path.join(student_dir, "meta.json")
    if os.path.isfile(meta_file):
        try:
            meta = json.load(open(meta_file, encoding="utf-8"))
            meta_schools = set()
            for key in ("colleges", "target_colleges", "schools"):
                if key in meta and isinstance(meta[key], list):
                    for item in meta[key]:
                        if isinstance(item, str):
                            meta_schools.add(item.lower())
                        elif isinstance(item, dict) and "name" in item:
                            meta_schools.add(item["name"].lower())
            if meta_schools:
                doc_schools = {s["name"].lower() for s in schools}
                diff = doc_schools.symmetric_difference(meta_schools)
                if diff:
                    findings.append(("WARN", f"meta.json schools out of sync with colleges.md ({len(diff)} difference)"))
        except Exception:
            pass

    return findings, safeties, targets, reaches, total


def main():
    if len(sys.argv) < 2:
        print("Usage: check_list.py students/<slug>", file=sys.stderr)
        sys.exit(2)
    sdir = sys.argv[1]
    findings, s, t, r, tot = check_list(sdir)

    for kind, msg in findings:
        print(f"{kind}  {msg}")

    print(f"list balance: {s} safeties, {t} targets, {r} reaches (total {tot})")

    has_fail = any(k == "FAIL" for k, _ in findings)
    if not has_fail:
        if not any(k == "WARN" for k, _ in findings):
            print("OK")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
