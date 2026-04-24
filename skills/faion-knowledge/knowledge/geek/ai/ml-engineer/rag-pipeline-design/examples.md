# RAG Pipeline Examples

Production-ready code examples for RAG systems.

---

## 1. Core Data Structures

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import hashlib

class ChunkingStrategy(Enum):
    FIXED = "fixed"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"
    PARAGRAPH = "paragraph"
    MARKDOWN_HEADER = "markdown_header"


@dataclass
class Document:
    """Source document with metadata."""
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(self.content.encode()).hexdigest()[:12]


@dataclass
class Chunk:
    """Document chunk with embedding."""
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    id: Optional[str] = None

    @property
    def token_count(self) -> int:
        # Rough estimate: 4 chars per token
        return len(self.content) // 4


@dataclass
class RetrievalResult:
    """Single retrieval result with score."""
    chunk: Chunk
    score: float

    def to_context(self, max_length: int = 500) -> str:
        """Format for LLM context."""
        source = self.chunk.metadata.get("source", "unknown")
        content = self.chunk.content[:max_length]
        return f"[Source: {source}]\n{content}"


@dataclass
class RAGResponse:
    """Complete RAG response with provenance."""
    query: str
    answer: str
    sources: List[RetrievalResult]
    latency_ms: float
    tokens_used: int = 0
```

---

## 2. Document Loaders

```python
from pathlib import Path
from typing import List
import json

class DocumentLoader:
    """Multi-format document loader."""

    @staticmethod
    def load_text(file_path: str) -> Document:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return Document(
            content=content,
            metadata={"source": file_path, "type": "text"},
            id=Path(file_path).stem
        )

    @staticmethod
    def load_pdf(file_path: str) -> Document:
        import pypdf

        reader = pypdf.PdfReader(file_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append(f"[Page {i+1}]\n{text}")

        return Document(
            content="\n\n".join(pages),
            metadata={
                "source": file_path,
                "type": "pdf",
                "pages": len(reader.pages)
            },
            id=Path(file_path).stem
        )

    @staticmethod
    def load_markdown(file_path: str) -> Document:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract title from first H1
        title = ""
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break

        return Document(
            content=content,
            metadata={"source": file_path, "type": "markdown", "title": title},
            id=Path(file_path).stem
        )

    @staticmethod
    def load_directory(
        directory: str,
        extensions: List[str] = [".txt", ".md", ".pdf"]
    ) -> List[Document]:
        documents = []
        dir_path = Path(directory)

        loaders = {
            ".txt": DocumentLoader.load_text,
            ".md": DocumentLoader.load_markdown,
            ".pdf": DocumentLoader.load_pdf,
        }

        for ext in extensions:
            loader = loaders.get(ext)
            if not loader:
                continue
            for file_path in dir_path.rglob(f"*{ext}"):
                try:
                    documents.append(loader(str(file_path)))
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")

        return documents
```

---

## 3. Chunking Strategies

```python
from typing import List, Callable
import re

class Chunker:
    """Multiple chunking strategies."""

    @staticmethod
    def fixed_size(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[str]:
        """Fixed character count with overlap."""
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]

            # Try to end at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                if last_period > chunk_size * 0.5:
                    chunk = chunk[:last_period + 1]
                    end = start + last_period + 1

            chunks.append(chunk.strip())
            start = end - overlap

        return [c for c in chunks if c]

    @staticmethod
    def recursive_character(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50,
        separators: List[str] = ["\n\n", "\n", ". ", " ", ""]
    ) -> List[str]:
        """LangChain-style recursive splitting."""

        def split_text(text: str, separators: List[str]) -> List[str]:
            if not separators:
                return [text]

            sep = separators[0]
            rest = separators[1:]

            if sep:
                splits = text.split(sep)
            else:
                splits = list(text)

            chunks = []
            current = ""

            for split in splits:
                piece = split + sep if sep else split
                if len(current) + len(piece) <= chunk_size:
                    current += piece
                else:
                    if current:
                        chunks.append(current.strip())
                    if len(piece) > chunk_size:
                        chunks.extend(split_text(piece, rest))
                        current = ""
                    else:
                        current = piece

            if current:
                chunks.append(current.strip())

            return chunks

        # Add overlap
        raw_chunks = split_text(text, separators)
        if overlap == 0:
            return raw_chunks

        overlapped = []
        for i, chunk in enumerate(raw_chunks):
            if i > 0 and len(raw_chunks[i-1]) > overlap:
                chunk = raw_chunks[i-1][-overlap:] + chunk
            overlapped.append(chunk)

        return overlapped

    @staticmethod
    def semantic(
        text: str,
        embedding_func: Callable[[str], List[float]],
        similarity_threshold: float = 0.75,
        min_chunk_size: int = 100
    ) -> List[str]:
        """Chunk based on semantic similarity between sentences."""
        import numpy as np

        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) < 2:
            return [text]

        # Get embeddings
        embeddings = [embedding_func(s) for s in sentences]

        # Group by similarity
        chunks = []
        current_chunk = [sentences[0]]

        for i in range(1, len(sentences)):
            # Cosine similarity
            sim = np.dot(embeddings[i], embeddings[i-1]) / (
                np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i-1]) + 1e-8
            )

            if sim >= similarity_threshold:
                current_chunk.append(sentences[i])
            else:
                chunk_text = " ".join(current_chunk)
                if len(chunk_text) >= min_chunk_size:
                    chunks.append(chunk_text)
                current_chunk = [sentences[i]]

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    @staticmethod
    def markdown_header(text: str) -> List[str]:
        """Chunk by markdown headers."""
        pattern = r'^(#{1,6})\s+(.+)$'
        lines = text.split('\n')

        chunks = []
        current_chunk = []
        current_header = ""

        for line in lines:
            header_match = re.match(pattern, line)
            if header_match:
                # Save previous chunk
                if current_chunk:
                    content = '\n'.join(current_chunk).strip()
                    if content:
                        chunks.append(f"{current_header}\n\n{content}" if current_header else content)
                current_header = line
                current_chunk = []
            else:
                current_chunk.append(line)

        # Save last chunk
        if current_chunk:
            content = '\n'.join(current_chunk).strip()
            if content:
                chunks.append(f"{current_header}\n\n{content}" if current_header else content)

        return chunks
