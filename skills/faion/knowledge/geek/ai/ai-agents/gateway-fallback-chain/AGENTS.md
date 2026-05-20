---
slug: gateway-fallback-chain
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Do not hard-code a single model in production agent code.
content_id: "ae99efe631d31b73"
tags: [agents, routing, availability, gateways, openrouter]
---
# Cost-Aware Gateway with Fallback Chain (OpenRouter Pattern)

## Summary

**One-sentence:** Do not hard-code a single model in production agent code.

**One-paragraph:** Do not hard-code a single model in production agent code. Send each call to a gateway (OpenRouter, LiteLLM proxy, Portkey, Kong AI Gateway) that exposes a primary model plus an ordered fallback chain; on provider 5xx, 429, or timeout the gateway transparently retries the next model in the list. Bill only the successful run. The result: better availability than any single vendor, no code change to swap models, and a single integration surface for prompt-caching, retries, observability, and budget caps.

## Applies If (ALL must hold)

- Production agents with an availability SLA above the single-vendor floor.
- Teams running A/B experiments across providers (Anthropic vs OpenAI vs Gemini) without code changes.
- Workloads that hit rate limits on a single provider during peak hours.
- Multi-region deployments where the cheapest provider differs per region.

## Skip If (ANY kills it)

- Strict data-residency or compliance regimes (EU healthcare, defense) where the gateway is a third-party processor — go direct, with a controlled fallback inside the same boundary.
- Pipelines that depend on raw vendor SDK features the gateway does not expose (Anthropic prompt caching, OpenAI Batch API, fine-tuned models).
- Local development and experimentation — the gateway adds latency and operational surface for no production benefit.
- Edge / on-device inference — gateway round-trip dominates total latency.

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

- parent skill: `geek/ai/ai-agents/`
