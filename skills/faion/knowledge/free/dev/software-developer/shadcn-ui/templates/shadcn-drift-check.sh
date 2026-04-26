#!/usr/bin/env bash
# shadcn-drift-check.sh — warn when local ui/ files diverge from upstream registry.
# Usage: shadcn-drift-check.sh [components/ui/*.tsx ...]
# Run weekly in CI to surface upstream bugfixes.
set -euo pipefail
ROOT="${ROOT:-components/ui}"
DRIFT=0
TMPDIR_WORK="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_WORK"' EXIT

for f in "$@"; do
  name="$(basename "$f" .tsx)"
  pristine="$TMPDIR_WORK/$name.tsx"

  # Download pristine version from upstream (skip on network error)
  npx --yes shadcn@latest add "$name" --yes \
      --cwd "$TMPDIR_WORK" >/dev/null 2>&1 || continue

  target="$TMPDIR_WORK/$ROOT/$name.tsx"
  [ -f "$target" ] || continue

  cp "$target" "$pristine"

  if ! diff -q "$f" "$pristine" >/dev/null 2>&1; then
    echo "drift: $f differs from upstream"
    diff -u "$pristine" "$f" | head -30
    DRIFT=$((DRIFT + 1))
  fi
done

[ "$DRIFT" -eq 0 ] && echo "OK — no drift" || { echo "drift in $DRIFT file(s)"; exit 1; }
