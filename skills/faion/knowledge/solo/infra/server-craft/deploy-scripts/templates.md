# Deploy Scripts Templates

## deploy.sh (Main Orchestrator)

Complete deploy script for multi-service platforms.

```bash
#!/bin/bash
# deploy.sh - Deploy NERO platform services
# Usage: bash deploy.sh <service|all> [--rebuild-venv]
#
# Examples:
#   bash deploy.sh nero-core              # Deploy single service
#   bash deploy.sh all                    # Deploy all services
#   bash deploy.sh all --rebuild-venv     # Full rebuild with new venvs
set -euo pipefail

# ============================================================
# Configuration
# ============================================================
WORKSPACE="$HOME/workspace/repos"
RUNTIME="/srv/nero"
ENV_FILE="$HOME/workspace/.env"

SERVICE="${1:?Usage: deploy.sh <service|all> [--rebuild-venv]}"
REBUILD_VENV="${2:-}"

# Service registry: name -> type
# Types: library, systemd, static, docker
declare -A SERVICE_TYPES=(
    [nero-sdk]="library"
    [nero-infra]="docker"
    [nero-core]="systemd"
    [nero-channel-web]="systemd"
    [nero-channel-tg]="systemd"
    [nero-web]="static"
)

# Deploy order (dependency-aware)
DEPLOY_ORDER=(nero-sdk nero-infra nero-core nero-channel-web nero-channel-tg nero-web)

# ============================================================
# Pre-Deploy Checks
# ============================================================
pre_deploy_check() {
    local errors=0

    if [ ! -f "$ENV_FILE" ]; then
        echo "ERROR: $ENV_FILE not found"
        ((errors++))
    fi

    local free_mb
    free_mb=$(df /srv --output=avail -BM | tail -1 | tr -d ' M')
    if [ "$free_mb" -lt 1024 ]; then
        echo "ERROR: Less than 1GB free disk space (${free_mb}MB)"
        ((errors++))
    fi

    if ! systemctl --user status >/dev/null 2>&1; then
        echo "ERROR: systemd user session not available"
        ((errors++))
    fi

    if [ "$errors" -gt 0 ]; then
        echo "Pre-deploy check failed ($errors errors)"
        exit 1
    fi
    echo "Pre-deploy checks passed"
}

# ============================================================
# Deploy Functions
# ============================================================
sync_code() {
    local svc="$1"
    local src="$WORKSPACE/$svc"
    local dst="$RUNTIME/$svc/src"

    mkdir -p "$dst"
    rsync -a --delete \
        --exclude='.git/' \
        --exclude='__pycache__/' \
        --exclude='.pytest_cache/' \
        --exclude='*.pyc' \
        --exclude='.venv/' \
        --exclude='.env' \
        --exclude='node_modules/' \
        --exclude='.direnv/' \
        --exclude='.mypy_cache/' \
        "$src/" "$dst/"
    echo "  Synced: $src -> $dst"
}

setup_venv() {
    local svc="$1"
    local venv="$RUNTIME/$svc/.venv"

    if [ "$REBUILD_VENV" = "--rebuild-venv" ] || [ ! -d "$venv" ]; then
        echo "  Creating virtualenv..."
        rm -rf "$venv"
        python3 -m venv "$venv"
    fi

    "$venv/bin/pip" install --upgrade pip --quiet
    "$venv/bin/pip" install -e "$RUNTIME/$svc/src/" --quiet
    echo "  Dependencies installed"
}

link_env() {
    local svc="$1"
    ln -sf "$ENV_FILE" "$RUNTIME/$svc/.env"
}

restart_service() {
    local svc="$1"
    local unit="nero-${svc#nero-}"
    # Handle "nero-core" -> "nero-core" (not "nero-nero-core")
    if [[ "$svc" == nero-* ]]; then
        unit="$svc"
    fi

    systemctl --user restart "$unit" 2>/dev/null || true
    sleep 2

    if systemctl --user is-active "$unit" >/dev/null 2>&1; then
        echo "  Service $unit: ACTIVE"
    else
        echo "  Service $unit: FAILED"
        journalctl --user -u "$unit" --since "30 sec ago" --no-pager | tail -5
        return 1
    fi
}

# ============================================================
# Deploy by Type
# ============================================================
deploy_library() {
    local svc="$1"
    echo "=== Deploying $svc (library) ==="
    sync_code "$svc"
    echo "  Library synced (no service to restart)"
}

deploy_systemd() {
    local svc="$1"
    echo "=== Deploying $svc (systemd) ==="
    sync_code "$svc"
    setup_venv "$svc"
    link_env "$svc"
    restart_service "$svc"
}

deploy_static() {
    local svc="$1"
    echo "=== Deploying $svc (static) ==="

    local src="$WORKSPACE/$svc"
    local dst="$RUNTIME/$svc"

    # Check if build is needed
    if [ -d "$src/dist" ]; then
        mkdir -p "$dst"
        rsync -a --delete "$src/dist/" "$dst/dist/"
        echo "  Static files synced"
    else
        echo "  WARNING: No dist/ directory. Build first: cd $src && npm run build"
    fi

    restart_service "$svc" 2>/dev/null || true
}

deploy_docker() {
    local svc="$1"
    echo "=== Deploying $svc (docker) ==="
    sync_code "$svc"
    cd "$RUNTIME/$svc/src"
    docker compose up -d
    echo "  Docker services started"
    cd -
}

# ============================================================
# Main
# ============================================================
deploy_one() {
    local svc="$1"
    local type="${SERVICE_TYPES[$svc]:-}"

    if [ -z "$type" ]; then
        echo "ERROR: Unknown service: $svc"
        echo "Available: ${!SERVICE_TYPES[*]}"
        exit 1
    fi

    case "$type" in
        library)  deploy_library "$svc" ;;
        systemd)  deploy_systemd "$svc" ;;
        static)   deploy_static "$svc" ;;
        docker)   deploy_docker "$svc" ;;
    esac
}

echo "============================================================"
echo "Deploy: $SERVICE $([ -n "$REBUILD_VENV" ] && echo "(rebuild venv)" || echo "")"
echo "============================================================"

pre_deploy_check

if [ "$SERVICE" = "all" ]; then
    for svc in "${DEPLOY_ORDER[@]}"; do
        deploy_one "$svc"
        echo ""
    done
else
    deploy_one "$SERVICE"
fi

echo "============================================================"
echo "Deploy complete"
echo "============================================================"
```

