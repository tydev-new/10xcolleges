#!/usr/bin/env python3
"""shapecheck — the skill shape's checker core, domain-neutral.

A host's checker (for 10xjobs: `skills/profile/scripts/check_files.py`)
supplies what is domain-specific — the workspace manifest, the history
headers, the declared tables — and runs these on top:

  load_schemas(skills_root)           -> {file: schema}, from every SKILL.md
                                         and references/schema.md declaring line
  check_file(path, schema, all, name) -> [(level, msg)] sections vs the schema
  check_table(path, header, enums)    -> [(level, msg)] a declared table
  check_history(path, header)         -> [(level, msg)] an append-only round table
  check_skill_prose(skills_root)      -> [(level, msg)] every backticked relative
                                         path in skill prose resolves

These functions are COPIES of the host's; `kit/tests/test_kit.py` asserts
the two stay byte-identical so a fix lands in both or fails loudly (the
sanctioned-duplication pattern: a guarded copy, no echo bookkeeping).
The parser's three rules are in docs/skill-shape.md § schema.md.
"""
import glob
import os
import re

def check_table(path, header, enums):
    """A declared table: exact header, matching cell counts, enum cells valid.
    Silent when the table is absent — not every application has one yet."""
    res = []
    raw = open(path, encoding="utf-8").read().replace("\\|", "")
    all_lines = [l.strip() for l in raw.splitlines()]
    if header not in all_lines:
        # a section titled for this table but carrying a near-miss header
        # is not "absent" — it is the altered-header case check_history
        # FAILs on; here it WARNs (2026-08-21 alignment review, L1)
        title = {COVERAGE_HEADER: "## Coverage", SELECTION_HEADER: "## Selection",
                 ROUNDS_HEADER: "## Rounds", PANEL_HEADER: "## Panel"}.get(header)
        if title and any(l.startswith(title) for l in all_lines):
            res.append(("WARN", f'{title} present but its header is not exactly "{header}"'))
        return res
    # the table is the CONTIGUOUS run of pipe rows under the header; stop at
    # the first line that is not one. An application file holds several
    # tables and free prose (apply/references/schema.md), so walking to EOF
    # measured the next table's rows against this header — four bogus WARNs
    # on the design's own normal file (measured 2026-08-18; the first tests
    # each used a single-table fixture, so this rung was green because it
    # never ran).
    block = []
    for l in all_lines[all_lines.index(header) + 1:]:
        if not l.startswith("|"):
            break
        block.append(l)
    ncols = header.count("|") - 1
    for l in block:
        if set(l) <= set("|-: "):
            continue                      # separator row
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) != ncols:
            res.append(("WARN", f'row has {len(cells)} cells, the header has {ncols}: "{l[:60]}"'))
            continue
        for idx, allowed in enums.items():
            v = cells[idx].lower().strip("`*_ ")
            if v and v not in allowed:
                res.append(("WARN", f'"{cells[idx]}" is not one of {sorted(allowed)} '
                                    f'— apply/references/schema.md declares the enum'))
        if header == PANEL_HEADER:
            o = cells[2].strip("`*_ ")
            if o and not (o == "fixed" or o.startswith("discarded —") or o == "—"):
                res.append(("WARN", f'panel outcome "{o}" is neither "fixed" nor "discarded — <why>" '
                                    f'(or "—" on a VOID row) — apply/references/schema.md'))
    return res

def check_history(path, header):
    """FAIL on a missing/altered header or a row whose cell count drifts —
    a malformed append silently corrupts the loop's audit trail."""
    res = []
    raw = open(path, encoding="utf-8").read().replace("\\|", "")  # escaped pipes are cell text
    lines = [l.strip() for l in raw.splitlines() if l.strip().startswith("|")]
    if header not in lines:
        res.append(("FAIL", f'history header missing or altered — must be exactly "{header}"'))
        return res
    ncols = header.count("|") - 1
    for i, l in enumerate(lines):
        if set(l) <= set("|-: "):
            continue  # the separator row
        cols = l.count("|") - 1
        if cols != ncols:
            res.append(("FAIL", f"history row {i} has {cols} cells, the header has {ncols}"))
    return res

