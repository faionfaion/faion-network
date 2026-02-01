# Docker Optimization

**Image size reduction, build caching, multi-stage builds, and security hardening**

## Overview

Docker image optimization focuses on four key areas:
1. **Image Size** - Smaller images = faster pulls, less storage, reduced attack surface
2. **Build Caching** - Faster builds through intelligent layer ordering
3. **Multi-Stage Builds** - Separate build and runtime environments
4. **Security** - Non-root users, scanning, secrets management

## Quick Reference

| Optimization | Impact | Complexity |
|--------------|--------|------------|
| Slim/Alpine base | -70-80% size | Low |
| Multi-stage builds | -50-90% size | Medium |
| BuildKit cache mounts | -60% build time | Low |
| .dockerignore | Variable | Low |
| Non-root user | Security | Low |
| Image scanning | Security | Low |

## Base Image Comparison (2025-2026)

| Base Image | Size | Use Case |
|------------|------|----------|
| `scratch` | 0 MB | Static Go/Rust binaries |
| `gcr.io/distroless/static` | <2 MB | Maximum security, no shell |
| `cgr.dev/chainguard/static` | <2 MB | Wolfi-based, zero CVEs |
| `alpine:3.20` | ~5 MB | Minimal with package manager |
| `debian:12-slim` | ~40 MB | Balance of tools and size |
| `ubuntu:24.04` | ~70 MB | General purpose |

## Modern Best Practices (2025-2026)

### 1. Enable BuildKit (Default in Docker 23+)

```bash
export DOCKER_BUILDKIT=1
```

### 2. Use Cache Mounts

```dockerfile
# syntax=docker/dockerfile:1.7
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

### 3. Pin Image Digests for Supply Chain Security

```dockerfile
FROM python:3.12-slim@sha256:abc123...
```

### 4. Scan Images with Docker Scout or Trivy

```bash
docker scout cves myapp:latest
trivy image myapp:latest
```

### 5. Use Chainguard/Wolfi Images for Zero-CVE Base

```dockerfile
FROM cgr.dev/chainguard/python:latest
```

## Size Reduction Formula

```
Final Size = Base Image + Dependencies + Application Code - Excluded Files
```

**Target:** Production images < 200 MB (ideally < 100 MB)

## Layer Ordering Principle

Order Dockerfile instructions from **least to most frequently changing**:

```
1. Base image (rarely changes)
2. System packages (occasionally changes)
3. Dependencies (changes with requirements)
4. Application code (changes frequently)
```

## Tools

| Tool | Purpose | Command |
|------|---------|---------|
| **Dive** | Layer analysis | `dive myapp:latest` |
| **Hadolint** | Dockerfile linting | `hadolint Dockerfile` |
| **Docker Scout** | Vulnerability scanning | `docker scout cves myapp` |
| **Trivy** | Security scanner | `trivy image myapp` |
| **DockerSlim** | Image minification | `docker-slim build myapp` |

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-build and post-build verification |
| [examples.md](examples.md) | Language-specific Dockerfile examples |
| [templates.md](templates.md) | Copy-paste production templates |
| [llm-prompts.md](llm-prompts.md) | AI-assisted optimization prompts |

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Set up GitHub Actions workflow from template | haiku | Pattern application, simple configuration |
| Design CI/CD pipeline architecture | opus | Complex system design with many variables |
| Write terraform code for infrastructure | sonnet | Implementation with moderate complexity |
| Debug failing pipeline step | sonnet | Debugging and problem-solving |
| Implement AIOps anomaly detection | opus | Novel ML approach, complex decision |
| Configure webhook and secret management | haiku | Mechanical setup using checklists |


## Sources

- [Docker Build Best Practices](https://docs.docker.com/build/building/best-practices/)
- [BuildKit Documentation](https://docs.docker.com/build/buildkit/)
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Chainguard Images](https://www.chainguard.dev/chainguard-images)
- [Dive Tool](https://github.com/wagoodman/dive)
- [Hadolint Linter](https://github.com/hadolint/hadolint)
- [Docker Best Practices 2026](https://thinksys.com/devops/docker-best-practices/)

---

*Docker Optimization | faion-cicd-engineer*
