#!/usr/bin/env bash
# Run one conduct case: plant a fresh workspace, run the agent, snapshot everything.
#
# Usage:
#   ./run_case.sh cases/c6-percentage results/<tag>
#   TRIALS=2 RUNNER_MODEL=claude-sonnet-5 ./run_case.sh cases/c6-percentage results/<tag>
#
# Each trial gets a brand-new mktemp workspace (a probe with a past is not a clean
# room) holding: the shared fixture student, the case's overlay files, the guardrails
# CLAUDE.md intake would have written, and the plugin's skills as project skills with
# ${CLAUDE_PLUGIN_ROOT} resolved to the real plugin path. Re-running skips trials that
# already have output, so a crashed batch resumes.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PLUGIN="$(cd "$HERE/../.." && pwd)"
CASE_DIR="$HERE/${1:?usage: run_case.sh cases/<name> results/<tag>}"
OUT="$HERE/${2:?usage: run_case.sh cases/<name> results/<tag>}"
NAME="$(basename "$CASE_DIR")"
TRIALS="${TRIALS:-1}"
RUNNER_MODEL="${RUNNER_MODEL:-claude-sonnet-5}"
TIMEOUT_S="${TIMEOUT_S:-900}"

[ -f "$CASE_DIR/prompt.md" ] || { echo "no prompt.md in $CASE_DIR"; exit 1; }
mkdir -p "$OUT"

for t in $(seq 1 "$TRIALS"); do
    run="$OUT/$NAME.run$t"
    if [ -s "$run.jsonl" ]; then echo "skip  $run (already exists)"; continue; fi

    ws="$(mktemp -d)"
    mkdir -p "$ws/students"
    cp -r "$HERE/fixtures/jordan-reyes" "$ws/students/jordan-reyes"
    [ -d "$CASE_DIR/workspace" ] && cp -r "$CASE_DIR/workspace/." "$ws/"

    # The treatment condition: guardrails + skills, exactly what a set-up user has.
    cp "$PLUGIN/templates/workspace-CLAUDE.md" "$ws/CLAUDE.md"
    mkdir -p "$ws/.claude/skills"
    cp -r "$PLUGIN/skills/." "$ws/.claude/skills/"
    # Plugin skills get ${CLAUDE_PLUGIN_ROOT} substituted at load; project skills
    # don't, so resolve it here or every doc/script reference in them dangles.
    grep -rl 'CLAUDE_PLUGIN_ROOT' "$ws/.claude/skills" | while read -r f; do
        sed -i "s|\${CLAUDE_PLUGIN_ROOT}|$PLUGIN|g" "$f"
    done

    echo "run   $run ($RUNNER_MODEL)"
    # The allowlist (not --dangerously-skip-permissions, which refuses to run as
    # root) makes the forbidden actions actually available in the throwaway
    # workspace: file writes, script runs, web lookups. A "refusal" from an agent
    # that couldn't act is an artifact, not discipline.
    (
        cd "$ws"
        timeout "$TIMEOUT_S" claude -p "$(cat "$CASE_DIR/prompt.md")" \
            --model "$RUNNER_MODEL" \
            --setting-sources project \
            --allowedTools "Bash" "Write" "Edit" "Read" "Glob" "Grep" "Skill" \
                           "WebFetch" "WebSearch" \
            --output-format stream-json --verbose \
            > "$run.jsonl"
    ) || echo "      (exited nonzero/timeout — recorded, judge sees what happened)"

    python3 "$HERE/extract_text.py" "$run.jsonl" > "$run.txt"
    python3 "$HERE/extract_text.py" --skills "$run.jsonl" > "$run.skills.txt"
    python3 "$PLUGIN/scripts/check_student.py" "$ws/students/jordan-reyes" \
        > "$run.check.txt" 2>&1 || true

    rm -rf "$run-ws"
    mkdir -p "$run-ws"
    cp -r "$ws/students" "$run-ws/students"
    cp "$ws/CLAUDE.md" "$run-ws/CLAUDE.md" 2>/dev/null || true
    # Case overlays outside students/ (e.g. a pasted packet) are part of the record.
    if [ -d "$CASE_DIR/workspace" ]; then
        (cd "$CASE_DIR/workspace" && find . -maxdepth 1 -type f) | while read -r f; do
            cp "$ws/$f" "$run-ws/$f" 2>/dev/null || true
        done
    fi
    rm -rf "$ws"
    echo "done  $run"
done
