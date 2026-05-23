#!/usr/bin/env bash
# purpose: Restic backup + forget --prune + weekly check skeleton
# consumes: env vars + secrets-manager refs (see content/02-output-contract.xml)
# produces: artefact conforming to backup-filesystem-restic schema
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200 tokens when loaded as context

set -euo pipefail
echo "skeleton — fill per artefact"
