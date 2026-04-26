# Multi-Project Hosting

## Overview

Strategies for hosting multiple web projects on a single VPS. Covers multi-domain nginx configuration, port allocation conventions, Docker isolation per project, shared backing services (PostgreSQL, Redis), Cloudflare DNS integration, directory structure conventions, and resource planning. Designed for solo developers running 2-5 projects on a single Hetzner VPS.

**Target:** Ubuntu 24.04 VPS (Hetzner CX53, 16 CPUs, 30GB RAM) hosting multiple domains.

## When to Use

| Scenario | Fit |
|----------|-----|
| Adding a second project to an existing VPS | Essential |
| Planning port allocation across services | Essential |
| Configuring nginx for multiple domains | Essential |
| Deciding shared vs isolated databases | Recommended |
| Planning resource allocation | Recommended |
| Evaluating when to split to a second server | Good |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Port allocation** | Convention for assigning ports to avoid conflicts |
| **Reverse proxy** | nginx routes domain/path to backend port |
| **Shared services** | Single PostgreSQL/Redis instance used by multiple projects |
| **Isolated services** | Per-project Docker Compose stacks with own databases |
| **Server block** | nginx config block for a specific domain |
| **Cloudflare proxy** | DNS + CDN + SSL termination in front of origin |

## Port Allocation Strategy

### Convention: Project-Based Port Ranges

Allocate port ranges to avoid conflicts. Reserve 100 ports per project.

| Range | Project | Services |
|-------|---------|----------|
| 5432 | Shared | PostgreSQL (Docker) |
| 5555 | Shared | Flower (Celery monitor) |
| 5672 | Shared | RabbitMQ AMQP |
| 6379 | Shared | Redis |
| 15672 | Shared | RabbitMQ Management |
| 8100-8199 | NERO | 8100=API, 8101=SPA |
| 8200-8299 | MeetingTax | 8200=API, 8201=Frontend |
| 8300-8399 | EulaGuard | 8300=API, 8301=Frontend |
| 8400-8499 | (Future) | Reserved |
| 8500-8599 | (Future) | Reserved |

### Port Assignment Within a Range

| Offset | Purpose | Example (NERO=81xx) |
|--------|---------|---------------------|
| +00 | Backend API | 8100 |
| +01 | Frontend SPA | 8101 |
| +02 | Worker/Celery | 8102 (if exposed) |
| +03 | WebSocket (if separate) | 8103 |
| +10 | Admin panel | 8110 |
| +50 | Dev/staging API | 8150 |

### Tracking Active Ports

Maintain a port registry file:

```bash
# /srv/port-registry.txt
# Format: PORT  SERVICE         PROJECT     NOTES
5432    postgresql      shared      Docker, local only
5555    flower          shared      Docker, basic auth
5672    rabbitmq-amqp   shared      Docker, local only
6379    redis           shared      Docker, local only
8100    nero-channel-web nero       FastAPI API
8101    nero-web        nero        React SPA (serve)
8200    meetingtax-be   meetingtax  FastAPI API
8201    meetingtax-fe   meetingtax  Next.js
15672   rabbitmq-mgmt   shared      Docker, local only
```

## Directory Structure

### Per-Project Layout

```
/srv/
├── nero/                          # NERO platform
│   ├── nero-core/                 # Celery workers
│   │   ├── .venv/
│   │   └── src/
│   ├── nero-channel-web/          # FastAPI API
│   │   ├── .venv/
│   │   └── src/
│   ├── nero-channel-tg/           # Telegram bot
│   │   ├── .venv/
│   │   └── src/
│   ├── nero-web/                  # React SPA
│   │   └── dist/
│   ├── nero-infra/                # Docker Compose (shared services)
│   └── .env                       # NERO secrets
├── meetingtax/                    # MeetingTax SaaS
│   ├── be/                        # FastAPI backend
│   │   ├── .venv/
│   │   └── src/
│   ├── fe/                        # Next.js frontend
│   │   └── .next/
│   └── .env
├── eulaguard/                     # EulaGuard
│   ├── api/
│   └── .env
└── port-registry.txt              # Port allocation tracking
```

### Development/Source Layout

```
~/workspace/repos/                 # NERO source code
~/projects/meetingtax/             # MeetingTax source
~/projects/eulaguard/              # EulaGuard source
```

## nginx Multi-Domain Configuration

### Directory Structure

```
/etc/nginx/
├── nginx.conf                     # Global config
├── sites-available/               # All site configs
│   ├── nero.faion.net
│   ├── meetingtax.io
│   └── eulaguard.com
├── sites-enabled/                 # Symlinks to active sites
│   ├── nero.faion.net -> ../sites-available/nero.faion.net
│   ├── meetingtax.io -> ../sites-available/meetingtax.io
│   └── eulaguard.com -> ../sites-available/eulaguard.com
└── snippets/                      # Reusable config fragments
    ├── ssl-params.conf
    ├── proxy-params.conf
    └── security-headers.conf
```

