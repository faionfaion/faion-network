# Docker Containerization LLM Prompts

Prompts for containerization tasks with Claude and other LLMs.

## Dockerfile Generation

### Generate Production Dockerfile

```
Create a production-ready Dockerfile for a {LANGUAGE} application with these requirements:

Application: {APP_DESCRIPTION}
Framework: {FRAMEWORK}
Entry point: {ENTRY_POINT}
Port: {PORT}
Database: {DATABASE_TYPE} (optional)

Requirements:
1. Multi-stage build to minimize image size
2. Non-root user execution
3. Health check endpoint at /health
4. Proper layer caching optimization
5. No secrets in Dockerfile
6. Security best practices (2025-2026)

Include:
- Appropriate base image selection with pinned version
- Build and production stages
- .dockerignore file
- Explanation of each decision
```

### Optimize Existing Dockerfile

```
Review and optimize this Dockerfile for production use:

```dockerfile
{CURRENT_DOCKERFILE}
```

Check for:
1. Image size optimization (multi-stage builds)
2. Security issues (root user, secrets, base image)
3. Layer caching efficiency
4. Build time optimization
5. Health check presence
6. Compliance with 2025-2026 best practices

Provide:
- Optimized Dockerfile
- Explanation of each change
- Estimated size reduction
```

### Convert to Multi-Stage Build

```
Convert this single-stage Dockerfile to a multi-stage build:

```dockerfile
{CURRENT_DOCKERFILE}
```

Goals:
1. Separate build and runtime stages
2. Minimize final image size
3. Include only runtime dependencies
4. Maintain all functionality

Explain the benefits of each stage.
```

## Security Analysis

### Security Audit

```
Perform a security audit of this Dockerfile:

```dockerfile
{DOCKERFILE}
```

Check for:
1. Base image vulnerabilities
2. Root user execution
3. Secrets exposure
4. Unnecessary packages
5. File permissions
6. Missing security headers/flags

Provide:
- List of issues with severity (HIGH/MEDIUM/LOW)
- Remediation for each issue
- Fixed Dockerfile
```

### Add Security Hardening

```
Add security hardening to this Dockerfile following 2025-2026 best practices:

```dockerfile
{DOCKERFILE}
```

Add:
1. Non-root user with minimal permissions
2. Read-only filesystem support
3. Capability dropping
4. Security scanning integration
5. Secret management pattern
6. Image signing setup

Explain each security measure.
```

## Docker Compose

### Generate Docker Compose

```
Create a docker-compose.yml for this architecture:

Services:
{LIST_OF_SERVICES}

Requirements:
- Health checks for all services
- Proper dependency ordering
- Named volumes for persistence
- Resource limits
- Environment variable management
- Network isolation

Include both development and production configurations.
```

### Convert to Production Compose

```
Convert this development docker-compose.yml to production-ready:

```yaml
{CURRENT_COMPOSE}
```

Changes needed:
1. Remove development-only features
2. Add resource limits
3. Add health checks
4. Configure proper restart policies
5. Set up proper networking
6. Add logging configuration
```

## Troubleshooting

### Debug Container Issues

```
Help debug this container issue:

Error: {ERROR_MESSAGE}

Dockerfile:
```dockerfile
{DOCKERFILE}
```

Context:
- Platform: {OS/ARCHITECTURE}
- Docker version: {VERSION}
- Base image: {IMAGE}
- What was tried: {PREVIOUS_ATTEMPTS}

Provide:
1. Root cause analysis
2. Step-by-step fix
3. Prevention measures
```

### Optimize Build Time

```
My Docker build is slow. Help optimize:

Dockerfile:
```dockerfile
{DOCKERFILE}
```

Current build time: {TIME}
CI/CD platform: {PLATFORM}

Analyze:
1. Layer caching issues
2. Unnecessary operations
3. Network fetches
4. Build context size

Provide optimized Dockerfile with expected improvements.
```

### Reduce Image Size

