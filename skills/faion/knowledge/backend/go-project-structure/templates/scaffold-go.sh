#!/usr/bin/env bash
# __faion_header_v1__
# purpose: Bootstrap the standard Go tree — cmd/, internal/, pkg/, migrations/, Makefile, go.mod
# consumes: module path + binary names
# produces: code
# depends-on: content/04-procedure.xml + content/01-core-rules.xml#cmd-internal-default
# token-budget-impact: ~340 tokens when loaded as context
# faion_header_json: {"__faion_header__":{"purpose":"Bootstrap the standard Go tree — cmd/, internal/, pkg/, migrations/, Makefile, go.mod","consumes":"module path + binary names","produces":"code","depends_on":"content/04-procedure.xml + content/01-core-rules.xml#cmd-internal-default","token_budget_impact":"~340 tokens when loaded as context"}}
# Usage: ./scaffold-go.sh github.com/org/name api worker
set -euo pipefail

MOD="${1:?module path required (e.g. github.com/org/name)}"
shift
BINS=("$@")
if [[ ${#BINS[@]} -eq 0 ]]; then
  BINS=("api")
fi

mkdir -p api deployments docs migrations pkg

for bin in "${BINS[@]}"; do
  mkdir -p "cmd/$bin"
  cat > "cmd/$bin/main.go" <<GOEOF
package main

import "log"

// Keep this thin: flags, config, wiring, app.Run(ctx). No business logic.
func main() {
	log.Println("$bin: starting")
}
GOEOF
done

for pkg in config database handler middleware model repository service shared; do
  mkdir -p "internal/$pkg"
done

go mod init "$MOD"
gofmt -w . 2>/dev/null || true

echo "scaffold ready: $MOD | binaries: ${BINS[*]}"
echo "next: author the Makefile targets and run 'go list -deps ./...' to confirm zero cycles"
