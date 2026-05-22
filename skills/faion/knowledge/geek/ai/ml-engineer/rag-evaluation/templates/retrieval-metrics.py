# purpose: Retrieval metrics calculator: Precision@K, Recall@K, MRR, Hit Rate
# consumes: retrieved doc ids + relevance labels
# produces: metric dict for the report
# depends-on: content/02-output-contract.xml
# token-budget-impact: small

"""
Retrieval metrics: hit rate, MRR, Precision@K.
Input: lists of retrieved and relevant document IDs per query.
"""


def compute_retrieval_metrics(
    retrieved_doc_ids: list[list[str]],
    relevant_doc_ids: list[list[str]],
    k: int = 10,
) -> dict:
    """
    Compute hit rate, MRR, and Precision@K over a query set.

    Args:
        retrieved_doc_ids: For each query, ordered list of retrieved doc IDs
        relevant_doc_ids: For each query, set of relevant doc IDs
        k: Cutoff rank

    Returns:
        Dict with hit_rate@k, mrr@k, precision@k
    """
    hit_rates, mrr_scores, precision_scores = [], [], []

    for retrieved, relevant in zip(retrieved_doc_ids, relevant_doc_ids):
        relevant_set = set(relevant)
        top_k = retrieved[:k]

        # Hit rate: was at least one relevant doc in top-K?
        hit_rates.append(float(any(doc in relevant_set for doc in top_k)))

        # MRR: reciprocal rank of first relevant doc
        mrr = 0.0
        for rank, doc in enumerate(top_k, 1):
            if doc in relevant_set:
                mrr = 1.0 / rank
                break
        mrr_scores.append(mrr)

        # Precision@K
        hits = sum(1 for doc in top_k if doc in relevant_set)
        precision_scores.append(hits / k)

    n = len(hit_rates)
    return {
        f"hit_rate@{k}": sum(hit_rates) / n,
        f"mrr@{k}": sum(mrr_scores) / n,
        f"precision@{k}": sum(precision_scores) / n,
        "n_queries": n,
    }
