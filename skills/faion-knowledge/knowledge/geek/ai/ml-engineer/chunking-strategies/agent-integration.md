# Agent Integration — Chunking Strategies for RAG

## When to use
- Building or improving a RAG ingestion pipeline where retrieval recall or precision is suboptimal
- Corpus contains mixed document types (code, markdown docs, PDFs, legal text) that require different splitting logic
- Current chunking causes hallucinations because LLM receives incomplete context at chunk boundaries
- Scaling to a large corpus where embedding cost is a concern (right-sized chunks reduce API calls)
- Migrating from a monolithic document-level embedding to a more precise retrieval system

## When NOT to use
- Documents are very short (< 500 tokens each) — embed at document level, no chunking needed
- Prototype or proof-of-concept with < 100 documents — use RecursiveCharacterTextSplitter defaults; optimize later
- Cost is the primary constraint and documents are uniform — fixed-size chunking (fastest, cheapest) is sufficient
- Late chunking (Jina embeddings) is available and documents fit in the model's context window — late chunking beats all others for contextual coherence

## Where it fails / limitations
- Fixed-size chunking ignores semantic boundaries — a sentence split across two chunks means neither chunk retrieves well for that concept
- Semantic chunking requires an embedding API call per sentence — adds significant ingestion cost and latency for large corpora
- Agentic chunking (LLM-decides) is expensive: one LLM call per document section; costs 10-50x more than rule-based approaches
- Hierarchical chunking doubles or triples the number of embeddings — index size grows proportionally; plan storage accordingly
- Overlap creates duplicate content in multiple chunks: if overlap is too large (> 25%), the same text appears in many candidates and clutters top-k results
- Code-aware chunking is language-specific — a Python AST parser cannot handle TypeScript without additional setup (treesitter)

## Agentic workflow
An ingestion agent receives a batch of raw documents, classifies each by type (code, markdown, legal, mixed PDF), selects the appropriate chunker, processes the batch, attaches metadata, and upserts to the vector store. For high-value documents (legal contracts, medical reports), the agent can invoke an LLM to add per-chunk summaries and section labels before embedding, improving retrieval quality at the cost of ingestion latency. Chunking decisions are logged per document type to inform future strategy tuning.

### Recommended subagents
- Document classifier subagent — receives file extension + first 200 chars, outputs `{type: "code"|"markdown"|"legal"|"pdf"|"general", recommended_strategy: "..."}`
- Chunk quality evaluator subagent — samples N chunks, computes average token count and coherence, flags chunks that are too short (< 50 tokens) or too long (> 1500 tokens) for review

### Prompt pattern
```
# Document type classifier prompt
You are a document classifier for a RAG chunking pipeline.
Given the file extension and content sample below, output JSON:
{
  "doc_type": "code" | "markdown" | "legal" | "scientific" | "general",
  "recommended_strategy": "code_aware" | "structure" | "semantic" | "recursive",
  "chunk_size_tokens": <integer 256-1024>,
  "overlap_pct": <integer 10-25>
}

Extension: {ext}
Sample (first 200 chars): {sample}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `chonkie` | Production chunking library (33x faster than alternatives) | `pip install chonkie` — [docs.chonkie.ai](https://docs.chonkie.ai/) |
| `langchain` text splitters | RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter, etc. | `pip install langchain` — [python.langchain.com](https://python.langchain.com/) |
| `llama-index` node parsers | SentenceSplitter, SemanticSplitterNodeParser, CodeSplitter | `pip install llama-index` — [docs.llamaindex.ai](https://docs.llamaindex.ai/) |
| `unstructured` | PDF/DOCX/HTML extraction before chunking | `pip install unstructured` — [unstructured.io](https://unstructured.io/) |
| `tree-sitter` | AST-based code parsing for code chunking | `pip install tree-sitter` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Chonkie | OSS | Yes — Python API | All major strategies; 33x faster than LangChain splitters |
| Unstructured.io | SaaS + OSS | Yes — REST + Python | Best-in-class PDF/DOCX parsing before chunking |
| LlamaIndex | OSS | Yes | SemanticSplitterNodeParser; SentenceWindowNodeParser |
| LangChain | OSS | Yes | MarkdownHeaderTextSplitter; HTMLHeaderTextSplitter |
| Jina AI Embeddings | SaaS | Yes — REST | Long-context models required for late chunking |

## Templates & scripts
See `templates.md` for configuration templates per document type.

Inline: Document-type-aware chunker dispatcher (< 50 lines):

```python
from chonkie import (
    TokenChunker, RecursiveChunker, SemanticChunker, CodeChunker
)

