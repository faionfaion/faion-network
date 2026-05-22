---
slug: embeddings-production-ops
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Running embedding systems in production requires attention to latency SLOs, rate limit handling, cost tracking, fault tolerance, and model migration.
content_id: "1cbcd8c94076aef9"
tags: [embeddings, production, monitoring, debugging, cost-optimization]
---
# Embedding System Production Operations

## Summary

**One-sentence:** Running embedding systems in production requires attention to latency SLOs, rate limit handling, cost tracking, fault tolerance, and model migration.

**One-paragraph:** Running embedding systems in production requires attention to latency SLOs, rate limit handling, cost tracking, fault tolerance, and model migration. The most common production failure modes are embedding drift (model version mismatch), silent token truncation, and missing monitoring until costs spike. Set up monitoring before launch, not after.

## Applies If (ALL must hold)

- Setting up monitoring and alerting for a new embedding pipeline.
- Debugging poor retrieval quality in production.
- Planning a model migration or version update.
- Optimizing costs as embedding volume grows.
- Hardening a prototype for production deployment.

## Skip If (ANY kills it)

- Early prototype with under 1000 documents — apply basic patterns from embeddings-provider-apis first.

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

- parent skill: `geek/ai/ml-engineer/`
