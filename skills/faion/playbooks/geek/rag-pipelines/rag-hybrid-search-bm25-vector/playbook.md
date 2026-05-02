---
name: rag-hybrid-search-bm25-vector
description: Build hybrid retrieval combining BM25 keyword search with dense vector search, fused via Reciprocal Rank Fusion and rewritten queries from Claude.
tier: geek
group: rag-pipelines
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working hybrid retrieval pipeline that scores chunks using both BM25 keyword relevance (via Postgres `tsvector`) and cosine similarity (via Qdrant dense vectors), merges the ranked lists with Reciprocal Rank Fusion (RRF), rewrites user queries with `claude-sonnet-4-6`, and returns chunks annotated with both scores.

## Prerequisites

- Python 3.11+ with `anthropic>=0.40`, `qdrant-client>=1.9`, `psycopg[binary]>=3.1`, `sentence-transformers>=3.0` installed.
- A running Postgres 15+ instance with `pg_trgm` extension (for fallback fuzzy matching) and a documents table.
- A running Qdrant instance (local Docker or Qdrant Cloud cluster URL + API key).
- An `ANTHROPIC_API_KEY` environment variable set.
- Qdrant collection already created with the correct vector dimension (768 for `all-mpnet-base-v2`). See `rag-vector-store-qdrant` for bootstrapping.
- Documents already ingested: text stored in Postgres, embeddings stored in Qdrant with matching `doc_id` payload.

## Steps

1. **Install dependencies** into your project virtual environment:

   ```bash
   pip install "anthropic>=0.40" "qdrant-client>=1.9" "psycopg[binary]>=3.1" \
       "sentence-transformers>=3.0" "pydantic>=2.7"
   ```

