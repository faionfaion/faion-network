---
name: rag-reranking
description: Rerank top-30 vector search candidates to top-5 using Cohere Rerank v3 or a local BAAI/bge-reranker-v2-m3 cross-encoder, improving NDCG@5 by 15-25pp.
tier: geek
group: rag-pipelines
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a two-stage RAG retrieval pipeline that fetches 30 candidates from a Qdrant vector store and reranks them to the top 5 using either the Cohere Rerank v3 API (hosted, $1/1k requests, ~150ms) or a local `BAAI/bge-reranker-v2-m3` cross-encoder (free, ~100ms/batch on CPU). You will know when to use each backend and have a production-grade fallback wrapper in place.

## Prerequisites

- Python 3.11+ with a virtual environment.
- `COHERE_API_KEY` set in environment (Cohere path only). Get a key at https://dashboard.cohere.com.
- A running Qdrant instance (local Docker or Qdrant Cloud). Collection already populated with dense embeddings. See `rag-hybrid-search-bm25-vector` for ingestion setup.
- For the local path: at least 4 GB RAM; GPU optional (CPU inference ~100ms/batch of 30).
- Familiarity with first-stage vector retrieval — this playbook covers Stage 2 only.

## Steps

1. **Install dependencies** for your chosen backend (install both if you want runtime switching):

   ```bash
   # Cohere path
   pip install "cohere>=5.5" "qdrant-client>=1.9" "pydantic>=2.7"

   # Local cross-encoder path
   pip install "sentence-transformers>=3.0" "qdrant-client>=1.9" "pydantic>=2.7"
   # BAAI model downloads on first use (~550 MB); pre-download with:
   python -c "from sentence_transformers import CrossEncoder; CrossEncoder('BAAI/bge-reranker-v2-m3')"
   ```

2. **Set environment variables**:

   ```bash
   export COHERE_API_KEY="<your-cohere-api-key>"
   export QDRANT_URL="http://localhost:6333"     # or Qdrant Cloud URL
   export QDRANT_API_KEY=""                       # leave empty for local
   export QDRANT_COLLECTION="knowledge_chunks"
   ```

