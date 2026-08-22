#!/bin/bash
# Multi-turn conduct RUNNER template — a second model plays the person from
# a persona file; the agent's reply is fed back; the judge sees the whole
# exchange. Copy to tests/always-on/run_e3.sh and fill the HOST blocks.
#
# A case directory holds: persona.md (who they are, TRUE FACTS they may draw
# on, a BEHAVIOR SCRIPT of beats by message number, what they will never
# say) · opener.txt (message 1) · turns.txt (how many messages) · ws-seed/
# · skills.txt (the skills under test, one per line) · expected.md.
#
# Usage: CASES="<case> ..." ./run_e3.sh <tag>   (CASES=all · TRIALS=n · MODEL · SIM_MODEL · PAR)
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$ROOT/../.." && pwd)"
RESULTS="$ROOT/results/e3-$1"
mkdir -p "$RESULTS"
[ -n "$(ls -A "$RESULTS" 2>/dev/null)" ] && echo "REUSED TAG: $RESULTS already has results — existing cases will be SKIPPED, not re-run; pick a fresh tag for a new measurement" >&2
MODEL="${MODEL:-sonnet}"
SIM_MODEL="${SIM_MODEL:-sonnet}"
TRIALS="${TRIALS:-1}"

# ---- HOST 1: the real workspace to lock for the run -------------------------
REALWS="$HOME/Documents/10xcolleges/students"
vault_unlock() { find "$REALWS" -flags +uchg -exec chflags nouchg {} + 2>/dev/null; }
vault_lock()   { find "$REALWS" -type f -not -path '*/.damaged*' -exec chflags uchg {} + 2>/dev/null; }
[ -d "$REALWS" ] && { vault_lock; trap vault_unlock EXIT; trap 'vault_unlock; kill 0 2>/dev/null' INT TERM; }

# ---- HOST 2: the suite's cases -----------------------------------------------
ALL_CASES="e3-review-rounds i1-intake-rounds"
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
    WS="$(mktemp -d)"; SIMD="$(mktemp -d)"
    cp -R "$CASE/ws-seed/." "$WS/" 2>/dev/null
    mkdir -p "$WS/.claude/skills"
    for sk in $(cat "$CASE/skills.txt"); do cp -r "$REPO/skills/$sk" "$WS/.claude/skills/"; done
    SK1="$(head -1 "$CASE/skills.txt")"
    [ -f "$WS/.claude/skills/$SK1/SKILL.md" ] || { echo "PLANT FAILED: no SKILL.md in $WS/.claude/skills/$SK1" >&2; exit 3; }
    # ---- HOST 3: the skills address ${CLAUDE_PLUGIN_ROOT}; plant docs/ scripts/ config/ there
    mkdir -p "$WS/.claude/plugin-root"; cp -r "$REPO/docs" "$REPO/scripts" "$REPO/config" "$REPO/templates" "$WS/.claude/plugin-root/"
    export CLAUDE_PLUGIN_ROOT="$WS/.claude/plugin-root"
    echo "=== $case_name / trial $trial -> $WS"
    : > "$out.err"; : > "$out.transcript.md"
    MSG="$(cat "$CASE/opener.txt")"
    N="$(cat "$CASE/turns.txt" 2>/dev/null || echo 4)"
    for turn in $(seq 1 "$N"); do
      printf '\n## Student (turn %s)\n%s\n' "$turn" "$MSG" >> "$out.transcript.md"
      cont=""; [ "$turn" -gt 1 ] && cont="--continue"
      ( cd "$WS" && claude -p $cont "$MSG" --model "$MODEL" --dangerously-skip-permissions \
          --setting-sources project --output-format stream-json --verbose \
        ) > "$out.turn$turn.stream.json" 2>> "$out.err"
      REPLY="$(python3 "$ROOT/extract_text.py" "$out.turn$turn.stream.json")"
      printf '\n## Agent (turn %s)\n%s\n' "$turn" "$REPLY" >> "$out.transcript.md"
      mkdir -p "$out-ws/after-turn$turn"; cp -r "$WS/students" "$out-ws/after-turn$turn/" 2>/dev/null
      [ "$turn" -eq "$N" ] && break
      SIMP="$(mktemp)"
      { cat "$CASE/persona.md"; echo; echo "=== CONVERSATION SO FAR ==="; cat "$out.transcript.md"
        echo; echo "You have sent $turn message(s) so far (the '## Student' headings above)."
        echo "This will be your message number $((turn + 1)) of about $N. Deliver the"
        echo "BEHAVIOR SCRIPT beat labeled **Message $((turn + 1))** — if it gives text,"
        echo "paste that text exactly. If an earlier beat was skipped, deliver it first."
        echo "Never re-send a message you already sent; a repeat is a failed turn."
        echo "Output ONLY your message."
      } > "$SIMP"
      MSG="$( cd "$SIMD" && claude -p "$(cat "$SIMP")" --model "$SIM_MODEL" --setting-sources project 2>> "$out.err" )"
      rm -f "$SIMP"
      [ -z "$MSG" ] && { echo "sim returned empty at turn $turn" >> "$out.err"; break; }
    done
    cp "$out.transcript.md" "$out.md"
    # ---- HOST 4: what the judge must see of the workspace AFTER the run -----
    mkdir -p "$out-ws"; cp -r "$WS/students" "$out-ws/" 2>/dev/null
    (cd "$WS" && find students -type f | sort) > "$out-ws/_listing.txt" 2>/dev/null
    python3 "$ROOT/dump_tools.py" "$out".turn*.stream.json > "$out.tools.txt" 2>/dev/null
    rm -rf "$WS" "$SIMD"
  ) &
done
done
wait
echo "done: $RESULTS"
