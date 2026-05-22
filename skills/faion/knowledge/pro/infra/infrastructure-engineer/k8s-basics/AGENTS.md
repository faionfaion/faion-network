---
slug: k8s-basics
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Core kubectl operations, pods, services, namespaces, and fundamental concepts for running containers at scale with reliability and efficiency.
content_id: "52deb0eaf95e1351"
tags: [kubernetes, kubectl, containers, k8s, orchestration]
---
# Kubernetes Basics

## Summary

**One-sentence:** Core kubectl operations, pods, services, namespaces, and fundamental concepts for running containers at scale with reliability and efficiency.

**One-paragraph:** Core kubectl operations, pods, services, namespaces, and fundamental concepts for running containers at scale with reliability and efficiency. Kubernetes (K8s) is the bedrock of modern container orchestration. Version requirements: Kubernetes 1.29+ (prefer 1.31+), kubectl matching cluster version, Helm 3.14+, Kustomize built into kubectl 1.14+.

## Applies If (ALL must hold)

- Running multiple containerized services that need independent scaling, fault isolation, and rolling deployments.
- Production workloads that require automatic failure recovery — pod restart, node replacement, and traffic rerouting.
- Teams managing more than a handful of services where per-service deployment scripts become unmanageable.
- Applications needing horizontal pod autoscaling based on CPU, memory, or custom metrics.
- Multi-tenant platforms where namespace-level resource isolation and RBAC are required.
- CI/CD pipelines that need ephemeral build and test environments on-demand.

## Skip If (ANY kills it)

- Single-service applications where Docker Compose or a PaaS (Heroku, Render, Railway) is simpler to operate.
- Batch or scheduled jobs with no concurrency requirements — a simple cron job on a VM may suffice.
- Teams without K8s operational experience and no time to invest in the learning curve — managed container services (ECS Fargate, Cloud Run) offer a lower operational burden.

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
