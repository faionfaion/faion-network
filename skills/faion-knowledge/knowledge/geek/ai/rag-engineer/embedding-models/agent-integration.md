# Agent Integration — Embedding Models

## When to use
- Selecting an embedding model at the start of a RAG project (model selection is a load-bearing decision)
- Benchmarking multiple embedding providers to find the best price/quality ratio for a specific corpus
- Migrating an existing RAG index from one model to another (e.g., ada-002 → text-embedding-3-large)
- Building a code-search RAG where general-purpose models underperform (use voyage-code-3 or BGE-M3)
- Processing multilingual corpora where English-only models degrade retrieval quality

## When NOT to use
- Corpus is already indexed with a specific model and migration cost outweighs quality gain — benchmark first
- Latency budget <20ms — local models add model-load overhead; API models add network RTT
- Fully offline / air-gapped deployment with no GPU — local models on CPU are slow for batches >1k; consider a cached pre-indexed corpus instead

## Where it fails / limitations
- Native dimension reduction (`dimensions` param) only works for OpenAI text-embedding-3 models; applying it to ada-002 raises an error
- Cohere's `input_type` parameter is mandatory for v3 models; omitting it defaults to a generic mode that underperforms asymmetric retrieval by ~5-10% NDCG
- BGE-M3 sparse embeddings (lexical_weights) are dicts of token→weight, not dense arrays; vector DBs that expect dense arrays cannot store them without adaptation
- Sentence-transformers GPU inference requires matching CUDA/torch versions; a CUDA version mismatch silently falls back to CPU without an error
- OpenAI batch API sorts embeddings by index in the response, but agents that skip the sort step will get misaligned embeddings for shuffled batches
- Mistral embed has a 512-token context limit on some model versions — longer texts are silently truncated

## Agentic workflow
An agent first selects the embedding model based on three inputs: corpus language, corpus type (text/code/multilingual), and cost/latency constraints. It documents the selection rationale and pins the model name + version in a config file. An embedding subagent runs batched embedding generation using the selected model, handling rate limits with exponential backoff. A validation subagent checks embedding dimensionality, absence of zero vectors, and spot-checks similarity scores between semantically related pairs. Model selection requires human sign-off before the full corpus is indexed because a model change invalidates the entire index.

### Recommended subagents
- `faion-sdd-executor-agent` — implement model selection and embedding generation as adjacent tasks in the RAG ingestion pipeline

### Prompt pattern
```
Select the best embedding model for the following requirements:
- Corpus language: {{language}}
- Corpus type: {{type}} (text/code/mixed)
- Avg document length: {{avg_tokens}} tokens
- Budget constraint: {{budget}} per 1M tokens
- Latency requirement: {{latency_ms}}ms per query

Return JSON: {model, provider, dimensions, rationale, estimated_monthly_cost}
Constrain: prefer models on MTEB leaderboard top-20 for the target language.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` | text-embedding-3-small/large with native dimension reduction | `pip install openai` · https://platform.openai.com/docs/guides/embeddings |
| `sentence-transformers` | Local: BGE, E5, MiniLM, nomic; GPU-accelerated batch | `pip install sentence-transformers` · https://www.sbert.net |
| `FlagEmbedding` | BGE-M3 dense + sparse + colbert embeddings | `pip install FlagEmbedding` · https://huggingface.co/BAAI/bge-m3 |
| `cohere` | embed-english-v3.0 / embed-multilingual-v3.0 | `pip install cohere` · https://docs.cohere.com/docs/cohere-embed |
| `mistralai` | mistral-embed (1024 dims, 512 context) | `pip install mistralai` · https://docs.mistral.ai/capabilities/embeddings/ |
| `voyageai` | voyage-3, voyage-code-3 | `pip install voyageai` · https://docs.voyageai.com/docs/embeddings |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Embeddings | SaaS | Yes (REST/SDK) | Best for general English text; text-embedding-3-small is the default recommendation |
| Cohere Embed v3 | SaaS | Yes (REST/SDK) | Best asymmetric retrieval; multilingual-v3.0 covers 100+ languages |
| Voyage AI | SaaS | Yes (REST/Python) | voyage-code-3 best for code; voyage-3 strong general; 32K context |
| Mistral AI | SaaS | Yes (REST/SDK) | mistral-embed; competitive multilingual performance |
| HuggingFace Inference API | SaaS | Yes (REST) | Any SBERT-compatible model; serverless option; pay-per-request |
| Ollama (local) | OSS | Yes (REST) | nomic-embed-text, mxbai-embed-large; zero cost; requires local server |
| NVIDIA NIM | SaaS/On-prem | Yes (OpenAI-compat) | Run embedding models on NVIDIA GPU cloud or self-hosted |

## Templates & scripts
See `templates.md` for OpenAI batch, Matryoshka dimension reduction, Cohere asymmetric, local SentenceTransformer, BGE-M3, async batch, retry, and EmbeddingPipeline templates.

Inline — model selection helper:
```python
def select_embedding_model(
    language: str,
    content_type: str,  # "text", "code", "mixed"
    budget_per_million: float,  # USD
) -> dict:
    if content_type == "code":
        return {"model": "voyage-code-3", "provider": "voyageai", "dims": 1024}
    if language != "en":
        if budget_per_million < 0.10:
            return {"model": "BAAI/bge-m3", "provider": "local", "dims": 1024}
        return {"model": "embed-multilingual-v3.0", "provider": "cohere", "dims": 1024}
    if budget_per_million < 0.05:
        return {"model": "text-embedding-3-small", "provider": "openai", "dims": 1536}
    return {"model": "text-embedding-3-large", "provider": "openai", "dims": 3072}
```

## Best practices
- Pin the exact model name (including version suffix if the provider uses them) in config — providers silently update model weights
- Run MTEB benchmark scores for your specific task type (retrieval vs. clustering vs. classification) — aggregate MTEB rank ≠ RAG retrieval rank
- For OpenAI text-embedding-3 models, start with `dimensions=512`; benchmark vs. full 1536/3072 before paying for extra storage
- Always use Cohere `input_type="search_document"` at index time and `input_type="search_query"` at query time — asymmetric embedding is a significant quality lever
- Pre-normalize all embeddings to unit length before storing; dot product then equals cosine similarity and is faster in most vector DBs
- Track the model name as metadata on every vector — if you ever need to migrate, you can identify which vectors need re-embedding

## AI-agent gotchas
- OpenAI batch API returns embeddings in a list that may not be in input order; always sort by `response.data[i].index` before pairing with input texts
- BGE-M3 `lexical_weights` output is a sparse dict per document, not a dense array — agents expecting `list[float]` will crash; handle both dense and sparse paths
- SentenceTransformer model download at first use can take 30s-5min; agents in time-bounded tasks must pre-download models or use a local model cache
- When using Matryoshka dimension reduction (`dimensions` param), the truncated vector is NOT simply the first N values of the full vector — it is separately trained; do not slice full-dim embeddings manually
- Voyage AI and Cohere have per-request token limits (varies by plan); agents must chunk texts before calling embed for texts >model context limit

## References
- https://platform.openai.com/docs/guides/embeddings
- https://docs.mistral.ai/capabilities/embeddings/
- https://docs.cohere.com/docs/cohere-embed
- https://huggingface.co/BAAI/bge-m3
- https://www.sbert.net/
- https://huggingface.co/spaces/mteb/leaderboard (MTEB leaderboard)
- https://docs.voyageai.com/docs/embeddings