## rollback.sh

```bash
#!/bin/bash
# rollback.sh - Rollback a service to a previous git commit
# Usage: bash rollback.sh <service> [commit-hash|HEAD~1]
set -euo pipefail

SERVICE="${1:?Usage: bash rollback.sh <service> [commit-hash]}"
COMMIT="${2:-HEAD~1}"
WORKSPACE="$HOME/workspace/repos"
DEPLOY_SCRIPT="$HOME/workspace/deploy/deploy.sh"

cd "$WORKSPACE/$SERVICE"

CURRENT=$(git rev-parse --short HEAD)
echo "Current commit: $CURRENT ($(git log --oneline -1))"
echo "Rolling back to: $COMMIT"

# Save current state
ROLLBACK_FROM="$CURRENT"

# Checkout target commit
git checkout "$COMMIT"

TARGET=$(git rev-parse --short HEAD)
echo "Now at: $TARGET ($(git log --oneline -1))"

# Redeploy
echo ""
bash "$DEPLOY_SCRIPT" "$SERVICE"

echo ""
echo "============================================================"
echo "Rollback complete: $ROLLBACK_FROM -> $TARGET"
echo "To undo: bash rollback.sh $SERVICE $ROLLBACK_FROM"
echo "============================================================"
```

## pre-deploy-check.sh

Standalone pre-deploy validation script.

