# Graph RAG Indexing Pipeline

## Summary

**One-sentence:** Builds the GraphRAG entity-and-relationship graph + community summaries from a document corpus, with deterministic chunking, entity dedup, and resumable batch processing.

**One-paragraph:** Builds the GraphRAG entity-and-relationship graph + community summaries from a document corpus, with deterministic chunking, entity dedup, and resumable batch processing. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Будуєш GraphRAG-індекс над корпусом > 10k документів і потрібен resumable pipeline.
- Перевикористання entity-extraction між запусками — entity dedup + canonicalization.
- Community summaries для multi-hop запитів (Leiden clustering + LLM-summary per cluster).
- Контроль вартості: GPT-4 extract + GPT-3.5 summarize замість усього на топ-моделі.

## Applies If (ALL must hold)

- Корпус > 10k документів з пов'язаними сутностями (people, orgs, products).
- Multi-hop запити вимагають traversal зв'язків, а не лише semantic similarity.
- Бюджет на одноразовий індекс + інкрементальне доповнення.

## Skip If (ANY kills it)

- Plain semantic similarity достатня (single-hop QA).
- Корпус < 1k документів — графовий overhead не окупається.
- Документи без іменованих сутностей (raw logs, metrics).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| document corpus | JSONL or directory of .md/.txt | ingestion source |
| entity schema | YAML list of allowed entity types | domain expert |
| LLM API key | env var | secrets manager |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[chunking-basics]] | deterministic chunking with stable chunk_ids |
| [[embedding-model-selection]] | embedding model locked before indexing |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 7-step procedure (input/action/output/decision-gate) | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule in 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| classify-input | sonnet | Light judgment; identifies branch in decision tree. |
| draft-output | sonnet | Drafting the output artefact per schema. |
| validate-output | haiku | Mechanical schema validation via script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/graphrag_index.py` | Runnable GraphRAG indexing pipeline skeleton |
| `templates/index-manifest.json` | Manifest matching the schema, written at end of indexing |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graph-rag-indexing.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[graph-rag-production]]
- [[graph-rag-retrieval]]
- [[rag-implementation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Does this corpus need traversal beyond single-hop semantic similarity?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/graphrag_index.py`

```python
"""graphrag_index.py — end-to-end GraphRAG indexing pipeline.

Reads a JSONL doc corpus and writes a versioned GraphRAG index
(chunks + entities + graph + communities + summaries).
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Iterator


def chunk_id(doc_id: str, idx: int, content: str) -> str:
    """Deterministic chunk id — survives pipeline reruns."""
    h = hashlib.sha1(
        f"{doc_id}|{idx}|{hashlib.sha1(content.encode()).hexdigest()}".encode()
    ).hexdigest()
    return h[:16]


def iter_chunks(corpus: Path, chunk_size: int = 800) -> Iterator[dict]:
    for line in corpus.open():
        doc = json.loads(line)
        text = doc["text"]
        for i in range(0, len(text), chunk_size):
            seg = text[i:i + chunk_size]
            yield {
                "chunk_id": chunk_id(doc["doc_id"], i, seg),
                "doc_id": doc["doc_id"],
                "text": seg,
            }


def main(corpus_path: str, out_dir: str, version: str) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with (out / f"chunks.{version}.jsonl").open("w") as fh:
        for c in iter_chunks(Path(corpus_path)):
            fh.write(json.dumps(c) + "\n")
    # entity extraction + graph build + community detect + summarize
    # are wired here in the production pipeline.


if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2], sys.argv[3])
```

### `templates/index-manifest.json`

```json
{
  "index_id": "graphrag-portfolio-2026q2",
  "doc_count": 12480,
  "chunk_count": 89321,
  "entity_count": 4210,
  "community_count": 84,
  "extraction_model": "gpt-4o-mini",
  "summary_model": "gpt-4o",
  "checkpoint_path": "/srv/graphrag/checkpoints/portfolio-2026q2.jsonl",
  "version": "v3"
}
```