3. **Create the retriever module** at `src/retrieval/reranking.py`:

   ```python
   """Two-stage RAG retrieval: vector top-30 → rerank to top-5."""
   from __future__ import annotations

   import logging
   import os
   import time
   from dataclasses import dataclass, field
   from typing import Literal

   import numpy as np
   from pydantic import BaseModel
   from qdrant_client import QdrantClient
   from sentence_transformers import SentenceTransformer

   logger = logging.getLogger(__name__)

   EMBED_MODEL = "all-mpnet-base-v2"   # 768-dim; swap to match your collection
   _encoder: SentenceTransformer | None = None


   def _get_encoder() -> SentenceTransformer:
       global _encoder
       if _encoder is None:
           _encoder = SentenceTransformer(EMBED_MODEL)
       return _encoder


   # ---------------------------------------------------------------------------
   # Data model
   # ---------------------------------------------------------------------------

   class RankedChunk(BaseModel):
       doc_id: str
       text: str
       vector_rank: int          # original rank from first-stage ANN
       rerank_score: float
       rerank_rank: int          # rank after reranking (1 = best)


   # ---------------------------------------------------------------------------
   # Stage 1: vector retrieval (top-30 candidates)
   # ---------------------------------------------------------------------------

   def vector_retrieve(
       query: str,
       qdrant: QdrantClient,
       collection: str,
       top_k: int = 30,
   ) -> list[dict]:
       """Return top_k chunks by cosine similarity from Qdrant."""
       embedding = _get_encoder().encode(query, normalize_embeddings=True).tolist()
       hits = qdrant.search(
           collection_name=collection,
           query_vector=embedding,
           limit=top_k,
           with_payload=True,
       )
       return [
           {
               "doc_id": str(hit.payload["doc_id"]),
               "text": hit.payload["text"],
               "cosine_score": float(hit.score),
               "vector_rank": rank,
           }
           for rank, hit in enumerate(hits, start=1)
       ]


   # ---------------------------------------------------------------------------
   # Stage 2a: Cohere Rerank v3 (hosted)
   # ---------------------------------------------------------------------------

   def cohere_rerank(
       query: str,
       candidates: list[dict],
       top_k: int = 5,
       model: str = "rerank-english-v3.0",
   ) -> list[RankedChunk]:
       """
       Rerank candidates using Cohere Rerank v3.

       Pricing: $1 per 1 000 requests (each request = one rerank call).
       Latency: ~150 ms p50 for 30 candidates.
       Limit: up to 1 000 documents per request, 10 K total chars — Stage 1
       cap of 30 well-sized chunks stays safely within both limits.
       """
       import cohere

       co = cohere.Client(api_key=os.environ["COHERE_API_KEY"])
       texts = [c["text"] for c in candidates]

       t0 = time.perf_counter()
       response = co.rerank(
           query=query,
           documents=texts,
           top_n=top_k,
           model=model,
       )
       elapsed = time.perf_counter() - t0
       logger.info("cohere_rerank: %d → %d in %.3fs", len(candidates), top_k, elapsed)

       # response.results is sorted by relevance_score descending;
       # use r.index to map back to the original candidate, not list position.
       return [
           RankedChunk(
               doc_id=candidates[r.index]["doc_id"],
               text=candidates[r.index]["text"],
               vector_rank=candidates[r.index]["vector_rank"],
               rerank_score=float(r.relevance_score),
               rerank_rank=rank,
           )
           for rank, r in enumerate(response.results, start=1)
       ]


   # ---------------------------------------------------------------------------
   # Stage 2b: Local BAAI/bge-reranker-v2-m3 cross-encoder (free)
   # ---------------------------------------------------------------------------

   _cross_encoder = None


   def _get_cross_encoder():
       global _cross_encoder
       if _cross_encoder is None:
           from sentence_transformers import CrossEncoder
           _cross_encoder = CrossEncoder("BAAI/bge-reranker-v2-m3")
       return _cross_encoder


   def local_rerank(
       query: str,
       candidates: list[dict],
       top_k: int = 5,
   ) -> list[RankedChunk]:
       """
       Rerank candidates using BAAI/bge-reranker-v2-m3 locally.

       Cost: free (open-weight model, Apache 2.0).
       Latency: ~100 ms for 30 candidates on CPU (batch_size=32).
       Quality: competitive with Cohere v3 on BEIR; multilingual-capable.
       Memory: ~550 MB model download; ~1.2 GB peak RAM during inference.
       """
       model = _get_cross_encoder()
       pairs = [[query, c["text"]] for c in candidates]

       t0 = time.perf_counter()
       scores = model.predict(pairs, batch_size=32)
       elapsed = time.perf_counter() - t0
       logger.info("local_rerank: %d → %d in %.3fs", len(candidates), top_k, elapsed)

       top_idx = np.argsort(scores)[::-1][:top_k]
       return [
           RankedChunk(
               doc_id=candidates[i]["doc_id"],
               text=candidates[i]["text"],
               vector_rank=candidates[i]["vector_rank"],
               rerank_score=float(scores[i]),
               rerank_rank=rank,
           )
           for rank, i in enumerate(top_idx, start=1)
       ]


   # ---------------------------------------------------------------------------
   # Production wrapper: fallback to initial retrieval order on failure
   # ---------------------------------------------------------------------------

   def rerank_with_fallback(
       query: str,
       candidates: list[dict],
       backend: Literal["cohere", "local"] = "local",
       top_k: int = 5,
   ) -> list[RankedChunk]:
       """
       Rerank with graceful fallback to initial retrieval order on any error.

       The reranker is an accuracy improvement, not a correctness requirement.
       Falling back to the original ANN order preserves user-facing results
       when the reranker is unavailable or exceeds its timeout.
       """
       try:
           if backend == "cohere":
               return cohere_rerank(query, candidates, top_k)
           return local_rerank(query, candidates, top_k)
       except Exception as exc:
           logger.error("rerank_with_fallback: %s failed (%s), using ANN order", backend, exc)
           return [
               RankedChunk(
                   doc_id=c["doc_id"],
                   text=c["text"],
                   vector_rank=c["vector_rank"],
                   rerank_score=1.0 - (c["vector_rank"] - 1) / len(candidates),
                   rerank_rank=c["vector_rank"],
               )
               for c in candidates[:top_k]
           ]


   # ---------------------------------------------------------------------------
   # Public pipeline: retrieve top-30 → rerank to top-5
   # ---------------------------------------------------------------------------

   @dataclass
   class RerankingRetriever:
       qdrant_url: str = field(default_factory=lambda: os.environ["QDRANT_URL"])
       qdrant_api_key: str = field(default_factory=lambda: os.environ.get("QDRANT_API_KEY", ""))
       collection: str = field(default_factory=lambda: os.environ["QDRANT_COLLECTION"])
       first_stage_k: int = 30
       final_k: int = 5
       backend: Literal["cohere", "local"] = "local"

       def retrieve(self, query: str) -> list[RankedChunk]:
           qdrant = QdrantClient(
               url=self.qdrant_url,
               api_key=self.qdrant_api_key or None,
           )
           candidates = vector_retrieve(query, qdrant, self.collection, self.first_stage_k)
           return rerank_with_fallback(query, candidates, self.backend, self.final_k)
   ```

