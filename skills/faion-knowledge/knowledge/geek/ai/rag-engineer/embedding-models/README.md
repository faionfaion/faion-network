# Embedding Models

API and local models for generating text embeddings.

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
```

### Batch Processing (Recommended)

```python
def get_embeddings_batch(
    texts: list[str],
    model: str = "text-embedding-3-large",
    batch_size: int = 2048  # OpenAI limit
) -> list[list[float]]:
    """Get embeddings for multiple texts efficiently."""
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(
            input=batch,
            model=model
        )
        # Preserve order (API may return out of order)
        sorted_embeddings = sorted(response.data, key=lambda x: x.index)
        all_embeddings.extend([e.embedding for e in sorted_embeddings])

    return all_embeddings
```

### Matryoshka Embeddings (Dimension Reduction)

OpenAI's text-embedding-3 models support native dimension reduction:

```python
def get_embedding_reduced(
    text: str,
    model: str = "text-embedding-3-large",
    dimensions: int = 256  # Reduce from 3072 to 256
) -> list[float]:
    """Get reduced-dimension embedding (cheaper storage, similar quality)."""
    response = client.embeddings.create(
        input=text,
        model=model,
        dimensions=dimensions  # 256, 512, 1024, 1536, 3072
    )
    return response.data[0].embedding
```

**Dimension vs Quality Trade-off:**

| Dimensions | Storage | MTEB Score (approx) | Use Case |
|------------|---------|---------------------|----------|
| 3072 | 12KB | 64.6% | Maximum quality |
| 1536 | 6KB | 64.2% | Balanced |
| 1024 | 4KB | 63.8% | Good for most |
| 512 | 2KB | 62.5% | Cost-sensitive |
| 256 | 1KB | 60.1% | High-volume, basic similarity |

---

## Mistral Embeddings

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

# Batch processing
def get_mistral_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Batch embeddings with Mistral."""
    response = client.embeddings.create(
        model="mistral-embed",
        inputs=texts
    )
    return [e.embedding for e in response.data]
```

---

## Cohere Embeddings

```python
import cohere

co = cohere.Client("YOUR_API_KEY")

def get_cohere_embedding(
    texts: list[str],
    input_type: str = "search_document"  # or "search_query"
) -> list[list[float]]:
    """
    Get Cohere embeddings.

    input_type options:
    - "search_document": For documents to be searched
    - "search_query": For search queries
    - "classification": For classification tasks
    - "clustering": For clustering tasks
    """
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type=input_type,
        truncate="END"  # or "START", "NONE"
    )
    return response.embeddings
```

**Cohere Best Practices:**
- Use `input_type="search_document"` for indexing
- Use `input_type="search_query"` for queries
- This asymmetric approach improves retrieval quality

---

## Local Models (sentence-transformers)

### Installation

```bash
pip install sentence-transformers
# For GPU support
pip install sentence-transformers[gpu]
```

### Basic Usage

```python
from sentence_transformers import SentenceTransformer

# Load model (downloads on first use)
model = SentenceTransformer("BAAI/bge-large-en-v1.5")

# Single text
embedding = model.encode("Your text here")

# Batch processing (automatic batching)
texts = ["Text 1", "Text 2", "Text 3"]
embeddings = model.encode(texts, show_progress_bar=True)
```

### GPU Acceleration

```python
import torch
from sentence_transformers import SentenceTransformer

# Auto-detect GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("BAAI/bge-large-en-v1.5", device=device)

# Encode with GPU
embeddings = model.encode(
    texts,
    batch_size=32,  # Adjust based on GPU memory
    show_progress_bar=True,
    convert_to_numpy=True,  # Return numpy array
    normalize_embeddings=True  # L2 normalize for cosine similarity
)
```

### Popular Local Models

```python
# Best quality (slow)
model = SentenceTransformer("BAAI/bge-m3")

# Good quality, balanced
model = SentenceTransformer("BAAI/bge-large-en-v1.5")
model = SentenceTransformer("intfloat/e5-large-v2")

# Fast inference
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Multilingual
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Long context (8K tokens)
model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
```

### BGE-M3 (Best Local Model)

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

# Dense embeddings (default)
embeddings = model.encode(texts)["dense_vecs"]

# Sparse embeddings (for hybrid search)
sparse = model.encode(texts, return_sparse=True)["lexical_weights"]

