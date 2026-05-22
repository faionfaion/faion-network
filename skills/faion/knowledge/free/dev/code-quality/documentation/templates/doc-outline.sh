# purpose: template for documentation (doc-outline.sh)
# consumes: documentation methodology inputs (see AGENTS.md Prerequisites)
# produces: filled-in artefact conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml + tool-runtime in same dir
# token-budget-impact: ~200-400 tokens when loaded as context

#!/usr/bin/env bash
# doc-outline.sh — emit a JSON outline for a directory the writer agent will fill.
# Usage: doc-outline.sh path/to/dir
# Output: JSON with dir, type, files (from git ls-files), languages (from tokei)
set -euo pipefail
DIR="$1"

jq -n \
  --arg dir "$DIR" \
  --argjson files "$(git ls-files "$DIR" | jq -Rsc 'split("\n")|map(select(length>0))')" \
  --argjson lang "$(tokei -o json "$DIR" 2>/dev/null | jq '.. | objects | select(.language) | {(.language): .code}' 2>/dev/null || echo '{}')" \
  --arg type "$(test -f "$DIR/package.json" && echo frontend \
                || test -f "$DIR/manage.py" && echo backend-django \
                || test -f "$DIR/pyproject.toml" && echo backend-python \
                || test -d "$DIR/terraform" && echo infra \
                || echo library)" \
  '{dir:$dir, type:$type, files:$files, languages:$lang}'
