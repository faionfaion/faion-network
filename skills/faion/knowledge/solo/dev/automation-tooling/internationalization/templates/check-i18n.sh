#!/usr/bin/env bash
# check-i18n.sh — fail build on missing or extra keys vs EN catalogue
# Usage: ./scripts/check-i18n.sh
set -euo pipefail

SRC=locales/en

for L in uk de fr ja ar; do
  TARGET="locales/$L"
  if [ ! -f "$TARGET/common.json" ]; then
    echo "Missing: $TARGET/common.json"
    exit 1
  fi

  diff \
    <(jq -r 'paths(scalars) | join(".")' "$SRC/common.json" | sort) \
    <(jq -r 'paths(scalars) | join(".")' "$TARGET/common.json" | sort) \
    || { echo "Key drift in $L vs EN"; exit 1; }
done

echo "i18n keys aligned across all locales."
