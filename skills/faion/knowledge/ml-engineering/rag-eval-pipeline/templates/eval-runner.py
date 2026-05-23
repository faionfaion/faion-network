# purpose: end-to-end RAG eval runner
# consumes: test_set JSONL, pipeline_callable, judge
# produces: report JSON matching 02-output-contract
# depends-on: content/01-core-rules.xml r1-r5
# token-budget-impact: zero at runtime; eval-time only

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
