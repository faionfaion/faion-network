# Docker Containerization

> **Entry point:** `/faion-net` — invoke for automatic routing.

## Overview

Docker containerization packages applications with their dependencies into standardized units for development, deployment, and scaling. Containers provide isolation, portability, and consistent environments across development, staging, and production.

## When to Use

| Scenario | Description |
|----------|-------------|
| Complex dependencies | Applications requiring specific runtime versions |
| Environment consistency | Matching dev, staging, and production environments |
| Microservices | Isolated services with independent scaling |
| CI/CD pipelines | Reproducible builds and deployments |
| Multi-tenant apps | Isolation between tenants |

## Key Concepts

| Concept | Description |
|---------|-------------|
| Image | Read-only template with instructions for creating container |
| Container | Runnable instance of an image |
| Dockerfile | Text file with instructions to build an image |
| Layer | Each instruction in Dockerfile creates a cacheable layer |
| Registry | Storage and distribution system for images (Docker Hub, ECR, GCR) |
| Volume | Persistent data storage outside container filesystem |
| Network | Communication layer between containers |

## Modern Best Practices (2025-2026)

### Container Design Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Single-container | One responsibility per container | Simple applications |
| Sidecar | Extend container behavior | Log processors, proxies |
| Ambassador | Proxy for external services | Load balancing, retries |
| Adapter | Standardize output/interfaces | Monitoring, logging |
| Init Container | Pre-initialization tasks | DB migrations, config |

### Security Principles

| Principle | Implementation |
|-----------|----------------|
| Non-root execution | Create dedicated user with `USER` directive |
| Read-only filesystem | Use `--read-only` flag at runtime |
| Minimal base images | Use `-slim` or `-alpine` variants |
| Capability dropping | Remove unnecessary Linux capabilities |
| Secrets management | Use Docker Secrets, Vault, or cloud secret managers |
| Image signing | Enable Docker Content Trust (DCT) |
| Vulnerability scanning | Integrate Trivy, Docker Scout, or Snyk |

### Image Optimization

| Technique | Benefit |
|-----------|---------|
| Multi-stage builds | Reduce final image size 70-90% |
| Layer caching | Faster rebuilds, order by change frequency |
| .dockerignore | Exclude unnecessary files from context |
| Minimal dependencies | Smaller attack surface |
| Distroless images | No shell, no package manager |

## Files in This Directory

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts (this file) |
| [checklist.md](checklist.md) | Production readiness checklist |
| [examples.md](examples.md) | Dockerfile examples by language/framework |
| [templates.md](templates.md) | Copy-paste templates for common scenarios |
| [llm-prompts.md](llm-prompts.md) | Prompts for containerization tasks |

## Quick Reference

### Image Size Comparison

| Base Image | Size | Use Case |
|------------|------|----------|
| `python:3.12` | ~900MB | Development only |
| `python:3.12-slim` | ~120MB | Production default |
| `python:3.12-alpine` | ~50MB | Size-critical apps |
| `node:20` | ~1GB | Development only |
| `node:20-slim` | ~200MB | Production default |
| `node:20-alpine` | ~130MB | Size-critical apps |
| `gcr.io/distroless/python3` | ~50MB | Maximum security |

### Container Runtime Flags

| Flag | Purpose |
|------|---------|
| `--read-only` | Read-only root filesystem |
| `--memory 512m` | Memory limit |
| `--cpus 0.5` | CPU limit |
| `--restart unless-stopped` | Auto-restart policy |
| `--cap-drop ALL` | Drop all capabilities |
| `--security-opt no-new-privileges` | Prevent privilege escalation |

## Related Methodologies

| Methodology | Path |
|-------------|------|
| Docker Compose | [docker-compose.md](../docker-compose.md) |
| Kubernetes | [../faion-infrastructure-engineer/kubernetes-basics.md](../faion-infrastructure-engineer/kubernetes-basics.md) |
| CI/CD Integration | [../faion-cicd-engineer/github-actions.md](../faion-cicd-engineer/github-actions.md) |

## References

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Docker Hardened Images](https://www.docker.com/blog/docker-hardened-images-for-every-developer/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Trivy Security Scanner](https://aquasecurity.github.io/trivy/)
