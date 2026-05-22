---
slug: release-planning
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured approach to bundling, scheduling, and communicating product releases across cross-functional teams.
content_id: "68460e3733a2e87f"
tags: [release-planning, release-management, product-coordination, readiness-gate, cross-functional]
---
# Release Planning

## Summary

**One-sentence:** Structured approach to bundling, scheduling, and communicating product releases across cross-functional teams.

**One-paragraph:** Structured approach to bundling, scheduling, and communicating product releases across cross-functional teams. Defines what ships, when, to whom, and how readiness is verified per function (eng, docs, support, marketing, legal) before deploy. The PM-flavored variant adds a release-readiness matrix (green/yellow/red per function with evidence URLs) on top of basic engineering deploy mechanics — decoupling "code is done" from "release is ready".

## Applies If (ALL must hold)

- Multi-team release crossing engineering, support, sales-enablement, marketing, and legal.
- Releases with paying customers where breaking changes or deprecations are present.
- Release calendar has slipped twice in a row (signal: shrink contents, shorten cycle).
- Regulated or contractual deploy windows require customer-facing change-control artifacts.
- Pre-launch GTM coordination where sales decks, support macros, and pricing copy must sequence.
- Release-train cadence reviews where the PM owns whether the train left full or empty.

## Skip If (ANY kills it)

- Trunk-based / continuous deployment with feature flags at scale — use a launch plan tied to flag percentages instead.
- Pure infra/refactor with zero customer-visible behavior change.
- Solo founder shipping to fewer than 50 users — git push + changelog post is sufficient.
- A/B experiments — use experimentation-design, not a ship date.
- Hotfixes for live incidents — use the incident-response runbook; release-planning deliberation kills time-to-mitigate.

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

- parent skill: `pro/product/product-manager/`
