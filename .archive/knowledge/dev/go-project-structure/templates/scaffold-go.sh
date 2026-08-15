#!/usr/bin/env bash
# purpose: Bootstrap script: create cmd/, internal/, pkg/, migrations/, Makefile
# consumes: See content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
# scaffold-go.sh — materialise a standard Go project tree
# Usage: ./scaffold-go.sh github.com/org/name api worker
# Creates: cmd/<bin>/main.go, internal/{config,database,handler,middleware,model,repository,service}/, pkg/, api/, Makefile, go.mod

set -euo pipefail

MOD="${1:?module path required (e.g. github.com/org/name)}"
shift
BINS=("$@")

if [[ ${#BINS[@]} -eq 0 ]]; then
  BINS=("api")
fi

mkdir -p api deployments docs scripts pkg

for bin in "${BINS[@]}"; do
  mkdir -p "cmd/$bin"
  cat > "cmd/$bin/main.go" <<GOEOF
package main

import "log"

func main() {
	log.Println("$bin: starting")
}
GOEOF
done

for pkg in config database handler middleware model repository service; do
  mkdir -p "internal/$pkg"
done

go mod init "$MOD"
gofmt -w . 2>/dev/null || true

echo "scaffold ready: $MOD | binaries: ${BINS[*]}"
