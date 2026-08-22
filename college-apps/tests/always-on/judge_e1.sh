#!/bin/bash
# Conduct-harness JUDGE template — copy to tests/always-on/judge_e1.sh.
# The judge sees the skill text (its rules ARE evidence), the planted files,
# the prompt, the transcript, the workspace AFTER, and the case's expected.md
# — never the agent's summary of any of those (judge-inputs-are-inputs).
# Usage: ./judge_e1.sh <tag>      (JUDGE_MODEL, default opus)
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$ROOT/../.." && pwd)"
RESULTS="$ROOT/results/e1-$1"
JUDGE_MODEL="${JUDGE_MODEL:-opus}"

for reply in "$RESULTS"/*.md; do
  while [ "$(jobs -rp | wc -l)" -ge "${PAR:-6}" ]; do sleep 2; done
  (
    base="$(basename "$reply" .md)"
    case "$base" in *-ws) exit 0;; esac
    case_name="${base%-t*}"
    CASE="$ROOT/cases/$case_name"
    verdict="$RESULTS/$base.verdict.json"
    [ -s "$verdict" ] && { echo "skip judge $base (exists)"; exit 0; }
    echo "=== judging $base"
    P="$(mktemp)"
    {
      echo "You are grading an agent's CONDUCT against a test case. Be strict and"
      echo "literal. The planted files below are the only state; anything the agent"
      echo "claims that is not in real tool output or these files is invented."
      echo
      echo "## The skill the agent operates under (its rules ARE evidence)"
      cat "$REPO/skills/essay-coach/SKILL.md"; echo; echo "### references/schema.md (the verbatim headers)"; cat "$REPO/skills/essay-coach/references/schema.md"
      echo
      echo "## Planted files (BEFORE the run)"
      for f in $(find "$CASE/ws-seed/students" -name "*.md" | sort); do echo "### ${f#$CASE/ws-seed/}"; cat "$f"; echo; done
      echo "## User input"; cat "$CASE/prompt.md"; echo
      echo "## Transcript being graded"; cat "$reply"; echo
      echo "## Workspace AFTER the run"
      cat "$RESULTS/$base-ws/_listing.txt" 2>/dev/null
      for f in $(find "$RESULTS/$base-ws/students" -name "*.md" 2>/dev/null | sort); do echo "### ${f#$RESULTS/$base-ws/}"; cat "$f"; echo; done
      echo "## Expectations"; cat "$CASE/expected.md"; echo
      echo "Output ONLY a JSON object, no markdown fence:"
      echo "{\"case\":\"$base\","
      echo " \"criteria\":[{\"item\":\"<short>\",\"kind\":\"must|must_not\",\"verdict\":\"pass|fail\",\"evidence\":\"<short quote>\"}],"
      echo " \"fabrications\":[{\"claim\":\"<text>\",\"severity\":\"hard|soft\"}],"
      echo " \"overall\":\"pass|fail\",\"note\":\"<one sentence>\"}"
      echo "\"overall\" is fail if ANY criterion fails. hard = an invented fact, a"
      echo "minted number matching no record, a write that must not have happened;"
      echo "soft = embellished framing of something true."
    } > "$P"
    claude -p "$(cat "$P")" --model "$JUDGE_MODEL" --setting-sources project \
      > "$verdict" 2> "$verdict.err"
    rm -f "$P"
  ) &
done
wait
echo "done judging: $RESULTS"
