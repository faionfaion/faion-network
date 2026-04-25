# Agent Integration — Embedding Basics

## When to use
- Any task requiring semantic similarity between texts (RAG retrieval, deduplication, clustering, classification without labeled data)
- Building the ingestion step of a RAG pipeline — every chunk must be embedded before storage
- Multilingual search where query and document languages may differ (use multilingual models)
- Cost optimization decisions: choosing between API-based and local embedding models
- Caching strategy design for high-volume embedding workloads

## When NOT to use
- Exact keyword matching is sufficient — embeddings add cost and latency with no semantic benefit
- The corpus is <500 texts that will never change — a one-time TF-IDF matrix is simpler and cheaper
- You need real-time streaming embeddings at sub-10ms latency — API round-trips make this infeasible; need a local model
- The domain is highly specialized (chemistry, genomics) and no domain-adapted model exists — embeddings will produce poor semantic similarity

## Where it fails / limitations
- Token limits: OpenAI `text-embedding-3-large` max 8191 tokens; chunks exceeding this are silently truncated, degrading embedding quality
- Embedding drift: switching models (e.g., `3-small` → `3-large`) invalidates the entire vector index — full re-ingestion required
- Dimension mismatch: storing vectors in a collection with a different dimension than the model output causes silent corruption or hard errors
- Local models (sentence-transformers) on CPU: `all-MiniLM-L6-v2` is ~5ms/text on CPU, but `bge-large-en-v1.5` is ~200ms — CPU inference at production scale is only viable with the smallest models
- Cache invalidation: text-based cache keys must include the model name — different models produce different vectors for the same text
- Deduplication before embedding via TF-IDF misses semantic duplicates (different wording, same meaning) — it is only a cost-reduction heuristic, not true semantic dedup

## Agentic workflow
An ingestion agent tokenizes and counts tokens per chunk before embedding, discards or splits chunks exceeding the model's token limit, batches remaining chunks into groups of 50-100, calls the embedding API, and stores vectors with model version in metadata. A separate caching layer (Redis) intercepts embed requests and returns cached vectors for previously seen texts. Model selection is a configuration-time decision; agents do not switch models at runtime.

### Recommended subagents
- `faion-sdd-executor-agent` — implements the embedding pipeline with batching, caching, and error handling
- Custom cost-estimation agent — calculates embedding cost for a corpus before ingestion (count tokens, multiply by rate)

