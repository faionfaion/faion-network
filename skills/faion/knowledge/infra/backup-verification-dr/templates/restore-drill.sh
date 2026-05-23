#!/usr/bin/env bash
# purpose: Restore-drill skeleton: pull latest backup, restore to scratch, run verification query
# consumes: env vars + secrets-manager refs (see content/02-output-contract.xml)
# produces: artefact conforming to backup-verification-dr schema
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200 tokens when loaded as context

set -euo pipefail
echo "skeleton — fill per artefact"
