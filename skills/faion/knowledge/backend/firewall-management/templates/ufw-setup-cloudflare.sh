#!/usr/bin/env bash
# ufw-setup-cloudflare.sh — Restrict HTTP/HTTPS to Cloudflare IPs only
# Prevents direct IP access; all web traffic must route through Cloudflare proxy.
set -euo pipefail

SSH_PORT="${SSH_PORT:-22}"

echo "=== UFW Setup: Cloudflare-Only Web Server ==="

ufw default deny incoming
ufw default allow outgoing
ufw default deny routed

ufw limit "${SSH_PORT}/tcp" comment "SSH"

echo "Fetching Cloudflare IPv4 ranges..."
for ip in $(curl -sf https://www.cloudflare.com/ips-v4); do
    ufw allow from "$ip" to any port 80,443 proto tcp comment "Cloudflare"
done

echo "Fetching Cloudflare IPv6 ranges..."
for ip in $(curl -sf https://www.cloudflare.com/ips-v6); do
    ufw allow from "$ip" to any port 80,443 proto tcp comment "Cloudflare"
done

ufw logging low
ufw --force enable

echo ""
echo "=== Cloudflare-only rules applied ==="
ufw status numbered
echo ""
echo "Automate updates: add update-cloudflare-ufw.sh to monthly cron."
