#!/usr/bin/env bash
# find-patterns.sh
#
# Phase 2 helper: discover service, handler, model, and migration patterns
# in a codebase using ripgrep. Run this before writing architecture decisions.
#
# Usage:
#   bash find-patterns.sh [SRC_DIR]
#   Default SRC_DIR: current directory (.)
#
# Requires: ripgrep (rg) — install with: apt install ripgrep

set -euo pipefail

SRC="${1:-.}"

if ! command -v rg &>/dev/null; then
    echo "ERROR: ripgrep (rg) not found. Install: apt install ripgrep" >&2
    exit 1
fi

echo "=== Services ==="
rg --type ts --type py -l "class.*Service" "$SRC" 2>/dev/null | head -20 || true

echo ""
echo "=== Controllers / Handlers / Routers ==="
rg --type ts -l "class.*Controller|export.*Router|@app\.route" "$SRC" 2>/dev/null | head -20 || true
rg --type py -l "class.*ViewSet|class.*APIView|@router\." "$SRC" 2>/dev/null | head -20 || true

echo ""
echo "=== Models ==="
rg --type py -l "class.*\(models\.Model\)" "$SRC" 2>/dev/null | head -20 || true
rg --type ts -l "interface.*{|type.*=" "$SRC" 2>/dev/null | head -10 || true

echo ""
echo "=== Existing migrations ==="
find "$SRC" \( -name "*.sql" -o -name "*migration*" \) 2>/dev/null | head -20 || true

echo ""
echo "=== Test patterns ==="
rg --type py -l "class.*TestCase|def test_" "$SRC" 2>/dev/null | head -10 || true
rg --type ts -l "describe\(|it\(|test\(" "$SRC" 2>/dev/null | head -10 || true

echo ""
echo "Pattern discovery complete for: $SRC"
