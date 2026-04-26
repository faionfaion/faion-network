# Docker Operations

## Summary

Docker builds images in layers; each instruction creates a cached layer. The single most impactful optimization is placing dependency installation before source code COPY so dependency layers are cached across code changes. Multi-stage builds separate build-time tooling from the runtime image, reducing size 50-90%. Non-root user, health check, exec-form CMD/ENTRYPOINT, and no secrets in image layers are non-negotiable for production.

## Why

Layer cache misses are the #1 cause of slow Docker builds. Large images (root user, no multi-stage, no distroless) expand the attack surface and slow rollouts. Using shell form for CMD/ENTRYPOINT prevents proper SIGTERM signal handling, causing ungraceful container shutdowns. Each anti-pattern has a concrete, testable fix.

## When To Use

- Containerizing any application for local development or deployment.
- Auditing an existing Dockerfile for security or size issues.
- Setting up Docker Compose for multi-service local stacks.
- Integrating Docker builds into CI/CD with scanning and signing.

## When NOT To Use

- Kubernetes deployments where Helm or Kustomize manage runtime config — Docker knowledge is a prerequisite but Dockerfile authoring is not the bottleneck.
- Serverless functions (AWS Lambda, Cloud Run) — container packaging rules differ.
- Windows-only applications without Linux compatibility.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Layer caching strategy, base image selection, CMD vs ENTRYPOINT, image optimization techniques, networking, volume types, anti-patterns |
| `content/02-checklists.xml` | Dockerfile quality, security, production readiness, Compose, multi-stage build, CI/CD integration checklists; quick audit commands |

## Templates

| File | Purpose |
|------|---------|
| `templates/Dockerfile.python` | Multi-stage Python production Dockerfile (slim base, non-root user, health check, exec form) |
| `templates/docker-compose.yml` | Compose template with named networks, volumes, depends_on health conditions, env overrides |
