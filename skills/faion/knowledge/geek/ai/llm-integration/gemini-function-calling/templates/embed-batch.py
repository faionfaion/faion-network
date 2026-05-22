"""
purpose: Batch embedding helper for Gemini text-embedding-004 (768-dim).
consumes: list of texts + task type
produces: list of 768-dim embeddings
depends-on: gemini-function-calling sibling RAG patterns
token-budget-impact: per-text embedding cost

Usage:
    doc_embeddings = embed_batch(document_texts)                     # for indexing
    query_embedding = embed_batch([query], task="RETRIEVAL_QUERY")[0] # for search
"""
import google.generativeai as genai

genai.configure(api_key="GOOGLE_API_KEY")

VALID_TASKS = {
    "RETRIEVAL_DOCUMENT",
    "RETRIEVAL_QUERY",
    "SEMANTIC_SIMILARITY",
    "CLASSIFICATION",
    "CLUSTERING",
}


def embed_batch(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a list of texts using text-embedding-004 (768 dimensions).

    Args:
        texts: List of strings to embed.
        task: Embedding task type. Use RETRIEVAL_DOCUMENT for indexing,
              RETRIEVAL_QUERY for search queries.

    Returns:
        List of 768-dimensional embedding vectors.
    """
    assert task in VALID_TASKS, f"Invalid task: {task}. Must be one of {VALID_TASKS}"
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=texts,
        task_type=task,
    )
    return result["embedding"]
