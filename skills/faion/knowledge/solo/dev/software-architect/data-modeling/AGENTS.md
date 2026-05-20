---
slug: data-modeling
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Build any persistent schema in three sequential passes: conceptual (entities/relationships in business terms) → logical (attributes, keys, cardinality, normalized to 3NF, technology-agnostic) → physical (tables, exact data types, indexes, partitions, engine-specific constraints).
content_id: "68c014492b30f9ea"
tags: [data-modeling, database-design, schema-design, normalization, paradigm-selection, indexing, partitioning]
---
# Data Modeling

## Summary

**One-sentence:** Build any persistent schema in three sequential passes: conceptual (entities/relationships in business terms) → logical (attributes, keys, cardinality, normalized to 3NF, technology-agnostic) → physical (tables, exact data types, indexes, partitions, engine-specific constraints).

**One-paragraph:** Build any persistent schema in three sequential passes: conceptual (entities/relationships in business terms) → logical (attributes, keys, cardinality, normalized to 3NF, technology-agnostic) → physical (tables, exact data types, indexes, partitions, engine-specific constraints). Skipping the logical pass is the dominant cause of unmaintainable schemas and expensive migrations.

## Applies If (ALL must hold)

- Designing any new persistent data layer (greenfield service, new bounded context, or migration from legacy).
- Choosing between database paradigms (relational, document, wide-column, key-value, graph, time-series, vector, search).
- Normalizing an existing schema that exhibits update anomalies, JSON-blob misuse, or column duplication.
- Adding an index strategy or partitioning plan before a table grows beyond ~10M rows or ~10 GB.
- Refactoring a schema before introducing a write-heavy feature (events, audit logs, telemetry).
- Performing an Architecture Decision Record (ADR) for storage choice or denormalization.

## Skip If (ANY kills it)

- Throwaway prototypes whose data will not be migrated to production — pick any paradigm and move on.
- Read-only analytical sandboxes already covered by a star/snowflake schema in a warehouse.
- Pure caching layers (Redis, Memcached) where the source of truth lives elsewhere.

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

- parent skill: `solo/dev/software-architect/`
