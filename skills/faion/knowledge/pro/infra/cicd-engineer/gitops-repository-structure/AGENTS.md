---
slug: gitops-repository-structure
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The config repository layout is the foundation of a maintainable GitOps setup.
content_id: "adfa87c93c5f77fe"
tags: [gitops, kustomize, helm, repository-structure, kubernetes]
---
# GitOps Repository Structure

## Summary

**One-sentence:** The config repository layout is the foundation of a maintainable GitOps setup.

**One-paragraph:** The config repository layout is the foundation of a maintainable GitOps setup. Use folder-per-environment in a monorepo with Kustomize base/overlays or Helm value files. Avoid branch-per-environment — it creates merge complexity and makes promotions difficult.

## Applies If (ALL must hold)

- Setting up a new GitOps config repository for one or more Kubernetes clusters.
- Migrating from a branch-per-environment workflow to a maintainable structure.
- Onboarding a new team or application into an existing GitOps platform.
- Defining environment promotion strategy (dev to staging to prod via PRs).

## Skip If (ANY kills it)

- Single-application, single-environment repos where the monorepo layout adds unnecessary complexity — use a flat structure.
- Non-Kubernetes workloads (bare VMs, serverless) where Kustomize/Helm overlays don't apply.

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
