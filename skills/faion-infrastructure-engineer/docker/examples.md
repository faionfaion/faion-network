# Docker Examples

**Production Patterns: Multi-stage Builds, Networking, Storage, Security (2025-2026)**

---

## Multi-stage Build Examples

### Python (FastAPI/Django)

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim AS production

LABEL maintainer="team@example.com"
LABEL version="1.0.0"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash --uid 1000 appuser

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app.main:app"]
```

### Go (Minimal Binary with Distroless)

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Build
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s" -o /app/server ./cmd/server

# Stage 2: Production (distroless for maximum security)
FROM gcr.io/distroless/static:nonroot AS production

COPY --from=builder /app/server /server

USER nonroot:nonroot

EXPOSE 8080

ENTRYPOINT ["/server"]
```

**Result:** Final image ~10-20MB, no shell, minimal attack surface.

### Node.js (Next.js with Standalone)

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production deps
FROM node:20-alpine AS prod-deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Stage 4: Production
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "server.js"]
```

### Rust (Minimal Binary)

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Build
FROM rust:1.75-alpine AS builder

RUN apk add --no-cache musl-dev

WORKDIR /app

# Cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src

# Build application
COPY src ./src
RUN touch src/main.rs
RUN cargo build --release

# Stage 2: Production (scratch = 0 bytes base)
FROM scratch AS production

COPY --from=builder /app/target/release/myapp /myapp

EXPOSE 8080

ENTRYPOINT ["/myapp"]
```

**Result:** Final image ~5-15MB

---

## Networking Examples

### Three-Tier Network Architecture

```yaml
# compose.yaml

services:
  nginx:
    image: nginx:alpine
    container_name: myapp-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3

  app:
    build:
      context: .
      target: production
    image: myapp:${VERSION:-latest}
    container_name: myapp
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://app:${DB_PASSWORD}@db:5432/appdb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:16-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=app
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=appdb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 100mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  frontend:
    driver: bridge
    # External access allowed
  backend:
    driver: bridge
    internal: true  # No external access - database isolation

volumes:
  postgres-data:
  redis-data:
```

### Custom Network with Subnet

```yaml
networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
    driver_opts:
      com.docker.network.bridge.enable_icc: "true"
      com.docker.network.bridge.enable_ip_masquerade: "true"
```

### Service Mesh Pattern (Microservices)

```yaml
services:
  api-gateway:
    image: kong:latest
    ports:
      - "8000:8000"
      - "8443:8443"
    networks:
      - public
      - services

  user-service:
    build: ./services/user
    networks:
      - services
      - user-db
    # No ports exposed externally

  order-service:
    build: ./services/order
    networks:
      - services
      - order-db
    # No ports exposed externally

  payment-service:
    build: ./services/payment
    networks:
      - services
      - payment-db
    # No ports exposed externally

networks:
  public:
    driver: bridge
  services:
    driver: bridge
    internal: false  # Services can reach each other
  user-db:
    driver: bridge
    internal: true  # User database isolated
  order-db:
    driver: bridge
    internal: true  # Order database isolated
  payment-db:
    driver: bridge
    internal: true  # Payment database isolated
```

### Network Segmentation with WAF (2025-2026)

```yaml
services:
  waf:
    image: owasp/modsecurity:nginx-alpine
    ports:
      - "443:443"
    networks:
      - dmz
    volumes:
      - ./waf/rules:/etc/modsecurity.d:ro

  app:
    build: .
    networks:
      - dmz
      - app-network
    # No direct external access

  db:
    image: postgres:16-alpine
    networks:
      - app-network
    # Isolated from DMZ

networks:
  dmz:
    driver: bridge
  app-network:
    driver: bridge
    internal: true
```

---

## Storage Examples

### Named Volumes for Persistence

```yaml
services:
  app:
    volumes:
      - app-data:/app/data           # Named volume for app data
      - app-uploads:/app/uploads     # Named volume for uploads

  db:
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  app-data:
    driver: local
  app-uploads:
    driver: local
  postgres-data:
    driver: local
```

### Read-Only and tmpfs Mounts

```yaml
services:
  app:
    read_only: true  # Root filesystem is read-only
    tmpfs:
      - /tmp:size=100M,mode=1777
      - /var/run:size=10M,mode=755
    volumes:
      - ./config:/app/config:ro              # Config read-only
      - app-data:/app/data                   # Persistent data writable
      - type: tmpfs                          # Alternative tmpfs syntax
        target: /app/cache
        tmpfs:
          size: 50000000  # 50MB
```

