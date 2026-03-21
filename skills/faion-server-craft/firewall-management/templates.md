# Firewall Management Templates

Copy-paste ready UFW configurations for common server setups.

## Template 1: Web Server with Docker (Standard Setup)

```bash
#!/bin/bash
# ufw-setup-webserver.sh — Standard web server + Docker host firewall
# Run as root or with sudo

set -euo pipefail

echo "=== UFW Setup: Web Server + Docker ==="

# Reset UFW (clean slate)
# WARNING: Only run on initial setup, not on production!
# ufw --force reset

# Default policies
ufw default deny incoming
ufw default allow outgoing
ufw default deny routed

# SSH (custom port, rate limited)
ufw limit 2222/tcp comment "SSH"

# Web traffic
ufw allow 80/tcp comment "HTTP"
ufw allow 443/tcp comment "HTTPS"

# Internal Docker subnet access to databases
ufw allow from 172.16.0.0/12 to any port 5432 proto tcp comment "PostgreSQL (Docker internal)"
ufw allow from 172.16.0.0/12 to any port 6379 proto tcp comment "Redis (Docker internal)"
ufw allow from 172.16.0.0/12 to any port 5672 proto tcp comment "RabbitMQ AMQP (Docker internal)"
ufw allow from 172.16.0.0/12 to any port 15672 proto tcp comment "RabbitMQ Mgmt (Docker internal)"

# Enable logging
ufw logging low

# Enable firewall
ufw --force enable

# Show result
ufw status verbose
echo ""
echo "=== UFW Setup Complete ==="
```

## Template 2: Cloudflare-Only Web Server

```bash
#!/bin/bash
# ufw-setup-cloudflare.sh — Restrict HTTP/HTTPS to Cloudflare IPs only
# Prevents direct IP access, all web traffic must go through Cloudflare

set -euo pipefail

echo "=== UFW Setup: Cloudflare-Only Web Server ==="

# Default policies
ufw default deny incoming
ufw default allow outgoing
ufw default deny routed

# SSH
ufw limit 2222/tcp comment "SSH"

# Fetch current Cloudflare IPv4 ranges
echo "Fetching Cloudflare IP ranges..."
CF_IPS=$(curl -s https://www.cloudflare.com/ips-v4)

for ip in $CF_IPS; do
    ufw allow from "$ip" to any port 80 proto tcp comment "Cloudflare IPv4"
    ufw allow from "$ip" to any port 443 proto tcp comment "Cloudflare IPv4"
done

# Cloudflare IPv6 ranges
CF_IPS6=$(curl -s https://www.cloudflare.com/ips-v6)
for ip in $CF_IPS6; do
    ufw allow from "$ip" to any port 80 proto tcp comment "Cloudflare IPv6"
    ufw allow from "$ip" to any port 443 proto tcp comment "Cloudflare IPv6"
done

# Internal Docker subnet
ufw allow from 172.16.0.0/12 to any port 5432 proto tcp comment "PostgreSQL (Docker)"
ufw allow from 172.16.0.0/12 to any port 6379 proto tcp comment "Redis (Docker)"

# Enable
ufw logging low
ufw --force enable

ufw status numbered
echo ""
echo "=== Cloudflare-only rules applied ==="
echo "NOTE: Update these rules when Cloudflare adds new IP ranges."
echo "Automate with a monthly cron job."
```

## Template 3: VPN Server (WireGuard + Web)

```bash
#!/bin/bash
# ufw-setup-vpn.sh — Web server with WireGuard VPN

set -euo pipefail

# Default policies
ufw default deny incoming
ufw default allow outgoing
ufw default allow routed    # IMPORTANT: Allow forwarding for VPN

# SSH
ufw limit 2222/tcp comment "SSH"

# Web
ufw allow 80/tcp comment "HTTP"
ufw allow 443/tcp comment "HTTPS"

# WireGuard
ufw allow 51820/udp comment "WireGuard VPN"

# Allow VPN clients to access internal services
ufw allow from 10.0.0.0/24 to any comment "VPN clients"

# NAT for VPN (add to /etc/ufw/before.rules)
echo ""
echo "Add the following to /etc/ufw/before.rules BEFORE *filter:"
echo ""
cat << 'NATRULES'
# NAT for WireGuard VPN
*nat
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s 10.0.0.0/24 -o eth0 -j MASQUERADE
COMMIT
NATRULES

# IP forwarding (add to /etc/ufw/sysctl.conf)
echo ""
echo "Also set in /etc/ufw/sysctl.conf:"
echo "net/ipv4/ip_forward=1"

ufw logging low
ufw --force enable
ufw status verbose
```

