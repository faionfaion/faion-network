#!/usr/bin/env bash
# debt-survey.sh — quarterly technical debt survey
# Usage: bash debt-survey.sh /path/to/repo
# Output: ~/debt/YYYY-MM-DD/{churn.txt,scc.json,cc.json,todos.txt,npm-outdated.json,pip-outdated.json,register.md}
# Requires: git, scc or tokei, radon (Python), grep, claude CLI (optional)
# Install tools: brew install scc; pip install radon

set -euo pipefail

REPO=${1:?Usage: debt-survey.sh <repo-path>}
DATE=$(date +%F)
OUT=~/debt/"$DATE"
mkdir -p "$OUT"

cd "$REPO"
echo "Surveying: $REPO → $OUT"

# 1. Hot-spots: file churn in last 90 days
echo "--- File churn (90d) ---"
git log --since='90 days ago' --name-only --pretty=format: \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -50 \
  > "$OUT/churn.txt"
echo "$(wc -l < "$OUT/churn.txt") files with churn"

# 2. Code complexity (scc preferred, radon for Python)
if command -v scc &>/dev/null; then
  scc --by-file --format json . > "$OUT/scc.json" 2>/dev/null || echo "scc partial"
fi
if command -v radon &>/dev/null; then
  radon cc -j -s . > "$OUT/cc.json" 2>/dev/null || true
fi

# 3. TODO/FIXME/HACK/XXX with line context
echo "--- TODO/FIXME scan ---"
grep -rn -E 'TODO|FIXME|HACK|XXX' \
  --include='*.py' --include='*.ts' --include='*.js' \
  --include='*.go' --include='*.rb' . \
  > "$OUT/todos.txt" 2>/dev/null || true
echo "$(wc -l < "$OUT/todos.txt") TODO/FIXME found"

# 4. Outdated dependencies
if [ -f package.json ]; then
  npm outdated --json 2>/dev/null > "$OUT/npm-outdated.json" || true
fi
if [ -f requirements.txt ] || [ -f pyproject.toml ]; then
  pip list --outdated --format=json 2>/dev/null > "$OUT/pip-outdated.json" || true
fi

# 5. Copy coverage if present
[ -f coverage.xml ] && cp coverage.xml "$OUT/" || true

# 6. Classify via Claude (optional — requires claude CLI and prompt file)
if command -v claude &>/dev/null && [ -f ~/prompts/debt-classify.txt ]; then
  echo "--- Running debt classifier ---"
  claude -p "$(cat ~/prompts/debt-classify.txt)" \
    --input-files "$OUT"/*.json "$OUT"/*.txt \
    > "$OUT/register.md"
  echo "Register → $OUT/register.md"
else
  echo "Skipping classifier (no claude CLI or ~/prompts/debt-classify.txt)"
  echo "Raw signals available in: $OUT/"
fi

echo "Survey complete: $OUT"
