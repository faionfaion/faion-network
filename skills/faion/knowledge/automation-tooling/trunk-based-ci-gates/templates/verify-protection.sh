# purpose: Verify required-status list matches CI job names
# consumes: input artefacts described in AGENTS.md ## Prerequisites
# produces: artefact conforming to content/02-output-contract.xml for trunk-based-ci-gates
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

#!/bin/sh
# Inputs: REPO (owner/name), BRANCH
set -e
REPO=${REPO:-faionfaion/faion-network}
BRANCH=${BRANCH:-main}

REQUIRED=$(gh api "repos/$REPO/branches/$BRANCH/protection" \
  --jq '.required_status_checks.contexts | sort | join(",")')

JOBS=$(grep -oE '^\s{2}[a-zA-Z0-9_-]+:$' .github/workflows/ci.yml \
  | tr -d ' :' | sort | paste -sd,)

if [ "$REQUIRED" != "$JOBS" ]; then
  echo "MISMATCH: required-status=$REQUIRED but jobs=$JOBS" >&2
  exit 1
fi
echo "OK"
