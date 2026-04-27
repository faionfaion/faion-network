#!/usr/bin/env bash
# ci-a11y-gate.sh — Fail build if new Critical a11y violations introduced vs baseline.
# Usage: ./ci-a11y-gate.sh [baseline-file]
#   baseline-file: JSON from a previous axe scan (default: a11y-baseline.json)
#   Create initial baseline: run once and save output as a11y-baseline.json
set -euo pipefail

BASELINE="${1:-a11y-baseline.json}"
CURRENT="a11y-current.json"

npx axe-cli \
  --browser chrome \
  --tags wcag2a,wcag2aa \
  --reporter json \
  "$(cat urls.txt)" > "$CURRENT"

python3 - <<'EOF'
import json
import os
import sys

baseline = (
    json.load(open("a11y-baseline.json"))
    if os.path.exists("a11y-baseline.json")
    else {"violations": []}
)
current = json.load(open("a11y-current.json"))

baseline_ids = {v["id"] for v in baseline.get("violations", [])}
new_violations = [
    v for v in current.get("violations", [])
    if v["id"] not in baseline_ids and v["impact"] == "critical"
]

if new_violations:
    print(f"FAIL: {len(new_violations)} new Critical a11y violations introduced:")
    for v in new_violations:
        print(f"  - {v['id']}: {v['description']}")
    sys.exit(1)

print("PASS: No new Critical a11y violations.")
EOF
