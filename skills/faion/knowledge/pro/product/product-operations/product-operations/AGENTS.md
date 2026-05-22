---
slug: product-operations
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A dedicated Product Ops function removes operational drag — process docs, tool plumbing, status updates, metric rollups, stakeholder comms — so PMs spend more time on discovery and strategy.
content_id: "da83746a670250be"
tags: [product-ops, operations, automation, metrics, process]
---
# Product Operations

## Summary

**One-sentence:** A dedicated Product Ops function removes operational drag — process docs, tool plumbing, status updates, metric rollups, stakeholder comms — so PMs spend more time on discovery and strategy.

**One-paragraph:** A dedicated Product Ops function removes operational drag — process docs, tool plumbing, status updates, metric rollups, stakeholder comms — so PMs spend more time on discovery and strategy. 96% of orgs now have this function; 50% report to CPO. Maturity runs from Level 1 (process docs) to Level 3 (AI automation). Agents are a near-perfect fit because Product Ops work is repetitive, system-of-record-driven, and benefits from deterministic automation.

## Applies If (ALL must hold)

- Solopreneur or small team where a human Product Ops hire isn't justified but the weekly operational tax (status updates, roadmap snapshots, metric rollups) still needs to be paid.
- Multi-product / multi-team setup with 3+ PMs working in different tools causing artifact drift.
- Migrating from ad-hoc PM workflows to a documented system.
- Pre-fundraise / board-prep cycles requiring recurring "state of product" packs from 5–10 sources.
- Org-wide release calendars, dependency maps, capacity planning across squads.

## Skip If (ANY kills it)

- A team with one PM and one product — the operational tax is too small; agent flows add more maintenance overhead than they save.
- During the first 30 days of a new product where workflows haven't stabilized.
- Strategic product decisions (pricing, positioning, kill/scale) — Product Ops enables those decisions, it does not make them.
- Heavily regulated environments where every status update has compliance implications.
- When PM tools have no public API — no API means no agents.

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

- parent skill: `pro/product/product-operations/`
