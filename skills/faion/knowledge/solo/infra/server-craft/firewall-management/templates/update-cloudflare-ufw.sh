#!/usr/bin/env bash
# update-cloudflare-ufw.sh — Refresh Cloudflare IP ranges in UFW
# Run monthly via cron: 0 3 1 * * /usr/local/bin/update-cloudflare-ufw.sh
set -euo pipefail

LOG="/var/log/cloudflare-ufw-update.log"
exec >> "$LOG" 2>&1
echo "=== $(date) ==="

# Remove old Cloudflare rules by deleting rules with "Cloudflare" comment
# ufw doesn't support delete by comment directly; use numbered delete
ufw status numbered | grep -i "Cloudflare" | awk -F'[][]' '{print $2}' | sort -rn | \
    while read -r num; do
        ufw --force delete "$num"
    done

echo "Old rules removed."

# Add current Cloudflare IPv4 ranges
for ip in $(curl -sf https://www.cloudflare.com/ips-v4); do
    ufw allow from "$ip" to any port 80,443 proto tcp comment "Cloudflare"
done

# Add current Cloudflare IPv6 ranges
for ip in $(curl -sf https://www.cloudflare.com/ips-v6); do
    ufw allow from "$ip" to any port 80,443 proto tcp comment "Cloudflare"
done

count=$(ufw status numbered | grep -c "Cloudflare" || true)
echo "Updated: $count Cloudflare rules active"
