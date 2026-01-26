# RAG Examples and Architectures

Real-world RAG implementations with complete code examples.

## Table of Contents

1. [Basic RAG Pipeline](#basic-rag-pipeline)
2. [LlamaIndex Implementation](#llamaindex-implementation)
3. [LangChain Implementation](#langchain-implementation)
4. [Hybrid Search RAG](#hybrid-search-rag)
5. [Agentic RAG](#agentic-rag)
6. [Multi-Modal RAG](#multi-modal-rag)
7. [Production Architecture](#production-architecture)
8. [Performance Optimization](#performance-optimization)

---

## Basic RAG Pipeline

### Minimal Working Example (LlamaIndex)

```python
"""
Minimal RAG pipeline with LlamaIndex.
Requirements: pip install llama-index llama-index-llms-openai
"""
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
import os

# Set API key
os.environ["OPENAI_API_KEY"] = "your-api-key"

# 1. Load documents
documents = SimpleDirectoryReader("./data").load_data()
print(f"Loaded {len(documents)} documents")

# 2. Create index (embeds and stores)
index = VectorStoreIndex.from_documents(documents)

# 3. Create query engine
query_engine = index.as_query_engine(
    similarity_top_k=5,
    llm=OpenAI(model="gpt-4o-mini", temperature=0)
)

# 4. Query
response = query_engine.query("What is the main topic of these documents?")
print(response.response)

# 5. Show sources
for node in response.source_nodes:
    print(f"Source: {node.metadata.get('file_name', 'unknown')}")
    print(f"Score: {node.score:.3f}")
```

### Minimal Working Example (LangChain)

```python
"""
Minimal RAG pipeline with LangChain.
Requirements: pip install langchain langchain-openai langchain-chroma
"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import os

os.environ["OPENAI_API_KEY"] = "your-api-key"

# 1. Load documents
loader = DirectoryLoader("./data", glob="**/*.md")
documents = loader.load()
print(f"Loaded {len(documents)} documents")

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# 3. Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. Create QA chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

# 5. Query
result = qa_chain.invoke({"query": "What is the main topic?"})
print(result["result"])

# 6. Show sources
for doc in result["source_documents"]:
    print(f"Source: {doc.metadata.get('source', 'unknown')}")
```

---

## LlamaIndex Implementation

### Production-Ready Setup with Qdrant

```python
"""
Production RAG with LlamaIndex and Qdrant.
Requirements:
    pip install llama-index llama-index-vector-stores-qdrant
    pip install llama-index-embeddings-openai llama-index-llms-openai
    pip install qdrant-client
"""
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
    PromptTemplate,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from qdrant_client import QdrantClient
import os

os.environ["OPENAI_API_KEY"] = "your-api-key"

# Configure global settings
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")
Settings.llm = OpenAI(model="gpt-4o", temperature=0)

class ProductionRAG:
    def __init__(self, data_dir: str, collection_name: str = "knowledge_base"):
        self.data_dir = data_dir
        self.collection_name = collection_name
        self.client = QdrantClient(path="./qdrant_data")
        self.index = None

    def build_index(self):
        """Build vector index from documents."""
        # Load documents
        documents = SimpleDirectoryReader(
            input_dir=self.data_dir,
            recursive=True,
            required_exts=[".pdf", ".md", ".txt", ".docx"],
            exclude_hidden=True,
        ).load_data()
        print(f"Loaded {len(documents)} documents")

        # Configure chunking
        parser = SentenceSplitter(
            chunk_size=1024,
            chunk_overlap=200,
            paragraph_separator="\n\n",
        )
        nodes = parser.get_nodes_from_documents(documents)
        print(f"Created {len(nodes)} chunks")

        # Setup vector store
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Build index
        self.index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            show_progress=True,
        )

        # Persist
        self.index.storage_context.persist(persist_dir="./index_storage")
        print("Index built and persisted")

    def load_index(self):
        """Load existing index."""
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
        )
        self.index = VectorStoreIndex.from_vector_store(vector_store)
        print("Index loaded")

    def query(self, question: str, top_k: int = 10, rerank_top_n: int = 5):
        """Query with reranking and citations."""
        if not self.index:
            self.load_index()

        # Custom prompt with citations
        qa_prompt = PromptTemplate(
            """You are a helpful assistant. Answer the question using ONLY the provided context.
Always cite your sources using [Source: filename] format.

Context:
{context_str}

Question: {query_str}

Instructions:
1. Answer based only on the context provided
2. Cite specific sources for each claim
3. If the context doesn't contain the answer, say "I don't have information about that"

Answer:"""
        )

        # Reranker for quality
        reranker = SentenceTransformerRerank(
            model="cross-encoder/ms-marco-MiniLM-L-2-v2",
            top_n=rerank_top_n,
        )

        # Create query engine
        query_engine = self.index.as_query_engine(
            similarity_top_k=top_k,
            node_postprocessors=[reranker],
            text_qa_template=qa_prompt,
        )

        response = query_engine.query(question)

        return {
            "answer": response.response,
            "sources": [
                {
                    "file": node.metadata.get("file_name", "unknown"),
                    "score": node.score,
                    "text": node.text[:300] + "..."
                }
                for node in response.source_nodes
            ]
        }


# Usage
if __name__ == "__main__":
    rag = ProductionRAG("./data")

    # Build index (run once)
    rag.build_index()

    # Query
    result = rag.query("What are the key features of the product?")
    print("Answer:", result["answer"])
    print("\nSources:")
    for src in result["sources"]:
        print(f"  - {src['file']} (score: {src['score']:.3f})")
```

### Semantic Chunking with LlamaIndex

```python
"""
Semantic chunking for better retrieval quality.
Requirements: pip install llama-index llama-index-embeddings-openai
"""
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Document

embed_model = OpenAIEmbedding()

# Semantic splitter groups sentences by meaning
splitter = SemanticSplitterNodeParser(
    buffer_size=1,  # Sentences to compare at a time
    breakpoint_percentile_threshold=95,  # Split when similarity drops below this
    embed_model=embed_model,
)

# Example document
doc = Document(text="""
Machine learning is a subset of artificial intelligence. It enables systems
to learn from data. Deep learning is a type of machine learning using neural
networks.

The weather today is sunny with mild temperatures. Tomorrow expects rain
in the afternoon. The weekly forecast shows improving conditions.
""")

nodes = splitter.get_nodes_from_documents([doc])
for i, node in enumerate(nodes):
    print(f"Chunk {i+1}:\n{node.text}\n---")
```

---

## LangChain Implementation

### Production RAG with FastAPI

```python
"""
Production RAG API with LangChain and FastAPI.
Requirements:
    pip install langchain langchain-openai langchain-community
    pip install chromadb fastapi uvicorn pydantic
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
import os

app = FastAPI(title="RAG API")

# Initialize components
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Global vectorstore (in production, use persistent storage)
vectorstore = None


class IndexRequest(BaseModel):
    directory: str


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]


@app.post("/index")
async def build_index(request: IndexRequest):
    """Build index from directory of documents."""
    global vectorstore

    if not os.path.exists(request.directory):
        raise HTTPException(status_code=400, detail="Directory not found")

    # Load documents
    loader = DirectoryLoader(request.directory, glob="**/*.{md,txt,pdf}")
    documents = loader.load()

    if not documents:
        raise HTTPException(status_code=400, detail="No documents found")

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)

    # Create vectorstore with persistence
    vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory="./chroma_db"
    )

    return {
        "status": "success",
        "documents": len(documents),
        "chunks": len(chunks)
    }


@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """Query the RAG system."""
    global vectorstore

    if vectorstore is None:
        # Try to load from disk
        try:
            vectorstore = Chroma(
                persist_directory="./chroma_db",
                embedding_function=embeddings
            )
        except Exception:
            raise HTTPException(status_code=400, detail="Index not built")

    # Custom prompt
    prompt_template = """Use the following pieces of context to answer the question.
If you don't know the answer based on the context, say "I don't have enough information."
Always cite the source document for each claim.

Context:
{context}

Question: {question}

Answer with citations:"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # Create retriever with compression
    base_retriever = vectorstore.as_retriever(
        search_kwargs={"k": request.top_k * 2}
    )

    compressor = LLMChainExtractor.from_llm(llm)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=compression_retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    result = qa_chain.invoke({"query": request.question})

    sources = [
        {
            "source": doc.metadata.get("source", "unknown"),
            "content_preview": doc.page_content[:200] + "..."
        }
        for doc in result["source_documents"][:request.top_k]
    ]

    return QueryResponse(
        answer=result["result"],
        sources=sources
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### LCEL (LangChain Expression Language) RAG

```python
"""
Modern RAG with LCEL for composability.
Requirements: pip install langchain langchain-openai langchain-chroma
"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter


def format_docs(docs):
    """Format documents for context injection."""
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )


# Components
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Prompt
template = """Answer the question based only on the following context.
Cite sources using [Source: filename] format.

Context:
{context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

# LCEL Chain - composable and streamable
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Usage
response = rag_chain.invoke("What are the key features?")
print(response)

# Streaming
for chunk in rag_chain.stream("What are the key features?"):
    print(chunk, end="", flush=True)
```

---

## Hybrid Search RAG

### BM25 + Vector Fusion

```python
"""
Hybrid search combining BM25 (keyword) and vector (semantic) search.
Requirements: pip install llama-index llama-index-retrievers-bm25 rank-bm25
"""
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever

# Load and chunk documents
documents = SimpleDirectoryReader("./data").load_data()
parser = SentenceSplitter(chunk_size=512, chunk_overlap=100)
nodes = parser.get_nodes_from_documents(documents)

# Create vector index
vector_index = VectorStoreIndex(nodes)

# BM25 retriever (keyword matching)
bm25_retriever = BM25Retriever.from_defaults(
    nodes=nodes,
    similarity_top_k=10,
)

# Vector retriever (semantic matching)
vector_retriever = vector_index.as_retriever(similarity_top_k=10)

# Fusion retriever with reciprocal rank fusion
hybrid_retriever = QueryFusionRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    retriever_weights=[0.4, 0.6],  # 40% keyword, 60% semantic
    mode="reciprocal_rerank",  # RRF fusion
    similarity_top_k=5,  # Final results
)

# Query
results = hybrid_retriever.retrieve("machine learning neural networks")
for node in results:
    print(f"Score: {node.score:.3f}")
    print(f"Text: {node.text[:200]}...\n")
```

### LangChain Ensemble Retriever

```python
"""
Ensemble retriever with LangChain.
Requirements: pip install langchain langchain-openai langchain-chroma rank-bm25
"""
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load and split documents
loader = DirectoryLoader("./data", glob="**/*.md")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

# BM25 retriever
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 5

# Vector retriever
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Ensemble with weights
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]
)

# Query
results = ensemble_retriever.invoke("What is deep learning?")
for doc in results:
    print(f"Source: {doc.metadata.get('source', 'unknown')}")
    print(f"Content: {doc.page_content[:200]}...\n")
```

---

## Agentic RAG

### Self-Correcting RAG Agent

```python
"""
Agentic RAG with self-correction and tool use.
Requirements: pip install llama-index llama-index-agent-openai
"""
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI

# Create knowledge base index
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=5)

# Wrap as tool
rag_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="knowledge_base",
        description=(
            "Use this tool to search the knowledge base for information. "
            "Provide a clear, specific query. "
            "If the first query doesn't return good results, try rephrasing."
        ),
    ),
)

# Create agent with RAG tool
agent = OpenAIAgent.from_tools(
    tools=[rag_tool],
    llm=OpenAI(model="gpt-4o", temperature=0),
    verbose=True,
    system_prompt="""You are a helpful assistant with access to a knowledge base.

When answering questions:
1. First try to answer from the knowledge base
2. If results are insufficient, try rephrasing your query
3. Cite sources for all factual claims
4. If information is not in the knowledge base, say so clearly
"""
)

# Agent can decide when to use RAG vs. parametric knowledge
response = agent.chat("What are the main features of the product and how do they compare to competitors?")
print(response)
```

### Multi-Document Agent

```python
"""
Agent that routes queries to multiple specialized indexes.
"""
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent

# Create multiple specialized indexes
product_docs = SimpleDirectoryReader("./data/product").load_data()
product_index = VectorStoreIndex.from_documents(product_docs)

api_docs = SimpleDirectoryReader("./data/api").load_data()
api_index = VectorStoreIndex.from_documents(api_docs)

faq_docs = SimpleDirectoryReader("./data/faq").load_data()
faq_index = VectorStoreIndex.from_documents(faq_docs)

# Create tools for each index
tools = [
    QueryEngineTool(
        query_engine=product_index.as_query_engine(),
        metadata=ToolMetadata(
            name="product_docs",
            description="Product features, pricing, and capabilities",
        ),
    ),
    QueryEngineTool(
        query_engine=api_index.as_query_engine(),
        metadata=ToolMetadata(
            name="api_docs",
            description="API reference, endpoints, authentication, code examples",
        ),
    ),
    QueryEngineTool(
        query_engine=faq_index.as_query_engine(),
        metadata=ToolMetadata(
            name="faq",
            description="Frequently asked questions and troubleshooting",
        ),
    ),
]

# Agent routes to appropriate index
agent = OpenAIAgent.from_tools(
    tools=tools,
    verbose=True,
)

# Agent decides which tool(s) to use
response = agent.chat("How do I authenticate API requests and what rate limits apply?")
print(response)
```

---

## Multi-Modal RAG

### Vision + Text RAG

```python
"""
Multi-modal RAG with images and text.
Requirements: pip install llama-index llama-index-multi-modal-llms-openai
"""
from llama_index.core import SimpleDirectoryReader
from llama_index.core.indices.multi_modal import MultiModalVectorStoreIndex
from llama_index.multi_modal_llms.openai import OpenAIMultiModal

# Load documents including images
documents = SimpleDirectoryReader(
    "./data",
    required_exts=[".png", ".jpg", ".pdf", ".md"],
).load_data()

# Create multi-modal index
index = MultiModalVectorStoreIndex.from_documents(
    documents,
    show_progress=True,
)

# Multi-modal query engine
mm_llm = OpenAIMultiModal(model="gpt-4o", max_new_tokens=1500)
query_engine = index.as_query_engine(
    llm=mm_llm,
    similarity_top_k=5,
)

# Query can reference both text and images
response = query_engine.query(
    "What does the architecture diagram show and how does it relate to the documentation?"
)
print(response)
```

---

## Production Architecture

### Complete Production Pipeline

```python
"""
Production-grade RAG with all best practices.
"""
import logging
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from functools import lru_cache

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings,
)
from llama_index.core.postprocessor import (
    SentenceTransformerRerank,
    MetadataReplacementPostProcessor,
)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from qdrant_client import QdrantClient
import redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGConfig(BaseModel):
    """Configuration for RAG pipeline."""
    collection_name: str = "production_kb"
    embedding_model: str = "text-embedding-3-large"
    llm_model: str = "gpt-4o"
    chunk_size: int = 1024
    chunk_overlap: int = 200
    retrieval_top_k: int = 20
    rerank_top_n: int = 5
    temperature: float = 0.0
    cache_ttl: int = 3600  # 1 hour


class QueryResult(BaseModel):
    """Query result with metadata."""
    answer: str
    sources: list[dict]
    latency_ms: float
    cached: bool = False
    query_id: str


class ProductionRAG:
    """Production RAG with caching, monitoring, and error handling."""

    def __init__(
        self,
        config: RAGConfig,
        qdrant_url: str = "localhost",
        qdrant_port: int = 6333,
        redis_url: Optional[str] = None,
    ):
        self.config = config

        # Vector store
        self.qdrant_client = QdrantClient(host=qdrant_url, port=qdrant_port)
        self.vector_store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=config.collection_name,
        )

        # Redis cache (optional)
        self.cache = redis.from_url(redis_url) if redis_url else None

        # Configure LlamaIndex
        Settings.embed_model = OpenAIEmbedding(model=config.embedding_model)
        Settings.llm = OpenAI(model=config.llm_model, temperature=config.temperature)

        # Load index
        self.index = VectorStoreIndex.from_vector_store(self.vector_store)

        # Reranker
        self.reranker = SentenceTransformerRerank(
            model="cross-encoder/ms-marco-MiniLM-L-2-v2",
            top_n=config.rerank_top_n,
        )

        logger.info(f"ProductionRAG initialized with collection: {config.collection_name}")

    def _get_cache_key(self, query: str) -> str:
        """Generate cache key for query."""
        import hashlib
        return f"rag:query:{hashlib.sha256(query.encode()).hexdigest()[:16]}"

    def _check_cache(self, query: str) -> Optional[dict]:
        """Check cache for existing response."""
        if not self.cache:
            return None
        try:
            cached = self.cache.get(self._get_cache_key(query))
            if cached:
                import json
                return json.loads(cached)
        except Exception as e:
            logger.warning(f"Cache read error: {e}")
        return None

    def _set_cache(self, query: str, result: dict):
        """Cache response."""
        if not self.cache:
            return
        try:
            import json
            self.cache.setex(
                self._get_cache_key(query),
                self.config.cache_ttl,
                json.dumps(result)
            )
        except Exception as e:
            logger.warning(f"Cache write error: {e}")

    def query(
        self,
        question: str,
        filters: Optional[dict] = None,
        skip_cache: bool = False,
    ) -> QueryResult:
        """
        Query the RAG system.

        Args:
            question: User question
            filters: Optional metadata filters
            skip_cache: Skip cache lookup

        Returns:
            QueryResult with answer, sources, and metadata
        """
        import time
        import uuid

        start_time = time.time()
        query_id = str(uuid.uuid4())[:8]

        logger.info(f"[{query_id}] Query: {question[:50]}...")

        # Check cache
        if not skip_cache:
            cached = self._check_cache(question)
            if cached:
                logger.info(f"[{query_id}] Cache hit")
                return QueryResult(
                    **cached,
                    latency_ms=(time.time() - start_time) * 1000,
                    cached=True,
                    query_id=query_id,
                )

        try:
            # Build query engine with filters
            query_engine = self.index.as_query_engine(
                similarity_top_k=self.config.retrieval_top_k,
                node_postprocessors=[self.reranker],
                vector_store_kwargs={"filter": filters} if filters else {},
            )

            # Execute query
            response = query_engine.query(question)

            # Format result
            sources = [
                {
                    "file": node.metadata.get("file_name", "unknown"),
                    "score": round(node.score, 4),
                    "text": node.text[:500],
                }
                for node in response.source_nodes
            ]

            result = {
                "answer": response.response,
                "sources": sources,
            }

            # Cache result
            self._set_cache(question, result)

            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"[{query_id}] Completed in {latency_ms:.0f}ms")

            return QueryResult(
                **result,
                latency_ms=latency_ms,
                cached=False,
                query_id=query_id,
            )

        except Exception as e:
            logger.error(f"[{query_id}] Error: {e}")
            raise


