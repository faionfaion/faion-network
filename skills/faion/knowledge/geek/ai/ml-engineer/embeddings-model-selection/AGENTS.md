---
slug: embeddings-model-selection
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Pick an embedding model by matching (use case, constraints, capabilities). Output is a decision record with chosen model + rejected alternatives.
content_id: "24a45ffa70b231d6"
complexity: medium
produces: decision-record
est_tokens: 4200
tags: [embeddings, model-selection, rag, semantic-search, vector]
---
# Embeddings Model Selection

## Summary

**One-sentence:** Pick an embedding model by matching (use case, constraints, capabilities). Output is a decision record with chosen model + rejected alternatives.

**One-paragraph:** Embedding model choice drives RAG retrieval quality, latency, and cost more than any other knob. This methodology produces a decision record naming the chosen model + the 3 axes that drove the choice (use case: RAG/search/clustering/classification; constraints: budget/latency/privacy/language; capabilities: Matryoshka dimensions, quantization, asymmetric input types) + ≥2 rejected alternatives.

**Ефективно для:** ML eng, що зараз обирають між OpenAI text-embedding-3-large vs Voyage vs BGE-M3 і хочуть закрити вибір з артефактом, а не з мемом.

## Applies If (ALL must hold)

- you are starting or migrating an embedding-driven system
- use case is one of (RAG, semantic search, clustering, classification)
- you have eval data (queries + ground-truth relevant docs) or can build it in a week
- monthly query volume + latency target are known
- data privacy posture is documented

## Skip If (ANY kills it)

- you already have a working model with > 90% recall@5 — don't fix what's not broken
- no eval data — build the eval first, then decide
- use case is wholly off-the-shelf (search-as-a-service) — let the vendor pick
- compute / privacy makes the choice forced (only local models allowed)

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
| `content/02-output-contract.xml` | essential | JSON Schema for produces=decision-record + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=decision-record`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-embeddings-model-selection.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | Embeddings model decision record skeleton |
| `templates/axis-scoring.csv` | 3-axis scoring rubric template |
| `templates/eval-script.py` | Embedding eval script (recall@k) |
| `templates/matryoshka-truncate.py` | Matryoshka truncation helper |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embeddings-model-selection.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-three-axes`, `r2-eval-driven`, `r3-asymmetric-when-search`, `r4-matryoshka-when-budget`, `r5-rejected-documented` from `content/01-core-rules.xml`.
