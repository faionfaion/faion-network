"""
Reciprocal Rank Fusion (RRF) implementation.
Input: list of ranked doc_id lists (one per retriever, best first)
Output: sorted list of (doc_id, rrf_score) tuples
k=60 per original RRF paper (Cormack et al., SIGIR 2009).
"""
from collections import defaultdict


def reciprocal_rank_fusion(
    result_lists: list[list[str]],
    k: int = 60,
    top_n: int = 10,
) -> list[tuple[str, float]]:
    scores: dict[str, float] = defaultdict(float)
    for result_list in result_lists:
        for rank, doc_id in enumerate(result_list, start=1):
            scores[doc_id] += 1.0 / (k + rank)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]


# Example: merge BM25 and vector results
if __name__ == "__main__":
    bm25_ids = ["doc3", "doc1", "doc5", "doc2"]
    vector_ids = ["doc1", "doc3", "doc7", "doc5"]
    fused = reciprocal_rank_fusion([bm25_ids, vector_ids])
    for doc_id, score in fused:
        print(f"{doc_id}: {score:.4f}")
