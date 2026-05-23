# purpose: Bash scaffold: bootstrap shadcn primitive directory + cn util.
# consumes: see content/02-output-contract.xml inputs for shadcn-ui-architecture
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-700 tokens when loaded as context
#!/usr/bin/env bash
# Usage: ./scaffold.sh button card dialog form input label
# Adds shadcn primitives from the registry, then generates a barrel export.
# Requires: npx shadcn@latest (Node + configured project)
set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <component> [component...]" >&2
  exit 1
fi

for c in "$@"; do
  echo "Adding $c..."
  npx shadcn@latest add "$c" --yes
done

BARREL="components/ui/index.ts"
{
  echo "// auto-generated barrel — do not edit manually"
  for c in "$@"; do
    echo "export * from './$c';"
  done
} > "$BARREL"

echo "Barrel written to $BARREL"
npx tsc --noEmit
echo "Scaffolded: $*"
