---
slug: llamaindex-agents-eval
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LlamaIndex agents provide autonomous reasoning with tool use (ReAct, OpenAI styles).
content_id: "be4931502ccd2de0"
tags: [llamaindex, agents, evaluation, rag, production-patterns]
---
# LlamaIndex: Agents & Evaluation

## Summary

**One-sentence:** LlamaIndex agents provide autonomous reasoning with tool use (ReAct, OpenAI styles).

**One-paragraph:** LlamaIndex agents provide autonomous reasoning with tool use (ReAct, OpenAI styles). Evaluation frameworks measure retrieval and response quality. Production patterns include caching, streaming, async execution, and observability. LlamaCloud offers managed parsing and indexing.

## Applies If (ALL must hold)

- Building autonomous agents that reason over multi-source data (documents, APIs, databases)
- Measuring retrieval quality with metrics like hit rate, MRR, or faithfulness scores
- Evaluating response correctness against ground truth answers
- Streaming responses to users in real-time
- Caching expensive embedding or indexing operations
- Running async retrieval and LLM calls for latency reduction
- Integrating LlamaCloud for managed document parsing and indexing

## Skip If (ANY kills it)

- Simple single-question retrieval without multi-step reasoning — use query engines directly
- Stateless, non-contextual LLM generation — agents add memory and state overhead
- Offline batch evaluation where latency does not matter — streaming and async add complexity
- Fully controlled workflows where branching is known upfront — LangGraph is more explicit for fixed control flow
- Small datasets where evaluation overhead exceeds value — evaluation is most useful at scale

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
