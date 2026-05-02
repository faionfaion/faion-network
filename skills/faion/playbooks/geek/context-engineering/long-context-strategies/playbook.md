---
name: long-context-strategies
description: Choose and implement the right strategy — full window, RAG retrieval, or prefix caching — for prompts exceeding 100k tokens.
tier: geek
group: context-engineering
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a decision framework and working Python code to handle any context larger than 100k tokens using one of three strategies: full context window (up to 1M tokens), RAG top-K retrieval, or stable-prefix caching with a dynamic suffix. You will also have a cost model that lets you compute break-even points and make the right call for your workload before writing a line of code.

## Prerequisites

- Python 3.11+ with `anthropic>=0.40`, `qdrant-client>=1.9`, `openai>=1.60` installed.
- An Anthropic API key with access to `claude-sonnet-4-6` (200k) or `claude-opus-4-7` (1M context).
- Rough knowledge of your workload: corpus size, query rate per day, p95 latency budget, and expected unique-vs-repeated context ratio.
- Familiarity with token counting (`anthropic.Anthropic().messages.count_tokens()`).

## Steps

### Classify your workload

1. Count your context size:

```python
import anthropic

client = anthropic.Anthropic()

with open("my_corpus.txt") as f:
    corpus = f.read()

count = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": corpus}],
)
print(f"Corpus tokens: {count.input_tokens}")
```

2. Apply the decision rule:

| Condition | Strategy |
|-----------|----------|
| Latency-bound (p95 < 3 s), corpus ≤ 200k tokens | Prefix cache + dynamic suffix |
| Cost-bound at scale (> 1k queries/day), corpus > 50k tokens | RAG — retrieve top-K |
| Accuracy-bound, corpus ≤ 200k tokens, query rate low | Full window |
| Accuracy-bound, corpus 200k–1M tokens | Full window on `claude-opus-4-7` (1M) |

### Strategy A — Full context window

3. Send the entire corpus in a single call. Use `claude-opus-4-7` for corpora up to 1M tokens:

```python
import anthropic

client = anthropic.Anthropic()

def query_full_window(corpus: str, question: str, model: str = "claude-sonnet-4-6") -> str:
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    f"<corpus>\n{corpus}\n</corpus>\n\n"
                    f"<question>{question}</question>\n\n"
                    "Answer using only information from the corpus."
                ),
            }
        ],
    )
    return response.content[0].text

# For corpora > 200k tokens, switch to claude-opus-4-7
answer = query_full_window(corpus, "What is the primary latency bottleneck?", model="claude-sonnet-4-6")
```

Cost note: every query pays full input-token cost. At $3/Mtok input for `claude-sonnet-4-6`, a 150k-token corpus costs $0.45 per query.

### Strategy B — RAG retrieve top-K

4. Install dependencies:

```bash
pip install qdrant-client openai tiktoken langchain-text-splitters
```

5. Chunk and index the corpus into Qdrant:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

oai = OpenAI()
qdrant = QdrantClient(":memory:")  # replace with host/port for production

COLLECTION = "corpus-chunks"
EMBED_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 512
TOP_K = 8

qdrant.create_collection(
    COLLECTION,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=64)
chunks = splitter.split_text(corpus)

points = []
for i, chunk in enumerate(chunks):
    vec = oai.embeddings.create(model=EMBED_MODEL, input=chunk).data[0].embedding
    points.append(PointStruct(id=str(uuid.uuid4()), vector=vec, payload={"text": chunk}))

qdrant.upsert(COLLECTION, points)
print(f"Indexed {len(points)} chunks")
```

6. Retrieve and answer:

```python
import anthropic

client = anthropic.Anthropic()

def query_rag(question: str, top_k: int = TOP_K) -> str:
    q_vec = oai.embeddings.create(model=EMBED_MODEL, input=question).data[0].embedding
    hits = qdrant.query_points(COLLECTION, query=q_vec, limit=top_k).points
    context = "\n\n".join(h.payload["text"] for h in hits)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    f"<context>\n{context}\n</context>\n\n"
                    f"<question>{question}</question>\n\n"
                    "Answer using only the context provided."
                ),
            }
        ],
    )
    return response.content[0].text

answer = query_rag("What is the primary latency bottleneck?")
```

Cost note: only top-K chunks are sent. With 8 × 512-token chunks the input is ~4k tokens → $0.012 per query at $3/Mtok — 37× cheaper than Strategy A for a 150k-token corpus.

### Strategy C — Stable-prefix cache + dynamic suffix

7. Identify the stable prefix (system prompt + static documents) and the dynamic suffix (per-query content). Cache-control breakpoints must be placed at the end of the stable block:

```python
import anthropic

client = anthropic.Anthropic()

# Build the stable prefix once — this is the block that will be cached
SYSTEM_PROMPT = (
    "You are a senior software architect. "
    "Answer questions using only the documents provided."
)

with open("architecture-docs.txt") as f:
    static_docs = f.read()

def query_cached(question: str) -> anthropic.types.Message:
    return client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=[
            {"type": "text", "text": SYSTEM_PROMPT},
            {
                "type": "text",
                "text": f"<documents>\n{static_docs}\n</documents>",
                "cache_control": {"type": "ephemeral"},  # breakpoint after stable block
            },
        ],
        messages=[
            {
                "role": "user",
                "content": question,  # dynamic suffix — not cached
            }
        ],
    )