# Usage
if __name__ == "__main__":
    config = RAGConfig(
        collection_name="my_knowledge_base",
        retrieval_top_k=15,
        rerank_top_n=5,
    )

    rag = ProductionRAG(
        config=config,
        qdrant_url="localhost",
        qdrant_port=6333,
        redis_url="redis://localhost:6379",
    )

    result = rag.query(
        "What are the security best practices?",
        filters={"category": "security"},
    )

    print(f"Answer: {result.answer}")
    print(f"Latency: {result.latency_ms:.0f}ms")
    print(f"Cached: {result.cached}")
    print(f"Sources: {len(result.sources)}")
```

---

## Performance Optimization

### Embedding Caching

```python
"""
Cache embeddings to reduce API calls and latency.
"""
from llama_index.core.embeddings import BaseEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
import hashlib
import redis
import json
from typing import List


class CachedEmbedding(BaseEmbedding):
    """Embedding model with Redis caching."""

    def __init__(
        self,
        base_model: BaseEmbedding,
        redis_url: str = "redis://localhost:6379",
        ttl: int = 86400 * 7,  # 7 days
    ):
        super().__init__()
        self._base_model = base_model
        self._cache = redis.from_url(redis_url)
        self._ttl = ttl

    def _cache_key(self, text: str) -> str:
        return f"emb:{hashlib.sha256(text.encode()).hexdigest()[:32]}"

    def _get_query_embedding(self, query: str) -> List[float]:
        key = self._cache_key(query)
        cached = self._cache.get(key)

        if cached:
            return json.loads(cached)

        embedding = self._base_model._get_query_embedding(query)
        self._cache.setex(key, self._ttl, json.dumps(embedding))
        return embedding

    def _get_text_embedding(self, text: str) -> List[float]:
        return self._get_query_embedding(text)  # Same logic

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)


