#!/usr/bin/env python3
"""check_record.py — the intake law, in code.

    python3 scripts/check_record.py students/<slug>

FAIL  a content line in profile.md / criteria.md with no source tag
FAIL  a `TODO:` that carries a value (a number or a dollar amount)
FAIL  conversations.md dated headers going backwards
WARN  a GPA line that does not say unweighted (and no TODO for it)
WARN  a budget row with no "set by"
Exit 1 on any FAIL, else 0. Prints one line per finding, `OK` when clean.
"""
import os
import re
import sys

TAG = re.compile(r"\[(packet|transcript|worksheet|student(?: \d{4}-\d{2}-\d{2})?|parent(?: \d{4}-\d{2}-\d{2})?|counselor(?: \d{4}-\d{2}-\d{2})?)\]")


HERE = os.path.dirname(os.path.abspath(__file__))


def template_lines(fname):
    """Lines of the shipped template — a line the agent left as it was is not a claim."""
    for root in (os.environ.get("CLAUDE_PLUGIN_ROOT"), os.path.join(HERE, "..")):
        if not root:
            continue
        p = os.path.join(root, "templates", "student", fname)
        if os.path.exists(p):
            return {l.strip() for l in open(p, encoding="utf-8").read().splitlines()}
    return set()


def content_lines(text, fname=""):
    """Lines that make a claim: bullets and table rows with something in them."""
    lines = text.splitlines()
    tmpl = template_lines(fname)
    for n, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s == "---" or s in tmpl:
            continue
        nxt = lines[n].strip() if n < len(lines) else ""
        if s.startswith("|") and re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", nxt):
            continue  # the header row — the rule row is under it
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r"-*:?-*", c) for c in cells):  # the rule row
                continue
            if cells and cells[0] in ("#",):  # header row
                continue
            if all(c == "" for c in cells[1:]):  # the template's empty row
                continue
            yield n, s, "row"
        elif s.startswith("-") or s.startswith("*"):
            yield n, s, "bullet"
        # plain prose paragraphs are the template's explanations — not claims


def check(sd):
    findings = []
    for fname in ("profile.md", "criteria.md"):
        p = os.path.join(sd, fname)
        if not os.path.exists(p):
            findings.append(("FAIL", f"{fname}: missing — intake writes it from the template"))
            continue
        text = open(p, encoding="utf-8").read()
        for n, s, kind in content_lines(text, fname):
            body = s.lstrip("-* ").strip()
            if body.startswith("TODO:"):
                rest = body[5:].strip()
                if re.search(r"\$\s?\d|(?<![\w-])\d+(\.\d+)?(?![\w-])", re.sub(r"\d{4}-\d{2}-\d{2}", "", rest)):
                    findings.append(("FAIL", f"{fname}:{n}: a TODO carrying a value — a blank is a TODO, never a guess: `{s[:80]}`"))
                continue
            if re.match(r"^\*\*[^*]+:\*\*\s*$", body):  # a label with nothing after it
                continue
            if "TODO:" in body:
                continue
            if not TAG.search(s):
                findings.append(("FAIL", f"{fname}:{n}: no source tag on a content line — [packet] [transcript] [worksheet] [student YYYY-MM-DD] [parent …] [counselor …]: `{s[:80]}`"))
            if fname == "profile.md" and re.search(r"\bGPA\b", body, re.I) and not re.search(r"unweighted", body, re.I):
                if not re.search(r"TODO:.*unweighted", text, re.I):
                    findings.append(("WARN", f"{fname}:{n}: GPA without 'unweighted' and no TODO for it — students quote the weighted one: `{s[:80]}`"))
            if fname == "criteria.md" and kind == "row" and re.search(r"budget|\$\s?\d|per year|/yr", body, re.I) and not re.search(r"set by", body, re.I):
                findings.append(("WARN", f"{fname}:{n}: a money row with no 'set by' — who set the number is the number: `{s[:80]}`"))
    cp = os.path.join(sd, "conversations.md")
    if os.path.exists(cp):
        dates = re.findall(r"^##\s*(\d{4}-\d{2}-\d{2})", open(cp, encoding="utf-8").read(), re.M)
        if dates != sorted(dates):
            findings.append(("FAIL", "conversations.md: dated headers go backwards — the log is append-only"))
    return findings


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sd = sys.argv[1]
    if not os.path.isdir(sd):
        print(f"FAIL {sd}: not a folder")
        sys.exit(1)
    findings = check(sd)
    for level, msg in findings:
        print(f"{level} {msg}")
    if not findings:
        print("OK")
    sys.exit(1 if any(l == "FAIL" for l, _ in findings) else 0)


if __name__ == "__main__":
    main()
