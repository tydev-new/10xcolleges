#!/usr/bin/env python3
"""Word counts for every skill — run on every skill prose change (PROCESS.md).

The soft budget is ~900 words per SKILL.md body (PRINCIPLES rule 14: small enough to
read; depth belongs in references/ loaded when the work reaches it). Exceeding the
budget triggers a review, never a build failure — the meter exists so growth is a
decision instead of a drift.

Usage:
    word_report.py            # report all skills
    word_report.py --check    # exit 1 if any skill exceeds the soft budget (for CI)
"""

import sys
from pathlib import Path

SOFT_TARGET = 900

SKILLS = Path(__file__).resolve().parent.parent / "skills"


def words(path):
    return len(path.read_text().split())


def main():
    over = []
    total = 0
    for skill_dir in sorted(SKILLS.iterdir()):
        body = skill_dir / "SKILL.md"
        if not body.exists():
            continue
        n = words(body)
        total += n
        flag = "  ← over soft budget, review the growth" if n > SOFT_TARGET else ""
        print(f"{n:>6}  {skill_dir.name}/SKILL.md{flag}")
        if n > SOFT_TARGET:
            over.append(skill_dir.name)
        refs = sorted((skill_dir / "references").glob("*.md")) \
            if (skill_dir / "references").is_dir() else []
        for ref in refs:
            print(f"{words(ref):>6}    references/{ref.name}")
    print(f"{total:>6}  total across SKILL.md bodies (soft budget {SOFT_TARGET}/skill)")
    if over and "--check" in sys.argv:
        print(f"\nOver budget: {', '.join(over)} — split into references/ or justify "
              "in the commit message.")
        sys.exit(1)


if __name__ == "__main__":
    main()