2. **Set environment variables** before running:

   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   export QDRANT_URL="http://localhost:6333"          # or Qdrant Cloud URL
   export QDRANT_API_KEY=""                            # leave empty for local
   export DATABASE_URL="postgresql://user:pass@localhost:5432/myrag"
   export QDRANT_COLLECTION="documents"
   ```

3. **Create the hybrid retriever module** at `src/retrieval/hybrid.py`:

   ```python
   """Hybrid BM25 + vector retrieval with Reciprocal Rank Fusion."""
   from __future__ import annotations

   import os
   from dataclasses import dataclass, field
   from typing import Any

   import anthropic
   import psycopg
   from pydantic import BaseModel
   from qdrant_client import QdrantClient
   from qdrant_client.models import Filter, FieldCondition, MatchValue
   from sentence_transformers import SentenceTransformer


   # ---------------------------------------------------------------------------
   # Data models
   # ---------------------------------------------------------------------------

   class RetrievedChunk(BaseModel):
       doc_id: str
       text: str
       bm25_rank: int | None = None
       vector_rank: int | None = None
       bm25_score: float | None = None
       cosine_score: float | None = None
       rrf_score: float


   # ---------------------------------------------------------------------------
   # Query rewriting via Claude
   # ---------------------------------------------------------------------------

   _claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


   def rewrite_query(raw_query: str) -> str:
       """Expand and clarify query for better BM25 + vector coverage."""
       response = _claude.messages.create(
           model="claude-sonnet-4-6",
           max_tokens=256,
           system=(
               "You are a search query optimizer. "
               "Rewrite the user query into a clearer, more precise version "
               "that will improve both keyword and semantic retrieval. "
               "Output only the rewritten query — no explanations."
           ),
           messages=[{"role": "user", "content": raw_query}],
       )
       return response.content[0].text.strip()


   # ---------------------------------------------------------------------------
   # BM25 via Postgres tsvector
   # ---------------------------------------------------------------------------

   def bm25_search(
       query: str,
       conn: psycopg.Connection,
       table: str = "documents",
       top_k: int = 20,
   ) -> list[dict[str, Any]]:
       """Return top_k rows ranked by ts_rank_cd (BM25 approximation)."""
       sql = f"""
           SELECT
               doc_id,
               content AS text,
               ts_rank_cd(search_vector, plainto_tsquery('english', %(q)s)) AS bm25_score
           FROM {table}
           WHERE search_vector @@ plainto_tsquery('english', %(q)s)
           ORDER BY bm25_score DESC
           LIMIT %(k)s
       """
       rows = conn.execute(sql, {"q": query, "k": top_k}).fetchall()
       return [
           {"doc_id": str(r[0]), "text": r[1], "bm25_score": float(r[2])}
           for r in rows
       ]


   # ---------------------------------------------------------------------------
   # Dense vector search via Qdrant
   # ---------------------------------------------------------------------------

   _encoder = SentenceTransformer("all-mpnet-base-v2")


   def vector_search(
       query: str,
       qdrant: QdrantClient,
       collection: str,
       top_k: int = 20,
       filter_: Filter | None = None,
   ) -> list[dict[str, Any]]:
       """Return top_k chunks by cosine similarity from Qdrant."""
       embedding = _encoder.encode(query, normalize_embeddings=True).tolist()
       hits = qdrant.search(
           collection_name=collection,
           query_vector=embedding,
           limit=top_k,
           query_filter=filter_,
           with_payload=True,
       )
       return [
           {
               "doc_id": str(hit.payload["doc_id"]),
               "text": hit.payload["text"],
               "cosine_score": float(hit.score),
           }
           for hit in hits
       ]


   # ---------------------------------------------------------------------------
   # Reciprocal Rank Fusion
   # ---------------------------------------------------------------------------

   def reciprocal_rank_fusion(
       bm25_results: list[dict],
       vector_results: list[dict],
       k: int = 60,
       top_n: int = 10,
   ) -> list[RetrievedChunk]:
       """
       Merge two ranked lists using RRF: score = 1/(k + rank).

       k=60 is the standard constant from Cormack et al. (2009).
       """
       scores: dict[str, dict] = {}

       for rank, item in enumerate(bm25_results, start=1):
           did = item["doc_id"]
           if did not in scores:
               scores[did] = {"text": item["text"], "rrf": 0.0}
           scores[did]["bm25_rank"] = rank
           scores[did]["bm25_score"] = item["bm25_score"]
           scores[did]["rrf"] += 1.0 / (k + rank)

       for rank, item in enumerate(vector_results, start=1):
           did = item["doc_id"]
           if did not in scores:
               scores[did] = {"text": item["text"], "rrf": 0.0}
           scores[did]["vector_rank"] = rank
           scores[did]["cosine_score"] = item["cosine_score"]
           scores[did]["rrf"] += 1.0 / (k + rank)

       ranked = sorted(scores.items(), key=lambda x: x[1]["rrf"], reverse=True)
       return [
           RetrievedChunk(
               doc_id=did,
               text=data["text"],
               bm25_rank=data.get("bm25_rank"),
               vector_rank=data.get("vector_rank"),
               bm25_score=data.get("bm25_score"),
               cosine_score=data.get("cosine_score"),
               rrf_score=data["rrf"],
           )
           for did, data in ranked[:top_n]
       ]


   # ---------------------------------------------------------------------------
   # Public API
   # ---------------------------------------------------------------------------

   @dataclass
   class HybridRetriever:
       db_url: str = field(default_factory=lambda: os.environ["DATABASE_URL"])
       qdrant_url: str = field(default_factory=lambda: os.environ["QDRANT_URL"])
       qdrant_api_key: str = field(default_factory=lambda: os.environ.get("QDRANT_API_KEY", ""))
       collection: str = field(default_factory=lambda: os.environ["QDRANT_COLLECTION"])
       bm25_top_k: int = 20
       vector_top_k: int = 20
       rrf_k: int = 60
       final_top_n: int = 10
       rewrite: bool = True

       def retrieve(self, query: str) -> list[RetrievedChunk]:
           effective_query = rewrite_query(query) if self.rewrite else query

           qdrant = QdrantClient(
               url=self.qdrant_url,
               api_key=self.qdrant_api_key or None,
           )

           with psycopg.connect(self.db_url) as conn:
               bm25 = bm25_search(effective_query, conn, top_k=self.bm25_top_k)

           vec = vector_search(
               effective_query, qdrant, self.collection, top_k=self.vector_top_k
           )

           return reciprocal_rank_fusion(bm25, vec, k=self.rrf_k, top_n=self.final_top_n)
   ```

4. **Ensure the Postgres table has a `tsvector` column** and a GIN index. Run once during schema migration:

   ```sql
   ALTER TABLE documents
       ADD COLUMN IF NOT EXISTS search_vector tsvector
       GENERATED ALWAYS AS (to_tsvector('english', content)) STORED;

   CREATE INDEX IF NOT EXISTS idx_documents_fts
       ON documents USING gin(search_vector);
   ```

5. **Write a quick smoke test** at `tests/test_hybrid.py` to validate the pipeline end-to-end with real data:

   ```python
   import os
   import pytest
   from src.retrieval.hybrid import HybridRetriever

   @pytest.mark.integration
   def test_hybrid_retrieval_returns_scored_chunks():
       retriever = HybridRetriever(rewrite=True)
       results = retriever.retrieve("transformer attention mechanism")

       assert len(results) >= 1
       for chunk in results:
           assert chunk.rrf_score > 0
           # At least one score source must be present per chunk
           assert chunk.bm25_score is not None or chunk.cosine_score is not None

   @pytest.mark.integration
   def test_rrf_scores_are_descending():
       retriever = HybridRetriever(rewrite=False)
       results = retriever.retrieve("BERT pre-training objectives")
       scores = [r.rrf_score for r in results]
       assert scores == sorted(scores, reverse=True)
   ```

6. **Run the integration tests** (requires both Postgres and Qdrant running):

   ```bash
   pytest tests/test_hybrid.py -v -m integration
   ```

7. **Inspect result scores** in a REPL or script to confirm dual-score annotation:

   ```python
   from src.retrieval.hybrid import HybridRetriever

   retriever = HybridRetriever(final_top_n=5)
   chunks = retriever.retrieve("What is masked language modeling?")

   for i, c in enumerate(chunks, 1):
       print(
           f"{i}. [RRF={c.rrf_score:.4f}] "
           f"[BM25={c.bm25_score:.4f} rank={c.bm25_rank}] "
           f"[cos={c.cosine_score:.4f} rank={c.vector_rank}]"
       )
       print(f"   {c.text[:120]}...")
   ```

## Verify

Run the following and confirm all assertions pass:

```bash
python - <<'EOF'
from src.retrieval.hybrid import HybridRetriever, reciprocal_rank_fusion

