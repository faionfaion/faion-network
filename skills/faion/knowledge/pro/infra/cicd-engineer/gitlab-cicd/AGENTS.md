---
slug: gitlab-cicd
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GitLab CI/CD is an integrated DevSecOps platform using.
content_id: "ec45d71f79f48a2c"
tags: [gitlab-ci, cicd, dag, devsecops, pipelines]
---
# GitLab CI/CD

## Summary

**One-sentence:** GitLab CI/CD is an integrated DevSecOps platform using.

**One-paragraph:** GitLab CI/CD is an integrated DevSecOps platform using .gitlab-ci.yml to define pipelines with stages, jobs, rules, and environments. Use DAG with the needs keyword to replace sequential stages and achieve parallelism. Never store secrets in .gitlab-ci.yml — use protected, masked CI/CD variables. GitLab 18 (2025) adds immutable artifact tags and structured pipeline inputs.

## Applies If (ALL must hold)

- Projects hosted on GitLab (cloud or self-hosted)
- Teams needing integrated DevSecOps: SAST, DAST, dependency scanning, secret detection
- Multi-environment deployments with review apps per merge request
- Monorepo projects with change-based job filtering (rules: changes)
- Organizations tracking DORA metrics natively

## Skip If (ANY kills it)

- Repositories hosted on GitHub — use GitHub Actions instead
- Simple single-developer projects — overhead of .gitlab-ci.yml is not justified; use a Makefile
- Projects requiring Jenkins-level plugin customization not available in GitLab

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
