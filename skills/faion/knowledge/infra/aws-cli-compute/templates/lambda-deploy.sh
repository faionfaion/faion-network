#!/usr/bin/env bash
# purpose: Lambda zip + update-function-code skeleton
# consumes: inputs declared in content/02-output-contract.xml
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~300-800 tokens when loaded as context

# AWS CLI Compute and Storage Operations (EC2 S3 Lambda) — lambda-deploy.sh
set -euo pipefail

PROFILE="${AWS_PROFILE:-default}"
REGION="${AWS_REGION:-us-east-1}"

usage() {
  cat <<EOF
Usage: $(basename "$0") [args]
  AWS_PROFILE  profile to use (default: default)
  AWS_REGION   region to operate in (default: us-east-1)
See AGENTS.md for the exact arg signature per operation.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

# Replace the body with the actual CLI invocation. Default to JSON output.
echo "Skeleton — fill in the actual command. profile=$PROFILE region=$REGION"
