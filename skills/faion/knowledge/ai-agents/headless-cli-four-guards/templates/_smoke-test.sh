#!/usr/bin/env bash
# purpose: smallest valid four-guard invocation for the linter
# consumes: nothing
# produces: example claude invocation matching content/02-output-contract.xml
# depends-on: claude on PATH (not actually run by lint)
# token-budget-impact: ~0 — purely textual
set -euo pipefail
TASK="smoke task"
claude -p "$TASK" \
  --allowedTools "Read,Edit,Bash(pytest:*)" \
  --max-turns 20 \
  < /dev/null
