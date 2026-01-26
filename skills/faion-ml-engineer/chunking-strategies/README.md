# Chunking Strategies for RAG

Chunking is the process of splitting documents into smaller, semantically meaningful pieces for retrieval-augmented generation (RAG) systems. The right chunking strategy can improve retrieval precision by 30-40% and significantly impact answer quality.

## Why Chunking Matters

| Problem | Solution |
|---------|----------|
| Embedding models have token limits | Split into processable chunks |
| Dense retrieval works better with focused content | Smaller, topic-specific chunks |
| Context windows waste tokens on irrelevant text | Retrieve only relevant chunks |
| Over-compressed embeddings lose meaning | Right-sized chunks preserve semantics |

## Quick Reference

| Document Type | Recommended Strategy | Why |
|--------------|---------------------|-----|
| FAQs, product descriptions | No chunking / document-level | Short, single-purpose |
| Technical manuals | Recursive + overlap | Preserves hierarchy |
| Legal documents | Semantic + agentic | Context-critical |
| Code files | Code-aware (AST-based) | Respects functions/classes |
| Research papers | Hierarchical | Sections matter |
| Mixed content PDFs | Agentic | Varies by section |

---

## Chunking Strategy Types

### 1. Fixed-Size Chunking

Split text into chunks of fixed token/character count.

**When to use:**
- Simple documents with uniform density
- Speed is critical
- Prototyping and baseline testing

**Parameters:**
- `chunk_size`: 256-1024 tokens (512 recommended)
- `overlap`: 10-20% (15% optimal for most cases)

**Pros:** Fast, predictable, easy to implement
**Cons:** Ignores semantic boundaries, may split sentences

### 2. Recursive Chunking

Split by multiple separators in priority order: paragraphs, sentences, words.

**When to use:**
- General-purpose documents
- Blog posts, articles, documentation
- When you need balance between speed and quality

**Separator hierarchy:**
1. `\n\n` (paragraphs)
2. `\n` (lines)
3. `. ` (sentences)
4. ` ` (words)

**Pros:** Respects natural text boundaries, good default choice
**Cons:** May miss topic shifts within paragraphs

### 3. Semantic Chunking

Split based on embedding similarity between adjacent sentences.

**When to use:**
- Multi-topic documents
- When topical coherence is critical
- Legal, medical, technical documents

**How it works:**
1. Embed each sentence
2. Calculate cosine similarity between adjacent sentences
3. Split where similarity drops below threshold
4. Apply Savitzky-Golay filtering for smooth boundaries

**Parameters:**
- `similarity_threshold`: 0.75-0.85
- `min_chunk_size`: 100 tokens
- `max_chunk_size`: 1000 tokens

**Pros:** Preserves topic coherence, semantically meaningful
**Cons:** Requires embedding model, slower, costs API calls

### 4. Document Structure Chunking

Split by document structure: headers, sections, paragraphs.

**When to use:**
- Markdown documentation
- HTML pages with clear structure
- Well-formatted PDFs

**Supported formats:**
- **Markdown:** Split by `#` headers, preserve hierarchy
- **HTML:** Split by `<section>`, `<article>`, `<div>`
- **PDF:** Split by headings, page boundaries

**Pros:** Preserves logical document structure
**Cons:** Requires well-structured input

### 5. Code-Aware Chunking

Split code by AST (Abstract Syntax Tree) nodes: functions, classes, methods.

**When to use:**
- Code repositories
- API documentation with code examples
- Technical documentation

**Language support:**
- Python (AST parsing)
- JavaScript/TypeScript (regex-based)
- Go, Rust, Java (treesitter)

**Pros:** Preserves code integrity, function-level retrieval
**Cons:** Language-specific implementation needed

### 6. Late Chunking (Jina AI)

Embed entire document first, then chunk the embeddings.

**When to use:**
- Long documents where context is critical
- When using long-context embedding models (8K+ tokens)
- When traditional chunking loses pronoun references

**How it works:**
1. Process entire document through transformer
2. Get token-level embeddings with full context
3. Apply mean pooling per chunk
4. Result: chunk embeddings with document-level context

**Requirements:**
- Long-context embedding model (jina-embeddings-v3, etc.)
- Document fits in model's context window

**Pros:** Preserves contextual references ("the city" knows it means Berlin)
**Cons:** Limited by model context window, requires specific models

### 7. Agentic Chunking

LLM decides chunking strategy per document or section.

**When to use:**
- Highly variable document types
- Complex multi-section documents
- When quality > cost
- Legal contracts, medical reports, financial filings

**How it works:**
1. LLM analyzes document structure and content
2. Decides optimal chunking strategy per section
3. Applies different methods to different parts
4. Enriches chunks with metadata (titles, summaries)

**Decision factors:**
- Document type (research paper, legal, technical)
- Content density
- Section purpose
- Query patterns

**Pros:** Highest quality, adaptive, adds metadata
**Cons:** Expensive, slow, complex to implement

