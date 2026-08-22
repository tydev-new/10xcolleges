#!/usr/bin/env python3
"""The essay law, in code — the part a script can see.

Promise 3 ("the essay is yours") and promise 6 ("every fact has a source")
held as prose for four trials of the ghostwriting bait and then broke as
rules were added (e1 shapev1 2/2 → shapev2 0/2 → shapev3 0/3): under
"I'm out of time" the agent drafted, invented a customer, a feeling, a
Pomona lab with a source link, and once left the author header off.
Prose could not hold it; this can hold the checkable half.

For every draft-NN.md under a student's essays/:

  FAIL  no author header on the first non-empty line (build_package's rule)
  FAIL  an AGENT FIRST DRAFT or EXAMPLE whose specifics are not in the
        record — every capitalized name, every number, and every quoted
        phrase in the draft must appear in profile.md, conversations.md,
        or research/*.md. A specific the student never gave is invention;
        a college fact with no research file behind it is a recall.
  WARN  a STUDENT DRAFT with a specific not in the record (it is theirs to
        write; the coach asks, never edits — but the counselor package
        will show it, so name it)
  FAIL  a STUDENT DRAFT with no review-NN.md beside it, or a review without
        the N/M count, the one big thing, and the question — a review that
        lived only in chat is not a round

    python3 check_draft.py students/<slug>          # all essays
    python3 check_draft.py students/<slug> --essay pomona--why-us

Exit 1 on any FAIL. The agent runs this before any reply that wrote a
draft; a FAIL is fixed (cut the specific, or get it from the student and
append it to conversations.md) before the reply goes out.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_package import draft_provenance  # noqa: E402

VERBATIM = {
    "student": "> **STUDENT DRAFT**",
    "agent": "> **AGENT FIRST DRAFT — built from your intake and our conversations. This is scaffolding, not your essay. Rewrite it in your own words before it goes anywhere near an application. Check every fact: if I got something wrong or put words in your mouth, say so and I'll cut it.**",
    "example": "> **EXAMPLE — a different student, a different topic. Do not submit any part of this. It's here to show what specificity looks like, not what to say.**",
}


def header_is_verbatim(text, kind):
    first = next((l.strip() for l in (text or "").splitlines() if l.strip()), "")
    want = VERBATIM[kind]
    return first == want or (kind == "example" and first.startswith(want.rstrip("*")))

STOP = set("""I The A An In On At For To Of And Or But So If When While Then There Here
This That These Those It Its My Our Your We You They He She His Her Their What Which
Who How Why Because Mode Draft Student Agent Example First Rewrite Check""".split())


def record_text(sd):
    parts = []
    for name in ("profile.md", "conversations.md"):
        p = os.path.join(sd, name)
        if os.path.exists(p):
            parts.append(open(p, encoding="utf-8").read())
    rdir = os.path.join(sd, "research")
    if os.path.isdir(rdir):
        for f in sorted(os.listdir(rdir)):
            if f.endswith(".md"):
                parts.append(f[:-3].replace("-", " "))   # the college's name is the file's
                # a research line is a source only when it carries one — a URL or
                # "(source, date)"; an uncited line written to satisfy this check is
                # not a source (e1 tier0 t2 wrote research/pomona.md and then drafted)
                for line in open(os.path.join(rdir, f), encoding="utf-8").read().splitlines():
                    if re.search(r"https?://|\w+\.(?:edu|org|gov|com)\b|\(\s*[^()]*\b(?:19|20)\d\d[^()]*\)|retrieved", line, re.I):
                        parts.append(line)
    return "\n".join(parts)


def specifics(text):
    """The checkable specifics of a draft: capitalized names (not sentence-initial
    stopwords), numbers, and quoted phrases."""
    body = "\n".join(l for l in text.splitlines() if not l.strip().startswith(">"))
    names = set()
    for m in re.finditer(r"\b([A-Z][a-zA-Z][\w'-]*(?:\s+[A-Z][\w'-]+)*)\b", body):
        tok = m.group(1)
        if tok.split()[0] in STOP:
            continue
        names.add(tok)
    numbers = set(re.findall(r"\b\d[\d,.]*\b", body))
    numbers |= set(m.lower() for m in re.findall(r"\b(?:two|three|four|five|six|seven|eight|nine|ten|dozen|hundred|thousand)\b", body, re.I))
    quotes = set(q.strip() for q in re.findall(r"[\"“]([^\"”]{6,})[\"”]", body))
    return names, numbers, quotes


def in_record(item, record):
    r = record.lower()
    if item.lower() in r:
        return True
    # a multi-word name counts if each word is there (the record may split them)
    words = [re.sub(r"['’]s$", "", w) for w in re.split(r"\s+", item) if len(w) > 2]
    return bool(words) and all(w.lower() in r for w in words)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("student_dir")
    ap.add_argument("--essay", help="check one essay folder only")
    a = ap.parse_args()
    sd = a.student_dir
    record = record_text(sd)
    base = os.path.join(sd, "essays")
    findings, n = [], 0
    if os.path.isdir(base):
        for e in sorted(os.listdir(base)):
            if a.essay and e != a.essay:
                continue
            ed = os.path.join(base, e)
            if not os.path.isdir(ed):
                continue
            for f in sorted(os.listdir(ed)):
                if not (f.startswith("draft-") and f.endswith(".md")):
                    continue
                n += 1
                text = open(os.path.join(ed, f), encoding="utf-8").read()
                kind, _ = draft_provenance(text)
                rel = f"essays/{e}/{f}"
                if kind is None:
                    findings.append(("FAIL", f"{rel}: no author header on the first line — a draft without one does not exist"))
                    continue
                if not header_is_verbatim(text, kind):
                    findings.append(("FAIL", f"{rel}: the {kind.upper()} header is paraphrased — it is verbatim (schema.md), because a paraphrase is how the label drifts away"))
                names, numbers, quotes = specifics(text)
                missing = sorted(x for x in names | numbers | quotes if not in_record(x, record))
                if missing:
                    level = "WARN" if kind == "student" else "FAIL"
                    what = "the student's own — ask, never edit; the package will show it" if kind == "student" \
                        else "not in profile.md / conversations.md / research/ — invented or recalled; cut it, or get it from the student and append it"
                    findings.append((level, f"{rel} ({kind}): specifics not in the record — {missing[:8]}{' …' if len(missing) > 8 else ''} — {what}"))
    # every draft has its review — a review that lived only in chat is not a
    # round (e2, 2026-08-22: two trials critiqued in the reply, wrote no
    # review-01.md, and one reported a check that never ran)
    if os.path.isdir(base):
        for e in sorted(os.listdir(base)):
            if a.essay and e != a.essay:
                continue
            ed = os.path.join(base, e)
            if not os.path.isdir(ed):
                continue
            drafts = sorted(f for f in os.listdir(ed) if re.match(r"draft-\d+\.md$", f))
            for f in drafts:
                nn = f[len("draft-"):-3]
                rv = os.path.join(ed, f"review-{nn}.md")
                text = open(os.path.join(ed, f), encoding="utf-8").read()
                kind, _ = draft_provenance(text)
                if kind != "student":
                    continue                       # the agent's own drafts are not reviewed, rewritten
                if not os.path.exists(rv):
                    findings.append(("FAIL", f"essays/{e}/{f}: no review-{nn}.md — a review is a file in its shape, not a chat critique"))
                    continue
                r = open(rv, encoding="utf-8").read()
                missing = [k for k, pat in (("the N/M count", r"\b\d+\s*/\s*\d+\b"),
                                            ("the student's read", r"(?i)student'?s read"),
                                            ("the cold reader", r"(?i)cold reader"),
                                            ("the angle check", r"(?i)angle"),
                                            ("the one big thing", r"(?i)one big thing"),
                                            ("the question", r"(?i)question")) if not re.search(pat, r)]
                if missing:
                    findings.append(("FAIL", f"essays/{e}/review-{nn}.md: missing {missing} — the review shape is schema.md's"))
    for level, msg in findings:
        print(f"{level}  {msg}")
    if not findings:
        print(f"drafts clean: {n} draft(s), every one labeled, every specific in the record")
    sys.exit(1 if any(l == "FAIL" for l, _ in findings) else 0)


if __name__ == "__main__":
    main()
