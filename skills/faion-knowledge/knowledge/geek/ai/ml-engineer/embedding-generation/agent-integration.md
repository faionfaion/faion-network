# Agent Integration — Embedding Generation

## When to use
- Agent needs semantic search over a document corpus (RAG, knowledge base retrieval)
- Deduplication of items before processing: compare embeddings to skip near-duplicates
- Routing agent queries to the right specialized sub-agent based on semantic similarity to example inputs
- Clustering unlabeled agent outputs to identify patterns or failure modes
- Building a memory layer: encode past agent interactions, retrieve relevant context for new tasks

## When NOT to use
- Keyword-exact matching (product SKUs, error codes, IDs) — BM25 or SQL LIKE is faster and cheaper
- Real-time response generation — embedding is a pre-processing step, not inline generation
- When corpus changes every second — index rebuild lag makes embeddings stale before they're useful
- Very short texts (<5 words) — embeddings for short strings are unreliable; use exact match instead
- When all queries are highly specific technical terms (code identifiers, domain acronyms) — domain-specific models needed

## Where it fails / limitations
- Model mismatch: querying with a different model than was used for indexing produces garbage similarity scores — always document model name + version in the index metadata
- Empty string embeddings produce zero vectors — must filter or the results are meaningless and pollute rankings
- Token limit truncation: texts exceeding the model's context (8191 tokens for OpenAI 3-large) are silently truncated — long documents need chunking before embedding
- Dimension mismatch: mixing embeddings from different models or different dimension settings causes silent errors in vector DBs that don't enforce schema
- Cosine similarity ceiling: at very high similarity (>0.98), small numerical differences no longer reflect meaningful semantic difference — don't over-optimize threshold
- Reindexing after fine-tuning or model change: all existing embeddings are invalid; complete reindex is required

## Agentic workflow
Agents use embedding generation as a retrieval gate: before making an LLM call, an agent embeds the user query and retrieves the top-K relevant chunks from a vector store. The retrieved context is injected into the LLM prompt. For memory systems, agent outputs are embedded and stored after each interaction; on the next invocation, the agent retrieves the most relevant prior interactions. Batch embed at ingestion time; generate single-query embeddings at inference time. Use a two-stage pipeline: cheap embedding model for recall (top-100), reranker for precision (top-10).

### Recommended subagents
- RAG retrieval agents (rag-engineer skill) use embedding generation as their core primitive
- Memory agents that persist and retrieve past agent interactions

### Prompt pattern
Query embedding + retrieval (Python):
```python
from openai import OpenAI
import numpy as np

client = OpenAI()

def embed(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """Generate normalized embedding for a single text."""
    text = text.replace("\n", " ").strip()
    if not text:
        raise ValueError("Cannot embed empty text")
    resp = client.embeddings.create(input=[text], model=model)
    vec = np.array(resp.data[0].embedding)
    return (vec / np.linalg.norm(vec)).tolist()  # normalize for cosine similarity

def batch_embed(texts: list[str], model: str = "text-embedding-3-small", batch_size: int = 100) -> list[list[float]]:
    """Batch embed with chunking to stay within API limits."""
    results = []
    for i in range(0, len(texts), batch_size):
        batch = [t.replace("\n", " ").strip() for t in texts[i:i+batch_size]]
        resp = client.embeddings.create(input=batch, model=model)
        for item in sorted(resp.data, key=lambda x: x.index):
            vec = np.array(item.embedding)
            results.append((vec / np.linalg.norm(vec)).tolist())
    return results
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` | text-embedding-3-small/large via API | `pip install openai` / platform.openai.com/docs/guides/embeddings |
| `cohere` | embed-v4 (multilingual, multimodal) | `pip install cohere` / docs.cohere.com/reference/embed |
| `sentence-transformers` | Local embedding generation (BGE-M3, nomic) | `pip install sentence-transformers` / sbert.net |
| `ollama` | nomic-embed-text, mxbai-embed-large locally | `ollama pull nomic-embed-text` / ollama.com |
| `voyageai` | voyage-3-large, voyage-3.5-lite (RAG-optimized) | `pip install voyageai` / docs.voyageai.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Embeddings API | SaaS | Yes | text-embedding-3-large: best general quality; supports dimension reduction |
| Cohere Embed API | SaaS | Yes | embed-v4: multilingual (100+ languages), task-type input hint |
| Voyage AI | SaaS | Yes | Best for domain-specific RAG (legal, medical, code); trained on tricky negatives |
| Qdrant | OSS | Yes | Vector DB; self-hosted; ideal for production agentic retrieval |
| Chroma | OSS | Yes | Dev/test vector store; in-memory or persistent |
| pgvector | OSS | Yes | PostgreSQL extension; good when you already use Postgres |

## Templates & scripts
See `templates.md` for: production embedding service with Redis cache, batch job with sorted-by-length optimization, Qdrant upsert pipeline.

Inline: embedding cache with content-hash key (~30 lines):

```python
import hashlib, json
from redis import Redis

redis = Redis(host="localhost", port=6379, db=0)
EMBED_MODEL = "text-embedding-3-small"

def cached_embed(text: str, client) -> list[float]:
    """Embed with exact-match Redis cache. Key = hash(model + text)."""
    key = f"emb:{EMBED_MODEL}:{hashlib.sha256(f'{EMBED_MODEL}:{text}'.encode()).hexdigest()}"
    cached = redis.get(key)
    if cached:
        return json.loads(cached)
    resp = client.embeddings.create(input=[text], model=EMBED_MODEL)
    vec = resp.data[0].embedding
    redis.setex(key, 86400, json.dumps(vec))  # 24h TTL
    return vec
```

## Best practices
- Always normalize embeddings before storing — enables dot product as a faster proxy for cosine similarity
- Sort batch inputs by token length before API calls — reduces padding waste, improves throughput ~40%
- Store embedding model name and version in index metadata — makes future migration auditable
- Use Cohere's `input_type` parameter (`search_document` vs `search_query`) — it materially improves retrieval precision
- Implement two-stage retrieval: embed-based recall (top-100) → reranker precision (top-10) — reduces cost while maintaining quality
- Cache embeddings for queries: user questions repeat more than you expect; Redis cache cut API calls 30-60% in production
- For multilingual corpora, use Cohere embed-v4 or BGE-M3 — OpenAI 3-large performance degrades outside English

## AI-agent gotchas
- Human-in-loop checkpoint: when retrieval quality (relevance scores) drops below threshold, the agent should ask the user to clarify rather than hallucinating from low-quality context
- Never reuse an existing embedding index after changing the embedding model — the resulting similarity scores are meaningless; complete reindex required
- Embedding API rate limits apply per minute of input tokens, not per request — large batch jobs hit limits unexpectedly; implement backoff
- Zero-vector trap: filtering empty texts before embedding is mandatory — a zero vector matches everything at similarity ~0 and poisons rankings
- Dimension reduction (e.g., OpenAI 3-large from 3072 → 1024 dimensions) reduces storage and latency but slightly reduces recall; test on your actual query distribution before applying globally

## References
- https://platform.openai.com/docs/guides/embeddings
- https://docs.cohere.com/reference/embed
- https://docs.voyageai.com/
- https://www.sbert.net/
- https://huggingface.co/spaces/mteb/leaderboard
- https://blog.skypilot.co/large-scale-embedding/
- https://www.mongodb.com/company/blog/engineering/token-count-based-batching-faster-cheaper-embedding-inference-for-queries
