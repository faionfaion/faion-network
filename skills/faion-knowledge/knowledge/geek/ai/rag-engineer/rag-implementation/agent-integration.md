# Agent Integration — RAG Implementation

## When to use
- Building a question-answering system over a proprietary document corpus (PDFs, Markdown, text)
- LLM needs to answer questions about data that postdates its training cutoff
- Reducing hallucinations by grounding generation in retrieved facts
- Products requiring citations or source attribution alongside answers
- Knowledge-base chatbots where answers must come only from a controlled corpus

## When NOT to use
- The corpus changes faster than the re-ingestion pipeline can keep up — consider a streaming update strategy first
- Queries are purely conversational with no need for factual grounding — RAG adds latency and cost with no benefit
- The entire knowledge base fits comfortably in the context window — just stuff it in; no retrieval needed
- Structured data questions (e.g., "What was Q3 revenue?") — SQL + function-calling beats RAG for tabular data

## Where it fails / limitations
- Chunking strategy mismatches query type: fixed-size chunks split mid-sentence cause poor retrieval for factual look-ups; semantic chunking is slower to build
- Context window stuffing: top-K chunks can fill the LLM context leaving no room for the answer — set `top_k` conservatively and measure token usage
- Retrieval recall failures: if the relevant chunk is not in top-K, the LLM cannot answer correctly regardless of generation quality
- Document loader accuracy: `pypdf` text extraction fails on scanned PDFs and complex layouts (tables, multi-column) — needs OCR fallback
- Re-ingestion on document updates requires delete+re-insert; without soft-delete tracking, stale chunks accumulate
- Answer generation may still hallucinate even with correct context if the system prompt does not explicitly enforce "answer only from context"
- HyDE (hypothetical document embedding) improves recall but doubles embedding API cost for every query

## Agentic workflow
A document ingestion agent loads, chunks, embeds, and upserts documents in batches. A query agent receives a question, optionally rewrites or expands it, retrieves top-K chunks from the vector store, filters below a score threshold, and passes the structured context to the generation LLM with a strict system prompt. A validation agent periodically samples random test questions and checks that retrieved sources contain the expected content. Chunking strategy and `top_k` value are set by configuration; changes require human review of benchmark results.

### Recommended subagents
- `faion-sdd-executor-agent` — executes implementation plan steps for pipeline setup and document loader selection
- Custom ingestion agent — handles batched embed+upsert with retry, deduplication, and progress logging
- Custom query agent — wraps retrieve+generate with fallback messaging when context is empty

### Prompt pattern
```
You are a RAG ingestion agent. Given: directory path, chunk_size, overlap, embedding_model.
Steps:
1. Load all .md, .txt, .pdf files from directory.
2. Chunk each document using the specified strategy.
3. Embed chunks in batches of 50.
4. Upsert to vector store with metadata: {source, chunk_index, source_id}.
Return: {"ingested_docs": N, "total_chunks": M, "failed": [list]}
```

```
You are a RAG query agent. Context provided. Rules:
- Answer ONLY from the provided context.
- If context is empty or score < 0.65, respond: "I don't have enough information."
- Cite source from metadata["source"] for each factual claim.
- Do not infer beyond what the context states.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain` | RAG chain orchestration, document loaders | `pip install langchain langchain-community` / [docs](https://python.langchain.com/) |
| `llama-index` | Index-centric RAG with query engines | `pip install llama-index` / [docs](https://docs.llamaindex.ai/) |
| `pypdf` | PDF text extraction | `pip install pypdf` / [PyPI](https://pypi.org/project/pypdf/) |
| `tiktoken` | Token counting for chunking | `pip install tiktoken` / [GitHub](https://github.com/openai/tiktoken) |
| `nltk` | Sentence tokenization for sentence-based chunking | `pip install nltk` / [docs](https://www.nltk.org/) |
| `unstructured` | Complex document parsing (tables, HTML, DOCX) | `pip install unstructured` / [docs](https://unstructured-io.github.io/unstructured/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Embeddings API | SaaS | Yes — batch up to 2048 texts | `text-embedding-3-small` for cost, `3-large` for quality |
| Anthropic Claude (generation) | SaaS | Yes — structured output | Use for citation-heavy generation with long context |
| LangChain Hub | SaaS | Yes — pull RAG prompt templates | Versioned prompt templates for RAG chains |
| Unstructured Cloud | SaaS | Yes — REST API | Handles PDFs with OCR, tables, and complex layout |
| LlamaCloud | SaaS | Yes | Managed ingestion pipeline with parsing |

## Templates & scripts
See `templates.md` for the full `RAGPipeline` class, `DocumentLoader`, and `ChunkingStrategy` implementations.

Critical inline pattern — score-filtered retrieval before generation:
```python
def retrieve_with_threshold(collection, query_embedding, top_k=10, min_score=0.65):
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k,
                               include=["documents", "metadatas", "distances"])
    filtered = [
        (results["documents"][0][i], 1 - results["distances"][0][i],
         results["metadatas"][0][i])
        for i in range(len(results["ids"][0]))
        if 1 - results["distances"][0][i] >= min_score
    ]
    return filtered  # Empty list → agent should say "insufficient context"
```

## Best practices
- Default to sentence-boundary chunking over fixed-size; it preserves semantic units and improves retrieval precision
- Always include `chunk_index` and `source_id` in chunk metadata — they enable parent-document reconstruction and citation
- Use 10-20% overlap (not 0) between chunks to avoid losing context at boundaries
- Set `score_threshold` explicitly and tune it per corpus; default 0.7 is often too aggressive for domain-specific text
- HyDE (generate hypothetical answer, embed it, use as query vector) consistently improves recall 10-20% for factual Q&A — worth the extra API call
- Cache query embeddings for repeated queries using a Redis cache keyed by `hash(model + query)`
- Separate ingestion and query pipelines — different scaling profiles and failure modes

## AI-agent gotchas
- PDF loaders return empty strings for scanned pages silently — agents must validate chunk content length (>50 chars) before embedding
- `response.data[0].embedding` is a list, not a numpy array — agents storing to numpy must convert explicitly
- LLM temperature must be low (≤0.3) for RAG generation; higher values cause the model to "drift" off the provided context
- Agents using HyDE must not cache the hypothetical answer embedding for subsequent different queries — it's query-specific
- When `filter` is passed to Chroma's `collection.query()`, the `where` dict syntax differs from Qdrant's `Filter` objects; agents must use the correct client's filter DSL
- Re-ranking results after retrieval is a separate step that requires a cross-encoder or rerank API call — agents must not confuse cosine score with cross-encoder relevance score

## References
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [LlamaIndex RAG Guide](https://docs.llamaindex.ai/en/stable/understanding/putting_it_all_together/)
- [RAG from Scratch (LangChain)](https://github.com/langchain-ai/rag-from-scratch)
- [HyDE Paper](https://arxiv.org/abs/2212.10496)
- [Unstructured IO](https://unstructured-io.github.io/unstructured/)
