#!/usr/bin/env bash
# purpose: Pre-commit guard: makemigrations --check --dry-run.
# consumes: project repo; see the methodology AGENTS.md for input contract.
# produces: the working artifact described above; placement: Add to pre-commit hook.
# depends-on: the tooling pinned in the methodology's AGENTS.md.
# token-budget-impact: zero — local-only template; build/CI time is the only cost.
# scripts/check-migrations.sh — refuse commit if models changed without a staged migration.
# Wire as pre-commit hook or in CI.
set -euo pipefail

changed=$(git diff --cached --name-only -- "apps/*/models/*.py" "apps/*/models.py" "core/models.py" 2>/dev/null || true)

[[ -z "$changed" ]] && exit 0

out=$(python manage.py makemigrations --dry-run --check 2>&1) || {
  echo "FAIL — models changed but migration not staged:"
  echo "$out"
  exit 1
}

echo "OK — migration is up to date"
