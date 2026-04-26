# Agent Integration — Embedding Applications

## When to use
- Building or benchmarking a RAG retrieval stage (model selection, quality gates)
- Choosing between embedding providers (OpenAI, Cohere, open-source) for a new project
- Running regression checks after switching embedding models or chunking strategy
- Populating or migrating a vector database (Qdrant, pgvector, Chroma, Weaviate)
- Validating retrieval quality against a labeled dataset before going to production

## When NOT to use
- The task is purely generative — no retrieval component needed
- Dataset is fewer than 50 query/document pairs; MTEB-style benchmarking yields noise at that scale
- Latency budget is so tight that embedding overhead is unacceptable (consider keyword search instead)
- Team lacks ground-truth relevance labels; benchmark numbers will mislead rather than guide

## Where it fails / limitations
- MTEB scores are aggregate; a model that tops MTEB may underperform on narrow domain vocabulary (legal, biomedical, code)
- Cosine similarity assumes normalized embeddings; pgvector `<=>` operator and raw dot-product give different rankings unless vectors are L2-normalized
- Speed benchmarks in the README run single-process; GPU batching and async I/O can 10-20x throughput — numbers are not directly comparable to production
- QdrantClient upsert has a default batch limit; large inserts need chunked upsert loops or the Qdrant batch upload API
- Embedding models drift with provider updates (OpenAI silently versions `text-embedding-3-*`); a stored collection may need re-indexing after a model deprecation

## Agentic workflow
An agent orchestrating embedding applications should first select a model via MTEB scores for the target task type (retrieval vs. classification vs. clustering), then generate embeddings in batches with the chosen provider, insert into the target vector database, and run the `benchmark_retrieval` function against a held-out labeled set to gate quality before promotion to production. Subagents can parallelize benchmarking across candidate models while a parent agent collects and compares results.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the full benchmark-select-insert-validate workflow from an SDD task card
- A dedicated benchmark subagent (custom) — runs `benchmark_retrieval` + `benchmark_speed` for each candidate model and returns a structured JSON report

### Prompt pattern
```
Given the following candidate embedding models and a 200-example labeled retrieval dataset,
run benchmark_retrieval for each model and return a JSON object with:
{"model": str, "recall_at_10": float, "mrr": float, "ms_per_text": float}
sorted by recall_at_10 descending.
```

```
Insert the following {N} documents into Qdrant collection "{collection_name}" using
text-embedding-3-large. Use batch size 100. Return total points upserted and any errors.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `qdrant-client` (Python) | Upsert, search, collection management | `pip install qdrant-client` / [docs.qdrant.tech](https://docs.qdrant.tech) |
| `psycopg2` + pgvector | Store and query embeddings in Postgres | `pip install psycopg2-binary pgvector` / [github.com/pgvector/pgvector](https://github.com/pgvector/pgvector) |
| `openai` SDK | OpenAI embeddings API | `pip install openai` / [platform.openai.com/docs/guides/embeddings](https://platform.openai.com/docs/guides/embeddings) |
| `sentence-transformers` | Run open-source embedding models locally | `pip install sentence-transformers` / [sbert.net](https://www.sbert.net/) |
| `mteb` | Run MTEB benchmark locally | `pip install mteb` / [github.com/embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) |
| `tiktoken` | Count tokens before embedding API calls | `pip install tiktoken` / [github.com/openai/tiktoken](https://github.com/openai/tiktoken) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Embeddings API | SaaS | Yes — simple REST, structured response | Rate limits vary by tier; batch up to 2048 inputs |
| Cohere Embed v3 | SaaS | Yes — supports input_type param for retrieval vs. document | Better multilingual than OpenAI on many tasks |
| Voyage AI | SaaS | Yes — voyage-3 ranks well on MTEB retrieval | Strong for code and domain-specific text |
| Qdrant Cloud | SaaS/OSS | Yes — REST + gRPC, Python client | Self-hostable; free tier for dev |
| Supabase (pgvector) | SaaS/OSS | Yes — standard Postgres SQL | Easy to use if already on Postgres stack |
| Weaviate Cloud | SaaS/OSS | Yes — GraphQL + REST | Built-in vectorizer modules |
| Chroma | OSS | Yes — Python-native, no server needed for dev | Not recommended for multi-node production |
| HuggingFace Inference API | SaaS | Yes — hosted open-source models | Useful for testing bge-m3 without GPU |

## Templates & scripts
See `templates.md` for JSONL dataset format and collection schema templates.

Inline — minimal production upsert loop for Qdrant with batching:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from openai import OpenAI
from typing import Iterator

def batch(iterable, n):
    it = iter(iterable)
    while chunk := list(__import__('itertools').islice(it, n)):
        yield chunk

def embed_and_upsert(
    texts: list[str],
    payloads: list[dict],
    collection: str,
    qdrant_url: str = "http://localhost:6333",
    batch_size: int = 100,
) -> int:
    oai = OpenAI()
    qd = QdrantClient(url=qdrant_url)
    total = 0
    for i, (txt_batch, pay_batch) in enumerate(
        zip(batch(texts, batch_size), batch(payloads, batch_size))
    ):
        resp = oai.embeddings.create(model="text-embedding-3-large", input=txt_batch)
        points = [
            PointStruct(id=i * batch_size + j, vector=e.embedding, payload=pay_batch[j])
            for j, e in enumerate(resp.data)
        ]
        qd.upsert(collection_name=collection, points=points)
        total += len(points)
    return total
```

## Best practices
- Always normalize vectors before inserting into pgvector — use `embedding / np.linalg.norm(embedding)` to ensure cosine distance and dot-product give identical rankings
- Benchmark on your domain data, not just MTEB; create 50-100 labeled query/doc pairs from real user queries before choosing a model
- Use `input_type="search_document"` / `"search_query"` for Cohere and Voyage — omitting this degrades retrieval quality measurably
- Store the model name and version in collection metadata so re-indexing is triggered automatically when the model changes
- For OpenAI, prefer `text-embedding-3-large` with `dimensions=256` when storage cost matters — Matryoshka embeddings retain most quality at 256 dims vs. 3072
- Run `benchmark_speed` with realistic batch sizes (32-128 texts), not single texts; latency per text drops 5-20x with batching
- Set a per-collection index type (HNSW params: `m=16, ef_construct=200`) at creation time; re-indexing after data ingestion is expensive

## AI-agent gotchas
- Embedding API rate limits (OpenAI: 1M tokens/min on tier 1) will throttle large bulk inserts; agents must implement exponential backoff or use the Batch API for offline jobs
- LLM agents should not select embedding models solely from MTEB leaderboard position; the leaderboard aggregates 56 tasks — retrieval rank can differ significantly from overall rank
- `benchmark_retrieval` requires ground-truth relevance labels; agents cannot generate reliable labels synthetically without human validation of at least a sample
- Vector DB schema changes (dimension size, distance metric) require full collection recreation — agents must check collection config before upsert and fail loudly if mismatch
- pgvector `<=>` (cosine) operator requires `vector_cosine_ops` index; creating the wrong index type is a silent correctness bug that agents commonly introduce

## References
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Matryoshka Representation Learning (paper)](https://arxiv.org/abs/2205.13147)
- [BGE-M3 Paper](https://arxiv.org/abs/2402.03216)
- [Qdrant Documentation](https://docs.qdrant.tech)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Sentence Transformers](https://www.sbert.net/)
- [Pinecone Chunking Strategies Guide](https://www.pinecone.io/learn/chunking-strategies/)
