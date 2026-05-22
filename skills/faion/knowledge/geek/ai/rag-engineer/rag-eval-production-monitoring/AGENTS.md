---
slug: rag-eval-production-monitoring
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production RAG monitoring logs latency, source count, and user feedback for every query, aggregates rolling summaries (24h default window), and detects anomalies against calibrated thresholds.
content_id: "8b55e4dd0985027a"
tags: [rag, monitoring, production, observability]
---
# RAG Production Monitoring

## Summary

**One-sentence:** Production RAG monitoring logs latency, source count, and user feedback for every query, aggregates rolling summaries (24h default window), and detects anomalies against calibrated thresholds.

**One-paragraph:** Production RAG monitoring logs latency, source count, and user feedback for every query, aggregates rolling summaries (24h default window), and detects anomalies against calibrated thresholds. Lightweight metrics (latency, hit rate, user signals) run on every query; expensive LLM-based evaluation (faithfulness, relevance) runs only on sampled batches. Anomaly thresholds must be calibrated against actual production baselines — hardcoded defaults are placeholders only.

## Applies If (ALL must hold)

- Any RAG system deployed to production with real user traffic.
- When user feedback signals (thumbs up/down, explicit ratings) are available in the product UI.
- When you need to detect sudden latency spikes (embedding model timeout, vector DB overload).
- When the corpus is updated regularly and quality drift is expected.

## Skip If (ANY kills it)

- High-frequency real-time LLM evaluation of every query — reserve LLM eval for sampled batches only; use lightweight metrics (latency, hit rate) for every query.
- When user feedback is too sparse (fewer than 10 signals per day) for anomaly detection to be reliable — rely on scheduled batch eval instead.

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

- parent skill: `geek/ai/rag-engineer/`
