#!/usr/bin/env bash
# __faion_header_v1__
# purpose: Ramp helper: bump rollout_percent in steps, wait for guardrails between
# consumes: see content/02-output-contract.xml
# produces: spec; depends-on: content/01-core-rules.xml#deterministic-per-user
# faion_header_json: {"__faion_header__":{"purpose":"Ramp helper: bump rollout_percent in steps, wait for guardrails between","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#deterministic-per-user","token_budget_impact":"~150 tokens when loaded"}}
set -euo pipefail
FLAG="$1"; shift
STEPS=("$@")
for pct in "${STEPS[@]}"; do
  echo "Ramping $FLAG to $pct%"
  # caller wires this to their flag-service / config-edit method
  curl -fsS -X PATCH "https://flags.internal/flags/$FLAG" -d "{\"rollout_percent\":$pct}"
  sleep 600
done
