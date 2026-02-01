---
id: chunking-basics
name: "Chunking Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Chunking Basics

## Overview

Chunking is the process of splitting documents into smaller pieces for embedding and retrieval. The chunking strategy significantly impacts RAG performance - too large chunks dilute relevance, too small chunks lose context.

## When to Use

- Preparing documents for RAG pipelines
- Building semantic search systems
- Processing long documents for LLMs
- Creating knowledge bases

## Key Concepts

### Chunking Trade-offs

| Aspect | Small Chunks | Large Chunks |
|--------|--------------|--------------|
| Precision | High (focused) | Low (diluted) |
| Context | Limited | Preserved |
| Retrieval | More granular | Fewer results |
| LLM Input | More chunks needed | Fewer chunks needed |
| Storage | More vectors | Fewer vectors |

### Typical Sizes

| Document Type | Chunk Size | Overlap |
|---------------|------------|---------|
| Technical docs | 500-1000 tokens | 50-100 |
| Legal documents | 1000-1500 tokens | 100-200 |
| Chat logs | 200-400 tokens | 20-50 |
| Code | 500-800 tokens | 0-50 |
| News articles | 300-600 tokens | 50-100 |

## Basic Strategies

### Fixed-Size Chunking

```python
from typing import List, Dict
import tiktoken

class FixedSizeChunker:
    """Split text into fixed-size chunks with overlap."""

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
        encoding: str = "cl100k_base"
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.get_encoding(encoding)

    def chunk(self, text: str) -> List[Dict]:
        """Split text into token-based chunks."""
        tokens = self.tokenizer.encode(text)
        chunks = []

        start = 0
        chunk_id = 0

        while start < len(tokens):
            end = start + self.chunk_size

            # Get token slice
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)

            chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "start_token": start,
                "end_token": min(end, len(tokens)),
                "token_count": len(chunk_tokens)
            })

            start = end - self.overlap
            chunk_id += 1

        return chunks

# Usage
chunker = FixedSizeChunker(chunk_size=500, overlap=50)
chunks = chunker.chunk(long_document)
```

### Sentence-Based Chunking

```python
import nltk
from typing import List, Dict

nltk.download('punkt', quiet=True)

class SentenceChunker:
    """Chunk by sentences, respecting size limits."""

    def __init__(
        self,
        max_chunk_size: int = 500,
        min_chunk_size: int = 100,
        overlap_sentences: int = 1
    ):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.overlap_sentences = overlap_sentences

    def chunk(self, text: str) -> List[Dict]:
        """Split text into sentence-based chunks."""
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_size = 0

        for i, sentence in enumerate(sentences):
            sentence_size = len(sentence.split())

            if current_size + sentence_size <= self.max_chunk_size:
                current_chunk.append(sentence)
                current_size += sentence_size
            else:
                # Save current chunk
                if current_size >= self.min_chunk_size:
                    chunks.append({
                        "text": " ".join(current_chunk),
                        "sentence_count": len(current_chunk),
                        "word_count": current_size
                    })

                # Start new chunk with overlap
                overlap_start = max(0, len(current_chunk) - self.overlap_sentences)
                current_chunk = current_chunk[overlap_start:] + [sentence]
                current_size = sum(len(s.split()) for s in current_chunk)

        # Don't forget last chunk
        if current_chunk:
            chunks.append({
                "text": " ".join(current_chunk),
                "sentence_count": len(current_chunk),
                "word_count": current_size
            })

        return chunks
```

### Paragraph-Based Chunking

