---
slug: rag-eval-test-set-generation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Generates a labeled RAG test set with question / ground-truth chunk-ids / expected answer, balanced across query types.
content_id: "afdc67235845f4d9"
complexity: medium
produces: report
est_tokens: 3200
tags: [rag, evaluation, test-set, question-generation]
---
# RAG Test Set Generation

## Summary

**One-sentence:** Generates a labeled RAG test set with question / ground-truth chunk-ids / expected answer, balanced across query types.

**One-paragraph:** A RAG evaluation can only be as good as its test set. This methodology produces a labeled JSONL of (query, relevant_chunk_ids, expected_answer) tuples, balanced across query types (factoid, multi-hop, summarisation, comparison), sourced from real user queries plus LLM-synthesised hard cases, and with human spot-check of at least 20% of entries.

**Ефективно для:** інженерів, які не мають labeled eval set і хочуть зібрати чесний baseline до launch.

## Applies If (ALL must hold)

- Building a new RAG system without an existing labeled eval set.
- Expanding an existing set to cover new query types.
- Generating hard cases (multi-hop, negation, ambiguity) the system fails on.

## Skip If (ANY kills it)

- An existing labeled set already covers all query types and is recent (< 90 days).
- Domain is too sensitive to expose to an LLM generator (PHI / classified).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Corpus chunks with stable ids | Qdrant/store | rag-implementation |
| Sample of real user queries | JSONL | production logs |
| LLM for synthesis | credentials | infra |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-eval-strategy` | Strategy defines test set size targets. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~700 |
| `content/06-decision-tree.xml` | essential | Decision tree with rule-id refs | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Sample real queries from logs | haiku | Mechanical sampling. |
| Synthesise hard cases | sonnet | Quality matters. |
| Human spot-check workflow | sonnet | Triage + corrections. |

## Templates

| File | Purpose |
|------|---------|
| `templates/synth-prompt.txt` | Prompt template for LLM hard-case synthesis. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-eval-test-set-generation.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[rag-eval-pipeline]]
- [[rag-eval-strategy]]
- [[rag-eval-generation-metrics]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides reuse / extend / regenerate based on existing test-set state. Each leaf references a rule id from `01-core-rules.xml`.
