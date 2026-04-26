#!/usr/bin/env bash
# migrate_dry_run.sh — extract, transform, count-diff, field-drift audit.
# Gate before each pilot or full-migration wave.
# Usage: migrate_dry_run.sh [migration.yaml]
set -euo pipefail

CFG="${1:-migration.yaml}"
OUT="dryrun-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"

echo "==> Extract from source"
python -m migration extract --config "$CFG" --out "$OUT/extract.jsonl"

echo "==> Transform to target format"
python -m migration transform --config "$CFG" \
  --in "$OUT/extract.jsonl" --out "$OUT/transform.jsonl"

src_n=$(wc -l < "$OUT/extract.jsonl")
tgt_n=$(wc -l < "$OUT/transform.jsonl")
echo "extract=$src_n transform=$tgt_n"

if [ "$src_n" != "$tgt_n" ]; then
  echo "FAIL: COUNT DRIFT — source=$src_n transform=$tgt_n" >&2
  exit 1
fi

echo "==> Audit field drift"
python -m migration audit-fields --config "$CFG" --in "$OUT/extract.jsonl" \
  > "$OUT/field-drift.json"

unmapped=$(jq '.unmapped_count' "$OUT/field-drift.json")
low_conf=$(jq '.low_confidence_count' "$OUT/field-drift.json")

if [ "$unmapped" != "0" ]; then
  echo "FAIL: $unmapped unmapped fields — review $OUT/field-drift.json" >&2
  exit 1
fi

if [ "$low_conf" != "0" ]; then
  echo "WARNING: $low_conf low-confidence mappings — human review required before load"
  jq '.low_confidence' "$OUT/field-drift.json"
fi

echo "==> Dry-run OK → $OUT"
echo "Next: review $OUT/field-drift.json, get human sign-off, then run full wave."
