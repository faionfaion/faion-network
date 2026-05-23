#!/usr/bin/env bash
# purpose: Dump the repo's commands (npm/yarn/just/make) into a CLAUDE.md-ready format.
# consumes: Repo root path.
# produces: Markdown command table on stdout, ready to paste into CLAUDE.md.
# depends-on: Standard POSIX shell utilities + jq when package.json is present.
# token-budget-impact: zero — local shell run.
# extract-commands.sh — Dump project commands into CLAUDE.md-ready format.
# Usage: bash extract-commands.sh
# Output: Commands section for CLAUDE.md based on package.json, Makefile, pyproject.toml

echo "## Commands"
echo ""

if [ -f package.json ]; then
  echo "### npm / Node"
  echo '```bash'
  jq -r '.scripts | to_entries[] | "\(.key)  # \(.value)"' package.json 2>/dev/null \
    | head -20
  echo '```'
fi

if [ -f Makefile ]; then
  echo ""
  echo "### Make"
  echo '```bash'
  grep -E "^[a-zA-Z_-]+:" Makefile \
    | sed 's/:.*//' \
    | head -20 \
    | while read -r t; do echo "make $t"; done
  echo '```'
fi

if [ -f pyproject.toml ]; then
  echo ""
  echo "### Python (ruff)"
  echo '```bash'
  echo "ruff check . --fix  # Lint + auto-fix"
  echo "ruff format .        # Format"
  echo "pytest --cov=src     # Tests with coverage"
  echo '```'
fi