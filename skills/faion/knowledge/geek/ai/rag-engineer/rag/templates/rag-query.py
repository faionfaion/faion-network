# purpose: RAG query execution helper (legacy variant)
# consumes: vector_store + reranker + llm + query
# produces: RAG answer dict matching 02-output-contract
# depends-on: templates/rag-pipeline.py.tmpl
# token-budget-impact: zero at runtime; scaffold

"""Minimal RAG query with cross-encoder reranking using LlamaIndex.

Usage:
    response = rag_query("What are the key phases of SDD?")
    print(response.response)
    for node in response.source_nodes:
        print(f"[{node.score:.2f}] {node.metadata.get('file_name')}")
"""
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.postprocessor import SentenceTransformerRerank

INDEX_DIR = "./index"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-2-v2"


def build_query_engine(index_dir: str = INDEX_DIR, top_n: int = 5):
    """Load index from disk and build a query engine with reranking.

    Args:
        index_dir: Directory where the LlamaIndex index was persisted.
        top_n: Number of chunks to return after reranking (retrieve 20, rerank to top_n).
    """
    storage = StorageContext.from_defaults(persist_dir=index_dir)
    index = load_index_from_storage(storage)
    reranker = SentenceTransformerRerank(model=RERANKER_MODEL, top_n=top_n)
    return index.as_query_engine(
        similarity_top_k=20,  # retrieve broadly
        node_postprocessors=[reranker],  # rerank to top_n
        response_mode="compact",
    )


_engine = None


def rag_query(question: str) -> object:
    """Query the RAG pipeline. Returns LlamaIndex Response with source_nodes.

    Args:
        question: Natural language question to answer from the knowledge base.
    """
    global _engine
    if _engine is None:
        _engine = build_query_engine()
    return _engine.query(question)
