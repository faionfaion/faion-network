# Docker Operations Mastery

**Container Development and Deployment Best Practices (2025-2026)**

## Overview

This folder contains comprehensive Docker documentation organized by purpose.

| File | Purpose |
|------|---------|
| [README.md](README.md) | Core concepts, principles, quick reference |
| [checklist.md](checklist.md) | Dockerfile, security, production checklists |
| [examples.md](examples.md) | Multi-stage builds, Compose configurations |
| [templates.md](templates.md) | Ready-to-use Dockerfile and Compose templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for Docker-related tasks |

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Dockerfile** | FROM, RUN, COPY, WORKDIR, ENV, CMD, ENTRYPOINT |
| **Multi-stage** | Builder pattern, minimal runtime images |
| **Compose** | Services, networks, volumes, dependencies |
| **Optimization** | Layer caching, image size, build time |
| **Security** | Non-root users, secrets, scanning |
| **Networking** | Bridge, host, overlay, custom networks |
| **Volumes** | Named volumes, bind mounts, tmpfs |
| **Registry** | Push, pull, tagging, private registries |

---

## Core Principles

### 1. Build Once, Run Anywhere

```
Source Code → Dockerfile → docker build → Image → docker run → Container
                                            ↓
                                       Registry (push/pull)
```

### 2. Image Layering

Docker images are built in layers. Each instruction creates a new layer.

```
Layer 4: CMD ["python", "app.py"]     (0 MB)
Layer 3: COPY . /app                  (50 MB)
Layer 2: RUN pip install -r req.txt   (200 MB)
Layer 1: FROM python:3.12-slim        (150 MB)
```

**Rule:** Order instructions from least to most frequently changing for optimal caching.

### 3. Layer Caching Strategy (2025-2026)

Understanding how the build cache works is critical for faster builds:
- Docker caches every layer in a Dockerfile
- Changes in a step invalidate cache for all subsequent steps
- Place frequently changed files at the end of the Dockerfile

```dockerfile
# BAD: Invalidates cache on any code change
COPY . .
RUN pip install -r requirements.txt

# GOOD: Dependencies cached separately
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

---

## Base Image Selection

| Image Type | Example | Size | Use Case |
|------------|---------|------|----------|
| **Full** | `python:3.12` | ~900MB | Development, debugging |
| **Slim** | `python:3.12-slim` | ~150MB | Production balance |
| **Alpine** | `python:3.12-alpine` | ~50MB | Minimal size |
| **Distroless** | `gcr.io/distroless/python3` | ~30MB | Maximum security |

**Recommendation:** Start with `-slim`, move to Alpine/Distroless for production.

**2025-2026 Update:** Alpine or minimal variants significantly reduce image sizes and associated security issues. For example, a Python application using `ubuntu:latest` could be several hundred MB, while Alpine could be less than 50 MB.

---

## Essential Instructions

### CMD vs ENTRYPOINT

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

### Shell Form vs Exec Form

```dockerfile
# Exec form (recommended) - runs directly
CMD ["python", "app.py"]
ENTRYPOINT ["./entrypoint.sh"]