# Unit-test RRF without network calls
bm25 = [{"doc_id": "d1", "text": "alpha", "bm25_score": 0.9},
        {"doc_id": "d2", "text": "beta",  "bm25_score": 0.5}]
vec  = [{"doc_id": "d2", "text": "beta",  "cosine_score": 0.95},
        {"doc_id": "d3", "text": "gamma", "cosine_score": 0.7}]

results = reciprocal_rank_fusion(bm25, vec, top_n=3)
assert results[0].doc_id == "d2", "d2 should win — appears in both lists"
assert results[0].bm25_rank == 2
assert results[0].vector_rank == 1
assert results[0].cosine_score == 0.95
assert results[0].bm25_score == 0.5
print("All RRF unit assertions passed")
EOF
```

Expected output: `All RRF unit assertions passed`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `psycopg.errors.UndefinedColumn: column search_vector does not exist` | Migration not run | Execute the `ALTER TABLE` + `CREATE INDEX` SQL in Step 4 |
| BM25 returns 0 rows for every query | `search_vector` column populated but GIN index missing | Run `REINDEX INDEX idx_documents_fts` then retry |
| `qdrant_client.http.exceptions.UnexpectedResponse: 404` on search | Collection name mismatch | Check `QDRANT_COLLECTION` env var matches the name used during ingestion |
| `sentence_transformers` downloads model on every startup | Model not cached | Set `SENTENCE_TRANSFORMERS_HOME=/data/models` and pre-download once with `_encoder = SentenceTransformer("all-mpnet-base-v2")` |
| RRF results always dominated by vector scores | BM25 returns very few hits (sparse keyword overlap) | Lower `bm25_top_k`, add synonyms via `ts_lexize`, or switch to OpenSearch with BM25+ tuning |
| `anthropic.APIStatusError: 529` during query rewrite | Claude API overload | Wrap `rewrite_query` in exponential backoff; fall back to raw query if retries exceed 3 |
| Cosine scores all near 0.99 (no discrimination) | Embeddings not normalized before insert | Re-ingest with `normalize_embeddings=True` in `SentenceTransformer.encode` |

## Next

- Add a reranking stage after RRF using a cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`) to re-score the top-10 with full query-document pairs — see `reranking-two-stage`.
- Replace Postgres `tsvector` with OpenSearch BM25+ (with `k1=1.6, b=0.75` tuning) for larger corpora where Postgres FTS becomes a bottleneck.
- Evaluate retrieval quality with NDCG@10 and MRR per query using a golden test set — see `rag-eval-retrieval-metrics`.

## References

- [knowledge/geek/ai/rag-engineer/hybrid-search-implementation](../../../knowledge/geek/ai/rag-engineer/hybrid-search-implementation) — provides the RRF constant derivation (k=60) and the score-merging algebra that Steps 3 and 5 implement directly.
- [knowledge/geek/ai/rag-engineer/hybrid-search-basics](../../../knowledge/geek/ai/rag-engineer/hybrid-search-basics) — covers BM25 term-frequency model and why keyword recall complements dense retrieval for named-entity and exact-match queries in Step 3.
- [knowledge/geek/ai/rag-engineer/db-qdrant](../../../knowledge/geek/ai/rag-engineer/db-qdrant) — Qdrant collection schema, payload indexing, and `search()` API used in the `vector_search` function in Step 3.
- [knowledge/geek/ai/rag-engineer/reranking-pipeline-integration](../../../knowledge/geek/ai/rag-engineer/reranking-pipeline-integration) — specifies the cross-encoder interface and latency budget needed to extend the RRF output in Step 3 into a two-stage pipeline without breaking sub-100ms SLA.
