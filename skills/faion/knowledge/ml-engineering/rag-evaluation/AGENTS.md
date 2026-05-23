# RAG Evaluation

## Summary

**One-sentence:** Evaluates a RAG pipeline by measuring retrieval (Precision@K, Recall@K, MRR, Hit Rate) and generation (Faithfulness, Answer Relevance, Hallucination Rate) components independently.

**One-paragraph:** Evaluates a RAG pipeline by measuring retrieval (Precision@K, Recall@K, MRR, Hit Rate) and generation (Faithfulness, Answer Relevance, Hallucination Rate) components independently. The methodology assumes the inputs in Prerequisites and produces a `report` artefact validated by `scripts/validate-rag-evaluation.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** ML engineers gating RAG promotions: separating retrieval failures from generation hallucinations to target the right fix.

## Applies If (ALL must hold)

- Before promoting a RAG pipeline to production — validate retrieval recall and generation faithfulness.
- After changing chunking strategy, embedding model, or vector DB configuration — check for regression.
- Comparing two embedding models for the same corpus — use Precision@K and MRR to decide.
- Diagnosing user complaints about wrong or hallucinated answers.
- Setting up continuous production monitoring (lightweight faithfulness + hit rate, sampled hourly).

## Skip If (ANY kills it)

- No ground truth queries and the domain is too specialized for reliable synthetic generation.
- Pipeline is a prototype and chunking/embedding strategy is still changing daily — evaluate after it stabilizes.
- Budget is insufficient for LLM-as-judge at scale — use automated retrieval metrics only as a proxy.
- Primary goal is latency optimization, not quality — use profiling tools instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[rag]]` | Adjacent context the agent normally already has when this methodology fires. |

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
| `compute-metrics` | sonnet | Deterministic metric computation. |
| `synthesize-narrative` | opus | Cross-metric story with caveats. |
| `format-report` | haiku | Template binding. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/report.md.tmpl` | Markdown report skeleton: metrics table, narrative, caveats, attachments. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-evaluation.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[rag]]
- [[embeddings-evaluation]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `rag-evaluation` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
