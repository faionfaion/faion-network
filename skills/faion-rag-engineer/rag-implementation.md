---
id: rag-implementation
name: "RAG Implementation"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# RAG Implementation

## Overview

Complete production-ready RAG pipeline implementation with document loading, chunking, embedding, retrieval, and generation.

## Complete Pipeline

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import numpy as np

@dataclass
class Document:
    content: str
    metadata: Dict[str, Any]
    id: Optional[str] = None

@dataclass
class Chunk:
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    id: Optional[str] = None

@dataclass
class RetrievalResult:
    chunk: Chunk
    score: float

class RAGPipeline:
    """Complete RAG pipeline implementation."""

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        llm_model: str = "gpt-4o",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 5
    ):
        from openai import OpenAI
        import chromadb

        self.client = OpenAI()
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k

        # Initialize vector store
        self.chroma = chromadb.PersistentClient(path="./rag_db")
        self.collection = self.chroma.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    # ==================== INDEXING ====================

    def ingest_documents(self, documents: List[Document]) -> int:
        """Ingest documents into the pipeline."""
        total_chunks = 0

        for doc in documents:
            chunks = self._chunk_document(doc)
            self._embed_chunks(chunks)
            self._store_chunks(chunks)
            total_chunks += len(chunks)

        return total_chunks

    def _chunk_document(self, doc: Document) -> List[Chunk]:
        """Split document into chunks."""
        text = doc.content
        chunks = []

        start = 0
        chunk_id = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]

            # Try to end at sentence boundary
            if end < len(text):
                last_period = chunk_text.rfind('.')
                if last_period > self.chunk_size * 0.5:
                    chunk_text = chunk_text[:last_period + 1]
                    end = start + last_period + 1

            chunks.append(Chunk(
                content=chunk_text.strip(),
                metadata={
                    **doc.metadata,
                    "chunk_index": chunk_id,
                    "source_id": doc.id
                },
                id=f"{doc.id}_chunk_{chunk_id}"
            ))

            start = end - self.chunk_overlap
            chunk_id += 1

        return chunks

    def _embed_chunks(self, chunks: List[Chunk]) -> None:
        """Generate embeddings for chunks."""
        texts = [c.content for c in chunks]

        response = self.client.embeddings.create(
            input=texts,
            model=self.embedding_model
        )

        for i, chunk in enumerate(chunks):
            chunk.embedding = response.data[i].embedding

    def _store_chunks(self, chunks: List[Chunk]) -> None:
        """Store chunks in vector database."""
        self.collection.upsert(
            ids=[c.id for c in chunks],
            embeddings=[c.embedding for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[c.metadata for c in chunks]
        )

    # ==================== RETRIEVAL ====================

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        filter: Optional[Dict] = None
    ) -> List[RetrievalResult]:
        """Retrieve relevant chunks for query."""
        top_k = top_k or self.top_k

        # Embed query
        response = self.client.embeddings.create(
            input=query,
            model=self.embedding_model
        )
        query_embedding = response.data[0].embedding

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter,
            include=["documents", "metadatas", "distances"]
        )

        # Format results
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

    # ==================== GENERATION ====================

    def generate(
        self,
        query: str,
        context: List[RetrievalResult],
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate response using retrieved context."""

        # Format context
        context_text = "\n\n".join([
            f"[Source: {r.chunk.metadata.get('source', 'unknown')}]\n{r.chunk.content}"
            for r in context
        ])

        # Default system prompt
        if not system_prompt:
            system_prompt = """You are a helpful assistant that answers questions based on the provided context.

Rules:
- Answer based ONLY on the provided context
- If the context doesn't contain the answer, say "I don't have enough information to answer this question"
- Cite sources when possible
- Be concise and accurate"""

        # Generate response
        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    # ==================== QUERY ====================

    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        filter: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Full RAG query: retrieve and generate."""
        # Retrieve
        results = self.retrieve(question, top_k, filter)

        # Generate
        answer = self.generate(question, results)

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "content": r.chunk.content[:200] + "...",
                    "score": r.score,
                    "metadata": r.chunk.metadata
                }
                for r in results
            ]
        }
```

## Document Loaders

```python
from pathlib import Path
from typing import List
import json

class DocumentLoader:
    """Load documents from various sources."""

    @staticmethod
    def load_text(file_path: str) -> Document:
        """Load plain text file."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return Document(
            content=content,
            metadata={"source": file_path, "type": "text"},
            id=Path(file_path).stem
        )

    @staticmethod
    def load_pdf(file_path: str) -> Document:
        """Load PDF file."""
        import pypdf

        reader = pypdf.PdfReader(file_path)
        content = ""
        for page in reader.pages:
            content += page.extract_text() + "\n"

        return Document(
            content=content,
            metadata={
                "source": file_path,
                "type": "pdf",
                "pages": len(reader.pages)
            },
            id=Path(file_path).stem
        )

    @staticmethod
    def load_markdown(file_path: str) -> Document:
        """Load Markdown file."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract title from first heading
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
        """Load all documents from directory."""
        documents = []
        dir_path = Path(directory)

        for ext in extensions:
            for file_path in dir_path.rglob(f"*{ext}"):
                if ext == ".txt":
                    documents.append(DocumentLoader.load_text(str(file_path)))
                elif ext == ".md":
                    documents.append(DocumentLoader.load_markdown(str(file_path)))
                elif ext == ".pdf":
                    documents.append(DocumentLoader.load_pdf(str(file_path)))

        return documents
