#!/usr/bin/env bash
# check-names.sh — read names.txt, run availability checks, output matrix.csv
# Usage: bash check-names.sh names.txt
# Output: ~/names/YYYY-MM-DD.csv with columns: name,com,io,co,app,gh,npm,pypi,twitter
# Requires: whois, curl, npm (for npm check)
# Rate-limit: 1s sleep between names to avoid WHOIS throttling

set -euo pipefail

NAMES=${1:?Usage: check-names.sh <names.txt>}
OUT=~/names/$(date +%F).csv
mkdir -p ~/names
echo "name,com,io,co,app,gh,npm,pypi,twitter" > "$OUT"

avail_whois() {
  local domain=$1
  # Match multiple registry responses: "no match", "not found", "no entries found", "AVAILABLE"
  if whois "$domain" 2>/dev/null | grep -qiE "no match|not found|no entries|AVAILABLE"; then
    echo Y
  else
    echo N
  fi
}

while IFS= read -r name; do
  [ -z "$name" ] && continue
  name=$(echo "$name" | tr -d '[:space:]')

  com=$(avail_whois "$name.com")
  io=$(avail_whois "$name.io")
  co=$(avail_whois "$name.co")
  app=$(avail_whois "$name.app")

  # GitHub org: 404 = available
  gh=$(curl -s -o /dev/null -w "%{http_code}" "https://github.com/$name" \
       | grep -q 404 && echo Y || echo N)

  # npm: non-zero exit = not found = available
  npm_avail=$(npm view "$name" 2>/dev/null >/dev/null && echo N || echo Y)

  # PyPI: 404 = available
  pypi=$(curl -s -o /dev/null -w "%{http_code}" \
         "https://pypi.org/pypi/$name/json" | grep -q 404 && echo Y || echo N)

  # Twitter/X: 404 = available (note: Twitter blocks many agents; treat errors as unknown)
  tw=$(curl -s -o /dev/null -w "%{http_code}" "https://twitter.com/$name" \
       | grep -q 404 && echo Y || echo N)

  echo "$name,$com,$io,$co,$app,$gh,$npm_avail,$pypi,$tw" >> "$OUT"
  echo "Checked: $name  .com=$com .io=$io .co=$co GitHub=$gh npm=$npm_avail"
  sleep 1  # rate-limit politeness
done < "$NAMES"

echo ""
echo "Results saved to: $OUT"
column -t -s, "$OUT"
