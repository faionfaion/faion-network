# Multi-Project Hosting Examples

## Example 1: NERO Server Hosting 3 Projects

The Hetzner CX53 server hosts multiple projects on different domains, sharing PostgreSQL and Redis.

### Port Allocation

```
# /srv/port-registry.txt
PORT    SERVICE              PROJECT      BIND        NOTES
5432    postgresql           shared       127.0.0.1   Docker, shared by all projects
5555    flower               shared       127.0.0.1   Celery monitor
5672    rabbitmq-amqp        shared       127.0.0.1   Message broker
6379    redis                shared       127.0.0.1   Cache
8100    nero-channel-web     nero         127.0.0.1   FastAPI API + WebSocket
8101    nero-web             nero         127.0.0.1   React SPA
8200    meetingtax-be        meetingtax   127.0.0.1   FastAPI API
8201    meetingtax-fe        meetingtax   127.0.0.1   Next.js frontend
8300    eulaguard-api        eulaguard    127.0.0.1   FastAPI API
15672   rabbitmq-mgmt        shared       127.0.0.1   RabbitMQ admin
```

### nginx Configuration: nero.faion.net

```nginx
# /etc/nginx/sites-available/nero.faion.net
server {
    listen 80;
    server_name nero.faion.net;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name nero.faion.net;

    ssl_certificate /etc/ssl/nero.faion.net/cert.pem;
    ssl_certificate_key /etc/ssl/nero.faion.net/key.pem;

    include snippets/security-headers.conf;

    access_log /var/log/nginx/nero.faion.net.access.log;
    error_log /var/log/nginx/nero.faion.net.error.log;

    location /api/ {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8100;
    }

    location /ws {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8100;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8101;
    }
}
```

### nginx Configuration: meetingtax.io

```nginx
# /etc/nginx/sites-available/meetingtax.io
server {
    listen 80;
    server_name meetingtax.io www.meetingtax.io;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name meetingtax.io www.meetingtax.io;

    ssl_certificate /etc/ssl/meetingtax.io/cert.pem;
    ssl_certificate_key /etc/ssl/meetingtax.io/key.pem;

    include snippets/security-headers.conf;

    access_log /var/log/nginx/meetingtax.io.access.log;
    error_log /var/log/nginx/meetingtax.io.error.log;

    # API
    location /api/ {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8200;
    }

    # Next.js frontend (SSR)
    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8201;
    }
}
```

### Shared PostgreSQL: Multiple Databases

```bash
# Create databases for each project
$ docker exec -i nero-postgres psql -U postgres << SQL
CREATE DATABASE nero;
CREATE DATABASE meetingtax;
CREATE DATABASE eulaguard;

CREATE USER nero_user WITH PASSWORD 'nero_db_password';
CREATE USER mtax_user WITH PASSWORD 'mtax_db_password';
CREATE USER eula_user WITH PASSWORD 'eula_db_password';

GRANT ALL PRIVILEGES ON DATABASE nero TO nero_user;
GRANT ALL PRIVILEGES ON DATABASE meetingtax TO mtax_user;
GRANT ALL PRIVILEGES ON DATABASE eulaguard TO eula_user;

ALTER DATABASE nero OWNER TO nero_user;
ALTER DATABASE meetingtax OWNER TO mtax_user;
ALTER DATABASE eulaguard OWNER TO eula_user;
SQL

# Each project's .env has its own DATABASE_URL
# ~/workspace/.env (NERO):     DATABASE_URL=postgresql://nero_user:pass@localhost:5432/nero
# /srv/meetingtax/.env:         DATABASE_URL=postgresql://mtax_user:pass@localhost:5432/meetingtax
# /srv/eulaguard/.env:          DATABASE_URL=postgresql://eula_user:pass@localhost:5432/eulaguard
```

### Shared Redis: Database Isolation

```bash
# Redis databases 0-15 are pre-allocated
# DB 0: NERO (default)
# DB 1: NERO Celery backend
# DB 2: MeetingTax sessions
# DB 3: MeetingTax cache
# DB 4: EulaGuard

# NERO .env:      REDIS_URL=redis://localhost:6379/0
# MeetingTax .env: REDIS_URL=redis://localhost:6379/2
# EulaGuard .env:  REDIS_URL=redis://localhost:6379/4
```

## Example 2: Adding a New Project (EulaGuard)

Step-by-step process for adding the EulaGuard project to the existing server.

### 1. Planning

```
Project: EulaGuard
Domain: eulaguard.com
Port: 8300 (API)
Database: eulaguard (shared PostgreSQL)
Redis: DB 4
Source: ~/projects/eulaguard/
Runtime: /srv/eulaguard/
Memory budget: 2GB (API only, no frontend)
```

### 2. Directory Setup

```bash
# Source
mkdir -p ~/projects/eulaguard

# Runtime
mkdir -p /srv/eulaguard/{api,.venv}
touch /srv/eulaguard/.env && chmod 600 /srv/eulaguard/.env
```

### 3. Create Database

```bash
$ docker exec -i nero-postgres psql -U postgres << SQL
CREATE DATABASE eulaguard;
CREATE USER eula_user WITH PASSWORD '$(openssl rand -base64 24)';
GRANT ALL PRIVILEGES ON DATABASE eulaguard TO eula_user;
ALTER DATABASE eulaguard OWNER TO eula_user;
SQL
```