# Both dense + sparse
output = model.encode(texts, return_dense=True, return_sparse=True)
```

---

## Production Patterns

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

    async def process_batch(batch: list[str]) -> list[list[float]]:
        async with semaphore:
            response = await async_client.embeddings.create(
                input=batch,
                model=model
            )
            sorted_data = sorted(response.data, key=lambda x: x.index)
            return [e.embedding for e in sorted_data]

    # Create batches
    batches = [texts[i:i+batch_size] for i in range(0, len(texts), batch_size)]

    # Process concurrently
    results = await asyncio.gather(*[process_batch(b) for b in batches])

    # Flatten
    return [emb for batch in results for emb in batch]
```

### Retry with Exponential Backoff

```python
import time
import random
from openai import RateLimitError, APIError

def get_embedding_with_retry(
    text: str,
    model: str = "text-embedding-3-large",
    max_retries: int = 5
) -> list[float]:
    """Robust embedding with retry logic."""
    for attempt in range(max_retries):
        try:
            return get_embedding(text, model)
        except RateLimitError:
            wait = (2 ** attempt) + random.random()
            print(f"Rate limited. Waiting {wait:.1f}s...")
            time.sleep(wait)
        except APIError as e:
            if attempt == max_retries - 1:
                raise
            wait = 1 + random.random()
            print(f"API error: {e}. Retrying in {wait:.1f}s...")
            time.sleep(wait)

    raise Exception("Max retries exceeded")
```

### Embedding Pipeline

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class EmbeddingConfig:
    model: str = "text-embedding-3-large"
    dimensions: Optional[int] = None
    chunk_size: int = 500
    chunk_overlap: int = 50
    batch_size: int = 100
    cache_enabled: bool = True

class EmbeddingPipeline:
    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self.cache = EmbeddingCache() if config.cache_enabled else None

    def process_document(self, text: str) -> list[list[float]]:
        """Full pipeline: chunk -> cache check -> embed."""
        # 1. Chunk
        chunks = chunk_by_tokens(
            text,
            max_tokens=self.config.chunk_size,
            overlap_tokens=self.config.chunk_overlap
        )

        # 2. Check cache
        uncached = []
        cached_embeddings = {}

        if self.cache:
            for i, chunk in enumerate(chunks):
                cached = self.cache.get(chunk, self.config.model)
                if cached:
                    cached_embeddings[i] = cached
                else:
                    uncached.append((i, chunk))
        else:
            uncached = list(enumerate(chunks))

        # 3. Embed uncached
        if uncached:
            indices, texts = zip(*uncached)
            new_embeddings = get_embeddings_batch(
                list(texts),
                model=self.config.model
            )

            for idx, emb in zip(indices, new_embeddings):
                cached_embeddings[idx] = emb
                if self.cache:
                    self.cache.set(chunks[idx], self.config.model, emb)

        # 4. Return in order
        return [cached_embeddings[i] for i in range(len(chunks))]
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **Rate limit errors** | Too many requests | Batch requests, add retry logic |
| **Token limit exceeded** | Text too long | Chunk text before embedding |
| **Poor retrieval quality** | Wrong model/chunk size | Benchmark different configs |
| **High latency** | Network/model size | Use local models or caching |
| **High costs** | Too many API calls | Cache, deduplicate, use smaller models |
| **Dimension mismatch** | Mixed models in DB | Use consistent model per index |

### Quality Debugging

```python
def debug_similarity(
    query: str,
    documents: list[str],
    model: str = "text-embedding-3-large"
) -> None:
    """Debug why certain documents rank high/low."""
    query_emb = np.array(get_embedding(query, model))
    doc_embs = np.array(get_embeddings_batch(documents, model))

    similarities = cosine_similarity([query_emb], doc_embs)[0]

    print(f"Query: {query[:100]}...")
    print("-" * 50)

    for doc, sim in sorted(zip(documents, similarities), key=lambda x: -x[1]):
        print(f"Score: {sim:.4f} | {doc[:80]}...")
```

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

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Mistral AI Embeddings](https://docs.mistral.ai/capabilities/embeddings/)
- [Cohere Embed v3](https://docs.cohere.com/docs/cohere-embed)
- [BGE-M3 Model](https://huggingface.co/BAAI/bge-m3)
- [Sentence Transformers](https://www.sbert.net/)
