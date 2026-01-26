# Docker Optimization LLM Prompts

AI-assisted prompts for Docker image optimization.

---

## Dockerfile Review

### Analyze Existing Dockerfile

```
Review this Dockerfile for optimization opportunities:

```dockerfile
{DOCKERFILE_CONTENT}
```

Analyze for:
1. Image size reduction opportunities
2. Build caching efficiency
3. Security issues
4. Layer optimization
5. Multi-stage build potential

Provide specific recommendations with code examples.
```

### Optimize for Size

```
Optimize this Dockerfile to minimize image size:

```dockerfile
{DOCKERFILE_CONTENT}
```

Requirements:
- Target size: < {TARGET_SIZE} MB
- Must use multi-stage build
- Remove all unnecessary dependencies
- Use slim/alpine/distroless base
- Maintain functionality

Provide the optimized Dockerfile with size reduction estimate.
```

---

## Security Hardening

### Security Audit

```
Perform a security audit of this Dockerfile:

```dockerfile
{DOCKERFILE_CONTENT}
```

Check for:
1. Running as root user
2. Secrets in build args or ENV
3. Unnecessary packages
4. Missing security headers
5. Outdated base images
6. Missing image signing

Provide remediation for each issue found.
```

### Harden Dockerfile

```
Harden this Dockerfile following OWASP container security guidelines:

```dockerfile
{DOCKERFILE_CONTENT}
```

Apply:
1. Non-root user with specific UID/GID
2. Read-only filesystem compatibility
3. No shell if not needed (distroless)
4. Minimal attack surface
5. Image signing setup

Provide the hardened Dockerfile with explanations.
```

---

## Build Performance

### Optimize Build Time

```
Optimize this Dockerfile for faster CI/CD builds:

```dockerfile
{DOCKERFILE_CONTENT}
```

Focus on:
1. Layer ordering for cache efficiency
2. BuildKit cache mounts for package managers
3. Parallel build stages where possible
4. Dependency caching strategy

Current build time: {CURRENT_TIME}
Target build time: < {TARGET_TIME}
```

### CI/CD Integration

```
Create a CI/CD-optimized Dockerfile for:

Application: {APP_TYPE}
CI Platform: {GITHUB_ACTIONS|GITLAB_CI|JENKINS}
Registry: {REGISTRY_URL}

Requirements:
1. Remote cache support (--cache-from)
2. Multi-platform build support (amd64, arm64)
3. Build args for versioning
4. Layer extraction for caching

Include:
- Dockerfile
- CI configuration snippet
- Cache strategy explanation
```

---

## Language-Specific

### Python Application

```
Create an optimized Dockerfile for this Python application:

Dependencies: {requirements.txt or pyproject.toml}
Framework: {FASTAPI|DJANGO|FLASK}
Python version: {VERSION}

Requirements:
1. Multi-stage build
2. pip cache mount
3. Non-root user
4. Health check
5. Target size < 200 MB

Include .dockerignore file.
```

### Node.js Application

```
Create an optimized Dockerfile for this Node.js application:

Package manager: {NPM|PNPM|YARN}
Framework: {NEXT.JS|EXPRESS|NESTJS}
Node version: {VERSION}

Requirements:
1. Multi-stage build (deps, builder, runner)
2. npm cache mount
3. Production dependencies only in final stage
4. Non-root user
5. Target size < 150 MB

Include .dockerignore file.
```

### Go Application

```
Create an optimized Dockerfile for this Go application:

Go version: {VERSION}
CGO required: {YES|NO}
Static binary: {YES|NO}

Requirements:
1. Multi-stage build
2. go mod cache mount
3. Scratch or distroless final stage
4. Build flags for size optimization (-ldflags="-w -s")
5. Target size < 20 MB
```

---

## Troubleshooting

### Diagnose Large Image

```
Help diagnose why this Docker image is {SIZE} MB:

```dockerfile
{DOCKERFILE_CONTENT}
```

I ran `docker history {IMAGE}` and got:
```
{HISTORY_OUTPUT}
```

Identify:
1. Which layers are largest
2. What's causing the bloat
3. Step-by-step optimization plan
4. Expected size after optimization
```

### Fix Cache Invalidation

```
My Docker build cache keeps invalidating unexpectedly.

Dockerfile:
```dockerfile
{DOCKERFILE_CONTENT}
```

Build output shows cache miss at:
{BUILD_OUTPUT}

Help me:
1. Identify why cache is invalidating
2. Restructure for better cache hits
3. Explain layer caching rules
```

---

## Migration

### Convert to Multi-Stage

```
Convert this single-stage Dockerfile to multi-stage:

```dockerfile
{DOCKERFILE_CONTENT}
```

Create stages for:
1. Dependencies installation
2. Build/compilation
3. Runtime (minimal)

Explain what artifacts to copy between stages.
```

### Migrate Base Image

```
Migrate this Dockerfile from {CURRENT_BASE} to {TARGET_BASE}:

```dockerfile
{DOCKERFILE_CONTENT}
```

Consider:
1. Package manager differences (apt vs apk)
2. Missing utilities
3. Path differences
4. User/group handling

Provide migration steps and gotchas.
```

---

## Comparison

### Compare Approaches

```
Compare these two Dockerfile approaches for {USE_CASE}:

Approach A:
```dockerfile
{DOCKERFILE_A}
```

Approach B:
```dockerfile
{DOCKERFILE_B}
```

Compare:
1. Image size
2. Build time
3. Security posture
4. Maintainability
5. CI/CD compatibility

Recommend the better approach with justification.
```

---

## Generation

### Generate from Scratch

```
Generate an optimized Dockerfile for:

Application type: {TYPE}
Language/Framework: {LANG/FRAMEWORK}
Build tool: {TOOL}
Production requirements: {REQUIREMENTS}

Include:
1. Multi-stage build
2. BuildKit features (syntax directive, cache mounts)
3. Security best practices
4. Health check
5. OCI labels
6. Comprehensive .dockerignore

Follow 2025-2026 best practices.
```

### Generate docker-compose

```
Generate docker-compose.yml for local development:

Services:
- App: {APP_DOCKERFILE}
- Database: {POSTGRES|MYSQL|MONGODB}
- Cache: {REDIS|MEMCACHED}

Include:
1. Health checks
2. Volume mounts for hot reload
3. Network isolation
4. Environment file support
5. Resource limits
```

---

*Docker Optimization LLM Prompts | faion-cicd-engineer*
