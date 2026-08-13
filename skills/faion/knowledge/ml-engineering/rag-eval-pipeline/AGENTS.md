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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/eval-runner.py`

```python
import json
from statistics import mean


def run(test_set, pipeline, judge, snapshot):
    rows = []
    for q in test_set:
        out = pipeline(q['query'])
        retr = _retrieval_metrics(out['retrieved_ids'], q.get('ground_truth_chunk_ids', []))
        gen = judge.score(q['query'], out['answer'], out['context'])
        rows.append({'query_id': q.get('query_id'), **retr, **gen})
    retr_agg = {k: mean(r[k] for r in rows) for k in ('precision_at_5', 'recall_at_5', 'mrr')}
    retr_agg['hit_rate'] = mean(1.0 if r['mrr'] > 0 else 0.0 for r in rows)
    gen_agg = {k: mean(r[k] for r in rows) for k in ('faithfulness', 'answer_relevance', 'context_relevance')}
    return {'snapshot': snapshot, 'n_questions': len(rows), 'retrieval': retr_agg, 'generation': gen_agg, 'per_query': rows}


def _retrieval_metrics(retrieved_ids, ground_truth_ids):
    gt = set(ground_truth_ids)
    hits = [i for i, x in enumerate(retrieved_ids[:5], 1) if x in gt]
    return {
        'precision_at_5': len(hits) / 5,
        'recall_at_5': len(hits) / max(len(gt), 1),
        'mrr': 1.0 / hits[0] if hits else 0.0,
    }
```

### `templates/report-skeleton.json`

```json
{
  "snapshot": {
    "pipeline_version": "",
    "judge_model": "",
    "embedding_model": "",
    "test_set_hash": ""
  },
  "n_questions": 0,
  "retrieval": {
    "precision_at_5": 0,
    "recall_at_5": 0,
    "mrr": 0,
    "hit_rate": 0
  },
  "generation": {
    "faithfulness": 0,
    "answer_relevance": 0,
    "context_relevance": 0
  },
  "per_query": []
}
```
