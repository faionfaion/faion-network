---
slug: helm-charts
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Helm is the package manager for Kubernetes (v4+ as of 2026).
content_id: "4241bbaf3ffb9121"
tags: [helm, kubernetes, charts, package-management, production-reliability]
---
# Helm Charts

## Summary

**One-sentence:** Helm is the package manager for Kubernetes (v4+ as of 2026).

**One-paragraph:** Helm is the package manager for Kubernetes (v4+ as of 2026). Charts bundle related K8s resources into configurable, versioned packages. Every production chart must include: resource requests/limits, HPA, PodDisruptionBudget, pod anti-affinity, all three health probes, and a non-root security context.

## Applies If (ALL must hold)

- Complex applications with many K8s resources across multiple environments
- Reusable deployment packages shared across teams or clusters
- GitOps workflows (ArgoCD, Flux) where charts are the unit of change
- Multi-environment deploys with per-environment values-{env}.yaml files

## Skip If (ANY kills it)

- Quick experiments or learning — plain YAML is simpler
- Small, static setups with no variation across environments — use Kustomize
- Single-resource deployments — overhead not justified
- When you want Helm to manage secrets — use External Secrets Operator instead

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
