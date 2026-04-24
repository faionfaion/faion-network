# Docker Templates

Ready-to-use templates for common scenarios. Copy and customize.

---

## Dockerfile Templates

### Python Web Application

```dockerfile
# syntax=docker/dockerfile:1

# ============================================
# Stage 1: Build
# ============================================
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

# Install dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.12-slim AS runtime

LABEL maintainer="your-email@example.com"
LABEL version="1.0.0"

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 appuser

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy application
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

### Node.js Application

```dockerfile
# syntax=docker/dockerfile:1

# ============================================
# Stage 1: Dependencies
# ============================================
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# ============================================
# Stage 2: Build
# ============================================
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# ============================================
# Stage 3: Production deps
# ============================================
FROM node:20-alpine AS prod-deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

# ============================================
# Stage 4: Runtime
# ============================================
FROM node:20-alpine AS runtime

LABEL maintainer="your-email@example.com"
LABEL version="1.0.0"

WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 appuser

COPY --from=builder --chown=appuser:nodejs /app/dist ./dist
COPY --from=prod-deps --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --chown=appuser:nodejs package.json ./

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

### Go Application

```dockerfile
# syntax=docker/dockerfile:1

# ============================================
# Stage 1: Build
# ============================================
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-w -s" \
    -o /app/server \
    ./cmd/server

# ============================================
# Stage 2: Runtime
# ============================================
FROM scratch

LABEL maintainer="your-email@example.com"
LABEL version="1.0.0"

COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080

ENTRYPOINT ["/server"]
```

### Static Site (Nginx)

```dockerfile
# syntax=docker/dockerfile:1

# ============================================
# Stage 1: Build
# ============================================
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ============================================
# Stage 2: Runtime
# ============================================
FROM nginx:alpine AS runtime

LABEL maintainer="your-email@example.com"
LABEL version="1.0.0"

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

---

## Docker Compose Templates

### Basic Web + Database

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ${PROJECT_NAME:-myapp}
    restart: unless-stopped
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      - DATABASE_URL=postgres://${DB_USER:-user}:${DB_PASSWORD:-pass}@db:5432/${DB_NAME:-mydb}
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:16-alpine
    container_name: ${PROJECT_NAME:-myapp}-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER:-user}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-pass}
      POSTGRES_DB: ${DB_NAME:-mydb}
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-user} -d ${DB_NAME:-mydb}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db_data:

networks:
  app-network:
    driver: bridge
```

### Full Stack with Cache and Proxy

```yaml
# docker-compose.yml
version: "3.9"

services:
  # Application
  app:
    build:
      context: .
      target: runtime
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
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
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M

  # Database
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Cache
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 100mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Reverse Proxy
  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:80/"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  db_data:
  redis_data:

networks:
  frontend:
  backend:
    internal: true
```

### Development Override

```yaml
# docker-compose.override.yml
version: "3.9"

services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules  # or /app/.venv for Python
    ports:
      - "8000:8000"
      - "5678:5678"  # Debugger port
    environment:
      - DEBUG=true
    command: ["npm", "run", "dev"]  # or uvicorn with --reload

  db:
    ports:
      - "5432:5432"

  redis:
    ports:
      - "6379:6379"
```

---

## Nginx Configuration Template

```nginx
# nginx.conf
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript
               application/xml application/xml+rss text/javascript;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    upstream app {
        server app:8000;
        keepalive 32;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://app;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Connection "";
            proxy_buffering off;
            proxy_read_timeout 300s;
        }

        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://app;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            access_log off;
            return 200 "OK";
            add_header Content-Type text/plain;
        }

        # Static files (if serving from nginx)
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

---

## .dockerignore Template

```dockerignore
# Version control
.git
.gitignore
.gitattributes

# Dependencies (will be installed in container)
node_modules
venv
.venv
__pycache__
*.pyc
*.pyo
.pytest_cache
.mypy_cache
.ruff_cache

# Build artifacts
dist
build
*.egg-info
.eggs
target
out

