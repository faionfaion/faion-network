---
slug: database-selection
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Framework for choosing among 100+ databases.
content_id: "91da026146a06cff"
tags: [database, architecture, selection, cap-theorem, polyglot-persistence]
---
# Database Selection Guide

## Summary

**One-sentence:** Framework for choosing among 100+ databases.

**One-paragraph:** Framework for choosing among 100+ databases. Relational for ACID. NewSQL for distributed SQL. Document for flexible schema. KV for cache. Time-series for metrics. Graph for relationships. Vector for embeddings. Search for full-text.

## Applies If (ALL must hold)

- Designing any new persistent data layer (greenfield or migration).
- Choosing between paradigms: relational, document, wide-column, graph, time-series, vector, search.
- Normalizing an existing schema with update anomalies, hotspots, or data duplication.
- Modeling polyglot persistence: assigning each data domain to its optimal store.
- Reviewing a system that misses latency, throughput, or consistency SLOs.

## Skip If (ANY kills it)

- Existing database meets SLOs and team has operational expertise — do not swap.
- Prototype with <1k rows and no production traffic — default to PostgreSQL, decide later.
- Pure cache or session store — go straight to Redis without full selection cycle.

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
