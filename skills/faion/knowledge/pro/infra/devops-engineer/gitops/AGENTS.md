---
slug: gitops
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GitOps uses a Git repository as the single source of truth for declarative infrastructure and applications.
content_id: "35cf187783ef05c1"
tags: [gitops, kubernetes, argocd, fluxcd, infrastructure]
---
# GitOps

## Summary

**One-sentence:** GitOps uses a Git repository as the single source of truth for declarative infrastructure and applications.

**One-paragraph:** GitOps uses a Git repository as the single source of truth for declarative infrastructure and applications. A pull-based operator (ArgoCD, FluxCD) running inside the cluster continuously reconciles live state with the desired state in Git, providing automatic drift detection and correction. The recommended pattern is hybrid: CI pipeline builds and pushes image tags / manifest updates to Git; the GitOps agent pulls and applies. Use folders (not branches) for environment separation.

## Applies If (ALL must hold)

- Kubernetes-native deployments requiring drift detection and automatic reconciliation.
- Multi-cluster/multi-environment setups where consistency must be enforced.
- Compliance or audit requirements where every config change needs a Git trail.
- Progressive delivery (canary/blue-green) with automated metric-driven promotion.

## Skip If (ANY kills it)

- Non-containerized legacy systems — GitOps tooling is Kubernetes-native.
- Teams with no Kubernetes experience — the learning curve adds cost before value.
- Tight deployment sequencing needs where push-based CI gives finer control.
- Small teams (<5 engineers) with a single environment and simple deploy pipeline.

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
