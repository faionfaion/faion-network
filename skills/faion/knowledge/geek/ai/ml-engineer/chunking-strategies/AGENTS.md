---
slug: chunking-strategies
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Document chunking decision rubric: fixed-size, recursive-character, semantic, structure-aware (markdown/HTML/code). Output is a chunking config + dispatcher.
content_id: "e8418304d2b24197"
complexity: medium
produces: config
est_tokens: 4200
tags: [chunking, rag, embeddings, retrieval, ingestion]
---
# Chunking Strategies

## Summary

**One-sentence:** Document chunking decision rubric: fixed-size, recursive-character, semantic, structure-aware (markdown/HTML/code). Output is a chunking config + dispatcher.

**One-paragraph:** Splits documents into retrieval-friendly chunks. Five strategies (fixed-size, recursive-character, semantic-similarity, structure-aware, hybrid) each fit different document types. Methodology output: a `chunking-config.yaml` per corpus + a dispatcher that picks the right strategy per document type. Includes evaluation rubric (chunk-faithfulness, retrieval-recall at top-k).

**Ефективно для:** RAG-інженер, який ставить «fixed-size 1000 chars» скрізь і бачить, що retrieval-recall топчеться на ~70%.

## Applies If (ALL must hold)

- RAG pipeline is in scope
- corpus has > 1 document type (markdown + code + HTML)
- retrieval-recall is the bottleneck
- you have an eval suite with retrieval ground truth
- vector store is configured

## Skip If (ANY kills it)

- single-document type with stable structure — pick once, move on
- corpus is tiny (< 100 docs) — chunking is not the bottleneck
- no eval suite — build the eval first, then optimise chunking
- downstream is full-document QA (no chunking needed)

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=config + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=config`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-chunking-strategies.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/chunker-dispatcher.py` | Per-type dispatcher skeleton |
| `templates/chunking-config.yaml` | YAML config with per-type chunker + parameters |
| `templates/markdown-chunker.py` | Markdown heading-aware chunker |
| `templates/code-chunker.py` | AST-based code chunker |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chunking-strategies.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-eval-driven`, `r2-structure-aware-when-possible`, `r3-overlap-bounded`, `r4-per-type-dispatcher`, `r5-chunk-size-by-model` from `content/01-core-rules.xml`.
