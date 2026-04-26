#!/usr/bin/env bash
# closeout-archive.sh — bundle a project closure archive with checksums.
# Usage: closeout-archive.sh <project-slug>
set -euo pipefail

proj="${1:?usage: closeout-archive.sh <project-slug>}"
out="closeout-${proj}-$(date +%Y%m%d)"

mkdir -p "$out"/{planning,execution,technical,contracts,closure}

cp -r docs/charter*    "$out/planning/"     2>/dev/null || true
cp -r docs/wbs*        "$out/planning/"     2>/dev/null || true
cp -r status-reports/  "$out/execution/"    2>/dev/null || true
cp -r CHANGE-REGISTER* "$out/execution/"    2>/dev/null || true
cp -r RISK-REGISTER*   "$out/execution/"    2>/dev/null || true
cp -r contracts/       "$out/contracts/"    2>/dev/null || true
cp -r docs/runbook*    "$out/closure/"      2>/dev/null || true

( cd "$out" && find . -type f -exec sha256sum {} \; > MANIFEST.sha256 )

tar czf "${out}.tar.gz" "$out"
echo "archive: ${out}.tar.gz"
