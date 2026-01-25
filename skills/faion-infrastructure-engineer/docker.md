---
name: faion-docker-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(docker:*, docker-compose:*)
---

# Docker Operations

**Container Development and Deployment Best Practices**

---

## Overview

Docker documentation is split into focused topic files. Use this index to navigate.

---

## Topic Files

| File | Topics Covered | Size |
|------|----------------|------|
| **[docker-basics.md](docker-basics.md)** | Dockerfile instructions, commands, networking, volumes, registry | ~1000 lines |
| **[dockerfile-patterns.md](dockerfile-patterns.md)** | Multi-stage builds, language-specific patterns, security | ~400 lines |
| **[ref-docker-compose.md](ref-docker-compose.md)** | Compose configuration, dev/prod setup, dependencies | ~300 lines |
| **[docker-optimization.md](docker-optimization.md)** | Layer caching, image size reduction, BuildKit | ~400 lines |

**Full methodology:** [docker-compose.md](docker-compose.md) (methodology format)

---

## Quick Navigation

### Getting Started
→ [docker-basics.md](docker-basics.md) - Learn Dockerfile, commands, networking

### Production Patterns
→ [dockerfile-patterns.md](dockerfile-patterns.md) - Multi-stage builds for Python, Go, Node.js

### Multi-Container Apps
→ [ref-docker-compose.md](ref-docker-compose.md) - Compose setup, dependencies, volumes

### Performance
→ [docker-optimization.md](docker-optimization.md) - Reduce image size, speed up builds

---

## Core Principles (Summary)

### 1. Build Once, Run Anywhere

```
Dockerfile → Image → Container → Registry
```

### 2. Layer Caching

Order instructions from least to most frequently changing:

```dockerfile
FROM python:3.12-slim        # Rarely changes
COPY requirements.txt .      # Sometimes changes
RUN pip install -r ...       # Sometimes changes
COPY . .                     # Frequently changes

### Dockerfile Basics
→ Image selection, instructions, CMD vs ENTRYPOINT
→ See: [docker-basics.md](docker-basics.md)

### Multi-stage Builds
→ Python, Go, Node.js, TypeScript patterns
→ See: [dockerfile-patterns.md](dockerfile-patterns.md)

### Docker Compose
→ Multi-container setup, dependencies, health checks
→ See: [ref-docker-compose.md](ref-docker-compose.md) and [docker-compose.md](docker-compose.md)

### Optimization
→ Layer caching, image size, BuildKit
→ See: [docker-optimization.md](docker-optimization.md)

### Security
→ Non-root users, secrets, scanning, best practices
→ See: [dockerfile-patterns.md](dockerfile-patterns.md) (security section)

---

## Common Commands (Quick Reference)

```bash
# Build
docker build -t myapp:latest .

# Run
docker run -d --name myapp -p 8080:80 myapp:latest

# Compose
docker compose up -d

# Logs
docker logs -f container_name

# Execute
docker exec -it container_name bash

# Clean up
docker system prune -a --volumes
```

For detailed commands, see [docker-basics.md](docker-basics.md).

---

## Checklists

### Dockerfile Checklist
- [ ] Base image version pinned
- [ ] Non-root user configured
- [ ] .dockerignore present
- [ ] Multi-stage build (if applicable)
- [ ] Layer caching optimized
- [ ] HEALTHCHECK defined

### Production Checklist
- [ ] Image tagged with version
- [ ] Health checks configured
- [ ] Resource limits defined
- [ ] Restart policy set
- [ ] Secrets management configured

---

## Tools

| Tool | Purpose |
|------|---------|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | GUI for Docker management |
| [Docker Scout](https://docs.docker.com/scout/) | Vulnerability scanning |
| [Dive](https://github.com/wagoodman/dive) | Image layer analysis |
| [Hadolint](https://github.com/hadolint/hadolint) | Dockerfile linting |
| [Trivy](https://github.com/aquasecurity/trivy) | Security scanning |

---

## Sources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose Specification](https://docs.docker.com/compose/compose-file/)
- [Docker Security](https://docs.docker.com/engine/security/)
