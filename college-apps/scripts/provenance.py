#!/usr/bin/env python3
"""Draft provenance markers — defined once, enforced twice.

Every essay draft must declare who wrote it, in its first few lines. An agent-drafted
essay is indistinguishable from a student's once the header is dropped, so the
declaration cannot be inferred after the fact — it has to be present at write time and
checked mechanically. Two scripts enforce the same markers: check_student.py at session
close (catches an unlabeled draft the day it was written) and build_package.py at build
time (the last line of defense before a counselor sees it).

A marker counts only at the *start* of one of the first six lines (allowing the
blockquote/bold prefix the templates prescribe). A substring anywhere was too loose:
a draft opening "For example, my summer…" is prose, not an EXAMPLE declaration.
"""

import re

PROVENANCE = [
    ("AGENT FIRST DRAFT", "agent", "Agent-drafted scaffolding — student has not yet rewritten"),
    ("EXAMPLE", "example", "Illustrative sample on another topic — not for submission"),
    ("STUDENT DRAFT", "student", "Student's own writing"),
]

# Built from PROVENANCE so a new marker can't be added to the list without the
# regex seeing it — one owner, even inside one file.
_MARKER = re.compile(r"^\s*(?:>\s*)?\**\s*("
                     + "|".join(re.escape(m) for m, _, _ in PROVENANCE)
                     + r")\b")


def draft_provenance(text):
    """Return (kind, label) from the draft's declared header, or (None, None)."""
    for line in (text or "").splitlines()[:6]:
        m = _MARKER.match(line.upper())
        if m:
            for marker, kind, label in PROVENANCE:
                if marker == m.group(1):
                    return kind, label
    return None, None
