---
id: chunking-advanced
name: "Advanced Chunking"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Advanced Chunking Strategies

## Overview

Advanced chunking techniques for specialized content: semantic chunking, document structure preservation, code parsing, and production-grade implementations.

## When to Use

- Processing structured documents (Markdown, HTML, code)
- Semantic similarity-based chunking
- Building production RAG systems
- Handling complex document hierarchies

## Advanced Strategies

### Semantic Chunking

```python
import numpy as np
from typing import List, Dict
import nltk

class SemanticChunker:
    """Chunk based on semantic similarity between sentences."""

    def __init__(
        self,
        embedding_func: callable,
        similarity_threshold: float = 0.75,
        max_chunk_size: int = 1000,
        min_chunk_size: int = 100
    ):
        self.embedding_func = embedding_func
        self.similarity_threshold = similarity_threshold
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size

    def chunk(self, text: str) -> List[Dict]:
        """Split text based on semantic breaks."""
        sentences = nltk.sent_tokenize(text)

        if len(sentences) <= 1:
            return [{"text": text, "sentence_count": len(sentences)}]

        # Get embeddings for all sentences
        embeddings = [self.embedding_func(s) for s in sentences]

        # Find semantic breakpoints
        breakpoints = self._find_breakpoints(embeddings)

        # Create chunks
        chunks = []
        start_idx = 0

        for break_idx in breakpoints + [len(sentences)]:
            chunk_sentences = sentences[start_idx:break_idx]
            chunk_text = " ".join(chunk_sentences)

            # Check size constraints
            if len(chunk_text.split()) > self.max_chunk_size:
                # Split oversized chunk
                sub_chunks = self._split_chunk(chunk_sentences)
                chunks.extend(sub_chunks)
            elif len(chunk_text.split()) >= self.min_chunk_size:
                chunks.append({
                    "text": chunk_text,
                    "sentence_count": len(chunk_sentences)
                })
            elif chunks:
                # Merge with previous if too small
                prev = chunks[-1]
                prev["text"] += " " + chunk_text
                prev["sentence_count"] += len(chunk_sentences)

            start_idx = break_idx

        return chunks

    def _find_breakpoints(self, embeddings: List[np.ndarray]) -> List[int]:
        """Find indices where semantic similarity drops."""
        breakpoints = []

        for i in range(1, len(embeddings)):
            similarity = self._cosine_similarity(embeddings[i-1], embeddings[i])

            if similarity < self.similarity_threshold:
                breakpoints.append(i)

        return breakpoints

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def _split_chunk(self, sentences: List[str]) -> List[Dict]:
        """Split oversized chunk by size."""
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
                    chunks.append({
                        "text": " ".join(current),
                        "sentence_count": len(current)
                    })
                current = [sent]
                current_size = sent_size

        if current:
            chunks.append({
                "text": " ".join(current),
                "sentence_count": len(current)
            })

        return chunks
```

### Document Structure Chunking

```python
import re
from typing import List, Dict

class MarkdownChunker:
    """Chunk Markdown documents by headers and structure."""

    def __init__(
        self,
        max_chunk_size: int = 1000,
        include_header_in_chunk: bool = True
    ):
        self.max_chunk_size = max_chunk_size
        self.include_header = include_header_in_chunk

    def chunk(self, text: str) -> List[Dict]:
        """Split Markdown by headers."""
        # Pattern for headers
        header_pattern = r'^(#{1,6})\s+(.+)$'

        lines = text.split('\n')
        chunks = []
        current_chunk = {"headers": [], "content": [], "level": 0}

        for line in lines:
            header_match = re.match(header_pattern, line)

            if header_match:
                # Save current chunk if not empty
                if current_chunk["content"]:
                    chunks.append(self._finalize_chunk(current_chunk))

                # Start new chunk
                level = len(header_match.group(1))
                title = header_match.group(2)

                # Inherit higher-level headers
                parent_headers = [
                    h for h in current_chunk["headers"]
                    if h["level"] < level
                ]

                current_chunk = {
                    "headers": parent_headers + [{"level": level, "title": title}],
                    "content": [],
                    "level": level
                }

                if self.include_header:
                    current_chunk["content"].append(line)
            else:
                current_chunk["content"].append(line)

                # Check size
                content_text = '\n'.join(current_chunk["content"])
                if len(content_text.split()) > self.max_chunk_size:
                    # Split current chunk
                    chunks.append(self._finalize_chunk(current_chunk))
                    current_chunk["content"] = []

        # Don't forget last chunk
        if current_chunk["content"]:
            chunks.append(self._finalize_chunk(current_chunk))

        return chunks

    def _finalize_chunk(self, chunk: Dict) -> Dict:
        """Prepare chunk for output."""
        header_path = " > ".join(h["title"] for h in chunk["headers"])
        return {
            "text": '\n'.join(chunk["content"]).strip(),
            "header_path": header_path,
            "level": chunk["level"],
            "metadata": {
                "headers": [h["title"] for h in chunk["headers"]]
            }
        }


class HTMLChunker:
    """Chunk HTML documents by structure."""

    def __init__(self, max_chunk_size: int = 1000):
        self.max_chunk_size = max_chunk_size

    def chunk(self, html: str) -> List[Dict]:
        """Split HTML by structural elements."""
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'html.parser')
        chunks = []

        # Process by sections
        for section in soup.find_all(['section', 'article', 'div']):
            # Get section header if exists
            header = section.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            header_text = header.get_text() if header else ""

            # Get text content
            text = section.get_text(separator=' ', strip=True)

            if len(text.split()) <= self.max_chunk_size:
                chunks.append({
                    "text": text,
                    "header": header_text,
                    "tag": section.name
                })
            else:
                # Split large sections
                sub_chunks = self._split_text(text, header_text)
                chunks.extend(sub_chunks)

        return chunks

    def _split_text(self, text: str, header: str) -> List[Dict]:
        """Split large text sections."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.max_chunk_size):
            chunk_words = words[i:i + self.max_chunk_size]
            chunks.append({
                "text": " ".join(chunk_words),
                "header": header,
                "part": i // self.max_chunk_size + 1
            })

        return chunks
```

