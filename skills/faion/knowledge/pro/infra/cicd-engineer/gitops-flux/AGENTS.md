---
slug: gitops-flux
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Flux is a lightweight, modular GitOps operator for Kubernetes.
content_id: "f1239c4f2da90671"
tags: [flux, gitops, kubernetes, helm, kustomize]
---
# Flux CD Setup and Operation

## Summary

**One-sentence:** Flux is a lightweight, modular GitOps operator for Kubernetes.

**One-paragraph:** Flux is a lightweight, modular GitOps operator for Kubernetes. It uses CRDs (GitRepository, Kustomization, HelmRelease, ImagePolicy) to reconcile cluster state from one or more Git/Helm sources. Flux excels at multi-tenancy, automation, and environments without a built-in UI requirement.

## Applies If (ALL must hold)

- Platform engineering teams building automation-first GitOps pipelines where a web UI is not required.
- Multi-tenant platforms where each tenant needs isolated source and reconciliation controllers.
- Existing Flux deployments being maintained or extended post-Weaveworks shutdown.
- Environments with resource constraints where ArgoCD's footprint is prohibitive.
- Helm-heavy clusters needing automated image tag updates via ImagePolicy + ImageUpdateAutomation.

## Skip If (ANY kills it)

- Teams requiring a built-in visual UI for day-to-day operations — use ArgoCD or pair Flux with Weave GitOps OSS UI.
- Organizations needing strong commercial support with SLA — ArgoCD's Akuity offering is more mature.
- Teams new to GitOps who need a gentler learning curve — ArgoCD's UI accelerates onboarding.

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
