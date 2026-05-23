#!/usr/bin/env bash
# purpose: Shell helper that scaffolds an empty ADR markdown for the 5 focus areas.
# consumes: see content/02-output-contract.xml inputs for pm-framework-focus-areas
# produces: decision-record
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~200-1000 tokens when loaded as context


# scaffold_focus_areas.sh — Create a docs/ tree with one folder and default
# artifacts per PMBOK 8 focus area.
#
# Usage: ./scaffold_focus_areas.sh [root-dir]
# Default root-dir: docs
#
# Output: folder tree under <root-dir>/ with placeholder files.
set -euo pipefail

ROOT="${1:-docs}"
mkdir -p "$ROOT"

for fa in initiating planning executing monitoring-controlling closing; do
    d="$ROOT/$fa"
    mkdir -p "$d"
    case "$fa" in
        initiating)
            files=(charter.md vision.md stakeholder-register.md)
            ;;
        planning)
            files=(spec.md design.md risk-register.md plan.md)
            ;;
        executing)
            files=(decisions.md status-reports/.gitkeep)
            ;;
        monitoring-controlling)
            files=(metrics.md change-log.md burn-up.md)
            ;;
        closing)
            files=(lessons-learned.md acceptance.md final-report.md)
            ;;
    esac
    for f in "${files[@]}"; do
        mkdir -p "$(dirname "$d/$f")"
        touch "$d/$f"
    done
done

echo "Scaffolded focus areas under $ROOT/"
