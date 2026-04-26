# Multi-Project Hosting Templates

## nginx Site Configuration Template

Generic template for adding a new domain to the server.

```nginx
# /etc/nginx/sites-available/DOMAIN.COM
# Enable: sudo ln -s /etc/nginx/sites-available/DOMAIN.COM /etc/nginx/sites-enabled/
# Test:   sudo nginx -t
# Reload: sudo systemctl reload nginx

# HTTP -> HTTPS redirect
server {
    listen 80;
    server_name DOMAIN.COM www.DOMAIN.COM;
    return 301 https://$host$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name DOMAIN.COM www.DOMAIN.COM;

    # SSL certificates (Cloudflare Origin Certificate)
    ssl_certificate /etc/ssl/DOMAIN.COM/cert.pem;
    ssl_certificate_key /etc/ssl/DOMAIN.COM/key.pem;

    # Security headers
    include snippets/security-headers.conf;

    # Logging
    access_log /var/log/nginx/DOMAIN.COM.access.log;
    error_log /var/log/nginx/DOMAIN.COM.error.log;

    # Backend API
    location /api/ {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:PORT_API;
    }

    # WebSocket (if applicable)
    location /ws {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:PORT_API;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

    # Frontend (SPA or SSR)
    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:PORT_FRONTEND;
    }
}
```

## nginx Snippet: Proxy Parameters

```nginx
# /etc/nginx/snippets/proxy-params.conf
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_http_version 1.1;
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
proxy_buffering off;
```

## nginx Snippet: Security Headers

```nginx
# /etc/nginx/snippets/security-headers.conf
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
```

## nginx Snippet: Static File Caching

```nginx
# /etc/nginx/snippets/static-cache.conf
location ~* \.(jpg|jpeg|png|gif|ico|svg|webp)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}

location ~* \.(css|js|woff|woff2|ttf|eot)$ {
    expires 7d;
    add_header Cache-Control "public";
}

location ~* \.(html)$ {
    expires -1;
    add_header Cache-Control "no-store, no-cache, must-revalidate";
}
```

## Port Allocation Registry

```
# /srv/port-registry.txt
# Server Port Allocation Registry
# Last updated: YYYY-MM-DD
#
# Format: PORT    SERVICE              PROJECT      BIND        NOTES
# ============================================================
# Shared Infrastructure (Docker)
# ============================================================
5432    postgresql           shared      127.0.0.1   Docker container
5555    flower               shared      127.0.0.1   Celery monitor, basic auth
5672    rabbitmq-amqp        shared      127.0.0.1   Message broker
6379    redis                shared      127.0.0.1   Cache + Celery backend
15672   rabbitmq-mgmt        shared      127.0.0.1   RabbitMQ admin UI

# ============================================================
# NERO Platform (8100-8199)
# ============================================================
8100    nero-channel-web     nero        127.0.0.1   FastAPI API + WebSocket
8101    nero-web             nero        127.0.0.1   React SPA (serve)

# ============================================================
# MeetingTax (8200-8299)
# ============================================================
# 8200    meetingtax-be       meetingtax  127.0.0.1   FastAPI API
# 8201    meetingtax-fe       meetingtax  127.0.0.1   Next.js frontend

# ============================================================
# EulaGuard (8300-8399)
# ============================================================
# 8300    eulaguard-api       eulaguard   127.0.0.1   FastAPI API

# ============================================================
# Reserved (8400-8599)
# ============================================================
# 8400-8499  (available)
# 8500-8599  (available)
```

## New Project Directory Setup Script

```bash
#!/bin/bash
# setup-project.sh - Set up directories for a new project
# Usage: bash setup-project.sh <project-name> <port-base>
# Example: bash setup-project.sh meetingtax 8200
set -euo pipefail

PROJECT="${1:?Usage: bash setup-project.sh <project-name> <port-base>}"
PORT_BASE="${2:?Provide port base (e.g., 8200)}"

RUNTIME="/srv/${PROJECT}"
SOURCE="$HOME/projects/${PROJECT}"

echo "=== Setting up project: $PROJECT ==="
echo "Runtime: $RUNTIME"
echo "Source:  $SOURCE"
echo "Ports:   ${PORT_BASE} (API), $((PORT_BASE + 1)) (Frontend)"

# Create directories
mkdir -p "$RUNTIME"/{be,fe}
mkdir -p "$SOURCE"

# Create .env
touch "$RUNTIME/.env"
chmod 600 "$RUNTIME/.env"
echo "# ${PROJECT} secrets" > "$RUNTIME/.env"

# Create systemd service files
SERVICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$SERVICE_DIR"

# Backend service
cat > "$SERVICE_DIR/${PROJECT}-be.service" << EOF
[Unit]
Description=${PROJECT} Backend API
After=network.target

[Service]
Type=simple
WorkingDirectory=${RUNTIME}/be/src
EnvironmentFile=${RUNTIME}/.env
ExecStart=${RUNTIME}/be/.venv/bin/uvicorn main:app --host 127.0.0.1 --port ${PORT_BASE}
Restart=on-failure
RestartSec=5
MemoryMax=2G
MemoryHigh=1500M
OOMScoreAdjust=-200

[Install]
WantedBy=default.target
EOF

echo "Created $SERVICE_DIR/${PROJECT}-be.service"

# Reload systemd
systemctl --user daemon-reload

# Update port registry
REGISTRY="/srv/port-registry.txt"
if [ -f "$REGISTRY" ]; then
    echo "${PORT_BASE}    ${PROJECT}-be            ${PROJECT}     127.0.0.1   Backend API" >> "$REGISTRY"
    echo "$((PORT_BASE + 1))    ${PROJECT}-fe            ${PROJECT}     127.0.0.1   Frontend" >> "$REGISTRY"
    echo "Updated port registry"
fi

echo ""
echo "=== Project setup complete ==="
echo "Next steps:"
echo "  1. Add domain DNS record in Cloudflare"
echo "  2. Create nginx site config: /etc/nginx/sites-available/${PROJECT}.com"
echo "  3. Install SSL certificate"
echo "  4. Deploy code and create .venv"
echo "  5. Start services: systemctl --user start ${PROJECT}-be"
```

