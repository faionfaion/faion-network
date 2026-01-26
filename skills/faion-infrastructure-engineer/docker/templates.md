# Docker Templates

**Ready-to-Use Dockerfiles and Compose Configurations (2025-2026)**

---

## Dockerfile Templates

### Python FastAPI/Django

```dockerfile
# syntax=docker/dockerfile:1

#############################################
# Stage 1: Build dependencies
#############################################
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies with cache mount
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

#############################################
# Stage 2: Development
#############################################
FROM python:3.12-slim AS development

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash --uid 1000 appuser

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

#############################################
# Stage 3: Production
#############################################
FROM python:3.12-slim AS production

LABEL maintainer="team@example.com"
LABEL version="1.0.0"

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash --uid 1000 appuser

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "app.main:app"]
```

### Node.js/Next.js

```dockerfile
# syntax=docker/dockerfile:1

#############################################
# Stage 1: Dependencies
#############################################
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

#############################################
# Stage 2: Build
#############################################
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

#############################################
# Stage 3: Production dependencies
#############################################
FROM node:20-alpine AS prod-deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

#############################################
# Stage 4: Development
#############################################
FROM node:20-alpine AS development
WORKDIR /app

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 appuser

COPY --from=deps /app/node_modules ./node_modules
COPY . .

USER appuser

EXPOSE 3000

CMD ["npm", "run", "dev"]

#############################################
# Stage 5: Production
#############################################
FROM node:20-alpine AS production

LABEL maintainer="team@example.com"
LABEL version="1.0.0"

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 appuser

COPY --from=builder /app/public ./public
COPY --from=builder --chown=appuser:nodejs /app/.next/standalone ./
COPY --from=builder --chown=appuser:nodejs /app/.next/static ./.next/static
COPY --from=prod-deps /app/node_modules ./node_modules

USER appuser

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "server.js"]
```

### Go API

```dockerfile
# syntax=docker/dockerfile:1

#############################################
# Stage 1: Build
#############################################
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Install dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source and build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s" -o /app/server ./cmd/server

#############################################
# Stage 2: Production (distroless)
#############################################
FROM gcr.io/distroless/static:nonroot AS production

LABEL maintainer="team@example.com"
LABEL version="1.0.0"

COPY --from=builder /app/server /server

USER nonroot:nonroot

EXPOSE 8080

ENTRYPOINT ["/server"]
```

### Rust API

```dockerfile
# syntax=docker/dockerfile:1

#############################################
# Stage 1: Build
#############################################
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

#############################################
# Stage 2: Production
#############################################
FROM scratch AS production

COPY --from=builder /app/target/release/myapp /myapp

EXPOSE 8080

ENTRYPOINT ["/myapp"]
```

### Java Spring Boot

```dockerfile
# syntax=docker/dockerfile:1

#############################################
# Stage 1: Build
#############################################
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN ./mvnw dependency:go-offline

COPY src ./src
RUN ./mvnw package -DskipTests

#############################################
# Stage 2: Production
#############################################
FROM eclipse-temurin:21-jre-alpine AS production

LABEL maintainer="team@example.com"
LABEL version="1.0.0"

WORKDIR /app

RUN addgroup --system --gid 1001 javauser \
    && adduser --system --uid 1001 javauser

COPY --from=builder /app/target/*.jar app.jar

USER javauser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD wget -q --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## Compose Templates

### Full Stack Template

```yaml
# compose.yaml

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
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
      - SECRET_KEY=${SECRET_KEY}
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

### Development Override Template

```yaml
# compose.override.yaml

services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules  # Exclude node_modules
      - /app/.venv         # Exclude venv
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    command: ["npm", "run", "dev"]  # Or uvicorn with --reload
    ports:
      - "${APP_PORT:-8000}:8000"
      - "9229:9229"  # Debug port

  db:
    ports:
      - "${DB_PORT:-5432}:5432"

  redis:
    ports:
      - "${REDIS_PORT:-6379}:6379"

  mailhog:
    image: mailhog/mailhog
    container_name: myapp-mailhog
    ports:
      - "1025:1025"
      - "8025:8025"
    networks:
      - backend
    profiles:
      - dev
```

### Production Override Template

```yaml
# compose.prod.yaml

services:
  app:
    image: ${REGISTRY}/myapp:${VERSION}
    build: null
    restart: always
    deploy:
      mode: replicated
      replicas: ${APP_REPLICAS:-2}
      resources:
        limits:
          cpus: "2.0"
          memory: 1G
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      rollback_config:
        parallelism: 1
        delay: 10s

  db:
    restart: always
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

  redis:
    restart: always
```