# IDE & Editor
.vscode
.idea
*.swp
*.swo
*~
.editorconfig

# Docker (avoid recursive)
Dockerfile*
docker-compose*
.docker
.dockerignore

# Environment & secrets
.env
.env.*
*.local
.secrets

# Tests & coverage
tests
test
__tests__
coverage
.coverage
htmlcov
.tox
.nox
pytest.ini
jest.config.*

# Documentation
docs
*.md
!README.md
CHANGELOG*
LICENSE*

# CI/CD
.github
.gitlab-ci.yml
.circleci
Jenkinsfile
azure-pipelines.yml

# Misc
*.log
*.logs
tmp
temp
.cache
.npm
.yarn
.pnpm-store

# OS files
.DS_Store
Thumbs.db
Desktop.ini

# Large files
*.zip
*.tar.gz
*.rar
*.7z
```

---

## Entrypoint Script Template

```bash
#!/bin/bash
set -e

# ============================================
# Configuration
# ============================================
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
WAIT_FOR_DB=${WAIT_FOR_DB:-true}
RUN_MIGRATIONS=${RUN_MIGRATIONS:-true}
COLLECT_STATIC=${COLLECT_STATIC:-false}

# ============================================
# Functions
# ============================================
wait_for_postgres() {
    echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
    while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 2
    done
    echo "PostgreSQL is ready!"
}

wait_for_redis() {
    if [ -n "$REDIS_HOST" ]; then
        echo "Waiting for Redis at $REDIS_HOST..."
        while ! redis-cli -h "$REDIS_HOST" ping > /dev/null 2>&1; do
            echo "Redis is unavailable - sleeping"
            sleep 2
        done
        echo "Redis is ready!"
    fi
}

run_migrations() {
    echo "Running database migrations..."
    python manage.py migrate --noinput
    echo "Migrations complete!"
}

collect_static() {
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    echo "Static files collected!"
}

# ============================================
# Main
# ============================================
echo "Starting application..."

# Wait for dependencies
if [ "$WAIT_FOR_DB" = "true" ]; then
    wait_for_postgres
fi
wait_for_redis

# Run migrations
if [ "$RUN_MIGRATIONS" = "true" ]; then
    run_migrations
fi

# Collect static files
if [ "$COLLECT_STATIC" = "true" ]; then
    collect_static
fi

# Execute the main command
echo "Executing: $@"
exec "$@"
```

---

## Environment File Template

```bash
# .env.example (copy to .env)

# Application
APP_NAME=myapp
APP_ENV=development
APP_DEBUG=true
APP_PORT=8000
SECRET_KEY=your-secret-key-here

# Database
DB_HOST=db
DB_PORT=5432
DB_NAME=mydb
DB_USER=user
DB_PASSWORD=pass
DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://${REDIS_HOST}:${REDIS_PORT}/0

# External services
# API_KEY=
# SMTP_HOST=
# SMTP_PORT=
# SMTP_USER=
# SMTP_PASSWORD=
```

---

## Makefile Template

```makefile
# Makefile for Docker operations

.PHONY: help build up down logs shell test clean

PROJECT_NAME ?= myapp
COMPOSE_FILE ?= docker-compose.yml

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build images
	docker compose -f $(COMPOSE_FILE) build

up: ## Start services
	docker compose -f $(COMPOSE_FILE) up -d

down: ## Stop services
	docker compose -f $(COMPOSE_FILE) down

logs: ## View logs
	docker compose -f $(COMPOSE_FILE) logs -f

shell: ## Open shell in app container
	docker compose -f $(COMPOSE_FILE) exec app bash

test: ## Run tests
	docker compose -f $(COMPOSE_FILE) exec app pytest

migrate: ## Run migrations
	docker compose -f $(COMPOSE_FILE) exec app python manage.py migrate

clean: ## Remove all containers, volumes, and images
	docker compose -f $(COMPOSE_FILE) down -v --rmi all

prod-up: ## Start production services
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down: ## Stop production services
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down
```
