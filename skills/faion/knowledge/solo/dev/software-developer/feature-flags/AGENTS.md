---
slug: feature-flags
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Feature flags gate incomplete or experimental code behind runtime toggles, decoupling deployment from release.
content_id: "ead1a6734770941d"
tags: [feature-flags, release-management, trunk-based-dev, progressive-rollout, kill-switch]
---
# Feature Flags

## Summary

**One-sentence:** Feature flags gate incomplete or experimental code behind runtime toggles, decoupling deployment from release.

**One-paragraph:** Feature flags gate incomplete or experimental code behind runtime toggles, decoupling deployment from release. Flags enable trunk-based development (no long feature branches), progressive rollouts (1% → 10% → 50% → 100%), and instant rollback without redeployment. Flags must be short-lived (except ops/kill-switch types) and removed after full rollout to prevent flag debt.

## Applies If (ALL must hold)

- Trunk-based development: hide unfinished features behind release flags so main is always shippable.
- Progressive rollouts (1% → 10% → 50% → 100%) with auto-rollback on error/latency regression.
- A/B tests where the experiment platform reads the same flag store as the application.
- Kill switches for risky external dependencies (payments, AI inference, third-party APIs).
- Per-tenant or per-plan features (premium tier, beta access) gated by attribute targeting.
- Operational toggles (maintenance mode, circuit breaker, queue draining) flipped without redeploy.

## Skip If (ANY kills it)

- Static configuration that never changes per request — environment variables suffice.
- Schema migrations or storage shape changes — flags cannot gate ALTER TABLE safely; use migration tooling.
- Permanent business rules that belong in domain logic, not toggles (flags are temporary by definition).
- Pre-product prototypes where the abstraction cost outstrips the rollout value.
- Hot paths where every microsecond matters — compile flags out for those modules instead of evaluating at runtime.

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

- parent skill: `solo/dev/software-developer/`
