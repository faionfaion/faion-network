# Docker Compose Templates

**Ready-to-Use Configurations for Modern Applications (2025-2026)**

---

## Quick Start Template

Minimal production-ready configuration.

```yaml
# compose.yaml

services:
  app:
    build:
      context: .
      target: production
    image: ${REGISTRY:-localhost}/myapp:${VERSION:-latest}
    restart: unless-stopped
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      - DATABASE_URL=postgres://${DB_USER:-app}:${DB_PASSWORD}@db:5432/${DB_NAME:-appdb}
    env_file:
      - .env
    depends_on:
      db:
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
          cpus: "1.0"
          memory: 512M
    networks:
      - frontend
      - backend
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${DB_USER:-app}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME:-appdb}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true

volumes:
  postgres-data:
```

---

## Full Stack Templates

### Python API Template

```yaml
# compose.yaml - Python FastAPI/Django

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
      args:
        - PYTHON_VERSION=3.12
    image: ${REGISTRY:-localhost}/${APP_NAME:-myapp}:${VERSION:-latest}
    container_name: ${APP_NAME:-myapp}
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
      - ALLOWED_HOSTS=${ALLOWED_HOSTS:-*}
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
      - app-static:/app/static
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  worker:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: ${REGISTRY:-localhost}/${APP_NAME:-myapp}:${VERSION:-latest}
    container_name: ${APP_NAME:-myapp}-worker
    restart: unless-stopped
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    command: celery -A app worker --loglevel=${LOG_LEVEL:-info}
    environment:
      - DATABASE_URL=postgres://${DB_USER:-app}:${DB_PASSWORD}@db:5432/${DB_NAME:-appdb}
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
    networks:
      - backend

  beat:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: ${REGISTRY:-localhost}/${APP_NAME:-myapp}:${VERSION:-latest}
    container_name: ${APP_NAME:-myapp}-beat
    restart: unless-stopped
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    command: celery -A app beat --loglevel=${LOG_LEVEL:-info}
    environment:
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      redis:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 128M
    networks:
      - backend

  db:
    image: postgres:16-alpine
    container_name: ${APP_NAME:-myapp}-db
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
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
    networks:
      - backend

  redis:
    image: redis:7-alpine
    container_name: ${APP_NAME:-myapp}-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 100mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 128M
    networks:
      - backend

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
  app-static:
```

### Node.js API Template

```yaml
# compose.yaml - Node.js/Next.js

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
      args:
        - NODE_VERSION=20
    image: ${REGISTRY:-localhost}/${APP_NAME:-myapp}:${VERSION:-latest}
    container_name: ${APP_NAME:-myapp}
    restart: unless-stopped
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp:size=100M
      - /app/.next/cache:size=500M
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    ports:
      - "${APP_PORT:-3000}:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://${DB_USER:-app}:${DB_PASSWORD}@db:5432/${DB_NAME:-appdb}
      - REDIS_URL=redis://redis:6379/0
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - NEXTAUTH_URL=${NEXTAUTH_URL:-http://localhost:3000}
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/api/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: "${APP_CPU_LIMIT:-1.0}"
          memory: ${APP_MEMORY_LIMIT:-512M}
    networks:
      - frontend
      - backend
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    container_name: ${APP_NAME:-myapp}-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${DB_USER:-app}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME:-appdb}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app}"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
    networks:
      - backend

  redis:
    image: redis:7-alpine
    container_name: ${APP_NAME:-myapp}-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 128M
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true

volumes:
  postgres-data:
  redis-data:
```

### Go API Template

```yaml
# compose.yaml - Go API

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: ${REGISTRY:-localhost}/${APP_NAME:-myapp}:${VERSION:-latest}
    container_name: ${APP_NAME:-myapp}
    restart: unless-stopped
    user: "nonroot:nonroot"
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    ports:
      - "${APP_PORT:-8080}:8080"
    environment:
      - DATABASE_URL=postgres://${DB_USER:-app}:${DB_PASSWORD}@db:5432/${DB_NAME:-appdb}
      - REDIS_URL=redis://redis:6379/0
      - LOG_LEVEL=${LOG_LEVEL:-info}
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "/server", "-health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: "${APP_CPU_LIMIT:-0.5}"
          memory: ${APP_MEMORY_LIMIT:-128M}
    networks:
      - frontend
      - backend
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    container_name: ${APP_NAME:-myapp}-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${DB_USER:-app}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME:-appdb}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app}"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true

volumes:
  postgres-data:
```

---

## Override Templates

### Development Override

```yaml
# compose.override.yaml

services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules     # Exclude for Node.js
      - /app/.venv            # Exclude for Python
      - /app/vendor           # Exclude for Go
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    ports:
      - "${APP_PORT:-8000}:8000"
      - "9229:9229"           # Node.js debug
      - "2345:2345"           # Go debug (delve)

  worker:
    volumes:
      - .:/app
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug

  db:
    ports:
      - "${DB_PORT:-5432}:5432"

  redis:
    ports:
      - "${REDIS_PORT:-6379}:6379"

  mailhog:
    image: mailhog/mailhog
    container_name: ${APP_NAME:-myapp}-mailhog
    ports:
      - "1025:1025"
      - "8025:8025"
    networks:
      - backend
    profiles:
      - dev

  pgadmin:
    image: dpage/pgadmin4
    container_name: ${APP_NAME:-myapp}-pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "5050:80"
    networks:
      - backend
    profiles:
      - dev
```

### Production Override

