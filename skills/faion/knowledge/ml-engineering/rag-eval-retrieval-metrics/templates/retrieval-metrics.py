# purpose: per-query retrieval metric implementations
# consumes: retrieved_ids list + relevant_ids list (or graded dict)
# produces: dict {precision, recall, mrr, [ndcg]}
# depends-on: content/01-core-rules.xml r1-r4
# token-budget-impact: zero at runtime; metric primitives

import math
from typing import List, Dict, Optional


def precision_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    if k <= 0:
        return 0.0
    return sum(1 for x in retrieved[:k] if x in set(relevant)) / k


def recall_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    if not relevant:
        return 0.0
    return sum(1 for x in retrieved[:k] if x in set(relevant)) / len(relevant)


def mrr(retrieved: List[str], relevant: List[str]) -> float:
    s = set(relevant)
    for i, x in enumerate(retrieved, 1):
        if x in s:
            return 1.0 / i
    return 0.0


def ndcg_at_k(retrieved: List[str], graded: Dict[str, float], k: int) -> float:
    dcg = 0.0
    for i, x in enumerate(retrieved[:k]):
        rel = graded.get(x, 0.0)
        dcg += (2 ** rel - 1) / math.log2(i + 2)
    ideal = sorted(graded.values(), reverse=True)[:k]
    idcg = sum((2 ** r - 1) / math.log2(i + 2) for i, r in enumerate(ideal))
    return dcg / idcg if idcg > 0 else 0.0
