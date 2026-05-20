---
slug: local-llm-ollama
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Run LLMs locally via Ollama's HTTP API (port 11434).
content_id: "4c1211984d932ca9"
tags: [ollama, local-llm, privacy, cost-optimization, inference]
---
# Local LLM with Ollama

## Summary

**One-sentence:** Run LLMs locally via Ollama's HTTP API (port 11434).

**One-paragraph:** Run LLMs locally via Ollama's HTTP API (port 11434). Primary use: privacy-sensitive workloads, offline environments, and cost elimination for high-volume low-stakes tasks. The OpenAI-compatible `/v1` endpoint allows swapping between local and cloud APIs by changing only `base_url` and `api_key`, enabling local development + cloud production without code changes.

## Applies If (ALL must hold)

- Data privacy requirements prohibiting external API calls
- High-volume, low-stakes tasks where cloud API costs are prohibitive
- Offline or air-gapped environments
- Development/testing — no API costs, no rate limits, instant iteration
- Deploying a custom fine-tuned model not hosted externally
- Latency-sensitive applications where local inference beats network round-trip

## Skip If (ANY kills it)

- Tasks requiring frontier-level reasoning (complex code, multi-step math) — local 7B/13B models underperform Opus/GPT-4o
- Machine has <8GB RAM — models will page to disk and be unusably slow
- Production services with unpredictable load spikes — local GPU is not elastically scalable
- Latest model capabilities needed — local model libraries lag cloud providers by months

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

- parent skill: `geek/ai/llm-integration/`
