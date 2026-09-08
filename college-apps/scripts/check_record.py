#!/usr/bin/env python3
"""check_record.py — the intake law, in code.

    python3 scripts/check_record.py students/<slug>

FAIL  a content line in profile.md / criteria.md with no source tag
FAIL  a `TODO:` that carries a value (a number or a dollar amount)
FAIL  conversations.md dated headers going backwards
WARN  a GPA line that does not say unweighted (and no TODO for it)
WARN  a budget row with no "set by"
Always prints both gates: `material N/3` (the essay's) and `gate N/4` (the list's),
each with what is missing; the reply repeats the line for what comes next.
Exit 1 on any FAIL, else 0. Prints one line per finding, `OK` when clean.
"""
import os
import re
import sys

TAG = re.compile(r"\[(packet|transcript|worksheet|(?:student|parent|counselor) \d{4}-\d{2}-\d{2})\]")
UNDATED = re.compile(r"\[(student|parent|counselor)\]")


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
            if "TODO:" in body:  # bare `- TODO: …` or labelled `- **GPA:** TODO: …`
                rest = body.split("TODO:", 1)[1].strip()
                if re.search(r"\$\s?\d|(?<![\w-])\d+(\.\d+)?(?![\w-])|\b(probably|maybe|likely|i think|guess)\b", re.sub(r"\d{4}-\d{2}-\d{2}", "", rest), re.I):
                    findings.append(("FAIL", f"{fname}:{n}: a TODO carrying a value — a blank is a TODO, never a guess: `{s[:80]}`"))
                continue
            if re.match(r"^\*\*[^*]+:\*\*\s*$", body):  # a label with nothing after it
                continue
            if "TODO:" in body:
                continue
            if UNDATED.search(s) and not TAG.search(s):
                findings.append(("FAIL", f"{fname}:{n}: a person's tag needs its date — [student YYYY-MM-DD]: `{s[:80]}`"))
            elif not TAG.search(s):
                findings.append(("FAIL", f"{fname}:{n}: no source tag on a content line — [packet] [transcript] [worksheet] [student YYYY-MM-DD] [parent …] [counselor …]: `{s[:80]}`"))
            if fname == "profile.md" and re.search(r"\bGPA\b", body, re.I) and not re.search(r"unweighted", body, re.I):
                if not re.search(r"TODO:.*unweighted", text, re.I):
                    findings.append(("WARN", f"{fname}:{n}: GPA without 'unweighted' and no TODO for it — students quote the weighted one: `{s[:80]}`"))
            if fname == "profile.md" and re.search(r"state of residence", body, re.I) and not re.search(r"TODO:", body, re.I) and not TAG.search(s):
                findings.append(("WARN", f"{fname}:{n}: state of residence has no value and no TODO — mark as explicit TODO: if unknown: `{s[:80]}`"))
            if fname == "criteria.md" and kind == "row" and re.search(r"budget|\$\s?\d|per year|/yr", body, re.I) and not re.search(r"set by", body, re.I):
                findings.append(("WARN", f"{fname}:{n}: a money row with no 'set by' — who set the number is the number: `{s[:80]}`"))
    cp = os.path.join(sd, "conversations.md")
    if os.path.exists(cp):
        ctext = open(cp, encoding="utf-8").read()
        dates = re.findall(r"^##\s*(\d{4}-\d{2}-\d{2})", ctext, re.M)
        if dates != sorted(dates):
            findings.append(("FAIL", "conversations.md: dated headers go backwards — the log is append-only"))
        if not dates:
            findings.append(("WARN", "conversations.md: no dated entry yet — the conversation is recorded as it happens, word for word"))
    return findings


def section(text, pattern):
    """Lines under the first `## ` header whose title matches pattern."""
    out, on = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            on = bool(re.search(pattern, line, re.I))
            continue
        if on:
            out.append(line.strip())
    return out