```

## Chunking Implementations

```python
from typing import List
import re

class ChunkingStrategy:
    """Different chunking strategies for various document types."""

    @staticmethod
    def fixed_size(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[str]:
        """Fixed size chunks with overlap."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap

        return chunks

    @staticmethod
    def sentence_based(
        text: str,
        max_chunk_size: int = 500,
        min_chunk_size: int = 100
    ) -> List[str]:
        """Chunk by sentences, respecting size limits."""
        import nltk
        nltk.download('punkt', quiet=True)

        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += sentence + " "
            else:
                if len(current_chunk) >= min_chunk_size:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    @staticmethod
    def paragraph_based(
        text: str,
        max_chunk_size: int = 1000
    ) -> List[str]:
        """Chunk by paragraphs."""
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current_chunk) + len(para) <= max_chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    @staticmethod
    def semantic_chunking(
        text: str,
        embedding_func: callable,
        similarity_threshold: float = 0.8
    ) -> List[str]:
        """Chunk based on semantic similarity between sentences."""
        import nltk
        from numpy import dot
        from numpy.linalg import norm

        sentences = nltk.sent_tokenize(text)
        if not sentences:
            return []

        # Get embeddings for all sentences
        embeddings = [embedding_func(s) for s in sentences]

        chunks = []
        current_chunk = [sentences[0]]

        for i in range(1, len(sentences)):
            # Calculate similarity with previous sentence
            sim = dot(embeddings[i], embeddings[i-1]) / (
                norm(embeddings[i]) * norm(embeddings[i-1])
            )

            if sim >= similarity_threshold:
                current_chunk.append(sentences[i])
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[i]]

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    @staticmethod
    def markdown_header_based(text: str) -> List[str]:
        """Chunk Markdown by headers."""
        # Split by headers (##, ###, etc.)
        pattern = r'(^#{1,6}\s+.+$)'
        sections = re.split(pattern, text, flags=re.MULTILINE)

        chunks = []
        current_header = ""
        current_content = ""

        for section in sections:
            section = section.strip()
            if not section:
                continue

            if re.match(r'^#{1,6}\s+', section):
                if current_content:
                    chunks.append(f"{current_header}\n\n{current_content}".strip())
                current_header = section
                current_content = ""
            else:
                current_content += section + "\n"

        if current_content:
            chunks.append(f"{current_header}\n\n{current_content}".strip())

        return chunks
```

## Query Enhancement

```python
class QueryEnhancer:
    """Enhance queries for better retrieval."""

    def __init__(self, client):
        self.client = client

    def expand_query(self, query: str) -> List[str]:
        """Generate query variations for better recall."""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Generate 3 alternative phrasings of the user's question. Return only the questions, one per line."
                },
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )

        variations = response.choices[0].message.content.strip().split("\n")
        return [query] + [v.strip() for v in variations if v.strip()]

    def generate_hypothetical_answer(self, query: str) -> str:
        """HyDE: Generate hypothetical answer for embedding."""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Answer the question as if you had access to the relevant documents. Be specific and detailed."
                },
                {"role": "user", "content": query}
            ],
            temperature=0.5
        )

        return response.choices[0].message.content

    def rewrite_query(self, query: str, context: str = "") -> str:
        """Rewrite query for clarity."""
        prompt = f"Rewrite this query to be more specific and searchable:\n\nQuery: {query}"
        if context:
            prompt += f"\n\nContext: {context}"

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content
```

## Usage Example

```python
# Initialize pipeline
rag = RAGPipeline(
    embedding_model="text-embedding-3-small",
    llm_model="gpt-4o",
    chunk_size=500,
    chunk_overlap=50,
    top_k=5
)

# Load documents
loader = DocumentLoader()
documents = loader.load_directory("./docs", [".md", ".txt", ".pdf"])

# Ingest documents
total_chunks = rag.ingest_documents(documents)
print(f"Indexed {total_chunks} chunks from {len(documents)} documents")

# Query
result = rag.query("What is RAG?")
print(f"Question: {result['question']}")
print(f"Answer: {result['answer']}")
print(f"Sources: {len(result['sources'])}")

# Retrieve only (no generation)
results = rag.retrieve("RAG", top_k=3)
for r in results:
    print(f"Score: {r.score:.3f} - {r.chunk.content[:100]}...")

# Generate with custom prompt
results = rag.retrieve("RAG")
answer = rag.generate(
    "What is RAG?",
    results,
    system_prompt="You are a technical writer. Explain concepts clearly."
)
print(answer)
```

## Sources

- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [LlamaIndex RAG Guide](https://docs.llamaindex.ai/en/stable/understanding/putting_it_all_together/index.html)
- [Building Production RAG](https://blog.llamaindex.ai/building-production-ready-rag-applications-a2a3d5f2c9f8)
- [RAG from Scratch](https://github.com/langchain-ai/rag-from-scratch)
