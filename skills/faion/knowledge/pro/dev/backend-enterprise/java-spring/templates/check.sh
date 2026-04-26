#!/usr/bin/env bash
# check.sh — block PR if entities leak from controllers or build/style fails.
# Usage: bash scripts/check.sh
set -euo pipefail

./mvnw -q -DskipTests compile spotless:check checkstyle:check

# Forbid returning entity types from REST controllers
if rg -nP 'public\s+(ResponseEntity<[A-Z]\w+>|[A-Z]\w+)\s+\w+\([^)]*\)\s*\{' \
     src/main/java -g '*Controller.java' \
   | grep -vE 'Response|Dto|ProblemDetail|Page<|Void|String|byte\[\]'; then
  echo "ERROR: Controller appears to return an entity directly — return a DTO."
  exit 1
fi

echo "OK: build clean, no entity leaks"
