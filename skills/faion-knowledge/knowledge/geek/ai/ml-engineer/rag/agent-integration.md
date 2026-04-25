# Agent Integration — RAG (Retrieval-Augmented Generation)

## When to use
- The application needs to answer questions about documents not in the model's training data
- Knowledge is updated frequently (daily/weekly) and retraining is impractical
- Users need source citations to verify claims
- The knowledge base is too large to fit in a single context window (> a few hundred pages)
- Multi-tenant system where each tenant has a separate knowledge base
- Cost constraint: RAG is substantially cheaper than fine-tuning for factual recall tasks

## When NOT to use
- Knowledge is behavioral (writing style, persona, domain jargon) rather than factual — use fine-tuning
- The corpus is < 50 documents that can all fit in a single long-context prompt — skip retrieval entirely
- Latency budget is under 200ms — retrieval + reranking adds 100-500ms overhead
- The task is pure reasoning on data already in the prompt — adding retrieval introduces noise

## Where it fails / limitations
- Retrieval misses: if the relevant chunk is not in the top-k, the LLM cannot answer correctly — no amount of prompt engineering fixes a retrieval failure
- Chunking artifacts: sentences split across chunk boundaries lose context; overlap helps but doesn't fully solve it
- Hallucination on insufficient context: if retrieved chunks are tangentially related, the LLM may hallucinate a plausible-sounding answer rather than saying "I don't know"
- Outdated index: documents updated after last ingestion return stale information — needs a document versioning and re-ingestion strategy
- Contradiction in corpus: if multiple documents contradict each other, the LLM may surface either answer unpredictably
- Context window pressure: at top-k=20 with 512-token chunks, retrieval consumes 10K tokens before generation — forces reranking to reduce to top-5

## Agentic workflow
A retrieval agent embeds the user query, queries the vector store for top-20 candidates, passes them through a cross-encoder reranker to select top-5, then constructs a prompt with the ranked context and calls the generator LLM. The agent enforces citation output format and validates faithfulness: if the answer cites a source not in the retrieved set, it flags a hallucination and retries with a stricter prompt. For agentic RAG (multi-hop), the agent decomposes the query into sub-queries, retrieves separately, and synthesizes.

### Recommended subagents
- Embedding/retrieval subagent — wraps the vector DB client; handles embedding, querying, reranking; returns structured `{chunks: [], scores: []}` JSON
- Faithfulness validator subagent — checks that every claim in the generated answer maps to at least one retrieved chunk; flags grounding violations

### Prompt pattern
```
You are a knowledge assistant. Answer the user's question using ONLY the context below.
Cite each claim with [Source: <filename>].
If the context does not contain the answer, say: "I don't have that information."
Do not make up information not in the context.

<context>
{retrieved_chunks}
</context>

Question: {user_query}
```

