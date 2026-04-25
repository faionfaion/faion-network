# Agent Integration — Text Embeddings

## When to use
- Building semantic search or RAG — embeddings are the core retrieval primitive
- Deduplication of large document sets where exact-match fails but meaning-match works
- Clustering or topic modeling across a corpus without labeled training data
- Code search across a codebase where function names and signatures are insufficient
- Classification when labeled training data is scarce — use embedding similarity to known class exemplars

## When NOT to use
- Exact keyword or structured data lookup — BM25 or SQL is faster and more precise
- Tiny corpora (< 500 docs) — cosine similarity across all docs is trivially fast without indexing
- When the domain is highly specialized and no domain-adapted model exists — consider fine-tuning or BM25 fallback
- Real-time streaming data where batch embedding latency blocks the pipeline

## Where it fails / limitations
- MTEB benchmark scores do not predict real-world performance on domain-specific corpora — always benchmark on your own data
- Token limits bite hard: most models cap at 512–8192 tokens; long documents must be chunked first
- Embedding drift: if you switch models or update the model version, all stored vectors must be re-embedded — no partial migration
- Asymmetric search (query vs document) is not supported by OpenAI — Cohere and Voyage models provide `input_type` for this
- Quantization (int8, binary) trades ~1–5% recall for 4–32x memory savings; agents must test recall impact before enabling
- Multilingual models (BGE-M3, embed-multilingual-v3) are slower and may underperform language-specific models for dominant-language queries

## Agentic workflow
Agents embed in two phases: indexing (one-time or incremental batch) and query-time (per request). For indexing, the agent iterates the document corpus in batches of 100–2048 items, calls the embedding API, and upserts vectors into the vector DB. For query-time, the agent embeds the user query (single call) and searches the vector DB. The embedding model must be the same for both phases — agents should validate model identity before upsert. Use asymmetric `input_type` when the provider supports it.

### Recommended subagents
- `faion-sdd-executor-agent` — for tracked embedding pipeline setup with rollback
- General Claude subagent with Python tool — for model benchmarking and migration tasks

### Prompt pattern
```python
# Indexing phase — batch with input_type
import voyageai
client = voyageai.Client()
embeddings = client.embed(
    texts=batch_of_texts,
    model="voyage-3.5",
    input_type="document",
).embeddings

# Query phase
query_emb = client.embed(
    texts=[user_query],
    model="voyage-3.5",
    input_type="query",
).embeddings[0]
```

```python
# Self-hosted BGE-M3 with sentence-transformers
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-m3")
doc_embeddings = model.encode(documents, batch_size=64, normalize_embeddings=True)
query_embedding = model.encode([query], normalize_embeddings=True)[0]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` | OpenAI text-embedding-3-* | `pip install openai` · platform.openai.com/docs/guides/embeddings |
| `voyageai` | Voyage AI embedding client | `pip install voyageai` · docs.voyageai.com |
| `cohere` | Cohere embed-v4, multilingual | `pip install cohere` · docs.cohere.com/docs/cohere-embed |
| `sentence-transformers` | Local models (BGE-M3, MiniLM) | `pip install sentence-transformers` · sbert.net |
| `fastembed` | Fast CPU-optimized local embeddings | `pip install fastembed` · github.com/qdrant/fastembed |
| `litellm` | Unified embedding API across providers | `pip install litellm` · docs.litellm.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Embeddings API | SaaS | Yes — REST | `text-embedding-3-large` / `3-small`; Matryoshka dims |
| Voyage AI | SaaS | Yes — REST | SOTA retrieval; `voyage-3.5`; asymmetric input_type |
| Cohere Embed API | SaaS | Yes — REST | `embed-v4` multimodal; 128K context; 100+ languages |
| Hugging Face Inference API | SaaS | Yes — REST | Any SBERT-compatible model |
| AWS Bedrock (Titan Embeddings) | SaaS | Yes — AWS SDK | Native AWS; Titan Embed Text v2 |
| Google Vertex AI (Gecko) | SaaS | Yes — gCloud SDK | `text-embedding-005`; GCP native |
| Jina Embeddings API | SaaS | Yes — REST | `jina-embeddings-v3`; 8192 tokens; free tier |

## Templates & scripts
See `templates.md` for full embedding pipeline with caching and batching.

Inline: caching embedding wrapper with deduplication (< 50 lines):

```python
import hashlib, json
from functools import lru_cache
from openai import OpenAI

client = OpenAI()
_cache: dict[str, list[float]] = {}

def embed_texts(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    results = [None] * len(texts)
    to_embed = []
    indices = []
    for i, text in enumerate(texts):
        key = hashlib.sha256(f"{model}:{text}".encode()).hexdigest()
        if key in _cache:
            results[i] = _cache[key]
        else:
            to_embed.append(text)
            indices.append((i, key))
    if to_embed:
        response = client.embeddings.create(input=to_embed, model=model)
        for (i, key), item in zip(indices, response.data):
            _cache[key] = item.embedding
            results[i] = item.embedding
    return results
```

## Best practices
- Always use the same model version for indexing and query — even a minor version bump can produce incompatible embeddings
- Use asymmetric embedding (document/query input types) when Cohere or Voyage is available — measurably improves retrieval precision
- Batch document embedding in groups of 100–500 to balance API throughput and error recovery
- Cache query embeddings by hash — identical or near-identical queries are common in chat applications
- Reduce dimensions with Matryoshka models (OpenAI, Voyage, Cohere) rather than PCA — native truncation preserves relative ordering
- Normalize embeddings before storage (`normalize_embeddings=True`) — cosine similarity then equals dot product, enabling faster ANN algorithms
- Benchmark at least 3 models on 200+ real queries from your domain before choosing; MTEB scores frequently diverge from production results

## AI-agent gotchas
- Agents that embed user queries must not cache embeddings keyed only by text when the model changes — include model identifier in the cache key
- Token counting before embedding is mandatory: silent truncation at 8192 tokens changes the semantic meaning without raising an error
- OpenAI embedding API returns floats as 64-bit by default; storing as float32 in Qdrant/Weaviate halves storage and has negligible quality impact — agents must cast explicitly
- Do not embed HTML or markdown with tags intact — strip formatting before embedding or the model wastes token budget on structure tokens
- Voyage and Cohere support `input_type`; if an agent forgets to set `input_type="query"` for search and uses `document`, retrieval quality drops 3–8%
- Rate limits on embedding APIs (OpenAI: 1M tokens/min on tier 1) will throttle indexing of large corpora — implement exponential backoff with jitter

## References
- https://platform.openai.com/docs/guides/embeddings
- https://docs.voyageai.com/docs/embeddings
- https://docs.cohere.com/docs/cohere-embed
- https://sbert.net/
- https://huggingface.co/spaces/mteb/leaderboard
- https://arxiv.org/abs/2205.13147 (Matryoshka Representation Learning)
- https://arxiv.org/abs/2402.03216 (BGE-M3)