### Code Chunking

```python
import re
from typing import List, Dict

class CodeChunker:
    """Chunk code files by functions/classes."""

    def __init__(
        self,
        max_chunk_size: int = 800,
        language: str = "python"
    ):
        self.max_chunk_size = max_chunk_size
        self.language = language

    def chunk(self, code: str) -> List[Dict]:
        """Split code by logical units."""
        if self.language == "python":
            return self._chunk_python(code)
        elif self.language in ["javascript", "typescript"]:
            return self._chunk_javascript(code)
        else:
            return self._chunk_generic(code)

    def _chunk_python(self, code: str) -> List[Dict]:
        """Chunk Python code by classes and functions."""
        import ast

        try:
            tree = ast.parse(code)
        except SyntaxError:
            return self._chunk_generic(code)

        chunks = []
        lines = code.split('\n')

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start_line = node.lineno - 1
                end_line = node.end_lineno

                chunk_lines = lines[start_line:end_line]
                chunk_text = '\n'.join(chunk_lines)

                # Get docstring if exists
                docstring = ast.get_docstring(node) or ""

                chunks.append({
                    "text": chunk_text,
                    "type": "class" if isinstance(node, ast.ClassDef) else "function",
                    "name": node.name,
                    "docstring": docstring,
                    "start_line": start_line + 1,
                    "end_line": end_line
                })

        # Handle module-level code
        if not chunks:
            return self._chunk_generic(code)

        return chunks

    def _chunk_javascript(self, code: str) -> List[Dict]:
        """Chunk JavaScript/TypeScript code."""
        # Pattern for functions and classes
        patterns = [
            (r'((?:export\s+)?(?:async\s+)?function\s+\w+\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', 'function'),
            (r'((?:export\s+)?class\s+\w+[^{]*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', 'class'),
            (r'(const\s+\w+\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', 'arrow_function'),
        ]

        chunks = []
        for pattern, chunk_type in patterns:
            for match in re.finditer(pattern, code, re.MULTILINE | re.DOTALL):
                chunk_text = match.group(1)
                if len(chunk_text.split()) <= self.max_chunk_size:
                    # Extract name
                    name_match = re.search(r'(?:function|class|const)\s+(\w+)', chunk_text)
                    name = name_match.group(1) if name_match else "anonymous"

                    chunks.append({
                        "text": chunk_text,
                        "type": chunk_type,
                        "name": name
                    })

        if not chunks:
            return self._chunk_generic(code)

        return chunks

    def _chunk_generic(self, code: str) -> List[Dict]:
        """Generic code chunking by lines."""
        lines = code.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0

        for line in lines:
            line_words = len(line.split())

            if current_size + line_words <= self.max_chunk_size:
                current_chunk.append(line)
                current_size += line_words
            else:
                if current_chunk:
                    chunks.append({
                        "text": '\n'.join(current_chunk),
                        "type": "code_block",
                        "line_count": len(current_chunk)
                    })
                current_chunk = [line]
                current_size = line_words

        if current_chunk:
            chunks.append({
                "text": '\n'.join(current_chunk),
                "type": "code_block",
                "line_count": len(current_chunk)
            })

        return chunks
```