```yaml
# compose.prod.yaml

services:
  app:
    image: ${REGISTRY}/${APP_NAME}:${VERSION}
    build: null  # Use pre-built image
    container_name: null  # Allow scaling
    restart: always
    deploy:
      mode: replicated
      replicas: ${APP_REPLICAS:-2}
      resources:
        limits:
          cpus: "2.0"
          memory: 1G
        reservations:
          cpus: "0.5"
          memory: 256M
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      rollback_config:
        parallelism: 1
        delay: 10s

  worker:
    image: ${REGISTRY}/${APP_NAME}:${VERSION}
    build: null
    restart: always
    deploy:
      replicas: ${WORKER_REPLICAS:-2}
      resources:
        limits:
          cpus: "1.0"
          memory: 512M

  db:
    restart: always
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G
        reservations:
          cpus: "0.5"
          memory: 512M

  redis:
    restart: always
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
```

### Test Override

```yaml
# compose.test.yaml

services:
  app:
    build:
      target: test
    command: pytest
    environment:
      - DATABASE_URL=postgres://test:test@db-test:5432/test
      - TESTING=true
    depends_on:
      db-test:
        condition: service_healthy

  db-test:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=test
      - POSTGRES_PASSWORD=test
      - POSTGRES_DB=test
    tmpfs:
      - /var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - backend
```

---

## Reverse Proxy Templates

### Nginx Reverse Proxy

```yaml
# compose.yaml

services:
  nginx:
    image: nginx:alpine
    container_name: ${APP_NAME:-myapp}-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
      - app-static:/var/www/static:ro
    depends_on:
      app:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 64M
    networks:
      - frontend

  app:
    # ... app configuration
    networks:
      - frontend
      - backend

networks:
  frontend:
  backend:
    internal: true

volumes:
  app-static:
```

### Nginx Configuration

```nginx
# nginx/nginx.conf

user nginx;
worker_processes auto;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    sendfile on;
    keepalive_timeout 65;
    gzip on;

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

### Traefik Reverse Proxy

```yaml
# compose.yaml

services:
  traefik:
    image: traefik:v3.0
    container_name: ${APP_NAME:-myapp}-traefik
    restart: unless-stopped
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik/certs:/certs:ro
    networks:
      - frontend

  app:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`app.localhost`)"
      - "traefik.http.routers.app.entrypoints=web"
      - "traefik.http.services.app.loadbalancer.server.port=8000"
    networks:
      - frontend
      - backend

networks:
  frontend:
  backend:
    internal: true
```

---

## Database Templates

### PostgreSQL with Init Scripts

```yaml
services:
  db:
    image: postgres:16-alpine
    container_name: ${APP_NAME:-myapp}-db
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
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G
    networks:
      - backend

volumes:
  postgres-data:
```

### MySQL

```yaml
services:
  db:
    image: mysql:8
    container_name: ${APP_NAME:-myapp}-db
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD}
      - MYSQL_USER=${DB_USER:-app}
      - MYSQL_PASSWORD=${DB_PASSWORD}
      - MYSQL_DATABASE=${DB_NAME:-appdb}
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G
    networks:
      - backend

volumes:
  mysql-data:
```

### MongoDB

```yaml
services:
  db:
    image: mongo:7
    container_name: ${APP_NAME:-myapp}-db
    restart: unless-stopped
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${DB_USER:-admin}
      - MONGO_INITDB_ROOT_PASSWORD=${DB_PASSWORD}
      - MONGO_INITDB_DATABASE=${DB_NAME:-appdb}
    volumes:
      - mongo-data:/data/db
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G
    networks:
      - backend

volumes:
  mongo-data:
```

---

## Environment Templates

### .env.example

```bash
# Application
APP_NAME=myapp
VERSION=1.0.0
SECRET_KEY=change-me-in-production
LOG_LEVEL=info
DEBUG=false

# Server
APP_PORT=8000
APP_CPU_LIMIT=1.0
APP_MEMORY_LIMIT=512M
APP_REPLICAS=2

# Database
DB_USER=app
DB_PASSWORD=secure-password-here
DB_NAME=appdb
DB_PORT=5432

# Redis
REDIS_PORT=6379

# Registry
REGISTRY=ghcr.io/org

# Auth (if applicable)
NEXTAUTH_SECRET=change-me
NEXTAUTH_URL=http://localhost:3000

# Feature Flags
ENABLE_FEATURE_X=false
```

### .dockerignore

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
vendor

# Build outputs
dist
build
target
.next

# IDE
.idea
.vscode
*.swp

# Testing
.coverage
htmlcov
.pytest_cache
coverage

# Environment
.env
.env.*
*.local

# Docker
Dockerfile*
docker-compose*
compose*.yaml
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

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs

# Temporary
tmp
temp
```

---

## Makefile Template

```makefile
# Makefile for Docker Compose operations

.PHONY: build up down logs shell test lint

# Variables
COMPOSE := docker compose
APP_NAME := myapp
VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")

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

up-prod:
	$(COMPOSE) -f compose.yaml -f compose.prod.yaml up -d

down:
	$(COMPOSE) down

down-v:
	$(COMPOSE) down -v

# Logs
logs:
	$(COMPOSE) logs -f

logs-app:
	$(COMPOSE) logs -f app

# Shell
shell:
	$(COMPOSE) exec app sh

shell-db:
	$(COMPOSE) exec db psql -U app -d appdb

# Testing
test:
	$(COMPOSE) -f compose.yaml -f compose.test.yaml run --rm app pytest

# Validation
config:
	$(COMPOSE) config --quiet && echo "Config valid"

lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

# Scaling
scale:
	$(COMPOSE) up -d --scale app=3

# Cleanup
prune:
	docker system prune -af --volumes

# Status
ps:
	$(COMPOSE) ps

stats:
	docker stats --no-stream
```

---

*Docker Compose Templates | faion-infrastructure-engineer*
