"""The kit's guarded copies: shapecheck.py's functions are byte-identical to
the host checker's, and PRINCIPLES.md Part 2 is the kit core — either the
core text verbatim (the source repo) or a pointer that adopts
`kit/PRINCIPLES-core.md` unchanged (a host repo). Runs under unittest
(`python3 -m unittest discover -s kit/tests`) and under pytest."""
import ast, os, unittest
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
    i = p.index("## Part 2 — How we build it")
    j = p.find("\n---\n", i); part2 = p[i:j if j > 0 else len(p)].strip()
    core = open(os.path.join(ROOT, "kit", "PRINCIPLES-core.md"), encoding="utf-8").read()
    if "kit/PRINCIPLES-core.md" in part2 and "unchanged" in part2:
        return  # a host adopts the core by pointer — one authoritative copy, in the kit
    assert part2 in core, "PRINCIPLES.md Part 2 drifted from kit/PRINCIPLES-core.md — fix both"


class Kit(unittest.TestCase):  # unittest discovery; pytest collects the bare functions too
    def test_shapecheck(self): test_shapecheck_matches_the_host_checker()
    def test_principles(self): test_principles_core_is_part_two_verbatim()


if __name__ == "__main__":
    unittest.main()
