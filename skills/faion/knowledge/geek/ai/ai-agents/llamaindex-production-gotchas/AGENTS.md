---
slug: llamaindex-production-gotchas
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LlamaIndex has several non-obvious failure modes in production: SubQuestionQueryEngine.
content_id: "c89dd0f1420781f5"
tags: [llamaindex, production, async, evaluation, observability]
---
# LlamaIndex Production Gotchas and Observability

## Summary

**One-sentence:** LlamaIndex has several non-obvious failure modes in production: SubQuestionQueryEngine.

**One-paragraph:** LlamaIndex has several non-obvious failure modes in production: SubQuestionQueryEngine.query() blocks async event loops, QueryFusionRetriever opens unbounded concurrent LLM calls, ReActAgent does not auto-recover from tool errors, and evaluation methods consume significant tokens. This methodology documents each trap with the fix and covers callbacks, caching, and tracing for production observability.

## Applies If (ALL must hold)

- Deploying any LlamaIndex component in an async web server (FastAPI, aiohttp) or async agent loop.
- Using QueryFusionRetriever with use_async=True under production load.
- Building evaluation pipelines with FaithfulnessEvaluator or RelevancyEvaluator at scale.
- Debugging intermittent failures in ReActAgent tool calls.
- Adding observability (traces, latency, token counts) to a LlamaIndex RAG pipeline.

## Skip If (ANY kills it)

- Development prototypes — most of these issues only surface under load or in async environments.
- Simple synchronous scripts — async gotchas do not apply outside event loops.

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
