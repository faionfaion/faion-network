#!/usr/bin/env bash
# ac-coverage.sh — verify every AC ID in spec.md has a matching test in test-plan.md
# Usage: ac-coverage.sh <feature-dir>
# Exit: 0 = all covered, 1 = gaps found, 2 = missing spec or plan
set -euo pipefail
DIR="${1:?feature dir required}"
SPEC="$DIR/spec.md"
PLAN="$DIR/test-plan.md"
[[ -f "$SPEC" && -f "$PLAN" ]] || { echo "missing spec.md or test-plan.md" >&2; exit 2; }

# Extract AC IDs (format: AC-<SLUG>-NN)
mapfile -t AC_IDS < <(grep -oE 'AC-[A-Z0-9]+-[0-9]+' "$SPEC" | sort -u)
mapfile -t TEST_REFS < <(grep -oE 'AC-[A-Z0-9]+-[0-9]+' "$PLAN" | sort -u)

missing=()
for id in "${AC_IDS[@]}"; do
  if ! printf '%s\n' "${TEST_REFS[@]}" | grep -qx "$id"; then
    missing+=("$id")
  fi
done

if (( ${#missing[@]} )); then
  echo "FAIL: ${#missing[@]} AC without test coverage:" >&2
  printf '  %s\n' "${missing[@]}" >&2
  exit 1
fi
echo "OK: ${#AC_IDS[@]} AC, all covered."