```
Help reduce Docker image size:

Current image: {IMAGE_NAME}
Current size: {SIZE}
Target size: {TARGET_SIZE}

Dockerfile:
```dockerfile
{DOCKERFILE}
```

Strategies to explore:
1. Base image alternatives
2. Multi-stage build improvements
3. Dependency pruning
4. Static linking
5. Compression techniques
```

## Migration

### Migrate from Docker to Kubernetes

```
Create Kubernetes manifests from this Docker Compose:

```yaml
{DOCKER_COMPOSE}
```

Generate:
1. Deployment manifests
2. Service manifests
3. ConfigMaps for environment
4. Secrets template
5. PersistentVolumeClaims
6. Ingress (if applicable)

Include:
- Resource requests/limits
- Health checks (readiness/liveness)
- Rolling update strategy
- Security contexts
```

### Migrate Legacy App to Container

```
Help containerize this legacy application:

Application: {APP_DESCRIPTION}
Language: {LANGUAGE}
Dependencies: {DEPENDENCIES}
Configuration: {CONFIG_FILES}
Data storage: {DATA_PATHS}

Current deployment: {CURRENT_METHOD}

Provide:
1. Containerization strategy
2. Dockerfile
3. Docker Compose (if multi-service)
4. Migration steps
5. Potential issues and solutions
```

## CI/CD Integration

### Create CI Pipeline for Docker

```
Create a CI pipeline for Docker builds:

CI platform: {PLATFORM} (GitHub Actions/GitLab CI/Jenkins)
Registry: {REGISTRY}
Testing requirements: {TESTS}
Deployment target: {TARGET}

Pipeline should include:
1. Build and tag image
2. Run tests
3. Security scan
4. Push to registry
5. Deploy (optional)

Include caching strategies and parallel execution where possible.
```

### Add Security Scanning

```
Add container security scanning to this CI pipeline:

```yaml
{CURRENT_PIPELINE}
```

Tools to integrate:
- Trivy (vulnerability scanning)
- Docker Scout (recommendations)
- Hadolint (Dockerfile linting)

Configuration:
- Fail on HIGH/CRITICAL vulnerabilities
- Generate SBOM
- Report to security dashboard
```

## Architecture Review

### Review Container Architecture

```
Review this container architecture:

Services:
{SERVICE_LIST}

docker-compose.yml:
```yaml
{COMPOSE}
```

Review for:
1. Service boundaries
2. Communication patterns
3. Data persistence strategy
4. Scaling considerations
5. Security isolation
6. Monitoring/logging approach

Provide recommendations with priority (HIGH/MEDIUM/LOW).
```

### Design Multi-Container Application

```
Design container architecture for:

Application: {APP_DESCRIPTION}
Expected load: {TRAFFIC}
Availability requirements: {SLA}
Team size: {TEAM_SIZE}

Constraints:
{CONSTRAINTS}

Provide:
1. Service breakdown
2. Container specifications
3. Communication patterns
4. Data flow diagram
5. Scaling strategy
6. docker-compose.yml or K8s manifests
```

## Prompt Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{LANGUAGE}` | Programming language | Python, Node.js, Go |
| `{FRAMEWORK}` | Application framework | Django, FastAPI, Express |
| `{APP_DESCRIPTION}` | What the app does | REST API for user management |
| `{ENTRY_POINT}` | Main file/command | main.py, server.js |
| `{PORT}` | Exposed port | 8000, 3000 |
| `{DATABASE_TYPE}` | Database system | PostgreSQL, MongoDB |
| `{DOCKERFILE}` | Current Dockerfile content | Full Dockerfile text |
| `{COMPOSE}` | Docker Compose content | Full YAML content |
| `{ERROR_MESSAGE}` | Error to debug | Build or runtime error |
| `{PLATFORM}` | CI/CD platform | GitHub Actions |
| `{REGISTRY}` | Container registry | Docker Hub, ECR |
| `{SIZE}` | Current image size | 1.2GB |
| `{TARGET_SIZE}` | Desired image size | <200MB |
