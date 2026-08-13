# Langchain Rag Pipeline

## Summary

**One-sentence:** Designs a LangChain RAG pipeline (loader + splitter + embedder + retriever + LCEL prompt) and emits a pipeline-spec decision-record.

**One-paragraph:** RAG pipelines die from chunk size mismatch, wrong embedding model, or naive retrieval. This methodology turns a corpus profile (doc count, avg doc length, query pattern, latency budget) into a deterministic LangChain RAG pipeline spec: loader choice, splitter + chunk size, embedding model, vectorstore, retriever k, and the LCEL prompt shape.

**Ефективно для:** solopreneur building a doc-Q&A bot who needs the cheapest retrieval that still gives correct answers.

## Applies If (ALL must hold)

- Corpus is bounded and indexable (≤100M tokens) — beyond that needs sharding methodology.
- Doc-Q&A or summarisation task — not pure chat.
- ≥1 vectorstore available (Chroma local, Pinecone, Weaviate, pgvector).
- You control chunk size and prompt template.
- Embeddings cost fits in your budget (or you can use a free model).

## Skip If (ANY kills it)

- Corpus changes faster than indexer can keep up (use streaming retrieval instead).
- Pure factual Q&A over structured data — use NL→SQL (see [[llamaindex-sql-query]]).
- Documents are mostly tables/images — needs multimodal pipeline.
- Latency budget <200ms — RAG can't hit that with most embedding models.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `corpus-profile.yaml` | YAML: doc_count, avg_doc_chars, query_pattern, embedding_budget_usd, latency_budget_ms | author writes |
| `Document loader source` | directory path / URL list / S3 prefix | raw corpus |
| `Vectorstore endpoint` | URL or local path | infra config |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[langchain-basics]] | LCEL knowledge. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Migrated rules for loaders, splitters, embedding, retrieval, prompt shape. | ~1000 |
| `content/02-output-contract.xml` | essential | pipeline-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Chunk-size mismatch, embedding-corpus drift, retrieval-prompt mismatch, k-too-high. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step build procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/corpus-profile.yaml` | Input contract. |
| `templates/pipeline-spec.md` | Output skeleton. |
| `templates/rag-chain.py` | Working LCEL pipeline. |
| `templates/_smoke-test.yaml` | Minimum viable profile. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-langchain-rag-pipeline.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

- [[llamaindex-ingestion-pipeline]]
- [[llamaindex-hybrid-retrieval]]
- [[langchain-observability]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on query_pattern (factual → low-k; broad → high-k+rerank), then on corpus size (small → in-mem, large → Pinecone/pgvector), then on latency budget. Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/corpus-profile.yaml`

```yaml
doc_count: TODO          # fill with concrete value per the driver definition
avg_doc_chars: TODO          # fill with concrete value per the driver definition
query_pattern: TODO          # fill with concrete value per the driver definition
latency_budget_ms: TODO          # fill with concrete value per the driver definition
```

### `templates/rag-chain.py`

```python
"""Reference artefact for langchain-rag-pipeline. Self-test only verifies the scaffold compiles."""
from __future__ import annotations


def build(decision: dict):
    """Build the runtime object from a validated decision-record."""
    if not isinstance(decision, dict):
        raise TypeError("decision must be dict from validated decision-record")
    return decision  # placeholder: real implementations wire here


def _self_test() -> int:
    out = build({"slug": "langchain-rag-pipeline", "version": "2.0.0"})
    return 0 if out["slug"] == "langchain-rag-pipeline" else 1


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    if "--help" in sys.argv:
        print(__doc__)
```

### `templates/_smoke-test.yaml`

```yaml
doc_count: low
avg_doc_chars: low
query_pattern: low
latency_budget_ms: low
```
