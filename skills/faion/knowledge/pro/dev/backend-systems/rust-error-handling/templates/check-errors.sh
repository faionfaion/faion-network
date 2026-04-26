#!/usr/bin/env bash
# CI script: fail PR if forbidden error-handling patterns appear.
# Usage: bash scripts/check-errors.sh
set -euo pipefail

cargo clippy --all-targets --all-features -- \
  -D clippy::unwrap_used \
  -D clippy::expect_used \
  -D clippy::panic \
  -D clippy::todo \
  -D clippy::unimplemented \
  -W clippy::missing_errors_doc

# Forbid Box<dyn Error> in public function signatures
if grep -rn 'pub\s\+fn\b.*Box<dyn\s\+\(std::error::\)\?Error' src/; then
  echo "ERROR: Box<dyn Error> in public API — use a typed error enum"
  exit 1
fi

echo "Error handling checks passed."
