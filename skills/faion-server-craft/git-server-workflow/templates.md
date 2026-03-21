# Git Server Workflow Templates

## Master Deploy Script

```bash
#!/bin/bash
# deploy.sh
# Deploy NERO platform services from workspace to runtime
# Usage:
#   deploy.sh nero-core              # Deploy single service
#   deploy.sh all                    # Deploy all services
#   deploy.sh nero-core --rebuild-venv  # Rebuild virtualenv
#   deploy.sh all --rebuild-venv     # Deploy all with fresh venvs

set -euo pipefail

WORKSPACE="$HOME/workspace/repos"
RUNTIME="/srv/nero"
ENV_FILE="$HOME/workspace/.env"
REBUILD_VENV=false

# Parse arguments
SERVICE="${1:?Usage: $0 <service-name|all> [--rebuild-venv]}"
shift
for arg in "$@"; do
    case "$arg" in
        --rebuild-venv) REBUILD_VENV=true ;;
        *) echo "Unknown option: $arg"; exit 1 ;;
    esac
done

# Service definitions
declare -A SERVICES=(
    [nero-sdk]="python:library"
    [nero-core]="python:service"
    [nero-channel-web]="python:service"
    [nero-channel-tg]="python:service"
    [nero-web]="node:static"
)

# Deploy order (dependencies first)
DEPLOY_ORDER=(nero-sdk nero-core nero-channel-web nero-channel-tg nero-web)

log() { echo "$(date '+%H:%M:%S') [$1] $2"; }

deploy_python_service() {
    local name="$1"
    local src="$WORKSPACE/$name"
    local dst="$RUNTIME/$name"

    log "$name" "Syncing source code..."
    rsync -a --delete \
        --exclude='.venv' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='*.pyc' \
        --exclude='.pytest_cache' \
        --exclude='.mypy_cache' \
        --exclude='.ruff_cache' \
        "$src/src/" "$dst/src/"

    # Sync config files
    for f in requirements.txt pyproject.toml setup.py setup.cfg; do
        [ -f "$src/$f" ] && rsync -a "$src/$f" "$dst/$f"
    done

    # Handle virtualenv
    if [ "$REBUILD_VENV" = true ] || [ ! -d "$dst/.venv" ]; then
        log "$name" "Creating virtualenv..."
        rm -rf "$dst/.venv"
        python3 -m venv "$dst/.venv"
        "$dst/.venv/bin/pip" install -q --upgrade pip setuptools wheel
        "$dst/.venv/bin/pip" install -q -r "$dst/requirements.txt"

        # Install SDK if it's a dependency
        if [ "$name" != "nero-sdk" ] && [ -d "$RUNTIME/nero-sdk" ]; then
            "$dst/.venv/bin/pip" install -q -e "$RUNTIME/nero-sdk"
        fi
    else
        # Install only if requirements changed
        if ! diff -q "$src/requirements.txt" "$dst/.last-requirements.txt" &>/dev/null 2>&1; then
            log "$name" "Requirements changed, installing..."
            "$dst/.venv/bin/pip" install -q -r "$dst/requirements.txt"

            if [ "$name" != "nero-sdk" ] && [ -d "$RUNTIME/nero-sdk" ]; then
                "$dst/.venv/bin/pip" install -q -e "$RUNTIME/nero-sdk"
            fi
        fi
    fi

    # Save last deployed requirements
    cp "$dst/requirements.txt" "$dst/.last-requirements.txt" 2>/dev/null || true
}

deploy_python_library() {
    local name="$1"
    local src="$WORKSPACE/$name"
    local dst="$RUNTIME/$name"

    log "$name" "Syncing library..."
    rsync -a --delete \
        --exclude='.venv' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='*.pyc' \
        --exclude='*.egg-info' \
        "$src/" "$dst/"
}

deploy_node_static() {
    local name="$1"
    local src="$WORKSPACE/$name"
    local dst="$RUNTIME/$name"

    # Build if needed
    if [ -f "$src/package.json" ]; then
        log "$name" "Building..."
        cd "$src"
        npm install --silent 2>/dev/null
        npm run build --silent 2>/dev/null
    fi

    log "$name" "Syncing dist..."
    mkdir -p "$dst"
    rsync -a --delete "$src/dist/" "$dst/dist/"
    rsync -a "$src/package.json" "$dst/package.json"
}

restart_service() {
    local name="$1"
    log "$name" "Restarting service..."
    systemctl --user restart "$name" 2>/dev/null || true

    sleep 2

    if systemctl --user is-active --quiet "$name" 2>/dev/null; then
        log "$name" "Running"
    else
        log "$name" "FAILED TO START"
        journalctl --user -u "$name" --since "30 sec ago" --no-pager | tail -5
        return 1
    fi
}

deploy_service() {
    local name="$1"
    local type="${SERVICES[$name]:-}"

    if [ -z "$type" ]; then
        echo "Unknown service: $name"
        return 1
    fi

    log "$name" "=== Deploying ==="

    case "$type" in
        python:library)
            deploy_python_library "$name"
            ;;
        python:service)
            deploy_python_service "$name"
            restart_service "$name"
            ;;
        node:static)
            deploy_node_static "$name"
            restart_service "$name"
            ;;
    esac

    log "$name" "=== Done ==="
    echo ""
}

# Main
echo "=== NERO Deploy $(date '+%Y-%m-%d %H:%M:%S') ==="
echo ""

if [ "$SERVICE" = "all" ]; then
    for svc in "${DEPLOY_ORDER[@]}"; do
        deploy_service "$svc"
    done
else
    deploy_service "$SERVICE"
fi

echo "=== Deploy complete ==="
```

