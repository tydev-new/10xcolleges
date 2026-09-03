"""The data-model registry (docs/data-model.md § Every file) and the skills agree.

One owner per file; the owner's references/schema.md has a section for it;
no other skill claims it under Owns; every schema link resolves; the
provenance tag list is stated once, in data-model.md, and every schema
that lists tags uses only those.
"""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DM = os.path.join(ROOT, "docs", "data-model.md")
SKILLS = os.path.join(ROOT, "skills")
SCHEMAS = os.path.join(ROOT, "schemas")


def registry():
    text = open(DM, encoding="utf-8").read()
    sec = text.split("## Every file", 1)[1].split("Shipped with the plugin", 1)[0]
    rows = []
    for line in sec.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        path, cls, owner, also, _ = cells
        rows.append({"path": path.strip("`"), "class": cls, "owner": owner, "also": also})
    return rows


def owner_skill(cell):
    m = re.match(r"([a-z-]+)", cell)
    return m.group(1) if m else None


def converted(skill):
    return skill in ("student-intake", "essay-coach", "major-fit", "rec-request", "app-tracker", "counselor-package", "college-app")


def owns_clause(skill):
    s = open(os.path.join(SKILLS, skill, "SKILL.md"), encoding="utf-8").read()
    m = re.search(r"^## State\s*\n(.*?)(?=\n\*\*|\n## )", s, re.S | re.M)
    return m.group(1) if m else ""


class Registry(unittest.TestCase):
    def test_table_parses_and_has_one_owner_per_file(self):
        rows = registry()
        self.assertGreater(len(rows), 10)
        for r in rows:
            self.assertTrue(owner_skill(r["owner"]) or r["owner"].startswith("`"), r)

    def test_converted_owner_has_a_schema_section_and_a_link(self):
        for r in registry():
            sk = owner_skill(r["owner"])
            if not sk or not converted(sk):
                continue
            base = os.path.basename(r["path"])
            self.assertIn("[schema](", r["owner"], f"{r['path']}: owner {sk} is converted — the registry row needs its schema link")
            link = re.search(r"\[schema\]\(([^)]+)\)", r["owner"]).group(1)
            target = os.path.normpath(os.path.join(os.path.dirname(DM), link))
            self.assertTrue(os.path.exists(target), f"{r['path']}: link {link} does not resolve")
            schema = open(target, encoding="utf-8").read()
            self.assertTrue(re.search(r"^## `%s`" % re.escape(base), schema, re.M), f"{target}: no `## `{base}`` section")

    def test_converted_owner_claims_it_and_nobody_else_does(self):
        for r in registry():
            sk = owner_skill(r["owner"])
            if not sk or not converted(sk):
                continue
            base = os.path.basename(r["path"])
            self.assertIn(base.split("-NN")[0], owns_clause(sk), f"{sk} § State does not list `{base}` under Owns")
            for other in os.listdir(SKILLS):
                if other == sk or not converted(other):
                    continue
                clause = owns_clause(other).split("Appends")[0]  # appends are allowed
                self.assertNotIn(f"`{base}`", clause, f"{other} § State claims `{base}`, owned by {sk}")

    def test_provenance_tags_stated_once(self):
        dm = open(DM, encoding="utf-8").read().split("## Provenance", 1)[1].split("\n## ", 1)[0]
        allowed = set(re.findall(r"`\[([a-z]+)", dm))
        self.assertIn("packet", allowed); self.assertIn("worksheet", allowed)
        if os.path.exists(SCHEMAS):
            for sf in os.listdir(SCHEMAS):
                p = os.path.join(SCHEMAS, sf)
                if not os.path.isfile(p):
                    continue
                used = set(re.findall(r"`\[([a-z]+)(?: YYYY-MM-DD)?\]`", open(p, encoding="utf-8").read()))
                self.assertTrue(used <= allowed, f"{sf} lists tags not in data-model § Provenance: {used - allowed}")

    def test_workspace_template_names_the_data_model(self):
        t = open(os.path.join(ROOT, "templates", "workspace-CLAUDE.md"), encoding="utf-8").read()
        self.assertIn("docs/data-model.md", t)
        self.assertIn("owns each file", t)


if __name__ == "__main__":
    unittest.main()
