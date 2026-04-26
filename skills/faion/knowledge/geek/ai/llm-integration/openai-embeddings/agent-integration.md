# Agent Integration — OpenAI Embeddings

## When to use
- Semantic search over a corpus (docs, tickets, FAQs) where keyword search misses intent
- Building or extending a RAG pipeline that requires dense vector retrieval
- Deduplication or clustering of text records at scale
- Classifying user input into categories without a fine-tuned model
- Offline/async enrichment of large datasets via the Batch API (50% cost reduction)

## When NOT to use
- Real-time latency-sensitive paths where a BM25 keyword index is fast enough
- When the corpus fits in context — just send the documents directly to the LLM
- When you need cross-lingual semantic search — check if the embedding model covers your languages
- When exact string match is the requirement — embeddings are approximate
- Fine-tuning use cases — the Batch API covers completions, not only embeddings

## Where it fails / limitations
- `text-embedding-3-large` max input is 8191 tokens — longer docs must be chunked before embedding
- Cosine similarity degrades for very short strings (1-3 words) — use BM25 or hybrid search instead
- Embedding model output is not comparable across different models or dimension settings — reindex if you change either
- Batch API has a 24-hour completion window and 50K requests/batch ceiling — not suitable for real-time
- Reducing dimensions (`dimensions=256`) saves cost but may hurt recall for nuanced queries; benchmark before using in production

## Agentic workflow
An agent embedding pipeline runs in two phases: (1) ingestion — chunk documents, embed in batch, upsert into a vector store; (2) query — embed the user query on demand, nearest-neighbor search, return top-k chunks. Agents should embed queries with the same model and dimension settings used during ingestion. Batch embedding via the OpenAI Batch API is the right choice for nightly re-indexing jobs; synchronous embedding is for interactive query paths only.

### Recommended subagents
- `faion-sdd-executor-agent` — coordinates embed-and-store pipeline as a multi-step SDD task

### Prompt pattern
For RAG retrieval, embed the rewritten/expanded query, not the raw user message:
```python
# Expand query before embedding for better recall
expanded = llm.complete(f"Rewrite for semantic search: {user_query}")
embedding = client.embeddings.create(model="text-embedding-3-small", input=expanded).data[0].embedding
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` (Python SDK) | Embeddings + Batch API | `pip install openai` / https://platform.openai.com/docs/api-reference/embeddings |
| `numpy` | Cosine similarity, vector math | `pip install numpy` |
| `faiss-cpu` / `faiss-gpu` | Fast ANN search over embeddings | `pip install faiss-cpu` / https://github.com/facebookresearch/faiss |
| `pgvector` (PostgreSQL extension) | Vector storage in Postgres | https://github.com/pgvector/pgvector |
| `chromadb` | Local vector DB for dev/test | `pip install chromadb` / https://www.trychroma.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Embeddings API | SaaS | Yes | Primary — REST + SDK |
| Pinecone | SaaS | Yes | Managed vector DB, serverless tier |
| Weaviate | SaaS / OSS | Yes | Hybrid search (BM25 + vectors) built-in |
| Qdrant | SaaS / OSS | Yes | Rust-based, good Docker self-hosting |
| pgvector + Supabase | SaaS | Yes | Postgres-native; good for existing PG stacks |
| Chroma | OSS | Yes | Dev-friendly local vector store |

## Templates & scripts
See `templates.md` for the full RAG ingestion template. Minimal similarity search:

```python
import numpy as np
from openai import OpenAI

client = OpenAI()

def embed(texts: list[str], model="text-embedding-3-small", dims=1536) -> list[list[float]]:
    resp = client.embeddings.create(model=model, input=texts, dimensions=dims)
    return [d.embedding for d in resp.data]

def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def top_k(query_emb, corpus_embs, corpus_texts, k=5):
    scores = [(cosine(query_emb, e), t) for e, t in zip(corpus_embs, corpus_texts)]
    return sorted(scores, reverse=True)[:k]
```

## Best practices
- Use `text-embedding-3-small` for most tasks — 20x cheaper than `ada-002` with better quality; `text-embedding-3-large` only when retrieval recall is measurably insufficient
- Normalize embeddings before storing — cosine similarity on normalized vectors equals dot product, which most vector DBs optimize for
- Chunk documents at semantic boundaries (paragraphs, sections), not fixed token counts; overlap chunks by ~10% to avoid boundary misses
- Store both the embedding and the chunk text; never try to reverse-engineer text from an embedding
- Use `dimensions` reduction only after benchmarking recall — start at full dimensions, reduce if cost is prohibitive
- For Batch API jobs, assign meaningful `custom_id` values (e.g., `doc_{id}_chunk_{n}`) to correlate results to source records
- Cache embeddings for static content — re-embedding the same text wastes money and time

## AI-agent gotchas
- Agents must chunk long documents before embedding — silently truncated inputs produce poor embeddings
- The Batch API returns results out of order; always use `custom_id` to reconstruct order, never assume FIFO
- Embedding a query and a document with different `dimensions` settings produces incomparable vectors — validate config parity at startup
- Rate limits on the embeddings endpoint are separate from chat completions — an agent that embeds in a loop can exhaust embeddings limits while chat limits are untouched
- Do not embed sensitive PII into a shared vector store — data leaks via nearest-neighbor queries are a real attack surface

## References
- https://platform.openai.com/docs/guides/embeddings
- https://platform.openai.com/docs/api-reference/embeddings
- https://platform.openai.com/docs/guides/batch
- https://github.com/openai/openai-python
- https://arxiv.org/abs/2201.10005 (text-embedding-3 model card context)
