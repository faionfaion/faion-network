---
slug: nosql-mongodb-patterns
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design MongoDB schemas around access patterns, not entity diagrams.
content_id: "c9559486c88e6576"
tags: [mongodb, nosql, document-store, data-modeling, indexing]
---
# MongoDB Document Design Patterns

## Summary

**One-sentence:** Design MongoDB schemas around access patterns, not entity diagrams.

**One-paragraph:** Design MongoDB schemas around access patterns, not entity diagrams. Choose embedding for 1:few relationships accessed together, referencing for 1:many or many:many. Use the bucket pattern for time-series. Always index query fields and add a schemaVersion field for evolution.

## Applies If (ALL must hold)

- Hierarchical or nested data structures where parent and children are always accessed together (1:few embedding).
- High-volume document workloads with flexible or evolving schemas.
- Time-series or sensor data where the bucket pattern aggregates measurements per time window.
- Full-text search requirements co-located with document data (text indexes).
- Session storage, content management, catalog systems with heterogeneous attributes.

## Skip If (ANY kills it)

- Strong-consistency multi-document transactions that touch many collections — Postgres handles this without two-phase commit overhead.
- Ad-hoc analytical queries with unknown access patterns — warehouse/lakehouse is a better fit.
- Small datasets (<100 GB, low QPS) where Postgres + JSONB provides the same flexibility without an extra engine.
- Reporting and BI surfaces — operational MongoDB stores should not serve analytical queries directly.

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

- parent skill: `pro/dev/backend-systems/`
