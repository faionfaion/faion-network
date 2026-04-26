#!/usr/bin/env bash
# verify-seo.sh — Assert SEO essentials on each route via Googlebot curl
# Usage: ./verify-seo.sh http://localhost:3000 routes.txt
# routes.txt: one path per line (e.g. /products/widget-a)
# Exit 1 if any route is missing any required element.

set -euo pipefail

BASE="${1:-http://localhost:3000}"
ROUTES_FILE="${2:-routes.txt}"
FAIL=0

REQUIRED=(
  '<title>'
  'name="description"'
  'rel="canonical"'
  'property="og:image"'
  'property="og:title"'
  'property="og:url"'
  'twitter:card'
)

while IFS= read -r path; do
  [[ -z "$path" || "$path" == \#* ]] && continue
  html=$(curl -fsSL -A "Googlebot/2.1" "$BASE$path" 2>/dev/null) || {
    echo "FETCH_FAIL $path"
    FAIL=1
    continue
  }
  for sel in "${REQUIRED[@]}"; do
    grep -q "$sel" <<<"$html" || {
      echo "MISS [$sel] @ $path"
      FAIL=1
    }
  done
done < "$ROUTES_FILE"

if [[ $FAIL -eq 0 ]]; then
  echo "OK all routes passed SEO check"
fi
exit $FAIL
