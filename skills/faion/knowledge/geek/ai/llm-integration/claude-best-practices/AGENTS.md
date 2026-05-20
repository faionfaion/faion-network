---
slug: claude-best-practices
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A set of production patterns for calling the Anthropic Messages API reliably and cost-efficiently: model tier selection (Haiku/Sonnet/Opus by task), prompt caching for repeated large contexts, Batch API for offline workloads, token counting for pre-flight validation, exponential backoff for rate limits, and a monitored client wrapper for cost attribution per subagent role.
content_id: "445c67dc19713ea9"
tags: [claude, anthropic, api-integration, cost-optimization, production-patterns]
---
# Claude Best Practices

## Summary

**One-sentence:** A set of production patterns for calling the Anthropic Messages API reliably and cost-efficiently: model tier selection (Haiku/Sonnet/Opus by task), prompt caching for repeated large contexts, Batch API for offline workloads, token counting for pre-flight validation, exponential backoff for rate limits, and a monitored client wrapper for cost attribution per subagent role.

**One-paragraph:** A set of production patterns for calling the Anthropic Messages API reliably and cost-efficiently: model tier selection (Haiku/Sonnet/Opus by task), prompt caching for repeated large contexts, Batch API for offline workloads, token counting for pre-flight validation, exponential backoff for rate limits, and a monitored client wrapper for cost attribution per subagent role.

## Applies If (ALL must hold)

- Building any production system that calls the Anthropic Messages API.
- Optimizing cost/quality tradeoff across multi-agent pipelines.
- When system prompts are large and repeated across many requests (prompt caching).
- Implementing retry logic, fallback models, or monitoring for Claude API calls.
- Selecting the right Claude model tier for a given agent role.

## Skip If (ANY kills it)

- Quick scripted one-off calls with no cost or reliability concerns.
- Provider-neutral code that must abstract over multiple LLM providers — use an abstraction layer instead.
- Token counting pre-flight adds latency; skip for simple short prompts.

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
