# Chunking Strategy Code Examples

Production-ready code examples for all chunking strategies.

---

## Table of Contents

1. [Fixed-Size Chunking](#1-fixed-size-chunking)
2. [Recursive Chunking](#2-recursive-chunking)
3. [Semantic Chunking](#3-semantic-chunking)
4. [Document Structure Chunking](#4-document-structure-chunking)
5. [Code-Aware Chunking](#5-code-aware-chunking)
6. [Late Chunking](#6-late-chunking)
7. [Agentic Chunking](#7-agentic-chunking)
8. [Hierarchical Chunking](#8-hierarchical-chunking)
9. [Production Service](#9-production-chunking-service)
10. [Comparison Examples](#10-comparison-examples)
11. [Optimization Examples](#11-optimization-examples)

---

## 1. Fixed-Size Chunking

### Basic Implementation

```python
from typing import List, Dict
import tiktoken

class FixedSizeChunker:
    """Split text into fixed-size token chunks with overlap."""

    def __init__(
        self,
        chunk_size: int = 512,
        overlap: int = 50,
        encoding_name: str = "cl100k_base"
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.encoding = tiktoken.get_encoding(encoding_name)

    def chunk(self, text: str) -> List[Dict]:
        """Split text into fixed-size chunks."""
        tokens = self.encoding.encode(text)
        chunks = []

        start = 0
        chunk_index = 0

        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)

            chunks.append({
                "text": chunk_text,
                "chunk_index": chunk_index,
                "token_count": len(chunk_tokens),
                "start_token": start,
                "end_token": end
            })

            chunk_index += 1
            start = end - self.overlap if end < len(tokens) else end

        return chunks

# Usage
chunker = FixedSizeChunker(chunk_size=512, overlap=50)
chunks = chunker.chunk(document_text)

for chunk in chunks:
    print(f"Chunk {chunk['chunk_index']}: {chunk['token_count']} tokens")
```

### Using Chonkie

```python
from chonkie import TokenChunker
from tokenizers import Tokenizer

# Initialize with tokenizer
tokenizer = Tokenizer.from_pretrained("gpt2")
chunker = TokenChunker(
    tokenizer=tokenizer,
    chunk_size=512,
    chunk_overlap=50
)

# Chunk text
chunks = chunker.chunk(document_text)

for chunk in chunks:
    print(f"Tokens: {chunk.token_count}, Text: {chunk.text[:50]}...")
```

### Using LangChain

```python
from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    encoding_name="cl100k_base"
)

chunks = splitter.split_text(document_text)
```

---

## 2. Recursive Chunking

### Basic Implementation

```python
from typing import List, Dict, Optional
import re

class RecursiveChunker:
    """Recursively split text by multiple separators."""

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
        separators: Optional[List[str]] = None
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separators = separators or ["\n\n", "\n", ". ", " "]

    def chunk(self, text: str) -> List[Dict]:
        """Split text recursively."""
        return self._split_text(text, self.separators)

    def _split_text(
        self,
        text: str,
        separators: List[str]
    ) -> List[Dict]:
        """Recursively split text by separators."""
        if not text:
            return []

        # If text is small enough, return as single chunk
        if len(text.split()) <= self.chunk_size:
            return [{"text": text.strip(), "word_count": len(text.split())}]

        # Find the first separator that exists in text
        separator = None
        for sep in separators:
            if sep in text:
                separator = sep
                break

        # If no separator found, fall back to word splitting
        if separator is None:
            return self._split_by_words(text)

        # Split by separator
        splits = text.split(separator)
        chunks = []
        current_chunk = []
        current_size = 0

        for split in splits:
            split_size = len(split.split())

            if current_size + split_size <= self.chunk_size:
                current_chunk.append(split)
                current_size += split_size
            else:
                # Save current chunk
                if current_chunk:
                    chunk_text = separator.join(current_chunk).strip()
                    if chunk_text:
                        chunks.append({
                            "text": chunk_text,
                            "word_count": len(chunk_text.split())
                        })

                # Check if split itself is too large
                if split_size > self.chunk_size:
                    # Recursively split with remaining separators
                    remaining_separators = separators[separators.index(separator) + 1:]
                    sub_chunks = self._split_text(split, remaining_separators)
                    chunks.extend(sub_chunks)
                    current_chunk = []
                    current_size = 0
                else:
                    current_chunk = [split]
                    current_size = split_size

        # Don't forget last chunk
        if current_chunk:
            chunk_text = separator.join(current_chunk).strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "word_count": len(chunk_text.split())
                })

        return self._add_overlap(chunks)

    def _split_by_words(self, text: str) -> List[Dict]:
        """Final fallback: split by words."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunks.append({
                "text": " ".join(chunk_words),
                "word_count": len(chunk_words)
            })

        return chunks

    def _add_overlap(self, chunks: List[Dict]) -> List[Dict]:
        """Add overlap between chunks."""
        if self.overlap == 0 or len(chunks) <= 1:
            return chunks

        result = []
        for i, chunk in enumerate(chunks):
            if i > 0 and self.overlap > 0:
                # Get last N words from previous chunk
                prev_words = chunks[i-1]["text"].split()[-self.overlap:]
                chunk["text"] = " ".join(prev_words) + " " + chunk["text"]
                chunk["word_count"] = len(chunk["text"].split())
            result.append(chunk)

        return result

# Usage
chunker = RecursiveChunker(chunk_size=500, overlap=50)
chunks = chunker.chunk(document_text)
```

### Using LangChain

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,  # characters
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " "],
    length_function=len
)

# Or with token counting
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)

chunks = splitter.split_text(document_text)
```

### Using Chonkie

```python
from chonkie import RecursiveChunker
from tokenizers import Tokenizer

tokenizer = Tokenizer.from_pretrained("gpt2")

chunker = RecursiveChunker(
    tokenizer=tokenizer,
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)

chunks = chunker.chunk(document_text)
```

---

## 3. Semantic Chunking

### Basic Implementation

```python
import numpy as np
from typing import List, Dict, Callable
import nltk

class SemanticChunker:
    """Chunk based on semantic similarity between sentences."""

    def __init__(
        self,
        embedding_func: Callable[[str], np.ndarray],
        similarity_threshold: float = 0.75,
        max_chunk_size: int = 1000,
        min_chunk_size: int = 100,
        buffer_size: int = 1
    ):
        self.embedding_func = embedding_func
        self.similarity_threshold = similarity_threshold
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.buffer_size = buffer_size

    def chunk(self, text: str) -> List[Dict]:
        """Split text based on semantic breaks."""
        sentences = nltk.sent_tokenize(text)

        if len(sentences) <= 1:
            return [{"text": text, "sentence_count": len(sentences)}]

        # Get embeddings for all sentences
        embeddings = self._get_embeddings(sentences)

        # Calculate similarities between adjacent sentences
        similarities = self._calculate_similarities(embeddings)

        # Find breakpoints using threshold or gradient
        breakpoints = self._find_breakpoints(similarities)

        # Create chunks from breakpoints
        chunks = self._create_chunks(sentences, breakpoints)

        return chunks

    def _get_embeddings(self, sentences: List[str]) -> List[np.ndarray]:
        """Get embeddings with optional buffering."""
        embeddings = []

        for i, sentence in enumerate(sentences):
            # Include buffer sentences for context
            start = max(0, i - self.buffer_size)
            end = min(len(sentences), i + self.buffer_size + 1)
            context = " ".join(sentences[start:end])

            embedding = self.embedding_func(context)
            embeddings.append(embedding)

        return embeddings

    def _calculate_similarities(
        self,
        embeddings: List[np.ndarray]
    ) -> List[float]:
        """Calculate cosine similarity between adjacent embeddings."""
        similarities = []

        for i in range(1, len(embeddings)):
            sim = self._cosine_similarity(embeddings[i-1], embeddings[i])
            similarities.append(sim)

        return similarities

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity."""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def _find_breakpoints(self, similarities: List[float]) -> List[int]:
        """Find indices where semantic similarity drops."""
        # Method 1: Simple threshold
        breakpoints = []
        for i, sim in enumerate(similarities):
            if sim < self.similarity_threshold:
                breakpoints.append(i + 1)  # +1 because similarities are between i and i+1

        return breakpoints

    def _find_breakpoints_percentile(
        self,
        similarities: List[float],
        percentile: float = 25
    ) -> List[int]:
        """Find breakpoints using percentile threshold."""
        threshold = np.percentile(similarities, percentile)

        breakpoints = []
        for i, sim in enumerate(similarities):
            if sim < threshold:
                breakpoints.append(i + 1)

        return breakpoints

    def _find_breakpoints_gradient(
        self,
        similarities: List[float],
        gradient_threshold: float = 0.1
    ) -> List[int]:
        """Find breakpoints using gradient (sudden drops)."""
        breakpoints = []

        for i in range(1, len(similarities)):
            gradient = similarities[i-1] - similarities[i]
            if gradient > gradient_threshold:
                breakpoints.append(i + 1)

        return breakpoints

    def _create_chunks(
        self,
        sentences: List[str],
        breakpoints: List[int]
    ) -> List[Dict]:
        """Create chunks from sentences and breakpoints."""
        chunks = []
        start_idx = 0

        for break_idx in breakpoints + [len(sentences)]:
            chunk_sentences = sentences[start_idx:break_idx]
            chunk_text = " ".join(chunk_sentences)

            # Check size constraints
            word_count = len(chunk_text.split())

            if word_count > self.max_chunk_size:
                # Split oversized chunk
                sub_chunks = self._split_oversized(chunk_sentences)
                chunks.extend(sub_chunks)
            elif word_count >= self.min_chunk_size or not chunks:
                chunks.append({
                    "text": chunk_text,
                    "sentence_count": len(chunk_sentences),
                    "word_count": word_count
                })
            else:
                # Merge with previous chunk if too small
                if chunks:
                    prev = chunks[-1]
                    prev["text"] += " " + chunk_text
                    prev["sentence_count"] += len(chunk_sentences)
                    prev["word_count"] = len(prev["text"].split())

            start_idx = break_idx

        return chunks

    def _split_oversized(self, sentences: List[str]) -> List[Dict]:
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
                        "sentence_count": len(current),
                        "word_count": current_size
                    })
                current = [sent]
                current_size = sent_size

        if current:
            chunks.append({
                "text": " ".join(current),
                "sentence_count": len(current),
                "word_count": current_size
            })

        return chunks

# Usage with OpenAI embeddings
from openai import OpenAI

client = OpenAI()

def get_embedding(text: str) -> np.ndarray:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

chunker = SemanticChunker(
    embedding_func=get_embedding,
    similarity_threshold=0.75,
    max_chunk_size=500,
    min_chunk_size=100
)

chunks = chunker.chunk(document_text)
```

### Using Chonkie SemanticChunker

```python
from chonkie import SemanticChunker
from chonkie.embeddings import OpenAIEmbeddings

# Initialize embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create semantic chunker
chunker = SemanticChunker(
    embeddings=embeddings,
    chunk_size=512,
    similarity_threshold=0.75,
    similarity_percentile=None,  # Use threshold instead
)

chunks = chunker.chunk(document_text)

for chunk in chunks:
    print(f"Chunk: {chunk.text[:100]}...")
    print(f"Sentences: {chunk.sentence_count}")
```

### Using LlamaIndex

```python
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding(model="text-embedding-3-small")

splitter = SemanticSplitterNodeParser(
    buffer_size=1,
    breakpoint_percentile_threshold=95,
    embed_model=embed_model
)

nodes = splitter.get_nodes_from_documents(documents)
```

### Semantic Double-Pass Merge (SDPM)

```python
from chonkie import SDPMChunker
from chonkie.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings(
    model="all-MiniLM-L6-v2"
)

# SDPM: First pass splits, second pass merges similar adjacent chunks
chunker = SDPMChunker(
    embeddings=embeddings,
    chunk_size=512,
    similarity_threshold=0.7,
    skip_window=2  # Look ahead for merging
)

chunks = chunker.chunk(document_text)
```

---

## 4. Document Structure Chunking

### Markdown Chunking

```python
import re
from typing import List, Dict

class MarkdownChunker:
    """Chunk Markdown documents by headers and structure."""

    def __init__(
        self,
        max_chunk_size: int = 1000,
        include_header_in_chunk: bool = True,
        min_header_level: int = 1,
        max_header_level: int = 6
    ):
        self.max_chunk_size = max_chunk_size
        self.include_header = include_header_in_chunk
        self.min_level = min_header_level
        self.max_level = max_header_level

    def chunk(self, text: str) -> List[Dict]:
        """Split Markdown by headers."""
        header_pattern = r'^(#{1,6})\s+(.+)$'
        lines = text.split('\n')
        chunks = []
        current_chunk = {
            "headers": [],
            "content": [],
            "level": 0
        }

        for line in lines:
            header_match = re.match(header_pattern, line)

            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()

                # Check if header is in allowed range
                if self.min_level <= level <= self.max_level:
                    # Save current chunk if not empty
                    if current_chunk["content"]:
                        chunks.append(self._finalize_chunk(current_chunk))

                    # Inherit parent headers (lower levels)
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
            else:
                current_chunk["content"].append(line)

                # Check size and split if needed
                content_text = '\n'.join(current_chunk["content"])
                if len(content_text.split()) > self.max_chunk_size:
                    chunks.append(self._finalize_chunk(current_chunk))
                    # Keep headers but reset content
                    current_chunk["content"] = []

        # Don't forget last chunk
        if current_chunk["content"]:
            chunks.append(self._finalize_chunk(current_chunk))

        return chunks

    def _finalize_chunk(self, chunk: Dict) -> Dict:
        """Prepare chunk for output."""
        header_path = " > ".join(h["title"] for h in chunk["headers"])
        content = '\n'.join(chunk["content"]).strip()

        return {
            "text": content,
            "header_path": header_path,
            "level": chunk["level"],
            "word_count": len(content.split()),
            "metadata": {
                "headers": [h["title"] for h in chunk["headers"]],
                "header_levels": [h["level"] for h in chunk["headers"]]
            }
        }

# Usage
chunker = MarkdownChunker(max_chunk_size=500)
chunks = chunker.chunk(markdown_text)

for chunk in chunks:
    print(f"Path: {chunk['header_path']}")
    print(f"Content: {chunk['text'][:100]}...")
```

### Using LangChain for Markdown

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False
)

chunks = splitter.split_text(markdown_text)

for chunk in chunks:
    print(f"Content: {chunk.page_content[:100]}...")
    print(f"Metadata: {chunk.metadata}")
```

### HTML Chunking

```python
from bs4 import BeautifulSoup
from typing import List, Dict

class HTMLChunker:
    """Chunk HTML documents by structure."""

    def __init__(
        self,
        max_chunk_size: int = 1000,
        split_tags: List[str] = None
    ):
        self.max_chunk_size = max_chunk_size
        self.split_tags = split_tags or ['section', 'article', 'div', 'p']

    def chunk(self, html: str) -> List[Dict]:
        """Split HTML by structural elements."""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        chunks = []

        # Process structural elements
        for tag_name in self.split_tags:
            for element in soup.find_all(tag_name):
                chunk = self._process_element(element)
                if chunk:
                    chunks.append(chunk)

        # If no structural elements found, process body
        if not chunks:
            body = soup.find('body') or soup
            text = body.get_text(separator=' ', strip=True)
            chunks = self._split_text(text)

        return chunks

    def _process_element(self, element) -> Dict | None:
        """Process a single HTML element."""
        # Get header if exists
        header = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        header_text = header.get_text(strip=True) if header else ""

        # Get text content
        text = element.get_text(separator=' ', strip=True)

        if not text or len(text) < 10:
            return None

        word_count = len(text.split())

        if word_count <= self.max_chunk_size:
            return {
                "text": text,
                "header": header_text,
                "tag": element.name,
                "word_count": word_count,
                "metadata": {
                    "id": element.get('id', ''),
                    "class": element.get('class', [])
                }
            }
        else:
            # Return as multiple chunks
            return self._split_text(text, header_text)[0]

    def _split_text(
        self,
        text: str,
        header: str = ""
    ) -> List[Dict]:
        """Split large text sections."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.max_chunk_size):
            chunk_words = words[i:i + self.max_chunk_size]
            chunks.append({
                "text": " ".join(chunk_words),
                "header": header,
                "part": i // self.max_chunk_size + 1,
                "word_count": len(chunk_words)
            })

        return chunks

# Usage
chunker = HTMLChunker(max_chunk_size=500)
chunks = chunker.chunk(html_content)
```

### Using LangChain for HTML

```python
from langchain.text_splitter import HTMLHeaderTextSplitter

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
]

splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
chunks = splitter.split_text(html_text)
```

---

## 5. Code-Aware Chunking

### Python Code Chunking with AST

```python
import ast
from typing import List, Dict

class PythonCodeChunker:
    """Chunk Python code by functions and classes using AST."""

    def __init__(
        self,
        max_chunk_size: int = 800,
        include_imports: bool = True,
        include_docstrings: bool = True
    ):
        self.max_chunk_size = max_chunk_size
        self.include_imports = include_imports
        self.include_docstrings = include_docstrings

    def chunk(self, code: str) -> List[Dict]:
        """Split Python code by logical units."""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            # Fallback to line-based chunking
            return self._chunk_by_lines(code)

        lines = code.split('\n')
        chunks = []

        # Extract imports
        imports = []
        if self.include_imports:
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_line = lines[node.lineno - 1]
                    imports.append(import_line)

        import_block = '\n'.join(imports) if imports else ""

        # Extract functions and classes
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                chunk = self._extract_function(node, lines, import_block)
                chunks.append(chunk)

            elif isinstance(node, ast.ClassDef):
                chunk = self._extract_class(node, lines, import_block)
                chunks.append(chunk)

        # If no functions/classes found, chunk by lines
        if not chunks:
            return self._chunk_by_lines(code)

        return chunks

    def _extract_function(
        self,
        node: ast.FunctionDef,
        lines: List[str],
        import_block: str
    ) -> Dict:
        """Extract a function as a chunk."""
        start_line = node.lineno - 1
        end_line = node.end_lineno

        # Include decorators
        if node.decorator_list:
            start_line = node.decorator_list[0].lineno - 1

        function_lines = lines[start_line:end_line]
        function_code = '\n'.join(function_lines)

        # Prepend imports if enabled
        if import_block:
            function_code = import_block + '\n\n' + function_code

        docstring = ast.get_docstring(node) or ""

        return {
            "text": function_code,
            "type": "function",
            "name": node.name,
            "docstring": docstring,
            "start_line": start_line + 1,
            "end_line": end_line,
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "parameters": [arg.arg for arg in node.args.args],
            "decorators": [
                ast.unparse(d) for d in node.decorator_list
            ] if node.decorator_list else []
        }

    def _extract_class(
        self,
        node: ast.ClassDef,
        lines: List[str],
        import_block: str
    ) -> Dict:
        """Extract a class as a chunk."""
        start_line = node.lineno - 1
        end_line = node.end_lineno

        # Include decorators
        if node.decorator_list:
            start_line = node.decorator_list[0].lineno - 1

        class_lines = lines[start_line:end_line]
        class_code = '\n'.join(class_lines)

        # Prepend imports if enabled
        if import_block:
            class_code = import_block + '\n\n' + class_code

        docstring = ast.get_docstring(node) or ""

        # Extract method names
        methods = [
            n.name for n in ast.iter_child_nodes(node)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        return {
            "text": class_code,
            "type": "class",
            "name": node.name,
            "docstring": docstring,
            "start_line": start_line + 1,
            "end_line": end_line,
            "methods": methods,
            "bases": [ast.unparse(base) for base in node.bases]
        }

    def _chunk_by_lines(self, code: str) -> List[Dict]:
        """Fallback: chunk by lines."""
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

# Usage
chunker = PythonCodeChunker(max_chunk_size=800)
chunks = chunker.chunk(python_code)

for chunk in chunks:
    print(f"Type: {chunk['type']}, Name: {chunk.get('name', 'N/A')}")
```

### JavaScript/TypeScript Chunking

```python
import re
from typing import List, Dict

class JavaScriptChunker:
    """Chunk JavaScript/TypeScript code by functions and classes."""

    def __init__(self, max_chunk_size: int = 800):
        self.max_chunk_size = max_chunk_size

        # Patterns for JS/TS constructs
        self.patterns = [
            # Regular functions
            (r'((?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\([^)]*\)\s*\{)', 'function'),
            # Arrow functions assigned to const/let/var
            (r'((?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>)', 'arrow_function'),
            # Classes
            (r'((?:export\s+)?class\s+(\w+)(?:\s+extends\s+\w+)?\s*\{)', 'class'),
            # React components (function)
            (r'((?:export\s+)?(?:const|function)\s+(\w+)\s*[=:]?\s*(?:\([^)]*\)\s*)?(?:=>)?\s*\{?\s*(?:return\s+)?<)', 'component'),
        ]

    def chunk(self, code: str) -> List[Dict]:
        """Split JavaScript code by logical units."""
        chunks = []
        used_ranges = set()

        for pattern, chunk_type in self.patterns:
            for match in re.finditer(pattern, code, re.MULTILINE):
                start = match.start()

                # Skip if this range was already used
                if any(start >= r[0] and start < r[1] for r in used_ranges):
                    continue

                # Find matching closing brace
                end = self._find_closing_brace(code, match.end())

                if end:
                    chunk_text = code[start:end]
                    name = match.group(2) if match.lastindex >= 2 else "anonymous"

                    word_count = len(chunk_text.split())
                    if word_count <= self.max_chunk_size:
                        chunks.append({
                            "text": chunk_text,
                            "type": chunk_type,
                            "name": name,
                            "start_char": start,
                            "end_char": end,
                            "word_count": word_count
                        })
                        used_ranges.add((start, end))

        # Sort by position in file
        chunks.sort(key=lambda x: x["start_char"])

        # Fallback if no chunks found
        if not chunks:
            return self._chunk_by_lines(code)

        return chunks

    def _find_closing_brace(self, code: str, start: int) -> int | None:
        """Find the matching closing brace."""
        # Handle arrow functions without braces
        if '=>' in code[max(0, start-20):start]:
            # Check if it's a single-expression arrow function
            next_semicolon = code.find(';', start)
            next_newline = code.find('\n', start)
            if next_semicolon != -1 and (next_newline == -1 or next_semicolon < next_newline):
                return next_semicolon + 1

        brace_count = 0
        i = start

        while i < len(code):
            if code[i] == '{':
                brace_count += 1
            elif code[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    return i + 1
            i += 1

        return None

    def _chunk_by_lines(self, code: str) -> List[Dict]:
        """Fallback chunking by lines."""
        lines = code.split('\n')
        chunks = []
        current = []
        current_size = 0

        for line in lines:
            size = len(line.split())
            if current_size + size <= self.max_chunk_size:
                current.append(line)
                current_size += size
            else:
                if current:
                    chunks.append({
                        "text": '\n'.join(current),
                        "type": "code_block",
                        "word_count": current_size
                    })
                current = [line]
                current_size = size

        if current:
            chunks.append({
                "text": '\n'.join(current),
                "type": "code_block",
                "word_count": current_size
            })

        return chunks

# Usage
chunker = JavaScriptChunker(max_chunk_size=800)
chunks = chunker.chunk(javascript_code)
```

### Using Chonkie CodeChunker

```python
from chonkie import CodeChunker

# Supports Python, JavaScript, TypeScript, Go, Rust, etc.
chunker = CodeChunker(
    language="python",  # or "javascript", "typescript", "go", etc.
    chunk_size=800,
    include_signature=True
)

chunks = chunker.chunk(code_content)

for chunk in chunks:
    print(f"Type: {chunk.chunk_type}, Name: {chunk.name}")
    print(f"Code: {chunk.text[:200]}...")
```

### Using LangChain

```python
from langchain.text_splitter import (
    PythonCodeTextSplitter,
    Language,
    RecursiveCharacterTextSplitter
)

# Python
python_splitter = PythonCodeTextSplitter(
    chunk_size=2000,
    chunk_overlap=200
)

# JavaScript/TypeScript
js_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.JS,
    chunk_size=2000,
    chunk_overlap=200
)

# TypeScript
ts_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.TS,
    chunk_size=2000,
    chunk_overlap=200
)

python_chunks = python_splitter.split_text(python_code)
js_chunks = js_splitter.split_text(javascript_code)
```

---

## 6. Late Chunking

### Using Jina AI

```python
import requests
import numpy as np
from typing import List, Dict

class LateChunker:
    """Late chunking using Jina embeddings."""

    def __init__(
        self,
        api_key: str,
        model: str = "jina-embeddings-v3",
        chunk_size: int = 512
    ):
        self.api_key = api_key
        self.model = model
        self.chunk_size = chunk_size
        self.api_url = "https://api.jina.ai/v1/embeddings"

    def chunk_and_embed(self, text: str) -> List[Dict]:
        """Apply late chunking: embed first, then chunk."""
        # First, get token-level embeddings
        response = requests.post(
            self.api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "input": [text],
                "model": self.model,
                "encoding_type": "float",
                "late_chunking": True,
                "chunk_size": self.chunk_size
            }
        )

        response.raise_for_status()
        result = response.json()

        chunks = []
        for i, chunk_data in enumerate(result.get("data", [])):
            chunks.append({
                "text": chunk_data.get("text", ""),
                "embedding": np.array(chunk_data["embedding"]),
                "chunk_index": i,
                "token_count": chunk_data.get("token_count", 0)
            })

        return chunks

# Usage
chunker = LateChunker(
    api_key="jina_xxx",
    chunk_size=512
)

chunks = chunker.chunk_and_embed(long_document)

for chunk in chunks:
    print(f"Chunk {chunk['chunk_index']}: {chunk['text'][:100]}...")
    print(f"Embedding shape: {chunk['embedding'].shape}")
```

### Using Chonkie LateChunker (Experimental)

```python
from chonkie import LateChunker
from chonkie.embeddings import JinaEmbeddings

# Initialize with Jina embeddings
embeddings = JinaEmbeddings(
    model="jina-embeddings-v3",
    api_key="your-api-key"
)

chunker = LateChunker(
    embeddings=embeddings,
    chunk_size=512
)

chunks = chunker.chunk(document_text)

for chunk in chunks:
    print(f"Text: {chunk.text[:100]}...")
    print(f"Embedding: {chunk.embedding[:5]}...")
```

### Manual Late Chunking Implementation

```python
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

class ManualLateChunker:
    """
    Manual late chunking using HuggingFace transformers.
    Embeds entire document, then chunks the embeddings.
    """

    def __init__(
        self,
        model_name: str = "jinaai/jina-embeddings-v2-base-en",
        chunk_size: int = 512,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(device)
        self.chunk_size = chunk_size
        self.device = device

    def chunk(self, text: str) -> List[Dict]:
        """Apply late chunking."""
        # Tokenize the entire document
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=8192  # Long context model limit
        ).to(self.device)

        # Get token-level embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            token_embeddings = outputs.last_hidden_state.squeeze(0)

        # Get token-to-character mapping
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"].squeeze())

        # Define chunk boundaries in tokens
        num_tokens = len(tokens)
        chunks = []

        for start in range(0, num_tokens, self.chunk_size):
            end = min(start + self.chunk_size, num_tokens)

            # Get chunk text
            chunk_token_ids = inputs["input_ids"].squeeze()[start:end]
            chunk_text = self.tokenizer.decode(chunk_token_ids, skip_special_tokens=True)

            # Mean pooling over chunk tokens
            chunk_embedding = token_embeddings[start:end].mean(dim=0)

            chunks.append({
                "text": chunk_text,
                "embedding": chunk_embedding.cpu().numpy(),
                "start_token": start,
                "end_token": end,
                "token_count": end - start
            })

        return chunks

# Usage
chunker = ManualLateChunker(chunk_size=512)
chunks = chunker.chunk(long_document)
```

---

## 7. Agentic Chunking

### Basic LLM-Based Chunking

```python
from typing import List, Dict
from openai import OpenAI

class AgenticChunker:
    """
    Agentic chunking: LLM decides how to chunk each document.
    """

    def __init__(
        self,
        client: OpenAI,
        model: str = "gpt-4o-mini",
        max_chunk_size: int = 500
    ):
        self.client = client
        self.model = model
        self.max_chunk_size = max_chunk_size

    def chunk(self, text: str, document_type: str = "general") -> List[Dict]:
        """Let LLM decide chunking strategy and apply it."""
        # Step 1: Analyze document and decide strategy
        strategy = self._decide_strategy(text, document_type)

        # Step 2: Apply chosen strategy
        if strategy["method"] == "semantic":
            chunks = self._semantic_split(text, strategy)
        elif strategy["method"] == "structure":
            chunks = self._structure_split(text, strategy)
        elif strategy["method"] == "topic":
            chunks = self._topic_split(text, strategy)
        else:
            chunks = self._default_split(text)

        # Step 3: Enrich chunks with metadata
        enriched_chunks = self._enrich_chunks(chunks, document_type)

        return enriched_chunks

    def _decide_strategy(self, text: str, document_type: str) -> Dict:
        """Ask LLM to decide chunking strategy."""
        prompt = f"""Analyze this document and decide the best chunking strategy.

Document type: {document_type}
Document preview (first 2000 chars):
{text[:2000]}

Consider:
1. Document structure (headers, sections, lists)
2. Content density (technical vs. narrative)
3. Topic changes
4. Target chunk size: {self.max_chunk_size} words

Respond with JSON:
{{
    "method": "semantic" | "structure" | "topic" | "fixed",
    "reasoning": "brief explanation",
    "split_points": ["description of where to split"],
    "metadata_fields": ["suggested metadata to extract"]
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        import json
        return json.loads(response.choices[0].message.content)

    def _semantic_split(self, text: str, strategy: Dict) -> List[Dict]:
        """Ask LLM to identify semantic boundaries."""
        prompt = f"""Split this text into semantically coherent chunks.

Rules:
1. Each chunk should be about one topic/concept
2. Target size: {self.max_chunk_size} words per chunk
3. Don't split mid-sentence
4. Mark natural topic transitions

Text:
{text}

Respond with JSON:
{{
    "chunks": [
        {{"text": "chunk content", "topic": "brief topic description"}}
    ]
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        import json
        result = json.loads(response.choices[0].message.content)
        return result.get("chunks", [])

    def _structure_split(self, text: str, strategy: Dict) -> List[Dict]:
        """Split by document structure."""
        prompt = f"""Split this text by its structural elements (headers, sections, etc.).

Text:
{text}

Respond with JSON:
{{
    "chunks": [
        {{
            "text": "chunk content",
            "section": "section name/path",
            "level": 1-6
        }}
    ]
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        import json
        result = json.loads(response.choices[0].message.content)
        return result.get("chunks", [])

    def _topic_split(self, text: str, strategy: Dict) -> List[Dict]:
        """Split by topic boundaries."""
        prompt = f"""Identify topic changes in this text and split accordingly.

Text:
{text}

For each chunk, identify:
1. The main topic
2. Key entities mentioned
3. Start and end of the topic segment

Respond with JSON:
{{
    "chunks": [
        {{
            "text": "chunk content",
            "topic": "main topic",
            "entities": ["entity1", "entity2"],
            "summary": "one sentence summary"
        }}
    ]
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        import json
        result = json.loads(response.choices[0].message.content)
        return result.get("chunks", [])

    def _default_split(self, text: str) -> List[Dict]:
        """Fallback: simple paragraph split."""
        paragraphs = text.split('\n\n')
        chunks = []
        current = []
        current_size = 0

        for para in paragraphs:
            size = len(para.split())
            if current_size + size <= self.max_chunk_size:
                current.append(para)
                current_size += size
            else:
                if current:
                    chunks.append({"text": '\n\n'.join(current)})
                current = [para]
                current_size = size

        if current:
            chunks.append({"text": '\n\n'.join(current)})

        return chunks

    def _enrich_chunks(
        self,
        chunks: List[Dict],
        document_type: str
    ) -> List[Dict]:
        """Add metadata to each chunk."""
        enriched = []

        for i, chunk in enumerate(chunks):
            # Add basic metadata
            chunk["chunk_index"] = i
            chunk["word_count"] = len(chunk.get("text", "").split())
            chunk["document_type"] = document_type

            # Generate title/summary if not present
            if "summary" not in chunk:
                chunk["summary"] = self._generate_summary(chunk["text"])

            enriched.append(chunk)

        return enriched

    def _generate_summary(self, text: str) -> str:
        """Generate a brief summary for the chunk."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": f"Summarize in one sentence (max 20 words):\n\n{text[:500]}"
            }],
            max_tokens=50
        )
        return response.choices[0].message.content.strip()

# Usage
client = OpenAI()
chunker = AgenticChunker(client, max_chunk_size=500)

# Chunk a legal document
chunks = chunker.chunk(
    text=legal_document,
    document_type="legal_contract"
)

for chunk in chunks:
    print(f"Topic: {chunk.get('topic', 'N/A')}")
    print(f"Summary: {chunk.get('summary', 'N/A')}")
    print(f"Text: {chunk['text'][:100]}...")
```

### Using Chonkie SlumberChunker (Agentic)

```python
from chonkie import SlumberChunker
from chonkie.llms import OpenAILLM

# Initialize LLM
llm = OpenAILLM(model="gpt-4o-mini")

# SlumberChunker = Agentic chunking
chunker = SlumberChunker(
    llm=llm,
    chunk_size=512,
    chunk_overlap=50
)

chunks = chunker.chunk(document_text)

for chunk in chunks:
    print(f"Chunk: {chunk.text[:100]}...")
```

---

## 8. Hierarchical Chunking

### Multi-Level Hierarchy

```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class HierarchicalChunk:
    text: str
    level: str  # "document", "section", "paragraph"
    parent_id: str | None
    chunk_id: str
    children: List[str]
    metadata: Dict

class HierarchicalChunker:
    """
    Create multi-level chunk hierarchy.
    Levels: document > section > paragraph
    """

    def __init__(
        self,
        section_max_size: int = 2000,
        paragraph_max_size: int = 500
    ):
        self.section_max_size = section_max_size
        self.paragraph_max_size = paragraph_max_size

    def chunk(self, text: str, doc_id: str = "doc_001") -> List[HierarchicalChunk]:
        """Create hierarchical chunks."""
        chunks = []

        # Level 1: Document summary
        doc_chunk = HierarchicalChunk(
            text=self._create_summary(text),
            level="document",
            parent_id=None,
            chunk_id=doc_id,
            children=[],
            metadata={"word_count": len(text.split())}
        )
        chunks.append(doc_chunk)

        # Level 2: Sections
        sections = self._split_into_sections(text)
        section_ids = []

        for i, section in enumerate(sections):
            section_id = f"{doc_id}_section_{i:03d}"
            section_ids.append(section_id)

            section_chunk = HierarchicalChunk(
                text=section["text"],
                level="section",
                parent_id=doc_id,
                chunk_id=section_id,
                children=[],
                metadata={
                    "header": section.get("header", ""),
                    "word_count": len(section["text"].split())
                }
            )
            chunks.append(section_chunk)

            # Level 3: Paragraphs
            paragraphs = self._split_into_paragraphs(section["text"])
            paragraph_ids = []

            for j, para in enumerate(paragraphs):
                para_id = f"{section_id}_para_{j:03d}"
                paragraph_ids.append(para_id)

                para_chunk = HierarchicalChunk(
                    text=para,
                    level="paragraph",
                    parent_id=section_id,
                    chunk_id=para_id,
                    children=[],
                    metadata={"word_count": len(para.split())}
                )
                chunks.append(para_chunk)

            # Update section children
            section_chunk.children = paragraph_ids

        # Update document children
        doc_chunk.children = section_ids

        return chunks

    def _create_summary(self, text: str) -> str:
        """Create document summary (first 500 words or custom logic)."""
        words = text.split()
        return " ".join(words[:500]) + ("..." if len(words) > 500 else "")

    def _split_into_sections(self, text: str) -> List[Dict]:
        """Split text into sections by headers or size."""
        import re

        # Try to split by headers
        header_pattern = r'^(#{1,3})\s+(.+)$'
        lines = text.split('\n')

        sections = []
        current_section = {"header": "", "content": []}

        for line in lines:
            header_match = re.match(header_pattern, line)

            if header_match:
                # Save current section
                if current_section["content"]:
                    sections.append({
                        "header": current_section["header"],
                        "text": '\n'.join(current_section["content"]).strip()
                    })

                # Start new section
                current_section = {
                    "header": header_match.group(2),
                    "content": [line]
                }
            else:
                current_section["content"].append(line)

        # Don't forget last section
        if current_section["content"]:
            sections.append({
                "header": current_section["header"],
                "text": '\n'.join(current_section["content"]).strip()
            })

        # If no headers found, split by size
        if len(sections) <= 1:
            return self._split_by_size(text, self.section_max_size)

        return sections

    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split section into paragraphs."""
        paragraphs = text.split('\n\n')
        result = []
        current = []
        current_size = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            size = len(para.split())

            if current_size + size <= self.paragraph_max_size:
                current.append(para)
                current_size += size
            else:
                if current:
                    result.append('\n\n'.join(current))
                current = [para]
                current_size = size

        if current:
            result.append('\n\n'.join(current))

        return result

    def _split_by_size(self, text: str, max_size: int) -> List[Dict]:
        """Split text by word count."""
        words = text.split()
        sections = []

        for i in range(0, len(words), max_size):
            section_words = words[i:i + max_size]
            sections.append({
                "header": f"Section {i // max_size + 1}",
                "text": " ".join(section_words)
            })

        return sections

# Usage
chunker = HierarchicalChunker(
    section_max_size=2000,
    paragraph_max_size=500
)

chunks = chunker.chunk(long_document, doc_id="doc_001")

# Print hierarchy
for chunk in chunks:
    indent = "  " * (0 if chunk.level == "document" else 1 if chunk.level == "section" else 2)
    print(f"{indent}{chunk.level}: {chunk.chunk_id}")
    if chunk.level == "paragraph":
        print(f"{indent}  Text: {chunk.text[:50]}...")
```

### Hierarchical Retrieval

```python
class HierarchicalRetriever:
    """
    Two-pass retrieval: sections first, then paragraphs.
    """

    def __init__(self, vector_store, embedding_func):
        self.vector_store = vector_store
        self.embedding_func = embedding_func

    def retrieve(
        self,
        query: str,
        top_k_sections: int = 3,
        top_k_paragraphs: int = 5
    ) -> List[Dict]:
        """Two-pass hierarchical retrieval."""
        query_embedding = self.embedding_func(query)

        # Pass 1: Retrieve relevant sections
        sections = self.vector_store.search(
            embedding=query_embedding,
            filter={"level": "section"},
            top_k=top_k_sections
        )

        # Get section IDs
        section_ids = [s["chunk_id"] for s in sections]

        # Pass 2: Retrieve paragraphs from relevant sections
        paragraphs = self.vector_store.search(
            embedding=query_embedding,
            filter={
                "level": "paragraph",
                "parent_id": {"$in": section_ids}
            },
            top_k=top_k_paragraphs
        )

        return paragraphs

# Usage
retriever = HierarchicalRetriever(vector_store, embedding_func)
results = retriever.retrieve(
    query="What is the refund policy?",
    top_k_sections=3,
    top_k_paragraphs=5
)
```

---

## 9. Production Chunking Service

### Complete Service Implementation

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import logging
from abc import ABC, abstractmethod

class ChunkingStrategy(Enum):
    FIXED = "fixed"
    RECURSIVE = "recursive"
    SEMANTIC = "semantic"
    MARKDOWN = "markdown"
    HTML = "html"
    CODE = "code"
    LATE = "late"
    AGENTIC = "agentic"
    AUTO = "auto"

@dataclass
class ChunkingConfig:
    """Configuration for chunking."""
    strategy: ChunkingStrategy = ChunkingStrategy.AUTO
    chunk_size: int = 512
    overlap: int = 50
    min_chunk_size: int = 100
    max_chunk_size: int = 2000

    # Semantic chunking
    similarity_threshold: float = 0.75

    # Code chunking
    language: str = "python"

    # Agentic chunking
    llm_model: str = "gpt-4o-mini"

class ChunkingService:
    """
    Production-ready chunking service with multiple strategies.
    """

    def __init__(
        self,
        config: Optional[ChunkingConfig] = None,
        embedding_func: Optional[Callable] = None,
        llm_client: Optional[Any] = None
    ):
        self.config = config or ChunkingConfig()
        self.embedding_func = embedding_func
        self.llm_client = llm_client
        self.logger = logging.getLogger(__name__)

        # Initialize chunkers
        self._chunkers = {}

    def chunk(
        self,
        text: str,
        strategy: Optional[ChunkingStrategy] = None,
        metadata: Optional[Dict] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Chunk text using specified or auto-detected strategy.

        Args:
            text: Text to chunk
            strategy: Chunking strategy (optional, auto-detected if not provided)
            metadata: Metadata to attach to all chunks
            **kwargs: Additional strategy-specific parameters

        Returns:
            List of chunk dictionaries
        """
        strategy = strategy or self.config.strategy

        # Auto-detect strategy if needed
        if strategy == ChunkingStrategy.AUTO:
            strategy = self._detect_strategy(text)
            self.logger.info(f"Auto-detected strategy: {strategy.value}")

        try:
            chunker = self._get_chunker(strategy)
            chunks = chunker.chunk(text, **kwargs)

            # Post-process chunks
            chunks = self._post_process(chunks, metadata)

            self.logger.info(
                f"Created {len(chunks)} chunks using {strategy.value} strategy"
            )
            return chunks

        except Exception as e:
            self.logger.error(f"Chunking failed: {e}")
            return self._fallback_chunk(text, metadata)

    def _detect_strategy(self, text: str) -> ChunkingStrategy:
        """Auto-detect the best strategy for the content."""
        # Check for code
        if self._looks_like_code(text):
            return ChunkingStrategy.CODE

        # Check for Markdown
        if self._looks_like_markdown(text):
            return ChunkingStrategy.MARKDOWN

        # Check for HTML
        if self._looks_like_html(text):
            return ChunkingStrategy.HTML

        # Default to recursive for general text
        return ChunkingStrategy.RECURSIVE

    def _looks_like_code(self, text: str) -> bool:
        """Check if text appears to be code."""
        code_indicators = [
            'def ', 'class ', 'import ', 'from ',  # Python
            'function ', 'const ', 'let ', 'var ',  # JS
            'public ', 'private ', 'static ',  # Java/C#
        ]
        return any(indicator in text for indicator in code_indicators)

    def _looks_like_markdown(self, text: str) -> bool:
        """Check if text appears to be Markdown."""
        import re
        return bool(re.search(r'^#{1,6}\s+', text, re.MULTILINE))

    def _looks_like_html(self, text: str) -> bool:
        """Check if text appears to be HTML."""
        return '<html' in text.lower() or '<!doctype' in text.lower()

    def _get_chunker(self, strategy: ChunkingStrategy):
        """Get or create chunker for strategy."""
        if strategy not in self._chunkers:
            self._chunkers[strategy] = self._create_chunker(strategy)
        return self._chunkers[strategy]

    def _create_chunker(self, strategy: ChunkingStrategy):
        """Create chunker instance."""
        if strategy == ChunkingStrategy.FIXED:
            return FixedSizeChunker(
                self.config.chunk_size,
                self.config.overlap
            )
        elif strategy == ChunkingStrategy.RECURSIVE:
            return RecursiveChunker(
                self.config.chunk_size,
                self.config.overlap
            )
        elif strategy == ChunkingStrategy.SEMANTIC:
            if not self.embedding_func:
                raise ValueError("Semantic chunking requires embedding function")
            return SemanticChunker(
                self.embedding_func,
                similarity_threshold=self.config.similarity_threshold,
                max_chunk_size=self.config.max_chunk_size,
                min_chunk_size=self.config.min_chunk_size
            )
        elif strategy == ChunkingStrategy.MARKDOWN:
            return MarkdownChunker(self.config.chunk_size)
        elif strategy == ChunkingStrategy.CODE:
            return PythonCodeChunker(self.config.chunk_size)
        elif strategy == ChunkingStrategy.AGENTIC:
            if not self.llm_client:
                raise ValueError("Agentic chunking requires LLM client")
            return AgenticChunker(
                self.llm_client,
                model=self.config.llm_model,
                max_chunk_size=self.config.chunk_size
            )
        else:
            return RecursiveChunker(
                self.config.chunk_size,
                self.config.overlap
            )

    def _post_process(
        self,
        chunks: List[Dict],
        metadata: Optional[Dict]
    ) -> List[Dict]:
        """Post-process chunks: add metadata, validate, clean."""
        processed = []

        for i, chunk in enumerate(chunks):
            # Ensure text field exists
            if "text" not in chunk:
                continue

            # Clean text
            chunk["text"] = chunk["text"].strip()

            # Skip empty chunks
            if not chunk["text"]:
                continue

            # Add index
            chunk["chunk_index"] = i

            # Add word/token count
            chunk["word_count"] = len(chunk["text"].split())

            # Merge with provided metadata
            if metadata:
                chunk["metadata"] = {
                    **metadata,
                    **chunk.get("metadata", {})
                }

            processed.append(chunk)

        return processed

    def _fallback_chunk(
        self,
        text: str,
        metadata: Optional[Dict]
    ) -> List[Dict]:
        """Simple fallback chunking when main strategy fails."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.config.chunk_size):
            chunk_words = words[i:i + self.config.chunk_size]
            chunks.append({
                "text": " ".join(chunk_words),
                "chunk_index": i // self.config.chunk_size,
                "word_count": len(chunk_words),
                "metadata": metadata or {}
            })

        return chunks

# Usage Example
from openai import OpenAI

# Initialize service
client = OpenAI()

def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

config = ChunkingConfig(
    strategy=ChunkingStrategy.AUTO,
    chunk_size=512,
    overlap=50
)

service = ChunkingService(
    config=config,
    embedding_func=get_embedding,
    llm_client=client
)

# Chunk different document types
markdown_chunks = service.chunk(
    text=markdown_document,
    metadata={"source": "docs/readme.md", "type": "documentation"}
)

code_chunks = service.chunk(
    text=python_code,
    strategy=ChunkingStrategy.CODE,
    metadata={"source": "src/main.py", "type": "code"}
)

semantic_chunks = service.chunk(
    text=legal_document,
    strategy=ChunkingStrategy.SEMANTIC,
    metadata={"source": "contracts/agreement.pdf", "type": "legal"}
)
```

---

## 10. Comparison Examples

### Strategy Comparison Script

```python
from typing import List, Dict
import time

def compare_strategies(
    text: str,
    strategies: List[ChunkingStrategy],
    service: ChunkingService
) -> Dict:
    """Compare multiple chunking strategies on the same text."""
    results = {}

    for strategy in strategies:
        start_time = time.time()

        chunks = service.chunk(text, strategy=strategy)

        elapsed = time.time() - start_time

        # Calculate statistics
        chunk_sizes = [c["word_count"] for c in chunks]

        results[strategy.value] = {
            "num_chunks": len(chunks),
            "avg_chunk_size": sum(chunk_sizes) / len(chunk_sizes) if chunks else 0,
            "min_chunk_size": min(chunk_sizes) if chunks else 0,
            "max_chunk_size": max(chunk_sizes) if chunks else 0,
            "std_chunk_size": np.std(chunk_sizes) if chunks else 0,
            "processing_time": elapsed,
            "chunks": chunks  # For detailed analysis
        }

    return results

# Usage
strategies = [
    ChunkingStrategy.FIXED,
    ChunkingStrategy.RECURSIVE,
    ChunkingStrategy.SEMANTIC
]

results = compare_strategies(document_text, strategies, service)

# Print comparison
print("\n=== Strategy Comparison ===\n")
for strategy, stats in results.items():
    print(f"{strategy}:")
    print(f"  Chunks: {stats['num_chunks']}")
    print(f"  Avg size: {stats['avg_chunk_size']:.1f} words")
    print(f"  Size range: {stats['min_chunk_size']}-{stats['max_chunk_size']}")
    print(f"  Std dev: {stats['std_chunk_size']:.1f}")
    print(f"  Time: {stats['processing_time']:.3f}s")
    print()
```

### Retrieval Quality Comparison

```python
from typing import List, Tuple
import numpy as np

def evaluate_retrieval(
    chunks: List[Dict],
    queries: List[str],
    ground_truth: List[List[int]],  # Relevant chunk indices per query
    embedding_func,
    top_k: int = 5
) -> Dict:
    """Evaluate retrieval quality for chunks."""
    # Embed all chunks
    chunk_embeddings = [embedding_func(c["text"]) for c in chunks]

    precision_scores = []
    recall_scores = []
    mrr_scores = []

    for query, relevant_indices in zip(queries, ground_truth):
        query_embedding = embedding_func(query)

        # Calculate similarities
        similarities = [
            np.dot(query_embedding, ce) /
            (np.linalg.norm(query_embedding) * np.linalg.norm(ce))
            for ce in chunk_embeddings
        ]

        # Get top-k
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # Calculate metrics
        relevant_in_top_k = len(set(top_indices) & set(relevant_indices))

        precision = relevant_in_top_k / top_k
        recall = relevant_in_top_k / len(relevant_indices) if relevant_indices else 0

        # MRR
        mrr = 0
        for i, idx in enumerate(top_indices):
            if idx in relevant_indices:
                mrr = 1 / (i + 1)
                break

        precision_scores.append(precision)
        recall_scores.append(recall)
        mrr_scores.append(mrr)

    return {
        "precision@k": np.mean(precision_scores),
        "recall@k": np.mean(recall_scores),
        "mrr": np.mean(mrr_scores)
    }

# Usage
test_queries = [
    "What is the refund policy?",
    "How do I contact support?",
    "What are the shipping options?"
]

ground_truth = [
    [5, 6],     # Relevant chunks for query 1
    [12],       # Relevant chunks for query 2
    [8, 9, 10]  # Relevant chunks for query 3
]

for strategy, result in results.items():
    metrics = evaluate_retrieval(
        result["chunks"],
        test_queries,
        ground_truth,
        get_embedding,
        top_k=5
    )
    print(f"\n{strategy} Retrieval Metrics:")
    print(f"  Precision@5: {metrics['precision@k']:.3f}")
    print(f"  Recall@5: {metrics['recall@k']:.3f}")
    print(f"  MRR: {metrics['mrr']:.3f}")
```

---

## 11. Optimization Examples

### Chunk Size Optimization

```python
def optimize_chunk_size(
    text: str,
    test_queries: List[str],
    ground_truth: List[List[int]],
    embedding_func,
    size_range: Tuple[int, int] = (128, 1024),
    step: int = 128
) -> Dict:
    """Find optimal chunk size for given content and queries."""
    results = {}

    for chunk_size in range(size_range[0], size_range[1] + 1, step):
        chunker = RecursiveChunker(
            chunk_size=chunk_size,
            overlap=int(chunk_size * 0.15)  # 15% overlap
        )

        chunks = chunker.chunk(text)

        # Re-index ground truth for new chunking
        # (In practice, you'd need to re-label)

        metrics = evaluate_retrieval(
            chunks, test_queries, ground_truth, embedding_func
        )

        results[chunk_size] = {
            "num_chunks": len(chunks),
            **metrics
        }

    # Find best size
    best_size = max(results, key=lambda x: results[x]["precision@k"])

    return {
        "results": results,
        "optimal_size": best_size,
        "optimal_metrics": results[best_size]
    }
```

### Overlap Optimization

```python
def optimize_overlap(
    text: str,
    chunk_size: int,
    overlap_percentages: List[int] = [0, 10, 15, 20, 25, 30],
    embedding_func=None
) -> Dict:
    """Find optimal overlap percentage."""
    results = {}

    for pct in overlap_percentages:
        overlap = int(chunk_size * pct / 100)

        chunker = RecursiveChunker(chunk_size=chunk_size, overlap=overlap)
        chunks = chunker.chunk(text)

        # Calculate chunk uniqueness (less redundancy is better)
        chunk_texts = [c["text"] for c in chunks]
        total_words = sum(len(t.split()) for t in chunk_texts)
        unique_words = len(set(" ".join(chunk_texts).split()))
        redundancy = 1 - (unique_words / total_words)

        results[pct] = {
            "overlap_tokens": overlap,
            "num_chunks": len(chunks),
            "redundancy": redundancy,
            "total_tokens": total_words
        }

    return results
```

### Batch Processing Optimization

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class BatchChunkingService:
    """Optimized service for batch document processing."""

    def __init__(
        self,
        service: ChunkingService,
        max_workers: int = 4
    ):
        self.service = service
        self.max_workers = max_workers

    def chunk_batch(
        self,
        documents: List[Dict[str, str]],
        strategy: ChunkingStrategy = ChunkingStrategy.AUTO
    ) -> List[List[Dict]]:
        """Process multiple documents in parallel."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(
                    self.service.chunk,
                    doc["text"],
                    strategy=strategy,
                    metadata={"source": doc.get("source", "")}
                )
                for doc in documents
            ]

            results = [f.result() for f in futures]

        return results

    async def chunk_batch_async(
        self,
        documents: List[Dict[str, str]],
        strategy: ChunkingStrategy = ChunkingStrategy.AUTO
    ) -> List[List[Dict]]:
        """Async batch processing."""
        loop = asyncio.get_event_loop()

        tasks = [
            loop.run_in_executor(
                None,
                self.service.chunk,
                doc["text"],
                strategy
            )
            for doc in documents
        ]

        return await asyncio.gather(*tasks)

# Usage
batch_service = BatchChunkingService(service, max_workers=4)

documents = [
    {"text": doc1, "source": "doc1.pdf"},
    {"text": doc2, "source": "doc2.pdf"},
    {"text": doc3, "source": "doc3.pdf"},
]

# Sync batch processing
all_chunks = batch_service.chunk_batch(documents)

# Async batch processing
all_chunks = await batch_service.chunk_batch_async(documents)
```
