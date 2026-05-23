#!/usr/bin/env bash
# design-quality-gate.sh — Verify FR coverage and file table traces between spec and design.
# Usage: ./design-quality-gate.sh spec.md design.md
# Output: OK/FAIL for each FR, and FR/AD trace status for each file table row.
set -euo pipefail

SPEC="${1:?Usage: $0 spec.md design.md}"
DESIGN="${2:?Usage: $0 spec.md design.md}"

echo "=== Design Quality Gate ==="
echo "Spec:   $SPEC"
echo "Design: $DESIGN"
echo ""

# Check all spec FRs appear in design
echo "--- FR Coverage ---"
SPEC_FRS=$(grep -oP 'FR-\d+' "$SPEC" | sort -u)
DESIGN_FRS=$(grep -oP 'FR-\d+' "$DESIGN" | sort -u)
FAIL=0
for FR in $SPEC_FRS; do
  if echo "$DESIGN_FRS" | grep -q "$FR"; then
    echo "  OK    $FR — referenced in design"
  else
    echo "  FAIL  $FR — NOT referenced in design"
    FAIL=1
  fi
done

echo ""
echo "--- File Table Trace Check ---"
grep -P '\|\s*(CREATE|MODIFY)' "$DESIGN" | while IFS= read -r line; do
  file=$(echo "$line" | grep -oP '`[^`]+`' | head -1 | tr -d '`')
  has_fr=$(echo "$line" | grep -qP 'FR-\d+' && echo "yes" || echo "NO ")
  has_ad=$(echo "$line" | grep -qP 'AD-\d+' && echo "yes" || echo "NO ")
  echo "  $file: FR=$has_fr AD=$has_ad"
done

echo ""
if [ "$FAIL" -eq 1 ]; then
  echo "RESULT: FAIL — some FRs not covered in design"
  exit 1
else
  echo "RESULT: OK — all spec FRs referenced in design"
fi
