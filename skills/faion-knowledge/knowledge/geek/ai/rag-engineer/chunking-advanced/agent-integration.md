# Agent Integration — Advanced Chunking

## When to use
- Indexing Markdown documentation, HTML sites, or structured wikis where header hierarchy must be preserved
- Ingesting source code repositories into a code-search RAG (Python AST, JS/TS function-level splitting)
- High-stakes retrieval domains (legal, medical, scientific) where splitting mid-concept degrades answer quality
- Production pipelines that handle mixed content types within a single ingestion run
- After baseline (chunking-basics) benchmarks show retrieval precision below acceptable threshold

## When NOT to use
- Quick prototyping — RecursiveChunker from chunking-basics is faster to wire up and sufficient for ≤10k docs
- Semantic chunking when embedding budget is constrained; it calls the embedding API once per sentence during indexing
- Code chunking via JS regex patterns on TypeScript with decorators or generics — AST parsers handle those correctly; regex does not
- Corpora entirely in languages without NLTK punkt support — sentence tokenization silently degrades

## Where it fails / limitations
- SemanticChunker requires the embedding function at index time, creating a tight coupling between ingestion and embedding provider
- MarkdownChunker can produce very small chunks (single-line code blocks, list items) that embed poorly; min_chunk_size guard is essential
- CodeChunker Python path uses `ast.parse` — it silently falls back to generic line-based splitting for syntax errors without warning
- HTMLChunker targets `section/article/div`; flat HTML pages with no sectioning elements produce one giant chunk
- ChunkingService's fallback uses word-based splitting that ignores token limits — verify with tiktoken before ingesting

## Agentic workflow
A subagent detects the content type of each document, instantiates the matching chunker from ChunkingService, runs chunking, validates the size distribution (log a warning if >5% of chunks exceed max_chunk_size), and emits enriched chunk dicts with `header_path`, `type`, and `metadata` fields. A second agent reviews the distribution and can trigger a re-chunk with adjusted parameters. No human approval is needed unless the chunk count changes >2x from the previous run.

### Recommended subagents
- `faion-sdd-executor-agent` — orchestrate multi-strategy chunking within an ingestion pipeline task

### Prompt pattern
```
Given the document below, identify its content type (markdown/html/python/javascript/prose),
select the appropriate advanced chunker, apply it, and return chunks as JSON:
{id, text, type, header_path?, name?, start_line?, metadata}.

Validate: no chunk exceeds 1000 words. Flag any that do.

Document path: {{path}}
Content:
<document>{{content}}</document>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langchain-text-splitters` | MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter | `pip install langchain-text-splitters` |
| `beautifulsoup4` | HTML parsing for HTMLChunker | `pip install beautifulsoup4` |
| `nltk` | Sentence tokenization for SemanticChunker | `pip install nltk` + punkt download |
| `ast` (stdlib) | Python AST parsing for CodeChunker | built-in |
| `tree-sitter` | Language-agnostic AST for multi-language code chunking | `pip install tree-sitter` |
| `llama-index-core` | SemanticSplitterNodeParser (semantic chunking) | `pip install llama-index-core llama-index-embeddings-openai` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Unstructured.io | SaaS/OSS | Yes (REST/Python) | Pre-processes PDFs/DOCX into clean structural elements before semantic/markdown chunking |
| LlamaParse | SaaS | Yes (Python SDK) | Table-aware PDF parsing; critical before MarkdownChunker on academic/legal PDFs |
| Docling (IBM) | OSS | Yes (Python lib) | Local, preserves document layout hierarchy; good for enterprise air-gap deployments |
| Chonkie | OSS | Yes (Python lib) | Pure-Python chunking library with semantic, token, sentence modes; no LangChain dep |

## Templates & scripts
See `templates.md` for SemanticChunker, MarkdownChunker, HTMLChunker, CodeChunker, and ChunkingService templates.

Inline — content-type router feeding ChunkingService:
```python
from pathlib import Path

def chunk_file(path: str, embedding_func=None) -> list[dict]:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    ext = Path(path).suffix.lower()
    if ext in (".md", ".mdx"):
        strategy = ChunkingStrategy.MARKDOWN
    elif ext in (".py",):
        strategy = ChunkingStrategy.CODE
    elif ext in (".js", ".ts", ".tsx"):
        strategy = ChunkingStrategy.CODE
    elif ext in (".html", ".htm"):
        strategy = ChunkingStrategy.RECURSIVE  # HTMLChunker handles internally
    else:
        strategy = ChunkingStrategy.SEMANTIC if embedding_func else ChunkingStrategy.RECURSIVE
    svc = ChunkingService(embedding_func=embedding_func)
    return svc.chunk(text, strategy=strategy, metadata={"source": path})
```

## Best practices
- Cache sentence embeddings used in SemanticChunker — re-chunking the same doc without cache costs 2x the embedding API calls
- For MarkdownChunker, set `include_header_in_chunk=True`; embedding the header path inside the chunk text improves retrieval recall
- CodeChunker via AST produces overlapping chunks when a class contains methods; deduplicate by `(name, start_line)` before indexing
- Always set `min_chunk_size`; empty code blocks and single-word paragraphs produce near-zero vectors that pollute nearest-neighbor results
- Validate strategy selection with at least 20 representative queries spanning all content types before committing to production index
- For multi-language codebases, prefer `tree-sitter` bindings over regex-based JS chunking — the regex patterns in the reference impl fail on arrow functions with implicit returns

## AI-agent gotchas
- SemanticChunker calls embedding_func once per sentence at index time; for a 10k-doc corpus this adds significant API cost — quantify before using in production
- ChunkingService catches all exceptions and falls back to word-split; agents must check that `strategy_used` in output matches the requested strategy
- MarkdownChunker inherits parent headers into sub-chunks — this is intentional but can cause `header_path` to be >200 chars for deeply nested docs, which breaks some vector DB metadata limits
- Agents running CodeChunker on `.py` files with encoding errors must handle the `ast.parse` `SyntaxError` branch explicitly; the fallback `_chunk_generic` silently drops class/function metadata
- When switching chunking strategy on an existing index, the chunk count per document changes → chunk IDs collide → stale vectors remain; always clear the collection or use a versioned collection name

## References
- https://python.langchain.com/docs/modules/data_connection/document_transformers/
- https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking/
- https://arxiv.org/abs/2409.04701 (Late Chunking — embedding full document then slicing)
- https://github.com/tree-sitter/tree-sitter (language-agnostic AST)
