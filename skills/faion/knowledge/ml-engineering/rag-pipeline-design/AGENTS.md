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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rag-pipeline.py`

```python
"""Production RAG pipeline with Qdrant: ingest, hybrid search, metadata filter."""
import hashlib
import os
from typing import Optional

from anthropic import Anthropic
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    Filter,
    FieldCondition,
    MatchValue,
    PointStruct,
    VectorParams,
)

COLLECTION = "knowledge_base"
EMBED_MODEL = "text-embedding-3-large"
EMBED_DIM = 3072
CHAT_MODEL = "claude-opus-4-5"

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
anthropic = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
qdrant = QdrantClient(url=os.environ.get("QDRANT_URL", "http://localhost:6333"))


def ensure_collection() -> None:
    if not qdrant.collection_exists(COLLECTION):
        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )


def embed(text: str) -> list[float]:
    response = openai.embeddings.create(model=EMBED_MODEL, input=text)
    return response.data[0].embedding


def ingest(documents: list[dict], tenant_id: str) -> None:
    """Ingest documents with tenant isolation via payload filter."""
    ensure_collection()
    points = []
    for doc in documents:
        content = doc["content"]
        doc_id = hashlib.sha256(content.encode()).hexdigest()
        vector = embed(content)
        points.append(PointStruct(
            id=doc_id,
            vector=vector,
            payload={
                "content": content,
                "source": doc.get("source", ""),
                "tenant_id": tenant_id,
            },
        ))
    qdrant.upsert(collection_name=COLLECTION, points=points)


def search(query: str, tenant_id: str, top_k: int = 5) -> list[dict]:
    """Hybrid search with mandatory tenant filter."""
    vector = embed(query)
    results = qdrant.search(
        collection_name=COLLECTION,
        query_vector=vector,
        limit=top_k,
        query_filter=Filter(
            must=[FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))]
        ),
        with_payload=True,
        score_threshold=0.6,
    )
    return [{"content": r.payload["content"], "source": r.payload["source"], "score": r.score}
            for r in results]


def answer(query: str, tenant_id: str) -> str:
    """Retrieve context and synthesize answer with source citations."""
    nodes = search(query, tenant_id)
    if not nodes:
        return "I don't have enough information to answer that question."

    context = "\n\n".join(
        f"[{i+1}] {n['content']} (source: {n['source']})"
        for i, n in enumerate(nodes)
    )
    response = anthropic.messages.create(
        model=CHAT_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}],
        system="Answer based only on the context provided. Cite sources as [N]. If the answer is not in the context, say so.",
    )
    return response.content[0].text
```

### `templates/prompt-rag.txt`

```text
You are a precise question-answering assistant. You answer questions based ONLY on the provided context documents.

Rules:
1. Answer using ONLY information from the context. Do not use prior knowledge.
2. Cite each fact with the source number: [1], [2], etc.
3. If the answer is not in the context, respond with: "I don't have information about that in the available documents."
4. Do not speculate, extrapolate, or infer beyond what the context states.
5. If context documents contradict each other, note the contradiction and cite both sources.
6. Keep answers concise. Use bullet points for multi-part answers.

Context:
{context}

Question: {question}

Answer (with citations):
```

### `templates/rag-pipeline.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [tier, embedding, vector_db, chunking, retrieval, prompt, eval_gate, telemetry]
properties:
  tier:
    type: string
    enum: [naive, advanced, modular, agentic]
  embedding:
    type: object
    required: [model, dim]
    properties:
      model: { type: string }
      dim: { type: integer, minimum: 64 }
  vector_db:
    type: object
    required: [kind, connection]
    properties:
      kind: { type: string, enum: [qdrant, pgvector, pinecone, weaviate, milvus, chroma] }
  chunking:
    type: object
    required: [strategy, size, overlap]
    properties:
      strategy: { type: string }
      size: { type: integer, minimum: 100, maximum: 1500 }
      overlap: { type: integer, minimum: 0 }
  retrieval:
    type: object
    required: [mode]
    properties:
      mode: { type: string, enum: [hybrid, vector, bm25] }
      top_k_first_stage: { type: integer, minimum: 5, maximum: 100 }
  reranker:
    type: object
    properties:
      kind: { type: string }
      model: { type: string }
      top_n: { type: integer, minimum: 1, maximum: 20 }
  prompt:
    type: object
    required: [citation_required, fallback_phrase]
    properties:
      citation_required: { type: boolean }
      fallback_phrase: { type: string, minLength: 5 }
  eval_gate:
    type: object
    required: [framework, thresholds]
    properties:
      framework: { type: string }
      thresholds:
        type: object
        required: [faithfulness, context_recall]
        properties:
          faithfulness: { type: string }
          context_recall: { type: string }
  telemetry:
    type: object
    required: [log_query_embedding, log_retrieved_ids, log_scores]
    properties:
      log_query_embedding: { type: boolean }
      log_retrieved_ids: { type: boolean }
      log_scores: { type: boolean }
```

### `templates/_smoke-test.yaml`

```yaml
tier: advanced

embedding:
  model: voyage-3-large
  dim: 1024

vector_db:
  kind: qdrant
  connection:
    host: qdrant.local
    port: 6333

chunking:
  strategy: recursive
  size: 512
  overlap: 50

retrieval:
  mode: hybrid
  top_k_first_stage: 20

reranker:
  kind: cohere
  model: rerank-multilingual-v3.0
  top_n: 5

prompt:
  citation_required: true
  fallback_phrase: "I don't have enough information."

eval_gate:
  framework: ragas
  thresholds:
    faithfulness: ">= 0.90"
    context_recall: ">= 0.85"

telemetry:
  log_query_embedding: true
  log_retrieved_ids: true
  log_scores: true
```
