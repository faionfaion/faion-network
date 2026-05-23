# RAG Pipeline Design

## Summary

**One-sentence:** Designs a production RAG pipeline grounded in domain data — embeddings + hybrid (vector + BM25) search + cross-encoder reranking + semantic caching — and selects the architecture tier (Naive, Advanced, Modular, Agentic) that matches query complexity.

**One-paragraph:** RAG fails in production 73% from retrieval, not generation. Naive vector search misses exact-match queries (product codes, names, technical terms); hybrid search (vector + BM25 fused via Reciprocal Rank Fusion) lifts recall@10 by 15-25%. Re-ranking the top-20 with a cross-encoder (Cohere Rerank, BGE) yields top-5 better than naive top-20. Production setup pins: embedding model (Voyage-3-large for quality, text-embedding-3-small for cost, BGE local for privacy), vector DB (Qdrant self-hosted, pgvector if Postgres exists, Pinecone managed), chunk strategy (RecursiveCharacterTextSplitter 400-512 tokens with 50 overlap as default), and evaluation gate (Ragas faithfulness ≥ 0.9, context-recall ≥ 0.85) before every release. Output: a versioned `rag-pipeline.yaml` declaring each stage + telemetry.

**Ефективно для:**

- Production RAG над приватними / часто оновлюваними даними з вимогою citations — hybrid + rerank дає precision яку pure vector не дає.
- Команд з мультиджерельною KB (PDF + SQL + API) — Modular RAG паралелить retrieval через джерела і мерджить на synthesis.
- Cost-sensitive use cases — semantic cache + content-hash gate знижує embedding cost 40-60%.
- Domain queries з низькою overlap до моделі (legal, medical, code) — HyDE або agentic reformulation покривають vocabulary gap.

## Applies If (ALL must hold)

- LLM needs access to private, domain-specific, or frequently updated knowledge not in training data
- Application requires citations: users must verify sources
- Knowledge base exceeds the model's context window (>200K tokens of documents)
- ≥2 heterogeneous data sources need unified semantic search OR a single source >5k documents
- Answer accuracy is below acceptable threshold with prompt engineering alone

## Skip If (ANY kills it)

- Knowledge is fully covered by the model's training and does not change
- Corpus &lt;50 documents — include them all in context instead
- Retrieval latency &gt;500ms unacceptable and caching cannot compensate
- Team lacks infra to maintain vector DB + embedding pipeline — use a managed RAG service (LlamaCloud, Azure AI Search)
- Queries are always the same — pre-generate + cache answers instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `corpus-inventory.yaml` | YAML | data-engineering team listing sources + sizes + update cadence |
| `query-sample.jsonl` | JSONL | ≥100 labelled queries with `intent` + `expected_doc_ids` |
| `latency-budget-ms.json` | JSON | product/PM commitment (p50 / p95 / p99) |
| `embedding-budget-usd.json` | JSON | finance approval for indexing + monthly inference |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `vector-databases` | DB selection vocabulary |
| `reranking` | Cross-encoder discipline |
| `rag-feature-acceptance-contract` | Defines per-intent thresholds this pipeline must hit |
| `rag-evaluation-frameworks` | Ragas / TruLens used in the eval gate |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: tier selection, hybrid default, chunk-512, reranker after retrieval, citation enforcement, eval gate | 1100 |
| `content/02-output-contract.xml` | essential | `rag-pipeline.yaml` schema (stages + telemetry + ship gates) | 800 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: naive chunking, missing reranker, no eval gate, tenant leak, context overflow, HyDE-everywhere | 900 |
| `content/04-procedure.xml` | essential | 6 steps: pick tier → choose DB+embed → ingest+chunk → wire hybrid+rerank → eval gate → ship | 900 |
| `content/05-examples.xml` | essential | Worked example: Advanced RAG over support KB with Qdrant + Cohere Rerank | 700 |
| `content/06-decision-tree.xml` | essential | Routes by query complexity to Naive / Advanced / Modular / Agentic tier | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tier_selection_from_query_sample` | sonnet | Cluster + classify query types; bounded judgement |
| `pipeline_yaml_drafting` | opus | Cross-component synthesis; needs depth |
| `chunk_strategy_pick` | sonnet | Document-type heuristics |
| `eval_gate_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag-pipeline.py` | Production RAG with Qdrant: hybrid search + metadata filter |
| `templates/prompt-rag.txt` | RAG system prompt enforcing citation + "don't know" fallback |
| `templates/rag-pipeline.schema.yaml` | Schema for declarative pipeline spec |
| `templates/_smoke-test.yaml` | Minimum-viable pipeline spec that validates clean |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-pipeline-design.py` | Lint `rag-pipeline.yaml` against schema | Pre-commit + pre-deploy |

## Related

- [[vector-databases]] — DB selection
- [[reranking]] — second-stage retrieval
- [[rag-feature-acceptance-contract]] — ship gate this pipeline must pass
- external: [Ragas](https://docs.ragas.io/) · [Qdrant hybrid](https://qdrant.tech/articles/hybrid-search/) · [Anthropic RAG](https://www.anthropic.com/news/contextual-retrieval)

## Decision tree

See `content/06-decision-tree.xml`. Branches by query-complexity (single-intent FAQ → Naive; ambiguous → Advanced; multi-source → Modular; multi-step reasoning → Agentic) and budget envelope.
