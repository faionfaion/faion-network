---
slug: claude-api
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production guide for calling Anthropic's Claude API directly via the Python and TypeScript SDKs.
content_id: "14e4663154507302"
tags: [claude, api, llm, agents, prompt-caching]
---
# Claude API

## Summary

**One-sentence:** Production guide for calling Anthropic's Claude API directly via the Python and TypeScript SDKs.

**One-paragraph:** Production guide for calling Anthropic's Claude API directly via the Python and TypeScript SDKs. Covers the Messages API, Tool Use (agentic loops with MAX_TURNS guard), Prompt Caching (90% input-cost reduction on repeated system prompts), Extended Thinking (Opus 4.5 only, minimum 1,024 budget tokens), Streaming (SSE), and the Batch API (50% cost savings, 24-hour window). Always cache system prompts; always enforce MAX_TURNS; always use forced tool use for structured output.

## Applies If (ALL must hold)

- Building an agentic loop that calls tools and needs full control over the message array
- System prompts or large context blocks repeat across requests — Prompt Caching applies immediately
- Processing hundreds of documents in batch where 50% cost savings outweigh 24-hour latency
- Complex reasoning tasks where Extended Thinking (Opus 4.5) meaningfully improves accuracy
- Existing codebase has no multi-provider requirement — LiteLLM abstraction adds unnecessary overhead

## Skip If (ANY kills it)

- The codebase already uses LiteLLM, LangChain, or another multi-provider abstraction — keep that layer
- Latency budget is under 200ms — streaming still has SSE overhead; Batch API is unsuitable
- Task complexity does not justify Sonnet or above — route to Haiku or a cheaper provider first (see decision-framework)
- System is already in production with a working multi-provider setup — don't break it for caching savings

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
