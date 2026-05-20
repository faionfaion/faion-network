---
slug: langchain-basics
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Core LangChain concepts, installation, chain patterns, prompt engineering, and output parsing for building sequential AI pipelines.
content_id: "d5c20c0283cf1103"
tags: [langchain, chains, prompts, lcel, llm]
---
# LangChain Basics

## Summary

**One-sentence:** Core LangChain concepts, installation, chain patterns, prompt engineering, and output parsing for building sequential AI pipelines.

**One-paragraph:** Core LangChain concepts, installation, chain patterns, prompt engineering, and output parsing for building sequential AI pipelines.

## Applies If (ALL must hold)

- Building sequential LLM pipelines where output of one step feeds the next
- You need rapid structured output with Pydantic validation via `with_structured_output()`
- The task is prompt engineering and chain composition, not stateful agent loops
- Streaming output to a user interface is required — LCEL chains support `.stream()` natively
- Team wants LangSmith observability out of the box with minimal configuration

## Skip If (ANY kills it)

- You need stateful multi-step agents with conditional branching — use LangGraph instead
- Pure document retrieval/RAG is the primary concern — LlamaIndex handles indexing better
- The pipeline has no LLM calls — plain Python functions with no framework overhead are simpler
- You need agentic memory, tool loops, or human-in-the-loop — all require LangGraph
- Latency is critical and you want to minimize abstraction layers; direct Anthropic SDK calls are faster

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
