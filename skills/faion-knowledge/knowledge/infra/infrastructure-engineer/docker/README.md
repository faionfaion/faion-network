# Docker Infrastructure

**Production-Grade Container Development and Deployment (2025-2026)**

---

## Overview

Docker containerization packages applications with dependencies into portable units. This skill covers production-grade Docker infrastructure: image building, optimization, networking, storage, security hardening, and deployment best practices.

---

## Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Production readiness and security checklists |
| [examples.md](examples.md) | Multi-stage builds, networking, storage patterns |
| [templates.md](templates.md) | Production Dockerfiles and compose configurations |
| [llm-prompts.md](llm-prompts.md) | AI prompts for Docker infrastructure tasks |

---

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Image** | Read-only template with app + dependencies |
| **Container** | Running instance of an image |
| **Layer** | Each Dockerfile instruction creates a layer |
| **Registry** | Image storage (Docker Hub, ECR, GCR, GHCR) |
| **Volume** | Persistent data outside container |
| **Network** | Container communication layer |

### Image vs Container

```
Image (Blueprint)          Container (Instance)
+------------------+       +------------------+
| Read-only        |       | Writable layer   |
| Shareable        |  ->   | Isolated process |
| Versioned        |       | Runtime state    |
+------------------+       +------------------+
```

---

## Image Selection Guide (2025-2026)

| Image Type | Example | Size | Security | Use Case |
|------------|---------|------|----------|----------|
| **Full** | `python:3.12` | ~900MB | Low | Development, debugging |
| **Slim** | `python:3.12-slim` | ~150MB | Medium | Production balance |
| **Alpine** | `python:3.12-alpine` | ~50MB | Medium | Minimal footprint |
| **Distroless** | `gcr.io/distroless/python3` | ~30MB | High | Maximum security |
| **Chainguard** | `cgr.dev/chainguard/python` | ~25MB | High | Supply chain security |

**2025-2026 Recommendation:** Start with `-slim` for development, move to Distroless or Chainguard for production.

---

## Key Principles (2025-2026)

### 1. Immutable Infrastructure

- Treat images as immutable artifacts
- Never modify running containers
- Rebuild rather than patch
- Tag images with semantic versions + git SHA

### 2. Layer Caching Optimization

Order instructions from least to most frequently changing:

```dockerfile
FROM python:3.12-slim        # Rarely changes
COPY requirements.txt .      # Sometimes changes
RUN pip install -r ...       # Sometimes changes
COPY . .                     # Frequently changes
```

### 3. Security by Default (Zero Trust)

- Run as non-root user (UID 1000+)
- Use read-only filesystems
- Scan images for vulnerabilities (Trivy, Scout)
- Never embed secrets in images
- Apply seccomp and AppArmor profiles
- Drop all capabilities, add only needed ones

### 4. Observability

- Add health checks (HEALTHCHECK)
- Configure structured logging (JSON)
- Set resource limits (memory, CPU)
- Expose metrics endpoint (Prometheus)

### 5. AI-Enhanced Operations (2026 Trend)

- AI-powered monitoring and anomaly detection
- Automated resource optimization
- Predictive scaling based on load patterns
- AI-assisted log analysis

---

## Production Best Practices (2025-2026)

### Image Building

| Practice | Description |
|----------|-------------|
| Pin versions | Use `python:3.12.1-slim@sha256:...`, not `python:latest` |
| Multi-stage builds | Separate build and runtime stages |
| BuildKit caching | Use `--mount=type=cache` for dependencies |
| Scan before push | Integrate Trivy/Scout in CI/CD |
| Sign images | Use Docker Content Trust or Cosign |
| Generate SBOM | Track software bill of materials |

### Networking

| Practice | Description |
|----------|-------------|
| Custom networks | Never use default bridge network |
| Internal networks | Mark backend networks as `internal: true` |
| No exposed DB ports | Database ports only via internal network |
| TLS everywhere | Encrypt all external traffic |
| Network segmentation | Isolate frontend, backend, database tiers |
| DNS names | Use container/service names, not IPs |

### Storage

| Practice | Description |
|----------|-------------|
| Named volumes | Use for persistent data (databases) |
| Read-only mounts | Use `:ro` for configs and secrets |
| tmpfs for temp data | Use `--tmpfs /tmp` for temporary files |
| Backup volumes | Regular backup of named volumes |
| No bind mounts in prod | Bind mounts only for development |
| Encryption at rest | Encrypt volumes with KMS/secrets |

