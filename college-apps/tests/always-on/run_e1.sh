#!/bin/bash
# Conduct-harness RUNNER template — copy to tests/always-on/run_e1.sh and
# fill the four HOST blocks. Everything else is the kit's: the vault, targeted
# cases by default, bounded concurrency, the reused-tag warning.
#
# Usage: CASES="<case> ..." ./run_e1.sh <tag>     (CASES=all · TRIALS=n · MODEL · PAR)
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$ROOT/../.." && pwd)"
RESULTS="$ROOT/results/e1-$1"
mkdir -p "$RESULTS"
[ -n "$(ls -A "$RESULTS" 2>/dev/null)" ] && echo "REUSED TAG: $RESULTS already has results — existing cases will be SKIPPED, not re-run; pick a fresh tag for a new measurement" >&2
MODEL="${MODEL:-sonnet}"
TRIALS="${TRIALS:-1}"

# ---- HOST 1: the real workspace to lock for the run (personal data) --------
REALWS="$HOME/Documents/10xcolleges/students"
vault_unlock() { find "$REALWS" -flags +uchg -exec chflags nouchg {} + 2>/dev/null; }
vault_lock()   { find "$REALWS" -type f -not -path '*/.damaged*' -exec chflags uchg {} + 2>/dev/null; }
[ -d "$REALWS" ] && { vault_lock; trap vault_unlock EXIT; trap 'vault_unlock; kill 0 2>/dev/null' INT TERM; }

# ---- HOST 2: the suite's cases ---------------------------------------------
ALL_CASES="e1-just-write-it e2-review-round"
CASES="${CASES:-}"
[ -z "$CASES" ] && { echo "usage: CASES=\"<case> ...\" $0 <tag>   (CASES=all for the suite: $ALL_CASES)" >&2; rmdir "$RESULTS" 2>/dev/null; exit 2; }
[ "$CASES" = all ] && CASES="$ALL_CASES"

for trial in $(seq 1 "$TRIALS"); do
for case_name in $CASES; do
  while [ "$(jobs -rp | wc -l)" -ge "${PAR:-6}" ]; do sleep 2; done
  (
    CASE="$ROOT/cases/$case_name"
    out="$RESULTS/$case_name-t$trial"
    [ -f "$out.md" ] && { echo "skip $case_name t$trial (exists)"; exit 0; }
    WS="$(mktemp -d)"
    # ---- HOST 3: plant the workspace — fixtures, the case's ws-seed, the
    #      workspace rules file, and ONLY the skills under test ---------------
    cp -r "$CASE/ws-seed/." "$WS/" 2>/dev/null
    mkdir -p "$WS/.claude/skills"    cp -r "$REPO"/skills/essay-coach "$REPO"/skills/college-research "$WS/.claude/skills/"
    # the skills address the plugin root as ${CLAUDE_PLUGIN_ROOT}; in a
    # copied-skills install that is unset, so plant docs/ and scripts/ where
    # a plugin root would be and export it
    mkdir -p "$WS/.claude/plugin-root"; cp -r "$REPO/docs" "$REPO/scripts" "$REPO/config" "$WS/.claude/plugin-root/"
    export CLAUDE_PLUGIN_ROOT="$WS/.claude/plugin-root"
    echo "=== $case_name / trial $trial -> $WS"
    : > "$out.err"
    ( cd "$WS" && claude -p "$(cat "$CASE/prompt.md")" \
        --model "$MODEL" --dangerously-skip-permissions \
        --setting-sources project --output-format stream-json --verbose \
      ) > "$out.turn1.stream.json" 2>> "$out.err"
    python3 "$ROOT/extract_text.py" "$out.turn1.stream.json" > "$out.md"
    python3 "$ROOT/dump_tools.py" "$out".turn*.stream.json > "$out.tools.txt" 2>/dev/null
    # ---- HOST 4: what the judge must see of the workspace AFTER the run -----
    mkdir -p "$out-ws"; cp -r "$WS/students" "$out-ws/" 2>/dev/null
    (cd "$WS" && find students -type f | sort) > "$out-ws/_listing.txt" 2>/dev/null
    rm -rf "$WS"
  ) &
done
done
wait
echo "done: $RESULTS"
