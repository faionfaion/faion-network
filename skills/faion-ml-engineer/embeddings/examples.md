# Text Embedding Code Examples

Comprehensive code examples for generating embeddings with all major providers, batch processing, similarity search, and multimodal embeddings.

---

## Table of Contents

1. [OpenAI Embeddings](#openai-embeddings)
2. [Voyage AI Embeddings](#voyage-ai-embeddings)
3. [Cohere Embeddings](#cohere-embeddings)
4. [Local Models (sentence-transformers)](#local-models-sentence-transformers)
5. [Mistral Embeddings](#mistral-embeddings)
6. [Batch Processing](#batch-processing)
7. [Similarity Search](#similarity-search)
8. [Chunking Strategies](#chunking-strategies)
9. [Caching](#caching)
10. [Multimodal Embeddings](#multimodal-embeddings)
11. [Hybrid Search](#hybrid-search)
12. [Vector Database Integration](#vector-database-integration)

---

## OpenAI Embeddings

### Basic Usage

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

def get_embedding(text: str, model: str = "text-embedding-3-large") -> list[float]:
    """Get embedding for a single text."""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

# Usage
embedding = get_embedding("Machine learning is fascinating")
print(f"Dimensions: {len(embedding)}")  # 3072 for text-embedding-3-large
```

### Dimension Reduction (Matryoshka)

```python
def get_embedding_reduced(
    text: str,
    model: str = "text-embedding-3-large",
    dimensions: int = 256
) -> list[float]:
    """Get reduced-dimension embedding for cheaper storage."""
    response = client.embeddings.create(
        input=text,
        model=model,
        dimensions=dimensions  # 256, 512, 1024, 1536, 3072
    )
    return response.data[0].embedding

# Usage - 12x smaller vector with ~4% quality loss
small_embedding = get_embedding_reduced("Machine learning", dimensions=256)
print(f"Dimensions: {len(small_embedding)}")  # 256
```

### Batch Processing

```python
def get_embeddings_batch(
    texts: list[str],
    model: str = "text-embedding-3-large",
    batch_size: int = 2048,  # OpenAI limit
    dimensions: int | None = None
) -> list[list[float]]:
    """Get embeddings for multiple texts efficiently."""
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        kwargs = {"input": batch, "model": model}
        if dimensions:
            kwargs["dimensions"] = dimensions

        response = client.embeddings.create(**kwargs)

        # Preserve order (API may return out of order)
        sorted_embeddings = sorted(response.data, key=lambda x: x.index)
        all_embeddings.extend([e.embedding for e in sorted_embeddings])

    return all_embeddings

# Usage
texts = ["First document", "Second document", "Third document"]
embeddings = get_embeddings_batch(texts)
print(f"Generated {len(embeddings)} embeddings")
```

### Async Batch Processing

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def get_embeddings_async(
    texts: list[str],
    model: str = "text-embedding-3-large",
    batch_size: int = 100,
    max_concurrent: int = 5
) -> list[list[float]]:
    """Process large volumes with controlled concurrency."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_batch(batch: list[str], batch_idx: int) -> tuple[int, list[list[float]]]:
        async with semaphore:
            response = await async_client.embeddings.create(
                input=batch,
                model=model
            )
            sorted_data = sorted(response.data, key=lambda x: x.index)
            return batch_idx, [e.embedding for e in sorted_data]

    # Create batches
    batches = [texts[i:i+batch_size] for i in range(0, len(texts), batch_size)]

    # Process concurrently
    tasks = [process_batch(batch, idx) for idx, batch in enumerate(batches)]
    results = await asyncio.gather(*tasks)

    # Sort by batch index and flatten
    sorted_results = sorted(results, key=lambda x: x[0])
    return [emb for _, batch_embs in sorted_results for emb in batch_embs]

# Usage
async def main():
    texts = [f"Document {i}" for i in range(1000)]
    embeddings = await get_embeddings_async(texts)
    print(f"Generated {len(embeddings)} embeddings")

asyncio.run(main())
```

---

## Voyage AI Embeddings

### Basic Usage

```python
import voyageai

client = voyageai.Client()  # Uses VOYAGE_API_KEY env var

def get_voyage_embedding(
    text: str,
    model: str = "voyage-3.5",
    input_type: str = "document"
) -> list[float]:
    """Get Voyage AI embedding."""
    result = client.embed(
        texts=[text],
        model=model,
        input_type=input_type  # "document" or "query"
    )
    return result.embeddings[0]

# Usage - asymmetric search
doc_embedding = get_voyage_embedding("Python is a programming language", input_type="document")
query_embedding = get_voyage_embedding("What is Python?", input_type="query")
```

### Batch with Dimension Reduction

```python
def get_voyage_embeddings_batch(
    texts: list[str],
    model: str = "voyage-3.5",
    input_type: str = "document",
    output_dimension: int = 1024,  # Matryoshka: 256, 512, 1024, 2048
    output_dtype: str = "float"  # "float", "int8", "binary"
) -> list[list[float]]:
    """Batch embeddings with dimension reduction and quantization."""
    result = client.embed(
        texts=texts,
        model=model,
        input_type=input_type,
        output_dimension=output_dimension,
        output_dtype=output_dtype
    )
    return result.embeddings

# Usage - 75% smaller vectors
embeddings = get_voyage_embeddings_batch(
    texts=["Doc 1", "Doc 2"],
    output_dimension=512,
    output_dtype="int8"
)
```

### Contextualized Chunks (voyage-context-3)

```python
def embed_contextualized_chunks(
    chunks: list[str],
    document_context: str,
    model: str = "voyage-context-3"
) -> list[list[float]]:
    """Embed chunks with full document context."""
    # Prepend context to each chunk
    contextualized = [
        f"Document context: {document_context}\n\nChunk: {chunk}"
        for chunk in chunks
    ]

    result = client.embed(
        texts=contextualized,
        model=model,
        input_type="document"
    )
    return result.embeddings

# Usage
document = "This is a long document about machine learning..."
chunks = ["Neural networks", "Gradient descent", "Backpropagation"]
embeddings = embed_contextualized_chunks(chunks, document[:500])
```

---

## Cohere Embeddings

### Basic Usage

```python
import cohere

co = cohere.Client()  # Uses COHERE_API_KEY env var

def get_cohere_embedding(
    texts: list[str],
    input_type: str = "search_document",
    model: str = "embed-v4"
) -> list[list[float]]:
    """
    Get Cohere embeddings.

    input_type options:
    - "search_document": For documents to be searched
    - "search_query": For search queries
    - "classification": For classification tasks
    - "clustering": For clustering tasks
    - "image": For image embeddings (embed-v4 only)
    """
    response = co.embed(
        texts=texts,
        model=model,
        input_type=input_type,
        truncate="END"  # or "START", "NONE"
    )
    return response.embeddings

# Usage - asymmetric search
documents = ["Python guide", "Java tutorial"]
doc_embeddings = get_cohere_embedding(documents, input_type="search_document")

query = "programming language"
query_embedding = get_cohere_embedding([query], input_type="search_query")[0]
```

### Multilingual Embeddings

```python
def get_multilingual_embeddings(texts: list[str]) -> list[list[float]]:
    """Embed texts in 100+ languages."""
    response = co.embed(
        texts=texts,
        model="embed-multilingual-v3.0",
        input_type="search_document"
    )
    return response.embeddings

# Usage - same embedding space for all languages
texts = [
    "Hello world",           # English
    "Bonjour le monde",      # French
    "Hola mundo",            # Spanish
    "Hallo Welt",            # German
]
embeddings = get_multilingual_embeddings(texts)
```

### Embed-v4 with Dimension Reduction

```python
def get_cohere_v4_embedding(
    texts: list[str],
    input_type: str = "search_document",
    embedding_types: list[str] = ["float"],
    dimensions: int = 1024  # Matryoshka: 256, 512, 1024, 1536
) -> list[list[float]]:
    """Cohere embed-v4 with Matryoshka dimensions."""
    response = co.embed(
        texts=texts,
        model="embed-v4",
        input_type=input_type,
        embedding_types=embedding_types,
        output_dimension=dimensions
    )
    return response.embeddings

# Usage
embeddings = get_cohere_v4_embedding(
    ["Document 1", "Document 2"],
    dimensions=256  # Smallest, fastest
)
```

---

## Local Models (sentence-transformers)

### Basic Usage

```python
from sentence_transformers import SentenceTransformer

# Load model (downloads on first use)
model = SentenceTransformer("BAAI/bge-large-en-v1.5")

def get_local_embedding(text: str) -> list[float]:
    """Get embedding using local model."""
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

# Batch processing (automatic batching)
def get_local_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Batch embeddings with progress bar."""
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )
    return embeddings.tolist()

# Usage
texts = ["First text", "Second text"]
embeddings = get_local_embeddings_batch(texts)
```

### GPU Acceleration

```python
import torch
from sentence_transformers import SentenceTransformer

# Auto-detect GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model = SentenceTransformer("BAAI/bge-large-en-v1.5", device=device)

def get_gpu_embeddings(
    texts: list[str],
    batch_size: int = 32
) -> list[list[float]]:
    """Batch embeddings with GPU acceleration."""
    embeddings = model.encode(
        texts,
        batch_size=batch_size,  # Adjust based on GPU memory
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embeddings.tolist()

# Usage
texts = [f"Document {i}" for i in range(1000)]
embeddings = get_gpu_embeddings(texts, batch_size=64)
```

### BGE-M3 (Dense + Sparse)

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

def get_bge_m3_embeddings(
    texts: list[str],
    return_sparse: bool = False
) -> dict:
    """Get BGE-M3 dense and optionally sparse embeddings."""
    output = model.encode(
        texts,
        return_dense=True,
        return_sparse=return_sparse
    )

    result = {"dense": output["dense_vecs"].tolist()}

    if return_sparse:
        result["sparse"] = output["lexical_weights"]

    return result

# Usage - hybrid search
result = get_bge_m3_embeddings(
    ["Python programming", "Java development"],
    return_sparse=True
)
dense_embeddings = result["dense"]
sparse_embeddings = result["sparse"]  # For BM25-style matching
```

### Popular Local Models

```python
# Best quality (slow, 8K context)
model = SentenceTransformer("BAAI/bge-m3")

# Good quality, balanced
model = SentenceTransformer("BAAI/bge-large-en-v1.5")
model = SentenceTransformer("intfloat/e5-large-v2")

# Fast inference
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Multilingual
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Long context (8K tokens) with MoE
model = SentenceTransformer("nomic-ai/nomic-embed-text-v2-moe", trust_remote_code=True)

# Instruction-aware
model = SentenceTransformer("Alibaba-NLP/gte-Qwen2-7B-instruct", trust_remote_code=True)
```

---

## Mistral Embeddings

### Basic Usage

```python
from mistralai import Mistral

client = Mistral(api_key="YOUR_API_KEY")

def get_mistral_embedding(text: str) -> list[float]:
    """Get embedding using Mistral."""
    response = client.embeddings.create(
        model="mistral-embed",
        inputs=[text]
    )
    return response.data[0].embedding

def get_mistral_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Batch embeddings with Mistral."""
    response = client.embeddings.create(
        model="mistral-embed",
        inputs=texts
    )
    return [e.embedding for e in response.data]

# Usage
embedding = get_mistral_embedding("Hello world")
print(f"Dimensions: {len(embedding)}")  # 1024
```

---

## Batch Processing

### Unified Batch Processor

```python
from typing import Callable, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class BatchEmbedder:
    """Unified batch processor for any embedding provider."""

    def __init__(
        self,
        embed_fn: Callable[[list[str]], list[list[float]]],
        batch_size: int = 100,
        max_workers: int = 4,
        rate_limit_delay: float = 0.1
    ):
        self.embed_fn = embed_fn
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.rate_limit_delay = rate_limit_delay

    def embed(self, texts: list[str], show_progress: bool = True) -> list[list[float]]:
        """Embed texts in parallel batches."""
        batches = [
            texts[i:i + self.batch_size]
            for i in range(0, len(texts), self.batch_size)
        ]

        results = [None] * len(batches)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._process_batch, batch, idx): idx
                for idx, batch in enumerate(batches)
            }

            completed = 0
            for future in as_completed(futures):
                idx = futures[future]
                results[idx] = future.result()
                completed += 1

                if show_progress:
                    print(f"Progress: {completed}/{len(batches)} batches")

        # Flatten results
        return [emb for batch in results for emb in batch]

    def _process_batch(self, batch: list[str], idx: int) -> list[list[float]]:
        """Process single batch with rate limiting."""
        time.sleep(self.rate_limit_delay * idx)  # Stagger requests
        return self.embed_fn(batch)

# Usage with OpenAI
from openai import OpenAI
client = OpenAI()

def openai_embed(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(input=texts, model="text-embedding-3-large")
    return [e.embedding for e in sorted(response.data, key=lambda x: x.index)]

embedder = BatchEmbedder(openai_embed, batch_size=100, max_workers=4)
embeddings = embedder.embed([f"Doc {i}" for i in range(1000)])
```

### Progress Tracking with tqdm

```python
from tqdm import tqdm

def embed_with_progress(
    texts: list[str],
    embed_fn: Callable,
    batch_size: int = 100
) -> list[list[float]]:
    """Embed with progress bar."""
    all_embeddings = []

    for i in tqdm(range(0, len(texts), batch_size), desc="Embedding"):
        batch = texts[i:i + batch_size]
        embeddings = embed_fn(batch)
        all_embeddings.extend(embeddings)

    return all_embeddings
```

---

## Similarity Search

### Cosine Similarity

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def search_similar(
    query_embedding: list[float],
    document_embeddings: list[list[float]],
    top_k: int = 10
) -> list[tuple[int, float]]:
    """Find most similar documents by cosine similarity."""
    query = np.array(query_embedding).reshape(1, -1)
    docs = np.array(document_embeddings)

    # Cosine similarity
    similarities = cosine_similarity(query, docs)[0]

    # Get top-k indices
    top_indices = np.argsort(similarities)[::-1][:top_k]

    return [(int(idx), float(similarities[idx])) for idx in top_indices]

# Usage
query_emb = get_embedding("What is machine learning?")
doc_embs = get_embeddings_batch(["ML is AI", "Python is a language", "Neural networks"])

results = search_similar(query_emb, doc_embs, top_k=2)
for idx, score in results:
    print(f"Doc {idx}: {score:.4f}")
```

### Efficient Similarity with FAISS

```python
import faiss
import numpy as np

class FAISSIndex:
    """Fast similarity search with FAISS."""

    def __init__(self, dimension: int, use_gpu: bool = False):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine after L2 norm)

        if use_gpu and faiss.get_num_gpus() > 0:
            self.index = faiss.index_cpu_to_gpu(
                faiss.StandardGpuResources(),
                0,
                self.index
            )

        self.documents = []

    def add(self, embeddings: list[list[float]], documents: list[str]):
        """Add documents to index."""
        vectors = np.array(embeddings, dtype=np.float32)
        # L2 normalize for cosine similarity
        faiss.normalize_L2(vectors)
        self.index.add(vectors)
        self.documents.extend(documents)

    def search(self, query_embedding: list[float], top_k: int = 10) -> list[tuple[str, float]]:
        """Search for similar documents."""
        query = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query)

        scores, indices = self.index.search(query, top_k)

        return [
            (self.documents[idx], float(score))
            for score, idx in zip(scores[0], indices[0])
            if idx != -1
        ]

# Usage
index = FAISSIndex(dimension=3072)

documents = ["Doc 1", "Doc 2", "Doc 3"]
embeddings = get_embeddings_batch(documents)
index.add(embeddings, documents)

query_emb = get_embedding("search query")
results = index.search(query_emb, top_k=2)
```

### Maximal Marginal Relevance (MMR)

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def mmr_search(
    query_embedding: list[float],
    document_embeddings: list[list[float]],
    documents: list[str],
    top_k: int = 10,
    diversity: float = 0.5
) -> list[tuple[str, float]]:
    """
    Maximal Marginal Relevance for diverse results.

    Args:
        diversity: 0 = pure relevance, 1 = pure diversity
    """
    query = np.array(query_embedding).reshape(1, -1)
    docs = np.array(document_embeddings)

    # Initial similarities
    similarities = cosine_similarity(query, docs)[0]

    # Track selected indices
    selected = []
    candidates = list(range(len(documents)))

    for _ in range(min(top_k, len(documents))):
        if not candidates:
            break

        if not selected:
            # First selection: most similar to query
            best_idx = candidates[np.argmax(similarities[candidates])]
        else:
            # MMR selection
            mmr_scores = []
            for idx in candidates:
                relevance = similarities[idx]

                # Max similarity to already selected
                selected_embs = docs[selected]
                redundancy = max(
                    cosine_similarity([docs[idx]], selected_embs)[0]
                )

                mmr = (1 - diversity) * relevance - diversity * redundancy
                mmr_scores.append(mmr)

            best_idx = candidates[np.argmax(mmr_scores)]

        selected.append(best_idx)
        candidates.remove(best_idx)

    return [(documents[idx], float(similarities[idx])) for idx in selected]
```

---

## Chunking Strategies

### Token-Based Chunking

```python
import tiktoken

def chunk_by_tokens(
    text: str,
    max_tokens: int = 500,
    overlap_tokens: int = 50,
    model: str = "text-embedding-3-large"
) -> list[str]:
    """Split text by token count."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    chunks = []
    start = 0

    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        start = end - overlap_tokens

    return chunks

# Usage
text = "Long document text..." * 100
chunks = chunk_by_tokens(text, max_tokens=256, overlap_tokens=25)
```

### Semantic Chunking

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_semantic(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[str]:
    """Split at natural boundaries."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)
```

### Sentence-Based Chunking

```python
import nltk
nltk.download('punkt', quiet=True)

def chunk_by_sentences(
    text: str,
    sentences_per_chunk: int = 5,
    overlap_sentences: int = 1
) -> list[str]:
    """Split by sentences for semantic coherence."""
    sentences = nltk.sent_tokenize(text)
    chunks = []
    start = 0

    while start < len(sentences):
        end = start + sentences_per_chunk
        chunk = " ".join(sentences[start:end])
        chunks.append(chunk)
        start = end - overlap_sentences

    return chunks
```

---

## Caching

### Redis Cache

```python
import redis
import json
import hashlib
from typing import Callable

class RedisEmbeddingCache:
    """Production-ready Redis cache for embeddings."""

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        ttl_days: int = 30,
        prefix: str = "emb"
    ):
        self.client = redis.from_url(redis_url)
        self.ttl = 86400 * ttl_days
        self.prefix = prefix

    def _key(self, text: str, model: str) -> str:
        content = f"{model}:{text}"
        hash_val = hashlib.sha256(content.encode()).hexdigest()
        return f"{self.prefix}:{hash_val}"

    def get(self, text: str, model: str) -> list[float] | None:
        data = self.client.get(self._key(text, model))
        return json.loads(data) if data else None

    def set(self, text: str, model: str, embedding: list[float]):
        self.client.setex(
            self._key(text, model),
            self.ttl,
            json.dumps(embedding)
        )

    def get_or_compute(
        self,
        text: str,
        model: str,
        compute_fn: Callable[[str], list[float]]
    ) -> list[float]:
        """Get from cache or compute and store."""
        cached = self.get(text, model)
        if cached:
            return cached

        embedding = compute_fn(text)
        self.set(text, model, embedding)
        return embedding

    def get_batch_cached(
        self,
        texts: list[str],
        model: str,
        compute_fn: Callable[[list[str]], list[list[float]]]
    ) -> list[list[float]]:
        """Batch get with cache-aware computation."""
        results = {}
        uncached_texts = []
        uncached_indices = []

        # Check cache
        for i, text in enumerate(texts):
            cached = self.get(text, model)
            if cached:
                results[i] = cached
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)

        # Compute uncached
        if uncached_texts:
            new_embeddings = compute_fn(uncached_texts)
            for idx, text, emb in zip(uncached_indices, uncached_texts, new_embeddings):
                self.set(text, model, emb)
                results[idx] = emb

        return [results[i] for i in range(len(texts))]

# Usage
cache = RedisEmbeddingCache()

def compute_embedding(text: str) -> list[float]:
    return get_embedding(text, "text-embedding-3-large")

embedding = cache.get_or_compute("Hello", "text-embedding-3-large", compute_embedding)
```

### File-Based Cache (Development)

```python
import json
import hashlib
from pathlib import Path

class FileEmbeddingCache:
    """Simple file-based cache for development."""

    def __init__(self, cache_dir: str = ".embedding_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _path(self, text: str, model: str) -> Path:
        content = f"{model}:{text}"
        hash_val = hashlib.sha256(content.encode()).hexdigest()
        return self.cache_dir / f"{hash_val}.json"

    def get(self, text: str, model: str) -> list[float] | None:
        path = self._path(text, model)
        if path.exists():
            return json.loads(path.read_text())
        return None

    def set(self, text: str, model: str, embedding: list[float]):
        self._path(text, model).write_text(json.dumps(embedding))
```

---

## Multimodal Embeddings

### Cohere Embed-v4 (Text + Image)

```python
import cohere
import base64
from pathlib import Path

co = cohere.Client()

def embed_image(image_path: str) -> list[float]:
    """Embed an image with Cohere embed-v4."""
    # Read and encode image
    image_bytes = Path(image_path).read_bytes()
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    response = co.embed(
        model="embed-v4",
        input_type="image",
        images=[image_b64]
    )
    return response.embeddings[0]

def embed_mixed(
    texts: list[str] = None,
    image_paths: list[str] = None
) -> list[list[float]]:
    """Embed text and images in same space."""
    images_b64 = []
    if image_paths:
        for path in image_paths:
            image_bytes = Path(path).read_bytes()
            images_b64.append(base64.standard_b64encode(image_bytes).decode("utf-8"))

    response = co.embed(
        model="embed-v4",
        input_type="search_document",
        texts=texts or [],
        images=images_b64 or []
    )
    return response.embeddings

# Usage - cross-modal search
text_emb = embed_mixed(texts=["A cat sitting on a couch"])[0]
image_emb = embed_image("cat_photo.jpg")

# These can be compared directly!
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity([text_emb], [image_emb])[0][0]
```

### CLIP (Local Multimodal)

```python
from sentence_transformers import SentenceTransformer
from PIL import Image

# Load CLIP model
model = SentenceTransformer("clip-ViT-B-32")

def embed_text_clip(text: str) -> list[float]:
    """Embed text with CLIP."""
    return model.encode(text, convert_to_numpy=True).tolist()

def embed_image_clip(image_path: str) -> list[float]:
    """Embed image with CLIP."""
    image = Image.open(image_path)
    return model.encode(image, convert_to_numpy=True).tolist()

# Usage
text_emb = embed_text_clip("A sunset over mountains")
image_emb = embed_image_clip("sunset.jpg")
```

---

## Hybrid Search

### BM25 + Dense Embeddings

```python
from rank_bm25 import BM25Okapi
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class HybridSearch:
    """Combine BM25 and dense embeddings."""

    def __init__(
        self,
        documents: list[str],
        embeddings: list[list[float]],
        alpha: float = 0.5  # 0 = pure BM25, 1 = pure dense
    ):
        self.documents = documents
        self.embeddings = np.array(embeddings)
        self.alpha = alpha

        # Build BM25 index
        tokenized = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def search(
        self,
        query: str,
        query_embedding: list[float],
        top_k: int = 10
    ) -> list[tuple[str, float]]:
        """Hybrid search combining BM25 and dense scores."""
        # BM25 scores
        bm25_scores = self.bm25.get_scores(query.lower().split())
        bm25_scores = bm25_scores / (bm25_scores.max() + 1e-6)  # Normalize

        # Dense scores
        query_vec = np.array(query_embedding).reshape(1, -1)
        dense_scores = cosine_similarity(query_vec, self.embeddings)[0]

        # Combine
        hybrid_scores = (1 - self.alpha) * bm25_scores + self.alpha * dense_scores

        # Get top-k
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]

        return [
            (self.documents[idx], float(hybrid_scores[idx]))
            for idx in top_indices
        ]

# Usage
docs = ["Python programming", "Java development", "Machine learning"]
embs = get_embeddings_batch(docs)

search = HybridSearch(docs, embs, alpha=0.7)
query = "coding in Python"
query_emb = get_embedding(query)

results = search.search(query, query_emb, top_k=2)
```

### BGE-M3 Hybrid (Dense + Sparse)

```python
from FlagEmbedding import BGEM3FlagModel
import numpy as np

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

class BGEM3HybridSearch:
    """Native hybrid search with BGE-M3."""

    def __init__(self, documents: list[str]):
        self.documents = documents
        output = model.encode(documents, return_dense=True, return_sparse=True)
        self.dense_embeddings = output["dense_vecs"]
        self.sparse_embeddings = output["lexical_weights"]

    def search(
        self,
        query: str,
        top_k: int = 10,
        dense_weight: float = 0.7
    ) -> list[tuple[str, float]]:
        """Search using both dense and sparse representations."""
        query_output = model.encode([query], return_dense=True, return_sparse=True)
        query_dense = query_output["dense_vecs"][0]
        query_sparse = query_output["lexical_weights"][0]

        scores = []
        for i, doc in enumerate(self.documents):
            # Dense score (cosine)
            dense_score = np.dot(query_dense, self.dense_embeddings[i]) / (
                np.linalg.norm(query_dense) * np.linalg.norm(self.dense_embeddings[i])
            )

            # Sparse score (lexical overlap)
            sparse_score = self._sparse_similarity(query_sparse, self.sparse_embeddings[i])

            # Combine
            final_score = dense_weight * dense_score + (1 - dense_weight) * sparse_score
            scores.append((doc, final_score))

        return sorted(scores, key=lambda x: -x[1])[:top_k]

    def _sparse_similarity(self, q_sparse: dict, d_sparse: dict) -> float:
        """Calculate sparse vector similarity."""
        score = 0.0
        for token, q_weight in q_sparse.items():
            if token in d_sparse:
                score += q_weight * d_sparse[token]
        return score
```

---

## Vector Database Integration

### Qdrant

```python
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

client = QdrantClient("localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
)

# Add documents
documents = ["Doc 1", "Doc 2", "Doc 3"]
embeddings = get_embeddings_batch(documents)

points = [
    PointStruct(
        id=i,
        vector=emb,
        payload={"text": doc, "source": "example"}
    )
    for i, (emb, doc) in enumerate(zip(embeddings, documents))
]
client.upsert("documents", points)

# Search
query_emb = get_embedding("search query")
results = client.search(
    collection_name="documents",
    query_vector=query_emb,
    limit=10
)
for result in results:
    print(f"Score: {result.score:.4f} | {result.payload['text']}")
```

### pgvector (PostgreSQL)

```python
import psycopg2
from pgvector.psycopg2 import register_vector

conn = psycopg2.connect("postgresql://user:pass@localhost/db")
register_vector(conn)

cur = conn.cursor()

# Create table with vector column
cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(3072)
    )
""")

# Add documents
documents = ["Doc 1", "Doc 2", "Doc 3"]
embeddings = get_embeddings_batch(documents)

for doc, emb in zip(documents, embeddings):
    cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (doc, emb)
    )
conn.commit()

# Search (cosine distance)
query_emb = get_embedding("search query")
cur.execute("""
    SELECT content, 1 - (embedding <=> %s) as similarity
    FROM documents
    ORDER BY embedding <=> %s
    LIMIT 10
""", (query_emb, query_emb))

for row in cur.fetchall():
    print(f"Score: {row[1]:.4f} | {row[0]}")
```

### Pinecone

```python
from pinecone import Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")

# Create index
pc.create_index(
    name="documents",
    dimension=3072,
    metric="cosine",
    spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
)

index = pc.Index("documents")

# Add documents
documents = ["Doc 1", "Doc 2", "Doc 3"]
embeddings = get_embeddings_batch(documents)

vectors = [
    {"id": str(i), "values": emb, "metadata": {"text": doc}}
    for i, (emb, doc) in enumerate(zip(embeddings, documents))
]
index.upsert(vectors)

# Search
query_emb = get_embedding("search query")
results = index.query(vector=query_emb, top_k=10, include_metadata=True)

for match in results["matches"]:
    print(f"Score: {match['score']:.4f} | {match['metadata']['text']}")
```

---

*For more examples, see the [templates.md](templates.md) file for complete pipeline templates.*