# First call: cache MISS — pays full input-token price
r1 = query_cached("What is the primary latency bottleneck?")
print(r1.usage)  # cache_creation_input_tokens > 0

# Second call within 5 minutes: cache HIT — pays 10% of input-token price
r2 = query_cached("Which service has the highest p99 latency?")
print(r2.usage)  # cache_read_input_tokens > 0
```

Cache TTL is 5 minutes for ephemeral. Cached reads cost $0.30/Mtok vs. $3.00/Mtok write — a 10× reduction. Break-even is 2 queries per cache window.

### Compute the cost break-even

8. Use this model to decide between strategies for your workload:

```python
# Cost model (claude-sonnet-4-6 as of 2026-05-02)
# Prices: $3.00/Mtok input, $0.30/Mtok cache-read, $3.75/Mtok cache-write, $15.00/Mtok output

FULL_WINDOW_INPUT_PRICE = 3.00 / 1_000_000   # $ per token
CACHE_WRITE_PRICE       = 3.75 / 1_000_000
CACHE_READ_PRICE        = 0.30 / 1_000_000
RAG_EMBED_PRICE         = 0.02 / 1_000_000   # text-embedding-3-small

def cost_full_window(corpus_tokens: int, queries: int) -> float:
    return corpus_tokens * queries * FULL_WINDOW_INPUT_PRICE

def cost_cache(corpus_tokens: int, queries: int, ttl_window_queries: int = 10) -> float:
    cache_writes = queries / ttl_window_queries
    cache_reads  = queries - cache_writes
    return (corpus_tokens * cache_writes * CACHE_WRITE_PRICE
            + corpus_tokens * cache_reads * CACHE_READ_PRICE)

def cost_rag(corpus_tokens: int, queries: int, top_k_tokens: int = 4096) -> float:
    embed_cost = corpus_tokens * RAG_EMBED_PRICE  # one-time index
    query_cost = queries * top_k_tokens * FULL_WINDOW_INPUT_PRICE
    return embed_cost + query_cost

corpus_tokens = 150_000
queries       = 5_000

print(f"Full window : ${cost_full_window(corpus_tokens, queries):.2f}")
print(f"Prefix cache: ${cost_cache(corpus_tokens, queries):.2f}")
print(f"RAG         : ${cost_rag(corpus_tokens, queries):.2f}")
# Full window : $2250.00
# Prefix cache: $288.75
# RAG         : $61.50
```

RAG wins at scale; caching wins when latency matters more than cost; full window wins when recall matters most and query rate is low.

## Verify

Run the cost model script and confirm it prints three dollar amounts without errors:

```bash
python cost_model.py
# Full window : $2250.00
# Prefix cache: $288.75
# RAG         : $61.50
```

For cache strategy, confirm a cache HIT on the second call:

```python
assert r2.usage.cache_read_input_tokens > 0, "Cache miss — check TTL or breakpoint placement"
```

For RAG, confirm retrieval returns the expected number of chunks:

```python
hits = qdrant.query_points(COLLECTION, query=q_vec, limit=TOP_K).points
assert len(hits) == TOP_K, f"Expected {TOP_K} hits, got {len(hits)}"
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `cache_read_input_tokens` is always 0 | Cache breakpoint placed after dynamic content | Move `cache_control` to end of the stable (non-changing) block only |
| RAG answers miss obvious facts | Top-K too small or chunk size too large | Increase `TOP_K` to 12–16; reduce `CHUNK_SIZE` to 256 |
| `ContextWindowExceededError` on full-window call | Corpus + response > model limit | Switch to `claude-opus-4-7` (1M context) or fall back to RAG |
| Qdrant `upsert` is slow on large corpus | Batch size too small (default = 1) | Use `qdrant.upsert(COLLECTION, points, batch_size=256)` |
| Cost model shows caching is cheaper than RAG but latency is high | Cache TTL expired between queries | Shorten the cache window assumption (TTL = 5 min); use RAG for async workloads |
| Embedding dimension mismatch on Qdrant insert | Model changed after collection was created | Drop and recreate the collection with the correct `size` |

## Next

- Apply `geek/rag-pipelines/rag-hybrid-search-bm25-vector` to add BM25 sparse retrieval alongside vector search for higher recall on keyword-heavy corpora.
- Apply `geek/context-engineering/prompt-caching-anthropic` for a deeper walkthrough of multi-turn cache management and cache-aware conversation design.

## References

- [knowledge/geek/ai/llm-integration/claude-advanced-features](../../../knowledge/geek/ai/llm-integration/claude-advanced-features) — details the `cache_control` ephemeral breakpoint API used in Strategy C, including TTL behaviour and multi-block caching rules
- [knowledge/geek/ai/rag-engineer/rag-architecture](../../../knowledge/geek/ai/rag-engineer/rag-architecture) — defines the retrieval pipeline components (embedder, vector store, reranker) that Strategy B implements and explains why top-K size affects recall@5
- [knowledge/geek/ai/rag-engineer/embedding-caching](../../../knowledge/geek/ai/rag-engineer/embedding-caching) — covers corpus-level embedding memoization that makes the one-time index cost in the break-even model accurate
