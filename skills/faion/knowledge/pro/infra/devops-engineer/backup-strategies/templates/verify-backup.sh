# purpose: Restore-verification script — restores latest snapshot to /tmp + asserts
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (spec)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

#!/usr/bin/env bash
set -euo pipefail

export RESTIC_REPOSITORY="${RESTIC_REPOSITORY:?missing}"
export RESTIC_PASSWORD="${RESTIC_PASSWORD:?missing}"
TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

restic restore latest --target "$TMP"
[[ -d "$TMP/var/lib/postgresql" ]] || { echo "FAIL: pg dir missing"; exit 1; }
echo OK
