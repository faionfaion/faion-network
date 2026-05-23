# purpose: CLI router: takes goal + stage and prints the picked framework slug
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1500 tokens when loaded as context
#!/usr/bin/env bash
# framework-router.sh — pick frameworks based on the decision being made
# Usage: ./framework-router.sh <idea|validate|size|position|pivot>
# Output: space-separated list of framework names to load
set -euo pipefail

mode="${1:?mode required: idea|validate|size|position|pivot}"

case "$mode" in
  idea)     echo "7ps paul-graham niche-evaluation" ;;
  validate) echo "validation-criteria jtbd problem-interviews" ;;
  size)     echo "tam-sam-som competitor-analysis" ;;
  position) echo "value-prop-canvas competitor-analysis jtbd" ;;
  pivot)    echo "niche-evaluation tam-sam-som value-prop-canvas" ;;
  *)        echo "unknown mode: $mode" >&2; exit 1 ;;
esac
