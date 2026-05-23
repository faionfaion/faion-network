#!/bin/bash
# setup-project.sh — Create runtime directories, .env, systemd service, update port registry
#
# Usage: bash setup-project.sh <project-name> <port-base>
# Example: bash setup-project.sh meetingtax 8200

set -euo pipefail

PROJECT="${1:?Usage: bash setup-project.sh <project-name> <port-base>}"
PORT_BASE="${2:?Provide port base (e.g., 8200)}"
PORT_API="$PORT_BASE"
PORT_FE="$((PORT_BASE + 1))"

RUNTIME="/srv/${PROJECT}"
SERVICE_DIR="$HOME/.config/systemd/user"
REGISTRY="/srv/port-registry.txt"

echo "=== Setting up project: $PROJECT ==="
echo "Runtime: $RUNTIME"
echo "Ports:   ${PORT_API} (API), ${PORT_FE} (Frontend)"

# Runtime directories
mkdir -p "${RUNTIME}"/{be,fe}
echo "  Created $RUNTIME/{be,fe}"

# .env file
touch "${RUNTIME}/.env"
chmod 600 "${RUNTIME}/.env"
cat > "${RUNTIME}/.env" << EOF
# ${PROJECT} secrets — chmod 600, never commit
DATABASE_URL=postgresql://${PROJECT}_user:CHANGEME@localhost:5432/${PROJECT}
REDIS_URL=redis://localhost:6379/0
EOF
echo "  Created ${RUNTIME}/.env (chmod 600)"

# systemd service: backend API
mkdir -p "$SERVICE_DIR"
cat > "${SERVICE_DIR}/${PROJECT}-be.service" << EOF
[Unit]
Description=${PROJECT} Backend API
After=network.target

[Service]
Type=simple
WorkingDirectory=${RUNTIME}/be/src
EnvironmentFile=${RUNTIME}/.env
ExecStart=${RUNTIME}/be/.venv/bin/uvicorn main:app --host 127.0.0.1 --port ${PORT_API}
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=300
StartLimitBurst=5
MemoryMax=2G
MemoryHigh=1500M

[Install]
WantedBy=default.target
EOF
echo "  Created ${SERVICE_DIR}/${PROJECT}-be.service"

systemctl --user daemon-reload
echo "  Reloaded systemd user daemon"

# Update port registry
if [ -f "$REGISTRY" ]; then
    echo "${PORT_API}    ${PROJECT}-be            ${PROJECT}    127.0.0.1   Backend API" >> "$REGISTRY"
    echo "${PORT_FE}    ${PROJECT}-fe            ${PROJECT}    127.0.0.1   Frontend" >> "$REGISTRY"
    echo "  Updated $REGISTRY"
fi

echo ""
echo "=== Setup complete ==="
echo "Next steps:"
echo "  1. Add DNS record in Cloudflare for your domain"
echo "  2. Create /etc/nginx/sites-available/yourdomain.com using templates/nginx-site.conf"
echo "  3. Install Cloudflare origin certificate to /etc/ssl/yourdomain.com/"
echo "  4. sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/"
echo "  5. sudo nginx -t && sudo systemctl reload nginx"
echo "  6. Deploy code to $RUNTIME/be/ and create .venv"
echo "  7. Fill in $RUNTIME/.env with real credentials"
echo "  8. systemctl --user enable --now ${PROJECT}-be"
