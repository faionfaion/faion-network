# purpose: dynamic alpha selector for linear-fusion hybrid search
# consumes: query string + query features
# produces: alpha ∈ [0,1] per query
# depends-on: content/01-core-rules.xml r2-tune-alpha
# token-budget-impact: zero at runtime; reference scaffold only

"""Dynamic alpha selection for hybrid search based on query characteristics.

Usage:
    alpha = compute_alpha("What is the price of SKU-8942?")
    results = hybrid_search(query, alpha=alpha)
"""


def compute_alpha(query: str) -> float:
    """Select semantic/keyword weight based on query characteristics.

    Alpha = 1.0 is pure semantic (vector) search.
    Alpha = 0.0 is pure keyword (BM25) search.

    Args:
        query: The user's search query string.

    Returns:
        Alpha value in [0.0, 1.0] for use in the hybrid search call.
    """
    # Quoted phrase → favor exact keyword match
    if '"' in query:
        return 0.2

    # Contains digits/codes → likely product/model numbers
    if any(c.isdigit() for c in query):
        return 0.35

    # Short query (≤3 words) → specific lookup, balance evenly
    if len(query.split()) <= 3:
        return 0.5

    # Long conceptual query → favor semantic understanding
    return 0.7
