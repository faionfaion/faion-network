# Deploy Scripts

## Overview

Deployment automation for solo developer VPS platforms using the workspace/runtime separation pattern. Covers rsync-based code deployment, virtualenv management, dependency resolution, service restart orchestration, rollback procedures, zero-downtime deploy, pre-deploy validation, and deploy hooks. Designed for systemd user services deployed from a workspace directory to a runtime directory.

**Target:** Ubuntu 24.04 VPS with workspace/runtime separation pattern (source in ~/workspace/repos/, runtime in /srv/nero/).

## When to Use

| Scenario | Fit |
|----------|-----|
| Deploying code changes to production | Essential |
| Setting up initial deploy pipeline | Essential |
| Adding a new service to deploy | Essential |
| Rolling back a bad deployment | Essential |
| Rebuilding virtualenvs after Python upgrade | Recommended |
| Automating post-deploy validation | Recommended |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Workspace** | Source code location (~/workspace/repos/), git repos, editable |
| **Runtime** | Execution location (/srv/nero/), deployed code, systemd runs from here |
| **Separation pattern** | Code lives in workspace, gets deployed (rsync) to runtime |
| **pip install -e .** | Editable install, uses pyproject.toml, runtime links to deployed source |
| **Deploy unit** | Single service that can be deployed independently |
| **Deploy hook** | Script that runs at a specific point in the deploy lifecycle |
| **Rollback** | Reverting to previous deployment state |

## Workspace/Runtime Separation

### Why Separate?

| Concern | Workspace | Runtime |
|---------|-----------|---------|
| Purpose | Development, git operations | Service execution |
| Location | ~/workspace/repos/ | /srv/nero/ |
| Ownership | User (nero) | User (nero) |
| Contents | Full git repo, tests, docs | Deployed source, .venv |
| Modification | Frequent (development) | Only during deploy |
| Backup | Git (remote repo) | Not needed (reproducible) |

### Directory Mapping

```
~/workspace/repos/nero-core/     →  /srv/nero/nero-core/src/
~/workspace/repos/nero-core/     →  /srv/nero/nero-core/.venv/
~/workspace/repos/nero-channel-web/ →  /srv/nero/nero-channel-web/src/
~/workspace/repos/nero-web/dist/ →  /srv/nero/nero-web/dist/
```

## Deploy Flow

### Single Service Deploy

```
1. Pre-deploy checks
   ├── Validate .env exists
   ├── Check disk space
   └── Verify service is defined

2. Sync code
   └── rsync workspace/repos/{service}/ → /srv/nero/{service}/src/

3. Dependencies
   ├── Create/reuse virtualenv
   ├── pip install -e . (uses pyproject.toml)
   └── pip install -r requirements.txt (if exists)

4. Restart service
   └── systemctl --user restart nero-{service}

5. Post-deploy validation
   ├── Wait for service to start
   ├── Check health endpoint
   └── Verify logs for errors
```

### Full Stack Deploy Order

Services must be deployed in dependency order:

```
1. nero-sdk (library, no service)
2. nero-infra (docker-compose, if needed)
3. nero-core (Celery workers)
4. nero-channel-web (FastAPI API)
5. nero-channel-tg (Telegram bot)
6. nero-web (React SPA, static files)
```

### Dependency-Aware Deploy

```
nero-sdk changes    → redeploy: nero-core, nero-channel-web, nero-channel-tg
nero-core changes   → redeploy: nero-core only
nero-web changes    → redeploy: nero-web only (no backend restart)
```

## Deploy Script Architecture

### Main Deploy Script

