---
slug: devops-elk-index-management
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Index templates define field mappings and settings for all matching indices before they are created.
content_id: "0225f28694ef05e1"
tags: [elasticsearch, ilm, index-management, logging, devops]
---
# Elasticsearch Index Lifecycle Management and Templates

## Summary

**One-sentence:** Index templates define field mappings and settings for all matching indices before they are created.

**One-paragraph:** Index templates define field mappings and settings for all matching indices before they are created. ILM (Index Lifecycle Management) automates the hot-rollover-warm-cold-delete lifecycle. Rollover aliases provide a write-stable endpoint that persists across index generations. Together these three primitives replace all manual index management.

## Applies If (ALL must hold)

- Any production Elasticsearch cluster receiving time-series logs with a defined retention period.
- Setting up a new log source that will grow beyond a single index over time.
- Migrating from daily index naming (logs-2025.01.15) to size-based rollover.
- Reducing storage costs by moving aging data to warm/cold tiers automatically.

## Skip If (ANY kills it)

- Development or throwaway clusters with no retention requirement — plain indices without ILM are simpler.
- Static datasets (imported once, never updated) — snapshot/restore is a better fit than ILM lifecycle management.

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

- parent skill: `pro/infra/devops-engineer/`