### Security

| Practice | Description |
|----------|-------------|
| Non-root user | Always use `USER appuser` (UID 1000+) |
| Read-only root | Run with `--read-only` flag |
| Drop capabilities | `--cap-drop ALL`, add only needed |
| Seccomp profile | Use default or custom seccomp profile |
| AppArmor/SELinux | Apply mandatory access controls |
| Secrets management | Use Docker secrets or external vault |
| No privileged mode | Never use `--privileged` in production |
| Keep updated | Regular host and Docker updates |

---

## Modern Practices (2025-2026 Updates)

### Compose File Naming

```bash
# Old (deprecated)
docker-compose.yaml
docker-compose up

# New (modern)
compose.yaml
docker compose up
```

### Version Field

The `version:` field in compose files is obsolete. Start directly with `services:`.

### BuildKit Features

BuildKit is now default. Use advanced features:

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Mount cache for faster rebuilds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Mount secrets securely (not exposed in layer)
RUN --mount=type=secret,id=github_token \
    pip install git+https://$(cat /run/secrets/github_token)@github.com/...
```

### Docker Scout & Trivy

Built-in vulnerability scanning:

```bash
# Docker Scout (built-in)
docker scout cves myapp:latest
docker scout recommendations myapp:latest

# Trivy (comprehensive)
trivy image --severity HIGH,CRITICAL myapp:latest
```

---

## Essential Dockerfile Instructions

```dockerfile
# Base image - always pin version with digest
FROM python:3.12-slim@sha256:abc123...

# Labels for metadata
LABEL maintainer="team@example.com"
LABEL version="1.0.0"
LABEL description="Production API service"

# Set working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies (combine RUN commands)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser
USER appuser

# Expose port (documentation only)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Entry point and command (exec form)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:application"]
```

---

## CMD vs ENTRYPOINT

| Instruction | Purpose | Override |
|-------------|---------|----------|
| **ENTRYPOINT** | Defines executable | `--entrypoint` flag |
| **CMD** | Default arguments | Command line args |

```dockerfile
# Pattern 1: ENTRYPOINT for fixed command
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8000"]  # docker run myapp --port 9000

# Pattern 2: CMD for flexible command
CMD ["python", "app.py"]  # docker run myapp sh (replaces entirely)

# Pattern 3: Combined (recommended)
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "app:app"]
```

**Always use exec form** for proper signal handling.

---

## Quick Commands

```bash
# Build with BuildKit
DOCKER_BUILDKIT=1 docker build -t myapp:1.0.0 .

# Build with specific tag and SHA
docker build -t myapp:v1.2.3 -t myapp:$(git rev-parse --short HEAD) .

# Run with security hardening
docker run -d --name myapp \
    --user 1000:1000 \
    --read-only \
    --cap-drop ALL \
    --security-opt no-new-privileges:true \
    --memory=512m \
    --cpus=0.5 \
    --tmpfs /tmp \
    -p 8080:80 \
    myapp:1.0.0

# Compose
docker compose up -d
docker compose logs -f app
docker compose down

# Security scan
docker scout cves myapp:latest
trivy image --severity HIGH,CRITICAL myapp:latest

# Inspect
docker stats myapp
docker inspect myapp
docker exec -it myapp sh

# Clean up
docker system prune -a --volumes
```

---

## Container Networking

### Network Types

| Type | Use Case | Command |
|------|----------|---------|
| **bridge** (default) | Container-to-container on same host | `docker network create mynet` |
| **host** | Container uses host network | `--network host` |
| **none** | No networking | `--network none` |
| **overlay** | Multi-host communication (Swarm) | `docker network create -d overlay mynet` |

### Network Architecture

```
                    Internet
                        |
                   [Load Balancer]
                        |
            +-----------+-----------+
            |     Frontend Network   |
            |  (nginx, reverse proxy)|
            +-----------+-----------+
                        |
            +-----------+-----------+
            |    Application Network |
            |   (app, worker, api)   |
            +-----------+-----------+
                        |
            +-----------+-----------+
            |    Backend Network     |
            |  (internal: true)      |
            |  (db, redis, queue)    |
            +-----------+-----------+
