# purpose: Restic backup script — production-ready bash with retention prune
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (spec)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

#!/usr/bin/env bash
set -euo pipefail

export RESTIC_REPOSITORY="${RESTIC_REPOSITORY:?missing}"
export RESTIC_PASSWORD="${RESTIC_PASSWORD:?missing}"

TARGETS=("/var/lib/postgresql" "/etc")

restic snapshots >/dev/null 2>&1 || restic init
restic backup --tag prod "${TARGETS[@]}"
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
restic check
