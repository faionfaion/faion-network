---
slug: argocd-gitops
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: ArgoCD is a declarative GitOps CD tool for Kubernetes (used in approximately 60% of Kubernetes clusters per CNCF 2025).
content_id: "46497c1ae1b79cc1"
tags: [argocd, gitops, kubernetes, ci-cd, deployment]
---
# ArgoCD GitOps

## Summary

**One-sentence:** ArgoCD is a declarative GitOps CD tool for Kubernetes (used in approximately 60% of Kubernetes clusters per CNCF 2025).

**One-paragraph:** ArgoCD is a declarative GitOps CD tool for Kubernetes (used in approximately 60% of Kubernetes clusters per CNCF 2025). It synchronizes Kubernetes cluster state from Git, detects drift, and enables automated or manual sync with rollback. Key rules: keep app code and GitOps config in separate repos; use folders for environments (not branches); always use Helm or Kustomize (never raw YAML); use ApplicationSets to automate multi-env or multi-cluster deployments. Never run kubectl directly in production — all changes must go through Git.

## Applies If (ALL must hold)

- Kubernetes-native deployments requiring automated sync and drift detection.
- Multi-cluster deployments (ApplicationSet with Cluster generator).
- Teams adopting GitOps with PR-based change workflow for production.
- Progressive delivery with canary or blue/green (via Argo Rollouts).
- Projects that need deployment audit trail via Git commit history.
- Kubernetes-first deployments where Git is the desired source of truth, with declarative reconciliation and drift detection out of the box.
- Multi-cluster fleets (5-500 clusters) — ApplicationSet with cluster generators is the cleanest fan-out story available today.
- Multi-tenant platforms where teams own namespaces and need RBAC-isolated apps without giving them cluster-admin.
- Audit-heavy environments — every cluster change traceable to a Git commit with author/SHA/CI run.

## Skip If (ANY kills it)

- Non-Kubernetes workloads (VMs, serverless functions, legacy on-prem) — ArgoCD only manages Kubernetes resources.
- Single-developer projects with a single cluster — Helm + CI kubectl apply is simpler.
- When the team is not ready to treat Git as the only truth — partial adoption breaks the model.
- Non-Kubernetes workloads (VMs, serverless functions, on-prem bare metal). Use Flux for some of these or just Terraform/Pulumi.
- Tiny single-cluster deployments — kubectl apply -k ./manifests in CI is simpler and avoids running the ArgoCD control plane.
- Teams that want push-based deploys (kubectl apply from CI). ArgoCD is pull-based; mixing the two leads to constant fights.
- Workloads needing immediate sync from CI — pull interval (default 3 min) plus refresh latency means "deploy" is not instantaneous unless you wire webhooks correctly.

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

- parent skill: `pro/infra/cicd-engineer/`
