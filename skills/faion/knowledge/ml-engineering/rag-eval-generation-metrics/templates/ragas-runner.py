# purpose: minimal RAGAS wrapper that emits JSONL per query
# consumes: list of {query, answer, contexts, ground_truth?}
# produces: JSONL matching 02-output-contract schema
# depends-on: ragas pip package
# token-budget-impact: zero at runtime; eval-time only

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
