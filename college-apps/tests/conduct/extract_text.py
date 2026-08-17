#!/usr/bin/env python3
"""Reassemble a claude -p stream-json transcript.

`claude -p` prints only the final assistant block; prose emitted between tool calls is
silently dropped (the sibling 10xjobs harness lost a verdict to this before finding it).
Every runner therefore captures `--output-format stream-json --verbose` and this script
rebuilds the full assistant text.

Usage:
    extract_text.py run.jsonl            # all assistant text, in order
    extract_text.py --skills run.jsonl   # which skills the agent actually loaded
"""

import json
import sys


def events(path):
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue  # truncated tail of a killed run — keep what parsed


def main():
    args = sys.argv[1:]
    skills_mode = "--skills" in args
    paths = [a for a in args if not a.startswith("--")]
    if len(paths) != 1:
        sys.exit(__doc__)

    for ev in events(paths[0]):
        if ev.get("type") != "assistant":
            continue
        for block in ev.get("message", {}).get("content", []):
            if skills_mode:
                if block.get("type") == "tool_use" and block.get("name") == "Skill":
                    print(block.get("input", {}).get("skill", "?"))
            elif block.get("type") == "text" and block.get("text"):
                print(block["text"])
                print()


if __name__ == "__main__":
    main()
