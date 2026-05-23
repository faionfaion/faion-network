#!/usr/bin/env bash
# run-cog-walk.sh — Orchestrate planner -> captures -> evaluators -> cw-findings.
# Input: $1 = spec.md (feature spec), $2 = persona.md
# Output: $OUT/plan.md, $OUT/shots/step_*.json, $OUT/cw-findings.md
# Requires: claude CLI, node, capture.js (Playwright script from walk.py)

set -euo pipefail

SPEC="${1:?Usage: run-cog-walk.sh spec.md persona.md}"
PERSONA="${2:?Usage: run-cog-walk.sh spec.md persona.md}"
OUT="cog-walk-$(date +%Y%m%d-%H%M)"
mkdir -p "$OUT/shots"

echo "=== Step 1: Generate walkthrough plan ==="
claude -p "Run walk-planner on $SPEC with persona $PERSONA.
Produce a filled Walkthrough Planning Template (markdown).
Action sequence MUST be the minimum-clicks happy path. Number each step.
Out of scope: error paths, alternative flows, expert shortcuts." \
  > "$OUT/plan.md"

echo "=== Step 2: Capture per-step screenshots ==="
node capture.js "$OUT/plan.md" "$OUT/shots/"

echo "=== Step 3: Evaluate each step ==="
for s in "$OUT"/shots/step_*.json; do
  echo "  Evaluating: $s"
  claude -p "Run walk-evaluator on step data at $s.
Answer Q1-Q4 for the step. Return JSON: {q1,q2,q3,q4,suggested_fix}.
Each q* has: {ans: yes|no|partial, evidence: string}.
evidence MUST cite a visible element or state what is missing.
Do not assume capabilities the persona lacks." \
    > "${s%.json}.eval.json"
done

echo "=== Step 4: Synthesize cw-findings ==="
claude -p "Synthesize cog-walk evaluation files at $OUT/shots/*.eval.json
and planning template at $OUT/plan.md into a cw-findings.md.
Rules:
- Max 3 High-severity issues.
- Every issue: step number, Q1/Q2/Q3/Q4, one-line fix, affected component.
- Positive findings section: list at least 3 steps that passed.
- Executive summary: max 5 bullets." \
  > "$OUT/cw-findings.md"

echo "Done: $OUT/cw-findings.md"
