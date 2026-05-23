#!/usr/bin/env bash
# deploy.sh — Master deploy script: rsync + venv + systemd restart
# Usage: ./deploy.sh [service|all] [--rebuild-venv]
set -euo pipefail

WORKSPACE=~/workspace/repos
RUNTIME=/srv/nero
DEPLOY_ORDER=(nero-sdk nero-infra nero-core nero-channel-web nero-channel-tg nero-web)

REBUILD_VENV=false
TARGET="${1:-all}"
shift || true
for arg in "$@"; do
    [[ "$arg" == "--rebuild-venv" ]] && REBUILD_VENV=true
done

deploy_service() {
    local svc="$1"
    local src="$WORKSPACE/$svc"
    local dst="$RUNTIME/$svc"

    if [[ ! -d "$src" ]]; then
        echo "[SKIP] $svc — workspace dir not found: $src"
        return 0
    fi

    echo "[DEPLOY] $svc"

    # Sync source files
    rsync -a --delete \
        --exclude='.git/' \
        --exclude='__pycache__/' \
        --exclude='.pytest_cache/' \
        --exclude='*.pyc' \
        --exclude='.venv/' \
        --exclude='.env' \
        --exclude='node_modules/' \
        "$src/" "$dst/src/"

    # Link env file if not already linked
    if [[ ! -L "$dst/.env" ]]; then
        ln -sf ~/workspace/.env "$dst/.env"
    fi

    # Install/update pip dependencies only if requirements changed
    if [[ -f "$dst/src/requirements.txt" ]]; then
        if [[ "$REBUILD_VENV" == "true" ]] || \
           ! diff -q "$dst/src/requirements.txt" "$dst/.last-requirements.txt" &>/dev/null 2>&1; then
            echo "  Installing requirements..."
            if [[ ! -d "$dst/.venv" ]] || [[ "$REBUILD_VENV" == "true" ]]; then
                python3 -m venv "$dst/.venv"
            fi
            "$dst/.venv/bin/pip" install -q -r "$dst/src/requirements.txt"
            cp "$dst/src/requirements.txt" "$dst/.last-requirements.txt"
        fi
    fi

    # Restart systemd user service
    local unit="${svc}.service"
    if systemctl --user is-enabled "$unit" &>/dev/null; then
        systemctl --user restart "$unit"
        echo "  Restarted $unit"
    else
        echo "  [WARN] Service $unit not enabled, skipping restart"
    fi
}

if [[ "$TARGET" == "all" ]]; then
    for svc in "${DEPLOY_ORDER[@]}"; do
        deploy_service "$svc"
    done
else
    deploy_service "$TARGET"
fi

echo "[DONE]"