### 4. Create systemd Service

```bash
$ cat > ~/.config/systemd/user/eulaguard-api.service << 'EOF'
[Unit]
Description=EulaGuard API
After=network.target

[Service]
Type=simple
WorkingDirectory=/srv/eulaguard/api/src
EnvironmentFile=/srv/eulaguard/.env
ExecStart=/srv/eulaguard/api/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8300
Restart=on-failure
RestartSec=5
MemoryMax=2G
MemoryHigh=1500M
OOMScoreAdjust=-200

[Install]
WantedBy=default.target
EOF

$ systemctl --user daemon-reload
$ systemctl --user enable eulaguard-api
```

### 5. Configure nginx

```bash
# Create Origin Certificate in Cloudflare dashboard
$ sudo mkdir -p /etc/ssl/eulaguard.com
$ sudo nano /etc/ssl/eulaguard.com/cert.pem   # Paste cert
$ sudo nano /etc/ssl/eulaguard.com/key.pem    # Paste key
$ sudo chmod 600 /etc/ssl/eulaguard.com/key.pem

# Create nginx config
$ sudo nano /etc/nginx/sites-available/eulaguard.com
# (paste site config with proxy_pass to 127.0.0.1:8300)

$ sudo ln -s /etc/nginx/sites-available/eulaguard.com /etc/nginx/sites-enabled/
$ sudo nginx -t
nginx: configuration file /etc/nginx/nginx.conf test is successful
$ sudo systemctl reload nginx
```

### 6. Cloudflare DNS

```
Type: A
Name: eulaguard.com
Content: 203.0.113.50 (server IP)
Proxy: Proxied (orange cloud)
SSL Mode: Full (Strict)
```

### 7. Deploy and Verify

```bash
# Deploy code
$ cd ~/projects/eulaguard
# ... git clone, setup code ...
$ bash deploy-eulaguard.sh

# Start service
$ systemctl --user start eulaguard-api

# Verify
$ systemctl --user status eulaguard-api
  Active: active (running)

$ curl http://127.0.0.1:8300/health
{"status": "ok"}

$ curl https://eulaguard.com/api/health
{"status": "ok"}
```

### 8. Update Port Registry

```bash
$ echo "8300    eulaguard-api        eulaguard    127.0.0.1   FastAPI API" >> /srv/port-registry.txt
```

## Example 3: Resource Monitoring Across Projects

Checking resource usage across all hosted projects.

```bash
$ cat ~/workspace/scripts/resource-report.sh
#!/bin/bash
echo "=== Resource Report: $(date) ==="
echo ""

echo "--- Memory by Project ---"
echo "NERO:"
for svc in nero-core nero-channel-web nero-channel-tg nero-web; do
    MEM=$(systemctl --user show $svc -p MemoryCurrent 2>/dev/null | cut -d= -f2)
    if [ -n "$MEM" ] && [ "$MEM" != "[not set]" ]; then
        echo "  $svc: $((MEM / 1048576))MB"
    fi
done

echo "MeetingTax:"
for svc in meetingtax-be meetingtax-fe; do
    MEM=$(systemctl --user show $svc -p MemoryCurrent 2>/dev/null | cut -d= -f2)
    if [ -n "$MEM" ] && [ "$MEM" != "[not set]" ]; then
        echo "  $svc: $((MEM / 1048576))MB"
    fi
done

echo "EulaGuard:"
for svc in eulaguard-api; do
    MEM=$(systemctl --user show $svc -p MemoryCurrent 2>/dev/null | cut -d= -f2)
    if [ -n "$MEM" ] && [ "$MEM" != "[not set]" ]; then
        echo "  $svc: $((MEM / 1048576))MB"
    fi
done

echo ""
echo "--- Docker ---"
docker stats --no-stream --format "  {{.Name}}: {{.MemUsage}}"

echo ""
echo "--- Total ---"
free -h | head -3

echo ""
echo "--- Disk ---"
echo "  /srv/nero/: $(du -sh /srv/nero/ 2>/dev/null | cut -f1)"
echo "  /srv/meetingtax/: $(du -sh /srv/meetingtax/ 2>/dev/null | cut -f1)"
echo "  /srv/eulaguard/: $(du -sh /srv/eulaguard/ 2>/dev/null | cut -f1)"
echo "  Docker volumes: $(docker system df --format '{{.Size}}' 2>/dev/null | head -1)"
```

### Sample Output

```
=== Resource Report: 2026-03-21 ===

--- Memory by Project ---
NERO:
  nero-core: 2148MB
  nero-channel-web: 342MB
  nero-channel-tg: 128MB
  nero-web: 52MB
MeetingTax:
  meetingtax-be: 285MB
  meetingtax-fe: 180MB
EulaGuard:
  eulaguard-api: 156MB

--- Docker ---
  nero-postgres: 1.8GiB / 30GiB
  nero-redis: 512MiB / 30GiB
  nero-rabbitmq: 210MiB / 30GiB
  nero-flower: 85MiB / 30GiB

--- Total ---
               total        used        free      shared  buff/cache   available
Mem:            30Gi       8.2Gi        18Gi       128Mi       3.8Gi        21Gi

--- Disk ---
  /srv/nero/: 2.1G
  /srv/meetingtax/: 850M
  /srv/eulaguard/: 320M
  Docker volumes: 4.5GB
```
