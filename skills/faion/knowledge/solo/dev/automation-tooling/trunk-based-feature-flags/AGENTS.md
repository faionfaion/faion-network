---
slug: trunk-based-feature-flags
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Deploy incomplete features to production on trunk by hiding them behind flags.
content_id: "d5ed5cb89d43f42f"
tags: [trunk-based-development, feature-flags, dark-launch, keystone-interface, rollout]
---
# Feature Flags for Trunk-Based Development

## Summary

**One-sentence:** Deploy incomplete features to production on trunk by hiding them behind flags.

**One-paragraph:** Deploy incomplete features to production on trunk by hiding them behind flags. Keystone Interface and Dark Launch extend this: build parts incrementally without exposing them, then test with live traffic before enabling users. One flag = one task = one cleanup ticket.

## Applies If (ALL must hold)

- A feature requires more than one day to implement — wrap each increment behind a flag and merge daily.
- You want to test new backend logic with production traffic before switching users — use Dark Launch.
- A feature requires multiple sequential build parts where only the final wire-up exposes the functionality — use Keystone Interface.
- SDD task lifecycle: flag name matches task ID, cleanup ticket filed at flag creation.

## Skip If (ANY kills it)

- Feature flag infrastructure setup — see feature-flags-types-lifecycle and feature-flags-core-implementation for provider choice and evaluation engine.
- Mobile/desktop release gating where store review is the exposure gate, not a flag.
- Very small features completable in a single commit — adding flag overhead exceeds the benefit.
- Codebases with no automated tests — a broken flag state produces silent production failures with no safety net.

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