```

---

## Volume Management

### Volume Types

| Type | Syntax | Use Case |
|------|--------|----------|
| **Named volume** | `mydata:/app/data` | Persistent data |
| **Bind mount** | `./src:/app/src` | Development, configs |
| **tmpfs** | `--tmpfs /tmp` | Temporary, sensitive data |

### Storage Architecture

```
Container Layer (ephemeral, read-only in prod)
    |
    +-- tmpfs: /tmp (temporary data)
    |
    +-- Named Volume: /app/data (persistent)
    |
    +-- Named Volume: /var/lib/postgresql/data (database)
    |
    +-- Bind Mount (dev only): ./src:/app/src
    |
    +-- Secret Mount: /run/secrets/* (secrets)
```

---

## Health Checks

### Health Check Options

| Option | Description |
|--------|-------------|
| `--interval` | Time between checks (default: 30s) |
| `--timeout` | Maximum time to wait for check (default: 30s) |
| `--start-period` | Grace period for container startup |
| `--retries` | Consecutive failures before unhealthy |

### Health Check Patterns

```dockerfile
# HTTP health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# TCP health check
HEALTHCHECK CMD nc -z localhost 8000 || exit 1

# Script health check
HEALTHCHECK CMD /app/healthcheck.sh
```

---

## Debugging

### Container Inspection

```bash
# Inspect container
docker inspect container_name

# View processes
docker top container_name

# Resource usage
docker stats container_name

# View logs with timestamps
docker logs --timestamps container_name

# Follow logs
docker logs -f --tail 100 container_name
```

### Network Debugging

```bash
# List networks
docker network ls

# Inspect network
docker network inspect bridge

# Test connectivity from container
docker exec -it app ping db
docker exec -it app nslookup db
```

### Build Debugging

```bash
# Build with verbose output
docker build --progress=plain -t myapp .

# Build specific stage
docker build --target builder -t myapp:debug .

# Analyze layers
dive myapp:latest
```

---

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Using `latest` tag | Unpredictable deployments | Pin specific versions with digest |
| Root user | Security vulnerability | Create non-root user (UID 1000+) |
| Secrets in ENV | Visible in inspect/logs | Use Docker secrets or vault |
| Large images | Slow deploys, more vulnerabilities | Multi-stage builds, distroless |
| Default bridge network | No isolation | Custom networks with segmentation |
| No health checks | Silent failures | Add HEALTHCHECK |
| Hardcoding config | Inflexible containers | Use ENV/secrets |
| Single RUN per line | Many layers, large image | Combine RUN commands |

---

## Tools (2025-2026)

| Tool | Purpose |
|------|---------|
| [Docker Scout](https://docs.docker.com/scout/) | Built-in vulnerability scanning |
| [Trivy](https://github.com/aquasecurity/trivy) | Comprehensive security scanner |
| [Cosign](https://github.com/sigstore/cosign) | Container signing and verification |
| [Hadolint](https://github.com/hadolint/hadolint) | Dockerfile linter |
| [Dive](https://github.com/wagoodman/dive) | Image layer analysis |
| [Dagger](https://dagger.io/) | Programmable CI/CD engine |
| [Lazydocker](https://github.com/jesseduffield/lazydocker) | Terminal UI |
| [Buildpacks](https://buildpacks.io/) | Auto-build images from source |

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Dockerfile optimization | sonnet | Layer optimization expertise |
| Base image selection | haiku | Straightforward choice |
| Multi-stage builds | sonnet | Pattern application |
| Build cache management | haiku | Mechanical configuration |

## Sources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Docker Compose Specification](https://docs.docker.com/compose/compose-file/)
- [Modern Docker Best Practices 2025](https://talent500.com/blog/modern-docker-best-practices-2025/)
- [Docker Best Practices 2026](https://thinksys.com/devops/docker-best-practices/)
- [Docker in 2026 Innovations](https://medium.com/devops-ai-decoded/docker-in-2026-top-10-must-see-innovations-and-best-practices-for-production-success-30a5e090e5d6)
- [Docker Security Best Practices](https://betterstack.com/community/guides/scaling-docker/docker-security-best-practices/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Container Security 2025](https://www.thesamurai.com/best-practices-for-container-security-in-2025/)
- [Docker Security in 2025](https://cloudnativenow.com/topics/cloudnativedevelopment/docker/docker-security-in-2025-best-practices-to-protect-your-containers-from-cyberthreats/)
- [GitGuardian Docker Security Cheat Sheet](https://blog.gitguardian.com/how-to-improve-your-docker-containers-security-cheat-sheet/)

---

*Docker Infrastructure | faion-infrastructure-engineer*
