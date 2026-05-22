---
slug: docker
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-Grade Container Development and Deployment (2025-2026).
content_id: "06df1eeebc2e1c0b"
tags: [docker, containers, dockerfile, security, devops]
---
# Docker Infrastructure

## Summary

**One-sentence:** Production-Grade Container Development and Deployment (2025-2026).

**One-paragraph:** Production-Grade Container Development and Deployment (2025-2026). Docker containerization packages applications with dependencies into portable units. This methodology covers production-grade Docker infrastructure: image building, optimization, networking, storage, security hardening, and deployment best practices.

## Applies If (ALL must hold)

- Packaging applications with all dependencies into portable, reproducible units.
- Building multi-stage CI/CD pipelines where images are built, scanned, signed, and promoted.
- Running multi-service stacks locally with Docker Compose during development.
- Deploying stateless workloads to any container-compatible runtime (ECS, Cloud Run, K8s).
- Enforcing security baselines: non-root users, read-only filesystems, capability dropping.

## Skip If (ANY kills it)

- Stateful workloads that require direct hardware access or kernel-level features incompatible with container isolation.
- Production orchestration at scale — use Kubernetes or managed container services instead of raw Docker Swarm.
- Legacy applications that cannot be containerized without significant refactoring (e.g., apps requiring GUI, complex COM/DCOM on Windows).

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

- parent skill: `pro/infra/infrastructure-engineer/`
