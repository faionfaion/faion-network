# LlamaIndex

## Summary

**One-sentence:** Produces a LlamaIndex RAG / agent pipeline: heterogeneous loaders → chunking → vector index → query engine with source citations and async Workflow event pipelines.

**One-paragraph:** Produces a LlamaIndex RAG / agent pipeline. LlamaIndex solves the document-retrieval problem the LLM SDK does not: heterogeneous document loaders, chunking strategies, vector + property-graph indexes, and answer synthesis with source citations. Its Workflow abstraction provides async-first, type-safe event pipelines that map directly to agent task queues and pause/resume for human-in-loop checkpoints.

**Ефективно для:** Дата-інженер для RAG over heterogeneous docs — fixed pipeline з loaders + chunk + index + cited query.

## Applies If (ALL must hold)

- Need RAG over heterogeneous document sources (PDF, HTML, DB, Notion, S3, ...).
- Source citations are a hard requirement (regulated / customer-facing).
- Python stack — LlamaIndex is Python-canonical.
- Have or can stand up a vector store (Qdrant, Pinecone, pgvector, Chroma).
- Want a Workflow event pipeline for pause/resume / HITL.

## Skip If (ANY kills it)

- Single-source plain-text RAG — provider-native RAG suffices.
- Need a graph-first knowledge model — use GraphRAG instead (or LlamaIndex PropertyGraphIndex).
- Non-Python stack — use a thinner native client.
- No source-citation requirement AND simple chunking — LangChain is leaner.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Source corpus | directory / db / api list | data team |
| Vector store | url + creds | infra |
| Chunk strategy | yaml (size, overlap) | ML lead |
| Provider choice | string | decision record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-decision-framework` | Provider + RAG choice. |
| `geek/ai/ml-engineer/llm-observability-stack` | Trace ingestion + query. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: load → chunk → index → query → cite. | ~800 |
| `content/06-decision-tree.xml` | essential | Branch: vector vs property-graph + workflow vs query-engine. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-pipeline` | haiku | Fill rag_workflow.py + config.py from decisions. |
| `design-chunking` | sonnet | Choose chunk_size + overlap from doc shape. |
| `audit-retrieval` | opus | Cross-document retrieval-quality audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag_workflow.py` | RAG Workflow with retrieval + synthesis + citations. |
| `templates/config.py` | Settings: embed model, chunk_size, top_k. |
| `templates/prompt-qa.txt` | QA prompt with source-citation policy. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llamaindex.py` | Validate the pipeline config (loaders, chunk, index, citation policy). | Pre-merge of every LlamaIndex pipeline PR. |

## Related

- [[graph-rag]] — graph-first alternative.
- [[langchain]] — alternative agent framework.
- [[llm-observability-stack]] — tracing.

## Decision tree

Decision tree at `content/06-decision-tree.xml` decides index type (vector / property-graph / hybrid) and pipeline shape (Workflow vs QueryEngine).
