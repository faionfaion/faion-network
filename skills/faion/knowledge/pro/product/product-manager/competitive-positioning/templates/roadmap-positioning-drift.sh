#!/usr/bin/env bash
# roadmap-positioning-drift.sh — flag backlog items that dilute positioning.
# Inputs:
#   $1 — positioning-canvas.md (with YAML frontmatter unique_attributes:)
#   $2 — backlog.csv with columns: id,title,description,positioning_fit
# Output: drift table; non-zero exit if dilution detected.
# Wire into CI or run as a pre-planning gate.
set -euo pipefail
CANVAS="${1:?canvas.md required}"; BACKLOG="${2:?backlog.csv required}"

# Pull unique attributes from YAML frontmatter (between --- markers)
ATTRS=$(awk '/^---/{p++; next} p==1 && /^unique_attributes:/{flag=1; next}
             p==1 && flag && /^  - /{print substr($0, index($0,$2)); next}
             p==1 && flag && /^[a-z]/{flag=0}
             p>=2{exit}' "$CANVAS" | sed '/^$/d')

[ -z "$ATTRS" ] && { echo "FAIL: no unique_attributes in canvas YAML frontmatter" >&2; exit 1; }

echo "id,title,positioning_fit,reinforces,dilutes"
DILUTED=0
while IFS=',' read -r id title desc fit; do
  [ "$id" = "id" ] && continue
  reinforces=""
  while IFS= read -r attr; do
    [ -z "$attr" ] && continue
    grep -qiE "$attr" <<<"$title $desc" && reinforces="${reinforces};${attr}"
  done <<<"$ATTRS"
  dilutes=""
  # Heuristic: score 0 or enterprise keywords in a "simple/solo" positioned product
  if [ "$fit" = "0" ]; then
    dilutes="positioning_fit=0"
    DILUTED=$((DILUTED + 1))
  elif grep -qiE '\b(enterprise|sso|saml|audit-log|compliance)\b' <<<"$title $desc" \
       && grep -qiE '\b(simple|solo|individual|personal|lightweight)\b' <<<"$ATTRS"; then
    dilutes="enterprise-vs-simple-positioning"
    DILUTED=$((DILUTED + 1))
  fi
  echo "${id},\"${title}\",${fit},${reinforces#;},${dilutes}"
done < "$BACKLOG"

if [ $DILUTED -gt 0 ]; then
  echo "FAIL: $DILUTED items dilute positioning — review before sprint planning" >&2
  exit 2
fi
echo "OK: no dilution detected." >&2