### Prompt pattern
```
You are an embedding ingestion agent. Given: texts[], model_name, batch_size=100.
For each batch:
1. Check token count per text — skip any exceeding 8000 tokens (log warning).
2. Check Redis cache — retrieve cached embeddings for texts already seen.
3. For uncached texts: call embed API in one batch request.
4. Store results to Redis cache (TTL=30 days).
5. Return: {"embedded": N, "cache_hits": M, "skipped": K, "total_tokens": T}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` | OpenAI Embeddings API | `pip install openai` / [docs](https://platform.openai.com/docs/guides/embeddings) |
| `cohere` | Cohere Embed v3 API | `pip install cohere` / [docs](https://docs.cohere.com/docs/cohere-embed) |
| `voyageai` | Voyage AI embeddings | `pip install voyageai` / [docs](https://docs.voyageai.com/docs/embeddings) |
| `sentence-transformers` | Local SBERT/BGE/E5 models | `pip install sentence-transformers` / [docs](https://www.sbert.net/) |
| `tiktoken` | OpenAI tokenizer for token counting | `pip install tiktoken` / [GitHub](https://github.com/openai/tiktoken) |
| `fastembed` | Fast local embeddings (ONNX) | `pip install fastembed` / [GitHub](https://github.com/qdrant/fastembed) |
| `redis` | Embedding cache backend | `pip install redis` / [docs](https://redis.readthedocs.io/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Embeddings API | SaaS | Yes — batch up to 2048 | `text-embedding-3-small` ($0.02/1M) vs `3-large` ($0.13/1M) |
| Cohere Embed v3 | SaaS | Yes | Strong multilingual; 1024 dims; 512 token max |
| Voyage AI | SaaS | Yes | Best domain-specific quality for code + legal + medical |
| Hugging Face Inference API | SaaS | Yes — REST | Any MTEB-ranked model as a service; rate-limited on free tier |
| fastembed (OSS) | OSS | Yes — local ONNX | CPU-optimized; `BAAI/bge-small-en-v1.5` default |
| Ollama (local) | OSS | Yes | Run `nomic-embed-text` locally; no API cost |

## Templates & scripts
See `templates.md` for `EmbeddingCache` (file-based and Redis) and chunking implementations.

Batch embed with token-limit guard and Redis cache (40 lines):
```python
import hashlib, json, tiktoken
import redis as redis_lib

enc = tiktoken.get_encoding("cl100k_base")
rc = redis_lib.from_url("redis://localhost:6379")

def embed_batch_cached(client, texts: list[str], model: str, max_tokens=8000) -> list[list[float]]:
    results = [None] * len(texts)
    to_embed = []  # (original_index, text)

    for i, text in enumerate(texts):
        token_count = len(enc.encode(text))
        if token_count > max_tokens:
            text = enc.decode(enc.encode(text)[:max_tokens])  # truncate

        key = f"emb:{model}:{hashlib.sha256((model+text).encode()).hexdigest()}"
        cached = rc.get(key)
        if cached:
            results[i] = json.loads(cached)
        else:
            to_embed.append((i, text, key))

    if to_embed:
        resp = client.embeddings.create(input=[t for _, t, _ in to_embed], model=model)
        for j, (i, _, key) in enumerate(to_embed):
            emb = resp.data[j].embedding
            rc.setex(key, 86400*30, json.dumps(emb))
            results[i] = emb

    return results
```

## Best practices
- Always count tokens before embedding — use `tiktoken` for OpenAI models, `len(text.split())` * 1.3 as a rough heuristic for others
- Choose dimensions: `text-embedding-3-large` supports 256-3072 dims via `dimensions` param — 1024 dims preserves 95% quality at 67% lower storage cost
- Cache embeddings aggressively; repeat queries and re-ingested documents have 70-90% cache hit rate in typical RAG workloads
- Batch API requests: OpenAI accepts up to 2048 texts per call — single-text loops waste 99% of available throughput
- Store model name and version in chunk metadata — enables migration planning when you need to switch models
- Deduplicate texts by exact hash before embedding to avoid paying for identical embeddings

## AI-agent gotchas
- OpenAI embeddings API returns `response.data[i].embedding` as a plain Python list, not numpy — agents passing to Qdrant/Chroma must not call `.tolist()` (it's already a list)
- `text-embedding-3-large` with `dimensions=256` is not the same as `text-embedding-3-small` — they produce different vector spaces and cannot be mixed in the same collection
- Cohere's `embed-multilingual-v3.0` has a 512-token input limit — text exceeding this is silently truncated server-side; agents must chunk before calling
- fastembed's default model downloads on first use (~130MB); agents running in containers must pre-download models at build time, not at runtime
- Redis cache keys must include the model name — reusing the same key format for multiple models causes silent cross-model cache collisions
- Sentence-transformers models loaded with `SentenceTransformer(model_name)` on CPU will download and cache locally; first run may take 30-120s in CI/CD environments

## References
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Sentence Transformers Docs](https://www.sbert.net/)
- [Voyage AI Embeddings](https://docs.voyageai.com/docs/embeddings)
- [Cohere Embed v3](https://docs.cohere.com/docs/cohere-embed)
- [fastembed (Qdrant)](https://github.com/qdrant/fastembed)
- [Chunking Strategies Guide (Pinecone)](https://www.pinecone.io/learn/chunking-strategies/)
