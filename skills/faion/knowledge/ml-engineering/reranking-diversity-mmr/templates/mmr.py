# purpose: Maximal Marginal Relevance rerank
# consumes: query_embedding, candidates [{id, score, embedding}], lambda, top_k
# produces: dict matching 02-output-contract schema
# depends-on: content/01-core-rules.xml r1-r5
# token-budget-impact: zero at runtime; pairwise compute only

import math
from typing import List, Dict


def cosine(a, b):
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def mmr(query_embedding, candidates: List[Dict], lambda_: float = 0.5, top_k: int = 5) -> Dict:
    selected: List[Dict] = []
    pool = list(candidates)
    while pool and len(selected) < top_k:
        best, best_score = None, -1e9
        for c in pool:
            rel = cosine(query_embedding, c['embedding'])
            div = max((cosine(c['embedding'], s['embedding']) for s in selected), default=0.0)
            score = lambda_ * rel - (1 - lambda_) * div
            if score > best_score:
                best, best_score = c, score
                best_rel = rel
                best_div = div
        selected.append({'id': best['id'], 'relevance': best_rel, 'diversity_penalty': best_div, 'mmr_score': best_score})
        pool.remove(best)
    return {'lambda': lambda_, 'pool_n': len(candidates), 'top_k': top_k, 'results': selected}
