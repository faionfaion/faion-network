#!/usr/bin/env bash
# Pre-commit error-handling gate for Go projects.
# Usage: bash scripts/check-errors.sh
set -euo pipefail

go vet ./...
errcheck -ignoretests ./...
golangci-lint run --enable=errorlint,wrapcheck,nilerr,errcheck,gocritic ./...

# Forbid storage sentinels leaking outside repository layer
if grep -rn 'sql\.ErrNoRows\|pgx\.ErrNoRows\|mongo\.ErrNoDocuments' \
    --include='*.go' \
    --exclude-dir=internal/repository \
    --exclude-dir=internal/storage .; then
  echo "ERROR: storage sentinel leaked outside repository layer"
  exit 1
fi

echo "Error handling checks passed."
