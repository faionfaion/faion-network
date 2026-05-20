---
slug: docker-image-optimization
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reduce production Docker image size 70-90% and accelerate CI builds by applying multi-stage builds, strategic layer ordering, cache mounts,.
content_id: "5e733016f5dadd66"
tags: [docker, image-optimization, multi-stage-build, layer-caching, containerization]
---
# Docker Image Optimization

## Summary

**One-sentence:** Reduce production Docker image size 70-90% and accelerate CI builds by applying multi-stage builds, strategic layer ordering, cache mounts,.

**One-paragraph:** Reduce production Docker image size 70-90% and accelerate CI builds by applying multi-stage builds, strategic layer ordering, cache mounts, .dockerignore, and the smallest viable base image. These techniques compound: a 900 MB Python image becomes 50-120 MB with correct choices.

## Applies If (ALL must hold)

- Any production image — apply multi-stage builds by default.
- CI pipelines where build time exceeds 2 minutes — cache mounts and layer ordering cut most of that.
- Images exceeding 300 MB — switch base image variant first, then apply multi-stage.
- Repos with large node_modules, __pycache__, .venv, or target/ that end up in build context.
- Security-sensitive workloads where a smaller attack surface is required.

## Skip If (ANY kills it)

- Development-only images where fast iteration matters more than size — keep the full image and use bind mounts.
- Throwaway one-shot scripts where build overhead is not paid repeatedly.
- When the runtime requires build tools at runtime (e.g., native C extensions rebuilt on startup) — stay single-stage but document why.

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