```bash
#!/bin/bash
# pre-deploy-check.sh - Validate environment before deployment
# Usage: bash pre-deploy-check.sh
set -euo pipefail

WORKSPACE="$HOME/workspace/repos"
RUNTIME="/srv/nero"
ENV_FILE="$HOME/workspace/.env"

ERRORS=0
WARNINGS=0

check_pass() { echo "[PASS] $1"; }
check_fail() { echo "[FAIL] $1"; ((ERRORS++)); }
check_warn() { echo "[WARN] $1"; ((WARNINGS++)); }

echo "=== Pre-Deploy Validation ==="
echo ""

# Environment
echo "--- Environment ---"
[ -f "$ENV_FILE" ] && check_pass ".env file exists" || check_fail ".env file missing"
[ -d "$RUNTIME" ] && check_pass "Runtime dir exists" || check_fail "Runtime dir missing"
[ -d "$WORKSPACE" ] && check_pass "Workspace dir exists" || check_fail "Workspace dir missing"

# Required env vars
if [ -f "$ENV_FILE" ]; then
    for var in DATABASE_URL REDIS_URL ANTHROPIC_API_KEY RABBITMQ_URL; do
        if grep -q "^$var=" "$ENV_FILE"; then
            check_pass "$var is set"
        else
            check_fail "$var is missing from .env"
        fi
    done
fi

# Disk space
FREE_MB=$(df /srv --output=avail -BM | tail -1 | tr -d ' M')
if [ "$FREE_MB" -gt 5120 ]; then
    check_pass "Disk space: ${FREE_MB}MB free"
elif [ "$FREE_MB" -gt 1024 ]; then
    check_warn "Disk space low: ${FREE_MB}MB free"
else
    check_fail "Disk space critical: ${FREE_MB}MB free"
fi

# systemd
systemctl --user status >/dev/null 2>&1 && \
    check_pass "systemd user session available" || \
    check_fail "systemd user session not available"

# Docker
if command -v docker &>/dev/null; then
    docker info >/dev/null 2>&1 && \
        check_pass "Docker is running" || \
        check_fail "Docker is not running"
fi

# Python
command -v python3 &>/dev/null && \
    check_pass "Python3: $(python3 --version 2>&1)" || \
    check_fail "Python3 not found"

# Git repos (check for uncommitted changes)
echo ""
echo "--- Git Status ---"
for repo in nero-sdk nero-core nero-channel-web nero-channel-tg nero-web nero-infra; do
    repo_dir="$WORKSPACE/$repo"
    if [ -d "$repo_dir/.git" ]; then
        if git -C "$repo_dir" diff --quiet && git -C "$repo_dir" diff --cached --quiet; then
            check_pass "$repo: clean"
        else
            check_warn "$repo: uncommitted changes"
        fi
    fi
done

# Backing services
echo ""
echo "--- Backing Services ---"
curl -sf http://127.0.0.1:5432 2>&1 | grep -q "" && check_warn "PostgreSQL port check (expected)" || true
redis-cli -p 6379 ping >/dev/null 2>&1 && check_pass "Redis: responding" || check_warn "Redis: not responding"

echo ""
echo "=== Results: $ERRORS errors, $WARNINGS warnings ==="
[ "$ERRORS" -eq 0 ] && echo "Ready to deploy." || echo "Fix errors before deploying."
exit "$ERRORS"
```

## deploy-hooks/post-sync.sh (Migration Hook)

```bash
#!/bin/bash
# deploy-hooks/post-sync.sh - Run after code sync
# Called by deploy.sh with args: <service> <runtime-dir>
set -euo pipefail

SERVICE="$1"
RUNTIME_DIR="$2"

# Run Alembic migrations (only for services with DB)
case "$SERVICE" in
    nero-channel-web)
        echo "  Running database migrations..."
        INFRA_DIR="/srv/nero/nero-infra/src"
        if [ -d "$INFRA_DIR" ] && [ -f "$INFRA_DIR/alembic.ini" ]; then
            cd "$INFRA_DIR"
            /srv/nero/nero-channel-web/.venv/bin/alembic upgrade head
            echo "  Migrations complete"
        fi
        ;;
    *)
        # No migrations for this service
        ;;
esac
```

## Status Check Script

```bash
#!/bin/bash
# status.sh - Check status of all NERO services
# Usage: bash status.sh

echo "=== NERO Platform Status ==="
echo ""

echo "--- systemd Services ---"
for svc in nero-core nero-channel-web nero-channel-tg nero-web nero-watcher; do
    STATUS=$(systemctl --user is-active "$svc" 2>/dev/null || echo "not found")
    case "$STATUS" in
        active)    printf "  %-25s %s\n" "$svc" "ACTIVE" ;;
        inactive)  printf "  %-25s %s\n" "$svc" "INACTIVE" ;;
        failed)    printf "  %-25s %s\n" "$svc" "FAILED" ;;
        *)         printf "  %-25s %s\n" "$svc" "$STATUS" ;;
    esac
done

echo ""
echo "--- Docker Services ---"
if command -v docker &>/dev/null; then
    docker ps --format "  {{.Names}}\t{{.Status}}" 2>/dev/null || echo "  Docker not available"
fi

echo ""
echo "--- Health Checks ---"
for port_name in "8100:nero-channel-web"; do
    PORT="${port_name%%:*}"
    NAME="${port_name##*:}"
    HEALTH=$(curl -sf "http://127.0.0.1:$PORT/health" 2>/dev/null | jq -r '.status' 2>/dev/null || echo "unreachable")
    printf "  %-25s %s (port %s)\n" "$NAME" "$HEALTH" "$PORT"
done

echo ""
echo "--- Resources ---"
echo "  Memory: $(free -h | awk '/^Mem:/{print $3 "/" $2}')"
echo "  Swap:   $(free -h | awk '/^Swap:/{print $3 "/" $2}')"
echo "  Disk:   $(df -h / | awk 'NR==2{print $3 "/" $2 " (" $5 " used)"}')"
echo "  Load:   $(cat /proc/loadavg | awk '{print $1, $2, $3}')"
```
