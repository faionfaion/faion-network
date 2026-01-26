# Docker Containerization Checklist

Production readiness checklist for containerized applications.

## Dockerfile Checklist

### Base Image

- [ ] Use official or verified base images
- [ ] Pin specific version tag (e.g., `python:3.12.1-slim`, not `python:latest`)
- [ ] Choose minimal variant (`-slim`, `-alpine`, distroless)
- [ ] Verify image signatures with Docker Content Trust

### Build Optimization

- [ ] Use multi-stage builds to separate build and runtime
- [ ] Order instructions by change frequency (rarely changed first)
- [ ] Combine RUN commands with `&&` to reduce layers
- [ ] Use `--no-cache-dir` for pip, `--no-cache` for npm
- [ ] Enable BuildKit (`DOCKER_BUILDKIT=1`)
- [ ] Use cache mounts for package managers (`--mount=type=cache`)

### Security

- [ ] Create non-root user with `USER` directive
- [ ] Set appropriate file ownership with `--chown`
- [ ] No secrets in Dockerfile or build args
- [ ] No unnecessary packages or tools
- [ ] Remove package manager caches (`rm -rf /var/lib/apt/lists/*`)
- [ ] Use `COPY` instead of `ADD` (unless extracting archives)

### Runtime Configuration

- [ ] Set `WORKDIR` for organized file structure
- [ ] Define `EXPOSE` for documentation
- [ ] Use `HEALTHCHECK` instruction
- [ ] Set default `CMD` or `ENTRYPOINT`
- [ ] Use exec form: `CMD ["executable", "param"]`

## .dockerignore Checklist

- [ ] Exclude `.git` directory
- [ ] Exclude `node_modules`, `__pycache__`, `.venv`
- [ ] Exclude IDE configs (`.idea`, `.vscode`)
- [ ] Exclude test files and coverage reports
- [ ] Exclude `.env` files and secrets
- [ ] Exclude documentation (keep README if needed)
- [ ] Exclude Dockerfile and docker-compose files

## Container Runtime Checklist

### Resource Limits

- [ ] Set memory limit (`--memory`)
- [ ] Set CPU limit (`--cpus`)
- [ ] Configure restart policy (`--restart`)
- [ ] Set PID limit (`--pids-limit`)

### Security Hardening

- [ ] Run as non-root user
- [ ] Use read-only filesystem (`--read-only`)
- [ ] Mount tmpfs for temp directories (`--tmpfs /tmp`)
- [ ] Drop all capabilities (`--cap-drop ALL`)
- [ ] Add only required capabilities (`--cap-add`)
- [ ] Prevent privilege escalation (`--security-opt no-new-privileges`)
- [ ] Use seccomp profiles where applicable

### Networking

- [ ] Use user-defined networks (not default bridge)
- [ ] Expose only necessary ports
- [ ] Consider read-only volume mounts (`:ro`)
- [ ] Avoid host network mode in production

### Logging

- [ ] Configure log driver
- [ ] Set log rotation limits
- [ ] Output logs to stdout/stderr

## Image Security Checklist

### Scanning

- [ ] Scan images for vulnerabilities (Trivy, Docker Scout, Snyk)
- [ ] Fail builds on HIGH/CRITICAL vulnerabilities
- [ ] Scan regularly, not just at build time
- [ ] Generate and review SBOM (Software Bill of Materials)

### Registry

- [ ] Use private registry for proprietary images
- [ ] Enable image signing
- [ ] Implement image retention policy
- [ ] Restrict push access to CI/CD systems

### Updates

- [ ] Monitor base image updates
- [ ] Automate dependency updates (Dependabot, Renovate)
- [ ] Rebuild images regularly (weekly minimum)
- [ ] Track CVEs for base images

## CI/CD Integration Checklist

### Build Pipeline

- [ ] Build images in CI, not manually
- [ ] Tag images with git commit SHA
- [ ] Tag releases with semantic versions
- [ ] Push to registry only from CI
- [ ] Cache layers between builds

### Testing

- [ ] Run container structure tests
- [ ] Test health check endpoint
- [ ] Verify non-root execution
- [ ] Check resource consumption

### Deployment

- [ ] Use immutable image tags (SHA, not `latest`)
- [ ] Implement rolling updates
- [ ] Configure readiness/liveness probes (K8s)
- [ ] Plan rollback strategy

## Orchestration Checklist (Docker Compose / Kubernetes)

### Service Configuration

- [ ] Define resource requests and limits
- [ ] Configure health checks
- [ ] Set up proper service dependencies
- [ ] Use environment-specific configs

### Data Management

- [ ] Use named volumes for persistence
- [ ] Plan backup strategy
- [ ] Document volume mount points
- [ ] Avoid host path mounts in production

### Networking

- [ ] Define internal/external networks
- [ ] Configure service discovery
- [ ] Set up load balancing
- [ ] Implement network policies (K8s)

## Monitoring Checklist

- [ ] Collect container metrics (CPU, memory, network)
- [ ] Set up log aggregation
- [ ] Configure alerting for health check failures
- [ ] Monitor image vulnerabilities continuously
- [ ] Track container restarts

## Quick Validation Commands

```bash
# Check image for non-root user
docker inspect --format='{{.Config.User}}' IMAGE

# Verify health check
docker inspect --format='{{json .Config.Healthcheck}}' IMAGE

# Check image size
docker images IMAGE --format "{{.Size}}"

# Scan for vulnerabilities
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy image --severity HIGH,CRITICAL IMAGE

# Test container starts correctly
docker run --rm --read-only IMAGE

# List image layers
docker history IMAGE
```
