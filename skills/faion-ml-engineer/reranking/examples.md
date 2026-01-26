# Reranking Code Examples

Practical code examples for implementing reranking in RAG systems using various models and libraries.

---

## Table of Contents

- [Basic Reranking Examples](#basic-reranking-examples)
- [API-Based Reranking](#api-based-reranking)
- [Self-Hosted Models](#self-hosted-models)
- [RAG Pipeline Integration](#rag-pipeline-integration)
- [Advanced Patterns](#advanced-patterns)
- [Performance Optimization](#performance-optimization)

---

## Basic Reranking Examples

### Sentence Transformers Cross-Encoder

```python
"""
Basic cross-encoder reranking with sentence-transformers.
Fast setup, good for development and small-scale production.
"""
from sentence_transformers import CrossEncoder
import numpy as np
from typing import List, Dict, Any

# Available models (speed vs accuracy trade-off)
MODELS = {
    "fast": "cross-encoder/ms-marco-MiniLM-L-6-v2",     # 22M params
    "balanced": "cross-encoder/ms-marco-MiniLM-L-12-v2", # 33M params
    "accurate": "cross-encoder/ms-marco-electra-base",   # 110M params
    "multilingual": "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
}


class BasicReranker:
    """Simple reranker using sentence-transformers CrossEncoder."""

    def __init__(self, model_name: str = "balanced", device: str = None):
        model_path = MODELS.get(model_name, model_name)
        self.model = CrossEncoder(model_path, device=device)
        self.model_name = model_name

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
        return_scores: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents by relevance to query.

        Args:
            query: Search query
            documents: List of document texts
            top_k: Number of results to return
            return_scores: Include relevance scores

        Returns:
            List of dicts with document, score, and original index
        """
        if not documents:
            return []

        # Create query-document pairs
        pairs = [[query, doc] for doc in documents]

        # Get relevance scores
        scores = self.model.predict(pairs)

        # Sort by score descending
        sorted_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in sorted_indices:
            result = {
                "document": documents[idx],
                "original_index": int(idx)
            }
            if return_scores:
                result["score"] = float(scores[idx])
            results.append(result)

        return results


# Usage example
if __name__ == "__main__":
    reranker = BasicReranker(model_name="balanced")

    query = "What is the capital of France?"
    documents = [
        "Paris is the capital and largest city of France.",
        "France is a country in Western Europe.",
        "The Eiffel Tower is located in Paris, France.",
        "Berlin is the capital of Germany.",
        "French cuisine is world-renowned."
    ]

    results = reranker.rerank(query, documents, top_k=3)

    for i, r in enumerate(results):
        print(f"{i+1}. [Score: {r['score']:.4f}] {r['document'][:50]}...")
```

### Using AnswerDotAI Rerankers Library

```python
"""
Unified reranker interface using the rerankers library.
Supports multiple backends with consistent API.
"""
from rerankers import Reranker
from typing import List, Dict, Any, Optional


class UnifiedReranker:
    """
    Unified reranker supporting multiple backends:
    - cross-encoder (sentence-transformers)
    - colbert
    - flashrank
    - cohere
    - jina
    """

    SUPPORTED_MODELS = {
        # Cross-encoder models
        "cross-encoder/ms-marco-MiniLM-L-6-v2": "cross-encoder",
        "cross-encoder/ms-marco-MiniLM-L-12-v2": "cross-encoder",
        "BAAI/bge-reranker-v2-m3": "cross-encoder",
        "jinaai/jina-reranker-v2-base-multilingual": "cross-encoder",

        # FlashRank (lightweight)
        "ms-marco-MiniLM-L-12-v2": "flashrank",
        "ms-marco-MultiBERT-L-12": "flashrank",

        # ColBERT (late interaction)
        "colbert-ir/colbertv2.0": "colbert",

        # API-based
        "cohere": "api",
        "jina-reranker-v2-base-multilingual": "api"
    }

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-12-v2",
        api_key: Optional[str] = None
    ):
        self.model_name = model_name
        self.ranker = Reranker(model_name, api_key=api_key)

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
        doc_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents using the configured model.

        Args:
            query: Search query
            documents: List of document texts
            top_k: Number of top results
            doc_ids: Optional document IDs for tracking

        Returns:
            List of reranked results
        """
        # Handle empty input
        if not documents:
            return []

        # Rerank using the library
        results = self.ranker.rank(
            query=query,
            docs=documents,
            doc_ids=doc_ids
        )

        # Format output
        output = []
        for result in results.top_k(top_k):
            output.append({
                "document": result.document.text,
                "score": result.score,
                "original_index": result.document.doc_id or result.rank,
                "rank": result.rank
            })

        return output


# Usage with different models
if __name__ == "__main__":
    # Local cross-encoder
    local_reranker = UnifiedReranker("BAAI/bge-reranker-v2-m3")

    # FlashRank (lightweight)
    flash_reranker = UnifiedReranker("ms-marco-MiniLM-L-12-v2")

    query = "machine learning best practices"
    docs = [
        "Deep learning requires large datasets for training.",
        "Best practices for ML include cross-validation and regularization.",
        "Neural networks are a subset of machine learning.",
        "Always split your data into train, validation, and test sets.",
        "Python is popular for machine learning development."
    ]

    print("BGE Reranker results:")
    for r in local_reranker.rerank(query, docs, top_k=3):
        print(f"  [{r['score']:.3f}] {r['document'][:60]}")
```

---

## API-Based Reranking

### Cohere Rerank API

```python
"""
Production-ready Cohere reranking integration.
Supports both standard and Nimble models.
"""
import cohere
from typing import List, Dict, Any, Optional
import os
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass
class CohereConfig:
    api_key: str
    model: str = "rerank-english-v3.0"  # or "rerank-multilingual-v3.0", "rerank-english-v3.0-nimble"
    timeout: int = 30
    max_documents: int = 1000


class CohereReranker:
    """Production Cohere reranker with retry logic and error handling."""

    MODELS = {
        "english": "rerank-english-v3.0",
        "multilingual": "rerank-multilingual-v3.0",
        "english-nimble": "rerank-english-v3.0-nimble",  # Faster, slightly less accurate
        "multilingual-nimble": "rerank-multilingual-v3.0-nimble"
    }

    def __init__(self, config: Optional[CohereConfig] = None):
        self.config = config or CohereConfig(
            api_key=os.getenv("COHERE_API_KEY")
        )
        self.client = cohere.Client(
            api_key=self.config.api_key,
            timeout=self.config.timeout
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def rerank(
        self,
        query: str,
        documents: List[str],
        top_n: int = 5,
        return_documents: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents using Cohere API.

        Args:
            query: Search query
            documents: List of document texts
            top_n: Number of results to return
            return_documents: Include document text in response

        Returns:
            List of reranked results with scores
        """
        if not documents:
            return []

        # Truncate if too many documents
        docs_to_rank = documents[:self.config.max_documents]

        response = self.client.rerank(
            query=query,
            documents=docs_to_rank,
            top_n=top_n,
            model=self.config.model,
            return_documents=return_documents
        )

        results = []
        for r in response.results:
            result = {
                "score": r.relevance_score,
                "original_index": r.index
            }
            if return_documents:
                result["document"] = documents[r.index]
            results.append(result)

        return results

    def rerank_with_metadata(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        text_field: str = "content",
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents with metadata preservation.

        Args:
            query: Search query
            documents: List of dicts with text and metadata
            text_field: Key containing document text
            top_n: Number of results

        Returns:
            Reranked documents with original metadata
        """
        texts = [doc[text_field] for doc in documents]

        reranked = self.rerank(
            query=query,
            documents=texts,
            top_n=top_n,
            return_documents=False
        )

        results = []
        for r in reranked:
            original_doc = documents[r["original_index"]].copy()
            original_doc["rerank_score"] = r["score"]
            results.append(original_doc)

        return results


# Usage
if __name__ == "__main__":
    reranker = CohereReranker(CohereConfig(
        api_key=os.getenv("COHERE_API_KEY"),
        model="rerank-english-v3.0-nimble"  # Fast variant
    ))

    query = "How to handle errors in Python?"
    docs = [
        {"content": "Try-except blocks catch exceptions in Python.", "source": "doc1"},
        {"content": "Python is an interpreted language.", "source": "doc2"},
        {"content": "Error handling with try/except/finally is a best practice.", "source": "doc3"},
        {"content": "Lists and dictionaries are Python data structures.", "source": "doc4"}
    ]

    results = reranker.rerank_with_metadata(query, docs, top_n=2)
    for r in results:
        print(f"[{r['rerank_score']:.3f}] {r['content'][:50]}... (source: {r['source']})")
```

### Jina AI Reranker API

```python
"""
Jina AI Reranker API integration.
Supports Jina Reranker v2 and v3 models.
"""
import httpx
from typing import List, Dict, Any, Optional
import os
from dataclasses import dataclass


@dataclass
class JinaConfig:
    api_key: str
    model: str = "jina-reranker-v2-base-multilingual"
    base_url: str = "https://api.jina.ai/v1/rerank"
    timeout: int = 30


class JinaReranker:
    """Jina AI reranker with async support."""

    MODELS = {
        "v2-base": "jina-reranker-v2-base-multilingual",
        "v2-turbo": "jina-reranker-v2-turbo-multilingual",  # Faster
        "v3": "jina-reranker-v3"  # Latest, SOTA
    }

    def __init__(self, config: Optional[JinaConfig] = None):
        self.config = config or JinaConfig(
            api_key=os.getenv("JINA_API_KEY")
        )
        self.headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Synchronous reranking with Jina API.
        """
        payload = {
            "model": self.config.model,
            "query": query,
            "documents": documents,
            "top_n": top_n
        }

        with httpx.Client(timeout=self.config.timeout) as client:
            response = client.post(
                self.config.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()

        data = response.json()

        results = []
        for r in data.get("results", []):
            results.append({
                "document": documents[r["index"]],
                "score": r["relevance_score"],
                "original_index": r["index"]
            })

        return results

    async def arerank(
        self,
        query: str,
        documents: List[str],
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Async reranking with Jina API.
        """
        payload = {
            "model": self.config.model,
            "query": query,
            "documents": documents,
            "top_n": top_n
        }

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                self.config.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()

        data = response.json()

        results = []
        for r in data.get("results", []):
            results.append({
                "document": documents[r["index"]],
                "score": r["relevance_score"],
                "original_index": r["index"]
            })

        return results


# Usage
if __name__ == "__main__":
    reranker = JinaReranker(JinaConfig(
        api_key=os.getenv("JINA_API_KEY"),
        model="jina-reranker-v3"
    ))

    results = reranker.rerank(
        query="What is machine learning?",
        documents=[
            "Machine learning is a subset of AI.",
            "Deep learning uses neural networks.",
            "Supervised learning requires labeled data."
        ],
        top_n=2
    )

    for r in results:
        print(f"[{r['score']:.3f}] {r['document']}")
```

---

## Self-Hosted Models

### BGE Reranker with Hugging Face

```python
"""
Self-hosted BGE Reranker using Hugging Face Transformers.
Best open-source option for production.
"""
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import List, Dict, Any, Optional
import numpy as np


class BGEReranker:
    """
    BGE Reranker for self-hosted deployment.

    Models:
    - BAAI/bge-reranker-v2-m3: Multilingual, 568M params
    - BAAI/bge-reranker-large: English, larger
    - BAAI/bge-reranker-base: English, base
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-v2-m3",
        device: Optional[str] = None,
        max_length: int = 512
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.max_length = max_length

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

    @torch.no_grad()
    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
        batch_size: int = 32
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents using BGE model.

        Args:
            query: Search query
            documents: List of documents
            top_k: Number of results
            batch_size: Batch size for inference

        Returns:
            Reranked results with scores
        """
        if not documents:
            return []

        # Create pairs
        pairs = [[query, doc] for doc in documents]

        # Process in batches
        all_scores = []
        for i in range(0, len(pairs), batch_size):
            batch = pairs[i:i + batch_size]

            inputs = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt"
            ).to(self.device)

            outputs = self.model(**inputs)
            scores = outputs.logits.squeeze(-1).cpu().numpy()

            # Handle single document case
            if scores.ndim == 0:
                scores = np.array([scores])

            all_scores.extend(scores.tolist())

        # Sort by score
        scores_array = np.array(all_scores)
        sorted_indices = np.argsort(scores_array)[::-1][:top_k]

        results = []
        for idx in sorted_indices:
            results.append({
                "document": documents[idx],
                "score": float(scores_array[idx]),
                "original_index": int(idx)
            })

        return results

    def compute_scores(
        self,
        query: str,
        documents: List[str],
        batch_size: int = 32
    ) -> List[float]:
        """
        Compute relevance scores without sorting.
        Useful when combining with other signals.
        """
        pairs = [[query, doc] for doc in documents]
        all_scores = []

        with torch.no_grad():
            for i in range(0, len(pairs), batch_size):
                batch = pairs[i:i + batch_size]

                inputs = self.tokenizer(
                    batch,
                    padding=True,
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors="pt"
                ).to(self.device)

                outputs = self.model(**inputs)
                scores = outputs.logits.squeeze(-1).cpu().numpy()

                if scores.ndim == 0:
                    scores = np.array([scores])

                all_scores.extend(scores.tolist())

        return all_scores


# Usage with GPU optimization
if __name__ == "__main__":
    # Initialize with half precision for faster inference
    reranker = BGEReranker(
        model_name="BAAI/bge-reranker-v2-m3",
        device="cuda"  # or "cpu"
    )

    query = "How does photosynthesis work?"
    documents = [
        "Photosynthesis converts sunlight into chemical energy.",
        "Plants use chlorophyll to absorb light.",
        "Carbon dioxide and water are inputs to photosynthesis.",
        "Cellular respiration releases energy from glucose.",
        "Chloroplasts are the organelles where photosynthesis occurs."
    ]

    results = reranker.rerank(query, documents, top_k=3)

    for r in results:
        print(f"[{r['score']:.4f}] {r['document']}")
```

### FlashRank (Lightweight Reranking)

```python
"""
FlashRank: Ultra-lightweight reranking for resource-constrained environments.
Great for CPU-only deployment and edge devices.
"""
from flashrank import Ranker, RerankRequest
from typing import List, Dict, Any, Optional


class FlashReranker:
    """
    FlashRank reranker for minimal overhead.

    Models:
    - ms-marco-MiniLM-L-12-v2 (default, best quality)
    - ms-marco-TinyBERT-L-2-v2 (smallest)
    - rank-T5-flan (T5-based)
    """

    MODELS = {
        "default": "ms-marco-MiniLM-L-12-v2",
        "tiny": "ms-marco-TinyBERT-L-2-v2",
        "t5": "rank-T5-flan"
    }

    def __init__(
        self,
        model_name: str = "default",
        cache_dir: Optional[str] = None
    ):
        model = self.MODELS.get(model_name, model_name)
        self.ranker = Ranker(model_name=model, cache_dir=cache_dir)

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fast reranking with FlashRank.
        """
        if not documents:
            return []

        # Create passages in FlashRank format
        passages = [{"id": i, "text": doc} for i, doc in enumerate(documents)]

        # Create rerank request
        request = RerankRequest(query=query, passages=passages)

        # Get results
        results = self.ranker.rerank(request)

        # Format output
        output = []
        for r in results[:top_k]:
            output.append({
                "document": r["text"],
                "score": r["score"],
                "original_index": r["id"]
            })

        return output


# Usage
if __name__ == "__main__":
    # FlashRank is ~10x faster than sentence-transformers cross-encoders
    reranker = FlashReranker(model_name="default")

    results = reranker.rerank(
        query="Python async programming",
        documents=[
            "Asyncio provides infrastructure for writing async code.",
            "Python supports object-oriented programming.",
            "Coroutines are the building blocks of async Python.",
            "Threading is another concurrency approach in Python."
        ],
        top_k=2
    )

    for r in results:
        print(f"[{r['score']:.4f}] {r['document'][:50]}...")
```

---

## RAG Pipeline Integration

### LangChain Integration

```python
"""
Reranking integration with LangChain RAG pipeline.
"""
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from typing import List, Optional


class LangChainRerankingRAG:
    """RAG pipeline with reranking using LangChain."""

    def __init__(
        self,
        collection_name: str = "documents",
        reranker_model: str = "BAAI/bge-reranker-v2-m3",
        initial_k: int = 20,
        final_k: int = 5
    ):
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings()

        # Initialize vector store
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings
        )

        # Base retriever
        self.base_retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": initial_k}
        )

        # Cross-encoder reranker
        cross_encoder = HuggingFaceCrossEncoder(model_name=reranker_model)
        reranker = CrossEncoderReranker(
            model=cross_encoder,
            top_n=final_k
        )

        # Compression retriever with reranking
        self.retriever = ContextualCompressionRetriever(
            base_compressor=reranker,
            base_retriever=self.base_retriever
        )

        # LLM for generation
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def add_documents(self, texts: List[str], metadatas: Optional[List[dict]] = None):
        """Add documents to vector store."""
        self.vectorstore.add_texts(texts, metadatas=metadatas)

    def query(self, question: str) -> str:
        """Query with reranking."""
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True
        )

        result = qa_chain({"query": question})
        return result["result"]

    def retrieve(self, query: str) -> List[dict]:
        """Retrieve reranked documents without generation."""
        docs = self.retriever.get_relevant_documents(query)
        return [{"content": d.page_content, "metadata": d.metadata} for d in docs]


# Usage
if __name__ == "__main__":
    rag = LangChainRerankingRAG(
        initial_k=50,
        final_k=5
    )

    # Add documents
    rag.add_documents([
        "Python is a high-level programming language.",
        "Machine learning uses algorithms to learn from data.",
        "FastAPI is a modern Python web framework.",
        "Deep learning is a subset of machine learning.",
        "Django is a popular Python web framework."
    ])

    # Query with reranking
    answer = rag.query("What is a good Python web framework?")
    print(answer)
```

### LlamaIndex Integration

```python
"""
Reranking integration with LlamaIndex.
"""
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import Settings
from typing import Optional
import os


class LlamaIndexRerankingRAG:
    """RAG pipeline with reranking using LlamaIndex."""

    def __init__(
        self,
        reranker_type: str = "sentence-transformer",  # or "cohere"
        reranker_model: str = "BAAI/bge-reranker-v2-m3",
        initial_k: int = 20,
        final_k: int = 5
    ):
        self.initial_k = initial_k
        self.final_k = final_k
        self.index = None

        # Initialize reranker based on type
        if reranker_type == "sentence-transformer":
            self.reranker = SentenceTransformerRerank(
                model=reranker_model,
                top_n=final_k
            )
        elif reranker_type == "cohere":
            self.reranker = CohereRerank(
                api_key=os.getenv("COHERE_API_KEY"),
                top_n=final_k
            )
        else:
            raise ValueError(f"Unknown reranker type: {reranker_type}")

    def load_documents(self, directory: str):
        """Load documents from directory."""
        documents = SimpleDirectoryReader(directory).load_data()
        self.index = VectorStoreIndex.from_documents(documents)

    def create_index_from_texts(self, texts: list[str]):
        """Create index from text list."""
        from llama_index.core import Document
        documents = [Document(text=t) for t in texts]
        self.index = VectorStoreIndex.from_documents(documents)

    def query(self, question: str) -> str:
        """Query with reranking."""
        if self.index is None:
            raise ValueError("Index not initialized. Load documents first.")

        # Create retriever
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=self.initial_k
        )

        # Create query engine with reranking
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[self.reranker]
        )

        response = query_engine.query(question)
        return str(response)

    def retrieve(self, query: str) -> list[dict]:
        """Retrieve reranked documents."""
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=self.initial_k
        )

        nodes = retriever.retrieve(query)
        reranked = self.reranker.postprocess_nodes(nodes, query_str=query)

        return [
            {"content": n.node.get_content(), "score": n.score}
            for n in reranked
        ]


# Usage
if __name__ == "__main__":
    rag = LlamaIndexRerankingRAG(
        reranker_type="sentence-transformer",
        initial_k=20,
        final_k=5
    )

    rag.create_index_from_texts([
        "Python is a high-level programming language.",
        "JavaScript runs in web browsers.",
        "TypeScript adds types to JavaScript.",
        "Go is known for concurrency.",
        "Rust ensures memory safety."
    ])

    answer = rag.query("Which language is best for web development?")
    print(answer)
```

### Custom RAG Pipeline

```python
"""
Custom RAG pipeline with reranking.
Full control over each component.
"""
from typing import List, Dict, Any, Optional, Protocol
from dataclasses import dataclass
import numpy as np


class EmbeddingService(Protocol):
    """Protocol for embedding service."""
    def embed(self, text: str) -> np.ndarray: ...
    def embed_batch(self, texts: List[str]) -> np.ndarray: ...


class VectorStore(Protocol):
    """Protocol for vector store."""
    def search(self, embedding: np.ndarray, top_k: int, filter: Optional[Dict] = None) -> List[Dict]: ...


class Reranker(Protocol):
    """Protocol for reranker."""
    def rerank(self, query: str, documents: List[str], top_k: int) -> List[Dict]: ...


class LLMService(Protocol):
    """Protocol for LLM service."""
    def generate(self, prompt: str) -> str: ...


@dataclass
class RAGConfig:
    initial_top_k: int = 50
    rerank_top_k: int = 5
    use_reranking: bool = True
    use_diversity: bool = False
    diversity_lambda: float = 0.5


class CustomRerankingRAG:
    """
    Flexible RAG pipeline with configurable reranking.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        reranker: Optional[Reranker] = None,
        llm_service: Optional[LLMService] = None,
        config: Optional[RAGConfig] = None
    ):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.reranker = reranker
        self.llm_service = llm_service
        self.config = config or RAGConfig()

    def retrieve(
        self,
        query: str,
        filter: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Two-stage retrieval with optional reranking.
        """
        # Stage 1: Vector search
        query_embedding = self.embedding_service.embed(query)
        initial_results = self.vector_store.search(
            embedding=query_embedding,
            top_k=self.config.initial_top_k,
            filter=filter
        )

        # Extract documents for reranking
        documents = [r["content"] for r in initial_results]

        # Stage 2: Reranking (optional)
        if self.config.use_reranking and self.reranker and len(documents) > 0:
            reranked = self.reranker.rerank(
                query=query,
                documents=documents,
                top_k=self.config.rerank_top_k
            )

            # Map back to original results with metadata
            final_results = []
            for r in reranked:
                original_idx = r["original_index"]
                result = initial_results[original_idx].copy()
                result["rerank_score"] = r["score"]
                final_results.append(result)

            # Optional: Apply diversity selection
            if self.config.use_diversity:
                final_results = self._apply_diversity(
                    query, final_results, self.config.diversity_lambda
                )

            return final_results

        # No reranking - return top-k from initial retrieval
        return initial_results[:self.config.rerank_top_k]

    def query(
        self,
        question: str,
        filter: Optional[Dict] = None,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Full RAG query with retrieval, reranking, and generation.
        """
        # Retrieve relevant documents
        documents = self.retrieve(question, filter)

        # Build context from documents
        context = "\n\n".join([
            f"Document {i+1}:\n{doc['content']}"
            for i, doc in enumerate(documents)
        ])

        # Build prompt
        if system_prompt:
            prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        else:
            prompt = f"Based on the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"

        # Generate answer
        if self.llm_service:
            answer = self.llm_service.generate(prompt)
        else:
            answer = None

        return {
            "answer": answer,
            "sources": documents,
            "query": question
        }

    def _apply_diversity(
        self,
        query: str,
        results: List[Dict],
        lambda_param: float
    ) -> List[Dict]:
        """
        Apply Maximal Marginal Relevance for diversity.
        """
        if len(results) <= 1:
            return results

        # Get embeddings for diversity calculation
        query_emb = self.embedding_service.embed(query)
        doc_embs = self.embedding_service.embed_batch([r["content"] for r in results])

        # Normalize embeddings
        query_emb = query_emb / np.linalg.norm(query_emb)
        doc_embs = doc_embs / np.linalg.norm(doc_embs, axis=1, keepdims=True)

        # MMR selection
        selected = []
        remaining = list(range(len(results)))
        scores = np.array([r.get("rerank_score", 0.5) for r in results])

        while len(selected) < len(results) and remaining:
            mmr_scores = []

            for idx in remaining:
                relevance = scores[idx]

                if selected:
                    similarities = np.dot(doc_embs[selected], doc_embs[idx])
                    max_sim = np.max(similarities)
                else:
                    max_sim = 0

                mmr = lambda_param * relevance - (1 - lambda_param) * max_sim
                mmr_scores.append((idx, mmr))

            best_idx = max(mmr_scores, key=lambda x: x[1])[0]
            selected.append(best_idx)
            remaining.remove(best_idx)

        return [results[i] for i in selected]


# Usage with concrete implementations
if __name__ == "__main__":
    from sentence_transformers import CrossEncoder, SentenceTransformer

    # Concrete embedding service
    class SentenceTransformerEmbedding:
        def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
            self.model = SentenceTransformer(model_name)

        def embed(self, text: str) -> np.ndarray:
            return self.model.encode(text)

        def embed_batch(self, texts: List[str]) -> np.ndarray:
            return self.model.encode(texts)

    # Concrete reranker
    class CrossEncoderReranker:
        def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"):
            self.model = CrossEncoder(model_name)

        def rerank(self, query: str, documents: List[str], top_k: int) -> List[Dict]:
            pairs = [[query, doc] for doc in documents]
            scores = self.model.predict(pairs)
            sorted_indices = np.argsort(scores)[::-1][:top_k]
            return [
                {"document": documents[i], "score": float(scores[i]), "original_index": i}
                for i in sorted_indices
            ]

    # Example with in-memory vector store
    class SimpleVectorStore:
        def __init__(self, embedding_service):
            self.embedding_service = embedding_service
            self.documents = []
            self.embeddings = None

        def add(self, texts: List[str]):
            self.documents.extend(texts)
            new_embs = self.embedding_service.embed_batch(texts)
            if self.embeddings is None:
                self.embeddings = new_embs
            else:
                self.embeddings = np.vstack([self.embeddings, new_embs])

        def search(self, embedding: np.ndarray, top_k: int, filter: Optional[Dict] = None) -> List[Dict]:
            if self.embeddings is None:
                return []

            similarities = np.dot(self.embeddings, embedding)
            top_indices = np.argsort(similarities)[::-1][:top_k]

            return [
                {"content": self.documents[i], "score": float(similarities[i])}
                for i in top_indices
            ]

    # Build pipeline
    embedding_service = SentenceTransformerEmbedding()
    vector_store = SimpleVectorStore(embedding_service)
    reranker = CrossEncoderReranker()

    rag = CustomRerankingRAG(
        vector_store=vector_store,
        embedding_service=embedding_service,
        reranker=reranker,
        config=RAGConfig(initial_top_k=10, rerank_top_k=3)
    )

    # Add documents
    vector_store.add([
        "Python is great for data science.",
        "JavaScript powers the web.",
        "Machine learning uses Python extensively.",
        "React is a JavaScript library.",
        "Scikit-learn is a Python ML library."
    ])

    # Retrieve with reranking
    results = rag.retrieve("Best language for machine learning?")
    for r in results:
        print(f"[{r.get('rerank_score', r.get('score')):.3f}] {r['content']}")
```

---

## Advanced Patterns

### Multi-Stage Reranking

```python
"""
Multi-stage reranking: fast filter -> accurate rerank.
Handles large candidate pools efficiently.
"""
from typing import List, Dict, Any
from sentence_transformers import CrossEncoder
import numpy as np


class MultiStageReranker:
    """
    Two-stage reranking pipeline:
    1. Light reranker for coarse filtering (fast)
    2. Heavy reranker for fine ranking (accurate)
    """

    def __init__(
        self,
        light_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        heavy_model: str = "BAAI/bge-reranker-v2-m3",
        device: str = None
    ):
        self.light_reranker = CrossEncoder(light_model, device=device)
        self.heavy_reranker = CrossEncoder(heavy_model, device=device)

    def rerank(
        self,
        query: str,
        documents: List[str],
        intermediate_k: int = 20,
        final_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Multi-stage reranking.

        Stage 1: Light reranker reduces 100+ docs to 20
        Stage 2: Heavy reranker refines 20 docs to 5
        """
        if len(documents) <= final_k:
            # Skip multi-stage for small sets
            return self._single_stage_rerank(
                query, documents, final_k, self.heavy_reranker
            )

        # Stage 1: Light reranking
        pairs = [[query, doc] for doc in documents]
        light_scores = self.light_reranker.predict(pairs)

        # Get top intermediate_k indices
        intermediate_indices = np.argsort(light_scores)[::-1][:intermediate_k]
        intermediate_docs = [documents[i] for i in intermediate_indices]

        # Stage 2: Heavy reranking on reduced set
        heavy_pairs = [[query, doc] for doc in intermediate_docs]
        heavy_scores = self.heavy_reranker.predict(heavy_pairs)

        # Get final top_k
        final_local_indices = np.argsort(heavy_scores)[::-1][:final_k]

        results = []
        for local_idx in final_local_indices:
            global_idx = intermediate_indices[local_idx]
            results.append({
                "document": documents[global_idx],
                "score": float(heavy_scores[local_idx]),
                "light_score": float(light_scores[global_idx]),
                "original_index": int(global_idx)
            })

        return results

    def _single_stage_rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int,
        reranker: CrossEncoder
    ) -> List[Dict[str, Any]]:
        pairs = [[query, doc] for doc in documents]
        scores = reranker.predict(pairs)
        sorted_indices = np.argsort(scores)[::-1][:top_k]

        return [
            {
                "document": documents[i],
                "score": float(scores[i]),
                "original_index": i
            }
            for i in sorted_indices
        ]


# Usage
if __name__ == "__main__":
    reranker = MultiStageReranker()

    # Simulate 100 retrieved documents
    docs = [f"Document {i} about various topics" for i in range(100)]
    docs[42] = "This document is highly relevant to the query"
    docs[87] = "Another relevant document with important information"

    results = reranker.rerank(
        query="Find relevant information",
        documents=docs,
        intermediate_k=20,
        final_k=5
    )

    print("Multi-stage reranking results:")
    for r in results:
        print(f"[Heavy: {r['score']:.3f}, Light: {r['light_score']:.3f}] "
              f"{r['document'][:50]}...")
```

### Hybrid Fusion with Reranking

```python
"""
Hybrid search with RRF fusion and reranking.
Combines BM25 and dense retrieval before reranking.
"""
from typing import List, Dict, Any, Optional
import numpy as np


def reciprocal_rank_fusion(
    rankings: List[List[int]],
    k: int = 60
) -> List[tuple[int, float]]:
    """
    Reciprocal Rank Fusion for combining multiple rankings.

    Args:
        rankings: List of ranked doc indices from different retrievers
        k: RRF constant (default 60)

    Returns:
        Fused ranking as (doc_id, score) tuples
    """
    scores = {}

    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += 1 / (k + rank + 1)

    # Sort by fused score
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs


class HybridRerankingPipeline:
    """
    Hybrid retrieval with RRF fusion and reranking.
    """

    def __init__(
        self,
        bm25_retriever,  # BM25 or sparse retriever
        dense_retriever,  # Dense/vector retriever
        reranker,         # Cross-encoder reranker
        rrf_k: int = 60
    ):
        self.bm25 = bm25_retriever
        self.dense = dense_retriever
        self.reranker = reranker
        self.rrf_k = rrf_k

    def retrieve(
        self,
        query: str,
        documents: List[str],
        initial_k: int = 100,
        fusion_k: int = 50,
        final_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Three-stage retrieval:
        1. BM25 and dense retrieval in parallel
        2. RRF fusion to combine rankings
        3. Cross-encoder reranking for final results
        """
        # Stage 1a: BM25 retrieval
        bm25_results = self.bm25.search(query, documents, top_k=initial_k)
        bm25_ranking = [r["index"] for r in bm25_results]

        # Stage 1b: Dense retrieval
        dense_results = self.dense.search(query, documents, top_k=initial_k)
        dense_ranking = [r["index"] for r in dense_results]

        # Stage 2: RRF fusion
        fused = reciprocal_rank_fusion(
            [bm25_ranking, dense_ranking],
            k=self.rrf_k
        )

        # Get top fusion_k docs for reranking
        fusion_indices = [doc_id for doc_id, _ in fused[:fusion_k]]
        fusion_docs = [documents[i] for i in fusion_indices]

        # Stage 3: Reranking
        reranked = self.reranker.rerank(
            query=query,
            documents=fusion_docs,
            top_k=final_k
        )

        # Map back to global indices
        results = []
        for r in reranked:
            local_idx = r["original_index"]
            global_idx = fusion_indices[local_idx]

            results.append({
                "document": documents[global_idx],
                "rerank_score": r["score"],
                "rrf_score": fused[local_idx][1],
                "original_index": global_idx
            })

        return results


# Example BM25 implementation
class SimpleBM25:
    """Simple BM25 implementation for demonstration."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b

    def search(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10
    ) -> List[Dict]:
        from collections import Counter
        import math

        # Tokenize
        query_terms = query.lower().split()
        doc_terms = [doc.lower().split() for doc in documents]

        # Calculate IDF
        N = len(documents)
        df = Counter()
        for terms in doc_terms:
            for term in set(terms):
                df[term] += 1

        idf = {term: math.log((N - freq + 0.5) / (freq + 0.5) + 1)
               for term, freq in df.items()}

        # Calculate average document length
        avgdl = sum(len(terms) for terms in doc_terms) / N

        # Score documents
        scores = []
        for idx, terms in enumerate(doc_terms):
            tf = Counter(terms)
            dl = len(terms)

            score = 0
            for term in query_terms:
                if term in tf:
                    term_freq = tf[term]
                    score += (idf.get(term, 0) * term_freq * (self.k1 + 1)) / \
                             (term_freq + self.k1 * (1 - self.b + self.b * dl / avgdl))

            scores.append({"index": idx, "score": score})

        # Sort by score
        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]
```

### LLM-Based Reranking

```python
"""
LLM-based reranking for complex reasoning queries.
Uses LLM to score relevance with explanations.
"""
from typing import List, Dict, Any, Optional
from openai import OpenAI
import json


class LLMReranker:
    """
    LLM-based reranker using GPT-4 or similar models.
    Best for complex queries requiring reasoning.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None
    ):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
        explain: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Rerank using LLM scoring.

        Args:
            query: Search query
            documents: List of documents
            top_k: Number of results
            explain: Include explanation for scores

        Returns:
            Reranked results with LLM scores
        """
        if not documents:
            return []

        # Build prompt for scoring
        docs_text = "\n".join([
            f"[{i}] {doc[:500]}"  # Truncate long docs
            for i, doc in enumerate(documents)
        ])

        if explain:
            prompt = self._build_explain_prompt(query, docs_text, top_k)
        else:
            prompt = self._build_score_prompt(query, docs_text, top_k)

        # Call LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a document relevance expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        # Parse response
        result = json.loads(response.choices[0].message.content)

        # Format output
        rankings = result.get("rankings", [])
        output = []
        for r in rankings[:top_k]:
            idx = r["index"]
            output.append({
                "document": documents[idx],
                "score": r["score"],
                "original_index": idx,
                "explanation": r.get("explanation", "") if explain else None
            })

        return output

    def _build_score_prompt(self, query: str, docs_text: str, top_k: int) -> str:
        return f"""Rate the relevance of each document to the query on a scale of 0-10.

Query: {query}

Documents:
{docs_text}

Return a JSON object with this structure:
{{
  "rankings": [
    {{"index": 0, "score": 8.5}},
    {{"index": 1, "score": 3.2}},
    ...
  ]
}}

Sort by score descending. Include top {top_k} most relevant documents."""

    def _build_explain_prompt(self, query: str, docs_text: str, top_k: int) -> str:
        return f"""Rate the relevance of each document to the query on a scale of 0-10.
Explain why each document is or isn't relevant.

Query: {query}

Documents:
{docs_text}

Return a JSON object with this structure:
{{
  "rankings": [
    {{"index": 0, "score": 8.5, "explanation": "Directly answers the question about..."}},
    {{"index": 1, "score": 3.2, "explanation": "Mentions related topic but..."}},
    ...
  ]
}}

Sort by score descending. Include top {top_k} most relevant documents."""


# Listwise LLM reranking (more efficient for many docs)
class ListwiseLLMReranker:
    """
    Listwise LLM reranker - compares all docs at once.
    More token-efficient than pointwise scoring.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None
    ):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Listwise reranking - returns ordered list of indices.
        """
        if not documents:
            return []

        # Build document list
        docs_text = "\n".join([
            f"[{i}] {doc[:300]}"
            for i, doc in enumerate(documents)
        ])

        prompt = f"""Given the query, rank the following documents by relevance.
Return ONLY a JSON object with the indices of the {top_k} most relevant documents in order.

Query: {query}

Documents:
{docs_text}

Return format:
{{"ranking": [2, 0, 4, 1, 3]}}

The first index is most relevant, last is least relevant."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        ranking = result.get("ranking", [])[:top_k]

        return [
            {
                "document": documents[idx],
                "rank": rank + 1,
                "original_index": idx
            }
            for rank, idx in enumerate(ranking)
        ]


# Usage
if __name__ == "__main__":
    reranker = LLMReranker(model="gpt-4o-mini")

    results = reranker.rerank(
        query="What are the benefits of exercise?",
        documents=[
            "Regular exercise improves cardiovascular health.",
            "Python is a programming language.",
            "Physical activity reduces stress and anxiety.",
            "Exercise helps with weight management.",
            "The weather is nice today."
        ],
        top_k=3,
        explain=True
    )

    for r in results:
        print(f"[{r['score']:.1f}] {r['document'][:50]}")
        if r['explanation']:
            print(f"    Reason: {r['explanation']}")
```

---

## Performance Optimization

### Batch Processing

```python
"""
Optimized batch reranking for high-throughput scenarios.
"""
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from sentence_transformers import CrossEncoder
import numpy as np
import time


class BatchOptimizedReranker:
    """
    Batch-optimized reranker with parallel processing.
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-12-v2",
        batch_size: int = 32,
        max_workers: int = 4
    ):
        self.model = CrossEncoder(model_name)
        self.batch_size = batch_size
        self.max_workers = max_workers

    def rerank_single(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Single query reranking with optimal batching."""
        pairs = [[query, doc] for doc in documents]

        # Process in batches for optimal GPU utilization
        all_scores = []
        for i in range(0, len(pairs), self.batch_size):
            batch = pairs[i:i + self.batch_size]
            scores = self.model.predict(batch)
            if scores.ndim == 0:
                scores = np.array([scores])
            all_scores.extend(scores.tolist())

        scores_array = np.array(all_scores)
        sorted_indices = np.argsort(scores_array)[::-1][:top_k]

        return [
            {
                "document": documents[i],
                "score": float(scores_array[i]),
                "original_index": i
            }
            for i in sorted_indices
        ]

    def rerank_batch(
        self,
        queries: List[str],
        document_lists: List[List[str]],
        top_k: int = 5
    ) -> List[List[Dict[str, Any]]]:
        """
        Batch reranking for multiple queries.
        Uses thread pool for I/O-bound API calls.
        """
        results = [None] * len(queries)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.rerank_single, q, docs, top_k): i
                for i, (q, docs) in enumerate(zip(queries, document_lists))
            }

            for future in as_completed(futures):
                idx = futures[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    results[idx] = [{"error": str(e)}]

        return results


class CachedReranker:
    """
    Reranker with result caching for repeated queries.
    """

    def __init__(
        self,
        reranker,
        cache_size: int = 1000,
        ttl_seconds: int = 3600
    ):
        self.reranker = reranker
        self.cache = {}
        self.cache_timestamps = {}
        self.cache_size = cache_size
        self.ttl_seconds = ttl_seconds

    def _cache_key(self, query: str, documents: Tuple[str, ...], top_k: int) -> str:
        """Generate cache key from query and docs."""
        import hashlib
        doc_hash = hashlib.md5(str(documents).encode()).hexdigest()
        return f"{query}:{doc_hash}:{top_k}"

    def _evict_expired(self):
        """Remove expired cache entries."""
        current_time = time.time()
        expired = [
            key for key, ts in self.cache_timestamps.items()
            if current_time - ts > self.ttl_seconds
        ]
        for key in expired:
            del self.cache[key]
            del self.cache_timestamps[key]

    def _evict_oldest(self):
        """Remove oldest entries if cache is full."""
        while len(self.cache) >= self.cache_size:
            oldest_key = min(self.cache_timestamps, key=self.cache_timestamps.get)
            del self.cache[oldest_key]
            del self.cache_timestamps[oldest_key]

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Rerank with caching."""
        # Create cache key
        docs_tuple = tuple(documents)
        cache_key = self._cache_key(query, docs_tuple, top_k)

        # Check cache
        if cache_key in self.cache:
            if time.time() - self.cache_timestamps[cache_key] < self.ttl_seconds:
                return self.cache[cache_key]

        # Evict expired and oldest
        self._evict_expired()
        self._evict_oldest()

        # Compute result
        result = self.reranker.rerank(query, documents, top_k)

        # Cache result
        self.cache[cache_key] = result
        self.cache_timestamps[cache_key] = time.time()

        return result


# Async reranking for API-based services
import asyncio
import httpx


class AsyncAPIReranker:
    """
    Async reranker for API-based services.
    Maximizes throughput for concurrent requests.
    """

    def __init__(
        self,
        api_url: str,
        api_key: str,
        max_concurrent: int = 10
    ):
        self.api_url = api_url
        self.api_key = api_key
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def rerank_single(
        self,
        client: httpx.AsyncClient,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Single async rerank call."""
        async with self.semaphore:
            response = await client.post(
                self.api_url,
                json={
                    "query": query,
                    "documents": documents,
                    "top_n": top_k
                },
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return response.json()["results"]

    async def rerank_batch(
        self,
        queries: List[str],
        document_lists: List[List[str]],
        top_k: int = 5
    ) -> List[List[Dict[str, Any]]]:
        """Batch async reranking."""
        async with httpx.AsyncClient() as client:
            tasks = [
                self.rerank_single(client, q, docs, top_k)
                for q, docs in zip(queries, document_lists)
            ]
            return await asyncio.gather(*tasks, return_exceptions=True)


# Usage
if __name__ == "__main__":
    # Batch processing
    batch_reranker = BatchOptimizedReranker(batch_size=32, max_workers=4)

    queries = ["query 1", "query 2", "query 3"]
    doc_lists = [
        ["doc a", "doc b", "doc c"],
        ["doc d", "doc e", "doc f"],
        ["doc g", "doc h", "doc i"]
    ]

    results = batch_reranker.rerank_batch(queries, doc_lists, top_k=2)

    for i, query_results in enumerate(results):
        print(f"Query {i+1}: {queries[i]}")
        for r in query_results:
            print(f"  [{r.get('score', 'N/A')}] {r.get('document', r)[:30]}")
```

### GPU Optimization

```python
"""
GPU-optimized reranking with mixed precision and batching.
"""
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import List, Dict, Any, Optional
import numpy as np


class GPUOptimizedReranker:
    """
    GPU-optimized reranker with:
    - Half precision (FP16) inference
    - Optimal batch sizing
    - CUDA graph optimization
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-v2-m3",
        device: str = "cuda",
        use_fp16: bool = True,
        max_length: int = 512,
        optimal_batch_size: int = 32
    ):
        self.device = device
        self.max_length = max_length
        self.optimal_batch_size = optimal_batch_size

        # Load model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

        # Move to device
        self.model.to(device)

        # Enable half precision
        if use_fp16 and device == "cuda":
            self.model = self.model.half()

        # Set eval mode
        self.model.eval()

        # Warm up
        self._warmup()

    def _warmup(self):
        """Warm up GPU with dummy inference."""
        dummy_input = self.tokenizer(
            [["query", "document"]],
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            _ = self.model(**dummy_input)

    @torch.inference_mode()
    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        GPU-optimized reranking.
        """
        if not documents:
            return []

        pairs = [[query, doc] for doc in documents]
        all_scores = []

        # Process in optimal batches
        for i in range(0, len(pairs), self.optimal_batch_size):
            batch = pairs[i:i + self.optimal_batch_size]

            inputs = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt"
            ).to(self.device)

            outputs = self.model(**inputs)
            scores = outputs.logits.squeeze(-1).cpu().numpy()

            if scores.ndim == 0:
                scores = np.array([scores])

            all_scores.extend(scores.tolist())

        # Sort and return
        scores_array = np.array(all_scores)
        sorted_indices = np.argsort(scores_array)[::-1][:top_k]

        return [
            {
                "document": documents[i],
                "score": float(scores_array[i]),
                "original_index": int(i)
            }
            for i in sorted_indices
        ]

    def find_optimal_batch_size(
        self,
        sample_query: str,
        sample_doc_length: int = 200
    ) -> int:
        """
        Find optimal batch size for current GPU.
        """
        sample_doc = "a " * sample_doc_length

        for batch_size in [8, 16, 32, 64, 128, 256]:
            try:
                pairs = [[sample_query, sample_doc]] * batch_size
                inputs = self.tokenizer(
                    pairs,
                    padding=True,
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors="pt"
                ).to(self.device)

                with torch.no_grad():
                    _ = self.model(**inputs)

                optimal = batch_size
            except RuntimeError:  # Out of memory
                break

        return optimal


# Usage
if __name__ == "__main__":
    if torch.cuda.is_available():
        reranker = GPUOptimizedReranker(
            model_name="BAAI/bge-reranker-v2-m3",
            device="cuda",
            use_fp16=True
        )

        # Find optimal batch size
        optimal = reranker.find_optimal_batch_size("test query")
        print(f"Optimal batch size: {optimal}")

        # Benchmark
        import time
        docs = ["Sample document " * 50] * 100

        start = time.time()
        results = reranker.rerank("test query", docs, top_k=10)
        elapsed = time.time() - start

        print(f"Reranked 100 docs in {elapsed:.3f}s ({100/elapsed:.1f} docs/sec)")
    else:
        print("CUDA not available")
```
