#!/usr/bin/env bash
# research-run.sh — drive faion-researcher modes sequentially.
# Usage: research-run.sh "<product description>" "ideas market competitors pricing"
# Each mode runs only after the previous one completes and its output file exists.
set -euo pipefail

PRODUCT="$1"; shift
MODES="${*:-ideas market competitors personas validate pricing}"
OUT_DIR=".aidocs/product_docs"
mkdir -p "$OUT_DIR"

declare -A MODE_FILE=(
  [ideas]="idea-validation.md"
  [market]="market-research.md"
  [competitors]="competitive-analysis.md"
  [pains]="pain-points.md"
  [personas]="user-personas.md"
  [validate]="problem-validation.md"
  [niche]="niche-evaluation.md"
  [pricing]="pricing-research.md"
  [names]="name-candidates.md"
)

for mode in $MODES; do
  out="$OUT_DIR/${MODE_FILE[$mode]}"
  # Build context-file list from any prior outputs
  prior_context=""
  for prior in "$OUT_DIR"/*.md; do
    [ -f "$prior" ] && prior_context+=" Prior context file: $prior."
  done
  echo "[$(date -Is)] mode=$mode → $out"
  claude -p "You are faion-research-agent. Mode: $mode. Product: '$PRODUCT'. \
Geography: EU/UA unless product context says otherwise. \
$prior_context \
Read any listed prior context files before starting. \
Write result to $out. \
Start the file with: <!-- generated: faion-research-agent mode=$mode on $(date -I) --> \
Cite every factual claim with [Source](URL). Write 'Data not available' for any \
unfound figure — do not estimate. Output only the absolute path on success." \
    --output-format text > "$out.log" 2>&1
  # Verify output file was created and is non-empty
  if [ ! -s "$out" ]; then
    echo "FAIL mode=$mode — output file empty or missing"
    cat "$out.log"
    exit 1
  fi
  echo "OK $out ($(wc -l < "$out") lines)"
done

echo "Research package complete → $OUT_DIR"
