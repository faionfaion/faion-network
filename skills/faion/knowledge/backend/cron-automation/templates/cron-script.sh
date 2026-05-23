#!/bin/bash
# script-name.sh
# Description: What this script does
# Schedule: 0 3 * * * (daily at 3 AM)
# Log: /var/log/nero-scriptname.log

set -euo pipefail

# === Configuration ===
SCRIPT_NAME="$(basename "$0" .sh)"
LOG_FILE="/var/log/nero-${SCRIPT_NAME}.log"
LOCK_FILE="/tmp/${SCRIPT_NAME}.lock"

# === Logging ===
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$SCRIPT_NAME] $1" >> "$LOG_FILE"
}

# === Locking (prevent overlapping runs) ===
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
    log "ERROR: Another instance is already running, exiting"
    exit 1
fi

# === Error handling ===
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log "ERROR: Failed with exit code $exit_code"
        # Uncomment for Telegram alerts:
        # /usr/local/bin/notify-telegram.sh "CRON FAIL: $SCRIPT_NAME (exit $exit_code)" 2>/dev/null || true
    fi
}
trap cleanup EXIT

# === Load environment ===
if [ -f "$HOME/workspace/.env" ]; then
    set -a
    source "$HOME/workspace/.env"
    set +a
fi

# === Main logic ===
log "Starting..."

# Your code here

log "Completed successfully"
