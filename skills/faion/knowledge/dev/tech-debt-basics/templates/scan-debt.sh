# purpose: template for tech-debt-basics (scan-debt.sh)
# consumes: tech-debt-basics methodology inputs (see AGENTS.md Prerequisites)
# produces: filled-in artefact conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml + tool-runtime in same dir
# token-budget-impact: ~200-400 tokens when loaded as context

#!/usr/bin/env bash
# scan-debt.sh — emit candidate technical debt items as JSONL.
# Pipe output into a triage agent for deduplication and severity classification.
# Usage: scan-debt.sh [src-dir]
set -euo pipefail

ROOT="${1:-.}"

# Code debt: high-complexity functions (CCN > 15)
if command -v lizard >/dev/null 2>&1; then
  lizard -C 15 "$ROOT" --csv 2>/dev/null \
    | awk -F, 'NR>1 && $3+0>15 {
        printf "{\"type\":\"code\",\"location\":\"%s:%s\",\"evidence\":\"CCN=%s\"}\n",
        $NF, $5, $3
      }'
fi

# Test debt: Python files lacking a sibling test_ file
find "$ROOT" -name '*.py' -not -path '*/tests/*' -not -path '*/__pycache__/*' \
  | while read -r f; do
    base=$(basename "$f" .py)
    if ! find "$ROOT" -name "test_${base}.py" -print -quit 2>/dev/null | grep -q .; then
      echo "{\"type\":\"test\",\"location\":\"$f\",\"evidence\":\"no test_${base}.py found\"}"
    fi
  done

# Infra debt: outdated npm dependencies
if [ -f "$ROOT/package.json" ] && command -v npm >/dev/null 2>&1; then
  (cd "$ROOT" && npm outdated --json 2>/dev/null \
    | jq -r 'to_entries[] |
        "{\"type\":\"infra\",\"location\":\"package.json:\(.key)\",\"evidence\":\"outdated \(.value.current)→\(.value.latest)\"}"' \
    2>/dev/null || true)
fi

# Infra debt: outdated Python deps
if [ -f "$ROOT/pyproject.toml" ] && command -v pip >/dev/null 2>&1; then
  pip list --outdated --format=json 2>/dev/null \
    | jq -r '.[] | "{\"type\":\"infra\",\"location\":\"pyproject.toml:\(.name)\",\"evidence\":\"outdated \(.version)→\(.latest_version)\"}"' \
    2>/dev/null || true
fi
