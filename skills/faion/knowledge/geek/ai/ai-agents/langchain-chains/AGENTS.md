---
slug: langchain-chains
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LCEL chain patterns, prompt templates, output parsers, error handling, and streaming for composing LLM pipelines with LangChain.
content_id: "2b23fdf17b17437e"
tags: [langchain, chains, lcel, prompts, parsing]
---
# LangChain Chains: Patterns and Composition

## Summary

**One-sentence:** LCEL chain patterns, prompt templates, output parsers, error handling, and streaming for composing LLM pipelines with LangChain.

**One-paragraph:** LCEL chain patterns, prompt templates, output parsers, error handling, and streaming for composing LLM pipelines with LangChain.

## Applies If (ALL must hold)

- Composing discrete LLM steps in a linear pipeline where each step transforms and passes output to the next
- Routing user input to specialized handlers without maintaining state between requests
- Parallel execution of independent sub-tasks in a single LLM call batch
- Building resilient pipelines where a primary model may fail and a fallback must take over transparently
- Prompt engineering iteration — LCEL chain composition makes it easy to swap templates, models, or parsers without restructuring code

## Skip If (ANY kills it)

- The pipeline needs to loop, retry with modified state, or maintain context between steps — use LangGraph
- You need tool use (web search, database queries) inside the pipeline — LangGraph agent with tools is the right primitive
- The "chain" would consist of a single prompt + model call — use the model directly without LCEL overhead
- Output parsing is complex with multiple fallback formats — `with_structured_output()` with function calling is more reliable than chaining parsers
- The team needs visual workflow debugging — LangGraph's graph structure is far easier to inspect than nested LCEL chains

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
