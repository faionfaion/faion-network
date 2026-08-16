# Llamaindex Ingestion Pipeline

## Summary

**One-sentence:** Designs a LlamaIndex IngestionPipeline (loaders + metadata extractors + node parsers + vector store persistence) and emits an ingestion-spec.

**One-paragraph:** Ad-hoc ingestion scripts re-embed on every restart and skip metadata. IngestionPipeline solves this by chaining loaders, metadata extractors (TitleExtractor, SummaryExtractor), node parsers, and a persistent vector store. This methodology converts a corpus profile into a deterministic ingestion-spec.

**Ефективно для:** solopreneur whose ingestion is a notebook one-liner and now needs to scale to thousands of docs without re-embedding.

## Applies If (ALL must hold)

- Using LlamaIndex.
- Corpus updates ≥1× per week.
- Embedding cost matters (≥$10/build).
- ≥1 persistent vector store available.
- Documents need metadata (title/summary/source) for retrieval filtering.

## Skip If (ANY kills it)

- One-off prototype with <100 docs.
- Corpus never changes.
- Custom non-LlamaIndex pipeline.
- Metadata isn't useful for retrieval (rare).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `corpus-profile.yaml` | doc_count, update_frequency, embedding_budget_usd, metadata_needs | author |
| `Vector store endpoint` | Chroma/Pinecone URL | infra |
| `LLM + embedder creds` | secret | config |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[llamaindex-basics]] | Index foundations. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for IngestionPipeline composition, splitter choice, vector-store persistence. | ~1000 |
| `content/02-output-contract.xml` | essential | ingestion-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Re-embed on restart, missing dedup, splitter mismatch. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step pipeline procedure. | ~800 |
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
| `templates/corpus-profile.yaml` | Input. |
| `templates/ingestion-spec.md.j2` | Output. |
| `templates/ingestion-spec.md` | Output. Generated from `templates/ingestion-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pipeline.py` | Working IngestionPipeline. |
| `templates/_smoke-test.yaml` | Minimum. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llamaindex-ingestion-pipeline.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

- [[llamaindex-basics]]
- [[llamaindex-indexes-queries]]
- [[llamaindex-production-gotchas]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on update_frequency (high → docstore dedup required), then on embedding_budget (low → SentenceSplitter; high → SemanticSplitterNodeParser), then on metadata needs. Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/corpus-profile.yaml`

```yaml
doc_count: TODO          # fill with concrete value per the driver definition
update_frequency: TODO          # fill with concrete value per the driver definition
embedding_budget_usd: TODO          # fill with concrete value per the driver definition
```

### `templates/pipeline.py`

```python
"""Reference artefact for llamaindex-ingestion-pipeline. Self-test only verifies the scaffold compiles."""
from __future__ import annotations


def build(decision: dict):
    """Build the runtime object from a validated decision-record."""
    if not isinstance(decision, dict):
        raise TypeError("decision must be dict from validated decision-record")
    return decision  # placeholder: real implementations wire here


def _self_test() -> int:
    out = build({"slug": "llamaindex-ingestion-pipeline", "version": "2.0.0"})
    return 0 if out["slug"] == "llamaindex-ingestion-pipeline" else 1


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
update_frequency: low
embedding_budget_usd: low
```
