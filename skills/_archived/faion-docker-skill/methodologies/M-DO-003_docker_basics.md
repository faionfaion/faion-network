# M-DO-003: Docker Basics

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Beginner
- **Tags:** #devops, #docker, #containers, #methodology
- **Agent:** faion-devops-agent

---

## Problem

"It works on my machine" is a common developer excuse. Different environments cause bugs that are hard to reproduce. Deployment becomes environment-dependent.

## Promise

After this methodology, you will containerize applications with Docker. Your apps will run identically everywhere - development, CI, and production.

## Overview

Docker packages applications and dependencies into containers. Containers are lightweight, portable, and isolated from the host system.

---

## Framework

### Step 1: Docker Installation

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Log out and back in

# macOS
brew install --cask docker

# Verify
docker --version
docker run hello-world
```

### Step 2: Dockerfile Basics

```dockerfile
# Use official base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency files first (layer caching)
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build application
RUN npm run build

# Expose port
EXPOSE 3000

# Run command
CMD ["npm", "start"]
```

### Step 3: Multi-Stage Builds

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Copy only production dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy built assets
COPY --from=builder /app/dist ./dist

# Non-root user
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -D appuser
USER appuser

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Step 4: Docker Commands

```bash
# Build image
docker build -t myapp:latest .
docker build -t myapp:1.0.0 -f Dockerfile.prod .

# Run container
docker run -d --name myapp -p 3000:3000 myapp:latest
docker run -it --rm myapp:latest sh  # Interactive shell

# Container management
docker ps                     # Running containers
docker ps -a                  # All containers
docker logs myapp             # View logs
docker logs -f myapp          # Follow logs
docker exec -it myapp sh      # Execute command

# Stop and remove
docker stop myapp
docker rm myapp
docker rm -f myapp            # Force remove running

# Images
docker images                 # List images
docker rmi myapp:latest       # Remove image
docker image prune -a         # Remove unused images
```

### Step 5: Environment Variables

```dockerfile
# Define in Dockerfile
ENV NODE_ENV=production
ENV PORT=3000

# Use ARG for build-time
ARG VERSION=1.0.0
ENV APP_VERSION=$VERSION
```

```bash
# Pass at runtime
docker run -e DATABASE_URL=postgres://... myapp
docker run --env-file .env myapp

# .env file
DATABASE_URL=postgres://localhost:5432/db
REDIS_URL=redis://localhost:6379
API_KEY=secret
```

### Step 6: Volumes and Data

```bash
# Named volumes (managed by Docker)
docker volume create mydata
docker run -v mydata:/app/data myapp

# Bind mounts (host directory)
docker run -v $(pwd)/data:/app/data myapp
docker run -v $(pwd):/app myapp  # Development

# Read-only
docker run -v $(pwd)/config:/app/config:ro myapp
```

---

## Templates

### Node.js Production Dockerfile

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build
COPY . .
RUN npm run build

# Production image
FROM node:20-alpine

WORKDIR /app

# Security: non-root user
RUN addgroup -g 1001 nodejs && \
    adduser -u 1001 -G nodejs -D nodejs

# Production dependencies only
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

# Copy build
COPY --from=builder /app/dist ./dist

# Set ownership
RUN chown -R nodejs:nodejs /app

USER nodejs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

### Python Production Dockerfile

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app

# Install poetry
RUN pip install poetry

# Export requirements
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

# Production image
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Non-root user
RUN useradd -m -u 1000 appuser
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Go Production Dockerfile

```dockerfile
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/server

# Minimal production image
FROM scratch

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/server /server

EXPOSE 8080

ENTRYPOINT ["/server"]
```

### .dockerignore

```
# Git
.git
.gitignore

# Dependencies
node_modules
vendor
__pycache__

# Build outputs
dist
build
*.egg-info

# IDE
.idea
.vscode
*.swp

# Docker
Dockerfile*
docker-compose*
.dockerignore

# Environment
.env
.env.*
!.env.example

# Tests
coverage
.pytest_cache
.nyc_output

# Docs
README.md
docs
*.md
```

---

## Examples

### Development Dockerfile

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install nodemon for hot reload
RUN npm install -g nodemon

# Copy package files
COPY package*.json ./
RUN npm install

# Copy source (will be overwritten by volume mount)
COPY . .

EXPOSE 3000

CMD ["nodemon", "--watch", "src", "src/index.js"]
```

### Build and Push

```bash
# Build with tag
docker build -t myrepo/myapp:1.0.0 .

# Login to registry
docker login
# or
docker login ghcr.io

# Push
docker push myrepo/myapp:1.0.0

# Multi-platform build
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t myrepo/myapp:1.0.0 --push .
```

---

## Common Mistakes

1. **Using :latest in production** - Pin specific versions
2. **Running as root** - Add non-root USER
3. **Large images** - Use alpine, multi-stage builds
4. **No .dockerignore** - Include node_modules, .git
5. **Secrets in image** - Use runtime env vars or secrets

---

## Checklist

- [ ] Multi-stage build for production
- [ ] Alpine or slim base images
- [ ] Non-root user
- [ ] .dockerignore configured
- [ ] HEALTHCHECK defined
- [ ] Specific version tags
- [ ] Layer order optimized (deps first)
- [ ] No secrets in image

---

## Next Steps

- M-DO-004: Docker Compose
- M-DO-005: Kubernetes Basics
- M-DO-001: GitHub Actions

---

*Methodology M-DO-003 v1.0*