```

---

## 4. Embedding Service

```python
from typing import List
from functools import lru_cache
import os

class EmbeddingService:
    """Unified embedding interface with caching."""

    def __init__(
        self,
        provider: str = "openai",
        model: str = "text-embedding-3-small",
        cache_size: int = 10000
    ):
        self.provider = provider
        self.model = model
        self._client = None

        # Configure caching
        self.embed_text = lru_cache(maxsize=cache_size)(self._embed_text_impl)

    @property
    def client(self):
        if self._client is None:
            if self.provider == "openai":
                from openai import OpenAI
                self._client = OpenAI()
            elif self.provider == "voyageai":
                import voyageai
                self._client = voyageai.Client()
            elif self.provider == "cohere":
                import cohere
                self._client = cohere.Client()
        return self._client

    @property
    def dimensions(self) -> int:
        dims = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "voyage-3-large": 1024,
            "embed-english-v3.0": 1024,
        }
        return dims.get(self.model, 1536)

    def _embed_text_impl(self, text: str) -> tuple:
        """Actual embedding call (cached via decorator)."""
        if self.provider == "openai":
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return tuple(response.data[0].embedding)

        elif self.provider == "voyageai":
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type="document"
            )
            return tuple(response.embeddings[0])

        elif self.provider == "cohere":
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type="search_document"
            )
            return tuple(response.embeddings[0])

        raise ValueError(f"Unknown provider: {self.provider}")

    def embed(self, text: str) -> List[float]:
        """Embed single text with caching."""
        return list(self.embed_text(text))

    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Embed multiple texts efficiently."""
        embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            if self.provider == "openai":
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.model
                )
                embeddings.extend([d.embedding for d in response.data])
            else:
                # Fallback to individual calls for other providers
                embeddings.extend([self.embed(t) for t in batch])

        return embeddings
```

---

## 5. Vector Store Abstraction

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import uuid

class VectorStore(ABC):
    """Abstract vector store interface."""

    @abstractmethod
    def upsert(self, chunks: List[Chunk]) -> int:
        """Insert or update chunks."""
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        filter: Optional[Dict] = None
    ) -> List[RetrievalResult]:
        """Search for similar chunks."""
        pass

    @abstractmethod
    def delete(self, ids: List[str]) -> int:
        """Delete chunks by ID."""
        pass


class ChromaVectorStore(VectorStore):
    """Chroma implementation for local development."""

    def __init__(self, collection_name: str = "documents", persist_dir: str = "./chroma_db"):
        import chromadb
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def upsert(self, chunks: List[Chunk]) -> int:
        ids = [c.id or str(uuid.uuid4()) for c in chunks]
        self.collection.upsert(
            ids=ids,
            embeddings=[c.embedding for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[c.metadata for c in chunks]
        )
        return len(chunks)

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        filter: Optional[Dict] = None
    ) -> List[RetrievalResult]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter,
            include=["documents", "metadatas", "distances"]
        )

        retrieval_results = []
        for i in range(len(results["ids"][0])):
            chunk = Chunk(
                id=results["ids"][0][i],
                content=results["documents"][0][i],
                metadata=results["metadatas"][0][i]
            )
            score = 1 - results["distances"][0][i]  # Convert distance to similarity
            retrieval_results.append(RetrievalResult(chunk=chunk, score=score))

        return retrieval_results

    def delete(self, ids: List[str]) -> int:
        self.collection.delete(ids=ids)
        return len(ids)


class QdrantVectorStore(VectorStore):
    """Qdrant implementation for production."""

    def __init__(
        self,
        collection_name: str = "documents",
        url: str = "http://localhost:6333",
        vector_size: int = 1536
    ):
        from qdrant_client import QdrantClient
        from qdrant_client.models import VectorParams, Distance

        self.client = QdrantClient(url=url)
        self.collection_name = collection_name

        # Create collection if not exists
        collections = [c.name for c in self.client.get_collections().collections]
        if collection_name not in collections:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

    def upsert(self, chunks: List[Chunk]) -> int:
        from qdrant_client.models import PointStruct

        points = [
            PointStruct(
                id=c.id or str(uuid.uuid4()),
                vector=c.embedding,
                payload={"content": c.content, **c.metadata}
            )
            for c in chunks
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        return len(points)

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        filter: Optional[Dict] = None
    ) -> List[RetrievalResult]:
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        qdrant_filter = None
        if filter:
            conditions = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filter.items()
            ]
            qdrant_filter = Filter(must=conditions)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=qdrant_filter
        )

        return [
            RetrievalResult(
                chunk=Chunk(
                    id=str(r.id),
                    content=r.payload.get("content", ""),
                    metadata={k: v for k, v in r.payload.items() if k != "content"}
                ),
                score=r.score
            )
            for r in results
        ]

    def delete(self, ids: List[str]) -> int:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=ids
        )
        return len(ids)
```

---

## 6. Complete RAG Pipeline

```python
import time
from typing import Optional, Dict, List

class RAGPipeline:
    """Production RAG pipeline with all components."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        llm_model: str = "gpt-4o",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 5
    ):
        from openai import OpenAI

        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.llm_client = OpenAI()
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k

    # ==================== INDEXING ====================

    def ingest(
        self,
        documents: List[Document],
        chunking_strategy: str = "recursive"
    ) -> int:
        """Ingest documents into the pipeline."""
        total_chunks = 0

        for doc in documents:
            # Chunk
            if chunking_strategy == "recursive":
                texts = Chunker.recursive_character(
                    doc.content,
                    self.chunk_size,
                    self.chunk_overlap
                )
            elif chunking_strategy == "markdown":
                texts = Chunker.markdown_header(doc.content)
            else:
                texts = Chunker.fixed_size(
                    doc.content,
                    self.chunk_size,
                    self.chunk_overlap
                )

            # Create chunks with metadata
            chunks = [
                Chunk(
                    content=text,
                    metadata={
                        **doc.metadata,
                        "chunk_index": i,
                        "source_id": doc.id
                    },
                    id=f"{doc.id}_chunk_{i}"
                )
                for i, text in enumerate(texts)
            ]

            # Embed
            embeddings = self.embedding_service.embed_batch([c.content for c in chunks])
            for chunk, embedding in zip(chunks, embeddings):
                chunk.embedding = embedding

            # Store
            self.vector_store.upsert(chunks)
            total_chunks += len(chunks)

        return total_chunks

    # ==================== RETRIEVAL ====================

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        filter: Optional[Dict] = None
    ) -> List[RetrievalResult]:
        """Retrieve relevant chunks."""
        top_k = top_k or self.top_k

        # Embed query
        query_embedding = self.embedding_service.embed(query)

        # Search
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            filter=filter
        )

        return results

    # ==================== GENERATION ====================

    def generate(
        self,
        query: str,
        context: List[RetrievalResult],
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate response from context."""

        # Format context
        context_text = "\n\n---\n\n".join([
            r.to_context(max_length=800) for r in context
        ])

        # Default system prompt
        if not system_prompt:
            system_prompt = """You are a helpful assistant that answers questions based on the provided context.

Rules:
- Answer based ONLY on the provided context
- If the context doesn't contain the answer, say "I don't have enough information"
- Cite sources using [Source: X] format
- Be concise and accurate
- Do not make up information"""

        response = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context_text}\n\n---\n\nQuestion: {query}"}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    # ==================== QUERY ====================

    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        filter: Optional[Dict] = None,
        system_prompt: Optional[str] = None
    ) -> RAGResponse:
        """Full RAG query: retrieve + generate."""
        start_time = time.time()

        # Retrieve
        results = self.retrieve(question, top_k, filter)

        # Generate
        answer = self.generate(question, results, system_prompt)

        latency_ms = (time.time() - start_time) * 1000

        return RAGResponse(
            query=question,
            answer=answer,
            sources=results,
            latency_ms=latency_ms
        )
```

---

## 7. Query Enhancement

```python
class QueryEnhancer:
    """Improve retrieval through query manipulation."""

    def __init__(self, llm_client, model: str = "gpt-4o-mini"):
        self.llm = llm_client
        self.model = model

    def expand(self, query: str, n_variations: int = 3) -> List[str]:
        """Generate query variations for multi-query retrieval."""
        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": f"Generate {n_variations} alternative phrasings of the user's question. Return only the questions, one per line, no numbering."
                },
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )

        variations = response.choices[0].message.content.strip().split("\n")
        return [query] + [v.strip() for v in variations if v.strip()]

    def hyde(self, query: str) -> str:
        """HyDE: Generate hypothetical document for embedding."""
        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Write a detailed paragraph that would answer the user's question. Be specific and technical as if you were writing documentation."
                },
                {"role": "user", "content": query}
            ],
            temperature=0.5
        )

        return response.choices[0].message.content

    def rewrite(self, query: str, context: str = "") -> str:
        """Rewrite query for clarity and searchability."""
        prompt = f"Rewrite this query to be more specific and searchable: {query}"
        if context:
            prompt += f"\n\nConversation context: {context}"

        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content
```

---

## 8. Usage Example

```python
# Initialize components
embedding_service = EmbeddingService(
    provider="openai",
    model="text-embedding-3-small"
)

vector_store = ChromaVectorStore(
    collection_name="my_docs",
    persist_dir="./rag_db"
)

# Or for production:
# vector_store = QdrantVectorStore(
#     collection_name="my_docs",
#     url="http://qdrant:6333"
# )

# Create pipeline
rag = RAGPipeline(
    embedding_service=embedding_service,
    vector_store=vector_store,
    llm_model="gpt-4o",
    chunk_size=500,
    chunk_overlap=50,
    top_k=5
)

# Ingest documents
loader = DocumentLoader()
documents = loader.load_directory("./docs", [".md", ".txt", ".pdf"])
total_chunks = rag.ingest(documents, chunking_strategy="recursive")
print(f"Indexed {total_chunks} chunks from {len(documents)} documents")

# Query
result = rag.query("What is the architecture of the system?")
print(f"Answer: {result.answer}")
print(f"Latency: {result.latency_ms:.0f}ms")
print(f"Sources: {len(result.sources)}")

# Retrieve only
results = rag.retrieve("system architecture", top_k=3)
for r in results:
    print(f"Score: {r.score:.3f} - {r.chunk.content[:100]}...")
```
