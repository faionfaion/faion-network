# LlamaIndex

## Summary

LlamaIndex is a data framework for building LLM applications that connect to custom data sources. Use it when retrieval quality and document-centric pipelines are the primary concern — it provides indexes, query engines, and event-driven workflows (Workflows + AgentWorkflow) for building production RAG and agentic systems.

## Why

LlamaIndex solves the document retrieval problem that raw LLM APIs do not: loading heterogeneous document sources, chunking them optimally, indexing into a vector store, and synthesizing answers with source citations. Its Workflow abstraction provides async-first, type-safe event pipelines that map directly to agent task queues, enabling pause/resume for human-in-loop checkpoints.

## When To Use

- Building RAG over private documents: PDFs, Notion, GitHub repos, SQL databases
- Application is document-centric and retrieval quality is the primary concern
- Need LlamaParse for complex document parsing (tables, figures, multi-column PDFs)
- Building multi-step data-aware agents using `AgentWorkflow` with typed events
- Enterprise search combining vector search, keyword search, and metadata filtering
- GraphRAG: entity relationships matter (contracts, knowledge graphs)

## When NOT To Use

- Pure text orchestration without a retrieval step — LangChain or direct SDK is simpler
- Complex multi-tool agent with >10 heterogeneous tools — LangGraph offers better state management
- Real-time data streams where indexing latency is unacceptable
- Team is already deep in LangChain — migration cost may exceed retrieval quality gain
- Prototyping a simple chatbot with no private data — direct LLM call is faster

## Content

| File | What's inside |
|------|---------------|
| `content/01-indexes.xml` | Index types (VectorStoreIndex, PropertyGraphIndex, KeywordTableIndex), selection rules, chunking strategy |
| `content/02-query-engines.xml` | Query engine patterns, response modes, hybrid retrieval, reranking, metadata filtering |
| `content/03-workflows.xml` | Workflow architecture, event-driven steps, state management, multi-agent orchestration |
| `content/04-production.xml` | Production checklist: settings, persistence, caching, observability, evaluation |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.py` | LlamaIndex Settings config with pydantic-settings |
| `templates/rag_workflow.py` | Production RAG Workflow with retrieve → rerank → synthesize steps |
| `templates/prompt-qa.txt` | Custom QA prompt template for domain-specific answering |
