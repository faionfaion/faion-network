#!/usr/bin/env bash
# purpose: Wrapper running git bisect with the failing spec as oracle.
# consumes: see content/02-output-contract.xml inputs for spec-driven-debugging
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-700 tokens when loaded as context
set -euo pipefail

GOOD=${1:-}
BAD=${2:-HEAD}
TEST=${3:-tests/test_<area>.py}

if [ -z "$GOOD" ]; then
  echo "usage: $0 <good-sha> <bad-sha=HEAD> <test-path>" >&2
  exit 2
fi

git bisect start "$BAD" "$GOOD"
git bisect run pytest "$TEST" -q
git bisect log