# Shell form - runs via /bin/sh -c
CMD python app.py
ENTRYPOINT ./entrypoint.sh  # Cannot receive signals properly
```

**Always use exec form** for proper signal handling.

---

## Image Optimization (2025-2026)

### Reducing Image Size

| Technique | Example | Impact |
|-----------|---------|--------|
| **Use slim/alpine** | `python:3.12-slim` vs `python:3.12` | -80% |
| **Multi-stage builds** | Separate build/runtime | -50-90% |
| **Remove cache** | `rm -rf /var/lib/apt/lists/*` | -50MB |
| **Combine RUN** | Multiple commands in one RUN | -5-10% |
| **Use .dockerignore** | Exclude unnecessary files | Variable |
| **No dev dependencies** | `npm ci --omit=dev` | -30-50% |
| **--no-cache-dir** | `pip install --no-cache-dir` | -10-30% |

### BuildKit Features (2025-2026)

Enable BuildKit for advanced features:

```bash
export DOCKER_BUILDKIT=1
```

- **Cache mounts:** `--mount=type=cache` for faster builds
- **Layer compression:** Docker 25.x automatic compression optimization
- **Parallel builds:** Faster multi-stage execution

---

## Container Networking

### Network Types

| Type | Use Case | Command |
|------|----------|---------|
| **bridge** (default) | Container-to-container on same host | `docker network create mynet` |
| **host** | Container uses host network | `--network host` |
| **none** | No networking | `--network none` |
| **overlay** | Multi-host communication (Swarm) | `docker network create -d overlay mynet` |
| **macvlan** | Container with MAC address | `docker network create -d macvlan ...` |

### DNS and Service Discovery

Containers on the same network can reach each other by service name:

```
postgres://db:5432/mydb
http://api:8000/health
```

---

## Volume Management

### Volume Types

| Type | Syntax | Use Case |
|------|--------|----------|
| **Named volume** | `mydata:/app/data` | Persistent data |
| **Bind mount** | `./src:/app/src` | Development, configs |
| **tmpfs** | `--tmpfs /tmp` | Temporary, sensitive data |

### Best Practices

1. **Use named volumes for persistent data** (databases, uploads)
2. **Use bind mounts for development** (source code, configs)
3. **Use read-only where possible** (`:ro` flag)
4. **Backup volumes regularly**
5. **Clean unused volumes:** `docker volume prune`

---

## Health Checks

### Dockerfile HEALTHCHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Options

| Option | Description |
|--------|-------------|
| `--interval` | Time between checks (default: 30s) |
| `--timeout` | Maximum time to wait for check (default: 30s) |
| `--start-period` | Grace period for container startup |
| `--retries` | Consecutive failures before unhealthy |

---

## Common Commands

### Build

```bash
docker build -t myapp:latest .                    # Build image
docker build -f Dockerfile.prod -t myapp:prod .   # Different Dockerfile
docker build --build-arg VERSION=1.0.0 -t myapp . # With build args
docker build --no-cache -t myapp:latest .         # Without cache
docker build --target builder -t myapp:builder .  # Specific stage
docker build --progress=plain -t myapp .          # Verbose output
```

### Run

```bash
docker run -it --rm myapp:latest bash        # Interactive
docker run -d --name myapp myapp:latest      # Detached
docker run -e DATABASE_URL=postgres://... myapp  # With environment
docker run -p 8080:80 myapp                  # Port mapping
docker run -v $(pwd)/data:/app/data myapp    # With volume
docker run --memory=512m --cpus=0.5 myapp    # Resource limits
```

### Compose

```bash
docker compose up -d                 # Start services
docker compose up -d --build         # Build and start
docker compose logs -f app           # View logs
docker compose down                  # Stop services
docker compose down -v               # Stop and remove volumes
docker compose exec app bash         # Execute in service
docker compose up -d --scale app=3   # Scale service
```

### Maintenance

```bash
docker ps                              # Running containers
docker ps -a                           # All containers
docker logs -f container_name          # Follow logs
docker exec -it container_name bash    # Execute in container
docker cp container:/app/file.txt ./   # Copy files
docker system prune -a --volumes       # Prune all
docker history myapp:latest            # View layers
docker stats                           # Resource usage
```

---

## Analyzing Images

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

## Image Tagging Strategy

| Tag | Purpose | Example |
|-----|---------|---------|
| `latest` | Most recent build | `myapp:latest` |
| Semantic version | Release version | `myapp:1.2.3` |
| Git SHA | Specific commit | `myapp:abc1234` |
| Branch | Feature branches | `myapp:feature-login` |
| Date | Build timestamp | `myapp:2026-01-26` |

**Recommended:** Use semantic versioning + git SHA for production.

```bash
docker build -t myapp:latest \
             -t myapp:v1.2.3 \
             -t myapp:$(git rev-parse --short HEAD) \
             .
```

---

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Using `latest` tag | Unpredictable deployments | Pin specific versions |
| Root user | Security vulnerability | Create non-root user |
| Secrets in ENV | Visible in inspect/logs | Use Docker secrets |
| Large images | Slow deploys, more vulnerabilities | Multi-stage builds |
| Ignoring .dockerignore | Large context, slow builds | Proper exclusions |
| Not using health checks | Silent failures | Add HEALTHCHECK |
| Hardcoding config | Inflexible containers | Use ENV/secrets |
| Single RUN per line | Many layers, large image | Combine RUN commands |

---

## Tools

| Tool | Purpose |
|------|---------|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | GUI for Docker management |
| [Docker Scout](https://docs.docker.com/scout/) | Vulnerability scanning |
| [Dive](https://github.com/wagoodman/dive) | Image layer analysis |
| [Hadolint](https://github.com/hadolint/hadolint) | Dockerfile linting |
| [Trivy](https://github.com/aquasecurity/trivy) | Security scanning |
| [Buildx](https://github.com/docker/buildx) | Multi-platform builds |
| [Docker Compose](https://docs.docker.com/compose/) | Multi-container orchestration |
| [Lazydocker](https://github.com/jesseduffield/lazydocker) | Terminal UI for Docker |

---

## Sources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/build/building/best-practices/)
- [Docker Compose Specification](https://docs.docker.com/compose/compose-file/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Hadolint Rules](https://github.com/hadolint/hadolint#rules)
- [Docker Best Practices 2026 - Thinksys](https://thinksys.com/devops/docker-best-practices/)
- [Modern Docker Best Practices 2025 - Talent500](https://talent500.com/blog/modern-docker-best-practices-2025/)
- [Multi-stage builds - Docker Docs](https://docs.docker.com/build/building/multi-stage/)
