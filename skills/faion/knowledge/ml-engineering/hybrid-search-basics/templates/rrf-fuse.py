# purpose: Reciprocal Rank Fusion implementation for hybrid search
# consumes: ranked result lists from dense + sparse legs
# produces: fused rank list ready for the top-K cut
# depends-on: content/01-core-rules.xml r1-rrf-default
# token-budget-impact: zero at runtime; reference scaffold only

"""Provider-agnostic RRF fusion of ranked ID lists.

Usage:
    fused = rrf_fuse([vector_ids, bm25_ids])
    top_ids = [doc_id for doc_id, _ in fused[:10]]
"""
from collections import defaultdict


def rrf_fuse(
    rankings: list[list[str]],
    k: int = 60,
) -> list[tuple[str, float]]:
    """Reciprocal Rank Fusion over multiple ranked ID lists.

    Args:
        rankings: List of ranked document ID lists, one per retriever.
                  Each list is ordered from most to least relevant.
        k: RRF constant (default 60 from original paper). Higher k reduces
           the impact of rank position differences.

    Returns:
        Sorted list of (doc_id, rrf_score) tuples, highest score first.
    """
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] += 1.0 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
