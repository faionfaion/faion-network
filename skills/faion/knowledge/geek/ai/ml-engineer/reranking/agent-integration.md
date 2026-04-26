# Agent Integration — Reranking

## When to use
- RAG pipeline where initial vector retrieval produces noisy or inconsistent top results
- First-stage retrieval uses a fast bi-encoder and you have a latency budget of 200ms+ beyond it
- Hybrid search (BM25 + dense) needs a single score for final ranking
- Domain-critical applications: legal, medical, enterprise knowledge bases where precision matters
- Corpus size > 10K documents where bi-encoder recall starts to degrade

## When NOT to use
- Real-time autocomplete or sub-100ms latency requirements — cross-encoder overhead is prohibitive
- Fewer than 10 candidate documents retrieved — marginal improvement does not justify cost
- Simple keyword-match use cases with deterministic answer lookup
- High-volume low-value queries where API cost exceeds quality benefit

## Where it fails / limitations
- Reranker cannot recover documents that first-stage retrieval missed — bad recall at stage 1 is not fixed
- Cross-encoders score (query, doc) pairs independently — they cannot reason about diversity or de-duplicate
- Self-hosted rerankers on CPU are slow (100-400ms for 50 docs with MiniLM-L12); GPU required for production throughput
- Cohere/Jina API rerankers add 200-400ms network latency and per-request cost that compounds at scale
- Listwise rerankers (BGE Layerwise/Gemma) are accurate but slow — unsuitable for interactive response time

## Agentic workflow
A Claude subagent drives reranking by first emitting a retrieval call to the vector database, receiving the top-50 to top-100 candidates, then calling the reranker API or local model with the (query, candidates) batch. The agent inspects the reranked scores, applies a cutoff threshold (e.g., discard below 0.3), and passes the refined top-5 to the answer-generation step. For self-hosted models the agent invokes a Python subprocess or FastAPI endpoint wrapping sentence-transformers.

### Recommended subagents
- `faion-sdd-executor-agent` — when reranking pipeline setup is a tracked SDD task
- General Claude subagent with tool access — drives retrieval → reranking → generation as a sequential tool-call chain

### Prompt pattern
```
Given the query: <query>
And these candidate passages (indexed 0–N):
<passages>

Score each passage for relevance to the query on a 0–1 scale.
Return a JSON array: [{"index": i, "score": f}, ...]
Rank by score descending.
```

```python
# Using sentence-transformers cross-encoder
from sentence_transformers import CrossEncoder
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")
pairs = [(query, doc) for doc in candidates]
scores = model.predict(pairs)
ranked = sorted(zip(scores, candidates), reverse=True)
top_k = [doc for _, doc in ranked[:5]]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `sentence-transformers` | Local cross-encoder reranking | `pip install sentence-transformers` · sbert.net |
| `rerankers` (AnswerDotAI) | Unified API for multiple rerankers | `pip install rerankers` · github.com/AnswerDotAI/rerankers |
| `flashrank` | Lightweight CPU-friendly reranker | `pip install flashrank` · github.com/PrithivirajDamodaran/FlashRank |
| `llama-index` | Reranking nodes built-in | `pip install llama-index` · docs.llamaindex.ai |
| `langchain` | RerankerDocumentCompressor | `pip install langchain` · python.langchain.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cohere Rerank API | SaaS | Yes — REST JSON | `rerank-v3.5` and `rerank-v3.5-nimble`; 100+ languages; simple HTTP call |
| Jina AI Reranker API | SaaS | Yes — REST JSON | `jina-reranker-v3`; SOTA multilingual BEIR 61.94; free tier available |
| Pinecone Rerank | SaaS | Yes — via Pinecone client | Integrated with Pinecone index; no separate infra |
| ZeroEntropy | SaaS | Yes — REST | Proprietary reranker; claims +28% vs baseline |
| Hugging Face Inference API | SaaS/OSS | Yes — REST | Serve BGE or MiniLM via HF endpoints |
| Qdrant (built-in re-score) | OSS | Yes — REST/gRPC | Vector re-score pass using quantized + full vectors |

## Templates & scripts
Inline script — self-hosted reranking endpoint (< 50 lines):

```python
# reranker_server.py — FastAPI wrapper around sentence-transformers
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import CrossEncoder
import torch

app = FastAPI()
MODEL = CrossEncoder("BAAI/bge-reranker-v2-m3", device="cuda" if torch.cuda.is_available() else "cpu")

class RerankRequest(BaseModel):
    query: str
    documents: list[str]
    top_k: int = 10

@app.post("/rerank")
def rerank(req: RerankRequest):
    pairs = [(req.query, doc) for doc in req.documents]
    scores = MODEL.predict(pairs).tolist()
    ranked = sorted(
        [{"index": i, "document": doc, "score": scores[i]} for i, doc in enumerate(req.documents)],
        key=lambda x: x["score"],
        reverse=True,
    )
    return {"results": ranked[: req.top_k]}
```

See `templates.md` for Cohere API integration template and LangChain/LlamaIndex wrappers.

## Best practices
- Always retrieve 5–10x more candidates than the final top-k you send to the LLM (retrieve 50, rerank to 5-10)
- Use the `AnswerDotAI/rerankers` library as an abstraction layer — swap models without changing pipeline code
- For multilingual corpora use Jina Reranker v3 or BGE-M3 — MiniLM is English-only
- Apply a score threshold (typically 0.25–0.4) to hard-filter low-confidence candidates before passing to LLM
- Cache reranker results by (query_hash, doc_hash) for repeated queries — saves latency and cost
- Run A/B test comparing bi-encoder-only vs bi-encoder+reranker on your actual queries before committing to reranker overhead
- In hybrid BM25 + dense pipelines, always rerank after RRF fusion — the fused ranks are not calibrated scores

## AI-agent gotchas
- Agents must cap the candidate list sent to a cross-encoder: feeding 200+ documents will exceed latency or API limits — cap at 100 with a hard coded guard
- Cohere and Jina APIs have per-document token limits (512–4096 tokens); agents must chunk long documents before reranking
- LLM-as-reranker (asking Claude to rank passages) is an option but adds 1-2s and significant cost per query — only use if no dedicated reranker is available
- Cross-encoder scores are not calibrated probabilities across different models — do not compare raw scores between BGE and MiniLM
- When the agent runs reranking inside a multi-turn conversation, re-run reranking per turn; cached results from prior turns may no longer match the refined query

## References
- https://www.sbert.net/examples/applications/cross-encoder/README.html
- https://docs.cohere.com/docs/reranking
- https://jina.ai/models/jina-reranker-v3/
- https://github.com/AnswerDotAI/rerankers
- https://arxiv.org/abs/2004.12832 (ColBERT)
- https://arxiv.org/html/2509.25085v2 (Jina Reranker v3)
- https://huggingface.co/spaces/mteb/leaderboard
- https://www.pinecone.io/learn/series/rag/rerankers/
