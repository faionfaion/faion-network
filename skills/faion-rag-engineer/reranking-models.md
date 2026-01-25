---
id: reranking-models
name: "Reranking Models & Services"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Reranking Models & Services

API-based reranking services and production patterns.

## Cohere Rerank

```python
import cohere

co = cohere.Client(api_key="your-api-key")

def cohere_rerank(
    query: str,
    documents: list[str],
    top_n: int = 5,
    model: str = "rerank-english-v3.0"
) -> list[dict]:
    """
    Rerank documents using Cohere Rerank API.
    """
    response = co.rerank(
        query=query,
        documents=documents,
        top_n=top_n,
        model=model
    )

    return [
        {
            "document": documents[result.index],
            "score": result.relevance_score,
            "index": result.index
        }
        for result in response.results
    ]

# Usage
documents = [
    "Python is a programming language.",
    "Machine learning uses Python extensively.",
    "JavaScript is used for web development.",
    "Python has great ML libraries like scikit-learn.",
]

results = cohere_rerank(
    query="What programming language is best for ML?",
    documents=documents,
    top_n=3
)

for r in results:
    print(f"Score: {r['score']:.4f} - {r['document']}")
```

## Jina Rerank

```python
import requests

def jina_rerank(
    query: str,
    documents: list[str],
    top_n: int = 5,
    api_key: str = None
) -> list[dict]:
    """
    Rerank using Jina AI Reranker.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.jina.ai/v1/rerank",
        headers=headers,
        json={
            "query": query,
            "documents": documents,
            "top_n": top_n,
            "model": "jina-reranker-v2-base-multilingual"
        }
    )

    data = response.json()

    return [
        {
            "document": documents[r["index"]],
            "score": r["relevance_score"],
            "index": r["index"]
        }
        for r in data["results"]
    ]
```

## Voyage AI Rerank

```python
import voyageai

vo = voyageai.Client(api_key="your-api-key")

def voyage_rerank(
    query: str,
    documents: list[str],
    top_k: int = 5
) -> list[dict]:
    """
    Rerank using Voyage AI.
    """
    response = vo.rerank(
        query=query,
        documents=documents,
        model="rerank-2",
        top_k=top_k
    )

    return [
        {
            "document": documents[r.index],
            "score": r.relevance_score,
            "index": r.index
        }
        for r in response.results
    ]
```

## LLM-based Reranking

```python
from openai import OpenAI
import json

client = OpenAI()

def llm_rerank(
    query: str,
    documents: list[str],
    top_k: int = 5
) -> list[dict]:
    """
    Rerank using LLM (slower but can handle complex queries).
    """
    # Format documents with indices
    doc_list = "\n".join([
        f"[{i}] {doc[:500]}"  # Truncate long docs
        for i, doc in enumerate(documents)
    ])

    prompt = f"""Given the query and documents, rank the documents by relevance.

Query: {query}

Documents:
{doc_list}

Return a JSON array of document indices ordered by relevance (most relevant first).
Only include the top {top_k} most relevant documents.
Format: {{"rankings": [index1, index2, ...]}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0
    )

    result = json.loads(response.choices[0].message.content)
    rankings = result.get("rankings", [])[:top_k]

    return [
        {
            "document": documents[idx],
            "rank": rank + 1,
            "index": idx
        }
        for rank, idx in enumerate(rankings)
        if idx < len(documents)
    ]

def llm_rerank_with_scores(
    query: str,
    documents: list[str],
    top_k: int = 5
) -> list[dict]:
    """
    LLM rerank with relevance scores.
    """
    doc_list = "\n".join([
        f"[{i}] {doc[:500]}"
        for i, doc in enumerate(documents)
    ])

    prompt = f"""Score each document's relevance to the query from 0-10.

Query: {query}

Documents:
{doc_list}

Return JSON with scores: {{"scores": [{{"index": 0, "score": 8}}, ...]}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0
    )

    result = json.loads(response.choices[0].message.content)
    scores = sorted(result["scores"], key=lambda x: x["score"], reverse=True)

    return [
        {
            "document": documents[s["index"]],
            "score": s["score"] / 10.0,
            "index": s["index"]
        }
        for s in scores[:top_k]
        if s["index"] < len(documents)
    ]
```

## Production Reranking Service

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import logging
import time
import numpy as np

class RerankerType(Enum):
    CROSS_ENCODER = "cross_encoder"
    COHERE = "cohere"
    JINA = "jina"
    LLM = "llm"

@dataclass
class RerankerConfig:
    reranker_type: RerankerType = RerankerType.CROSS_ENCODER
    model: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"
    batch_size: int = 32
    timeout: float = 30.0
    fallback_to_original: bool = True

