#!/usr/bin/env bash
# deploy.sh — Deploy orchestrator: rsync + venv + systemd restart
# Usage: bash deploy.sh <service|all> [--rebuild-venv]
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/workspace/repos}"
RUNTIME="${RUNTIME:-/srv/nero}"
ENV_FILE="${ENV_FILE:-$HOME/workspace/.env}"
REBUILD_VENV=false

TARGET="${1:?Usage: deploy.sh <service|all> [--rebuild-venv]}"
shift || true
[[ "${1:-}" == "--rebuild-venv" ]] && REBUILD_VENV=true

# Service registry: name → type (systemd|library|static|docker)
declare -A SERVICES=(
    [nero-sdk]="library"
    [nero-infra]="docker"
    [nero-core]="systemd"
    [nero-channel-web]="systemd"
    [nero-channel-tg]="systemd"
    [nero-web]="static"
)
HEALTH_PORTS=([nero-channel-web]=8100)
DEPLOY_ORDER=(nero-sdk nero-infra nero-core nero-channel-web nero-channel-tg nero-web)

# ── Pre-deploy checks ─────────────────────────────────────────────────────────
pre_deploy_check() {
    local errors=0
    [[ ! -f "$ENV_FILE" ]] && echo "ERROR: $ENV_FILE not found" && ((errors++)) || true
    local free_mb; free_mb=$(df /srv --output=avail -BM | tail -1 | tr -d ' M')
    [[ "$free_mb" -lt 1024 ]] && echo "ERROR: Low disk: ${free_mb}MB free" && ((errors++)) || true
    systemctl --user status >/dev/null 2>&1 || { echo "ERROR: no systemd user session"; ((errors++)); }
    [[ $errors -gt 0 ]] && { echo "Pre-deploy failed ($errors errors)"; exit 1; }
    echo "Pre-deploy checks passed"
}

# ── rsync ─────────────────────────────────────────────────────────────────────
sync_code() {
    local svc="$1" dst_dir="$2"
    rsync -a --delete \
        --exclude='.git/' --exclude='__pycache__/' --exclude='.pytest_cache/' \
        --exclude='*.pyc' --exclude='.venv/' --exclude='.env' --exclude='node_modules/' \
        "$WORKSPACE/$svc/" "$dst_dir/src/"
}

# ── Virtualenv management ─────────────────────────────────────────────────────
setup_venv() {
    local svc_dir="$1"
    local venv="$svc_dir/.venv"
    if [[ "$REBUILD_VENV" == "true" ]] || [[ ! -d "$venv" ]]; then
        echo "  Creating venv..."
        rm -rf "$venv"
        python3 -m venv "$venv"
    fi
    local req="$svc_dir/src/requirements.txt"
    local stamp="$svc_dir/.last-requirements.txt"
    if [[ -f "$req" ]] && ! diff -q "$req" "$stamp" &>/dev/null 2>&1; then
        echo "  Installing requirements..."
        "$venv/bin/pip" install -q -r "$req"
        cp "$req" "$stamp"
    fi
    [[ -f "$svc_dir/src/pyproject.toml" ]] && "$venv/bin/pip" install -q -e "$svc_dir/src/" || true
    ln -sf "$ENV_FILE" "$svc_dir/.env" 2>/dev/null || true
}

# ── Hooks ─────────────────────────────────────────────────────────────────────
run_hook() {
    local svc="$1" hook="$2"
    local file="$WORKSPACE/$svc/deploy-hooks/${hook}.sh"
    if [[ -f "$file" ]]; then
        echo "  [hook] $hook"
        bash "$file" "$svc" "$RUNTIME/$svc"
    fi
}

# ── Restart + validate ────────────────────────────────────────────────────────
restart_and_check() {
    local unit="${1}.service" port="${2:-}"
    systemctl --user restart "$unit"
    local waited=0
    while [[ $waited -lt 30 ]]; do
        systemctl --user is-active "$unit" &>/dev/null && break
        sleep 1; ((waited++))
    done
    systemctl --user is-active "$unit" &>/dev/null || {
        echo "  ERROR: $unit failed to start"
        systemctl --user status "$unit" --no-pager
        return 1
    }
    if [[ -n "$port" ]]; then
        curl -sf "http://127.0.0.1:${port}/health" >/dev/null 2>&1 || echo "  WARN: health check on port $port failed"
    fi
    echo "  Restarted $unit: OK"
}

# ── Per-type deploy functions ─────────────────────────────────────────────────
deploy_library() {
    local svc="$1"
    sync_code "$svc" "$RUNTIME/$svc"
    echo "  library synced (no restart)"
}

deploy_docker() {
    local svc="$1"
    sync_code "$svc" "$RUNTIME/$svc"
    docker compose -f "$RUNTIME/$svc/src/docker-compose.yml" up -d --remove-orphans
}

deploy_systemd() {
    local svc="$1"
    local svc_dir="$RUNTIME/$svc"
    local port="${HEALTH_PORTS[$svc]:-}"
    sync_code "$svc" "$svc_dir"
    run_hook "$svc" "post-sync"
    setup_venv "$svc_dir"
    run_hook "$svc" "pre-restart"
    restart_and_check "$svc" "$port"
    run_hook "$svc" "post-restart"
}

deploy_static() {
    local svc="$1"
    rsync -a --delete "$WORKSPACE/$svc/dist/" "$RUNTIME/$svc/dist/"
    local unit="${svc}.service"
    systemctl --user is-enabled "$unit" &>/dev/null && systemctl --user restart "$unit" && echo "  Restarted $unit" || echo "  static files synced (no service)"
}

# ── Dispatch ──────────────────────────────────────────────────────────────────
deploy_one() {
    local svc="$1"
    local type="${SERVICES[$svc]:-}"
    [[ -z "$type" ]] && { echo "[SKIP] $svc — not in service registry"; return 0; }
    echo "[DEPLOY] $svc"
    case "$type" in
        library) deploy_library "$svc" ;;
        docker)  deploy_docker  "$svc" ;;
        systemd) deploy_systemd "$svc" ;;
        static)  deploy_static  "$svc" ;;
    esac
}

pre_deploy_check

if [[ "$TARGET" == "all" ]]; then
    for svc in "${DEPLOY_ORDER[@]}"; do deploy_one "$svc"; done
else
    deploy_one "$TARGET"
fi

echo "[DONE]"
