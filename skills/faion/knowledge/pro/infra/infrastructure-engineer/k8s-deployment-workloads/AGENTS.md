---
slug: k8s-deployment-workloads
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Kubernetes orchestrates containerized applications via Deployment (stateless) and StatefulSet (stateful) resources.
content_id: "9a536d1fb060dfdf"
tags: [kubernetes, deployment, statefulset, health-probes, production]
---
# Kubernetes Deployment and StatefulSet Workloads

## Summary

**One-sentence:** Kubernetes orchestrates containerized applications via Deployment (stateless) and StatefulSet (stateful) resources.

**One-paragraph:** Kubernetes orchestrates containerized applications via Deployment (stateless) and StatefulSet (stateful) resources. Every production workload requires correct resource requests/limits, all three health probes (startup, liveness, readiness), pod anti-affinity, and topology spread constraints to achieve zero-downtime updates and high availability.

## Applies If (ALL must hold)

- Deciding whether a workload needs Deployment or StatefulSet.
- Writing or reviewing a new Kubernetes manifest for production.
- Auditing an existing workload for missing probes or resource limits.
- Setting up pod scheduling constraints (anti-affinity, topology spread).

## Skip If (ANY kills it)

- Rolling update strategy tuning — covered in k8s-rolling-update.
- HPA / PDB autoscaling — covered in k8s-scaling-availability.
- Canary or progressive delivery — covered in k8s-canary-progressive.
- Security hardening (PSS, NetworkPolicy) — covered in k8s-security-hardening.

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
