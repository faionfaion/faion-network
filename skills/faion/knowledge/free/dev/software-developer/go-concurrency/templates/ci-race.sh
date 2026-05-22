#!/usr/bin/env bash
# purpose: CI gate — vet, race detector x3 (or x10 for critical), staticcheck.
# consumes: cwd = repo root with go.mod; ./... or specific package list.
# produces: exit 0 on pass; non-zero with stderr report on failure.
# depends-on: go toolchain, staticcheck (`go install honnef.co/go/tools/cmd/staticcheck`).
# token-budget-impact: 0 — shell script, not loaded into LLM context.
set -euo pipefail
go vet ./...
go test -race -count=3 -timeout=120s ./...
go run honnef.co/go/tools/cmd/staticcheck@latest ./...
