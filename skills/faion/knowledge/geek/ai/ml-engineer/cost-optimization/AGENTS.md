---
slug: cost-optimization
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LLM costs can be reduced 60-90% through model routing (50-75% savings), prompt caching (80-90% on repeated system prompts), response caching (70-95% for deterministic queries), token reduction (20-40%), and Batch API (50% discount on async workloads).
content_id: "bf7aefc9ad69a72e"
tags: [cost-optimization, llm, routing, caching, budget-control]
---
# LLM Cost Optimization

## Summary

**One-sentence:** LLM costs can be reduced 60-90% through model routing (50-75% savings), prompt caching (80-90% on repeated system prompts), response caching (70-95% for deterministic queries), token reduction (20-40%), and Batch API (50% discount on async workloads).

**One-paragraph:** LLM costs can be reduced 60-90% through model routing (50-75% savings), prompt caching (80-90% on repeated system prompts), response caching (70-95% for deterministic queries), token reduction (20-40%), and Batch API (50% discount on async workloads). Track cost per pipeline stage from day 1 — you cannot optimize what you cannot attribute. Optimize only after measuring; premature optimization wastes time.

## Applies If (ALL must hold)

- Monthly LLM spend exceeds $500 and is growing faster than revenue
- Agentic pipelines with greater than 10K requests/day where model selection matters
- Batch workloads with greater than 1h latency tolerance (Batch API = 50% off)
- System prompts greater than 1K tokens (OpenAI) or greater than 2K tokens (Claude) that repeat across many calls
- Multi-step pipelines where early stages can use cheap models for routing

## Skip If (ANY kills it)

- Early prototype phase — optimize only after measuring
- Tasks where quality degradation from cheaper models is unacceptable (medical, legal, safety-critical)
- Very low volume (less than 100 calls/day) — savings are negligible, complexity is not worth it
- When the cost driver is output tokens on complex reasoning tasks — only better prompts help, not routing

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
