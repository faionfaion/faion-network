# Docker LLM Prompts

Prompts for common Docker tasks. Use with Claude, GPT, or other LLMs.

---

## Dockerfile Creation

### Create Optimized Dockerfile

```
Create a production-ready Dockerfile for a [LANGUAGE/FRAMEWORK] application with:

Requirements:
- Multi-stage build (builder + runtime stages)
- Minimal base image (slim/alpine/distroless)
- Non-root user for security
- Layer caching optimization
- Health check
- Proper labels (maintainer, version)

Application details:
- Framework: [Django/FastAPI/Express/Next.js/etc.]
- Entry point: [app.py/index.js/etc.]
- Port: [8000/3000/etc.]
- Dependencies file: [requirements.txt/package.json/etc.]
- Build command: [npm run build/etc. if applicable]

Additional requirements:
- [Any specific packages needed]
- [Environment variables]
- [Volume mounts]
```

### Optimize Existing Dockerfile

```
Optimize this Dockerfile for production:

[PASTE CURRENT DOCKERFILE]

Requirements:
1. Reduce image size (currently [SIZE])
2. Improve build speed with layer caching
3. Add security best practices (non-root user, minimal capabilities)
4. Add health check
5. Use multi-stage build if not already

Target:
- Image size: <200MB
- Build time: <2 minutes (with cache)
- Security: Run as non-root, no secrets in image
```

### Convert Single-Stage to Multi-Stage

```
Convert this single-stage Dockerfile to an optimized multi-stage build:

[PASTE DOCKERFILE]

Requirements:
- Stage 1 (builder): Install build dependencies and compile
- Stage 2 (runtime): Only runtime dependencies and artifacts
- Final image should not contain build tools, source code (if compiled), or dev dependencies
- Preserve layer caching for dependencies
```

---

## Docker Compose

### Generate Compose File

```
Create a docker-compose.yml for a [STACK_TYPE] application:

Services needed:
- [app]: [Language/Framework] - port [PORT]
- [db]: [PostgreSQL/MySQL/MongoDB] - version [VERSION]
- [cache]: [Redis/Memcached] (optional)
- [nginx]: Reverse proxy (optional)

Requirements:
- Named volumes for persistent data
- Custom network
- Health checks for all services
- Proper dependency ordering with health conditions
- Environment variables from .env file
- Resource limits

Additional:
- Include development override file (docker-compose.override.yml)
- Include production configuration (docker-compose.prod.yml)
```

### Debug Compose Issues

```
Debug this docker-compose configuration. The issue is: [DESCRIBE ISSUE]

[PASTE DOCKER-COMPOSE.YML]

Error message:
[PASTE ERROR]

Please:
1. Identify the root cause
2. Explain why it happens
3. Provide corrected configuration
4. Suggest best practices improvements
```

---

## Security

### Security Audit

```
Perform a security audit on this Dockerfile:

[PASTE DOCKERFILE]

Check for:
1. Running as root
2. Secrets or credentials in image
3. Unnecessary packages or tools
4. Missing security headers
5. Capabilities that should be dropped
6. Missing read-only filesystem potential
7. Base image vulnerabilities

Provide:
- List of issues found (severity: Critical/High/Medium/Low)
- Fixed Dockerfile
- Runtime security recommendations (docker run flags)
```

### Add Security Hardening

```
Add security hardening to this Dockerfile and compose configuration:

Dockerfile:
[PASTE]

docker-compose.yml:
[PASTE]

Add:
1. Non-root user with specific UID/GID
2. Read-only root filesystem where possible
3. Drop all capabilities, add only required
4. no-new-privileges security option
5. Resource limits
6. Secrets management (Docker secrets, not ENV)
7. Network segmentation (internal networks for backend)
```

---

## Optimization

### Reduce Image Size

```
Help me reduce the size of this Docker image:

Current Dockerfile:
[PASTE]

Current image size: [SIZE]
Target image size: <[TARGET_SIZE]

Analyze:
1. Layer sizes (which layers are largest?)
2. Unnecessary files or dependencies
3. Base image choice
4. Multi-stage build opportunities
5. .dockerignore improvements

Provide optimized Dockerfile with expected size reduction for each change.
```

### Improve Build Performance

```
Optimize build performance for this Dockerfile:

[PASTE DOCKERFILE]

Current build time: [TIME] (without cache: [TIME])
Target: <[TARGET_TIME]

Optimize:
1. Layer ordering for better caching
2. Parallel operations where possible
3. BuildKit features (cache mounts, etc.)
4. Dependency caching strategy
5. .dockerignore to reduce build context

Provide optimized Dockerfile with explanation of each optimization.
```

---

## Migration & Conversion

### Migrate to Docker

