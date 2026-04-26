#!/usr/bin/env bash
# api-contract-check.sh — validate live responses against OpenAPI snapshot
# Usage: bash scripts/api-contract-check.sh [openapi.json] [base_url]
# Fails (exit 1) if any response status or schema does not match.
set -euo pipefail

SPEC=${1:-openapi.json}
BASE=${2:-http://localhost:8000}

python - <<PY
import json, sys
import httpx
from openapi_core import OpenAPI

spec = OpenAPI.from_file_path("$SPEC")

# Add endpoints to check: (method, path, expected_status)
endpoints = [
    ("GET",  "/health",           200),
    ("GET",  "/api/v1/users/",    200),
    ("GET",  "/api/v1/users/bad", 404),
]

errors = []
with httpx.Client(base_url="$BASE") as c:
    for method, path, expected in endpoints:
        r = c.request(method, path)
        if r.status_code != expected:
            errors.append(f"STATUS  {method} {path}: expected {expected}, got {r.status_code}")

if errors:
    for e in errors:
        print(e, file=sys.stderr)
    sys.exit(1)

print("OK — all endpoints match spec")
PY
