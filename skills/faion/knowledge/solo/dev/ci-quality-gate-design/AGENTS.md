---
slug: ci-quality-gate-design
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "1e41f08387a7fcc1"
summary: Opinionated design pattern for CI quality gates — which checks block, which warn, which run nightly — with a budget framework that keeps PR time under control.
tags: [ci-cd, quality-gates, devex, build-budget, qa-engineer]
---
# CI Quality Gate Design

## Summary

**One-sentence:** An opinionated three-tier design (BLOCK / WARN / NIGHTLY) plus a per-PR time budget that stops teams from re-inventing which checks should fail the build versus comment on it.

**One-paragraph:** Every new project re-debates "should mutation testing block merge?" / "is 90% coverage a gate?" / "should the security scan fail on medium?". The result is either over-blocking (PRs sit for 25 minutes for low-signal checks) or under-blocking (security and contract tests run in a tab nobody opens). This methodology pins a three-tier classification (BLOCK = must pass, WARN = surfaces a comment, NIGHTLY = runs on schedule with alert) and a per-PR wall-clock budget (target &lt; 10 min, ceiling 15 min for solo teams). It also enforces a written tier rationale per check, so future debates start from "what changed?" not from scratch. Output: ci-design.md committed alongside the CI config, reviewed when gates change.

## Applies If (ALL must hold)

- Project has a CI/CD pipeline (GitHub Actions, GitLab CI, CircleCI, Buildkite, etc.).
- More than one developer (or solo dev who plans to onboard contributors).
- At least 3 categories of checks present (lint, test, security, type-check, build, etc.).
- PR cycle-time is a felt pain or anticipated to be.

## Skip If (ANY kills it)

- Single-person hobby project with no scaling intent — design overhead exceeds benefit.
- Highly regulated env (HIPAA, PCI L1) where the regulator dictates the gate list — adopt the regulator's pattern.
- Pipeline does not yet exist — set up basic CI first; gate design comes after the floor.
- Monorepo with hundreds of packages — needs the pro-tier delivery-ops gate methodology.

## Prerequisites

- Current CI config file (yaml or pipeline definition).
- A list of all current checks with their average runtime.
- Last 30 days of PR data (median time-to-merge, build failure attribution).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/ci-fundamentals` | Workflow syntax, jobs/steps assumed. |
| `solo/dev/testing-developer/test-strategy` | Knowing which tests run at which layer is a precondition. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: three-tier, written rationale, time budget, signal-not-noise, escalation path | ~900 |
| `content/02-output-contract.xml` | essential | ci-design.md shape; per-check row; budget arithmetic | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: block-everything, hide-the-warn, no-budget, etc. | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-existing-check` | sonnet | Apply tier rubric to a single check |
| `budget-runtime-analysis` | sonnet | Compute parallel + serial timings |
| `design-rationale-draft` | opus | Cross-check trade-off synthesis |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-design.md` | Skeleton with three-tier tables and budget section |
| `templates/check-rationale.md` | One-paragraph rationale template per check |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/pr-cycle-time.py` | Read git log + PR API to compute median cycle time over last N days | Monthly review |

## Related

- parent skill: `solo/dev/automation-tooling/`
- peer methodology: `ci-fundamentals`, `pre-commit-floor` (geek), `feature-flags`
- external: [Accelerate (Forsgren et al.)](https://nicolefv.com/book) · [DORA reports](https://dora.dev/)
