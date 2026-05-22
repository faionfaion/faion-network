---
slug: rag
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Specifies a production RAG pipeline: chunking strategy, embedding model, vector DB, hybrid search, reranking, prompt template, and evaluation hooks.
content_id: "3328b6fffebf5dd2"
complexity: deep
produces: spec
est_tokens: 4300
tags: [rag, retrieval, embeddings, vector-db, llm]
---
# RAG (Retrieval-Augmented Generation)

## Summary

**One-sentence:** Specifies a production RAG pipeline: chunking strategy, embedding model, vector DB, hybrid search, reranking, prompt template, and evaluation hooks.

**One-paragraph:** Specifies a production RAG pipeline: chunking strategy, embedding model, vector DB, hybrid search, reranking, prompt template, and evaluation hooks. The methodology assumes the inputs in Prerequisites and produces a `spec` artefact validated by `scripts/validate-rag.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** ML engineers building RAG systems beyond toy notebooks: production indexing, retrieval, and generation with evaluation.

## Applies If (ALL must hold)

- The application needs to answer questions about documents not in the model's training data
- Knowledge is updated frequently (daily/weekly) and retraining is impractical
- Users need source citations to verify claims
- The knowledge base is too large to fit in a single context window (more than a few hundred pages)
- Multi-tenant system where each tenant has a separate knowledge base

## Skip If (ANY kills it)

- Knowledge is behavioral (writing style, persona, domain jargon) rather than factual — use fine-tuning
- The corpus is fewer than 50 documents that can all fit in a single long-context prompt — skip retrieval entirely
- Latency budget is under 200ms — retrieval + reranking adds 100-500ms overhead
- The task is pure reasoning on data already in the prompt — adding retrieval introduces noise

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[rag-evaluation]]` | Adjacent context the agent normally already has when this methodology fires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules with rationale and source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples for the output artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix. | ~800 |
| `content/04-procedure.xml` | medium | Five-step procedure with decision-gates. | ~700 |
| `content/05-examples.xml` | medium | One end-to-end worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether the methodology applies, ending in rule refs. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-requirements` | sonnet | Structured interview-style extraction. |
| `synthesize-spec` | opus | Cross-section trade-off synthesis. |
| `lint-output` | haiku | Schema validation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/spec.md.tmpl` | Markdown spec skeleton with the required sections + placeholders. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[rag-evaluation]]
- [[chunking-strategies]]
- [[hybrid-search]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `rag` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
