---
slug: prompt-cache-prefix-order
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Prompt caching saves 80-90% on repeated content by caching tokens only at the prefix level.
content_id: "efc1f5fa030533ef"
tags: [prompt-caching, cost-optimization, prefix-order, cache-control, api-economics]
---
# Prompt-Cache Prefix Order

## Summary

**One-sentence:** Prompt caching saves 80-90% on repeated content by caching tokens only at the prefix level.

**One-paragraph:** Prompt caching saves 80-90% on repeated content by caching tokens only at the prefix level. To maximize cache hits, order your prompt so the longest-stable segments come first, then mark a cache_control breakpoint after them. Each subsequent call in the cache window pays only 10% for those cached tokens.

## Applies If (ALL must hold)

- Long system prompts (>1024 tokens, the Anthropic minimum cacheable size)
- Stable tool definitions (almost always — tool defs rarely change mid-session)
- Long-stable contexts: codebase manifests, user profiles, knowledge bases
- High call volume on the same prefix (chat, agent loops, batch processing)
- Multi-turn agents — each turn pays only for the new turn

## Skip If (ANY kills it)

- One-shot calls (no second call to amortize the cache write)
- Prefixes < 1024 tokens (Anthropic minimum) or < 2048 tokens (OpenAI)
- Prefixes that change every call (no cache hit possible)
- Cost-sensitive systems where prefix is small relative to output (output is never cached)

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
