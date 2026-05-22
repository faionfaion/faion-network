---
slug: llm-cost-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Understanding LLM API costs, tracking usage, model pricing, and basic optimization for production applications.
content_id: "15ce56e15d9b7b60"
tags: [cost, llm, pricing, optimization]
---
# LLM Cost Basics

## Summary

**One-sentence:** Understanding LLM API costs, tracking usage, model pricing, and basic optimization for production applications.

**One-paragraph:** Understanding LLM API costs, tracking usage, model pricing, and basic optimization for production applications.

## Applies If (ALL must hold)

- Starting new LLM projects and needing a cost model before choosing a provider and model tier
- Setting up cost tracking for an existing API-based system to prevent surprise billing
- Implementing model routing to assign cheap models to simple tasks and expensive ones to complex tasks
- Preparing a budget estimate for a product feature that involves LLM calls
- Auditing existing LLM usage to find optimization opportunities

## Skip If (ANY kills it)

- The application makes fewer than 100 LLM calls per day — overhead of a full cost tracker is unnecessary; use provider dashboard directly
- The system uses only one model with no routing complexity — cost tracking at the provider level (dashboard alerts) is sufficient
- The primary optimization goal is latency, not cost — routing by complexity adds latency overhead that may not be acceptable
- Self-hosted models (Ollama, vLLM) — token-based pricing does not apply; cost model shifts to GPU infrastructure

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
