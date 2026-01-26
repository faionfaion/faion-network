# Docker Optimization Checklist

## Pre-Build Checklist

### Base Image Selection

- [ ] Using official images from trusted registries
- [ ] Using slim/alpine/distroless variants where possible
- [ ] Base image pinned to specific version (not `latest`)
- [ ] Consider Chainguard/Wolfi images for zero-CVE base
- [ ] Image digest pinned for supply chain security (production)

### Dockerfile Structure

- [ ] `# syntax=docker/dockerfile:1.7` directive at top (for BuildKit features)
- [ ] Instructions ordered from least to most frequently changing
- [ ] Dependencies copied before application code
- [ ] RUN commands combined with `&&` where appropriate
- [ ] Cache cleaning in same layer as package installation

### Build Context

- [ ] `.dockerignore` file present and comprehensive
- [ ] Excludes: `.git`, `node_modules`, `__pycache__`, `venv`, `.env`
- [ ] Excludes: `tests/`, `docs/`, `*.md` (except README if needed)
- [ ] Excludes: IDE files (`.vscode/`, `.idea/`)
- [ ] Build context size verified (`docker build` shows context size)

### Multi-Stage Build

- [ ] Separate build and runtime stages
- [ ] Build tools not present in final image
- [ ] Only necessary artifacts copied to final stage
- [ ] Using `--target` for specific stage builds if needed

### Security

- [ ] Non-root user configured (`USER nobody` or specific UID)
- [ ] No secrets in Dockerfile or build args
- [ ] Using BuildKit secrets for sensitive data during build
- [ ] No unnecessary packages installed
- [ ] `--no-install-recommends` used with apt-get

---

## Post-Build Checklist

### Image Size Verification

- [ ] Image size < 200 MB (ideally < 100 MB for microservices)
- [ ] `docker history` shows no unexpectedly large layers
- [ ] Dive analysis shows no wasted space
- [ ] No dev dependencies in final image

### Security Scanning

- [ ] `docker scout cves` or `trivy image` run
- [ ] No critical/high vulnerabilities (or documented exceptions)
- [ ] Base image CVEs reviewed and acceptable
- [ ] Hadolint passes with no errors

### Runtime Verification

- [ ] Container runs as non-root user
- [ ] Read-only filesystem works (if applicable)
- [ ] Resource limits tested (memory, CPU)
- [ ] Health check configured and working
- [ ] Graceful shutdown works (SIGTERM handling)

### Build Performance

- [ ] Build uses cache effectively (rebuild without changes is fast)
- [ ] BuildKit cache mounts configured for package managers
- [ ] Parallel stages used where dependencies allow
- [ ] CI/CD caching configured (registry cache or local)

---

## Quick Commands

```bash
# Check image size
docker images myapp --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# View layer sizes
docker history myapp:latest

# Deep analysis with Dive
dive myapp:latest

# Lint Dockerfile
hadolint Dockerfile

# Security scan
docker scout cves myapp:latest
trivy image --severity HIGH,CRITICAL myapp:latest

# Verify non-root user
docker run --rm myapp:latest whoami

# Check build context size
docker build --no-cache -t test . 2>&1 | grep "Sending build context"
```

---

## Size Targets by Application Type

| Type | Target Size | Base Image |
|------|-------------|------------|
| Static site (nginx) | < 30 MB | nginx:alpine |
| Go microservice | < 20 MB | scratch or distroless |
| Rust service | < 30 MB | scratch or distroless |
| Node.js API | < 150 MB | node:20-alpine |
| Python API | < 200 MB | python:3.12-slim |
| Java service | < 250 MB | eclipse-temurin:21-jre-alpine |
| Full-stack app | < 300 MB | Multi-stage |

---

## Red Flags

Warning signs that optimization is needed:

| Issue | Indicator | Solution |
|-------|-----------|----------|
| Large image | > 500 MB | Multi-stage, slim base |
| Slow builds | Cache invalidation | Reorder instructions |
| Many layers | > 15 layers | Combine RUN commands |
| Root user | `whoami` returns root | Add USER instruction |
| Vulnerabilities | Scout/Trivy warnings | Update base, remove packages |
| Large context | > 100 MB sent | Fix .dockerignore |

---

*Docker Optimization Checklist | faion-cicd-engineer*
