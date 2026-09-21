#!/usr/bin/env python3
"""Build BOOTSTRAP.md — one file an AI assistant can read when a user pastes the repo link.

It is generated, never edited by hand: the orchestrator skill first, then the voice and
citation guides, then every other workflow skill. `tests/test_docs.py` fails if it is stale.

    python3 skills/core/scripts/make_bootstrap.py            # writes ../../BOOTSTRAP.md
    python3 skills/core/scripts/make_bootstrap.py --check    # exit 1 if out of date
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent.parent.parent          # college-apps/
REPO = PLUGIN.parent
OUT = REPO / "BOOTSTRAP.md"
RAW = "https://raw.githubusercontent.com/tydev-new/10xcolleges/main"

HEADER = f"""# 10xcolleges — assistant bootstrap

*Generated from the skills in this repo by `college-apps/skills/core/scripts/make_bootstrap.py`. Do not edit by hand.*

**If you are an AI assistant and a person pasted a link to this repository:** they want you
to act as the 10xcolleges college counselor. Everything you need to do that in one
conversation is in this file. Read it fully, then follow it.

What you can and cannot do here, said plainly to the person:

1. You are following the 10xcolleges skills as text. The Python checkers and generators
   that normally verify every file (`check_*.py`, the tracker spreadsheet, the counselor
   packet) do not run in this setting. Say so once, in one sentence.
2. Every number about a college — admit rate, cost, deadline — must come from the
   college's own website or its Common Data Set, read in this conversation and cited
   with the page and date. You do not have the Scorecard lookup here. Never from memory.
3. Keep the person's files in the shapes described below so they can move to the full
   install later without losing work. Full installs, which do run the checkers:
   - Claude Code, one line: `claude plugin marketplace add tydev-new/10xcolleges && claude plugin install college-apps@10xcolleges`
   - Claude Cowork: Customize → Plugins → Add marketplace → `tydev-new/10xcolleges` → Install
   - Codex, Gemini CLI and other agents that read Agent Skills: `npx skills add tydev-new/10xcolleges`
4. Everything else in the skills applies unchanged: the student's essay is theirs, no
   made-up percentages, affordability is fit, plain language, one next step at a time.

Where paths below say `${{CLAUDE_PLUGIN_ROOT}}/skills/core/...`, the file is at
`{RAW}/college-apps/skills/core/...` — fetch it if you need a schema or template.

---
"""


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)


def build() -> str:
    skills = PLUGIN / "skills"
    order = ["college-app"]
    rest = sorted(p.name for p in skills.iterdir() if p.is_dir() and p.name not in ("core", "college-app"))
    parts = [HEADER]
    for name in order + ["__refs__"] + rest:
        if name == "__refs__":
            for ref in ("voice.md", "citations.md"):
                parts.append(f"\n\n# Reference — {ref}\n\n" + (skills / "core" / "references" / ref).read_text().strip() + "\n")
            continue
        body = strip_frontmatter((skills / name / "SKILL.md").read_text()).strip()
        parts.append(f"\n\n<!-- skill: {name} -->\n" + body + "\n")
    return "".join(parts).rstrip() + "\n"


def main(argv=None):
    argv = argv or sys.argv[1:]
    text = build()
    if "--check" in argv:
        current = OUT.read_text() if OUT.exists() else ""
        if current != text:
            print(f"{OUT.name} is out of date — run: python3 college-apps/skills/core/scripts/make_bootstrap.py", file=sys.stderr)
            return 1
        print(f"{OUT.name} is current ({len(text):,} chars)")
        return 0
    OUT.write_text(text)
    print(f"wrote {OUT} ({len(text):,} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
