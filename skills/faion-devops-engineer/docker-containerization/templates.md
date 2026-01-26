# Docker Containerization Templates

Copy-paste templates for common containerization scenarios.

## Dockerfile Templates

### Template: Multi-Stage Build (Generic)

```dockerfile
# ==============================================================================
# Stage 1: Build
# ==============================================================================
FROM {BASE_IMAGE_BUILD} AS builder

WORKDIR /app

# Install build dependencies
RUN {INSTALL_BUILD_DEPS}

# Copy dependency files first (for caching)
COPY {DEPENDENCY_FILES} ./
RUN {INSTALL_DEPENDENCIES}

# Copy source and build
COPY . .
RUN {BUILD_COMMAND}

# ==============================================================================
# Stage 2: Production
# ==============================================================================
FROM {BASE_IMAGE_PROD}

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Install runtime dependencies only
RUN {INSTALL_RUNTIME_DEPS}

# Copy artifacts from builder
COPY --from=builder --chown=appuser:appgroup {BUILD_OUTPUT} .

USER appuser

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD {HEALTH_CHECK_CMD}

EXPOSE {PORT}

CMD {RUN_COMMAND}
```

### Template: Python Application

```dockerfile
# syntax=docker/dockerfile:1
# ==============================================================================
# Multi-stage Python Application
# ==============================================================================

# Stage 1: Build
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim

RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

COPY --chown=app:app . .

USER app

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["python", "-m", "app"]
```

### Template: Node.js Application

```dockerfile
# syntax=docker/dockerfile:1
# ==============================================================================
# Multi-stage Node.js Application
# ==============================================================================

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine

RUN addgroup -g 1001 -S nodejs && adduser -S app -u 1001

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder --chown=app:nodejs /app/dist ./dist
COPY package*.json ./

USER app

ENV NODE_ENV=production

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Template: Go Application (Distroless)

```dockerfile
# syntax=docker/dockerfile:1
# ==============================================================================
# Multi-stage Go Application
# ==============================================================================

FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server .

FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/server /server

USER nonroot:nonroot

EXPOSE 8080

ENTRYPOINT ["/server"]
```

## Docker Compose Templates

### Template: Single Service

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    image: ${IMAGE_NAME:-myapp}:${IMAGE_TAG:-latest}
    container_name: myapp
    restart: unless-stopped
    ports:
      - "${PORT:-8000}:8000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    env_file:
      - .env
    volumes:
      - app_data:/app/data
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M

volumes:
  app_data:
```

### Template: Full Stack (App + Database + Cache)

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "${PORT:-8000}:8000"
    environment:
      - DATABASE_URL=postgres://postgres:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: "2"
          memory: 1G

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB:-app}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 512M

  cache:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M

volumes:
  postgres_data:
  redis_data:
```

### Template: Development Environment

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
      target: development
    volumes:
      - .:/app
      - /app/node_modules  # Exclude node_modules from bind mount
    ports:
      - "${PORT:-3000}:3000"
      - "9229:9229"  # Debugger
    environment:
      - NODE_ENV=development
      - DEBUG=*
    command: npm run dev

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=dev
      - POSTGRES_DB=app_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_dev:/var/lib/postgresql/data

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgres_dev:
```

## .dockerignore Template

```
# ==============================================================================
# .dockerignore - Exclude from Docker build context
# ==============================================================================

# Version control
.git
.gitignore
.gitattributes

# Dependencies (will be installed in container)
node_modules
__pycache__
*.pyc
.venv
venv
vendor
target

# Build outputs (will be built in container)
dist
build
out
*.egg-info
.next
.nuxt

# IDE and editor
.idea
.vscode
*.swp
*.swo
*~
.project
.classpath
.settings

# Testing and coverage
.coverage
htmlcov
.pytest_cache
.tox
coverage
*.cover
*.log
junit.xml

# Environment and secrets
.env
.env.*
*.local
.secrets

# Docker files (not needed in context)
Dockerfile*
docker-compose*
.docker
.dockerignore

# Documentation (optional - remove if needed in image)
docs
*.md
!README.md
LICENSE

# CI/CD configuration
.github
.gitlab-ci.yml
Jenkinsfile
.circleci
.travis.yml
azure-pipelines.yml

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Misc
*.bak
*.tmp
*.temp
```

## Nginx Configuration Template

```nginx
# nginx.conf - Production configuration for static sites
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "OK";
        add_header Content-Type text/plain;
    }

    # Static assets with cache
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA routing - serve index.html for all routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Disable access to hidden files
    location ~ /\. {
        deny all;
    }
}
```

## Health Check Scripts

### Python Health Check

```python
#!/usr/bin/env python3
"""health_check.py - Container health check script"""
import sys
import urllib.request

try:
    response = urllib.request.urlopen('http://localhost:8000/health', timeout=3)
    if response.status == 200:
        sys.exit(0)
    sys.exit(1)
except Exception:
    sys.exit(1)
```

### Node.js Health Check

```javascript
// health_check.js - Container health check script
const http = require('http');

const options = {
  host: 'localhost',
  port: 3000,
  path: '/health',
  timeout: 3000,
};

const req = http.get(options, (res) => {
  process.exit(res.statusCode === 200 ? 0 : 1);
});

req.on('error', () => process.exit(1));
req.on('timeout', () => {
  req.destroy();
  process.exit(1);
});
```

### Shell Health Check

```bash
#!/bin/sh
# health_check.sh - Container health check script

set -e

# HTTP health check
curl -sf http://localhost:8000/health > /dev/null 2>&1

# Or for wget
# wget --no-verbose --tries=1 --spider http://localhost:8000/health

exit 0
```
