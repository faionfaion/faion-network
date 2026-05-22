---
slug: cd-pipelines
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structure as discrete jobs: build → integration → staging → E2E → production.
content_id: "00441a0053d61abf"
tags: [ci-cd, github-actions, deployment-strategy, dora-metrics, rollback]
---
# CD Pipelines and Deployment Strategies

## Summary

**One-sentence:** Structure as discrete jobs: build → integration → staging → E2E → production.

**One-paragraph:** Structure as discrete jobs: build → integration → staging → E2E → production. Choose a deployment strategy: rolling, blue/green, or canary. Always emit DORA events with version, sha, and duration for observability.

## Applies If (ALL must hold)

- Authoring or refactoring .github/workflows/cd.yml (or GitLab CI / Buildkite equivalent) for a service.
- Adding deployment-strategy primitives: blue/green, canary, rolling with proper readiness/liveness probes.
- Wiring smoke tests, rollback triggers, deployment notifications, and DORA metric tracking.
- Replacing ad-hoc deploy-gh.sh scripts with observable, gated pipelines.

## Skip If (ANY kills it)

- Pure CI (build + test only) — this is CD-specific; see cd-basics for CI principles.
- Full platform engineering (multi-cluster, cross-region, GitOps with Argo/Flux) — use pro/infra/cicd-engineer.
- Serverless deploys managed by the vendor (Vercel, Netlify, Cloud Run) — those only need build config.
- Monorepo selective deploys per package — requires Turborepo/Nx-aware pipelines not covered here.

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

- parent skill: `solo/dev/automation-tooling/`
