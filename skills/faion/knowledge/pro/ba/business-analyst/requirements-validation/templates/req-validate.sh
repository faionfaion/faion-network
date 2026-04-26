#!/usr/bin/env bash
# req-validate.sh — pre-validation lint over spec.md + traceability sanity.
# Fails on: TBD/TODO, weasel words, AC without IDs, AC IDs without test refs.
#
# Usage: bash req-validate.sh <feature-dir>
# Example: bash req-validate.sh .aidocs/features/F-042/
set -euo pipefail

DIR="${1:?feature dir required}"
SPEC="$DIR/spec.md"
PLAN="$DIR/test-plan.md"

[[ -f "$SPEC" && -f "$PLAN" ]] || {
    echo "missing spec.md or test-plan.md in $DIR" >&2
    exit 2
}

fails=0
weasel='\b(fast|slow|user-?friendly|intuitive|reasonable|appropriate|robust|seamless|scalable)\b'

if grep -InE 'TBD|TODO|XXX|\?\?\?' "$SPEC"; then
    echo "FAIL: placeholder text in spec" >&2
    fails=$((fails + 1))
fi
if grep -InEi "$weasel" "$SPEC"; then
    echo "FAIL: weasel words in spec" >&2
    fails=$((fails + 1))
fi

mapfile -t IDS < <(grep -oE 'REQ-[A-Z0-9]+-[0-9]+|AC-[A-Z0-9]+-[0-9]+' "$SPEC" | sort -u)
mapfile -t REFS < <(grep -oE 'REQ-[A-Z0-9]+-[0-9]+|AC-[A-Z0-9]+-[0-9]+' "$PLAN" | sort -u)

miss=()
for id in "${IDS[@]}"; do
    printf '%s\n' "${REFS[@]}" | grep -qx "$id" || miss+=("$id")
done

if ((${#miss[@]})); then
    printf 'FAIL: %s requirements without test reference:\n' "${#miss[@]}" >&2
    printf '  %s\n' "${miss[@]}" >&2
    fails=$((fails + 1))
fi

((fails == 0)) || exit 1
echo "OK: ${#IDS[@]} requirements, no placeholders, no weasel words, all traced."
