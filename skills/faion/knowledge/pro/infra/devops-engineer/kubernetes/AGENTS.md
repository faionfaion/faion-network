---
slug: kubernetes
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Kubernetes production readiness requires: always set resource requests AND limits, configure liveness + readiness + startup probes, enforce runAsNonRoot: true + readOnlyRootFilesystem: true + allowPrivilegeEscalation: false + capabilities.
content_id: "81419648c7c4d695"
tags: [kubernetes, k8s, container-orchestration, production-readiness, security-context]
---
# Kubernetes

## Summary

**One-sentence:** Kubernetes production readiness requires: always set resource requests AND limits, configure liveness + readiness + startup probes, enforce runAsNonRoot: true + readOnlyRootFilesystem: true + allowPrivilegeEscalation: false + capabilities.

**One-paragraph:** Kubernetes production readiness requires: always set resource requests AND limits, configure liveness + readiness + startup probes, enforce runAsNonRoot: true + readOnlyRootFilesystem: true + allowPrivilegeEscalation: false + capabilities.drop: ["ALL"] on every container, and define a PodDisruptionBudget for every Deployment with more than one replica. Never use latest image tags in production.

## Applies If (ALL must hold)

- Deploying any containerized workload that needs horizontal scaling, rolling updates, or self-healing
- Multi-service application where service discovery via DNS is needed
- Workloads requiring persistent storage with automated provisioning
- Environments where GitOps (ArgoCD/Flux) manages the desired state

## Skip If (ANY kills it)

- Single-container application with no scaling needs — Docker Compose or a simple VM is simpler
- Stateful workloads with complex data replication not supported by a Kubernetes Operator — managed databases are a better fit
- Batch/ETL workload that runs infrequently — serverless (Cloud Run, Lambda) avoids paying for idle nodes
- Team has no Kubernetes operational experience and production SLO is tight — operational learning curve is high

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
