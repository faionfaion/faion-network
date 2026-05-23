#!/bin/bash
# health-check.sh
# Comprehensive health check for VPS platform
# Exit codes: 0 = all OK, 1 = warnings, 2 = errors
#
# Usage: ./health-check.sh
#        ./health-check.sh || notify-telegram.sh "Health check FAILED"

set -euo pipefail

ERRORS=0
WARNINGS=0

ok()   { echo "OK   $1"; }
warn() { echo "WARN $1"; WARNINGS=$((WARNINGS + 1)); }
fail() { echo "FAIL $1"; ERRORS=$((ERRORS + 1)); }

check_service() {
    local name="$1" cmd="$2"
    if eval "$cmd" > /dev/null 2>&1; then ok "$name"; else fail "$name"; fi
}

echo "=== Health Check: $(date '+%Y-%m-%d %H:%M:%S') ==="

# --- Infrastructure (Docker) ---
echo ""
echo "--- Infrastructure ---"
check_service "Docker" "systemctl is-active docker"
check_service "PostgreSQL" "docker exec nero-postgres pg_isready -U nero -q"
check_service "Redis" "docker exec nero-redis redis-cli ping"
check_service "RabbitMQ" "docker exec nero-rabbitmq rabbitmq-diagnostics -q ping"

# --- Application services ---
echo ""
echo "--- Services ---"
SERVICES=(nero-core nero-channel-web nero-channel-tg nero-web nero-beat nero-autoheal)
for svc in "${SERVICES[@]}"; do
    check_service "$svc" "systemctl --user is-active --quiet $svc"
done

# --- HTTP endpoints ---
echo ""
echo "--- Endpoints ---"
check_service "API /health" "curl -sf --max-time 5 http://127.0.0.1:8100/health"
check_service "Web frontend" "curl -sf --max-time 5 http://127.0.0.1:8101/ -o /dev/null"

# --- System resources ---
echo ""
echo "--- Resources ---"

# Disk
DISK_PCT=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "$DISK_PCT" -gt 90 ]; then fail "Disk: ${DISK_PCT}%"
elif [ "$DISK_PCT" -gt 80 ]; then warn "Disk: ${DISK_PCT}%"
else ok "Disk: ${DISK_PCT}%"; fi

# Memory
MEM_PCT=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_PCT" -gt 95 ]; then fail "Memory: ${MEM_PCT}%"
elif [ "$MEM_PCT" -gt 85 ]; then warn "Memory: ${MEM_PCT}%"
else ok "Memory: ${MEM_PCT}%"; fi

# CPU load
LOAD=$(awk '{print $1}' /proc/loadavg)
CPUS=$(nproc)
LOAD_PCT=$(echo "$LOAD $CPUS" | awk '{printf "%.0f", ($1/$2)*100}')
if [ "$LOAD_PCT" -gt 90 ]; then warn "CPU Load: $LOAD (${LOAD_PCT}%)"
else ok "CPU Load: $LOAD (${LOAD_PCT}%)"; fi

# Swap
SWAP_TOTAL=$(free -m | awk '/Swap:/ {print $2}')
SWAP_USED=$(free -m | awk '/Swap:/ {print $3}')
if [ "$SWAP_TOTAL" -gt 0 ] && [ "$SWAP_USED" -gt $((SWAP_TOTAL / 2)) ]; then
    warn "Swap: ${SWAP_USED}M/${SWAP_TOTAL}M used"
else
    ok "Swap: ${SWAP_USED}M/${SWAP_TOTAL}M"
fi

# --- Summary ---
echo ""
if [ "$ERRORS" -gt 0 ]; then
    echo "RESULT: $ERRORS errors, $WARNINGS warnings"
    exit 2
elif [ "$WARNINGS" -gt 0 ]; then
    echo "RESULT: $WARNINGS warnings"
    exit 1
else
    echo "RESULT: All systems healthy"
    exit 0
fi