class RerankerService:
    """Production reranking service with fallback."""

    def __init__(self, config: Optional[RerankerConfig] = None):
        self.config = config or RerankerConfig()
        self.logger = logging.getLogger(__name__)
        self._init_reranker()

    def _init_reranker(self):
        """Initialize reranker based on type."""
        if self.config.reranker_type == RerankerType.CROSS_ENCODER:
            from sentence_transformers import CrossEncoder
            self.reranker = CrossEncoder(self.config.model)
        elif self.config.reranker_type == RerankerType.COHERE:
            import cohere
            self.reranker = cohere.Client()

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5,
        metadata: Optional[List[Dict]] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents with error handling and metrics.
        """
        start_time = time.time()

        try:
            if self.config.reranker_type == RerankerType.CROSS_ENCODER:
                results = self._cross_encoder_rerank(query, documents, top_k)
            elif self.config.reranker_type == RerankerType.COHERE:
                results = self._cohere_rerank(query, documents, top_k)
            else:
                results = self._llm_rerank(query, documents, top_k)

            # Attach metadata if provided
            if metadata:
                for result in results:
                    idx = result["index"]
                    if idx < len(metadata):
                        result["metadata"] = metadata[idx]

            latency = time.time() - start_time
            self.logger.info(f"Reranking completed in {latency:.3f}s")

            return results

        except Exception as e:
            self.logger.error(f"Reranking failed: {e}")

            if self.config.fallback_to_original:
                # Return original order
                return [
                    {"document": doc, "score": 1.0 - i/len(documents), "index": i}
                    for i, doc in enumerate(documents[:top_k])
                ]
            raise

    def _cross_encoder_rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int
    ) -> List[Dict]:
        """Cross-encoder reranking."""
        pairs = [[query, doc] for doc in documents]
        scores = self.reranker.predict(pairs, batch_size=self.config.batch_size)

        sorted_indices = np.argsort(scores)[::-1][:top_k]

        return [
            {"document": documents[i], "score": float(scores[i]), "index": i}
            for i in sorted_indices
        ]

    def _cohere_rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int
    ) -> List[Dict]:
        """Cohere reranking."""
        response = self.reranker.rerank(
            query=query,
            documents=documents,
            top_n=top_k,
            model="rerank-english-v3.0"
        )

        return [
            {
                "document": documents[r.index],
                "score": r.relevance_score,
                "index": r.index
            }
            for r in response.results
        ]

    def _llm_rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int
    ) -> List[Dict]:
        """LLM-based reranking."""
        return llm_rerank_with_scores(query, documents, top_k)
```

## Model Selection Guide

### API Services

| Service | Best For | Cost | Latency |
|---------|----------|------|---------|
| **Cohere Rerank** | English, high quality | $$$ | 100-300ms |
| **Jina Rerank** | Multilingual, balanced | $$ | 150-400ms |
| **Voyage AI** | Domain-specific | $$$ | 100-300ms |
| **LLM (GPT-4)** | Complex queries | $$$$ | 500-2000ms |

### Local Models

| Model | Size | Latency | Quality |
|-------|------|---------|---------|
| ms-marco-MiniLM-L-6-v2 | Small | 20-50ms | Good |
| ms-marco-MiniLM-L-12-v2 | Medium | 40-100ms | Better |
| ms-marco-electra-base | Large | 80-200ms | Best |
| mmarco-mMiniLMv2-L12 | Medium | 40-100ms | Multilingual |

## Integration Examples

### FastAPI Service

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class RerankRequest(BaseModel):
    query: str
    documents: List[str]
    top_k: int = 5

class RerankResponse(BaseModel):
    results: List[Dict[str, Any]]
    latency: float

reranker = RerankerService(
    RerankerConfig(reranker_type=RerankerType.CROSS_ENCODER)
)

@app.post("/rerank", response_model=RerankResponse)
async def rerank_endpoint(request: RerankRequest):
    """Rerank documents endpoint."""
    start = time.time()

    try:
        results = reranker.rerank(
            query=request.query,
            documents=request.documents,
            top_k=request.top_k
        )

        return RerankResponse(
            results=results,
            latency=time.time() - start
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### LangChain Integration

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

# Setup retriever
base_retriever = vector_store.as_retriever(search_kwargs={"k": 50})

# Add Cohere reranking
compressor = CohereRerank(
    cohere_api_key="your-api-key",
    model="rerank-english-v3.0",
    top_n=5
)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# Use in chain
docs = compression_retriever.get_relevant_documents(
    "What is the capital of France?"
)
```

## Sources

- [Cohere Rerank API](https://docs.cohere.com/docs/reranking)
- [Jina Reranker](https://jina.ai/reranker/)
- [Voyage AI Rerank](https://docs.voyageai.com/docs/reranker)
- [MixedBread AI](https://www.mixedbread.ai/docs/reranking)
