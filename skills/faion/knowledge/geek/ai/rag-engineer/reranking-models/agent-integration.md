# Agent Integration — Reranking Models & Services

## When to use
- RAG pipelines where first-stage retrieval recall is high but precision is low — top-50 contains the answer but top-5 does not
- Two-stage retrieval: fast ANN (k=50-100) → rerank to top-5 for generation
- Domain-specific corpora where embedding similarity scores are poorly calibrated (legal, medical, code)
- Multilingual retrieval where the query and document languages may differ
- Production pipelines that can tolerate 100-400ms additional latency per query for precision gains

## When NOT to use
- First-stage retrieval precision is already acceptable (precision@5 > 0.85) — reranking adds latency and cost with diminishing returns
- Latency SLA is <100ms total — even fast local cross-encoders add 20-50ms
- Document corpus is short (<200 chars per chunk) — cross-encoders underperform on very short texts
- Cost is the primary constraint and a small local model is not viable — skip and improve chunking instead
- Queries are purely keyword-based with no semantic ambiguity — BM25 or hybrid search already handles these well

## Where it fails / limitations
- Cohere and Jina rerankers have per-request document count limits (Cohere: 10K total chars per document, max 1000 documents)
- LLM-based reranking (GPT-4o scoring) is 500-2000ms and $$$; viable only for low-QPS offline workflows
- Cross-encoder models score query-document pairs independently — they cannot compare documents to each other, which means ties are broken arbitrarily
- Reranker output scores are not calibrated probabilities — a score of 0.9 from Cohere vs 0.9 from a local cross-encoder mean different things; do not compare scores across providers
- Local cross-encoders require GPU for production throughput; CPU inference on MiniLM-L6 is ~30ms/pair, which becomes 1500ms for 50 candidates
- Reranking does not fix a retrieval failure — if the correct document was not retrieved in the first stage, reranking cannot surface it

## Agentic workflow
The retrieval agent fetches top-50 candidates from the vector store using ANN. A reranking agent receives the query and all 50 candidate texts, calls the configured reranking service, and returns the top-5 re-ranked results to the generation agent. The reranking step is wrapped in a fallback: if the service fails or times out, the original retrieval order is preserved. The choice of reranking service (Cohere vs local cross-encoder) is a configuration decision made at deployment time, not by the agent at runtime.

### Recommended subagents
- `faion-sdd-executor-agent` — provisions and wires the reranking service into the RAG pipeline
- Custom reranking agent — calls the rerank API with error handling and fallback to original ordering

### Prompt pattern
```
You are a reranking agent. Given: query, list of {id, text} candidates.
Steps:
1. Call rerank API with query and candidate texts.
2. If API fails, return candidates in original order with warning.
3. Return top-K reranked candidates: [{id, text, score, original_rank, new_rank}]
4. Log score delta between original_rank=1 and new_rank=1.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cohere` | Cohere Rerank API client | `pip install cohere` / [docs](https://docs.cohere.com/docs/reranking) |
| `voyageai` | Voyage AI rerank client | `pip install voyageai` / [docs](https://docs.voyageai.com/docs/reranker) |
| `sentence-transformers` | Local cross-encoder models | `pip install sentence-transformers` / [docs](https://www.sbert.net/docs/cross_encoder/usage/usage.html) |
| `requests` | Jina Rerank REST calls | stdlib / [Jina docs](https://jina.ai/reranker/) |
| `langchain` | `CohereRerank` + `ContextualCompressionRetriever` | `pip install langchain-cohere` / [docs](https://python.langchain.com/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cohere Rerank | SaaS | Yes — Python client | `rerank-english-v3.0` best English quality; 100-300ms |
| Jina Reranker | SaaS | Yes — REST | `jina-reranker-v2-base-multilingual`; multilingual |
| Voyage AI Rerank | SaaS | Yes — Python client | `rerank-2`; strong on domain-specific text |
| MixedBread AI | SaaS | Yes — REST | `mxbai-rerank-large-v1`; competitive quality |
| Local CrossEncoder (ms-marco) | OSS | Yes — runs in-process | `ms-marco-MiniLM-L-12-v2` best quality/latency tradeoff |
| LangChain CohereRerank | OSS wrapper | Yes | Drop-in compressor for LangChain retrieval chains |

## Templates & scripts
See `templates.md` for `RerankerService` with fallback and FastAPI endpoint.

Minimal production-safe rerank wrapper with fallback:
```python
import logging, time
logger = logging.getLogger(__name__)

def rerank_with_fallback(reranker_fn, query, candidates, top_k=5):
    """candidates: list of str. Returns list of {text, score, index}."""
    try:
        start = time.time()
        results = reranker_fn(query, candidates, top_k)
        logger.info(f"Rerank: {len(candidates)} → {top_k} in {time.time()-start:.3f}s")
        return results
    except Exception as e:
        logger.error(f"Rerank failed ({e}), using original order")
        return [{"text": c, "score": 1.0 - i/len(candidates), "index": i}
                for i, c in enumerate(candidates[:top_k])]
```

## Best practices
- Always retrieve 5-10x the final top-K at stage 1, then rerank to final top-K — reranking is most effective with a larger candidate pool
- Use a local cross-encoder (`ms-marco-MiniLM-L-12-v2`) for latency-sensitive paths; Cohere/Jina for batch offline eval
- Attach `metadata` separately from document texts when calling the API — do not include metadata in the text passed for scoring, as it dilutes the relevance signal
- Monitor the rank delta (original rank vs reranked rank) per query — a consistently low delta means stage-1 retrieval is already good and reranking may not be worth the cost
- Cache reranking results for identical (query, candidate_set) pairs with a short TTL (5 minutes) — repeated queries in chatbot sessions benefit significantly
- For multilingual pipelines, use `jina-reranker-v2-base-multilingual` or `mmarco-mMiniLMv2-L12` local model rather than English-only Cohere

## AI-agent gotchas
- Cohere API returns results indexed into the original `documents` list — agents must preserve the original list order and use `result.index` to map back, not assume results are in input order
- Local CrossEncoder `.predict(pairs)` takes a list of `[query, doc]` pairs, not a flat list — agents must zip query with each candidate correctly
- LLM-based reranking with JSON output can return indices out of range if the LLM hallucinates — agents must bounds-check all `rankings` values before indexing into the candidate list
- Reranker score is not a probability and is not directly comparable to embedding cosine score — agents must not filter by reranker score using the same threshold as cosine score
- Jina API rate limits are per-minute; agents processing large batches must implement request pacing or use exponential backoff
- The LangChain `CohereRerank` compressor requires the base retriever to return `Document` objects with `page_content` — agents wiring custom retrievers must adapt the interface

## References
- [Cohere Rerank API Docs](https://docs.cohere.com/docs/reranking)
- [Jina Reranker](https://jina.ai/reranker/)
- [Voyage AI Rerank](https://docs.voyageai.com/docs/reranker)
- [MixedBread AI Reranking](https://www.mixedbread.ai/docs/reranking)
- [MS MARCO Cross-Encoders (SBERT)](https://www.sbert.net/docs/pretrained-models/ce-msmarco.html)
- [ColBERT: Efficient Multi-Vector Retrieval](https://arxiv.org/abs/2004.12832)