## Post-Receive Hook Template

```bash
#!/bin/bash
# /srv/git/nero-core.git/hooks/post-receive
# Auto-deploy on push to main branch

set -euo pipefail

DEPLOY_SCRIPT="/home/nero/workspace/deploy/deploy.sh"
LOG_FILE="/var/log/nero-deploy.log"

while read oldrev newrev refname; do
    BRANCH=$(git rev-parse --symbolic --abbrev-ref "$refname" 2>/dev/null || echo "")

    if [ "$BRANCH" = "main" ]; then
        echo "=== Deploying $(basename $(pwd) .git) ==="

        # Update workspace repo
        SERVICE_NAME=$(basename $(pwd) .git)
        GIT_WORK_TREE="/home/nero/workspace/repos/$SERVICE_NAME" git checkout -f main

        # Run deploy script
        echo "$(date) Deploying $SERVICE_NAME (commit: ${newrev:0:8})" >> "$LOG_FILE"
        bash "$DEPLOY_SCRIPT" "$SERVICE_NAME" 2>&1 | tee -a "$LOG_FILE"

        echo "=== Deploy complete ==="
    else
        echo "Pushed to $BRANCH, skipping deploy (only main triggers deploy)"
    fi
done
```

## Worktree Management Script

```bash
#!/bin/bash
# worktree-manage.sh
# Manage git worktrees for parallel agent work
# Usage:
#   worktree-manage.sh create nero-core feature-auth
#   worktree-manage.sh list
#   worktree-manage.sh remove nero-core feature-auth
#   worktree-manage.sh clean

set -euo pipefail

REPOS_DIR="$HOME/workspace/repos"
ACTION="${1:?Usage: $0 <create|list|remove|clean> [repo-name] [branch-name]}"

case "$ACTION" in
    create)
        REPO="${2:?Usage: $0 create <repo-name> <branch-name>}"
        BRANCH="${3:?Usage: $0 create <repo-name> <branch-name>}"
        REPO_DIR="$REPOS_DIR/$REPO"
        WORKTREE="$REPOS_DIR/${REPO}-${BRANCH}"

        cd "$REPO_DIR"

        # Create branch if doesn't exist
        if ! git show-ref --verify --quiet "refs/heads/$BRANCH" 2>/dev/null; then
            git branch "$BRANCH"
        fi

        git worktree add "$WORKTREE" "$BRANCH"
        echo "Created: $WORKTREE"
        echo "  cd $WORKTREE"
        ;;

    list)
        for repo in "$REPOS_DIR"/*/; do
            repo_name=$(basename "$repo")
            if [ -d "$repo/.git" ] || [ -f "$repo/.git" ]; then
                worktrees=$(cd "$repo" && git worktree list 2>/dev/null | wc -l)
                if [ "$worktrees" -gt 1 ]; then
                    echo "=== $repo_name ($worktrees worktrees) ==="
                    cd "$repo" && git worktree list
                    echo ""
                fi
            fi
        done
        ;;

    remove)
        REPO="${2:?Usage: $0 remove <repo-name> <branch-name>}"
        BRANCH="${3:?Usage: $0 remove <repo-name> <branch-name>}"
        REPO_DIR="$REPOS_DIR/$REPO"
        WORKTREE="$REPOS_DIR/${REPO}-${BRANCH}"

        cd "$REPO_DIR"
        git worktree remove "$WORKTREE"
        echo "Removed: $WORKTREE"
        ;;

    clean)
        for repo in "$REPOS_DIR"/*/; do
            if [ -d "$repo/.git" ]; then
                cd "$repo"
                PRUNED=$(git worktree prune -v 2>&1 | grep -c "Removing" || true)
                if [ "$PRUNED" -gt 0 ]; then
                    repo_name=$(basename "$repo")
                    echo "Pruned $PRUNED stale worktrees in $repo_name"
                fi
            fi
        done
        echo "Done"
        ;;

    *)
        echo "Usage: $0 <create|list|remove|clean> [repo-name] [branch-name]"
        exit 1
        ;;
esac
```

