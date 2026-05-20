---
slug: gha-deployment-patterns
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structure CD pipelines as staged deploy jobs (staging auto, production manual approval) backed by GitHub Environments.
content_id: "ddbbc3f1be8e7d48"
tags: [github-actions, cd, deployment, reusable-workflows, release]
---
# GitHub Actions Deployment Patterns

## Summary

**One-sentence:** Structure CD pipelines as staged deploy jobs (staging auto, production manual approval) backed by GitHub Environments.

**One-paragraph:** Structure CD pipelines as staged deploy jobs (staging auto, production manual approval) backed by GitHub Environments. Extract shared deploy logic into reusable workflows called with workflow_call and shared steps into composite actions. For production, implement canary (10% traffic, metrics gate, full rollout) or blue-green (swap load balancer after validation). Release workflows trigger on version tags and publish packages plus Docker images.

## Applies If (ALL must hold)

- Any push to main that should automatically deploy to staging and optionally to production after review.
- Organisations with multiple service repos that share the same deploy target (K8s cluster, ECS, Vercel org).
- Release pipelines that must publish npm/PyPI packages and Docker images together on a version tag.
- Workflows that need to deploy to more than two environments (dev, staging, prod) with different approval requirements.

## Skip If (ANY kills it)

- Long-running batch jobs exceeding GHA's 6-hour job limit — use Argo Workflows or Airflow instead.
- Deployments requiring shared mutable state between jobs — GHA jobs run on isolated runners; passing large state via artifacts is slow and fragile.
- Heavy parallel fanout (1000+ jobs at once) — GHA concurrency limits and queuing cause stalls; use BuildKit cluster or Buildbarn.
- Repos on GitLab/Bitbucket — a GHA mirror creates a dual source of truth and fragments PR review.

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
