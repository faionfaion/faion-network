# Docker Optimization Examples

## Python (FastAPI/Django)

### Before Optimization (~950 MB)

```dockerfile
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

### After Optimization (~180 MB, -81%)

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy only Python packages
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY . .

# Security: non-root user
RUN useradd -r -s /bin/false appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Node.js (Next.js)

### Before Optimization (~1.2 GB)

```dockerfile
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
CMD ["npm", "start"]
```

### After Optimization (~150 MB, -87%)

```dockerfile
# syntax=docker/dockerfile:1.7

# Dependencies stage
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Security: non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy only necessary files
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
```

---

## Go (Microservice)

### Before Optimization (~800 MB)

```dockerfile
FROM golang:1.22
WORKDIR /app
COPY . .
RUN go build -o main .
CMD ["./main"]
```

### After Optimization (~12 MB, -98%)

```dockerfile
# syntax=docker/dockerfile:1.7

# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Cache dependencies
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Build with optimizations
COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o main .

# Runtime stage - scratch (smallest possible)
FROM scratch

# Copy binary
COPY --from=builder /app/main /main

# Copy CA certificates for HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Security: non-root (numeric UID for scratch)
USER 65534

EXPOSE 8080
ENTRYPOINT ["/main"]
```

### Alternative: Distroless (~15 MB)

```dockerfile
FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/main /main

USER nonroot:nonroot

ENTRYPOINT ["/main"]
```

---

## Rust (Microservice)

### Optimized (~20 MB)

```dockerfile
# syntax=docker/dockerfile:1.7

# Build stage
FROM rust:1.75-slim AS builder

WORKDIR /app

# Cache dependencies
RUN cargo new --bin app
WORKDIR /app/app
COPY Cargo.toml Cargo.lock ./
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    cargo build --release && rm -rf src

# Build application
COPY src ./src
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/app/target \
    cargo build --release && cp target/release/app /app/binary

# Runtime stage
FROM gcr.io/distroless/cc-debian12

COPY --from=builder /app/binary /app

USER nonroot:nonroot

ENTRYPOINT ["/app"]
```

---

## Java (Spring Boot)

### Before Optimization (~600 MB)

```dockerfile
FROM openjdk:21
COPY target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### After Optimization (~200 MB, -67%)

```dockerfile
# syntax=docker/dockerfile:1.7

# Build stage
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

# Copy build files
COPY mvnw pom.xml ./
COPY .mvn .mvn
COPY src src

# Build with layer extraction
RUN --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    java -Djarmode=layertools -jar target/*.jar extract

# Runtime stage
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy layers (ordered by change frequency)
COPY --from=builder /app/dependencies/ ./
COPY --from=builder /app/spring-boot-loader/ ./
COPY --from=builder /app/snapshot-dependencies/ ./
COPY --from=builder /app/application/ ./

# Security
RUN addgroup --system javauser && adduser --system --ingroup javauser javauser
USER javauser

EXPOSE 8080
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
```

---

## Nginx (Static Site)

### Optimized (~25 MB)

```dockerfile
# syntax=docker/dockerfile:1.7

# Build stage (if using build tools)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Custom nginx config (optional)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Security: non-root
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid

USER nginx

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Multi-Language (Python + Node.js)

### Parallel Build (~250 MB)

```dockerfile
# syntax=docker/dockerfile:1.7

# Python dependencies (parallel)
FROM python:3.12-slim AS python-deps
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# Node dependencies (parallel)
FROM node:20-alpine AS node-deps
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Build frontend (depends on node-deps)
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY --from=node-deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Final runtime
FROM python:3.12-slim

WORKDIR /app

# Python packages
COPY --from=python-deps /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Static files from frontend build
COPY --from=frontend-builder /app/dist ./static

# Application code
COPY . .

USER nobody
EXPOSE 8000
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8000"]
```

---

## .dockerignore (Universal)

```dockerignore
# Git
.git
.gitignore
.gitattributes

# Dependencies (rebuilt in container)
node_modules
venv
.venv
__pycache__
*.pyc
*.pyo
vendor

# Build artifacts
dist
build
*.egg-info
target
*.jar
*.war

# IDE and editors
.vscode
.idea
*.swp
*.swo
.DS_Store

# Docker
Dockerfile*
docker-compose*
.docker
.dockerignore

# Environment and secrets
.env
.env.*
*.local
.secrets
credentials.json

# Testing
tests
test
coverage
.coverage
.pytest_cache
.nyc_output
*.test.js
*.spec.js

# Documentation
docs
*.md
!README.md
LICENSE

# CI/CD
.github
.gitlab-ci.yml
.travis.yml
Jenkinsfile

# Logs and temp
*.log
logs
tmp
temp
*.tmp
```

---

*Docker Optimization Examples | faion-cicd-engineer*
