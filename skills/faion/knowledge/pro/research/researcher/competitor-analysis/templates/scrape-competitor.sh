#!/usr/bin/env bash
# scrape-competitor.sh — fetch homepage, pricing, G2, and Wayback for one competitor.
# Usage: ./scrape-competitor.sh <name> <homepage_url> [pricing_url]
# Output: ./_competitors/<slug>/ with homepage.txt, pricing.txt, g2.txt, wayback.txt, _meta.json
# Feed the output directory to the snapshot agent prompt.
set -euo pipefail

NAME="$1"
HOME_URL="$2"
PRICE_URL="${3:-$HOME_URL/pricing}"
SLUG="$(echo "$NAME" | tr '[:upper:] ' '[:lower:]-')"
OUT_DIR="./_competitors/$SLUG"
mkdir -p "$OUT_DIR"

fetch() {
  local url="$1" file="$2"
  echo "  fetching $url → $file"
  curl -fsSL --max-time 15 -A "Mozilla/5.0 (compatible; faion-research)" "$url" \
    | lynx -stdin -dump -nolist -width=120 2>/dev/null \
    > "$OUT_DIR/$file" \
    || echo "FETCH_FAILED $url" > "$OUT_DIR/$file"
}

fetch "$HOME_URL"  "homepage.txt"
fetch "$PRICE_URL" "pricing.txt"
fetch "https://www.g2.com/search?query=${NAME// /+}" "g2.txt"
fetch "https://web.archive.org/web/2024*/$HOME_URL"  "wayback.txt"

cat > "$OUT_DIR/_meta.json" <<EOF
{
  "name": "$NAME",
  "slug": "$SLUG",
  "homepage": "$HOME_URL",
  "pricing": "$PRICE_URL",
  "fetched_at": "$(date -Iseconds)"
}
EOF

echo "→ $OUT_DIR ready for snapshot agent"
echo "  Files: $(ls "$OUT_DIR" | tr '\n' ' ')"
