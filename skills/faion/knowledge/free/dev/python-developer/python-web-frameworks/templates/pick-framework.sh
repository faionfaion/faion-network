#!/usr/bin/env bash
# purpose: Keyword-score a Python web project brief and emit a framework decision-record JSON.
# consumes: stdin (Markdown / plain-text brief of the project).
# produces: decision-record JSON conforming to content/02-output-contract.xml.
# depends-on: bash, python3 (stdlib only).
# token-budget-impact: zero; pure local keyword count, &lt; 100ms.
set -euo pipefail

python - <<'PY'
import json, sys

brief = sys.stdin.read().lower()
score = {"django": 0, "fastapi": 0, "flask": 0}

# Django signals
for kw in ["admin panel", "cms", "full-stack", "html template", "migrations", "enterprise"]:
    if kw in brief: score["django"] += 2
if "rapid development" in brief: score["django"] += 1

# FastAPI signals
for kw in ["ml model", "high concurrency", "async", "websocket", "openapi", "pydantic"]:
    if kw in brief: score["fastapi"] += 2
if "microservice" in brief: score["fastapi"] += 2
if "ai" in brief or "inference" in brief: score["fastapi"] += 1

# Flask signals
for kw in ["prototype", "internal tool", "minimal", "small", "flexibility"]:
    if kw in brief: score["flask"] += 2
if "learning" in brief: score["flask"] += 1

choice = max(score, key=score.get)
print(json.dumps({"framework": choice, "scores": score}, indent=2))
PY