```bash
#!/bin/bash
# deploy.sh - Main deploy orchestrator
# Usage: bash deploy.sh <service|all> [--rebuild-venv]

set -euo pipefail

WORKSPACE="$HOME/workspace/repos"
RUNTIME="/srv/nero"
ENV_FILE="$HOME/workspace/.env"

SERVICE="${1:?Usage: deploy.sh <service|all> [--rebuild-venv]}"
REBUILD_VENV="${2:-}"

# Service registry
declare -A SERVICES=(
    [nero-sdk]="library"        # No systemd service
    [nero-core]="systemd"
    [nero-channel-web]="systemd"
    [nero-channel-tg]="systemd"
    [nero-web]="static"         # No venv, static files
    [nero-infra]="docker"       # Docker Compose
)

deploy_one() {
    local svc="$1"
    local type="${SERVICES[$svc]}"

    echo "=== Deploying $svc (type: $type) ==="

    case "$type" in
        library)   deploy_library "$svc" ;;
        systemd)   deploy_systemd "$svc" ;;
        static)    deploy_static "$svc" ;;
        docker)    deploy_docker "$svc" ;;
        *)         echo "Unknown type: $type"; exit 1 ;;
    esac
}
```

### rsync Patterns

```bash
# Sync Python service (exclude .git, __pycache__, tests)
rsync -av --delete \
    --exclude='.git/' \
    --exclude='__pycache__/' \
    --exclude='.pytest_cache/' \
    --exclude='*.pyc' \
    --exclude='.venv/' \
    --exclude='.env' \
    --exclude='node_modules/' \
    "$WORKSPACE/$svc/" "$RUNTIME/$svc/src/"

# Sync static files (React build)
rsync -av --delete \
    "$WORKSPACE/nero-web/dist/" "$RUNTIME/nero-web/dist/"
```

### Virtualenv Management

```bash
deploy_systemd() {
    local svc="$1"
    local svc_dir="$RUNTIME/$svc"
    local venv_dir="$svc_dir/.venv"

    # Sync source code
    rsync -av --delete \
        --exclude='.git/' --exclude='__pycache__/' \
        --exclude='.venv/' --exclude='.env' \
        "$WORKSPACE/$svc/" "$svc_dir/src/"

    # Create or rebuild virtualenv
    if [ "$REBUILD_VENV" = "--rebuild-venv" ] || [ ! -d "$venv_dir" ]; then
        echo "Creating virtualenv for $svc..."
        rm -rf "$venv_dir"
        python3 -m venv "$venv_dir"
    fi

    # Install dependencies
    "$venv_dir/bin/pip" install --upgrade pip
    "$venv_dir/bin/pip" install -e "$svc_dir/src/"

    # Symlink shared .env
    ln -sf "$ENV_FILE" "$svc_dir/.env"

    # Restart service
    systemctl --user restart "nero-$svc" || true

    # Verify
    sleep 2
    systemctl --user is-active "nero-$svc" && echo "$svc: OK" || echo "$svc: FAILED"
}
```

## Rollback

### Strategy: Git-Based Rollback

Since workspace contains git repos, rollback means checking out a previous commit and redeploying.

```bash
#!/bin/bash
# rollback.sh - Rollback a service to previous commit
# Usage: bash rollback.sh <service> [commit-hash]

set -euo pipefail

SERVICE="$1"
COMMIT="${2:-HEAD~1}"
WORKSPACE="$HOME/workspace/repos"

cd "$WORKSPACE/$SERVICE"

# Save current state
CURRENT=$(git rev-parse HEAD)
echo "Current: $CURRENT"
echo "Rolling back to: $COMMIT"

# Checkout previous commit
git checkout "$COMMIT"

# Redeploy
bash "$HOME/workspace/deploy/deploy.sh" "$SERVICE"

echo "Rolled back $SERVICE from $CURRENT to $(git rev-parse HEAD)"
echo "To restore: git checkout $CURRENT && bash deploy.sh $SERVICE"
```

### Fast Rollback (Pre-deploy Snapshot)

```bash
# Before deploy: snapshot runtime directory
pre_deploy_snapshot() {
    local svc="$1"
    local snapshot_dir="/srv/nero/.snapshots/$svc/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$snapshot_dir"
    rsync -a "$RUNTIME/$svc/src/" "$snapshot_dir/"
    echo "$snapshot_dir"
}

# Rollback from snapshot
rollback_from_snapshot() {
    local svc="$1"
    local snapshot_dir="$2"
    rsync -av --delete "$snapshot_dir/" "$RUNTIME/$svc/src/"
    systemctl --user restart "nero-$svc"
}
```

## Pre-Deploy Validation

