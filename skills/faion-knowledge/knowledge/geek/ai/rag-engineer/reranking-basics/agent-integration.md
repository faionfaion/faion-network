# Agent Integration — Reranking Basics

## When to use
- RAG pipelines where initial vector retrieval returns noisy or low-precision results
- High-stakes domains (legal, medical, compliance) where the top-k result must be correct
- After hybrid search to reconcile BM25 + vector rankings into a single ordered list
- When user queries are long or ambiguous and bi-encoder similarity scores are unreliable
- Production systems with latency budget >200ms per query and quality is the priority metric

## When NOT to use
- Latency-critical paths (<50ms budget) — cross-encoders add 100-500ms per call
- Candidate pool is already ≤5 results — reranking overhead exceeds benefit
- Corpus is multilingual and no suitable multilingual cross-encoder exists for the language mix
- Simple keyword lookup tasks — BM25 alone outperforms reranking for exact-match queries
- Cost is the primary constraint and Cohere/API reranking fees are prohibitive at scale

## Where it fails / limitations
- Cross-encoder latency scales linearly with candidate pool size; 100 candidates × 500ms = unusable
- `cross-encoder/ms-marco-*` models are English-only; applying them to Ukrainian/French/etc. silently degrades precision
- Cohere reranking API has rate limits and adds external API dependency to the hot path
- LLM reranking (ask GPT-4 to score) is the most accurate but 10-50× more expensive than cross-encoders
- MMR diversity reranking requires embeddings of all candidates at rerank time — doubles embedding cost
- Score scales differ across rerankers; mixing scores (e.g., from two different rerankers for AB testing) is not directly comparable

## Agentic workflow
A retrieval subagent fetches an initial candidate pool (top 50-100 via vector search), then passes `(query, documents[])` to a reranking step. The reranker (cross-encoder or Cohere API) returns scored pairs, and the agent selects the top-k for context assembly. The reranking step is synchronous and blocking — the generation agent should not proceed until reranking is complete. A fallback must exist: if the reranker is unavailable, use initial retrieval scores directly rather than failing the query.

### Recommended subagents
- `faion-sdd-executor-agent` — implement the two-stage retrieval + reranking pipeline as a task within a RAG system build

### Prompt pattern
```
You have a query and a list of candidate documents from initial retrieval.
Score each document's relevance to the query on a scale of 0-1.
Return a JSON array sorted by score descending:
[{"index": <original_index>, "score": <float>, "reason": "<one sentence>"}]

Query: {{query}}
Candidates:
{{#each candidates}}
[{{@index}}] {{this}}
{{/each}}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `sentence-transformers` | Local cross-encoder reranking | `pip install sentence-transformers` · https://www.sbert.net |
| `cohere` | Cohere Rerank API (rerank-english-v3.0, rerank-multilingual-v3.0) | `pip install cohere` · https://docs.cohere.com/docs/reranking |
| `flashrank` | Lightweight local reranker (ms-marco, MiniLM variants) | `pip install flashrank` · https://github.com/PrithivirajDamodaran/FlashRank |
| `ragatouille` | ColBERT late-interaction reranking | `pip install ragatouille` · https://github.com/bclavie/RAGatouille |
| `llama-index-postprocessor-cohere-rerank` | LlamaIndex Cohere rerank postprocessor | `pip install llama-index-postprocessor-cohere-rerank` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cohere Rerank | SaaS | Yes (REST/Python SDK) | Best managed option; rerank-multilingual-v3.0 covers 100+ languages |
| Jina AI Reranker | SaaS | Yes (REST) | jina-reranker-v2-base-multilingual; free tier available |
| Mixedbread AI | SaaS | Yes (REST/Python) | mxbai-rerank-large-v1; strong BEIR benchmark scores |
| Voyage AI | SaaS | Yes (REST) | voyage-rerank-2; especially strong for code and technical content |
| vLLM | OSS | Yes (OpenAI-compat API) | Run cross-encoders locally as a service; GPU recommended |

## Templates & scripts
See `templates.md` for cross_encoder_rerank, RerankingRAG, batch_rerank, and diverse_rerank (MMR) templates.

Inline — production reranking with fallback:
```python
def rerank_with_fallback(
    query: str,
    results: list[dict],
    top_k: int = 5,
    timeout: float = 2.0
) -> list[dict]:
    """Rerank with graceful fallback to initial order."""
    import signal

    def _handler(signum, frame):
        raise TimeoutError

    try:
        signal.signal(signal.SIGALRM, _handler)
        signal.alarm(int(timeout))
        from sentence_transformers import CrossEncoder
        model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")
        pairs = [[query, r["content"]] for r in results]
        scores = model.predict(pairs)
        for r, s in zip(results, scores):
            r["rerank_score"] = float(s)
        signal.alarm(0)
        return sorted(results, key=lambda x: x["rerank_score"], reverse=True)[:top_k]
    except Exception:
        return results[:top_k]  # fallback: initial retrieval order
```

## Best practices
- Retrieve 3-10× more candidates than the final top-k; reranking cannot recover relevant docs not in the candidate pool
- Use `cross-encoder/ms-marco-MiniLM-L-12-v2` as the default local reranker — best accuracy/latency ratio for English
- For multilingual content, use `cohere rerank-multilingual-v3.0` or `Jina jina-reranker-v2-base-multilingual`
- Cache reranked results by `hash(query + sorted(doc_ids))` — identical queries with the same candidate pool repeat often in chat interfaces
- Truncate documents to 512 tokens before passing to cross-encoder; longer inputs reduce quality and spike latency
- Log `initial_rank` vs `rerank_rank` to detect systematic retrieval failures (documents always ranked low initially but promoted by reranker indicate embedding model mismatch)

## AI-agent gotchas
- Cross-encoders run on CPU by default in sentence-transformers; agents on CPU-only infra should use FlashRank (designed for CPU) or the Cohere API
- Cohere Rerank API returns results in a different order than the input list; always use `r.index` to map back to original docs, not list position
- LLM-based reranking prompts must constrain output to JSON; without schema enforcement the agent may produce freeform ranking prose that breaks the parser
- Batch reranking with ThreadPoolExecutor can hit `ulimit` on open file descriptors when candidate pool size × workers is large — test with realistic loads
- MMR diversity reranking requires embeddings at rerank time; if the agent discarded embeddings after indexing they must be recomputed, doubling cost

## References
- https://www.sbert.net/examples/applications/cross-encoder/README.html
- https://docs.cohere.com/docs/reranking
- https://arxiv.org/abs/2112.09118 (MS MARCO cross-encoder training)
- https://github.com/PrithivirajDamodaran/FlashRank
- https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf (MMR)
