#!/usr/bin/env bash
# find-circular-imports.sh — Grep for unaliased cross-app model imports likely to cause circular deps.
# Run from project root. Adjust APP_PREFIX to your project's apps namespace.

set -euo pipefail

APP_PREFIX=${1:-apps}
SRC_DIR=${2:-.}

echo "==> Scanning for unaliased cross-app imports in $SRC_DIR (prefix: $APP_PREFIX)..."
echo ""

# Pattern 1: Direct model import from another app (unaliased)
# e.g. "from apps.users.models import User" — should be aliased
echo "── Unaliased cross-app model imports ──────────────────────────────────"
grep -rn \
    --include="*.py" \
    --exclude-dir=".git" \
    --exclude-dir="migrations" \
    -E "from ${APP_PREFIX}\.[a-z_]+\.(models|services|selectors) import [A-Z]" \
    "$SRC_DIR" || echo "  (none found)"

echo ""

# Pattern 2: Multi-dot relative imports (should be absolute)
echo "── Multi-dot relative imports (fragile) ───────────────────────────────"
grep -rn \
    --include="*.py" \
    --exclude-dir=".git" \
    --exclude-dir="migrations" \
    -E "^from \.\.(\.*)?" \
    "$SRC_DIR" || echo "  (none found)"

echo ""

# Pattern 3: Star imports
echo "── Wildcard imports (never allowed) ───────────────────────────────────"
grep -rn \
    --include="*.py" \
    --exclude-dir=".git" \
    -E "^from .+ import \*" \
    "$SRC_DIR" || echo "  (none found)"

echo ""
echo "==> Scan complete."
echo ""
echo "Fix: Replace unaliased imports with:"
echo "  from ${APP_PREFIX}.users import models as user_models"
echo "  # then use: user_models.User"
