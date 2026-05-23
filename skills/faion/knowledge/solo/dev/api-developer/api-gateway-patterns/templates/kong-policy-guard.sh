#!/usr/bin/env bash
# purpose: Template helper for API Gateway Patterns (kong-policy-guard.sh).
# consumes: see content/02-output-contract.xml inputs for api-gateway-patterns
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
# kong-policy-guard.sh — fail CI if any public route is missing required plugins.
# Usage: ./kong-policy-guard.sh [path/to/kong.yml]
set -euo pipefail

CFG="${1:-ops/kong.yml}"
REQUIRED_PLUGINS=(jwt rate-limiting cors)

python3 - "$CFG" <<'PY'
import sys, yaml

cfg = yaml.safe_load(open(sys.argv[1]))
required = {"jwt", "rate-limiting", "cors"}
public_tag = "public"
fails = []

for svc in cfg.get("services", []):
    for route in svc.get("routes", []):
        tags = set(route.get("tags") or []) | set(svc.get("tags") or [])
        if public_tag not in tags:
            continue
        # Collect plugins from service + route + global
        plugins = {
            p.get("name")
            for src in (svc.get("plugins") or [], route.get("plugins") or [])
            for p in src
        }
        # Also collect global plugins from top-level
        for req in required:
            if req not in plugins:
                fails.append(f"{svc.get('name')}/{route.get('name')}: missing plugin '{req}'")

if fails:
    print("FAIL — missing required plugins:")
    for f in fails:
        print(f"  {f}")
    sys.exit(1)

print("OK — all public routes have required plugins")
PY
