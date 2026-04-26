#!/usr/bin/env bash
# bp2026-drift.sh — detect drift from the 2026 baseline.
# Usage: bp2026-drift.sh path/to/repo
set -euo pipefail
root="${1:-.}"
fail=0
note() { echo "- $*"; fail=1; }
if [ -f "$root/tsconfig.json" ]; then
  for k in '"strict": true' '"noUncheckedIndexedAccess": true' '"verbatimModuleSyntax": true'; do
    grep -q "$k" "$root/tsconfig.json" || note "tsconfig missing: $k"
  done
fi
if [ -f "$root/package.json" ]; then
  node -e '
    const p=require(process.argv[1]);
    const dep={...(p.dependencies||{}),...(p.devDependencies||{})};
    const want={typescript:"^5",react:"^19",next:"^15"};
    for (const [k,v] of Object.entries(want)) {
      if (k in dep && !new RegExp(v).test(dep[k]))
        console.log("- "+k+" pinned at "+dep[k]+", want "+v);
    }
  ' "$root/package.json"
fi
if [ -f "$root/pyproject.toml" ]; then
  grep -E 'python = "\\^?3\\.(12|13)' "$root/pyproject.toml" >/dev/null || note "Python <3.12"
  grep -q "ruff" "$root/pyproject.toml" || note "ruff not configured"
fi
exit $fail
