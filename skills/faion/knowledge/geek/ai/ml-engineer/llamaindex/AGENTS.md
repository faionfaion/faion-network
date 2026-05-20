---
slug: llamaindex
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LlamaIndex solves the document retrieval problem that raw LLM APIs do not: loading heterogeneous document sources, chunking them optimally, indexing into a vector store, and synthesizing answers with source citations.
content_id: "4c771c30e7d984e5"
tags: [rag, retrieval, workflows, llamaindex, agents]
---
# LlamaIndex

## Summary

**One-sentence:** LlamaIndex solves the document retrieval problem that raw LLM APIs do not: loading heterogeneous document sources, chunking them optimally, indexing into a vector store, and synthesizing answers with source citations.

**One-paragraph:** LlamaIndex solves the document retrieval problem that raw LLM APIs do not: loading heterogeneous document sources, chunking them optimally, indexing into a vector store, and synthesizing answers with source citations. Its Workflow abstraction provides async-first, type-safe event pipelines that map directly to agent task queues, enabling pause/resume for human-in-loop checkpoints.

## Applies If (ALL must hold)

- Building RAG over private documents: PDFs, Notion, GitHub repos, SQL databases
- Application is document-centric and retrieval quality is the primary concern
- Need LlamaParse for complex document parsing (tables, figures, multi-column PDFs)
- Building multi-step data-aware agents using AgentWorkflow with typed events
- Enterprise search combining vector search, keyword search, and metadata filtering
- GraphRAG: entity relationships matter (contracts, knowledge graphs)

## Skip If (ANY kills it)

- Pure text orchestration without a retrieval step — LangChain or direct SDK is simpler
- Complex multi-tool agent with >10 heterogeneous tools — LangGraph offers better state management
- Real-time data streams where indexing latency is unacceptable
- Team is already deep in LangChain — migration cost may exceed retrieval quality gain
- Prototyping a simple chatbot with no private data — direct LLM call is faster

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
