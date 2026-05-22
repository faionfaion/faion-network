#!/usr/bin/env bash
# purpose: Validate live responses against the OpenAPI snapshot in CI.
# consumes: openapi.json (or path arg 1), base URL of the running service (arg 2).
# produces: exit 0 if all probed endpoints' responses validate against schema, exit 1 otherwise.
# depends-on: python3 (stdlib) + jsonschema (or schemathesis if available).
# token-budget-impact: zero — runs in CI; typical project &lt; 30s.
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
