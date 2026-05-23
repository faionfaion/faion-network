# RAG Evaluation Pipeline

## Summary

**One-sentence:** Runs the full eval set through the RAG pipeline, computes retrieval + generation metrics, aggregates, and exports a JSON report.

**One-paragraph:** A complete evaluation pipeline runs each test-set question through the production RAG pipeline, computes retrieval metrics (precision@5, recall@5, MRR, hit rate) and generation metrics (faithfulness, answer relevance, context relevance) via LLM scoring or RAGAS, aggregates results, and exports to JSON. Human review of the aggregated report is required before any pipeline change is merged to production.

**Ефективно для:** команд, які тримають baseline-quality reports і блокують деплой при регресі.

## Applies If (ALL must hold)

- Before deploying a RAG system to production — establishing baseline quality scores.
- After any pipeline change (chunking, top-K, model swap) to detect regressions.
- Test set has at least 20 questions.
- Weekly batch evaluation on a sampled subset in production to catch drift.

## Skip If (ANY kills it)

- Real-time evaluation of every production query — use lightweight metrics instead.
- No ground truth available — only faithfulness and answer_relevance are computable.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| RAG pipeline runner | callable | rag-implementation |
| Test set | JSONL {query, ground_truth_chunk_ids, ground_truth_answer?} | rag-eval-test-set-generation |
| Metric set | rag-eval-retrieval-metrics + rag-eval-generation-metrics | config |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-eval-retrieval-metrics` | Computes precision/recall/MRR rows. |
| `geek/ai/rag-engineer/rag-eval-generation-metrics` | Computes RAG Triad rows. |

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
| Run pipeline over test set | haiku | Mechanical loop. |
| Compute metrics | haiku | Pure arithmetic + LLM judge for generation. |
| Aggregate report | sonnet | Per-bucket framing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/eval-runner.py` | End-to-end eval runner that consumes test JSONL and emits report JSON. |
| `templates/report-skeleton.json` | Empty report shape matching schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-eval-pipeline.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[rag-eval-strategy]]
- [[rag-eval-retrieval-metrics]]
- [[rag-eval-generation-metrics]]
- [[rag-eval-ab-testing]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks between full-set, sampled, or skip based on the use case (PR gate / weekly / realtime). Each leaf references a rule id from `01-core-rules.xml`.
