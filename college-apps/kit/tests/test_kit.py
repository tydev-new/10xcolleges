"""The kit's guarded copies: shapecheck.py's functions are byte-identical to
the host checker's, and PRINCIPLES-core.md is PRINCIPLES.md Part 2 verbatim."""
import ast, os
HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..", "..")

def _defs(path):
    src = open(path, encoding="utf-8").read()
    out = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.FunctionDef):
            out[n.name] = ast.dump(n)
        elif isinstance(n, ast.Assign) and hasattr(n.targets[0], "id"):
            out[n.targets[0].id] = ast.dump(n)
    return out

def test_shapecheck_matches_the_host_checker():
    host_path = os.environ.get("HOST_CHECKER", os.path.join(ROOT, "skills", "profile", "scripts", "check_files.py"))
    if not os.path.exists(host_path):
        return  # a host that uses shapecheck.py directly has no second copy to guard
    kit = _defs(os.path.join(ROOT, "kit", "shapecheck.py"))
    host = _defs(host_path)
    for name in ("load_schemas", "headings", "norm", "check_file", "check_table",
                 "check_history", "check_skill_prose", "FILE_RE", "FREEFORM", "SECTION_RE"):
        assert kit[name] == host[name], f"{name}: kit/shapecheck.py and check_files.py differ — fix both"

def test_principles_core_is_part_two_verbatim():
    p = open(os.path.join(ROOT, "PRINCIPLES.md"), encoding="utf-8").read()
    i = p.index("## Part 2 — How we build it"); j = p.index("\n---\n", i)
    core = open(os.path.join(ROOT, "kit", "PRINCIPLES-core.md"), encoding="utf-8").read()
    assert p[i:j].strip() in core
