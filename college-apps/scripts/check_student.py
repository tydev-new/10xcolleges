#!/usr/bin/env python3
"""Check a student folder against the data contract in docs/data-model.md.

The contract was previously binding on the honor system — every rule below existed as
prose, and nothing verified the disk. This script moves the checkable rows up to code:

FAIL (exit 1 — fix before ending the session):
  - profile.md is missing, or missing a required section. The heading list in
    templates/student/profile.md is the schema — one owner, so doc and checker
    can't drift apart.
  - an essay draft with no provenance header. build_package.py also refuses these,
    but package build is weeks after the draft was written; session close is not.
  - meta.json and colleges.md disagree (different schools, or different tiers).
  - meta.json is missing or unparseable, a college carries an unknown tier/status,
    a school is listed twice, or a colleges.md heading doesn't parse as
    '## School Name — Reach|Target|Safety'.

WARN (printed — decide, don't ignore):
  - a file the contract doesn't know about (a stray `colleges-v2.md` is how a second
    source of truth is born).
  - an entry in conversations.md or feedback.md whose heading has no ISO date.
  - an extra top-level section in profile.md.

Usage:
    check_student.py students/maya-rodriguez
"""

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path

from provenance import draft_provenance

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

TIERS = {"safety", "target", "reach"}
STATUSES = {"considering", "researching", "committed-to-apply", "in-progress",
            "submitted", "decided", "withdrawn"}

# The contract's file manifest, as patterns relative to the student folder.
# Matching is anchored to the whole relative path, segment by segment — a bare
# "profile.md" means the root-level file only. A nested copy of a contract name
# (backup/profile.md, old/colleges.md) is exactly the second-source-of-truth
# case this check exists to catch, so it must NOT match.
MANIFEST = [
    "profile.md", "conversations.md", "feedback.md", "criteria.md", "colleges.md",
    "counselor-questions.md", "criteria-worksheet.md", "meta.json", "packet.json",
    "research/*.md",
    "essays/*/brief.md", "essays/*/draft-*.md", "essays/*/review-*.md",
    "recs/brag-sheet--*.md", "recs/request--*.md",
]

# colleges.md entries look like:  ## School Name — Reach|Target|Safety
COLLEGE_HEADING = re.compile(r"^(.+?)\s*[—–-]+\s*(reach|target|safety)\s*$", re.I)

ISO_DATED_HEADING = re.compile(r"^\d{4}-\d{2}-\d{2}\b")


def required_profile_sections():
    """The template's H2 headings are the profile schema — the single owner."""
    tpl = PLUGIN_ROOT / "templates" / "student" / "profile.md"
    return [m.group(1).strip()
            for m in re.finditer(r"^##\s+(.+?)\s*$", tpl.read_text(), re.M)]


def read(p):
    return p.read_text() if p.exists() else ""


def check_profile(sd, fails, warns):
    path = sd / "profile.md"
    if not path.exists():
        fails.append("profile.md is missing — run student-intake")
        return
    have = [m.group(1).strip() for m in re.finditer(r"^##\s+(.+?)\s*$",
                                                    path.read_text(), re.M)]
    required = required_profile_sections()
    for section in required:
        if section not in have:
            fails.append(f"profile.md is missing the section '## {section}' — "
                         "an unknown value is a TODO: line under the section, "
                         "never a missing section")
    for section in have:
        if section not in required:
            warns.append(f"profile.md has an unrecognized section '## {section}' — "
                         "novel material belongs under an existing section, or the "
                         "template (the schema) should gain it deliberately")


def check_drafts(sd, fails):
    base = sd / "essays"
    if not base.exists():
        return
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        for f in sorted(d.glob("draft-*.md")):
            if draft_provenance(read(f))[0] is None:
                fails.append(
                    f"{f.relative_to(sd)} has no provenance header — every draft "
                    "opens with STUDENT DRAFT, AGENT FIRST DRAFT, or EXAMPLE"
                )


