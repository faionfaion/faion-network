# RAG Generation Quality Metrics

## Summary

**One-sentence:** Computes the RAG Triad (faithfulness, answer relevance, context relevance) via LLM-judge or RAGAS and exports a per-question scorecard.

**One-paragraph:** Generation metrics measure whether the RAG pipeline produces answers that are faithful to the retrieved context, relevant to the question, and sourced from contextually relevant documents. The three core metrics — Faithfulness, Answer Relevance, and Context Relevance — form the RAG Triad and are computed via LLM-judge prompts or the RAGAS framework. Use for development gates and offline production sampling.

**Ефективно для:** команд, які перевіряють якість генерації RAG до production-rollout або під час offline-sampling.

## Applies If (ALL must hold)

- Evaluating whether generated answers hallucinate (Faithfulness) — essential before production deploy.
- Checking whether answers address the user question (Answer Relevance).
- Checking whether retrieved context contains the info needed (Context Relevance).
- Sampling 10-20% of production queries for offline faithfulness monitoring.

## Skip If (ANY kills it)

- Real-time per-query LLM judging in production — too slow / expensive; use offline sampling.
- Cross-LLM judge comparisons — RAGAS scores vary by judge; not cross-comparable.
- Replacing retrieval metrics — without precision@K you cannot localise the failure.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| RAG pipeline output | JSONL {query, answer, context} | rag pipeline |
| Judge LLM credentials | env | infra |
| RAGAS install (optional) | pip | requirements |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-eval-retrieval-metrics` | Pairs with retrieval metrics to localise failure. |
| `geek/ai/rag-engineer/rag-eval-strategy` | Defines which metrics to run, when. |

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
| Run LLM-judge per query | haiku | Mechanical scoring. |
| Aggregate and write report | sonnet | Trade-off framing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/judge-prompt-faithfulness.txt` | Faithfulness judge prompt. |
| `templates/judge-prompt-relevance.txt` | Answer/context relevance judge prompt. |
| `templates/ragas-runner.py` | RAGAS wrapper that exports JSONL. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-eval-generation-metrics.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[rag-eval-retrieval-metrics]]
- [[rag-eval-pipeline]]
- [[rag-eval-strategy]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` selects between full-Triad, sampled-Triad, or skip based on context and judge availability. Each leaf references a rule id from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/judge-prompt-faithfulness.txt`

```text
You are evaluating whether the ANSWER is fully supported by the CONTEXT.
Return ONLY a float between 0 and 1 (no other text).

CONTEXT:
{context}

ANSWER:
{answer}

Score:
```

### `templates/judge-prompt-relevance.txt`

```text
Return JSON only: {"answer_relevance": <0-1>, "context_relevance": <0-1>}

QUERY: {query}
CONTEXT: {context}
ANSWER: {answer}
```

### `templates/ragas-runner.py`

```python
from typing import List, Dict
import json

def run(records: List[Dict], judge_model: str, out_path: str) -> None:
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy, context_precision
    ds = evaluate(records, metrics=[faithfulness, answer_relevancy, context_precision])
    with open(out_path, 'w', encoding='utf-8') as f:
        for row, rec in zip(ds.to_pandas().itertuples(), records):
            f.write(json.dumps({
                'query_id': rec['query_id'],
                'judge_model': judge_model,
                'faithfulness': float(row.faithfulness),
                'answer_relevance': float(row.answer_relevancy),
                'context_relevance': float(row.context_precision),
            }) + '\n')
```
