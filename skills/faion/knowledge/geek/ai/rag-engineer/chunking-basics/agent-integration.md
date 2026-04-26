# Agent Integration — Chunking Basics

## When to use
- Building any RAG pipeline that ingests unstructured text documents
- Processing Markdown, plain text, chat logs, or news articles into retrievable units
- Prototyping a new knowledge base and needing a fast baseline chunking strategy
- Establishing chunk size and overlap defaults before running retrieval benchmarks

## When NOT to use
- Source documents are already structured records (JSON rows, SQL tables) — no chunking needed
- Content is code — use AST-based splitting (see chunking-advanced) rather than sentence/paragraph splitters
- Documents are ultra-short (<200 tokens each) — chunking adds overhead with no benefit
- Legal or medical content requiring sentence-level precision — semantic chunking (chunking-advanced) is the right tier

## Where it fails / limitations
- Fixed-size and paragraph chunkers ignore token budgets; word counts diverge from token counts for non-English text
- Sentence tokenizers (NLTK punkt) are English-centric; multilingual docs produce garbage splits
- Overlap logic in RecursiveChunker is character-based, not token-based — downstream models may still exceed context limits
- No metadata is attached by default; source tracking must be wired in explicitly
- Chunk-size decisions made without retrieval benchmarks frequently require re-indexing

## Agentic workflow
A Claude subagent ingests a document corpus, selects the chunking strategy based on detected content type (Markdown headers present → MarkdownChunker, general prose → RecursiveChunker, sentences dominant → SentenceChunker), applies the chunker, and emits a list of `{id, text, metadata}` dicts to the next pipeline stage. The agent should emit a chunk-size distribution summary so a reviewing agent can flag outliers before the embedding step. Human review is only needed when p95 chunk size diverges >50% from the target.

### Recommended subagents
- `faion-sdd-executor-agent` — orchestrate the chunking step within a broader RAG ingestion pipeline task

### Prompt pattern
```
Given the document below, detect its content type, select the appropriate
chunking strategy (fixed/sentence/paragraph/recursive), apply it with
chunk_size=500 and overlap=50, and return a JSON list of
{id, text, word_count, strategy_used} objects.

Document:
<document>{{document}}</document>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tiktoken` | Token-accurate fixed-size chunking (OpenAI tokenizer) | `pip install tiktoken` · https://github.com/openai/tiktoken |
| `nltk` | Sentence tokenization for SentenceChunker | `pip install nltk` + `nltk.download('punkt')` |
| `langchain-text-splitters` | RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter | `pip install langchain-text-splitters` |
| `llama-index` | Node parsers (SentenceSplitter, TokenTextSplitter) | `pip install llama-index-core` |
| `spacy` | High-quality multilingual sentence splitting | `pip install spacy` + model download |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Unstructured.io | SaaS/OSS | Yes (REST API) | Handles PDFs, DOCX, HTML before chunking; outputs clean text elements |
| LlamaParse | SaaS | Yes (Python SDK) | Structured extraction from PDFs, preserves tables — use before chunking |
| Docling (IBM) | OSS | Yes (Python lib) | Local PDF/DOCX parsing with layout awareness |

## Templates & scripts
See `templates.md` for FixedSizeChunker, SentenceChunker, ParagraphChunker, and RecursiveChunker templates.

Inline helper — detect content type and select strategy:
```python
def select_chunker(text: str, path: str = "") -> str:
    if path.endswith(".md") or text.startswith("#"):
        return "markdown"
    code_ratio = sum(1 for c in text if c in "{}();") / max(len(text), 1)
    if code_ratio > 0.03:
        return "code"
    if "\n\n" in text:
        return "paragraph"
    return "recursive"
```

## Best practices
- Always measure chunk token counts with tiktoken before indexing; word counts are ≤30% accurate for token budgets
- Set overlap to 10-20% of chunk_size; for Q&A corpora where questions span boundaries use 20%
- Attach `{source, page, chunk_index, strategy}` metadata at creation time — retro-fitting later requires full re-index
- Test chunking with five representative queries before committing to a strategy; retrieval accuracy is the only ground truth
- For mixed corpora (docs + code + chat), route each file type through its own chunker before merging into one index
- Pre-clean text (strip headers/footers, normalize whitespace) before chunking; noise propagates into all downstream chunks

## AI-agent gotchas
- Agents writing chunk IDs as sequential integers break when the same document is re-ingested; use `md5(source_path + chunk_index)` instead
- NLTK punkt requires a download step; agents running in sandboxed environments must pre-download or the chunker silently falls back to whitespace splitting
- LLM-based chunking decisions (asking the model where to split) add latency and cost that scale linearly with corpus size — reserve for <1k doc batches
- When an agent changes chunk_size mid-pipeline, existing vector index entries become stale; always version the index name with the chunking config hash
- RecursiveChunker character-level overlap ≠ token-level overlap; a chunk nominally "500 chars with 50 overlap" may hit 800 tokens for dense technical text

## References
- https://www.pinecone.io/learn/chunking-strategies/
- https://python.langchain.com/docs/modules/data_connection/document_transformers/
- https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/
- https://arxiv.org/abs/2409.04701 (Late Chunking)
