#!/usr/bin/env bash
# health-report.sh — Poll all service /health endpoints and systemd status, print summary table
set -euo pipefail

echo "=============================="
echo "  Health Report"
echo "  $(hostname) — $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

check_http() {
    local name="$1" url="$2"
    status=$(curl -sf --max-time 5 "$url" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','?'))" 2>/dev/null || echo "ERROR")
    code=$(curl -so /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "0")
    echo "  $name — HTTP $code ($status)"
}

check_service() {
    local name="$1"
    state=$(systemctl --user is-active "$name" 2>/dev/null || echo "inactive")
    echo "  $name — $state"
}

echo ""
echo "--- HTTP Health Endpoints ---"
# check_http "nero-channel-web" "http://127.0.0.1:8100/health"

echo ""
echo "--- systemd Services ---"
# check_service "nero-core"
# check_service "nero-channel-web"
# check_service "nero-channel-tg"

echo ""
echo "--- Docker Containers ---"
if command -v docker &>/dev/null; then
    docker ps --format "  {{.Names}} — {{.Status}}" 2>/dev/null || echo "  (Docker not running)"
else
    echo "  (Docker not installed)"
fi