## systemd Service Template: Backend API

```ini
# ~/.config/systemd/user/PROJECT-be.service
[Unit]
Description=PROJECT Backend API
After=network.target

[Service]
Type=simple
WorkingDirectory=/srv/PROJECT/be/src
EnvironmentFile=/srv/PROJECT/.env

ExecStart=/srv/PROJECT/be/.venv/bin/uvicorn \
    main:app \
    --host 127.0.0.1 \
    --port 8200 \
    --workers 2 \
    --log-level info

Restart=on-failure
RestartSec=5
StartLimitIntervalSec=300
StartLimitBurst=5

MemoryMax=2G
MemoryHigh=1500M
OOMScoreAdjust=-200

[Install]
WantedBy=default.target
```

## systemd Service Template: Frontend (Next.js)

```ini
# ~/.config/systemd/user/PROJECT-fe.service
[Unit]
Description=PROJECT Frontend
After=network.target PROJECT-be.service

[Service]
Type=simple
WorkingDirectory=/srv/PROJECT/fe

ExecStart=/usr/bin/npx serve -s out -l 8201

Restart=on-failure
RestartSec=5

MemoryMax=512M
MemoryHigh=384M
OOMScoreAdjust=100

[Install]
WantedBy=default.target
```

## Shared PostgreSQL: Add Database Script

```bash
#!/bin/bash
# add-database.sh - Create a new database and user in shared PostgreSQL
# Usage: bash add-database.sh <dbname> <username> [password]
set -euo pipefail

DB_NAME="${1:?Usage: bash add-database.sh <dbname> <username> [password]}"
DB_USER="${2:?Provide database username}"
DB_PASS="${3:-$(openssl rand -base64 24)}"

echo "Creating database: $DB_NAME"
echo "Creating user: $DB_USER"

# Connect to PostgreSQL (via Docker)
docker exec -i nero-postgres psql -U postgres << SQL
CREATE DATABASE ${DB_NAME};
CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
ALTER DATABASE ${DB_NAME} OWNER TO ${DB_USER};
SQL

echo ""
echo "Database created successfully!"
echo "Connection URL: postgresql://${DB_USER}:${DB_PASS}@localhost:5432/${DB_NAME}"
echo ""
echo "Add to project .env:"
echo "DATABASE_URL=postgresql://${DB_USER}:${DB_PASS}@localhost:5432/${DB_NAME}"
```

## Resource Planning Spreadsheet Template

```markdown
# Resource Plan: [Server Name]

## Server Specs
- **Provider:** Hetzner CX53
- **CPUs:** 16 vCPU
- **RAM:** 30 GB
- **Disk:** 320 GB SSD
- **Swap:** 4 GB

## Memory Allocation

| Project | Service | MemoryMax | MemoryHigh | Actual (avg) |
|---------|---------|-----------|------------|--------------|
| Shared | PostgreSQL | 8G | 6G | |
| Shared | Redis | 4G | 3G | |
| Shared | RabbitMQ | 2G | 1.5G | |
| NERO | Core (Celery) | 8G | 6G | |
| NERO | Channel-Web | 2G | 1.5G | |
| NERO | Channel-TG | 1G | 768M | |
| NERO | Web (SPA) | 512M | 384M | |
| Project2 | Backend | 2G | 1.5G | |
| Project2 | Frontend | 512M | 384M | |
| OS | Kernel + system | 1G | - | |
| **Total** | | **29G** | | |
| Buffer | Swap | 4G | - | |

## Port Allocation

| Port Range | Project | Status |
|------------|---------|--------|
| 8100-8199 | NERO | Active |
| 8200-8299 | Project2 | Planned |
| 8300-8399 | Project3 | Reserved |
| 8400-8499 | Available | - |
| 8500-8599 | Available | - |

## Disk Usage

| Path | Size | Project |
|------|------|---------|
| /srv/nero/ | | NERO |
| /srv/project2/ | | Project2 |
| /var/lib/docker/ | | Docker volumes |
| /var/log/ | | System logs |
| **Total used** | | |
| **Free** | | |
```
