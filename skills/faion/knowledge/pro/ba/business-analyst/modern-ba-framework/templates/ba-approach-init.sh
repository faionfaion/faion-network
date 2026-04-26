#!/usr/bin/env bash
# ba-approach-init.sh — scaffold a Modern BA Framework approach for a feature.
# Creates .aidocs/<feature>/ba-approach.json with all KAs set to include: null.
# Fill perspectives + KA decisions, then commit.
# Usage: ba-approach-init.sh <feature-slug>
set -euo pipefail
FEATURE="${1:?usage: ba-approach-init.sh <feature-slug>}"
DIR=".aidocs/${FEATURE}"
mkdir -p "$DIR"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat > "$DIR/ba-approach.json" <<JSON
{
  "feature": "${FEATURE}",
  "created_at": "${TS}",
  "human_signoff_required": true,
  "human_signoff_at": null,
  "perspectives": [],
  "knowledge_areas": {
    "ba_planning_monitoring":       {"include": null, "rationale": "", "methodologies": []},
    "elicitation_collaboration":    {"include": null, "rationale": "", "methodologies": []},
    "requirements_lifecycle":       {"include": null, "rationale": "", "methodologies": []},
    "strategy_analysis":            {"include": null, "rationale": "", "methodologies": []},
    "requirements_analysis_design": {"include": null, "rationale": "", "methodologies": []},
    "solution_evaluation":          {"include": null, "rationale": "", "methodologies": []}
  },
  "competencies_needed": [],
  "model_routing": {
    "format_requirements":         "haiku",
    "write_acceptance_criteria":   "sonnet",
    "validate_with_stakeholders":  "sonnet",
    "gap_analysis":                "opus",
    "bpmn_modeling":               "opus"
  }
}
JSON
echo "Initialized ${DIR}/ba-approach.json"
echo "Next: fill perspectives[] and knowledge_areas[].include, then get human sign-off before execution."
