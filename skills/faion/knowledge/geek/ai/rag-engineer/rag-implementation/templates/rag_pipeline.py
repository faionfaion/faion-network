"""
RAGPipeline — complete RAG pipeline: ingest + retrieve + generate.

Usage:
    rag = RAGPipeline(embedding_model="text-embedding-3-small", llm_model="gpt-4o")
    rag.ingest_documents(DocumentLoader.load_directory("./docs"))
    result = rag.query("What is RAG?")
    # result = {"question": ..., "answer": ..., "sources": [...]}
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import chromadb
from openai import OpenAI


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
    SYSTEM_PROMPT = (
        "You are a helpful assistant. Answer ONLY from the provided context. "
        "If the context does not contain the answer, say 'I don't have enough information.'"
        " Cite sources when possible."
    )

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        llm_model: str = "gpt-4o",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 5,
        score_threshold: float = 0.6,
    ) -> None:
        self.client = OpenAI()
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.score_threshold = score_threshold
        chroma = chromadb.PersistentClient(path="./rag_db")
        self.col = chroma.get_or_create_collection("documents", metadata={"hnsw:space": "cosine"})

    # ------------------------------------------------------------------
    # Ingest
    # ------------------------------------------------------------------

    def ingest_documents(self, documents: List[Document]) -> int:
        total = 0
        for doc in documents:
            chunks = self._chunk(doc)
            self._embed_chunks(chunks)
            self.col.upsert(
                ids=[c.id for c in chunks],
                embeddings=[c.embedding for c in chunks],
                documents=[c.content for c in chunks],
                metadatas=[c.metadata for c in chunks],
            )
            total += len(chunks)
        return total

    def _chunk(self, doc: Document) -> List[Chunk]:
        text, chunks, start, idx = doc.content, [], 0, 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end].strip()
            chunks.append(Chunk(
                content=chunk_text,
                metadata={**doc.metadata, "chunk_index": idx, "source_id": doc.id},
                id=f"{doc.id}_chunk_{idx}",
            ))
            start = end - self.chunk_overlap
            idx += 1
        return chunks

    def _embed_chunks(self, chunks: List[Chunk]) -> None:
        r = self.client.embeddings.create(input=[c.content for c in chunks], model=self.embedding_model)
        for i, chunk in enumerate(chunks):
            chunk.embedding = r.data[i].embedding

    # ------------------------------------------------------------------
    # Retrieve
    # ------------------------------------------------------------------

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[RetrievalResult]:
        k = top_k or self.top_k
        qemb = self.client.embeddings.create(input=query, model=self.embedding_model).data[0].embedding
        r = self.col.query(query_embeddings=[qemb], n_results=k,
                           include=["documents", "metadatas", "distances"])
        results = []
        for i in range(len(r["ids"][0])):
            score = 1 - r["distances"][0][i]
            if score >= self.score_threshold:
                results.append(RetrievalResult(
                    chunk=Chunk(id=r["ids"][0][i], content=r["documents"][0][i], metadata=r["metadatas"][0][i]),
                    score=score,
                ))
        return results

    # ------------------------------------------------------------------
    # Generate
    # ------------------------------------------------------------------

    def generate(self, query: str, context: List[RetrievalResult], system_prompt: Optional[str] = None) -> str:
        ctx = "\n\n".join(
            f"[Source: {r.chunk.metadata.get('source', 'unknown')}]\n{r.chunk.content}"
            for r in context
        )
        r = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": system_prompt or self.SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{ctx}\n\nQuestion: {query}"},
            ],
            temperature=0.3,
        )
        return r.choices[0].message.content

    def query(self, question: str) -> Dict[str, Any]:
        results = self.retrieve(question)
        answer = self.generate(question, results)
        return {
            "question": question,
            "answer": answer,
            "sources": [{"content": r.chunk.content[:200], "score": r.score, "metadata": r.chunk.metadata}
                        for r in results],
        }


class DocumentLoader:
    @staticmethod
    def load_text(file_path: str) -> Document:
        p = Path(file_path)
        return Document(content=p.read_text(encoding="utf-8"),
                        metadata={"source": file_path, "type": "text"}, id=p.stem)

    @staticmethod
    def load_markdown(file_path: str) -> Document:
        p = Path(file_path)
        content = p.read_text(encoding="utf-8")
        title = next((l[2:].strip() for l in content.split("\n") if l.startswith("# ")), "")
        return Document(content=content, metadata={"source": file_path, "type": "markdown", "title": title}, id=p.stem)

    @staticmethod
    def load_directory(directory: str, extensions: List[str] = [".txt", ".md"]) -> List[Document]:
        docs = []
        for ext in extensions:
            for fp in Path(directory).rglob(f"*{ext}"):
                if ext == ".md":
                    docs.append(DocumentLoader.load_markdown(str(fp)))
                else:
                    docs.append(DocumentLoader.load_text(str(fp)))
        return docs
