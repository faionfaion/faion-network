#!/usr/bin/env bash
# ba-framework-select.sh — scaffold a primary-framework decision for a feature.
# Usage: ba-framework-select.sh <feature-slug>
# Fills a starter ba-framework-decision.json; feed scores to a planner LLM call.
set -euo pipefail
FEATURE="${1:?usage: ba-framework-select.sh <feature-slug>}"
DIR=".aidocs/${FEATURE}"
mkdir -p "$DIR"
cat > "$DIR/ba-framework-decision.json" <<'JSON'
{
  "context": {
    "industry": "",
    "regulation_set": [],
    "team_size": 0,
    "delivery_model": "",
    "contract_clauses": [],
    "existing_standards": [],
    "audit_required": false
  },
  "candidates_scored": {
    "BABOK_v3":              {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "BA_Standard_2025":      {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "IREB_CPRE":             {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "PMI_PBA":               {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "BCS_Diploma":           {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "SAFe_BA":               {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "Agile_Extension_BABOK": {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "SWEBOK_v4_Reqs":        {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0}
  },
  "primary": "",
  "extensions": [],
  "rationale": "",
  "glossary": {},
  "deviations": [],
  "human_signoff_required": true
}
JSON
echo "Initialized $DIR/ba-framework-decision.json — fill scores, pick primary, get human sign-off."
