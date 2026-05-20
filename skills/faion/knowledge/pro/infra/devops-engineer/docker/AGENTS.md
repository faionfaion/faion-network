---
slug: docker
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Docker builds images in layers; each instruction creates a cached layer.
content_id: "06df1eeebc2e1c0b"
tags: [docker, containerization, layer-caching, multi-stage-builds, image-optimization]
---
# Docker Operations

## Summary

**One-sentence:** Docker builds images in layers; each instruction creates a cached layer.

**One-paragraph:** Docker builds images in layers; each instruction creates a cached layer. Multi-stage builds separate build-time tooling from the runtime image, reducing size 50-90%. Non-root user, health check, exec-form CMD/ENTRYPOINT, and no secrets in image layers are non-negotiable for production.

## Applies If (ALL must hold)

- Containerizing any application for local development or deployment
- Auditing an existing Dockerfile for security or size issues
- Setting up Docker Compose for multi-service local stacks
- Integrating Docker builds into CI/CD with scanning and signing

## Skip If (ANY kills it)

- Kubernetes deployments where Helm or Kustomize manage runtime config — Docker knowledge is a prerequisite but Dockerfile authoring is not the bottleneck
- Serverless functions (AWS Lambda, Cloud Run) — container packaging rules differ
- Windows-only applications without Linux compatibility

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/devops-engineer/`