4. **Decide which backend to use** based on your constraints:

   | Criterion | Choose Cohere | Choose local (`BAAI/bge-reranker-v2-m3`) |
   |-----------|---------------|------------------------------------------|
   | Cost at scale | $1/1k requests → track monthly spend | Free |
   | Latency (30 candidates) | ~150 ms p50 | ~100 ms CPU, ~20 ms GPU |
   | Infra dependency | External API (uptime SLA 99.9%) | None (model on disk) |
   | Multilingual corpus | Use `rerank-multilingual-v3.0` | Model is multilingual natively |
   | Cold-start penalty | None | ~2 s first load; zero after warm-up |
   | NDCG@5 improvement | +15–25 pp over ANN-only | +12–22 pp over ANN-only |

   Switch the backend at runtime by passing `backend="cohere"` or `backend="local"` to `RerankingRetriever`.

5. **Wire the retriever into your RAG generation loop** at `src/rag_pipeline.py`:

   ```python
   import anthropic
   from src.retrieval.reranking import RerankingRetriever

   _client = anthropic.Anthropic()
   _retriever = RerankingRetriever(backend="local")  # swap to "cohere" for prod


   def answer(question: str) -> str:
       chunks = _retriever.retrieve(question)
       context = "\n\n".join(
           f"[{c.rerank_rank}] {c.text}" for c in chunks
       )
       response = _client.messages.create(
           model="claude-sonnet-4-6",
           max_tokens=1024,
           system=(
               "You are a knowledgeable assistant. "
               "Answer the question using only the provided context. "
               "If the context does not contain the answer, say so."
           ),
           messages=[
               {
                   "role": "user",
                   "content": f"Context:\n{context}\n\nQuestion: {question}",
               }
           ],
       )
       return response.content[0].text
   ```

6. **Run a smoke test** to confirm the pipeline returns 5 ranked chunks without errors:

   ```python
   from src.retrieval.reranking import RerankingRetriever

   r = RerankingRetriever(backend="local")
   results = r.retrieve("What is the attention mechanism in transformers?")
   assert len(results) == 5
   for chunk in results:
       assert chunk.rerank_rank >= 1
       assert chunk.vector_rank >= 1
       print(f"rank={chunk.rerank_rank} (was #{chunk.vector_rank}) score={chunk.rerank_score:.4f}")
   ```

## Verify

Run the following unit check against the module without a live Qdrant connection:

