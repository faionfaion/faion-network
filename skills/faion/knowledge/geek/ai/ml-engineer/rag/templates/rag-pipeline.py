# Production RAG pipeline: ingest → index → query with reranking (LlamaIndex)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.embeddings.openai import OpenAIEmbedding

# 1. Ingest documents with metadata preservation
docs = SimpleDirectoryReader("./docs", filename_as_id=True).load_data()
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=80)
nodes = splitter.get_nodes_from_documents(docs)

# 2. Index with embedding model
embed_model = OpenAIEmbedding(model="text-embedding-3-small")
index = VectorStoreIndex(nodes, embed_model=embed_model)

# 3. Query with broad retrieval + cross-encoder reranking
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-2-v2",
    top_n=5,
)
query_engine = index.as_query_engine(
    similarity_top_k=20,  # broad recall
    node_postprocessors=[reranker],  # precise reranking to top-5
)

response = query_engine.query("What is the refund policy?")
# Always check for empty results before using response
if not response.source_nodes:
    print("No relevant information found.")
else:
    print(response.response)
    for src in response.source_nodes:
        print(f"  [{src.score:.3f}] {src.metadata.get('file_name')}")