```python
from typing import List, Dict
import re

class ParagraphChunker:
    """Chunk by paragraphs with size constraints."""

    def __init__(
        self,
        max_chunk_size: int = 1000,
        min_chunk_size: int = 200
    ):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size

    def chunk(self, text: str) -> List[Dict]:
        """Split text by paragraphs."""
        # Split by double newline
        paragraphs = re.split(r'\n\s*\n', text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        chunks = []
        current_chunk = []
        current_size = 0

        for para in paragraphs:
            para_size = len(para.split())

            # Single paragraph exceeds max - split it
            if para_size > self.max_chunk_size:
                # Save current chunk first
                if current_chunk:
                    chunks.append({
                        "text": "\n\n".join(current_chunk),
                        "paragraph_count": len(current_chunk)
                    })
                    current_chunk = []
                    current_size = 0

                # Split large paragraph
                sub_chunks = self._split_large_paragraph(para)
                chunks.extend(sub_chunks)
                continue

            if current_size + para_size <= self.max_chunk_size:
                current_chunk.append(para)
                current_size += para_size
            else:
                # Save and start new
                if current_size >= self.min_chunk_size:
                    chunks.append({
                        "text": "\n\n".join(current_chunk),
                        "paragraph_count": len(current_chunk)
                    })
                current_chunk = [para]
                current_size = para_size

        # Last chunk
        if current_chunk:
            chunks.append({
                "text": "\n\n".join(current_chunk),
                "paragraph_count": len(current_chunk)
            })

        return chunks

    def _split_large_paragraph(self, para: str) -> List[Dict]:
        """Split oversized paragraph by sentences."""
        import nltk
        sentences = nltk.sent_tokenize(para)
        chunks = []
        current = []
        current_size = 0

        for sent in sentences:
            sent_size = len(sent.split())
            if current_size + sent_size <= self.max_chunk_size:
                current.append(sent)
                current_size += sent_size
            else:
                if current:
                    chunks.append({"text": " ".join(current), "paragraph_count": 1})
                current = [sent]
                current_size = sent_size

        if current:
            chunks.append({"text": " ".join(current), "paragraph_count": 1})

        return chunks
```

### Recursive Chunking (LangChain-style)

```python
from typing import List, Dict, Optional

class RecursiveChunker:
    """Recursively split text using multiple separators."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: Optional[List[str]] = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def chunk(self, text: str) -> List[Dict]:
        """Recursively split text."""
        return self._split_text(text, self.separators)

    def _split_text(
        self,
        text: str,
        separators: List[str]
    ) -> List[Dict]:
        """Split text recursively with separators."""
        final_chunks = []

        # Use first separator
        separator = separators[0]
        splits = text.split(separator) if separator else list(text)

        good_splits = []
        current_doc = []
        current_length = 0

        for split in splits:
            split_length = len(split)

            if current_length + split_length <= self.chunk_size:
                current_doc.append(split)
                current_length += split_length + len(separator)
            else:
                if current_doc:
                    doc = separator.join(current_doc)
                    if len(doc) > self.chunk_size and len(separators) > 1:
                        # Recursively split with next separator
                        final_chunks.extend(
                            self._split_text(doc, separators[1:])
                        )
                    else:
                        final_chunks.append({"text": doc})

                # Handle overlap
                overlap_docs = []
                overlap_length = 0
                for d in reversed(current_doc):
                    if overlap_length + len(d) <= self.chunk_overlap:
                        overlap_docs.insert(0, d)
                        overlap_length += len(d)
                    else:
                        break

                current_doc = overlap_docs + [split]
                current_length = sum(len(d) for d in current_doc) + len(separator) * (len(current_doc) - 1)

        # Last chunk
        if current_doc:
            doc = separator.join(current_doc)
            if len(doc) > self.chunk_size and len(separators) > 1:
                final_chunks.extend(self._split_text(doc, separators[1:]))
            else:
                final_chunks.append({"text": doc})

        return final_chunks
```

## Best Practices

1. **Match Strategy to Content**
   - Markdown docs: Use header-based
   - Code: Use AST-based
   - General text: Use recursive/sentence

2. **Size Selection**
   - Start with 500 tokens
   - Larger for technical/legal
   - Smaller for Q&A

3. **Overlap**
   - 10-20% overlap typically
   - More for highly contextual content
   - Less for independent sections

4. **Metadata Preservation**
   - Keep source document info
   - Preserve hierarchy (headers)
   - Track chunk position

5. **Testing**
   - Test with representative queries
   - Measure retrieval quality
   - Iterate on chunk size

## Common Pitfalls

1. **Splitting Mid-Sentence** - Losing meaning at boundaries
2. **No Overlap** - Context lost between chunks
3. **Ignoring Structure** - Missing document organization
4. **Same Size for All** - Different docs need different strategies
5. **Too Small** - Fragments without context
6. **Too Large** - Diluted relevance

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

- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [LlamaIndex Node Parsers](https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/)
- [Chunking Strategies - Pinecone](https://www.pinecone.io/learn/chunking-strategies/)
- [Text Splitters Deep Dive](https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/)
