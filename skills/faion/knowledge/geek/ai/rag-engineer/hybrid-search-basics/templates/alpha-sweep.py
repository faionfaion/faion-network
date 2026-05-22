# purpose: alpha sweep for linear-fusion hybrid search
# consumes: labeled query set + dense_search + sparse_search callables
# produces: prints NDCG@10 for each alpha; returns dict {alpha: score}
# depends-on: content/01-core-rules.xml rule r2
# token-budget-impact: zero at runtime; local eval loop

from typing import Callable, List, Dict


def ndcg_at_k(ranked_ids: List[str], relevant_ids: set, k: int = 10) -> float:
    import math
    dcg = 0.0
    for i, doc_id in enumerate(ranked_ids[:k]):
        if doc_id in relevant_ids:
            dcg += 1.0 / math.log2(i + 2)
    ideal = sum(1.0 / math.log2(i + 2) for i in range(min(len(relevant_ids), k)))
    return dcg / ideal if ideal > 0 else 0.0


def sweep(
    queries: List[Dict],
    dense_search: Callable[[str, int], List[Dict]],
    sparse_search: Callable[[str, int], List[Dict]],
    k_pool: int = 50,
    k_eval: int = 10,
) -> Dict[float, float]:
    results: Dict[float, float] = {}
    for alpha in (0.0, 0.25, 0.5, 0.75, 1.0):
        scores = []
        for q in queries:
            dense = {d["id"]: float(d["score"]) for d in dense_search(q["query"], k_pool)}
            sparse = {d["id"]: float(d["score"]) for d in sparse_search(q["query"], k_pool)}
            # min-max normalise per leg
            def norm(d):
                if not d:
                    return {}
                lo, hi = min(d.values()), max(d.values())
                return {k_: (v - lo) / (hi - lo + 1e-9) for k_, v in d.items()}
            d_n = norm(dense)
            s_n = norm(sparse)
            ids = set(d_n) | set(s_n)
            fused = {i: alpha * d_n.get(i, 0) + (1 - alpha) * s_n.get(i, 0) for i in ids}
            ranked = sorted(fused, key=fused.get, reverse=True)
            scores.append(ndcg_at_k(ranked, set(q["relevant_ids"]), k_eval))
        avg = sum(scores) / len(scores) if scores else 0.0
        results[alpha] = avg
        print(f"alpha={alpha:.2f}  ndcg@{k_eval}={avg:.4f}")
    return results