def get_chunker(doc_type: str, embed_fn=None):
    if doc_type == "code":
        return CodeChunker(chunk_size=512)
    elif doc_type == "markdown":
        return RecursiveChunker(
            chunk_size=512,
            chunk_overlap=80,
            separators=["\n## ", "\n### ", "\n\n", "\n", " "],
        )
    elif doc_type in ("legal", "scientific"):
        if embed_fn is None:
            raise ValueError("SemanticChunker requires an embed_fn")
        return SemanticChunker(
            embedding_model=embed_fn,
            similarity_threshold=0.80,
            min_chunk_size=100,
            max_chunk_size=800,
        )
    else:  # general
        return RecursiveChunker(chunk_size=512, chunk_overlap=77)  # 15% overlap

def chunk_document(text: str, doc_type: str, embed_fn=None):
    chunker = get_chunker(doc_type, embed_fn)
    chunks = chunker(text)
    return [{"text": c.text, "token_count": c.token_count} for c in chunks]
```

## Best practices
- Use 15% overlap (e.g., 77 tokens for 512-token chunks) as the default — empirically optimal for most corpora; increase to 25% only for dense technical content
- Always attach metadata to every chunk: source filename, page number, section header, chunk index — this enables metadata filtering and is essential for citations
- For markdown/HTML: use header-aware splitters (MarkdownHeaderTextSplitter) to include the header hierarchy as metadata; retrieval quality improves significantly when chunks include their section context
- Evaluate chunking on a held-out query set before committing: measure retrieval precision@10 with a sample of 50 representative queries; don't assume defaults are optimal for your corpus
- For code files: chunk at function/class boundaries (AST-based), not at fixed token counts — a function split across two chunks is almost impossible to retrieve correctly
- Rebuild the index after changing chunking strategy — old and new chunks in the same index cause inconsistent retrieval behavior

## AI-agent gotchas
- Metadata loss during chunking: if the chunker drops the source file path or page number, citations in the final RAG response will be wrong — always verify metadata propagation through the full ingestion pipeline
- Overlap causes duplicate retrieval: when top-k=20 returns 5 chunks that are overlapping windows of the same paragraph, the LLM receives 5x the same content; deduplicate by source range before passing to the reranker
- Semantic chunking embedding model mismatch: if you use `text-embedding-3-small` for semantic chunking but `text-embedding-3-large` for retrieval, similarity thresholds are calibrated to different vector spaces — use the same model for both
- Human-in-loop checkpoint: after changing chunking strategy on a live index, run a side-by-side retrieval comparison on 20 gold-standard queries before switching traffic to the new index

## References
- [Late Chunking Paper (arXiv)](https://arxiv.org/abs/2409.04701)
- [Jina AI Late Chunking](https://jina.ai/news/late-chunking-in-long-context-embedding-models/)
- [Weaviate Chunking Strategies](https://weaviate.io/blog/chunking-strategies-for-rag)
- [NVIDIA Chunking Guide](https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/)
- [Chonkie documentation](https://docs.chonkie.ai/)
- [Firecrawl Best Chunking 2025](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)
- [IBM Agentic Chunking](https://www.ibm.com/think/topics/agentic-chunking)