```
Create Docker configuration for this existing application:

Application details:
- Language: [LANGUAGE]
- Framework: [FRAMEWORK]
- Current deployment: [VM/bare metal/etc.]
- Dependencies: [List or file]
- Environment variables: [List]
- External services: [databases, caches, etc.]

Requirements:
- Dockerfile (multi-stage, production-ready)
- docker-compose.yml (local development)
- docker-compose.prod.yml (production)
- .dockerignore
- entrypoint script if needed

Consider:
- Database migration strategy
- Volume mapping for persistent data
- Environment-specific configuration
- Health checks and monitoring
```

### Migrate Docker Compose to Kubernetes

```
Convert this docker-compose.yml to Kubernetes manifests:

[PASTE DOCKER-COMPOSE.YML]

Generate:
1. Deployments for each service
2. Services (ClusterIP/LoadBalancer as appropriate)
3. ConfigMaps for non-sensitive config
4. Secrets for sensitive data
5. PersistentVolumeClaims for volumes
6. Ingress if nginx/proxy service exists
7. HorizontalPodAutoscaler (optional)

Format: Separate YAML files or single file with --- separators
```

---

## Troubleshooting

### Debug Container Issues

```
Help debug this Docker container issue:

Problem: [DESCRIBE THE ISSUE]

Dockerfile:
[PASTE]

docker-compose.yml (if applicable):
[PASTE]

Error/logs:
[PASTE ERROR OR LOGS]

Commands tried:
[LIST COMMANDS]

Please:
1. Identify likely causes
2. Provide debugging commands to run
3. Suggest fixes
4. Explain how to prevent this in future
```

### Fix Network Issues

```
Debug networking issue between Docker containers:

Setup:
[PASTE DOCKER-COMPOSE.YML OR DESCRIBE SETUP]

Issue: [Container A cannot reach Container B / DNS resolution fails / etc.]

What I've tried:
[LIST ATTEMPTS]

Please:
1. Diagnose the network configuration
2. Provide commands to debug (docker network inspect, exec into container, etc.)
3. Fix the configuration
4. Explain Docker networking best practices
```

---

## CI/CD Integration

### GitHub Actions Docker Build

```
Create a GitHub Actions workflow for building and pushing Docker images:

Requirements:
- Build on push to main and tags
- Multi-platform build (linux/amd64, linux/arm64)
- Push to [Docker Hub/GHCR/ECR]
- Cache layers between builds
- Security scanning with [Trivy/Scout]
- Tag with: latest, semantic version from tag, git SHA

Dockerfile location: [./Dockerfile]
Image name: [org/repo]
```

### GitLab CI Docker Build

```
Create a GitLab CI pipeline for Docker:

Stages needed:
1. Lint Dockerfile (hadolint)
2. Build image
3. Security scan (trivy)
4. Push to registry
5. Deploy to [environment]

Requirements:
- Use GitLab Container Registry
- Cache Docker layers
- Run on merge requests (build only, no push)
- Run full pipeline on main branch
- Semantic versioning from tags
```

---

## Best Practices Review

### Full Stack Review

```
Review this Docker setup for best practices:

Dockerfile:
[PASTE]

docker-compose.yml:
[PASTE]

.dockerignore:
[PASTE]

Review for:
1. Security (non-root, secrets, scanning)
2. Performance (image size, build time, caching)
3. Reliability (health checks, restart policies)
4. Maintainability (labels, documentation, structure)
5. Development experience (hot reload, debugging)
6. Production readiness (resource limits, logging)

Provide:
- Score (1-10) for each category
- Specific issues found
- Prioritized recommendations
- Updated configurations
```

---

## Quick Prompts

### One-Liner Generations

```
# Generate .dockerignore for [language]
Generate a comprehensive .dockerignore file for a [Python/Node.js/Go] project.

# Create health check for [service]
Create a HEALTHCHECK instruction for a [Django/FastAPI/Express] application running on port [PORT].

# Generate entrypoint script
Create a docker-entrypoint.sh script that waits for PostgreSQL, runs migrations, and starts the application.

# Multi-platform build command
Generate a docker buildx command to build and push multi-platform images (amd64, arm64) to [registry].

# Compose profiles
Add profiles to this docker-compose.yml to separate development, testing, and production services.
```

---

## Prompt Templates

### Standard Request Format

```
Task: [What you want to achieve]

Context:
- Application: [Type and framework]
- Current state: [Existing files/setup]
- Environment: [Dev/Staging/Prod]
- Constraints: [Size limits, security requirements, etc.]

Files:
[PASTE RELEVANT FILES]

Expected output:
- [List expected deliverables]

Additional requirements:
- [Any specific preferences or standards]
```

### Iterative Improvement Format

```
Current configuration:
[PASTE]

What I want to improve:
1. [Specific improvement 1]
2. [Specific improvement 2]

Constraints:
- Must maintain: [Feature/behavior to preserve]
- Cannot change: [Fixed requirements]

Please provide:
1. Analysis of current issues
2. Step-by-step improvements
3. Final updated configuration
4. Verification steps
```
