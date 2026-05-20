---
slug: llamaindex-basics
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LlamaIndex is a data indexing framework that sits between your documents and an LLM.
content_id: "a9c746d342caaeb8"
tags: [llamaindex, rag, retrieval, indexing, document-parsing]
---
# LlamaIndex Basics

## Summary

**One-sentence:** LlamaIndex is a data indexing framework that sits between your documents and an LLM.

**One-paragraph:** LlamaIndex is a data indexing framework that sits between your documents and an LLM. It loads documents from diverse sources (files, web, APIs), chunks them into nodes with metadata, embeds them, stores them in a vector or hybrid index, and provides query engines to retrieve and synthesize responses. Unlike LangChain (which orchestrates multi-step workflows), LlamaIndex specializes in the retrieval layer and ships production-ready defaults that work in 50 lines of code.

## Applies If (ALL must hold)

- Building a RAG pipeline over a static or semi-static document corpus (PDFs, Markdown, DOCX, web pages).
- Implementing document Q&A where retrieval quality matters more than workflow complexity.
- Prototyping needs to be operational in under 50 lines - LlamaIndex defaults cover most tuning later.
- The corpus is on disk or accessible via URL; batch ingestion is acceptable (not real-time streaming).
- You want node-level metadata (titles, keywords, summaries) auto-extracted before indexing.
- A team is already invested in the LlamaIndex ecosystem and wants to avoid mixing frameworks.

## Skip If (ANY kills it)

- Complex multi-step workflows with branching logic - use LangGraph instead.
- Agent-driven tool use is the primary concern - LlamaIndex has agents but LangGraph is more expressive.
- Real-time streaming ingestion (Kafka, CDC) - LlamaIndex ingestion is batch-oriented.
- Pure LLM generation with no retrieval needed - use Anthropic SDK directly; adding LlamaIndex is overhead.
- Team already standardized on LangChain; mixing frameworks adds maintenance burden.

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
