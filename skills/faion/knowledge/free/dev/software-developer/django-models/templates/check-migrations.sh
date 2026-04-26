#!/usr/bin/env bash
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