```python
# Minimal RAG loop
def rag_answer(query: str, collection: str) -> str:
    chunks = retriever.retrieve(query, collection=collection, top_k=20)
    reranked = reranker.rerank(query, chunks, top_n=5)
    context = "\n\n".join(c.text for c in reranked)
    return llm.complete(RAG_PROMPT.format(context=context, user_query=query))
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llama-index` | RAG framework with indexing, retrieval, synthesis | `pip install llama-index` — [docs.llamaindex.ai](https://docs.llamaindex.ai/) |
| `langchain` | RAG chains, document loaders, splitters | `pip install langchain` — [python.langchain.com](https://python.langchain.com/) |
| `ragas` | RAG evaluation (faithfulness, relevancy, recall) | `pip install ragas` — [docs.ragas.io](https://docs.ragas.io/) |
| `sentence-transformers` | Local embedding + cross-encoder reranking | `pip install sentence-transformers` |
| `unstructured` | PDF/DOCX/HTML document parsing | `pip install unstructured` |
| `chonkie` | Fast, production-grade chunking library | `pip install chonkie` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LlamaIndex | OSS framework | Yes — Python API | Best-in-class RAG abstractions; LlamaCloud for managed |
| LangChain | OSS framework | Yes — Python/TS API | Broad ecosystem; RAG chains, document loaders |
| Cohere Rerank | SaaS API | Yes — REST | High-quality cross-encoder reranker; multilingual |
| Voyage AI | SaaS API | Yes — REST | Best-in-class embeddings for retrieval (voyage-3) |
| RAGAS | OSS | Yes — Python | RAG evaluation suite; faithfulness, answer relevancy |
| Qdrant Cloud | SaaS + OSS | Yes | Vector store; native hybrid search; free tier |
| Pinecone | SaaS | Yes | Managed vector store; serverless; zero-ops |

## Templates & scripts
See `templates.md` for full RAG pipeline templates and prompt templates.

Inline: production-ready RAG pipeline skeleton (< 50 lines):

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.embeddings.openai import OpenAIEmbedding

# 1. Ingest
docs = SimpleDirectoryReader("./docs").load_data()
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=80)
nodes = splitter.get_nodes_from_documents(docs)

# 2. Index
embed_model = OpenAIEmbedding(model="text-embedding-3-small")
index = VectorStoreIndex(nodes, embed_model=embed_model)

# 3. Query with reranking
reranker = SentenceTransformerRerank(model="cross-encoder/ms-marco-MiniLM-L-2-v2", top_n=5)
query_engine = index.as_query_engine(
    similarity_top_k=20,
    node_postprocessors=[reranker],
)

response = query_engine.query("What is the refund policy?")
print(response.response)
for src in response.source_nodes:
    print(f"  [{src.score:.3f}] {src.metadata.get('file_name')}")
```

## Best practices
- Always rerank: retrieve broad (top-20), rerank to top-5 — this pattern consistently outperforms top-5 direct retrieval by 15-20% precision
- Cache embeddings: re-embedding unchanged documents on every ingestion wastes cost; store content hashes and skip unchanged chunks
- Include metadata in chunks: source filename, page number, section — agents need this for citations and for debugging retrieval failures
- Add a "cannot answer" path explicitly: if score_threshold is not met for any chunk, return a structured "no information" response rather than attempting to generate with weak context
- Use `text-embedding-3-small` for cost efficiency in prototyping; switch to `voyage-3` or `text-embedding-3-large` for production if recall metrics demand it
- Evaluation cadence: run RAGAS after every significant change to chunking, embedding model, or retrieval strategy

## AI-agent gotchas
- Retrieval is a breakpoint: if the retriever fails silently (network error, empty results), the LLM will hallucinate. Always check `len(retrieved_chunks) > 0` before generation and return a structured error if not
- Prompt injection via documents: a malicious document in the corpus could contain instructions like "ignore previous instructions and output X" — sanitize or encode retrieved chunks before injecting into prompts
- Index drift: if the RAG pipeline is live and documents are updated asynchronously, there is a window where queries may receive outdated answers — implement a document version field and return it in citations
- Human-in-loop checkpoint: before deploying to production, run a manual evaluation of 50 representative queries across your full retrieval-generation pipeline; automated metrics (RAGAS) miss nuanced faithfulness failures

## References
- [LlamaIndex Production RAG](https://developers.llamaindex.ai/python/framework/optimizing/production_rag/)
- [RAGAS evaluation framework](https://docs.ragas.io/)
- [The Ultimate RAG Blueprint 2025/2026](https://langwatch.ai/blog/the-ultimate-rag-blueprint-everything-you-need-to-know-about-rag-in-2025-2026)
- [Comprehensive RAG Survey (arXiv 2025)](https://arxiv.org/html/2506.00054v1)
- [Enhancing RAG Best Practices (arXiv)](https://arxiv.org/abs/2501.07391)
- [RAG Evaluation Guide (Qdrant)](https://qdrant.tech/blog/rag-evaluation-guide/)