# Usage
base_embed = OpenAIEmbedding(model="text-embedding-3-large")
cached_embed = CachedEmbedding(base_embed, redis_url="redis://localhost:6379")

# Use cached embedding in your index
Settings.embed_model = cached_embed
```

### Batch Processing

```python
"""
Efficient batch document processing.
"""
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time


def batch_embed_documents(
    documents: list[Document],
    batch_size: int = 100,
    max_workers: int = 4,
):
    """
    Process documents in batches with progress tracking.
    """
    parser = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
    embed_model = OpenAIEmbedding(model="text-embedding-3-large")

    # 1. Parse all documents into nodes
    print("Parsing documents...")
    all_nodes = []
    for doc in tqdm(documents, desc="Parsing"):
        nodes = parser.get_nodes_from_documents([doc])
        all_nodes.extend(nodes)

    print(f"Created {len(all_nodes)} chunks")

    # 2. Batch embed with rate limiting
    print("Embedding chunks...")
    embeddings = []

    for i in tqdm(range(0, len(all_nodes), batch_size), desc="Embedding"):
        batch = all_nodes[i:i + batch_size]
        texts = [node.text for node in batch]

        # Embed batch
        batch_embeddings = embed_model._get_text_embeddings(texts)
        embeddings.extend(batch_embeddings)

        # Rate limiting (respect API limits)
        time.sleep(0.1)

    # 3. Assign embeddings to nodes
    for node, embedding in zip(all_nodes, embeddings):
        node.embedding = embedding

    return all_nodes
```

### Query Optimization

```python
"""
Optimize queries with metadata filtering and caching.
"""
from llama_index.core.vector_stores import MetadataFilters, MetadataFilter


def optimized_query(
    index,
    question: str,
    category: str = None,
    date_after: str = None,
    top_k: int = 10,
):
    """
    Query with metadata filters for faster retrieval.
    """
    filters = []

    if category:
        filters.append(MetadataFilter(key="category", value=category))

    if date_after:
        filters.append(MetadataFilter(
            key="date",
            value=date_after,
            operator=">=",
        ))

    metadata_filters = MetadataFilters(filters=filters) if filters else None

    query_engine = index.as_query_engine(
        similarity_top_k=top_k,
        filters=metadata_filters,
    )

    return query_engine.query(question)


# Usage
response = optimized_query(
    index,
    "What are the latest security updates?",
    category="security",
    date_after="2024-01-01",
    top_k=5,
)
```