## Template 4: Docker-Compose Port Binding (Secure)

```yaml
# docker-compose.yml — Secure port bindings
# All services bind to 127.0.0.1 (localhost only)
# nginx handles external traffic

services:
  postgres:
    image: postgres:16
    ports:
      - "127.0.0.1:5432:5432"    # Localhost only
    networks:
      - internal

  redis:
    image: redis:7-alpine
    ports:
      - "127.0.0.1:6379:6379"    # Localhost only
    networks:
      - internal

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "127.0.0.1:5672:5672"    # AMQP — localhost only
      - "127.0.0.1:15672:15672"  # Management UI — localhost only
    networks:
      - internal

  flower:
    image: mher/flower
    ports:
      - "127.0.0.1:5555:5555"    # Flower UI — localhost only
    networks:
      - internal

networks:
  internal:
    driver: bridge
    # No need to expose this network externally
```

## Template 5: UFW Application Profile

File: `/etc/ufw/applications.d/nero-platform`

```ini
[NERO-Web]
title=NERO Web Channel
description=FastAPI HTTP/WebSocket gateway
ports=8100/tcp

[NERO-Frontend]
title=NERO React SPA
description=React SPA static file server
ports=8101/tcp

[NERO-Full]
title=NERO Full Platform
description=All NERO platform ports
ports=8100,8101/tcp
```

Usage:
```bash
# Allow using application profile
sudo ufw allow from 127.0.0.1 to any app NERO-Full

# List available apps
sudo ufw app list

# Show app info
sudo ufw app info NERO-Full
```

## Template 6: Firewall Status Report Script

```bash
#!/bin/bash
# ufw-report.sh — Generate firewall status report

set -euo pipefail

echo "=============================="
echo "  Firewall Status Report"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================="
echo ""

echo "--- UFW Status ---"
sudo ufw status verbose
echo ""

echo "--- Rules (Numbered) ---"
sudo ufw status numbered
echo ""

echo "--- Listening Ports ---"
sudo ss -tlnp | column -t
echo ""

echo "--- Docker Port Mappings ---"
if command -v docker &>/dev/null; then
    docker ps --format "table {{.Names}}\t{{.Ports}}" 2>/dev/null || echo "(Docker not running)"
else
    echo "(Docker not installed)"
fi
echo ""

echo "--- Exposed Ports (0.0.0.0) ---"
echo "These ports are accessible from the internet:"
sudo ss -tlnp | grep '0.0.0.0' | awk '{print $4, $6}' | column -t
echo ""

echo "--- Recent Blocks (last 1h) ---"
sudo journalctl -k --since "1 hour ago" --no-pager 2>/dev/null | grep -c "UFW BLOCK" || echo "0"
echo " blocked connections"
echo ""

echo "--- Top Blocked IPs (last 24h) ---"
sudo journalctl -k --since "24 hours ago" --no-pager 2>/dev/null | \
    grep "UFW BLOCK" | \
    grep -oP 'SRC=\K[^ ]+' | \
    sort | uniq -c | sort -rn | head -10 || echo "(no blocks)"
```

## Template 7: Cron Job for Cloudflare IP Updates

```bash
#!/bin/bash
# /usr/local/bin/update-cloudflare-ufw.sh
# Run monthly: 0 3 1 * * /usr/local/bin/update-cloudflare-ufw.sh

set -euo pipefail

LOG="/var/log/cloudflare-ufw-update.log"
exec >> "$LOG" 2>&1
echo "=== $(date) ==="

# Remove old Cloudflare rules
ufw status numbered | grep "Cloudflare" | awk -F'[][]' '{print $2}' | sort -rn | while read num; do
    ufw --force delete "$num"
done

# Add current Cloudflare IPv4 ranges
for ip in $(curl -s https://www.cloudflare.com/ips-v4); do
    ufw allow from "$ip" to any port 80,443 proto tcp comment "Cloudflare"
done

# Add current Cloudflare IPv6 ranges
for ip in $(curl -s https://www.cloudflare.com/ips-v6); do
    ufw allow from "$ip" to any port 80,443 proto tcp comment "Cloudflare"
done

echo "Updated $(date)"
ufw status numbered | grep -c "Cloudflare"
echo " Cloudflare rules active"
```
