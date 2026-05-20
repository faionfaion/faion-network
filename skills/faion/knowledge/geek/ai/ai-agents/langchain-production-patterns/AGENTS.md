---
slug: langchain-production-patterns
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production LangChain chains require fallbacks for model outages, retries for transient errors, configurable fields for runtime model swaps, and pinned dependency versions to avoid silent breakage.
content_id: "10ac13e5d8469825"
tags: [langchain, production, fallback, retry, lcel]
---
# LangChain Production Patterns

## Summary

**One-sentence:** Production LangChain chains require fallbacks for model outages, retries for transient errors, configurable fields for runtime model swaps, and pinned dependency versions to avoid silent breakage.

**One-paragraph:** Production LangChain chains require fallbacks for model outages, retries for transient errors, configurable fields for runtime model swaps, and pinned dependency versions to avoid silent breakage. Without these, chain failures propagate silently and are nearly impossible to debug retroactively.

## Applies If (ALL must hold)

- Any LangChain chain deployed to production where model outages or rate limits are possible.
- Projects that require LLM provider flexibility (swap OpenAI for Anthropic without rewriting the chain).
- Services that need runtime model switching (e.g. A/B testing gpt-4o vs gpt-4o-mini) without redeployment.
- Batch processing workflows that require concurrent chain invocations with controlled concurrency.

## Skip If (ANY kills it)

- Simple single-call LLM tasks — fallback and retry setup adds boilerplate with no value for throw-away scripts.
- When the team is unfamiliar with LangChain's abstraction layers — debugging failures in production chains requires deep framework knowledge.
- Projects with strict latency SLAs where LCEL's serialization overhead matters.

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
