#!/usr/bin/env python3
"""Dump the tool-call sequence from a claude stream-json transcript.

The judge needs to see BEHAVIOR the reply text can't show: what prompts
the persona subagents (Task calls) actually received, and whether the
mechanical checker ran (Bash calls). Prints one line per tool call; Task
and Bash inputs are included (truncated) because t10's baits live there.
"""
import json, sys

LIMIT = 2000

def walk(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = ev.get("message") or {}
            for block in msg.get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    name = block.get("name", "?")
                    inp = block.get("input") or {}
                    # The subagent tool is named "Task" or "Agent" depending on
                    # harness version — missing one poisoned the judge inputs
                    # once (t10 v1, 2026-08-16). Match both.
                    if name in ("Task", "Agent"):
                        text = (inp.get("prompt") or "")[:LIMIT]
                        print(f"TOOL {name}(subagent) type={inp.get('subagent_type','?')} "
                              f"desc={inp.get('description','')!r}")
                        print(f"  PROMPT: {text!r}")
                    elif name == "Bash":
                        print(f"TOOL Bash: {(inp.get('command') or '')[:400]!r}")
                    else:
                        keys = ",".join(sorted(inp)) if isinstance(inp, dict) else ""
                        print(f"TOOL {name} ({keys})")

for p in sys.argv[1:]:
    print(f"===== {p} =====")
    walk(p)
