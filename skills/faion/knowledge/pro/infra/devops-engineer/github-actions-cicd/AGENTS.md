---
slug: github-actions-cicd
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GitHub Actions automates workflows defined in `.
content_id: "2cbc20881e78590e"
tags: [github-actions, ci-cd, workflow, security, automation]
---
# GitHub Actions CI/CD

## Summary

**One-sentence:** GitHub Actions automates workflows defined in `.

**One-paragraph:** GitHub Actions automates workflows defined in `.github/workflows/` YAML files, triggered by push, pull_request, schedule, and other events. The critical security rule: pin every third-party action to a full commit SHA, not a mutable tag. Always set explicit `permissions:` blocks at workflow or job level, defaulting to `contents: read`.

## Applies If (ALL must hold)

- Repository is hosted on GitHub
- Project needs matrix builds across OS/versions/runtimes
- Team wants OIDC-based credentialless cloud authentication
- Open source project needs free CI minutes
- Workflows must trigger on GitHub-native events (PR, release, issue)

## Skip If (ANY kills it)

- Repository is on GitLab — use GitLab CI/CD instead
- Deployment is GitOps/ArgoCD-managed — trigger ArgoCD sync rather than kubectl in Actions
- Highly regulated environment requires runners on-prem and GitHub.com is not approved — self-hosted runners add operational burden; evaluate Jenkins or GitLab self-managed
- `pull_request_target` needed with untrusted fork code — high injection risk; use carefully

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
