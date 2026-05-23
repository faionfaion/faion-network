#!/usr/bin/env bash
# purpose: Interruption handler skeleton draining via SIGTERM in 90s
# consumes: env vars + secrets-manager refs (see content/02-output-contract.xml)
# produces: artefact conforming to fco-spot-instances schema
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200 tokens when loaded as context

set -euo pipefail
echo "skeleton — fill per artefact"
