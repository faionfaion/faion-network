# Docker Examples

Production-ready examples for multi-stage builds, Docker Compose, and common patterns.

---

## Multi-Stage Build Examples

### Python (Django/FastAPI)

```dockerfile
# Stage 1: Build dependencies
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

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

### Node.js (TypeScript)

```dockerfile
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

# Stage 3: Production dependencies
FROM node:20-alpine AS prod-deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

# Stage 4: Runtime
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs

COPY --from=builder /app/dist ./dist
COPY --from=prod-deps /app/node_modules ./node_modules
COPY package.json ./

USER nextjs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

### Next.js (Standalone)

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Stage 3: Runner
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
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
```

### Go (CGO Disabled)

```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server ./cmd/server

# Stage 2: Runtime (scratch = empty image)
FROM scratch

COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080

ENTRYPOINT ["/server"]
```

### Go (With CGO - Distroless)

```dockerfile
# Stage 1: Build
FROM golang:1.22 AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -ldflags="-w -s" -o /app/server ./cmd/server

# Stage 2: Runtime
FROM gcr.io/distroless/base-debian12

COPY --from=builder /app/server /server

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/server"]
```

### Rust

```dockerfile
# Stage 1: Build
FROM rust:1.75 AS builder

WORKDIR /app

# Build dependencies first (cache layer)
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release && rm -rf src

# Build application
COPY src ./src
RUN touch src/main.rs && cargo build --release

# Stage 2: Runtime
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home appuser

COPY --from=builder /app/target/release/myapp /usr/local/bin/

USER appuser

EXPOSE 8080

CMD ["myapp"]
```

---

## Docker Compose Examples

### Full Stack (Python + Postgres + Redis)

```yaml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
    image: myapp:latest
    container_name: myapp
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./uploads:/app/uploads
    networks:
      - app-network
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
        reservations:
          cpus: "0.25"
          memory: 128M

  db:
    image: postgres:16-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:alpine
    container_name: myapp-nginx
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
      - app-network

volumes:
  db_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

### Development Override

```yaml
# docker-compose.override.yml (auto-loaded in development)
version: "3.9"

services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/.venv  # Preserve venv
    ports:
      - "8000:8000"
      - "5678:5678"  # Debugger
    environment:
      - DEBUG=true
      - PYTHONDONTWRITEBYTECODE=1
    command: ["python", "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]

  db:
    ports:
      - "5432:5432"

  redis:
    ports:
      - "6379:6379"
```

### Production Override

```yaml
# docker-compose.prod.yml
version: "3.9"

services:
  app:
    build:
      target: production
    restart: always
    environment:
      - DEBUG=false
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

  db:
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

  nginx:
    deploy:
      replicas: 2

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### With Service Dependencies (Migrations)

```yaml
version: "3.9"

services:
  app:
    build: .
    depends_on:
      migrations:
        condition: service_completed_successfully
      db:
        condition: service_healthy

  migrations:
    build: .
    command: ["python", "manage.py", "migrate"]
    depends_on:
      db:
        condition: service_healthy
    restart: "no"

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s
      timeout: 5s
      retries: 10
```

---

## .dockerignore Example

```dockerignore
# Git
.git
.gitignore

# Dependencies
node_modules
venv
.venv
__pycache__
*.pyc
*.pyo
.pytest_cache
.mypy_cache

# Build artifacts
dist
build
*.egg-info
.eggs
target

# IDE
.vscode
.idea
*.swp
*.swo
*~

# Docker
Dockerfile*
docker-compose*
.docker

# Environment
.env
.env.*
*.local

# Tests
tests
test
coverage
.coverage
htmlcov
.tox

# Documentation
docs
*.md
!README.md

# Misc
*.log
tmp
temp
.cache
.npm
.yarn

# OS
.DS_Store
Thumbs.db
```

---

## Entrypoint Script Example

```bash
#!/bin/bash
set -e

# Wait for database
if [ -n "$DATABASE_URL" ]; then
    echo "Waiting for database..."
    while ! pg_isready -h db -p 5432 -q; do
        sleep 1
    done
    echo "Database is ready!"
fi

# Run migrations (if not disabled)
if [ "$SKIP_MIGRATIONS" != "true" ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput
fi

# Collect static files (if Django)
if [ "$COLLECT_STATIC" = "true" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Execute the main command
exec "$@"
```

Dockerfile usage:

```dockerfile
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

---

## Secure Container Example

```yaml
services:
  app:
    image: myapp:v1.0.0
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    user: "1000:1000"
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
        reservations:
          cpus: "0.25"
          memory: 128M
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## Registry Operations Example

```bash
# Login to registries
docker login
docker login ghcr.io
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Build with multiple tags
docker build \
    -t myapp:latest \
    -t myapp:v1.2.3 \
    -t myapp:$(git rev-parse --short HEAD) \
    -t ghcr.io/org/myapp:v1.2.3 \
    .

# Push all tags
docker push myapp:latest
docker push myapp:v1.2.3
docker push ghcr.io/org/myapp:v1.2.3

# Multi-platform build
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t myapp:v1.2.3 \
    --push \
    .
```

---

## Volume Backup/Restore

```bash
# Backup volume
docker run --rm \
    -v myapp_data:/data:ro \
    -v $(pwd)/backups:/backup \
    alpine tar czf /backup/myapp_data_$(date +%Y%m%d).tar.gz -C /data .

# Restore volume
docker run --rm \
    -v myapp_data:/data \
    -v $(pwd)/backups:/backup:ro \
    alpine tar xzf /backup/myapp_data_20260126.tar.gz -C /data

# Database backup (PostgreSQL)
docker exec myapp-db pg_dump -U user -d mydb > backup.sql

# Database restore
cat backup.sql | docker exec -i myapp-db psql -U user -d mydb
```
