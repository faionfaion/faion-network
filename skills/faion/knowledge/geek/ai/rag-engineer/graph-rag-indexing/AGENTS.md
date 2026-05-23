---
slug: graph-rag-indexing
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Builds the GraphRAG entity-and-relationship graph + community summaries from a document corpus, with deterministic chunking, entity dedup, and resumable batch processing.
content_id: "0ba7aad1a1f7dc47"
complexity: deep
produces: code
est_tokens: 4300
tags: [graph-rag, indexing, knowledge-graph, community-detection, llm]
---
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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graph-rag-indexing.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[graph-rag-production]]
- [[graph-rag-retrieval]]
- [[rag-implementation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Does this corpus need traversal beyond single-hop semantic similarity?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
