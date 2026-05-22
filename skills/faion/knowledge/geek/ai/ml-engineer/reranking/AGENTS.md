---
slug: reranking
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "817be12585bc88ee"
summary: Adds a cross-encoder reranker (Cohere Rerank, BGE, FlashRank) as a second stage after first-stage retrieval — retrieve top-N, rerank to top-K — for 20-35% accuracy lift on RAG when latency budget allows ~200ms.
complexity: medium
produces: code
est_tokens: 3500
tags: [reranking, rag, cross-encoder, retrieval, information-retrieval]
---

# Reranking for RAG Systems

## Summary

**One-sentence:** Two-stage retrieval — fast bi-encoder for top-N candidates + slow cross-encoder reranker for top-K — that lifts RAG accuracy 20-35% while adding 100-500ms latency per query.

**One-paragraph:** First-stage retrieval (bi-encoder or hybrid) prioritises recall and speed but compresses query+doc into independent vectors, losing nuanced relevance signals. Cross-encoder rerankers (Cohere Rerank, BGE Reranker, FlashRank, Voyage Rerank) jointly encode query+doc pairs with full attention, recovering precision. The pattern: retrieve top-N (20-100) with vector / hybrid search, rerank to top-K (3-5), pass to synthesis. Choose provider by latency / cost / privacy: Cohere managed, BGE local, FlashRank for batch. Output: a `reranker.yaml` block plugged into the parent rag-pipeline.yaml with provider + top_n + budget guardrail.

**Ефективно для:**

- Legal / medical / enterprise RAG де precision коштує грошей — reranker ловить "майже правильні" доки які перший stage пропускає.
- Hybrid search pipelines — score-fusion (vector + BM25) дає змішані score, cross-encoder нормалізує і ставить релевантний на 1-2.
- Code search — token-level relevance критичний; cross-encoder бачить що patch до function f(), а не до f2().
- Cost-sensitive але quality-критичних use case — local BGE дає 80% якості Cohere без API cost.

## Applies If (ALL must hold)

- RAG pipeline tier ≥ Advanced (rules from `rag-pipeline-design`)
- Latency budget allows ≥150ms per query for reranker call
- Retrieval recall@20 is already ≥80% (reranker improves precision, not recall)
- Queries are diverse enough that cross-encoder reordering matters (eval proves +10% precision lift)

## Skip If (ANY kills it)

- Real-time autocomplete / typeahead — &lt;50ms budget, no room for reranker
- Fewer than 10 candidates retrieved — limited reordering room; gain marginal
- First-stage recall already saturated near 100% on labelled set
- Cost-prohibitive: managed reranker exceeds budget AND no GPU for local model

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `eval-rerank.jsonl` | JSONL `{query, candidate_ids, relevance_labels}` | SME + log analysis |
| `latency-budget.yaml` | YAML | product SLO |
| `rate-cards.yaml` | YAML | Cohere / Voyage / Jina pricing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `rag-pipeline-design` | Parent pipeline this reranker plugs into |
| `vector-databases` | First-stage retrieval comes from here |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: reranker after retrieval, top-N capacity, latency budget, eval gate, fallback on provider down | 1000 |
| `content/02-output-contract.xml` | essential | `reranker.yaml` schema (provider + top_n + budget + fallback) | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: skip reranker, oversize top-N, no eval before adopt, hard-coded provider, no latency budget | 900 |
| `content/04-procedure.xml` | essential | 5 steps: measure recall → pick provider → tune top-N+top-K → wire fallback → eval+ship | 700 |
| `content/05-examples.xml` | essential | Worked example: Qdrant top-20 → Cohere Rerank top-5 with FlashRank fallback | 500 |
| `content/06-decision-tree.xml` | essential | Routes by latency budget + privacy → Cohere / Voyage / BGE / FlashRank | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `provider_selection` | sonnet | Cross-attribute comparison |
| `eval_lift_measurement` | sonnet | Run paired retrieval+rerank evaluation |
| `reranker_yaml_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/rerank-pipeline.py` | Top-N → reranker → top-K skeleton with provider abstraction |
| `templates/reranker.schema.yaml` | Schema for reranker.yaml |
| `templates/_smoke-test.yaml` | Minimum-viable reranker spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reranking.py` | Lint reranker.yaml | Pre-commit |

## Related

- [[rag-pipeline-design]] — parent pipeline
- [[vector-databases]] — first-stage retrieval
- external: [Cohere Rerank](https://docs.cohere.com/docs/rerank-2) · [BGE Reranker](https://github.com/FlagOpen/FlagEmbedding) · [FlashRank](https://github.com/PrithivirajDamodaran/FlashRank)

## Decision tree

See `content/06-decision-tree.xml`. Routes by latency budget + privacy requirement + cost cap to {Cohere Rerank, Voyage Rerank, BGE local, FlashRank batch}.