### Bind Mounts for Development

```yaml
# compose.override.yaml (development only)
services:
  app:
    volumes:
      - .:/app                          # Source code
      - /app/node_modules               # Exclude node_modules
      - /app/.venv                      # Exclude venv
      - ./config:/app/config:ro         # Config read-only
```

### Volume Backup Pattern

```bash
# Backup volume
docker run --rm \
    -v postgres-data:/data \
    -v $(pwd)/backups:/backup \
    alpine tar czf /backup/postgres-backup-$(date +%Y%m%d).tar.gz -C /data .

# Restore volume
docker run --rm \
    -v postgres-data:/data \
    -v $(pwd)/backups:/backup \
    alpine tar xzf /backup/postgres-backup-20260126.tar.gz -C /data
```

### Encrypted Volumes (2025-2026)

```yaml
# With external encryption
services:
  db:
    volumes:
      - type: volume
        source: encrypted-data
        target: /var/lib/postgresql/data
        volume:
          nocopy: true

volumes:
  encrypted-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/encrypted-storage/db
```

---

## Security Examples

### Hardened Container Configuration

```yaml
services:
  app:
    image: myapp:1.0.0
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to port < 1024
    security_opt:
      - no-new-privileges:true
      - seccomp:./seccomp-profile.json  # Custom seccomp
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
          pids: 100
        reservations:
          cpus: "0.25"
          memory: 128M
```

### Docker Secrets (Swarm Mode)

```yaml
services:
  app:
    image: myapp:1.0.0
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
      - API_KEY_FILE=/run/secrets/api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true  # Pre-created secret
```

### BuildKit Secrets (Build-time)

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim

# Secret not visible in image layers
RUN --mount=type=secret,id=github_token \
    pip install git+https://$(cat /run/secrets/github_token)@github.com/org/private-repo.git

# Build with:
# docker build --secret id=github_token,src=./github_token.txt -t myapp .
```

### External Vault Integration

```yaml
services:
  app:
    image: myapp:1.0.0
    environment:
      - VAULT_ADDR=https://vault.example.com
      - VAULT_ROLE=myapp
    volumes:
      - ./vault-agent-config.hcl:/etc/vault/config.hcl:ro
```

### AWS Secrets Manager Integration (2025-2026)

```yaml
services:
  app:
    image: myapp:1.0.0
    environment:
      - AWS_REGION=us-east-1
      - SECRET_ARN=arn:aws:secretsmanager:us-east-1:123456789:secret:myapp
    # Use init container or sidecar to fetch secrets
