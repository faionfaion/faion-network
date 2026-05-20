---
slug: feature-flags-types-lifecycle
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Feature flags (feature toggles) allow you to modify system behavior without deploying new code.
content_id: "230a9879ed6eebcc"
tags: [feature-flags, progressive-rollout, trunk-based-dev, technical-debt, lifecycle]
---
# Feature Flag Types and Lifecycle

## Summary

**One-sentence:** Feature flags (feature toggles) allow you to modify system behavior without deploying new code.

**One-paragraph:** Feature flags (feature toggles) allow you to modify system behavior without deploying new code. Each flag has a category (release, experiment, ops, permission, kill-switch) that determines its expected lifespan, ownership, and cleanup obligation. Treating all flags identically causes flag debt — the single largest source of maintenance burden in toggle systems.

## Applies If (ALL must hold)

- Trunk-based development: hide incomplete features in production so main is always shippable.
- Progressive feature rollouts (1% to 10% to 50% to 100%) with automatic rollback on error-rate spike.
- A/B experiments where the experiment platform reads the same flag store as the app.
- Kill switches for risky integrations (third-party payments, AI calls) that can be flipped without redeploy.
- Per-tenant features (premium tier, beta access) with attribute-based targeting.
- Operational circuit breakers and maintenance-mode toggles.

## Skip If (ANY kills it)

- One-line config that never changes — env vars suffice; flags add unnecessary indirection.
- Database schema changes — flags cannot gate ALTER TABLE migrations safely.
- Permanent business rules that belong in domain logic, not toggles.
- Pre-production prototypes where the flag infrastructure complexity outweighs the value.
- Time-critical hot paths where even 1ms of flag-evaluation latency matters — compile out or cache.

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
