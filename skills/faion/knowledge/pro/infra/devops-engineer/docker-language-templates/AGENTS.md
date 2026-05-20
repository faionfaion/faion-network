---
slug: docker-language-templates
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Copy-paste Dockerfile and Docker Compose templates for the most common language and framework combinations.
content_id: "76aa0421b86a5830"
tags: [docker, dockerfile, docker-compose, templates, containerization]
---
# Docker Language Templates

## Summary

**One-sentence:** Copy-paste Dockerfile and Docker Compose templates for the most common language and framework combinations.

**One-paragraph:** Copy-paste Dockerfile and Docker Compose templates for the most common language and framework combinations. Every template uses multi-stage builds, non-root users, HEALTHCHECK instructions, and pinned base images. Pick the template matching your stack and apply the optimization and security methodologies on top.

## Applies If (ALL must hold)

- Bootstrapping a new service — copy the matching template and customize entry point and port.
- Auditing an existing Dockerfile against best practices — compare line-by-line with the reference template.
- Onboarding junior engineers — templates serve as canonical examples that encode team standards.

## Skip If (ANY kills it)

- When the language or framework is not listed — derive from the generic multi-stage template and document the specialization.
- When the app has unusual runtime requirements (GPU, FUSE mounts, privileged sockets) — start from the template but expect significant adaptation.

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
