# purpose: template for code-quality-trends (detect-stack.sh)
# consumes: code-quality-trends methodology inputs (see AGENTS.md Prerequisites)
# produces: filled-in artefact conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml + tool-runtime in same dir
# token-budget-impact: ~200-400 tokens when loaded as context

#!/usr/bin/env bash
# detect-stack.sh — coarse stack classifier for the audit agent.
# Reads manifest files and emits lang/framework/version tags.
# Usage: detect-stack.sh [directory]
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

[ -f tsconfig.json ] && echo "lang:ts" || { [ -f package.json ] && echo "lang:js"; }
{ [ -f pyproject.toml ] || [ -f requirements.txt ] || [ -f setup.py ]; } && echo "lang:py"
[ -f go.mod ] && echo "lang:go"
[ -f Cargo.toml ] && echo "lang:rust"

[ -f next.config.js ] || [ -f next.config.mjs ] && echo "fw:next"
[ -f remix.config.js ] && echo "fw:remix"
[ -f svelte.config.js ] && echo "fw:svelte"
[ -f manage.py ] && echo "fw:django"
[ -f main.go ] && grep -q "gin" go.mod 2>/dev/null && echo "fw:gin"

[ -f package.json ] && grep -q '"react"' package.json 2>/dev/null && echo "lib:react"
[ -f package.json ] && grep -q '"vue"' package.json 2>/dev/null && echo "lib:vue"

[ -f pyproject.toml ] && grep -m1 'requires-python' pyproject.toml | sed 's/.*= */python:/'
[ -f package.json ] && jq -r '.engines.node // empty' package.json 2>/dev/null | sed 's/^/node:/'
