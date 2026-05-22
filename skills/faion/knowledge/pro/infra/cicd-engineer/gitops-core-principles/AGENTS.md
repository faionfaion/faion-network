---
slug: gitops-core-principles
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GitOps uses Git repositories as the single source of truth for declarative infrastructure and applications.
content_id: "26dc5abf47b843ea"
tags: [gitops, argocd, flux, kubernetes, ci-cd]
---
# GitOps Core Principles

## Summary

**One-sentence:** GitOps uses Git repositories as the single source of truth for declarative infrastructure and applications.

**One-paragraph:** GitOps uses Git repositories as the single source of truth for declarative infrastructure and applications. All cluster state is described in Git, applied by an in-cluster operator (pull model), and continuously reconciled — eliminating manual deployments, configuration drift, and unreliable releases.

## Applies If (ALL must hold)

- Migrating a Kubernetes (or Helm/Kustomize-managed) workload off kubectl apply and CI-driven pushes onto a pull-based reconciler (ArgoCD or Flux).
- Multi-cluster fleet management — single source of truth for 10+ clusters with environment promotion via PRs.
- Compliance / audit-heavy environments where every cluster change must be traceable to a Git commit and reviewer.
- Drift detection and self-healing of cluster state.
- Teams wanting to separate CI (build/test) from CD (deploy) cleanly.

## Skip If (ANY kills it)

- Non-declarative workloads (one-off scripts, ad-hoc data jobs) — use a CI pipeline, not GitOps.
- Single small cluster with one developer and no compliance pressure — overhead exceeds benefit.
- Stateful migrations with manual data steps — GitOps tools won't orchestrate "drain, snapshot, restore" sequencing; use a custom operator or runbook.
- Tight imperative sequencing (deploy A, wait for hook, then B, then C) where push-based pipelines are simpler.

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
