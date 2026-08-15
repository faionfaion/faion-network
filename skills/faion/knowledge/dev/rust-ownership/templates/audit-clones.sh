#!/usr/bin/env bash
# purpose: surface gratuitous .clone() calls and Rc/RefCell across spawn boundaries
# consumes: Cargo project
# produces: clippy report + clone-count baseline
# depends-on: content/01-core-rules.xml#clone-audit-in-ci
# token-budget-impact: ~160 tokens
# Usage: bash scripts/audit-clones.sh
set -euo pipefail

cargo clippy --all-targets -- \
  -W clippy::needless_clone \
  -W clippy::redundant_clone \
  -W clippy::clone_on_copy \
  -W clippy::implicit_clone 2>&1 | tee target/clippy-clones.txt

echo "--- Clone call count in src/ ---"
grep -rn '\.clone()\|\.to_string()\|\.to_owned()' src/ | wc -l

# Rc / RefCell are !Send + !Sync — flag any file that both uses them and spawns.
echo "--- Files using Rc/RefCell that also spawn ---"
for f in $(grep -rl 'Rc<\|RefCell<' src/ || true); do
  if grep -q 'thread::spawn\|tokio::spawn\|rayon::' "$f"; then
    echo "  $f  (see rule arc-mutex-across-threads)"
  fi
done

echo "--- clippy-clones.txt written to target/ ---"
