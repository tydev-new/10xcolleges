"""The invariants test — what must be true across EVERY skill in a skills/
directory, so the shape stays the shape. Each check is one of the
classes sixteen independent reviews caught by hand on 2026-08-21; here
they fail on every `tests/run.py`, instead of needing a reviewer.

Structure only — what code can see. Conduct stays with the harness.
"""
import glob
import os
import re
import sys

# Domain-neutral: point SKILLS_ROOT at any skills/ directory. The host's
# checker constants (manifest, history headers) are read from the module
# named by HOST_CHECKER (default: the kit's shapecheck, which has none —
# the manifest test then only checks schema owners are skills).
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
SKILLS = os.environ.get("SKILLS_ROOT", os.path.join(ROOT, "skills"))
sys.path.insert(0, os.path.join(ROOT, "kit"))
import shapecheck as cf  # noqa: E402
MANIFEST = getattr(cf, "MANIFEST_FILES", {})

ALL = sorted(os.path.basename(d) for d in glob.glob(os.path.join(SKILLS, "*")) if os.path.isdir(d))
STAGES_OF_A_SECTION = ("Runs when", "Exits")


def read(*parts):
    p = os.path.join(SKILLS, *parts)
    assert os.path.exists(p), f"{'/'.join(parts)}: missing — the five files are the shape's first invariant"
    return open(p, encoding="utf-8").read()


def loop_sections(skill):
    """Every `### ...` section between '## Loops'/'## Sequences'/'## The loop' and '## State'."""
    t = read(skill, "SKILL.md")
    m = re.search(r"^## (?:Loops and sequences|Sequences|The loop and the sequences|The loop|The loops)\b.*?(?=^## State)", t, re.S | re.M)
    if not m:
        return []
    body = m.group(0)
    parts = re.split(r"^### ", body, flags=re.M)[1:]
    return [(p.split("\n", 1)[0].strip(), p) for p in parts]


def test_every_skill_has_the_five_files():
    for skill in ALL:
        for f in ("SKILL.md", "references/eval.md", "references/schema.md", "references/patterns.md"):
            assert os.path.exists(os.path.join(SKILLS, skill, f)), f"{skill}: missing {f}"


def test_every_section_has_runs_when_and_exits():
    for skill in ALL:
        for title, body in loop_sections(skill):
            if title.lower().startswith("the other") or title.lower().startswith("the satellites") or title.lower().startswith("asking the bank"):
                continue  # the rule-4 table, not a section
            for needle in STAGES_OF_A_SECTION:
                assert needle in body, f"{skill} § {title}: missing '{needle}'"


def test_every_loop_has_a_standard_a_budget_and_a_ceiling():
    for skill in ALL:
        for title, body in loop_sections(skill):
            if "(the loop)" not in title.lower() and not title.startswith("Improve"):
                continue
            flat = " ".join(body.split())
            for needle in ("**Standard:**", "**Budget:**"):
                assert needle in flat, f"{skill} § {title}: missing {needle}"
            assert "ceiling" in flat or "two rounds" in flat or "two rows" in flat or "two reps" in flat or "two weekly" in flat, \
                f"{skill} § {title}: no ceiling at the exit"


def test_loop_sections_stay_short():
    # the skeleton (skill-shape rule 3): ~300 words per loop; hard ceiling 600
    for skill in ALL:
        for title, body in loop_sections(skill):
            if "(the loop)" not in title.lower() and not title.startswith("Improve"):
                continue
            n = len(body.split())
            assert n <= 600, f"{skill} § {title}: {n} words — a loop is a skeleton, not a procedure"


def test_one_owner_per_schema_file_and_manifest_agrees():
    schemas = cf.load_schemas(SKILLS)
    for name, s in schemas.items():
        assert s.get("owner") in ALL, f"{name}: owner {s.get('owner')!r} is not a skill"
    for fname, owner in MANIFEST.items():
        if fname in schemas:
            assert schemas[fname]["owner"] in owner, f"{fname}: schema owner {schemas[fname]['owner']} vs manifest '{owner}'"


def test_cross_skill_links_resolve():
    problems = [f"{l}: {m}" for l, m in cf.check_skill_prose(os.path.abspath(SKILLS)) if l == "FAIL"]
    assert not problems, "\n".join(problems)


def test_session_close_names_its_scripts_and_the_subagent_fact():
    for skill in ALL:
        t = read(skill, "SKILL.md")
        m = re.search(r"\*\*Session close[^*]*\*\*(.*?)(?=^## |\Z)", t, re.S | re.M)
        assert m, f"{skill}: no Session close"
        close = m.group(1)
        assert ".py" in close, f"{skill}: Session close names no script"
        assert "subagent" in close or "checker" in close.lower(), f"{skill}: Session close does not state the subagent fact"


def test_eval_is_verdict_bearing_and_patterns_has_the_proposal_rule():
    for skill in ALL:
        e = read(skill, "references", "eval.md")
        assert "## Who checks what" in e, skill
        assert "## Boundaries" not in e or "consumer" in e, f"{skill}: § Boundaries must be a consumer bar, not the skill's own conduct"
        p = read(skill, "references", "patterns.md")
        assert "never self-adopted" in p, skill


def test_no_reference_restates_a_loop_rule_verbatim():
    # a sentence of 12+ words that appears in SKILL.md's loop sections AND in a
    # reference is a second authority (the class cut in every review)
    for skill in ALL:
        loops = " ".join(body for _, body in loop_sections(skill))
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", " ".join(loops.split())) if len(s.split()) >= 12]
        refs = " ".join(" ".join(read(skill, "references", r).split()) for r in ("eval.md", "schema.md", "patterns.md"))
        dupes = [s for s in sentences if s in refs]
        assert not dupes, f"{skill}: restated in a reference: {dupes[0][:90]!r}"
