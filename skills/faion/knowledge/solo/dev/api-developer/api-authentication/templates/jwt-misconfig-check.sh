#!/usr/bin/env bash
# purpose: Template helper for API Authentication (jwt-misconfig-check.sh).
# consumes: see content/02-output-contract.xml inputs for api-authentication
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
# jwt-misconfig-check.sh — CI smoke test for JWT misconfiguration.
# Fails if the API accepts alg:none tokens or tokens with wrong audience.
# Requires: jwt-cli (mike-engel/jwt-cli) and JWT_SECRET env var.
#
# Usage: JWT_SECRET=mysecret ./jwt-misconfig-check.sh https://api.example.com
set -euo pipefail

HOST="${1:?Usage: $0 https://api.example.com}"

if ! command -v jwt &>/dev/null; then
  echo "ERROR: jwt-cli not found. Install: brew install mike-engel/jwt-cli/jwt-cli"
  exit 1
fi

# Token with alg:none — must be rejected with 401
NONE_TOKEN=$(jwt encode --alg none '{"sub":"attacker","exp":9999999999}' '' 2>/dev/null || true)

# Token with wrong audience — must be rejected with 401
WRONG_AUD_TOKEN=$(jwt encode --alg HS256 --secret "${JWT_SECRET:?JWT_SECRET not set}" \
  '{"sub":"attacker","aud":"other-service","exp":9999999999}')

failures=0

for label_token in "alg:none:${NONE_TOKEN}" "wrong-aud:${WRONG_AUD_TOKEN}"; do
  label="${label_token%%:*}"
  token="${label_token#*:}"
  code=$(curl -s -o /dev/null -w '%{http_code}' \
    "${HOST}/api/users/me" -H "Authorization: Bearer ${token}")
  if [ "$code" != "401" ]; then
    echo "FAIL: ${label} token was accepted with status ${code} (expected 401)"
    failures=$((failures + 1))
  else
    echo "OK: ${label} token rejected (401)"
  fi
done

[ $failures -eq 0 ] || exit 1
echo "All JWT misconfig checks passed"