## Rollback Script

```bash
#!/bin/bash
# rollback.sh
# Rollback a service to a previous commit
# Usage:
#   rollback.sh nero-core HEAD~1
#   rollback.sh nero-core v1.2.3
#   rollback.sh nero-core abc1234

set -euo pipefail

SERVICE="${1:?Usage: $0 <service-name> <commit|tag|HEAD~N>}"
TARGET="${2:?Usage: $0 <service-name> <commit|tag|HEAD~N>}"

REPO="$HOME/workspace/repos/$SERVICE"
DEPLOY_SCRIPT="$HOME/workspace/deploy/deploy.sh"

echo "=== Rollback $SERVICE to $TARGET ==="

cd "$REPO"

# Save current position
CURRENT=$(git rev-parse HEAD)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo "Current: $(git log --oneline -1)"
echo "Rolling back to: $TARGET"

# Checkout target
git checkout "$TARGET"
echo "Now at: $(git log --oneline -1)"

# Deploy
bash "$DEPLOY_SCRIPT" "$SERVICE"

# Return to original branch
git checkout "$CURRENT_BRANCH"

echo ""
echo "=== Rollback complete ==="
echo "Runtime is now running commit: $(git log --oneline "$TARGET" -1)"
echo "Workspace HEAD is back on: $CURRENT_BRANCH"
echo ""
echo "To make this permanent, revert the bad commits:"
echo "  cd $REPO"
echo "  git revert $CURRENT"
```

## Deploy Status Script

```bash
#!/bin/bash
# deploy-status.sh
# Show what's deployed vs what's in workspace

set -euo pipefail

WORKSPACE="$HOME/workspace/repos"
RUNTIME="/srv/nero"

echo "=== Deploy Status ==="
printf "%-20s %-12s %-12s %s\n" "SERVICE" "WORKSPACE" "RUNTIME" "DIFF"

for service in nero-sdk nero-core nero-channel-web nero-channel-tg nero-web; do
    ws_dir="$WORKSPACE/$service"
    rt_dir="$RUNTIME/$service"

    if [ ! -d "$ws_dir" ]; then
        printf "%-20s %-12s %-12s %s\n" "$service" "MISSING" "-" "-"
        continue
    fi

    # Get workspace commit
    ws_commit=$(cd "$ws_dir" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")

    # Compare source files
    if [ -d "$rt_dir/src" ]; then
        diff_count=$(diff -rq "$ws_dir/src/" "$rt_dir/src/" \
            --exclude='__pycache__' --exclude='*.pyc' 2>/dev/null | wc -l || echo "?")
        if [ "$diff_count" = "0" ]; then
            status="IN SYNC"
        else
            status="$diff_count files differ"
        fi
    elif [ -d "$rt_dir/dist" ]; then
        status="(static build)"
    else
        status="NOT DEPLOYED"
    fi

    printf "%-20s %-12s %-12s %s\n" "$service" "$ws_commit" "-" "$status"
done
```
