---
slug: jenkins-pipelines
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Declarative Jenkins pipelines for production CI/CD: parallel stages, Kubernetes pod agents, shared libraries, and multi-environment deployment with manual approval gates.
content_id: "bd5eaa1e821029c1"
tags: [jenkins, pipelines, ci-cd, declarative, kubernetes]
---
# Jenkins Pipelines

## Summary

**One-sentence:** Declarative Jenkins pipelines for production CI/CD: parallel stages, Kubernetes pod agents, shared libraries, and multi-environment deployment with manual approval gates.

**One-paragraph:** Declarative Jenkins pipelines for production CI/CD: parallel stages, Kubernetes pod agents, shared libraries, and multi-environment deployment with manual approval gates. Default to declarative syntax; use scripted only for dynamic logic (e.g., detecting changed services in a monorepo).

## Applies If (ALL must hold)

- CI/CD pipelines on an existing Jenkins installation
- Multi-environment deployments requiring human approval gates before production
- Monorepo builds that need to detect changed services and build only those
- Containerized builds requiring isolated, disposable Kubernetes pod agents

## Skip If (ANY kills it)

- New projects without existing Jenkins investment — prefer GitHub Actions or GitLab CI
- Simple single-step builds — overhead of Jenkins setup is not justified
- When you need native OIDC cloud auth without plugins — Jenkins requires plugins for this
- GitOps-first workflows — ArgoCD/Flux are better fits than Jenkins for K8s GitOps

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
