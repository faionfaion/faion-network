"""
Document-type-aware chunker dispatcher using chonkie.
Input: text string + doc_type string
Output: list of {text, token_count} dicts
"""
from chonkie import TokenChunker, RecursiveChunker, SemanticChunker, CodeChunker


def get_chunker(doc_type: str, embed_fn=None):
    """Return the appropriate chunker for the given document type."""
    if doc_type == "code":
        return CodeChunker(chunk_size=512)
    elif doc_type == "markdown":
        return RecursiveChunker(
            chunk_size=512,
            chunk_overlap=80,
            separators=["\n## ", "\n### ", "\n\n", "\n", " "],
        )
    elif doc_type in ("legal", "scientific"):
        if embed_fn is None:
            raise ValueError("SemanticChunker requires an embed_fn")
        return SemanticChunker(
            embedding_model=embed_fn,
            similarity_threshold=0.80,
            min_chunk_size=100,
            max_chunk_size=800,
        )
    else:  # general / fallback
        return RecursiveChunker(chunk_size=512, chunk_overlap=77)  # 15% overlap


def chunk_document(text: str, doc_type: str, embed_fn=None) -> list[dict]:
    """Chunk a document and return list of {text, token_count} dicts."""
    chunker = get_chunker(doc_type, embed_fn)
    chunks = chunker(text)
    return [{"text": c.text, "token_count": c.token_count} for c in chunks]


# Example usage
if __name__ == "__main__":
    with open("example.py") as f:
        code = f.read()
    chunks = chunk_document(code, "code")
    print(f"Code chunked into {len(chunks)} chunks")