def check_meta_sync(sd, fails):
    meta_path = sd / "meta.json"
    if not meta_path.exists():
        # Required: the template ships it, and without the index every check
        # downstream of it would silently vacuously pass.
        fails.append("meta.json is missing — every student folder carries the "
                     "machine-readable index (the template ships one)")
        return
    try:
        meta = json.loads(meta_path.read_text())
    except json.JSONDecodeError as e:
        fails.append(f"meta.json does not parse: {e}")
        return

    meta_entries = {}
    for c in meta.get("colleges", []):
        name = str(c.get("name", "")).strip()
        tier = str(c.get("tier", "")).strip().lower()
        status = str(c.get("status", "")).strip().lower()
        if not name:
            fails.append("meta.json has a college entry with no name")
            continue
        if tier not in TIERS:
            fails.append(f"meta.json: '{name}' has tier '{tier or '(none)'}' — "
                         f"must be one of {sorted(TIERS)}")
        if status and status not in STATUSES:
            fails.append(f"meta.json: '{name}' has status '{status}' — "
                         f"must be one of {sorted(STATUSES)}")
        if name.lower() in meta_entries:
            fails.append(f"meta.json lists '{name}' more than once — one entry "
                         "per school")
        meta_entries[name.lower()] = (name, tier)

    list_entries = {}
    unparsed = 0
    for h in re.finditer(r"^##\s+(.+?)\s*$", read(sd / "colleges.md"), re.M):
        m = COLLEGE_HEADING.match(h.group(1))
        if not m:
            unparsed += 1
            fails.append(f"colleges.md heading '## {h.group(1)}' doesn't match the "
                         "format '## School Name — Reach|Target|Safety' — anything "
                         "else (a plan, a note) belongs in the entry's body")
            continue
        name, tier = m.group(1).strip(), m.group(2).lower()
        if name.lower() in list_entries:
            fails.append(f"colleges.md lists '{name}' more than once — two entries "
                         "for one school will disagree eventually; merge them")
        list_entries[name.lower()] = (name, tier)

    for key, (name, tier) in meta_entries.items():
        if key not in list_entries:
            # With an unparseable heading present, the school may well be there
            # under the bad heading — a "missing" claim would point the fixer at
            # the wrong file. The format FAIL above already blocks the run.
            if not unparsed:
                fails.append(f"'{name}' is in meta.json but not in colleges.md — "
                             "the index has drifted from its source")
        elif tier in TIERS and list_entries[key][1] != tier:
            fails.append(f"'{name}' is tier '{tier}' in meta.json but "
                         f"'{list_entries[key][1]}' in colleges.md")
    for key, (name, _) in list_entries.items():
        if key not in meta_entries:
            fails.append(f"'{name}' is in colleges.md but not in meta.json — "
                         "update meta.json, then regenerate the tracker")


def _in_manifest(rel):
    """Anchored, segment-wise match — Path.match is right-anchored and would let
    backup/profile.md pass as profile.md, defeating the point of the check."""
    parts = rel.parts
    if parts[0] == "out":
        return True  # derived — anything under out/, at any depth, is regenerable
    for pat in MANIFEST:
        pat_parts = pat.split("/")
        if len(pat_parts) == len(parts) and all(
                fnmatch.fnmatchcase(a, b) for a, b in zip(parts, pat_parts)):
            return True
    return False


def check_strays(sd, warns):
    for f in sorted(sd.rglob("*")):
        if not f.is_file() or f.name == ".gitkeep":
            continue
        rel = f.relative_to(sd)
        if not _in_manifest(rel):
            warns.append(f"unrecognized file {rel} — if it holds student facts it is "
                         "a second source of truth; fold it into the owning file (see "
                         "docs/data-model.md) or add it to the contract deliberately")


def check_dated_entries(sd, warns):
    for name in ("conversations.md", "feedback.md"):
        for m in re.finditer(r"^##\s+(.+?)\s*$", read(sd / name), re.M):
            if not ISO_DATED_HEADING.match(m.group(1)):
                warns.append(f"{name} entry '## {m.group(1)}' has no ISO date — "
                             "append-only files date every entry")


def check(sd):
    """Return (fails, warns) for one student folder."""
    fails, warns = [], []
    check_profile(sd, fails, warns)
    check_drafts(sd, fails)
    check_meta_sync(sd, fails)
    check_strays(sd, warns)
    check_dated_entries(sd, warns)
    return fails, warns


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("student_dir")
    args = p.parse_args()

    sd = Path(args.student_dir)
    if not sd.exists():
        sys.exit(f"No such student directory: {sd}")

    fails, warns = check(sd)
    for w in warns:
        print(f"WARN  {w}")
    for f in fails:
        print(f"FAIL  {f}")
    if fails:
        sys.exit(f"\n{len(fails)} contract violation(s) in {sd} — fix before ending "
                 "the session.")
    print(f"OK    {sd} passes the contract"
          + (f" ({len(warns)} warning(s) above need a decision)" if warns else ""))


if __name__ == "__main__":
    main()