```

---

## Health Check Patterns

### HTTP Health Check

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### TCP Health Check

```yaml
healthcheck:
  test: ["CMD-SHELL", "nc -z localhost 8000 || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Database Health Checks

```yaml
# PostgreSQL
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER -d $POSTGRES_DB"]
  interval: 10s
  timeout: 5s
  retries: 5

# MySQL
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 10s
  timeout: 5s
  retries: 5

# MongoDB
healthcheck:
  test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
  interval: 10s
  timeout: 5s
  retries: 5

# Redis
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Script-based Health Check

```yaml
healthcheck:
  test: ["CMD", "/app/healthcheck.sh"]
  interval: 30s
  timeout: 10s
  retries: 3
```

```bash
#!/bin/sh
# /app/healthcheck.sh

# Check HTTP endpoint
if ! curl -sf http://localhost:8000/health; then
    exit 1
fi

# Check database connection
if ! python -c "from app import db; db.health_check()"; then
    exit 1
fi

exit 0
```

---

## Resource Limits Examples

### CPU and Memory Limits

```yaml
deploy:
  resources:
    limits:
      cpus: "2.0"
      memory: 1G
    reservations:
      cpus: "0.5"
      memory: 256M
```

### With PID and OOM Settings

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
          pids: 100
    mem_swappiness: 0
    oom_kill_disable: false
    oom_score_adj: 500  # Higher priority for OOM kill
```

### Sizing Guidelines

| Service Type | CPU | Memory | PIDs |
|--------------|-----|--------|------|
| API (low traffic) | 0.5-1.0 | 256-512M | 50 |
| API (high traffic) | 1.0-2.0 | 512M-1G | 100 |
| Worker | 0.5-1.0 | 256-512M | 50 |
| Database | 1.0-4.0 | 1-4G | 200 |
| Redis | 0.25-0.5 | 64-256M | 50 |

---

## Logging Examples

### JSON File with Rotation

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "5"
    compress: "true"
```

### Syslog

```yaml
logging:
  driver: "syslog"
  options:
    syslog-address: "tcp://192.168.1.100:514"
    syslog-facility: "daemon"
    tag: "myapp/{{.Name}}"
```

### Fluentd/Fluent Bit

```yaml
logging:
  driver: "fluentd"
  options:
    fluentd-address: "localhost:24224"
    tag: "docker.{{.Name}}"
    fluentd-async: "true"
```

### Loki

```yaml
logging:
  driver: "loki"
  options:
    loki-url: "http://loki:3100/loki/api/v1/push"
    loki-batch-size: "400"
    loki-retries: "3"
```

---

## CI/CD Integration Example

### GitHub Actions with Security Scanning

```yaml
# .github/workflows/docker.yml

name: Docker Build

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Lint Dockerfile
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile

      - name: Build image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          load: true
          tags: myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Scan for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          image: myapp:${{ github.sha }}
          format: spdx-json
          output-file: sbom.spdx.json

      - name: Sign image with Cosign
        if: github.ref == 'refs/heads/main'
        uses: sigstore/cosign-installer@v3

      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest
```

---

## Production Compose Pattern

### Full Stack with All Best Practices

```yaml
# compose.yaml

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
      args:
        - VERSION=${VERSION:-latest}
        - BUILD_DATE=${BUILD_DATE:-}
        - GIT_SHA=${GIT_SHA:-}
    image: ${REGISTRY:-localhost}/myapp:${VERSION:-latest}
    container_name: myapp
    restart: unless-stopped
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp:size=100M
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      - DATABASE_URL=postgres://${DB_USER:-app}:${DB_PASSWORD}@db:5432/${DB_NAME:-appdb}
      - REDIS_URL=redis://redis:6379/0
      - LOG_LEVEL=${LOG_LEVEL:-info}
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: "${APP_CPU_LIMIT:-1.0}"
          memory: ${APP_MEMORY_LIMIT:-512M}
          pids: 100
        reservations:
          cpus: "0.25"
          memory: 128M
    networks:
      - frontend
      - backend
    volumes:
      - app-data:/app/data
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${DB_USER:-app}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME:-appdb}
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app} -d ${DB_NAME:-appdb}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
    # No ports exposed - internal only

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 100mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 128M
    # No ports exposed - internal only

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  postgres-data:
  redis-data:
  app-data:
```

---

## Seccomp Profile Example (2025-2026)

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_AARCH64"],
  "syscalls": [
    {
      "names": [
        "accept", "accept4", "access", "arch_prctl", "bind",
        "brk", "capget", "capset", "chdir", "chmod", "chown",
        "clone", "close", "connect", "dup", "dup2", "dup3",
        "epoll_create", "epoll_create1", "epoll_ctl", "epoll_wait",
        "epoll_pwait", "execve", "exit", "exit_group", "fchmod",
        "fchown", "fcntl", "fstat", "fstatfs", "futex", "getcwd",
        "getdents64", "geteuid", "getgid", "getpeername", "getpid",
        "getppid", "getrandom", "getsockname", "getsockopt", "getuid",
        "ioctl", "listen", "lseek", "lstat", "madvise", "memfd_create",
        "mkdir", "mmap", "mprotect", "munmap", "nanosleep", "newfstatat",
        "open", "openat", "pipe", "pipe2", "poll", "prctl", "pread64",
        "prlimit64", "pwrite64", "read", "readlink", "recvfrom", "recvmsg",
        "rename", "rt_sigaction", "rt_sigprocmask", "rt_sigreturn",
        "sched_getaffinity", "sched_yield", "select", "sendmsg", "sendto",
        "set_robust_list", "set_tid_address", "setgid", "setgroups",
        "setsockopt", "setuid", "shutdown", "sigaltstack", "socket",
        "stat", "statfs", "tgkill", "umask", "uname", "unlink", "wait4",
        "write", "writev"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

---

*Docker Examples | faion-infrastructure-engineer*
