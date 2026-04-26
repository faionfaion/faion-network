#!/usr/bin/env bash
# worktree.sh — Git worktree create/list/remove/clean management
# Usage: bash worktree.sh <command> [args]
#   create <name> [branch]   — create worktree at ../<repo>-<name>
#   list                     — list all worktrees
#   remove <name>            — remove worktree and branch
#   clean                    — prune stale worktrees
set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || { echo "ERROR: not a git repo"; exit 1; })
REPO_NAME=$(basename "$REPO_ROOT")
CMD="${1:-list}"

case "$CMD" in
    create)
        NAME="${2:?Usage: worktree.sh create <name> [branch]}"
        BRANCH="${3:-agent/${NAME}}"
        TARGET="$(dirname "$REPO_ROOT")/${REPO_NAME}-${NAME}"

        if [[ -d "$TARGET" ]]; then
            echo "ERROR: $TARGET already exists"
            exit 1
        fi

        git worktree add "$TARGET" -b "$BRANCH"
        echo "[OK] Worktree created: $TARGET (branch: $BRANCH)"
        echo "Run: cd $TARGET"
        ;;

    list)
        git worktree list
        ;;

    remove)
        NAME="${2:?Usage: worktree.sh remove <name>}"
        TARGET="$(dirname "$REPO_ROOT")/${REPO_NAME}-${NAME}"
        BRANCH="agent/${NAME}"

        git worktree remove "$TARGET" 2>/dev/null || echo "[WARN] Could not remove worktree dir (may not exist)"
        git branch -d "$BRANCH" 2>/dev/null || echo "[WARN] Could not delete branch $BRANCH (may not exist or not merged)"
        echo "[OK] Removed worktree: $TARGET"
        ;;

    clean)
        git worktree prune -v
        echo "[OK] Stale worktrees pruned"
        ;;

    *)
        echo "Usage: worktree.sh <create|list|remove|clean> [args]"
        exit 1
        ;;
esac
