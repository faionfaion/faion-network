# Agent Integration — RAG Architecture

## When to use
- Starting a new RAG system from scratch and needing to make foundational decisions (chunking strategy, vector DB, retrieval approach)
- Evaluating whether RAG is the right approach vs. fine-tuning or long-context LLM
- Diagnosing production RAG quality problems (low faithfulness, hallucinations, slow retrieval)
- Designing multi-index or agentic RAG variants that go beyond a single vector store
- Domain: any custom document Q&A, chatbot, or search use case where the data changes frequently

## When NOT to use
- Data is static and small enough to fit in a single LLM context window — skip RAG, use long-context prompting
- Questions require real-time web data — use tool-calling with search APIs instead
- Fine-tuning already achieved acceptable accuracy on a stable, closed corpus
- Team has no infrastructure for a vector database — consider pgvector extension on existing Postgres before introducing a new service

## Where it fails / limitations
- Faithfulness breaks when the retrieval step returns off-topic chunks and the LLM generates from prior knowledge instead
- Static top-k retrieval causes both over-retrieval (noisy context) and under-retrieval (missing key chunks) for queries of varying complexity
- Context ordering matters but is often ignored — most relevant chunk should appear first; LLMs show recency bias
- Hybrid search requires both a vector index and a keyword index; schema changes must be synchronized across both
- Prompt templates that don't explicitly forbid hallucination ("only use the provided context") produce grounded-sounding but invented answers
- Latency budget must account for: embedding query + vector search + (optional rerank) + LLM generation — each stage can independently spike

## Agentic workflow
A planning subagent reads the corpus description and query types, selects the pipeline configuration (chunking strategy, embedding model, retrieval mode, reranking flag), and generates a structured config document. An implementation subagent executes the pipeline: load → chunk → embed → index. A retrieval subagent handles query-time flow: embed query → search → (rerank) → assemble context → prompt → generate. A quality subagent runs a small evaluation set and flags recall/faithfulness scores below thresholds. Human review is required before switching vector DB or embedding model on an active production index.

### Recommended subagents
- `faion-sdd-executor-agent` — execute RAG pipeline setup as a series of SDD tasks with quality gates at each stage

### Prompt pattern
```
You are a RAG assistant. Answer the question using ONLY the context below.
If the context does not contain enough information, respond:
"I don't have enough information to answer this question."
Do not use any external knowledge.

Context:
{{#each chunks}}
[Source: {{this.source}}, Chunk {{this.index}}]
{{this.text}}

{{/each}}

Question: {{question}}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain` | End-to-end RAG pipeline: loaders, splitters, retrievers, chains | `pip install langchain langchain-community` · https://python.langchain.com |
| `llama-index` | Alternative framework: index types, query engines, evaluators | `pip install llama-index` · https://docs.llamaindex.ai |
| `haystack` | RAG pipelines with pipeline DSL; strong evaluation tooling | `pip install haystack-ai` · https://haystack.deepset.ai |
| `ragas` | RAG evaluation: faithfulness, answer relevancy, context recall | `pip install ragas` · https://docs.ragas.io |
| `qdrant-client` | Recommended vector DB client | `pip install qdrant-client` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Qdrant | OSS/SaaS | Yes (REST + Python) | Recommended for production self-hosted; Docker; rich filtering |
| Chroma | OSS | Yes (Python embedded) | Best for local dev/prototyping; no server needed |
| pgvector | OSS | Yes (psycopg2/asyncpg) | Add vector search to existing Postgres; avoids new infrastructure |
| Pinecone | SaaS | Yes (REST/Python) | Fully managed; no self-hosting; higher cost at scale |
| Weaviate | OSS/SaaS | Yes (REST/Python) | Built-in hybrid search and BM25; good for multi-tenancy |
| OpenAI Assistants API | SaaS | Yes (OpenAI SDK) | Managed RAG with file search; limited customization |

## Templates & scripts
See `templates.md` for system prompts (default, technical docs, citation style) and retrieval strategy configurations.

Inline — minimal end-to-end RAG pipeline:
```python
from qdrant_client import QdrantClient
from openai import OpenAI

openai = OpenAI()
qdrant = QdrantClient(":memory:")

def embed(text: str) -> list[float]:
    return openai.embeddings.create(
        input=text, model="text-embedding-3-small"
    ).data[0].embedding

def retrieve(query: str, collection: str, top_k: int = 5) -> list[str]:
    hits = qdrant.query_points(
        collection_name=collection,
        query=embed(query),
        limit=top_k,
        with_payload=True,
    ).points
    return [h.payload["text"] for h in hits]

def generate(query: str, context: list[str]) -> str:
    ctx = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(context))
    messages = [
        {"role": "system", "content": "Answer using only the context. If unsure, say so."},
        {"role": "user", "content": f"Context:\n{ctx}\n\nQuestion: {query}"},
    ]
    return openai.chat.completions.create(
        model="gpt-4o-mini", messages=messages
    ).choices[0].message.content
```

## Best practices
- Use hybrid search (vector + BM25) from the start — pure vector retrieval misses exact-match queries; hybrid costs little extra
- Set `top_k` dynamically based on query type: simple factoid → 3, multi-part → 10, summary → 20
- Always include `source` and `chunk_index` in metadata; users and evaluation systems need citation support
- Separate indexing pipeline from query pipeline in code — indexing runs on a schedule; query pipeline runs on user request
- Run faithfulness and answer relevancy evals on ≥50 queries before any pipeline change reaches production
- Add a "no answer" escape valve in the prompt — without it the LLM will hallucinate rather than admit ignorance

## AI-agent gotchas
- Agents that embed the query and retrieve in a single function call cannot implement reranking without refactoring — decouple retrieve and generate from the start
- LangChain's `RetrievalQA` chain suppresses retrieval metadata by default; use `return_source_documents=True` or switch to LCEL for full observability
- Prompt injection via retrieved documents is a real attack vector — sanitize retrieved content if the corpus accepts user-supplied documents
- Context window overflow is silent in most frameworks; validate that `sum(len(chunk) for chunk in context) + prompt_size < model_max_tokens` before every generation call
- Vector DB schema changes (adding a metadata field) require collection recreation in Qdrant/Chroma — plan migrations before adding new document attributes

## References
- https://arxiv.org/abs/2005.11401 (original RAG paper — Lewis et al.)
- https://python.langchain.com/docs/tutorials/rag/
- https://docs.llamaindex.ai/
- https://www.pinecone.io/learn/advanced-rag-techniques/
- https://docs.ragas.io/ (evaluation)
