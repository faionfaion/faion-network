#!/usr/bin/env bash
# rollback.sh — Git-based rollback: checkout previous commit, redeploy
# Usage: bash rollback.sh <service> [<ref>]
#   <ref> defaults to HEAD~1; can be commit hash, tag, or HEAD~N
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/workspace/repos}"
DEPLOY_SCRIPT="$(dirname "$0")/deploy.sh"

SERVICE="${1:?Usage: rollback.sh <service> [<ref>]}"
REF="${2:-HEAD~1}"
SRC="$WORKSPACE/$SERVICE"

[[ ! -d "$SRC/.git" ]] && { echo "ERROR: $SRC is not a git repo"; exit 1; }

CURRENT=$(git -C "$SRC" rev-parse --short HEAD)
CURRENT_MSG=$(git -C "$SRC" log -1 --format="%s")
echo "[ROLLBACK] $SERVICE"
echo "  current: $CURRENT  ($CURRENT_MSG)"
echo "  target:  $REF"

git -C "$SRC" checkout "$REF"
NEW=$(git -C "$SRC" rev-parse --short HEAD)

bash "$DEPLOY_SCRIPT" "$SERVICE"

echo "[ROLLBACK DONE] $SERVICE: $CURRENT → $NEW"
echo "To return to main:"
echo "  git -C $SRC checkout main && bash $DEPLOY_SCRIPT $SERVICE"
