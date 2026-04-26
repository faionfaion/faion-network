"""
Semantic deduplication for brainstorming idea lists.
Removes near-duplicate ideas using sentence-transformers cosine similarity.

Install: pip install sentence-transformers
Usage:
  ideas = ["Automate onboarding email", "Send automated onboarding emails", "Build a kanban board"]
  unique = semantic_dedup(ideas, threshold=0.82)
"""

from sentence_transformers import SentenceTransformer, util


def semantic_dedup(ideas: list[str], threshold: float = 0.82) -> list[str]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(ideas, convert_to_tensor=True)
    keep: list[str] = []
    dropped: set[int] = set()

    for i in range(len(ideas)):
        if i in dropped:
            continue
        keep.append(ideas[i])
        for j in range(i + 1, len(ideas)):
            if j not in dropped:
                sim = float(util.cos_sim(embeddings[i], embeddings[j]))
                if sim >= threshold:
                    dropped.add(j)

    return keep
