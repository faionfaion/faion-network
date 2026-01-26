# Embedding Generation Examples

## OpenAI Embeddings

### Basic Embedding

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

def get_embedding(text: str, model: str = "text-embedding-3-small") -> list:
    """Generate embedding using OpenAI."""
    text = text.replace("\n", " ")
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding
```

### Batch Embedding

```python
def get_embeddings_batch(
    texts: list[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 100
) -> list:
    """Generate embeddings for multiple texts with batching."""
    texts = [t.replace("\n", " ") for t in texts]
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(
            input=batch,
            model=model
        )
        embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(embeddings)

    return all_embeddings
```

### Dimension Reduction (text-embedding-3 models only)

```python
def get_reduced_embedding(
    text: str,
    dimensions: int = 256,
    model: str = "text-embedding-3-small"
) -> list:
    """Get lower-dimensional embedding for efficiency."""
    response = client.embeddings.create(
        input=text,
        model=model,
        dimensions=dimensions  # Native dimension reduction
    )
    return response.data[0].embedding
```

## Cohere Embeddings

### Basic Usage with Input Types

```python
import cohere

co = cohere.Client(api_key="your-api-key")

def get_cohere_embeddings(
    texts: list[str],
    input_type: str = "search_document",
    model: str = "embed-english-v3.0"
) -> list:
    """
    Generate Cohere embeddings with task-specific input types.

    input_type options:
    - search_document: For documents to be searched
    - search_query: For search queries
    - classification: For classification tasks
    - clustering: For clustering tasks
    """
    response = co.embed(
        texts=texts,
        model=model,
        input_type=input_type
    )
    return response.embeddings


# Usage for RAG
doc_embeddings = get_cohere_embeddings(
    documents,
    input_type="search_document"
)

query_embedding = get_cohere_embeddings(
    [query],
    input_type="search_query"
)[0]
```

### Multilingual Embedding

```python
def get_multilingual_embeddings(
    texts: list[str],
    input_type: str = "search_document"
) -> list:
    """Cohere multilingual embeddings (100+ languages)."""
    response = co.embed(
        texts=texts,
        model="embed-multilingual-v3.0",
        input_type=input_type
    )
    return response.embeddings
```

## Voyage AI Embeddings

### Basic Usage

```python
import voyageai

vo = voyageai.Client(api_key="your-api-key")

def get_voyage_embeddings(
    texts: list[str],
    model: str = "voyage-3",
    input_type: str = "document"
) -> list:
    """
    Generate Voyage AI embeddings.

    input_type: "document" or "query"
    """
    result = vo.embed(
        texts,
        model=model,
        input_type=input_type
    )
    return result.embeddings
```

### Domain-Specific Models

```python
# Code retrieval
code_embeddings = vo.embed(
    code_snippets,
    model="voyage-code-2",
    input_type="document"
)

# Legal documents
legal_embeddings = vo.embed(
    legal_texts,
    model="voyage-law-2",
    input_type="document"
)
```

## Local Embeddings with Sentence Transformers

### Basic Usage

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model (downloads on first use)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_local_embedding(text: str) -> np.ndarray:
    """Generate embedding locally."""
    return model.encode(text)

def get_local_embeddings_batch(
    texts: list[str],
    batch_size: int = 32,
    show_progress: bool = True
) -> np.ndarray:
    """Batch embedding generation with GPU optimization."""
    return model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=show_progress,
        convert_to_numpy=True,
        normalize_embeddings=True  # Pre-normalize for cosine similarity
    )
```

### BGE Models (Higher Quality)

```python
bge_model = SentenceTransformer('BAAI/bge-large-en-v1.5')

def get_bge_embedding(
    text: str,
    is_query: bool = False
) -> np.ndarray:
    """BGE embeddings with instruction prefix for queries."""
    if is_query:
        # BGE models work better with instruction prefix for queries
        text = "Represent this sentence for retrieval: " + text
    return bge_model.encode(text, normalize_embeddings=True)
```

### BGE-M3 (Best Self-Hosted)

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

def get_bge_m3_embeddings(texts: list[str]) -> dict:
    """BGE-M3 returns dense, sparse, and colbert vectors."""
    return model.encode(
        texts,
        batch_size=12,
        max_length=8192,
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=True
    )
```

## Ollama Embeddings (Local)

### Basic Usage

```python
import ollama

def get_ollama_embedding(
    text: str,
    model: str = "nomic-embed-text"
) -> list:
    """Generate embedding using Ollama."""
    response = ollama.embeddings(
        model=model,
        prompt=text
    )
    return response["embedding"]

def get_ollama_embeddings_batch(
    texts: list[str],
    model: str = "nomic-embed-text"
) -> list:
    """Batch embeddings with Ollama (sequential)."""
    return [
        ollama.embeddings(model=model, prompt=text)["embedding"]
        for text in texts
    ]
```

## Similarity Calculations

### Cosine Similarity

```python
import numpy as np
from typing import List, Tuple

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def cosine_similarity_batch(
    query: np.ndarray,
    documents: np.ndarray
) -> np.ndarray:
    """Calculate cosine similarity between query and all documents."""
    # Normalize
    query_norm = query / np.linalg.norm(query)
    doc_norms = documents / np.linalg.norm(documents, axis=1, keepdims=True)
    # Dot product of normalized vectors = cosine similarity
    return np.dot(doc_norms, query_norm)
```

### Find Most Similar

```python
def find_most_similar(
    query_embedding: np.ndarray,
    document_embeddings: np.ndarray,
    top_k: int = 5
) -> List[Tuple[int, float]]:
    """Find most similar documents to query."""
    similarities = cosine_similarity_batch(query_embedding, document_embeddings)
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return [(idx, similarities[idx]) for idx in top_indices]
```

### Normalized Vectors (Faster)

```python
def normalize_embedding(embedding: np.ndarray) -> np.ndarray:
    """Normalize embedding to unit length."""
    norm = np.linalg.norm(embedding)
    return embedding / norm if norm > 0 else embedding

def normalize_batch(embeddings: np.ndarray) -> np.ndarray:
    """Normalize batch of embeddings."""
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1  # Avoid division by zero
    return embeddings / norms

# For pre-normalized vectors, use dot product (faster)
def similarity_normalized(a: np.ndarray, b: np.ndarray) -> float:
    """Dot product for normalized vectors equals cosine similarity."""
    return np.dot(a, b)
```

## Length-Based Sorting for Batch Optimization

```python
def embed_with_length_sorting(
    texts: list[str],
    embed_func: callable,
    batch_size: int = 32
) -> list:
    """
    Embed texts with length-based sorting to minimize padding.

    Achieves ~40% less computational waste.
    """
    # Create index-text pairs and sort by length
    indexed_texts = [(i, text) for i, text in enumerate(texts)]
    sorted_texts = sorted(indexed_texts, key=lambda x: len(x[1]))

    # Embed in batches
    embeddings = [None] * len(texts)
    for i in range(0, len(sorted_texts), batch_size):
        batch = sorted_texts[i:i + batch_size]
        batch_texts = [t[1] for t in batch]
        batch_embeddings = embed_func(batch_texts)

        # Restore original order
        for (orig_idx, _), emb in zip(batch, batch_embeddings):
            embeddings[orig_idx] = emb

    return embeddings
```

## Async Embedding with Rate Limiting

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def get_embedding_async(
    text: str,
    model: str = "text-embedding-3-small",
    semaphore: asyncio.Semaphore = None
) -> list:
    """Async embedding with rate limiting."""
    async with semaphore or asyncio.Semaphore(10):
        text = text.replace("\n", " ")
        response = await async_client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding

async def get_embeddings_concurrent(
    texts: list[str],
    max_concurrent: int = 10
) -> list:
    """Generate embeddings concurrently with rate limiting."""
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [
        get_embedding_async(text, semaphore=semaphore)
        for text in texts
    ]
    return await asyncio.gather(*tasks)
```