def claim(lines, pattern):
    """A tagged, non-TODO line matching pattern, with something after its label."""
    for l in lines:
        if "TODO:" in l or not TAG.search(l):
            continue
        if re.search(pattern, l, re.I) and re.sub(r"\*\*[^*]*\*\*|\[[^\]]*\]|[-*\s:]", "", l):
            return True
    return False


def gate(sd):
    """The four items the list needs; returns (n, missing)."""
    prof = open(os.path.join(sd, "profile.md"), encoding="utf-8").read() if os.path.exists(os.path.join(sd, "profile.md")) else ""
    crit = open(os.path.join(sd, "criteria.md"), encoding="utf-8").read() if os.path.exists(os.path.join(sd, "criteria.md")) else ""
    missing = []
    hard = [l for l in section(crit, r"hard filters") if l.startswith("|") and re.match(r"\|\s*H\d+\s*\|", l)]
    money = [l for l in hard if re.search(r"budget|\$\s?\d|per year|/yr", l, re.I)]
    if not any(re.search(r"set by:\s*(?!nobody)(?!.*guess)\S", l, re.I) and TAG.search(l) for l in money):
        missing.append("budget with who set it (a guess is 0)")
    basics = section(prof, r"basics")
    if not (claim(basics, r"GPA.*unweighted|unweighted.*GPA") and re.search(r"unweighted[^\n]*\d\.\d", "\n".join(basics), re.I)):
        missing.append("unweighted GPA")
    elif not claim(basics, r"test scores|testing plan|\bSAT\b|\bACT\b|test-optional"):
        missing.append("scores or the plan to test")
    elif not claim(basics, r"state of residence|home state|\bresidence\b"):
        missing.append("state of residence (needed for in-state tuition)")
    if not claim(section(prof, r"goals|direction|major"), r"."):
        missing.append("a direction (\"undecided\" counts)")
    deal = [l for l in section(crit, r"deal-breakers") if re.match(r"\|\s*D\d+\s*\|", l) and TAG.search(l)]
    hard_ok = [l for l in hard if TAG.search(l)]
    if not (hard_ok and deal):
        missing.append("a Hard filter and a Deal-breaker row")
    return 4 - len(missing), missing


def material(sd):
    """The essay gate: what essay-coach runs on; returns (n, missing)."""
    prof = open(os.path.join(sd, "profile.md"), encoding="utf-8").read() if os.path.exists(os.path.join(sd, "profile.md")) else ""
    conv = open(os.path.join(sd, "conversations.md"), encoding="utf-8").read() if os.path.exists(os.path.join(sd, "conversations.md")) else ""
    missing = []
    docs = os.path.join(sd, "documents")
    have_docs = os.path.isdir(docs) and any(not f.startswith(".") for f in os.listdir(docs))
    if not (have_docs or re.search(r"documents:\s*none", prof, re.I)):
        missing.append("documents read, or `documents: none` recorded")
    acts = section(prof, r"activities|work experience")
    rows = [l for l in acts if l.startswith("|") and not re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", l) and TAG.search(l)]
    def ok(row):
        cells = [c.strip() for c in row.strip("|").split("|")]
        return any(re.search(r"\d", c) for c in cells[1:4]) and len(cells) >= 5 and len(re.sub(r"\[[^\]]*\]", "", cells[-1]).strip()) > 15
    if not any(ok(r) for r in rows):
        missing.append("one activity with hours and what actually happened")
    if not claim(section(prof, r"goals|direction|major"), r"."):
        missing.append("the major they are applying for, and how sure (\"undecided\" counts)")
    return 3 - len(missing), missing


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
    m, mm = material(sd)
    print(f"material {m}/3" + (" — missing: " + "; ".join(mm) if mm else " — the essay can start"))
    n, missing = gate(sd)
    print(f"gate {n}/4" + (" — missing: " + "; ".join(missing) if missing else " — the list can start"))
    sys.exit(1 if any(l == "FAIL" for l, _ in findings) else 0)


if __name__ == "__main__":
    main()
