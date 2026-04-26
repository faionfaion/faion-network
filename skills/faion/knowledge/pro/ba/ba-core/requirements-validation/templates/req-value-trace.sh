#!/usr/bin/env bash
# req-value-trace.sh — fail if any requirement in spec.md lacks a YAML value-trace block.
# Usage: ./req-value-trace.sh spec.md
# Expected spec.md structure per requirement:
#   ---
#   req_id: REQ-PROJ-001
#   value_class: enabling|direct|indirect|none
#   goals_supported:
#     - goal-1
#   ---
set -euo pipefail

SPEC="${1:?spec.md required}"
[[ -f "$SPEC" ]] || { echo "missing $SPEC" >&2; exit 2; }

mapfile -t REQS < <(grep -oE 'REQ-[A-Z0-9]+-[0-9]+' "$SPEC" | sort -u)
fails=0

for r in "${REQS[@]}"; do
    block=$(awk -v r="$r" '
        $0 ~ "^---$" { in_yaml = !in_yaml; next }
        in_yaml && $0 ~ "req_id:.*"r { found=1 }
        found && $0 ~ "^---$" { exit }
        found { print }
    ' "$SPEC")

    if [[ -z "$block" ]]; then
        echo "FAIL: $r — no YAML value-trace block found" >&2
        fails=$((fails+1))
        continue
    fi

    vc=$(printf '%s\n' "$block" | grep -oE 'value_class:[[:space:]]*[a-z]+' | awk '{print $NF}' || true)
    goals=$(printf '%s\n' "$block" | grep -c 'goals_supported:' || true)

    case "$vc" in
        enabling|direct|indirect)
            : ;;
        none)
            echo "FAIL: $r value_class=none — remove or re-elicit" >&2
            fails=$((fails+1))
            ;;
        *)
            echo "FAIL: $r missing or invalid value_class (got: '$vc')" >&2
            fails=$((fails+1))
            ;;
    esac

    (( goals > 0 )) || {
        echo "FAIL: $r no goals_supported entries" >&2
        fails=$((fails+1))
    }
done

if (( fails == 0 )); then
    echo "OK: ${#REQS[@]} requirements, all value-traced."
else
    exit 1
fi
