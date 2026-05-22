---
slug: argocd-gitops
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: ArgoCD implements GitOps for Kubernetes: Git is the single source of truth for cluster state, ArgoCD continuously reconciles live state toward the desired Git state.
content_id: "46497c1ae1b79cc1"
tags: [gitops, argocd, kubernetes, continuous-deployment, declarative-infrastructure]
---
# ArgoCD GitOps for Kubernetes Deployments

## Summary

**One-sentence:** ArgoCD implements GitOps for Kubernetes: Git is the single source of truth for cluster state, ArgoCD continuously reconciles live state toward the desired Git state.

**One-paragraph:** ArgoCD implements GitOps for Kubernetes: Git is the single source of truth for cluster state, ArgoCD continuously reconciles live state toward the desired Git state. Use folders (not branches) to model environments. Use ApplicationSets to generate Applications across environments from a single template. Enable selfHeal: true to prevent configuration drift.

## Applies If (ALL must hold)

- Kubernetes workloads that need GitOps-controlled deployments.
- Multiple environments (dev/staging/prod) managed from a single repository.
- Multi-cluster management from a central control plane.
- Progressive delivery with Argo Rollouts (canary, blue-green).
- Teams that require deployment audit trail via Git history.

## Skip If (ANY kills it)

- Non-Kubernetes deployments — ArgoCD only targets Kubernetes clusters.
- Single-developer project with simple kubectl apply — GitOps overhead is not justified.
- Workflows where the build artifact (Docker image) needs to be deployed immediately without a Git commit to update the image tag — requires a separate image-update automation step (Argo CD Image Updater or CI commit).
- Environments where Git access from the cluster is not possible (air-gapped without Git mirror).

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