### Production Chunking Service

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import logging

class ChunkingStrategy(Enum):
    FIXED = "fixed"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"
    MARKDOWN = "markdown"
    CODE = "code"

@dataclass
class ChunkingConfig:
    strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE
    chunk_size: int = 500
    overlap: int = 50
    min_chunk_size: int = 100

class ChunkingService:
    """Production chunking service with multiple strategies."""

    def __init__(
        self,
        config: Optional[ChunkingConfig] = None,
        embedding_func: Optional[callable] = None
    ):
        self.config = config or ChunkingConfig()
        self.embedding_func = embedding_func
        self.logger = logging.getLogger(__name__)

    def chunk(
        self,
        text: str,
        strategy: Optional[ChunkingStrategy] = None,
        metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Chunk text using specified strategy."""
        strategy = strategy or self.config.strategy

        try:
            if strategy == ChunkingStrategy.FIXED:
                from chunking_basics import FixedSizeChunker
                chunks = FixedSizeChunker(
                    self.config.chunk_size,
                    self.config.overlap
                ).chunk(text)
            elif strategy == ChunkingStrategy.SENTENCE:
                from chunking_basics import SentenceChunker
                chunks = SentenceChunker(
                    self.config.chunk_size,
                    self.config.min_chunk_size
                ).chunk(text)
            elif strategy == ChunkingStrategy.SEMANTIC:
                if not self.embedding_func:
                    raise ValueError("Semantic chunking requires embedding function")
                chunks = SemanticChunker(
                    self.embedding_func,
                    max_chunk_size=self.config.chunk_size
                ).chunk(text)
            elif strategy == ChunkingStrategy.MARKDOWN:
                chunks = MarkdownChunker(
                    self.config.chunk_size
                ).chunk(text)
            else:
                from chunking_basics import RecursiveChunker
                chunks = RecursiveChunker(
                    self.config.chunk_size,
                    self.config.overlap
                ).chunk(text)

            # Add metadata to all chunks
            if metadata:
                for chunk in chunks:
                    chunk["metadata"] = {**metadata, **chunk.get("metadata", {})}

            self.logger.info(f"Created {len(chunks)} chunks using {strategy.value}")
            return chunks

        except Exception as e:
            self.logger.error(f"Chunking failed: {e}")
            # Fallback to simple splitting
            return self._fallback_chunk(text, metadata)

    def _fallback_chunk(self, text: str, metadata: Optional[Dict]) -> List[Dict]:
        """Simple fallback chunking."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.config.chunk_size):
            chunk_words = words[i:i + self.config.chunk_size]
            chunks.append({
                "text": " ".join(chunk_words),
                "metadata": metadata or {}
            })

        return chunks
```

## Implementation Guide

### Strategy Selection Matrix

| Content Type | Recommended Strategy | Reason |
|--------------|---------------------|--------|
| Markdown docs | MarkdownChunker | Preserves hierarchy |
| Code files | CodeChunker | Respects structure |
| Legal/Medical | SemanticChunker | Context-aware splits |
| News/Blog | RecursiveChunker | Natural boundaries |
| Mixed content | RecursiveChunker | General purpose |

### Usage Example

```python
# Production service
from chunking_advanced import ChunkingService, ChunkingConfig, ChunkingStrategy

config = ChunkingConfig(
    strategy=ChunkingStrategy.RECURSIVE,
    chunk_size=500,
    overlap=50
)

service = ChunkingService(config)

# Chunk document
chunks = service.chunk(
    text=document_text,
    metadata={"source": "doc.pdf", "page": 1}
)

# Use different strategy for code
code_chunks = service.chunk(
    text=code_content,
    strategy=ChunkingStrategy.CODE,
    metadata={"file": "main.py"}
)
```

## Advanced Best Practices

1. **Preserve Metadata**
   - Track source documents
   - Maintain hierarchy paths
   - Store chunk position

2. **Handle Edge Cases**
   - Empty documents
   - Oversized single paragraphs
   - Mixed content types

3. **Performance Optimization**
   - Cache embeddings for semantic chunking
   - Batch process multiple documents
   - Use AST parsing for code

4. **Quality Validation**
   - Test retrieval accuracy
   - Check chunk size distribution
   - Verify context preservation

## Sources

- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [LlamaIndex Node Parsers](https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/)
- [Late Chunking Paper](https://arxiv.org/abs/2409.04701)
- [Semantic Chunking with LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking/)
