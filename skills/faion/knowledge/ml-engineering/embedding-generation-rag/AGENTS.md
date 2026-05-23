# Embedding Generation

## Summary

**One-sentence:** Generates embedding pipeline — same-model index/query, batched calls (OpenAI ≤2048), SHA-256 cache keys, unit normalization, empty/overlong guards, provider-specific tuning.

**One-paragraph:** Wrong embedding generation produces silent recall regressions. This methodology produces an `EmbeddingService` that pins model+version, batches with provider-correct caps, normalizes to unit length for cosine, caches by SHA-256(model+version+text), rejects empty/overlong texts, and applies provider-specific tuning (Cohere input_type, OpenAI dimensions, single-process SentenceTransformer). Output is a code class consumed by the broader embedding-applications pipeline.

**Ефективно для:**

- New RAG project — embed indexing step.
- Replace per-text loop with batched calls (10–50x speedup).
- Add SHA-256 cache to recurring ingest.
- Migrate Ollama loop → SentenceTransformer for local.
- Cohere input_type compliance (5–10% quality boost).

## Applies If (ALL must hold)

- Embedding new corpus OR rewriting existing pipeline.
- Same embedder used for both indexing AND querying.
- Vector DB available.
- Named owner.

## Skip If (ANY kills it)

- Pure keyword search (no embeddings needed).
- &lt;10-token average texts (BM25 outperforms).
- Low-resource language без multilingual model.
- Existing pipeline validated &lt;90 days.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Embedding model name + version | YAML | service repo |
| Provider client | client | platform |
| Tokenizer (for guard checks) | tokenizer | platform |
| Cache backend (optional) | client | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-models]]` | Provider-specific quirks. |
| `[[embedding-caching]]` | Cache layer. |
| `[[embedding-applications]]` | Parent pipeline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules + run/skip terminals | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for embedder-config | ~700 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 5-step: pin model → wire batch → cache → normalize → guards | ~700 |
| `content/06-decision-tree.xml` | essential | Routes provider + corpus to embedder config | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pin-model-version` | haiku | Config write. |
| `tune-provider-params` | sonnet | Per-provider judgment. |
| `audit-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/embedding_service.py` | EmbeddingService class with batching + cache + guards. |
| `templates/embedder-config.json` | Config skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-generation.py` | Validate embedder-config | Pre-commit + CI |

## Related

- [[embedding-models]]
- [[embedding-caching]]
- [[embedding-cost-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by provider + corpus class to embedder config. Walk before wiring.
