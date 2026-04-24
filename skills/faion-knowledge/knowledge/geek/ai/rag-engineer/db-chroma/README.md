# Chroma Vector Database

In-memory vector database for prototyping and local development.

## Overview

Chroma is ideal for rapid prototyping and development. Simple API, fast, in-memory or persistent.

**Best For:** Prototyping | **Scale:** 1M vectors | **Hosting:** In-memory/Local

---

## Installation

```bash
pip install chromadb
```

---

## Basic Usage

```python
import chromadb
from chromadb.config import Settings

# In-memory (default)
client = chromadb.Client()

# Persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # cosine, l2, ip
)

# Add documents
collection.add(
    ids=["doc1", "doc2", "doc3"],
    embeddings=[emb1, emb2, emb3],
    metadatas=[
        {"source": "file1.pdf", "page": 1},
        {"source": "file2.pdf", "page": 2},
        {"source": "file3.pdf", "page": 3},
    ],
    documents=["Text 1", "Text 2", "Text 3"],  # Optional
)

# Query
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    where={"source": {"$eq": "file1.pdf"}},
    where_document={"$contains": "keyword"},
    include=["documents", "metadatas", "distances"],
)

print(results["ids"])
print(results["distances"])
print(results["documents"])

# Update
collection.update(
    ids=["doc1"],
    embeddings=[new_embedding],
    metadatas=[{"source": "updated.pdf"}],
)

# Delete
collection.delete(ids=["doc1", "doc2"])
collection.delete(where={"source": "old.pdf"})
```

---

## LangChain Integration

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# Create from documents
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="my_collection",
)

# Load existing
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="my_collection",
)

# Search
results = vectorstore.similarity_search_with_score(
    query="search query",
    k=10,
    filter={"source": "file.pdf"},
)
```

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## Sources

- [Chroma Documentation](https://docs.trychroma.com/)
- [Chroma GitHub](https://github.com/chroma-core/chroma)
- [LangChain Chroma Integration](https://python.langchain.com/docs/integrations/vectorstores/chroma)
