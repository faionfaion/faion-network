#!/usr/bin/env bash
# uc-to-plantuml.sh — emit @startuml UC diagram from use-case-index.json
# Usage: ./uc-to-plantuml.sh path/to/use-case-index.json "System Name"
# Output: PlantUML source on stdout; render with: plantuml diagram.puml
set -euo pipefail
JSON="${1:?usage: $0 <use-case-index.json> <system-name>}"
SYS="${2:-System}"

declare -A ACTORS
echo "@startuml"
echo "left to right direction"
echo "skinparam packageStyle rectangle"

# Collect distinct actors
while read -r a; do ACTORS["$a"]=1; done < <(jq -r '.[].actor' "$JSON" | sort -u)
for a in "${!ACTORS[@]}"; do
  printf 'actor "%s" as A_%s\n' "$a" "$(echo "$a" | tr -c '[:alnum:]' '_')"
done

echo "rectangle \"$SYS\" {"
jq -r '.[] | "  usecase \"\(.name)\\n[\(.id)]\" as \(.id|gsub("-";"_"))"' "$JSON"
echo "}"

# Edges: actor -> uc
jq -r '.[] | "\(.actor)\t\(.id)"' "$JSON" | \
while IFS=$'\t' read -r actor uc; do
  printf 'A_%s --> %s\n' \
    "$(echo "$actor" | tr -c '[:alnum:]' '_')" \
    "$(echo "$uc" | tr '-' '_')"
done

echo "@enduml"
