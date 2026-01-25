# Dockerfile Patterns

**Multi-stage builds and language-specific patterns**

---

## Multi-stage Build Fundamentals

### Basic Pattern

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Result:** Build tools not in final image, reduced size by ~90%.

---

## Python Multi-stage

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
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

---

## Go Multi-stage (CGO disabled)

```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server

# Stage 2: Runtime (scratch = empty image)
FROM scratch

COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080

ENTRYPOINT ["/server"]
```

**Result:** Final image ~10-20MB.

---

## Node.js Multi-stage

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

USER nextjs

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

---

## TypeScript Multi-stage

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

USER nextjs

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

---

## Security Best Practices

### Run as Non-root User

```dockerfile
# Create user
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser

# Copy files with correct ownership
COPY --chown=appuser:appuser . .

# Switch to user
USER appuser
```

---

## Security Scanning

```bash
# Scan with Docker Scout
docker scout cves myapp:latest

# Scan with Trivy
trivy image myapp:latest

# Scan with Snyk
snyk container test myapp:latest
```

---

## Security Checklist

- [ ] Use specific image tags (not `latest` in production)
- [ ] Run as non-root user
- [ ] Use read-only filesystem where possible
- [ ] Drop all capabilities: `--cap-drop ALL`
- [ ] Add only needed capabilities: `--cap-add NET_BIND_SERVICE`
- [ ] Scan images for vulnerabilities
- [ ] Use secrets for sensitive data (not ENV)
- [ ] Set resource limits
- [ ] Use distroless/minimal base images
- [ ] Keep images updated

---

## Dockerfile Checklist

- [ ] Base image version pinned
- [ ] Non-root user configured
- [ ] .dockerignore present
- [ ] Multi-stage build (if applicable)
- [ ] Layer caching optimized
- [ ] HEALTHCHECK defined
- [ ] Labels for metadata
- [ ] Exec form for CMD/ENTRYPOINT

---

## .dockerignore

```dockerignore
# Git
.git
.gitignore

# Dependencies
node_modules
venv
__pycache__
*.pyc

# Build artifacts
dist
build
*.egg-info

# IDE
.vscode
.idea
*.swp

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
.pytest_cache
.coverage

# Documentation
docs
*.md
!README.md

# Misc
*.log
tmp
temp
```

## Sources

- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Build Best Practices](https://docs.docker.com/build/building/best-practices/)
- [Multi-stage Build Patterns](https://docs.docker.com/build/building/multi-stage/)
- [BuildKit Features](https://docs.docker.com/build/buildkit/)
- [Dockerfile Linting with Hadolint](https://github.com/hadolint/hadolint)