```python
import numpy as np
from src.retrieval.reranking import local_rerank, RankedChunk

candidates = [
    {"doc_id": "d1", "text": "BERT uses bidirectional self-attention pre-training.", "vector_rank": 1, "cosine_score": 0.91},
    {"doc_id": "d2", "text": "Attention scores are computed as softmax(QK^T/sqrt(d_k))V.", "vector_rank": 2, "cosine_score": 0.88},
    {"doc_id": "d3", "text": "The capital of France is Paris.", "vector_rank": 3, "cosine_score": 0.85},
]

results = local_rerank("How does transformer attention work?", candidates, top_k=2)

assert len(results) == 2, f"Expected 2, got {len(results)}"
assert results[0].rerank_rank == 1
# The unrelated Paris chunk should drop out of the top-2
assert all(c.doc_id != "d3" for c in results), "Off-topic chunk should not be top-2"
print("Reranking smoke test passed:", [(c.doc_id, round(c.rerank_score, 3)) for c in results])
```

Expected output: `Reranking smoke test passed: [('d2', ...), ('d1', ...)]` (order may vary; Paris chunk absent).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `cohere.errors.CohereAPIError: 400` | Document list exceeds 1 000 items or 10 K total chars | Cap first-stage retrieval at `first_stage_k=30`; truncate each chunk to 512 chars before calling Cohere |
| Cohere results mapped to wrong documents | Using list position instead of `r.index` to look up candidates | Always index back via `candidates[r.index]`, not by loop position — Cohere returns results in score order |
| Local model takes > 5 s for 30 candidates | CPU inference with large batch or tokenization overhead | Set `batch_size=32` in `model.predict()`; warm the model at startup (call `_get_cross_encoder()` once before serving) |
| `BAAI/bge-reranker-v2-m3` download fails at runtime | No internet access in production container | Pre-download and bake the model into the Docker image: `python -c "from sentence_transformers import CrossEncoder; CrossEncoder('BAAI/bge-reranker-v2-m3')"` |
| Reranker promotes irrelevant chunks to top-1 | First-stage candidate pool too narrow — relevant doc not in top-30 | Increase `first_stage_k` to 50; reranking cannot surface documents absent from the candidate pool |
| NDCG@5 improvement < 5 pp in offline eval | Embedding model already well-calibrated for the domain | Profile rank deltas per query; if original ANN rank ≤ 3 for most answers, reranking overhead may not be worth the cost |
| `signal.SIGALRM` not available on Windows | Unix-only signal | Replace the timeout with `concurrent.futures.ThreadPoolExecutor` + `future.result(timeout=2.0)` |

## Next

- Add NDCG@5 / MRR evaluation on a golden test set to measure the actual improvement for your corpus — see `rag-eval-retrieval-metrics` methodology under `knowledge/geek/ai/rag-engineer/`.
- Chain with hybrid BM25 + vector retrieval to further improve Stage 1 recall before reranking — see `rag-hybrid-search-bm25-vector`.
- Introduce result-diversity reranking with MMR after precision reranking to avoid redundant top-5 chunks — see `reranking-diversity-mmr` in the same knowledge skill.

## References

- [knowledge/geek/ai/rag-engineer/reranking-models](../../../knowledge/geek/ai/rag-engineer/reranking-models) — provides the model selection table (Cohere v3 vs BAAI/bge-reranker-v2-m3 vs ms-marco family), score-scale incompatibility rules, and the RerankerService fallback pattern that Steps 3 and 4 implement.
- [knowledge/geek/ai/rag-engineer/reranking-two-stage](../../../knowledge/geek/ai/rag-engineer/reranking-two-stage) — derives the 3-10x oversampling rule (top-30 candidates for top-5 final) and the cross-encoder joint-scoring architecture that underpins Stage 2 in Step 3.
- [knowledge/geek/ai/rag-engineer/reranking-pipeline-integration](../../../knowledge/geek/ai/rag-engineer/reranking-pipeline-integration) — specifies the production fallback contract (return initial order on failure), the Cohere `r.index` mapping rule, and the `RerankingRAG` interface shape that `RerankingRetriever` follows in Step 3.
