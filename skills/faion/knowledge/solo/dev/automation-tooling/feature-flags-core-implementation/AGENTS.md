---
slug: feature-flags-core-implementation
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A FeatureFlagManager registers typed FeatureFlag dataclasses, loads overrides from environment variables (FF_* prefix) and a JSON config file, and exposes is_enabled(flag_name, user_id) as the single call site.
content_id: "80c1f4f991d15fc2"
tags: [feature-flags, python, implementation, decorator, middleware]
---
# Feature Flag Core Implementation

## Summary

**One-sentence:** A FeatureFlagManager registers typed FeatureFlag dataclasses, loads overrides from environment variables (FF_* prefix) and a JSON config file, and exposes is_enabled(flag_name, user_id) as the single call site.

**One-paragraph:** A FeatureFlagManager registers typed FeatureFlag dataclasses, loads overrides from environment variables (FF_* prefix) and a JSON config file, and exposes is_enabled(flag_name, user_id) as the single call site. The decorator pattern (@feature_flag) and a context-manager middleware layer are the two standard integration points for web frameworks.

## Applies If (ALL must hold)

- Building an in-process flag manager without a SaaS dependency (self-hosted, cost-sensitive, or offline-first).
- Wrapping an existing code path in a flag to enable progressive rollout of a new implementation.
- Adding a kill switch to a risky third-party integration that needs instant disable without redeploy.
- Integrating flag evaluation into a FastAPI or Django request lifecycle via middleware.

## Skip If (ANY kills it)

- Teams that need targeting rules, percentage rollout, or real-time flag updates without code deploys — use a dedicated service instead (see feature-flags-services-testing).
- Single env-var toggling that will never need targeting or rollout — direct os.getenv() is simpler.
- Cases where flag evaluation latency must be zero — compile the flag out at build time.

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
