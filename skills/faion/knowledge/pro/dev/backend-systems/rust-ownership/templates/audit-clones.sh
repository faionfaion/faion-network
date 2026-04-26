#!/usr/bin/env bash
# Surface gratuitous clone() calls in a crate for review.
# Usage: bash scripts/audit-clones.sh
set -euo pipefail

cargo clippy --all-targets -- \
  -W clippy::needless_clone \
  -W clippy::redundant_clone \
  -W clippy::clone_on_copy \
  -W clippy::implicit_clone 2>&1 | tee target/clippy-clones.txt

echo "--- Clone call count in src/ ---"
grep -rn '\.clone()\|\.to_string()\|\.to_owned()' src/ | wc -l

echo "--- clippy-clones.txt written to target/ ---"