def check_skill_prose(skills_root):
    """The skill files' own structure — the one artifact class that shipped
    unchecked while schemas, tables, materials and language all had a rung.

    Two checks only, both unambiguous:
      FAIL  a relative link or path that does not resolve
      WARN  a table row whose cell count differs from its header

    Deliberately NOT checked: "§ Some Section" pointers. A prototype flagged
    12 files and most were pointers into ANOTHER file ("base-resume.md
    § Claim rules"), indistinguishable from a local reference without
    parsing intent. A noisy rung trains people to ignore it — the
    earned-FAIL bar's warning, applied to a rung before it shipped.

    Earned 2026-08-19: two cross-skill links were one `../` short. One was
    tailoring.md's FIRST instruction ("read resume-engine.md first"), so an
    agent following it found nothing and assembled without the base-résumé
    resolution ladder.

    Widened 2026-08-19, same day, by the independent review of the CMF and
    negotiate deletions: the first pattern only matched links STARTING with
    `./` or `../`, so six more of the identical class were invisible to it —
    `apply/scripts/check_materials.py` written from inside profile, where the
    repo's own convention is `../../apply/...`. A rung that misses the bug it
    was built for is worse than no rung: it reports green. Any backticked
    path with a `/` and an .md/.py/.html suffix must now resolve, from either
    the file's directory or its skill root. Schema placeholders (`<slug>`)
    are exempt — they name a shape, not a file.
    """
    res = []
    for path in sorted(glob.glob(os.path.join(skills_root, "**", "*.md"), recursive=True)):
        rel_name = os.path.relpath(path, skills_root)
        text = open(path, encoding="utf-8").read()
        here = os.path.dirname(path)
        skill_root = os.path.join(skills_root, rel_name.split(os.sep)[0])
        seen = set()
        for m in re.finditer(
            r"\]\((\.\.?/[^)#\s]+)\)|`([\w./-]*/[\w./-]+\.(?:md|py|html))(?: §[^`]*)?`", text
        ):
            target = m.group(1) or m.group(2)
            if "<" in target or target in seen:
                continue
            seen.add(target)
            # a ./ or ../ link means what it says: it resolves from the
            # file's OWN directory, never from the skill root. Allowing the
            # root as a fallback would mask the original bug — an `../` one
            # short from inside references/ would quietly resolve.
            bases = (here,) if target.startswith(".") else (here, skill_root)
            hit = next(
                (
                    os.path.normpath(os.path.join(base, target))
                    for base in bases
                    if os.path.exists(os.path.normpath(os.path.join(base, target)))
                ),
                None,
            )
            if hit is None:
                res.append(("FAIL", f"{rel_name}: link does not resolve — {target}"))
            elif os.path.relpath(hit, skills_root).startswith(".."):
                # resolves in the repo, not in ~/.claude/skills — a skill must
                # be self-contained or its pointer is dead for every user
                res.append(
                    ("FAIL", f"{rel_name}: link escapes the skill tree — {target}")
                )
        lines = text.split("\n")
        i = 0
        while i < len(lines) - 1:
            head, sep = lines[i], lines[i + 1].strip()
            if head.startswith("|") and sep.startswith("|") and set(sep) <= set("|-: "):
                ncols = head.count("|")
                j = i + 2
                while j < len(lines) and lines[j].startswith("|"):
                    if lines[j].count("|") != ncols:
                        res.append(("WARN", f"{rel_name}: table row {j+1} has "
                                            f"{lines[j].count('|') - 1} cells, header has {ncols - 1}"))
                    j += 1
                i = j
            else:
                i += 1
    return res

# A schema block in a SKILL.md looks like:
#   **`profile.md` — who they are.** Any prose.
#   - `## Snapshot` — notes
#   - `## Intake findings` — with all four:
#     - `### Positioning strengths`
#   - `## Other notes` — optional
# Two declaration forms: the inline `**\`file.md\`**` block (SKILL.md § State),
# and a `## \`file.md\` — ...` heading (a references/schema.md organised per
# file). Added 2026-08-20 when profile's schema.md gained per-file headings
# and the old pattern silently dropped all five of its schemas — the printed
# schema count is what caught it.
FILE_RE = re.compile(r"^(?:\*\*|##\s+)`([\w\-.]+\.md)`")

# Some files carry the candidate's own structure (a résumé body). Their
# header line says "free-form body"; only the named sections are required
# and unknown headings there are not flagged.
FREEFORM = "free-form body"

SECTION_RE = re.compile(r"^(\s*)-\s+`(#{2,3})\s+([^`]+)`(.*)$")