```bash
pre_deploy_check() {
    local errors=0

    # Check .env exists
    if [ ! -f "$ENV_FILE" ]; then
        echo "ERROR: $ENV_FILE not found"
        ((errors++))
    fi

    # Check disk space (need at least 1GB free)
    local free_mb=$(df /srv --output=avail -BM | tail -1 | tr -d ' M')
    if [ "$free_mb" -lt 1024 ]; then
        echo "ERROR: Less than 1GB free disk space ($free_mb MB)"
        ((errors++))
    fi

    # Check systemd user session
    if ! systemctl --user status >/dev/null 2>&1; then
        echo "ERROR: systemd user session not available"
        ((errors++))
    fi

    # Check runtime directory exists
    if [ ! -d "$RUNTIME" ]; then
        echo "ERROR: Runtime directory $RUNTIME not found"
        ((errors++))
    fi

    if [ "$errors" -gt 0 ]; then
        echo "Pre-deploy check failed with $errors error(s)"
        exit 1
    fi

    echo "Pre-deploy checks passed"
}
```

## Post-Deploy Validation

```bash
post_deploy_check() {
    local svc="$1"
    local max_wait=30
    local waited=0

    echo "Waiting for $svc to become healthy..."

    while [ "$waited" -lt "$max_wait" ]; do
        if systemctl --user is-active "nero-$svc" >/dev/null 2>&1; then
            # For HTTP services, check health endpoint
            case "$svc" in
                nero-channel-web)
                    if curl -sf http://127.0.0.1:8100/health >/dev/null 2>&1; then
                        echo "$svc is healthy"
                        return 0
                    fi
                    ;;
                *)
                    echo "$svc is active"
                    return 0
                    ;;
            esac
        fi
        sleep 1
        ((waited++))
    done

    echo "WARNING: $svc did not become healthy within ${max_wait}s"
    systemctl --user status "nero-$svc" --no-pager
    return 1
}
```

## Deploy Hooks

### Hook Points

| Hook | When | Use Case |
|------|------|----------|
| pre-deploy | Before any deploy step | Validation, backup |
| pre-sync | Before rsync | Lock service |
| post-sync | After rsync | Run migrations |
| pre-restart | Before service restart | Drain connections |
| post-restart | After service restart | Health check, notify |
| post-deploy | After all steps | Cleanup, report |

### Hook Implementation

```bash
run_hook() {
    local svc="$1"
    local hook="$2"
    local hook_file="$WORKSPACE/$svc/deploy-hooks/$hook.sh"

    if [ -f "$hook_file" ]; then
        echo "Running hook: $hook for $svc"
        bash "$hook_file" "$svc" "$RUNTIME/$svc"
    fi
}
```

### Example: Migration Hook

```bash
# nero-channel-web/deploy-hooks/post-sync.sh
#!/bin/bash
# Run Alembic migrations after code sync
cd /srv/nero/nero-infra
source /srv/nero/nero-channel-web/.venv/bin/activate
alembic upgrade head
echo "Migrations complete"
```

## Zero-Downtime Deploy (Simple)

For a solo developer VPS, true zero-downtime is usually overkill. But for user-facing services:

```bash
zero_downtime_deploy() {
    local svc="$1"

    # 1. Deploy new code (don't restart yet)
    sync_code "$svc"
    install_deps "$svc"

    # 2. Run migrations (if any)
    run_hook "$svc" "post-sync"

    # 3. Graceful restart (SIGHUP for gunicorn/uvicorn)
    systemctl --user reload "nero-$svc" 2>/dev/null || \
        systemctl --user restart "nero-$svc"

    # 4. Wait and verify
    post_deploy_check "$svc"
}
```

## Related Methodologies

| Methodology | Relationship |
|-------------|-------------|
| [secrets-management](../secrets-management/) | .env symlink during deploy |
| [health-checks-autoheal](../health-checks-autoheal/) | Post-deploy health verification |
| [multi-project-hosting](../multi-project-hosting/) | Per-project deploy scripts |
| [server-init-bootstrap](../server-init-bootstrap/) | Initial runtime directory setup |
