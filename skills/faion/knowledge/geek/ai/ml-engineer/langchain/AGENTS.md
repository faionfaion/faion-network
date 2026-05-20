---
slug: langchain
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LangChain (LCEL pipe syntax) and LangGraph (state machine framework) for building production AI chains and agents.
content_id: "5a194fbbcfde4010"
tags: [langchain, langgraph, agents, lcel, chains]
---
# LangChain and LangGraph: Building Production AI Agents

## Summary

**One-sentence:** LangChain (LCEL pipe syntax) and LangGraph (state machine framework) for building production AI chains and agents.

**One-paragraph:** LangChain (LCEL pipe syntax) and LangGraph (state machine framework) for building production AI chains and agents. LangChain handles standard tool-calling agents via `create_react_agent()` and composable pipelines via `prompt | model | parser`. LangGraph adds durable state, checkpointing, human-in-the-loop interrupts, and multi-agent Supervisor patterns for complex control flow.

## Applies If (ALL must hold)

- Building multi-step AI workflows where each step's output feeds the next (LCEL pipe chains)
- Standard ReAct tool-calling agent with 3-10 tools — `create_react_agent()` covers 80% of use cases
- Complex control flow requiring state machines: human-in-the-loop approval, conditional branching, retry logic (LangGraph)
- Long-running workflows that must survive process restarts — LangGraph checkpointing persists state to disk/DB
- Multi-agent orchestration: Supervisor → Worker patterns with role specialization
- RAG pipelines requiring custom retrieval → reranking → synthesis chains

## Skip If (ANY kills it)

- Single LLM call — use the provider SDK directly (anthropic, openai); LangChain adds 50-200ms overhead
- Document-centric RAG with complex index types — LlamaIndex has better RAG abstractions
- Browser or desktop agents — LangChain's tools don't wrap browser automation well; use Playwright directly
- Simple prompt templates — Python f-strings or Jinja2 avoid the dependency
- High-throughput inference (greater than 100 RPS) — LangChain's Python overhead becomes measurable; use vLLM or direct SDK

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
