# purpose: Shell script: greps domain/ for framework imports; exits 1 if any.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml (domain-driven-design)
# depends-on: content/01-core-rules.xml
# token-budget-impact: small (template is loaded only when an artefact is being authored)
#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-myapp/domain}
if grep -RnE "^(from|import) (django|sqlalchemy|flask|fastapi|requests|aiohttp|httpx)" "$ROOT"; then
  echo "FAIL: framework import found in domain layer"
  exit 1
fi
echo OK
