#!/usr/bin/env python3
"""Draft provenance markers — defined once, enforced twice.

Every essay draft must declare who wrote it, in its first few lines. An agent-drafted
essay is indistinguishable from a student's once the header is dropped, so the
declaration cannot be inferred after the fact — it has to be present at write time and
checked mechanically. Two scripts enforce the same markers: check_student.py at session
close (catches an unlabeled draft the day it was written) and build_package.py at build
time (the last line of defense before a counselor sees it).
"""

PROVENANCE = [
    ("AGENT FIRST DRAFT", "agent", "Agent-drafted scaffolding — student has not yet rewritten"),
    ("EXAMPLE", "example", "Illustrative sample on another topic — not for submission"),
    ("STUDENT DRAFT", "student", "Student's own writing"),
]


def draft_provenance(text):
    """Return (kind, label) from the draft's declared header, or (None, None)."""
    head = "\n".join((text or "").splitlines()[:6]).upper()
    for marker, kind, label in PROVENANCE:
        if marker in head:
            return kind, label
    return None, None
