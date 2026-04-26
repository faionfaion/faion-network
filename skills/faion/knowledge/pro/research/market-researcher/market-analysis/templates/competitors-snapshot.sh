#!/usr/bin/env bash
# competitors-snapshot.sh
# Freeze a set of competitor URLs into a dated snapshot folder.
# Each page is saved as a markdown file via firecrawl (localhost:3002).
# Usage: ./competitors-snapshot.sh [snapshot-dir]
# Output: snapshots/YYYY-MM-DD/<index>-<slug>.md

set -euo pipefail

SNAPSHOT_DIR="${1:-snapshots/$(date +%Y-%m-%d)}"
FIRECRAWL_URL="${FIRECRAWL_URL:-http://localhost:3002}"

# Add competitor URLs here (one per line, no trailing comma on last entry)
COMPETITORS=(
  "https://example-competitor-1.com/pricing"
  "https://example-competitor-2.com/pricing"
  "https://example-competitor-3.com/features"
)

mkdir -p "$SNAPSHOT_DIR"

fetch_page() {
  local index="$1"
  local url="$2"
  local slug
  slug=$(printf '%s' "$url" | sed 's|https\?://||; s|/|-|g; s|[^a-zA-Z0-9_-]||g' | cut -c1-60)
  local out="$SNAPSHOT_DIR/$(printf '%02d' "$index")-${slug}.md"

  echo "  Fetching: $url"
  local response
  if response=$(curl -sf -X POST "$FIRECRAWL_URL/v1/scrape" \
      -H "Content-Type: application/json" \
      -d "{\"url\": \"$url\", \"formats\": [\"markdown\"], \"onlyMainContent\": true}" \
      --max-time 30); then
    # Extract markdown from JSON response
    local content
    content=$(printf '%s' "$response" | python3 -c "
import json, sys
data = json.load(sys.stdin)
md = data.get('data', {}).get('markdown', '') or data.get('markdown', '')
print(md)
" 2>/dev/null || printf '%s' "$response")
    if [ -n "$content" ]; then
      {
        printf '<!-- snapshot: %s -->\n' "$url"
        printf '<!-- date: %s -->\n\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
        printf '%s\n' "$content"
      } > "$out"
      echo "    Saved: $out"
    else
      echo "    WARN: empty content for $url"
      printf '<!-- snapshot: %s -->\n<!-- date: %s -->\n<!-- ERROR: empty response -->\n' \
        "$url" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$out"
    fi
  else
    echo "    ERROR: fetch failed for $url"
    printf '<!-- snapshot: %s -->\n<!-- date: %s -->\n<!-- ERROR: fetch failed -->\n' \
      "$url" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$out"
  fi
}

echo "Snapshots → $SNAPSHOT_DIR"
echo "Firecrawl → $FIRECRAWL_URL"
echo ""

index=1
for url in "${COMPETITORS[@]}"; do
  fetch_page "$index" "$url"
  index=$((index + 1))
  # Rate-limit: 1 request/second to avoid overloading target sites
  sleep 1
done

# Write index file
INDEX_FILE="$SNAPSHOT_DIR/INDEX.md"
{
  printf '# Competitor Snapshots — %s\n\n' "$(date +%Y-%m-%d)"
  printf '| # | File | URL |\n'
  printf '|---|------|-----|\n'
  idx=1
  for url in "${COMPETITORS[@]}"; do
    slug=$(printf '%s' "$url" | sed 's|https\?://||; s|/|-|g; s|[^a-zA-Z0-9_-]||g' | cut -c1-60)
    printf '| %d | [%02d-%s.md](%02d-%s.md) | %s |\n' \
      "$idx" "$idx" "$slug" "$idx" "$slug" "$url"
    idx=$((idx + 1))
  done
} > "$INDEX_FILE"

echo ""
echo "Done. Index: $INDEX_FILE"
echo "Files: $(ls "$SNAPSHOT_DIR"/*.md 2>/dev/null | wc -l) snapshots"