def load_schemas(skills_root):
    """Parse every skill's schema blocks into {filename: schema}.

    Read from BOTH `SKILL.md` and `references/schema.md`, because a skill
    may declare its file shapes in either. Extended 2026-08-20: profile's
    § State held 516 words of schema in the always-loaded tier; moving it
    to a reference cuts that from every session that fires the skill,
    and a schema is consulted when writing a record, not continuously.
    A filename declared in both places is a duplicate the caller reports.
    """
    schemas = {}
    paths = sorted(glob.glob(os.path.join(skills_root, "*", "SKILL.md")))
    paths += sorted(glob.glob(os.path.join(skills_root, "*", "references", "schema.md")))
    for path in paths:
        current = None
        for line in open(path, encoding="utf-8"):
            m = FILE_RE.match(line)
            if m:
                skill_dir = os.path.dirname(path)
                if os.path.basename(skill_dir) == "references":
                    skill_dir = os.path.dirname(skill_dir)  # references/schema.md -> the skill
                current = {"sections": [], "freeform": FREEFORM in line.lower(),
                           "owner": os.path.basename(skill_dir)}
                # A bare bold mention of a file in ANOTHER skill's prose must
                # never clobber the owner's real schema: only a block that
                # gathers sections may claim the name (caught 2026-08-14 —
                # search's "criteria.md is INPUT only" sentence silently
                # deleted profile's criteria schema).
                if m.group(1) not in schemas or not schemas[m.group(1)]["sections"]:
                    schemas[m.group(1)] = current
                continue
            if current is None:
                continue
            sec = SECTION_RE.match(line)
            if sec:
                _, hashes, name, rest = sec.groups()
                current["sections"].append({
                    "name": name.strip(),
                    "level": len(hashes),
                    "optional": "optional" in rest.lower(),
                })
            elif line.strip() and not line.startswith((" ", "\t", "*", "-")):
                current = None  # prose resumed; the block ended
    return {k: v for k, v in schemas.items() if v["sections"]}

def headings(text):
    """Headings present, each tagged with the `##` section it sits under.

    Anything under `## Other notes` carries under_escape=True: that section
    is the sanctioned home for novel material, so policing its internals
    would defeat the point of having an escape hatch."""
    out = []
    current_top = None
    for m in re.finditer(r"^(#{2,3})\s+(.+?)\s*$", text, re.M):
        level, name = len(m.group(1)), m.group(2).strip()
        if level == 2:
            current_top = name
        out.append({"name": name, "level": level,
                    "under_escape": norm(current_top or "") == norm("Other notes")
                                    and not (level == 2 and norm(name) == norm("Other notes"))})
    return out

def norm(s):
    """Compare on words only — an appended date or count is not a new section.

    Trailing plurals are folded so "Target" and "Targets" are one section,
    not a silent miss (caught on the first real workspace)."""
    s = re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
    parts = s.split()
    if parts and len(parts[-1]) > 3 and parts[-1].endswith("s"):
        parts[-1] = parts[-1][:-1]
    return " ".join(parts)

def check_file(path, schema, all_schemas, fname):
    res = []
    text = open(path, encoding="utf-8").read()
    present = headings(text)
    present_norm = {norm(h["name"]) for h in present}

    for want in schema["sections"]:
        if want["optional"]:
            continue
        w = norm(want["name"])
        # A required heading may carry a suffix ("Targets — two, 50/50").
        if not any(p == w or p.startswith(w) for p in present_norm):
            res.append(("FAIL", f'missing required section "{"#" * want["level"]} {want["name"]}"'))

    known = {norm(s["name"]) for s in schema["sections"]} | {norm("Other notes")}
    # Sections owned by some OTHER file — the cross-contamination class.
    foreign = {}
    for other, osch in all_schemas.items():
        if other == fname:
            continue
        for s in osch["sections"]:
            foreign.setdefault(norm(s["name"]), other)

    for h in present:
        if h.get("under_escape"):
            continue
        n = norm(h["name"])
        if any(n == k or n.startswith(k) for k in known):
            continue
        if schema.get("freeform"):
            continue  # the candidate's own headings are theirs
        owner = next((f for k, f in foreign.items() if n == k or n.startswith(k)), None)
        if owner:
            res.append(("FAIL", f'section "{h["name"]}" belongs to {owner} — '
                                f"content in the wrong file breaks its consumers"))
        else:
            res.append(("WARN", f'unrecognised section "{h["name"]}" — '
                                f"put novel material under `## Other notes`"))
    return res
