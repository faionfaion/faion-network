# Docker Optimization

**Image size, layer caching, and performance optimization**

---

## Layer Caching Strategy

```dockerfile
# BAD: Invalidates cache on any code change
COPY . .
RUN pip install -r requirements.txt

# GOOD: Dependencies cached separately
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

**Principle:** Order instructions from least to most frequently changing.

---

## Reducing Image Size

| Technique | Example | Impact |
|-----------|---------|--------|
| **Use slim/alpine** | `python:3.12-slim` vs `python:3.12` | -80% |
| **Multi-stage builds** | Separate build/runtime | -50-90% |
| **Remove cache** | `rm -rf /var/lib/apt/lists/*` | -50MB |
| **Combine RUN** | Multiple commands in one RUN | -5-10% |
| **Use .dockerignore** | Exclude unnecessary files | Variable |
| **No dev dependencies** | `npm ci --omit=dev` | -30-50% |

---

## Combine RUN Commands

```dockerfile
# BAD: Creates multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# GOOD: Single layer
RUN apt-get update && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

---

## Remove Package Manager Cache

### apt (Debian/Ubuntu)

```dockerfile
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

### apk (Alpine)

```dockerfile
RUN apk add --no-cache package1 package2
```

### yum (CentOS/RHEL)

```dockerfile
RUN yum install -y package1 package2 \
    && yum clean all
```

### pip (Python)

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

### npm (Node.js)

```dockerfile
ENV NPM_CONFIG_CACHE=/tmp/.npm
RUN npm ci --omit=dev
```

---

## Analyzing Image Size

```bash
# View image layers
docker history myapp:latest

# Detailed size analysis
docker image inspect myapp:latest --format='{{.Size}}'

# Use dive for deep analysis
dive myapp:latest

# Compare images
docker images --filter "reference=myapp" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

---

## .dockerignore Optimization

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

---

## BuildKit Optimizations

### Enable BuildKit

```bash
# Enable globally
export DOCKER_BUILDKIT=1

# Or per-build
DOCKER_BUILDKIT=1 docker build -t myapp .
```

### BuildKit Features

```dockerfile
# syntax=docker/dockerfile:1.4

# Mount cache for package managers
FROM python:3.12-slim
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Mount secrets (not in final image)
RUN --mount=type=secret,id=github_token \
    git clone https://$(cat /run/secrets/github_token)@github.com/repo.git

# Parallel builds
FROM node:20-alpine AS deps
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS build
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build
```

---

## Cache Mounts for Package Managers

### Python (pip)

```dockerfile
# syntax=docker/dockerfile:1.4
FROM python:3.12-slim

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

### Node.js (npm)

```dockerfile
# syntax=docker/dockerfile:1.4
FROM node:20-alpine

RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

### Go

```dockerfile
# syntax=docker/dockerfile:1.4
FROM golang:1.22-alpine

RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
```

---

## Multi-stage Build Best Practices

### 1. Minimize Runtime Image

```dockerfile
# Include only what's needed to run
FROM python:3.12-slim AS runtime

# No build tools
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
```

### 2. Use Specific Stages

```dockerfile
# Build for specific stage
docker build --target builder -t myapp:builder .
docker build --target runtime -t myapp:runtime .
```

### 3. Share Common Base

```dockerfile
# Base stage (shared)
FROM node:20-alpine AS base
WORKDIR /app

# Dependencies stage
FROM base AS deps
COPY package*.json ./
RUN npm ci

# Build stage
FROM deps AS builder
COPY . .
RUN npm run build

# Runtime stage
FROM base AS runtime
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
```

---

## Performance Tips

### 1. Order Layers by Change Frequency

```dockerfile
# Rarely changes → early in Dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y libpq-dev

# Sometimes changes
COPY requirements.txt .
RUN pip install -r requirements.txt

# Frequently changes → late in Dockerfile
COPY . .
```

### 2. Parallel Builds

```dockerfile
# syntax=docker/dockerfile:1.4

# Dependencies install in parallel stages
FROM base AS deps-python
RUN pip install -r requirements.txt

FROM base AS deps-node
RUN npm ci

# Combine in final stage
FROM base AS runtime
COPY --from=deps-python /opt/venv /opt/venv
COPY --from=deps-node /app/node_modules /app/node_modules
```

### 3. Use BuildKit's --mount

```dockerfile
# syntax=docker/dockerfile:1.4

# Bind mount (doesn't copy into image)
RUN --mount=type=bind,source=.,target=/src \
    cp /src/config.json /app/

# Cache mount (persists across builds)
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y package
```

---

## Size Comparison Examples

### Before Optimization

```dockerfile
FROM python:3.12
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

**Size:** ~950 MB

### After Optimization

```dockerfile
# syntax=docker/dockerfile:1.4
FROM python:3.12-slim AS builder
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
USER nobody
CMD ["python", "app.py"]
```

**Size:** ~180 MB (80% reduction)

---

## Tools for Optimization

| Tool | Purpose | Command |
|------|---------|---------|
| **Dive** | Layer analysis | `dive myapp:latest` |
| **Hadolint** | Dockerfile linting | `hadolint Dockerfile` |
| **docker history** | View layer sizes | `docker history myapp:latest` |
| **docker scout** | Vulnerability scanning | `docker scout cves myapp:latest` |

---

## Optimization Checklist

- [ ] Use slim/alpine base images
- [ ] Multi-stage builds implemented
- [ ] .dockerignore configured
- [ ] Package manager caches removed
- [ ] RUN commands combined
- [ ] Dependencies cached before code copy
- [ ] BuildKit enabled
- [ ] Cache mounts used for package managers
- [ ] Non-root user configured
- [ ] Image size < 200MB (if possible)

## Sources

- [Docker Build Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [BuildKit Documentation](https://docs.docker.com/build/buildkit/)
- [Dive Tool (GitHub)](https://github.com/wagoodman/dive)
- [Hadolint Linter](https://github.com/hadolint/hadolint)
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
