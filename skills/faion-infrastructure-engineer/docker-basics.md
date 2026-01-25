# Docker Basics

**Container fundamentals, commands, and best practices**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Dockerfile** | FROM, RUN, COPY, WORKDIR, ENV, CMD, ENTRYPOINT |
| **Security** | Non-root users, secrets, scanning |
| **Networking** | Bridge, host, overlay, custom networks |
| **Volumes** | Named volumes, bind mounts, tmpfs |
| **Registry** | Push, pull, tagging, private registries |

---

## Core Principles

### 1. Build Once, Run Anywhere

```
Source Code
    |
    v
Dockerfile --> docker build --> Image --> docker run --> Container
                                   |
                                   v
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

---

## Base Image Selection

| Image Type | Example | Size | Use Case |
|------------|---------|------|----------|
| **Full** | `python:3.12` | ~900MB | Development, debugging |
| **Slim** | `python:3.12-slim` | ~150MB | Production balance |
| **Alpine** | `python:3.12-alpine` | ~50MB | Minimal size |
| **Distroless** | `gcr.io/distroless/python3` | ~30MB | Maximum security |

**Recommendation:** Start with `-slim`, move to Alpine/Distroless for production.

---

## Essential Dockerfile Instructions

```dockerfile
# Base image - always pin version
FROM python:3.12-slim

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
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Expose port (documentation only)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Entry point and command
ENTRYPOINT ["python"]
CMD ["app.py"]
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

---

## Shell Form vs Exec Form

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

## Common Commands

### Build

```bash
# Build image
docker build -t myapp:latest .

# Build with different Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build with build args
docker build --build-arg VERSION=1.0.0 -t myapp:1.0.0 .

# Build without cache
docker build --no-cache -t myapp:latest .

# Build with target stage
docker build --target builder -t myapp:builder .
```

### Run

```bash
# Run interactive
docker run -it --rm myapp:latest bash

# Run detached
docker run -d --name myapp myapp:latest

# Run with environment
docker run -e DATABASE_URL=postgres://... myapp

# Run with port mapping
docker run -p 8080:80 myapp

# Run with volume
docker run -v $(pwd)/data:/app/data myapp

# Run with resource limits
docker run --memory=512m --cpus=0.5 myapp
```

### Maintenance

```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View logs
docker logs -f container_name

# Execute in container
docker exec -it container_name bash

# Copy files
docker cp container_name:/app/file.txt ./file.txt

# Prune unused resources
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
| **macvlan** | Container with MAC address | `docker network create -d macvlan ...` |

### Custom Bridge Network

```bash
# Create network
docker network create --driver bridge \
    --subnet=172.20.0.0/16 \
    --gateway=172.20.0.1 \
    app-network

# Run container on network
docker run -d --name app --network app-network myapp

# Connect running container
docker network connect app-network existing-container

# Inspect network
docker network inspect app-network
```

### Port Mapping

```bash
# Map container port to host
docker run -p 8080:80 nginx          # host:container
docker run -p 127.0.0.1:8080:80 nginx  # bind to localhost only
docker run -p 8080-8090:80-90 nginx    # port range
docker run -P nginx                    # auto-map EXPOSE ports
```

---

## Volume Management

### Volume Types

| Type | Syntax | Use Case |
|------|--------|----------|
| **Named volume** | `mydata:/app/data` | Persistent data |
| **Bind mount** | `./src:/app/src` | Development, configs |
| **tmpfs** | `--tmpfs /tmp` | Temporary, sensitive data |

### Named Volumes

```bash
# Create volume
docker volume create app-data

# Use in container
docker run -v app-data:/app/data myapp

# Inspect volume
docker volume inspect app-data

# Backup volume
docker run --rm -v app-data:/data -v $(pwd):/backup alpine \
    tar czf /backup/backup.tar.gz -C /data .

# Restore volume
docker run --rm -v app-data:/data -v $(pwd):/backup alpine \
    tar xzf /backup/backup.tar.gz -C /data
```

### Volume Best Practices

1. **Use named volumes for persistent data** (databases, uploads)
2. **Use bind mounts for development** (source code, configs)
3. **Use read-only where possible** (`:ro` flag)
4. **Backup volumes regularly**
5. **Clean unused volumes:** `docker volume prune`

---

## Registry Operations

### Docker Hub

```bash
# Login
docker login

# Tag image
docker tag myapp:latest username/myapp:v1.0.0

# Push to registry
docker push username/myapp:v1.0.0

# Pull from registry
docker pull username/myapp:v1.0.0
```

### Private Registry

```bash
# Run local registry
docker run -d -p 5000:5000 --name registry registry:2

# Tag for private registry
docker tag myapp:latest localhost:5000/myapp:v1.0.0

# Push to private registry
docker push localhost:5000/myapp:v1.0.0

# Pull from private registry
docker pull localhost:5000/myapp:v1.0.0
```

### AWS ECR

```bash
# Get login token
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Tag for ECR
docker tag myapp:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:v1.0.0

# Push to ECR
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:v1.0.0
```

### Image Tagging Strategy

| Tag | Purpose | Example |
|-----|---------|---------|
| `latest` | Most recent build | `myapp:latest` |
| Semantic version | Release version | `myapp:1.2.3` |
| Git SHA | Specific commit | `myapp:abc1234` |
| Branch | Feature branches | `myapp:feature-login` |
| Date | Build timestamp | `myapp:2026-01-18` |

**Recommended:** Use semantic versioning + git SHA for production.

```bash
# Tag with multiple tags
docker build -t myapp:latest \
             -t myapp:v1.2.3 \
             -t myapp:$(git rev-parse --short HEAD) \
             .
```

---

## Health Checks

### Dockerfile HEALTHCHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Health Check Options

| Option | Description |
|--------|-------------|
| `--interval` | Time between checks (default: 30s) |
| `--timeout` | Maximum time to wait for check (default: 30s) |
| `--start-period` | Grace period for container startup |
| `--retries` | Consecutive failures before unhealthy |

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

# Run shell in build stage
docker run -it --rm myapp:debug sh
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
| [Lazydocker](https://github.com/jesseduffield/lazydocker) | Terminal UI for Docker |

## Sources

- [Docker Official Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