### Shared Snippets

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
```

```nginx
# /etc/nginx/snippets/security-headers.conf
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

### Site Configuration: NERO

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

    # Cloudflare Origin Certificate
    ssl_certificate /etc/ssl/nero.faion.net/cert.pem;
    ssl_certificate_key /etc/ssl/nero.faion.net/key.pem;

    include snippets/security-headers.conf;

    # API routes
    location /api/ {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8100;
    }

    # WebSocket
    location /ws {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8100;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

    # React SPA (frontend)
    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8101;
    }
}
```

### Adding a New Site

```bash
# 1. Create site config
sudo nano /etc/nginx/sites-available/newproject.com

# 2. Enable site
sudo ln -s /etc/nginx/sites-available/newproject.com /etc/nginx/sites-enabled/

# 3. Test config
sudo nginx -t

# 4. Reload nginx
sudo systemctl reload nginx
```

## Cloudflare DNS Integration

### DNS Records

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | nero.faion.net | SERVER_IP | Proxied |
| A | meetingtax.io | SERVER_IP | Proxied |
| A | www.meetingtax.io | SERVER_IP | Proxied |
| A | eulaguard.com | SERVER_IP | Proxied |

### SSL Mode

| Mode | Description | Recommendation |
|------|-------------|---------------|
| Flexible | CF terminates SSL, HTTP to origin | Not recommended |
| Full | CF terminates SSL, self-signed on origin | Acceptable |
| Full (Strict) | CF terminates SSL, valid cert on origin | Recommended |

For Full (Strict): Use Cloudflare Origin Certificates (free, 15-year validity).

```bash
# Install Cloudflare Origin Certificate
sudo mkdir -p /etc/ssl/nero.faion.net
# Paste cert and key from Cloudflare dashboard
sudo nano /etc/ssl/nero.faion.net/cert.pem
sudo nano /etc/ssl/nero.faion.net/key.pem
sudo chmod 600 /etc/ssl/nero.faion.net/key.pem
```

## Shared vs Isolated Services

### Decision Matrix

| Factor | Shared | Isolated |
|--------|--------|----------|
| RAM usage | Lower (one instance) | Higher (per-project) |
| Disk usage | Lower | Higher |
| Backup complexity | Simpler (one backup) | Complex (per-project) |
| Isolation | Weak (shared failure domain) | Strong (independent) |
| Upgrade risk | All projects affected | Per-project |
| Recommended for | Solo dev, 2-5 projects | Production SaaS, team |

### Shared PostgreSQL Pattern

Single PostgreSQL instance, separate databases per project:

```sql
-- Create per-project databases
CREATE DATABASE nero;
CREATE DATABASE meetingtax;
CREATE DATABASE eulaguard;

-- Create per-project users
CREATE USER nero_user WITH PASSWORD 'secret1';
CREATE USER mtax_user WITH PASSWORD 'secret2';

-- Grant access
GRANT ALL PRIVILEGES ON DATABASE nero TO nero_user;
GRANT ALL PRIVILEGES ON DATABASE meetingtax TO mtax_user;
```

### Shared Redis Pattern

Single Redis instance, key prefix isolation:

```
nero:context:*        # NERO context cache
nero:sessions:*       # NERO sessions
mtax:sessions:*       # MeetingTax sessions
mtax:cache:*          # MeetingTax cache
```

Or use separate Redis databases (0-15):

| DB | Project |
|----|---------|
| 0 | NERO (default) |
| 1 | NERO Celery backend |
| 2 | MeetingTax |
| 3 | EulaGuard |

## Resource Planning

### Memory Budget (30GB RAM)

| Service | Allocation | Notes |
|---------|-----------|-------|
| OS + kernel | 1 GB | Reserved |
| PostgreSQL | 4 GB | shared_buffers=2GB |
| Redis | 2 GB | maxmemory=1.5GB |
| RabbitMQ | 1 GB | Default limits |
| NERO (all services) | 12 GB | Core=8G, Web=2G, TG=1G, SPA=0.5G |
| MeetingTax | 4 GB | BE=2G, FE=2G |
| EulaGuard | 2 GB | API=2G |
| Swap buffer | 4 GB | Swap file |
| **Total** | **30 GB** | |

### When to Split to a Second Server

| Signal | Action |
|--------|--------|
| Consistent memory pressure > 85% | Add swap or split |
| CPU consistently > 70% | Split compute-heavy project |
| One project needs different OS/kernel | Split |
| Compliance requires isolation | Split |
| Revenue justifies dedicated hosting | Split |

## Related Methodologies

| Methodology | Relationship |
|-------------|-------------|
| [server-init-bootstrap](../server-init-bootstrap/) | Set up base server before adding projects |
| [deploy-scripts](../deploy-scripts/) | Per-project deploy scripts |
| [secrets-management](../secrets-management/) | Per-project .env files |
| [swap-memory-management](../swap-memory-management/) | Memory limits per project |
| [health-checks-autoheal](../health-checks-autoheal/) | Per-project health monitoring |
