#!/usr/bin/env bash
# rollback.sh — Roll back a service to a previous commit or tag and redeploy
# Usage: ./rollback.sh <service> [<ref>]
#   <ref>  git ref to check out (default: HEAD~1)
#   Examples:
#     ./rollback.sh nero-core          # roll back one commit
#     ./rollback.sh nero-core HEAD~3   # roll back three commits
#     ./rollback.sh nero-core v1.4.2   # roll back to tag
set -euo pipefail

WORKSPACE=~/workspace/repos
DEPLOY_SCRIPT="$(dirname "$0")/deploy.sh"

SERVICE="${1:?Usage: rollback.sh <service> [<ref>]}"
REF="${2:-HEAD~1}"

SRC="$WORKSPACE/$SERVICE"

if [[ ! -d "$SRC/.git" ]]; then
    echo "ERROR: $SRC is not a git repository" >&2
    exit 1
fi

CURRENT=$(git -C "$SRC" rev-parse --short HEAD)
echo "[ROLLBACK] $SERVICE: $CURRENT → $REF"

git -C "$SRC" checkout "$REF"

bash "$DEPLOY_SCRIPT" "$SERVICE"

echo "[ROLLBACK DONE] $SERVICE is now at $(git -C "$SRC" rev-parse --short HEAD)"
echo "To return to main: git -C $SRC checkout main && $DEPLOY_SCRIPT $SERVICE"
