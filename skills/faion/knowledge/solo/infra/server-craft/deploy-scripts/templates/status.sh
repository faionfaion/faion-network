#!/usr/bin/env bash
# status.sh — Show all service status, Docker containers, health endpoints, resources
set -euo pipefail

SYSTEMD_SERVICES=(nero-core nero-channel-web nero-channel-tg nero-web nero-watcher)
HEALTH_CHECKS=([nero-channel-web]="http://127.0.0.1:8100/health")

echo "=== NERO Platform Status ==="
echo ""

echo "--- systemd Services ---"
for svc in "${SYSTEMD_SERVICES[@]}"; do
    unit="${svc}.service"
    if systemctl --user is-enabled "$unit" &>/dev/null; then
        state=$(systemctl --user is-active "$unit" 2>/dev/null || echo "inactive")
        printf "  %-30s %s\n" "$svc" "${state^^}"
    fi
done

echo ""
echo "--- Docker Containers ---"
if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
    docker ps --format "  {{.Names}}\t{{.Status}}" 2>/dev/null || echo "  (no containers)"
else
    echo "  (docker not available)"
fi

echo ""
echo "--- Health Checks ---"
for svc in "${!HEALTH_CHECKS[@]}"; do
    url="${HEALTH_CHECKS[$svc]}"
    if curl -sf "$url" >/dev/null 2>&1; then
        printf "  %-30s ok\n" "$svc"
    else
        printf "  %-30s FAIL (%s)\n" "$svc" "$url"
    fi
done

echo ""
echo "--- Resources ---"
mem=$(free -h | awk '/^Mem:/{printf "%s/%s", $3, $2}')
swap=$(free -h | awk '/^Swap:/{printf "%s/%s", $3, $2}')
disk=$(df /srv -h --output=used,size,pcent | tail -1 | awk '{printf "%s/%s (%s)", $1, $2, $3}')
load=$(uptime | awk -F'load average:' '{print $2}' | xargs)
printf "  Memory: %s   Swap: %s\n" "$mem" "$swap"
printf "  Disk:   %s  Load: %s\n" "$disk" "$load"