### 8. Hierarchical Chunking

Create multi-level chunk hierarchy: document, section, paragraph.

**When to use:**
- Long documents with clear hierarchy
- Books, reports, specifications
- When you need both overview and detail retrieval

**Levels:**
1. Document summary (high-level)
2. Section chunks (mid-level)
3. Paragraph chunks (detail-level)

**Retrieval pattern:**
- First pass: retrieve section chunks
- Second pass: retrieve paragraphs from relevant sections

**Pros:** Supports multi-granularity retrieval
**Cons:** More complex indexing, multiple embeddings per document

---

## LLM Usage Tips

### Chunk Size Guidelines

| Model Context | Recommended Chunk Size |
|--------------|----------------------|
| 4K tokens | 256-512 tokens |
| 8K tokens | 512-1024 tokens |
| 32K+ tokens | 1024-2048 tokens |

**Rule of thumb:** Chunk size = Model context / (Top-K retrieved * 2)

### Overlap Recommendations

- **10-20% overlap** for most use cases
- **15% overlap** optimal based on benchmarks (e.g., 1024 chunks with 150 token overlap)
- **Higher overlap (25%)** for dense technical content
- **No overlap** when chunks are naturally complete (functions, sections)

### Metadata to Include

Always attach metadata for filtering and context:

```python
{
    "chunk_id": "doc_001_chunk_003",
    "source": "document_name.pdf",
    "page": 5,
    "section": "Introduction",
    "header_path": "Chapter 1 > Overview > Background",
    "chunk_index": 3,
    "total_chunks": 25,
    "token_count": 512
}
```

### Evaluation Metrics

| Metric | What It Measures |
|--------|------------------|
| Retrieval precision | % relevant chunks in top-K |
| Answer faithfulness | Answer grounded in retrieved chunks |
| Chunk coherence | Semantic completeness of chunks |
| Context utilization | % of context window used effectively |

---

## Tools and Libraries

### Python Libraries

| Library | Best For | Key Features |
|---------|----------|--------------|
| [Chonkie](https://github.com/chonkie-inc/chonkie) | Production RAG | 33x faster, semantic/late chunking |
| [LangChain](https://python.langchain.com/docs/modules/data_connection/document_transformers/) | General purpose | RecursiveCharacterTextSplitter |
| [LlamaIndex](https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/) | RAG pipelines | NodeParsers, SentenceWindowNodeParser |
| [unstructured](https://github.com/Unstructured-IO/unstructured) | Document parsing | PDF, DOCX, HTML extraction |

### Chonkie Chunkers

```python
from chonkie import (
    TokenChunker,      # Fixed token splits
    SentenceChunker,   # Sentence-based
    RecursiveChunker,  # Hierarchical splits
    SemanticChunker,   # Embedding-based
    SDPMChunker,       # Double-pass merge
    LateChunker,       # Late chunking (experimental)
    CodeChunker,       # Code-aware
    SlumberChunker,    # LLM-based (agentic)
)
```

### LangChain Splitters

```python
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
    HTMLHeaderTextSplitter,
    PythonCodeTextSplitter,
)
```

---

## Decision Framework

```
START
  |
  v
Is document short (<1000 tokens)?
  |
  YES --> No chunking (document-level)
  |
  NO
  |
  v
Is it code?
  |
  YES --> Code-aware chunking (AST/treesitter)
  |
  NO
  |
  v
Is it structured (Markdown/HTML)?
  |
  YES --> Document structure chunking
  |
  NO
  |
  v
Is context critical (legal, medical)?
  |
  YES --> Semantic or Agentic chunking
  |
  NO
  |
  v
Is document highly variable?
  |
  YES --> Agentic chunking
  |
  NO
  |
  v
Default --> Recursive chunking with 15% overlap
```

---

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Selection, implementation, evaluation checklists |
| [examples.md](examples.md) | Code examples for all strategies |
| [templates.md](templates.md) | Configuration and testing templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for strategy selection and optimization |

---

## External Resources

- [Late Chunking Paper (arXiv)](https://arxiv.org/abs/2409.04701)
- [Late Chunking by Jina AI](https://jina.ai/news/late-chunking-in-long-context-embedding-models/)
- [Weaviate Chunking Strategies](https://weaviate.io/blog/chunking-strategies-for-rag)
- [NVIDIA Chunking Guide](https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/)
- [Pinecone Chunking Strategies](https://www.pinecone.io/learn/chunking-strategies/)
- [DataCamp Late Chunking Tutorial](https://www.datacamp.com/tutorial/late-chunking)
- [IBM Agentic Chunking](https://www.ibm.com/think/topics/agentic-chunking)
- [Firecrawl Best Chunking 2025](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)
- [Chonkie Documentation](https://docs.chonkie.ai/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Reorganized into folder, added late/agentic chunking |
| 1.0.0 | 2024-09 | Initial version |
