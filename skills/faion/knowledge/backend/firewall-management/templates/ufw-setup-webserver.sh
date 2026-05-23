#!/usr/bin/env bash
# ufw-setup-webserver.sh — Standard web server + Docker host initial UFW setup
# Run as root or with sudo. Adjust SSH_PORT to match your sshd_config.
set -euo pipefail

SSH_PORT="${SSH_PORT:-22}"

echo "=== UFW Setup: Web Server + Docker ==="

# Default policies
ufw default deny incoming
ufw default allow outgoing
ufw default deny routed

# SSH — MUST be first
ufw limit "${SSH_PORT}/tcp" comment "SSH (rate limited)"

# Web traffic
ufw allow 80/tcp  comment "HTTP"
ufw allow 443/tcp comment "HTTPS"

# Docker internal subnet can reach database ports (if not binding to 127.0.0.1)
# ufw allow from 172.16.0.0/12 to any port 5432 proto tcp comment "PostgreSQL (Docker internal)"
# ufw allow from 172.16.0.0/12 to any port 6379 proto tcp comment "Redis (Docker internal)"

# Logging
ufw logging low

# Enable
ufw --force enable

echo ""
echo "=== UFW Setup Complete ==="
ufw status verbose
