#!/usr/bin/env bash
# purpose: CI gate script enforcing async hygiene and coverage threshold
# consumes: see AGENTS.md Prerequisites
# produces: ASP.NET Core Patterns code
# depends-on: content/02-output-contract.xml schema
# token-budget-impact: ~300 tokens of agent context to invoke
# dotnet-gate.sh — fail PR if async hygiene or coverage slips.
# Usage: dotnet-gate.sh path/to/sln.sln [coverage_threshold]
set -euo pipefail
SLN="${1:?usage: dotnet-gate.sh SOLUTION [THRESHOLD]}"
THRESH="${2:-70}"
dotnet build "$SLN" -warnaserror -p:TreatWarningsAsErrors=true
dotnet test "$SLN" --collect:"XPlat Code Coverage" --results-directory /tmp/cov
COV_FILE=$(find /tmp/cov -name 'coverage.cobertura.xml' | head -1)
[ -n "$COV_FILE" ] || { echo "no coverage file"; exit 1; }
python3 - "$COV_FILE" "$THRESH" <<'PY'
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.argv[1]); root = tree.getroot()
rate = float(root.attrib.get("line-rate", 0)) * 100
thr = float(sys.argv[2])
print(f"line coverage: {rate:.1f}% (threshold {thr}%)")
sys.exit(0 if rate >= thr else 1)
PY
echo "Gate passed"