---

## .dockerignore Template

```dockerignore
# Git
.git
.gitignore
.gitattributes

# Dependencies
node_modules
.venv
venv
__pycache__
*.pyc
*.pyo
.eggs
*.egg-info

# Build outputs
dist
build
target
*.egg

# IDE
.idea
.vscode
*.swp
*.swo
*~

# Testing
.coverage
htmlcov
.pytest_cache
.tox
coverage.xml
*.cover
.hypothesis

# Environment
.env
.env.*
*.local
.envrc

# Docker
Dockerfile*
docker-compose*
compose*.yaml
compose*.yml
.docker
.dockerignore

# Documentation
docs
*.md
!README.md

# CI/CD
.github
.gitlab-ci.yml
Jenkinsfile
.circleci
.travis.yml

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs

# Temporary
tmp
temp
*.tmp
*.temp
```

---

## .env.example Template

```bash
# Application
APP_NAME=myapp
VERSION=1.0.0
SECRET_KEY=change-me-in-production
LOG_LEVEL=info
DEBUG=false

# Server
APP_PORT=8000
APP_HOST=0.0.0.0
APP_REPLICAS=2

# Resource Limits
APP_CPU_LIMIT=1.0
APP_MEMORY_LIMIT=512M

# Database
DB_USER=app
DB_PASSWORD=secure-password-here
DB_NAME=appdb
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Registry
REGISTRY=registry.example.com

# External Services (optional)
# SMTP_HOST=smtp.example.com
# SMTP_PORT=587
# SMTP_USER=noreply@example.com
# SMTP_PASSWORD=smtp-password

# Feature Flags
# ENABLE_FEATURE_X=false
```

---

## Nginx Configuration Template

```nginx
# nginx/nginx.conf

user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    keepalive_timeout  65;
    gzip  on;

    upstream app {
        server app:8000;
    }

    server {
        listen 80;
        server_name _;

        location /health {
            access_log off;
            return 200 "OK\n";
            add_header Content-Type text/plain;
        }

        location /static/ {
            alias /var/www/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        location / {
            proxy_pass http://app;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 86400;
        }
    }
}
```

---

## Makefile Template

```makefile
# Makefile for Docker operations

.PHONY: build up down logs shell test lint scan

# Variables
COMPOSE := docker compose
IMAGE := myapp
VERSION := $(shell git describe --tags --always --dirty)

# Build
build:
	$(COMPOSE) build --no-cache

build-dev:
	$(COMPOSE) build

# Run
up:
	$(COMPOSE) up -d

up-dev:
	$(COMPOSE) up

down:
	$(COMPOSE) down

down-volumes:
	$(COMPOSE) down -v

# Logs
logs:
	$(COMPOSE) logs -f

logs-app:
	$(COMPOSE) logs -f app

# Shell access
shell:
	$(COMPOSE) exec app sh

shell-db:
	$(COMPOSE) exec db psql -U app -d appdb

# Testing
test:
	$(COMPOSE) exec app pytest

lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

# Security
scan:
	docker scout cves $(IMAGE):$(VERSION)

scan-trivy:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
		aquasec/trivy:latest image $(IMAGE):$(VERSION)

# Cleanup
prune:
	docker system prune -af --volumes

# Production
prod-up:
	$(COMPOSE) -f compose.yaml -f compose.prod.yaml up -d

prod-down:
	$(COMPOSE) -f compose.yaml -f compose.prod.yaml down
```

---

## Seccomp Profile Template (2025-2026)

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

## Docker Entrypoint Template

```bash
#!/bin/bash
# docker-entrypoint.sh

set -e

# Wait for database
if [ -n "$DATABASE_URL" ]; then
    echo "Waiting for database..."
    until pg_isready -h db -U app 2>/dev/null; do
        sleep 1
    done
    echo "Database is ready!"
fi

# Run migrations (if applicable)
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput
fi

# Collect static files (if applicable)
if [ "$COLLECT_STATIC" = "true" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Execute main command
exec "$@"
```

---

## GitHub Actions Docker Workflow Template

```yaml
# .github/workflows/docker.yml

name: Docker Build & Push

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      security-events: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Lint Dockerfile
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile

      - name: Log in to registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha

      - name: Build image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          load: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Scan for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

      - name: Push image
        if: github.event_name != 'pull_request'
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

---

*Docker Templates | faion-infrastructure-engineer*
