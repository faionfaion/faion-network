---
slug: cost-reduction-strategies
tier: geek
group: ai
domain: ml-ops
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production LLM cost optimization through four orthogonal techniques: response caching (SHA-256 content hash key, Redis or in-memory TTL), prompt compression (whitespace normalization, redundant phrase removal), async batching, and model routing (default cheap model with fallback).
content_id: "0d2e13aeef1e038f"
tags: [cost-optimization, llm-cost, prompt-caching, model-routing, batching]
---
# Cost Reduction Strategies

## Summary

**One-sentence:** Production LLM cost optimization through four orthogonal techniques: response caching (SHA-256 content hash key, Redis or in-memory TTL), prompt compression (whitespace normalization, redundant phrase removal), async batching, and model routing (default cheap model with fallback).

**One-paragraph:** Production LLM cost optimization through four orthogonal techniques: response caching (SHA-256 content hash key, Redis or in-memory TTL), prompt compression (whitespace normalization, redundant phrase removal), async batching, and model routing (default cheap model with fallback). The `CostOptimizedLLM` class composes all four into a single production-ready service layer.

## Applies If (ALL must hold)

- Production LLM apps with high request volume (>1000 calls/day) where API costs are significant
- Budget-constrained projects that need to scale without proportional cost increase
- Multi-tenant SaaS where per-request costs must be predictable
- Pipelines running batch classification, extraction, or summarization at scale

## Skip If (ANY kills it)

- Low-volume prototypes — premature optimization adds complexity with no payoff
- Tasks requiring temperature > 0 (non-deterministic outputs) — caching is ineffective
- Latency-critical real-time systems where cache lookup adds unacceptable overhead
- Workflows where output freshness is mandatory (live data, personalized responses)

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

- parent skill: `geek/ai/ml-ops/`
