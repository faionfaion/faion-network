---
slug: gitlab-cicd
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GitLab CI/CD is an integrated pipeline platform built into GitLab, configured via.
content_id: "ec45d71f79f48a2c"
tags: [gitlab, cicd, pipelines, dag, deployment]
---
# GitLab CI/CD

## Summary

**One-sentence:** GitLab CI/CD is an integrated pipeline platform built into GitLab, configured via.

**One-paragraph:** GitLab CI/CD is an integrated pipeline platform built into GitLab, configured via .gitlab-ci.yml. Pipelines are defined with stages, jobs, rules, and DAG dependencies (needs:). Use rules: (not deprecated only/except) for conditional execution and needs: for parallelization across stage boundaries.

## Applies If (ALL must hold)

- Project is hosted on GitLab (cloud or self-managed).
- Pipeline needs parent-child or dynamic child pipelines (monorepo).
- Team needs built-in container registry without external tooling.
- GitLab-native environments and review apps are required.
- Security scanning without external CI integration is needed.

## Skip If (ANY kills it)

- Repository is on GitHub — use GitHub Actions instead (native integration).
- Organization already invested in Jenkins with shared libraries — migration cost may exceed benefit.
- Deployment target is exclusively managed by ArgoCD GitOps — push-based deploy conflicts with pull-based GitOps; trigger ArgoCD sync instead.

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
