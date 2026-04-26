#!/usr/bin/env bash
# domain-purity-check.sh — fail if domain/ imports infrastructure libs.
# Usage: domain-purity-check.sh <repo-root>
set -euo pipefail

ROOT="${1:-.}"
FORBIDDEN='sqlalchemy|django\.db|pymongo|redis|requests|httpx|aiohttp|kafka|boto3|fastapi|flask|pydantic\.BaseModel'

mapfile -t files < <(find "$ROOT" -type d -name domain -prune -exec grep -rlE "^(import|from) ($FORBIDDEN)" {} + || true)

if [ "${#files[@]}" -gt 0 ]; then
  echo "DDD violation: infrastructure imports inside domain layer:"
  printf '  %s\n' "${files[@]}"
  exit 1
fi

echo "domain/ is pure (no forbidden imports)."
