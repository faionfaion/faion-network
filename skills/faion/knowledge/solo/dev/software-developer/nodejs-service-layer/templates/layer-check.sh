#!/usr/bin/env bash
# layer-check.sh — fail CI if controllers depend on repos or services depend on framework.
# Usage: bash layer-check.sh [src-dir]
set -euo pipefail
ROOT="${1:-src}"

# 1. ESLint with eslint-plugin-boundaries (assumes config in repo)
npx --yes eslint "$ROOT/**/*.ts" --max-warnings=0

# 2. dependency-cruiser custom rules
cat > /tmp/dc.json <<'JSON'
{
  "forbidden": [
    {
      "name": "ctrl-no-repo",
      "from": { "path": "controllers" },
      "to": { "path": "repositories" },
      "comment": "Controllers must call services, not repositories."
    },
    {
      "name": "svc-no-framework",
      "from": { "path": "services" },
      "to": { "path": "node_modules/(express|fastify|@nestjs/core)" },
      "comment": "Services are framework-agnostic."
    },
    {
      "name": "no-circular",
      "severity": "error",
      "from": {},
      "to": { "circular": true }
    }
  ]
}
JSON
npx --yes dependency-cruiser --config /tmp/dc.json --output-type err "$ROOT"

# 3. Circular dependency check
npx --yes madge --circular --extensions ts "$ROOT"

echo "Layer check OK"
