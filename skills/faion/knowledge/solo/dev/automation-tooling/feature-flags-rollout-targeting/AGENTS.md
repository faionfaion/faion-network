---
slug: feature-flags-rollout-targeting
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Gradual rollouts require deterministic per-user assignment: the same user must consistently see the same variant.
content_id: "dd66d4dd48a46293"
tags: [feature-flags, rollout, targeting, a-b-testing, progressive-delivery]
---
# Feature Flag Rollout and Targeting

## Summary

**One-sentence:** Gradual rollouts require deterministic per-user assignment: the same user must consistently see the same variant.

**One-paragraph:** Gradual rollouts require deterministic per-user assignment: the same user must consistently see the same variant. The canonical approach combines MD5 hash bucketing for percentage rollout with an explicit allowlist (user IDs) and group membership (beta_testers, employees) evaluated in priority order. Couple rollout percentage changes to error-rate alerts to enable automatic rollback.

## Applies If (ALL must hold)

- Gradual feature rollouts where you want 1% → 10% → 50% → 100% progression with monitoring at each step.
- Beta programs where specific employees or opted-in users always see the new feature before general availability.
- A/B experiments where each user must consistently see the same variant for the experiment to be statistically valid.
- Group-based feature access: beta_testers, employees, premium_tier — evaluated before the percentage bucket.

## Skip If (ANY kills it)

- Anonymous traffic where no stable user_id exists — you cannot maintain consistent assignment without a persistent identifier.
- Features that must be either fully on or fully off for all users simultaneously — use a simple boolean flag instead.
- High-volume paths where hash computation is too expensive — pre-evaluate at session start and cache in the request context.

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
