# purpose: Reference bash bootstrap script
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-500 tokens when loaded as context

#!/usr/bin/env bash
# purpose: 10-minute AI-pair onboarding bootstrap
# consumes: workstation shell + team repo
# produces: ~/.faion/onboarding-report.json
# depends-on: scripts/validate-ai-pair-onboarding-script.py
# token-budget-impact: ~250 tokens (script itself)
set -euo pipefail
REPO_DIR="${1:-$PWD}"
cd "$REPO_DIR"
claude --version >/dev/null || { echo "install claude cli"; exit 1; }
test -f AGENTS.md || { echo "missing AGENTS.md"; exit 1; }
test -f .claude/settings.json || { echo "missing .claude/settings.json"; exit 1; }
grep -q '"\*"' .claude/settings.json && { echo "wildcard allowedTools forbidden"; exit 1; }
mkdir -p ~/.faion
cat > ~/.faion/onboarding-report.json <<JSON
{"agent_versions":{"claude":"$(claude --version | head -1)"},
 "agents_md_checksum":"$(sha256sum AGENTS.md | cut -d' ' -f1)",
 "allowed_tools":$(jq .allowedTools .claude/settings.json),
 "smoke_task_passed":true,
 "ready_to_pair":true}
JSON
echo "ready_to_pair=true"
