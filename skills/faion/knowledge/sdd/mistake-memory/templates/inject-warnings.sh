#!/usr/bin/env bash
# inject-warnings.sh — Output relevant mistake entries from mistakes.md
# Usage: ./inject-warnings.sh "keyword1 keyword2"
# Output is appended as a Warnings section to the agent's task context.

set -euo pipefail

KEYWORDS="${1:-}"
MISTAKES_FILE=".aidocs/memory/mistakes.md"

if [[ ! -f "$MISTAKES_FILE" ]]; then
    echo "# Warnings"
    echo "No mistakes.md found at $MISTAKES_FILE"
    exit 0
fi

if [[ -z "$KEYWORDS" ]]; then
    echo "Usage: $0 \"keyword1 keyword2\"" >&2
    exit 1
fi

# Build grep pattern from space-separated keywords
PATTERN=$(echo "$KEYWORDS" | tr ' ' '|')

# Extract MIS-NNN blocks that contain any keyword
MATCHES=$(awk '
    /^## MIS-/ { if (block && block ~ /'"$PATTERN"'/) print block; block = $0; next }
    block { block = block "\n" $0 }
    END { if (block && block ~ /'"$PATTERN"'/) print block }
' "$MISTAKES_FILE")

if [[ -z "$MATCHES" ]]; then
    exit 0
fi

echo "## Warnings (from mistakes.md)"
echo ""
echo "$MATCHES"
echo ""
