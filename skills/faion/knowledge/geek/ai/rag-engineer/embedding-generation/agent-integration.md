# Agent Integration — Embedding Generation

## When to use
- Building the indexing step of any RAG pipeline (chunks → vectors)
- Implementing semantic search over a document corpus
- Text clustering, deduplication by semantic similarity, or recommendation systems
- Evaluating embedding model options for a new project before committing to a provider
- Optimizing an existing embedding pipeline for cost, latency, or quality

## When NOT to use
- Exact-string keyword search is sufficient — embeddings add cost/latency with no precision gain for exact matches
- Very short texts (<10 tokens) embed poorly; BM25 outperforms semantic similarity at this scale
- Corpus is in a low-resource language without a multilingual embedding model — embeddings may produce near-random vectors
- Storage budget is constrained and 1536-3072 dimension vectors would overflow it — benchmark with reduced dimensions first

## Where it fails / limitations
- Model mismatch: indexing with `text-embedding-3-large` but querying with `text-embedding-3-small` produces incorrect similarity scores (different vector spaces)
- Token limit violations are silent in some SDKs; texts >8191 tokens are truncated without error, losing tail content
- File-based EmbeddingCache uses MD5 for keys — MD5 collision probability is non-zero at billion-document scale; use SHA-256 in production
- OpenAI batch API has 2048-item-per-request limit; exceeding it raises a 400 error, not a graceful split
- Local models (SentenceTransformers) load the full model into GPU/CPU RAM at init — agents must not instantiate multiple model instances per process
- Ollama embedding has no native batching; the loop-per-text approach in the reference impl is O(n) API calls

## Agentic workflow
An embedding subagent receives a list of `{id, text}` chunk dicts, batches them into groups of 100 (API) or 32 (local GPU), generates embeddings, and returns `{id, embedding, model, dimensions}` dicts. A separate upsert subagent writes the embeddings to the vector store. The two steps are decoupled so embedding failures do not corrupt the index. A validation subagent spot-checks 1% of embeddings by computing cosine similarity between semantically similar chunk pairs and flagging pairs with similarity <0.7.

### Recommended subagents
- `faion-sdd-executor-agent` — execute the embedding generation step as a task within the RAG ingestion pipeline

### Prompt pattern
```
Generate embeddings for the following texts using the configured provider.
Return a JSON array where each entry is {id, embedding_preview (first 5 values), dimensions, model}.
Use batch size 100. Log how many texts were processed and total API cost if available.

Texts (JSON array of {id, text}):
{{texts_json}}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` | OpenAI text-embedding-3-small/large via Python SDK | `pip install openai` · https://platform.openai.com/docs/guides/embeddings |
| `sentence-transformers` | Local embedding models (BGE, MiniLM, E5, nomic) | `pip install sentence-transformers` · https://www.sbert.net |
| `cohere` | Cohere embed-english-v3.0 / embed-multilingual-v3.0 | `pip install cohere` · https://docs.cohere.com/reference/embed |
| `ollama` | Local embedding via Ollama server (nomic-embed-text) | https://ollama.com/blog/embedding-models |
| `mistralai` | Mistral embed model | `pip install mistralai` · https://docs.mistral.ai/capabilities/embeddings/ |
| `FlagEmbedding` | BGE-M3 with sparse + dense embedding | `pip install FlagEmbedding` · https://huggingface.co/BAAI/bge-m3 |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Embeddings API | SaaS | Yes (REST/SDK) | text-embedding-3-small ($0.02/1M) best price/quality ratio; supports native dimension reduction |
| Cohere Embed v3 | SaaS | Yes (REST/SDK) | Asymmetric input_type (document/query) improves RAG retrieval; multilingual model available |
| Voyage AI | SaaS | Yes (REST/Python) | voyage-3 ($0.06/1M, 32K context); voyage-code-3 for code search |
| Mistral AI | SaaS | Yes (REST/SDK) | mistral-embed; strong multilingual; 1B context window |
| Ollama (local) | OSS | Yes (REST) | nomic-embed-text, mxbai-embed-large; requires local GPU/CPU server |
| HuggingFace Inference API | SaaS | Yes (REST) | Run any MTEB-ranked model in the cloud; serverless option available |

## Templates & scripts
See `templates.md` for EmbeddingService, EmbeddingCache, normalize_embedding, and get_embeddings_async templates.

Inline — async batch embedding with rate-limit retry:
```python
import asyncio, time, random
from openai import AsyncOpenAI, RateLimitError

async def embed_batch_async(
    texts: list[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 100,
    max_concurrent: int = 5,
) -> list[list[float]]:
    client = AsyncOpenAI()
    sem = asyncio.Semaphore(max_concurrent)

    async def _one_batch(batch: list[str], attempt: int = 0) -> list[list[float]]:
        async with sem:
            try:
                resp = await client.embeddings.create(input=batch, model=model)
                return [e.embedding for e in sorted(resp.data, key=lambda x: x.index)]
            except RateLimitError:
                await asyncio.sleep((2 ** attempt) + random.random())
                return await _one_batch(batch, attempt + 1)

    batches = [texts[i:i+batch_size] for i in range(0, len(texts), batch_size)]
    results = await asyncio.gather(*[_one_batch(b) for b in batches])
    return [emb for batch in results for emb in batch]
```

## Best practices
- Always use the same model for indexing and query embedding — cross-model queries produce meaningless scores
- Normalize embeddings to unit length before storing; enables dot-product similarity (faster than cosine on most vector DBs)
- For OpenAI text-embedding-3 models, use `dimensions=512` as default unless high-precision retrieval is required — 95% quality at 33% storage and cost
- Use Cohere's `input_type` parameter asymmetrically: `search_document` for indexing, `search_query` at query time
- Pre-check all texts for empty strings, whitespace-only, and >token-limit content before embedding — all three produce zero or truncated vectors
- Cache embeddings with `hash(model + text)` as key; re-embedding identical texts on re-index is the largest hidden cost in production pipelines

## AI-agent gotchas
- Agents using `EmbeddingCache` with MD5 keys should switch to SHA-256 for corpora >10M chunks — collision risk becomes measurable
- Local SentenceTransformer models require the first call to download the model from HuggingFace; agents in airgapped environments must pre-cache model weights
- BGE models require an instruction prefix for queries (`"Represent this sentence for retrieval: "`) but NOT for documents — omitting the prefix on queries degrades recall ~5-10%
- `ollama.embeddings()` is synchronous and not batched — for >1000 texts, agents must implement their own async wrapper or use a faster local server
- When the EmbeddingService falls back on exception, it returns None by default in some implementations — downstream vector DB upserts will fail with a type error; always validate embedding shape before upsert

## References
- https://platform.openai.com/docs/guides/embeddings
- https://www.sbert.net/
- https://huggingface.co/spaces/mteb/leaderboard (MTEB benchmark — model comparison)
- https://docs.cohere.com/reference/embed
- https://huggingface.co/BAAI/bge-m3
