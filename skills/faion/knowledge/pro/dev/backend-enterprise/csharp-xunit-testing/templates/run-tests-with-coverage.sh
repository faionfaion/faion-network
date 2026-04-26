#!/usr/bin/env bash
# run-tests-with-coverage.sh — agent entry point for test + coverage loop
# Usage: bash run-tests-with-coverage.sh <test-project-path> [threshold]
# Example: bash run-tests-with-coverage.sh MyApp.Tests/ 80
set -euo pipefail

PROJ="${1:?test project path required}"
THRESHOLD="${2:-80}"

dotnet test "$PROJ" \
  --collect:"XPlat Code Coverage" \
  --results-directory ./TestResults \
  --logger "trx;LogFileName=test_results.trx" \
  /p:Threshold="$THRESHOLD" /p:ThresholdType=line /p:ThresholdStat=total

COV=$(find TestResults -name 'coverage.cobertura.xml' | head -1)
if [[ -z "$COV" ]]; then
  echo "No coverage file found" >&2; exit 1
fi

reportgenerator \
  -reports:"$COV" \
  -targetdir:./coverage \
  -reporttypes:JsonSummary

jq '.summary.linecoverage' coverage/Summary.json
