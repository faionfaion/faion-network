#!/usr/bin/env bash
# validate-signal.sh — reject any JSONL signal row missing the required triple.
# Usage: cat signals.jsonl | bash validate-signal.sh
# Exit 1 if any row is invalid, 0 if all rows pass.
set -euo pipefail

FAILED=0
while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    src=$(echo "$line" | jq -r '.source_url // empty')
    fat=$(echo "$line" | jq -r '.fetched_at // empty')
    rh=$(echo "$line" | jq -r '.raw_hash // empty')
    if [[ -z "$src" || -z "$fat" || -z "$rh" ]]; then
        echo "FAIL: missing source_url/fetched_at/raw_hash in: $line" >&2
        FAILED=1
    fi
done

exit $FAILED
