# purpose: Bash wrapper applying wall-clock timeout
# consumes: input artefacts described in AGENTS.md ## Prerequisites
# produces: artefact conforming to content/02-output-contract.xml for puppeteer-agent-workflow
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

#!/bin/sh
# Run worker with a hard wall-clock timeout
ARTIFACT_PATH=/tmp/agent-run/result.json
timeout 60 node worker.mjs "$1" || {
  echo "worker failed (exit $?)" >&2
  exit 1
}
echo "$ARTIFACT_PATH"
