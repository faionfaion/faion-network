# Chunking Templates

Ready-to-use templates for different document types and configurations.

---

## Table of Contents

1. [Configuration Templates](#1-configuration-templates)
2. [Document Type Templates](#2-document-type-templates)
3. [Pipeline Templates](#3-pipeline-templates)
4. [Testing Templates](#4-testing-templates)
5. [Evaluation Templates](#5-evaluation-templates)
6. [Integration Templates](#6-integration-templates)

---

## 1. Configuration Templates

### Basic Configuration (YAML)

```yaml
# chunking_config.yaml
chunking:
  # Strategy selection
  strategy: recursive  # fixed, recursive, semantic, code, agentic, auto

  # Size parameters
  chunk_size: 512         # Target chunk size in tokens
  chunk_overlap: 50       # Overlap between chunks
  min_chunk_size: 100     # Minimum chunk size
  max_chunk_size: 2000    # Maximum chunk size

  # Token counting
  encoding: cl100k_base   # OpenAI tokenizer encoding

  # Separator hierarchy (for recursive)
  separators:
    - "\n\n"  # Paragraphs
    - "\n"    # Lines
    - ". "    # Sentences
    - " "     # Words

  # Semantic chunking
  semantic:
    similarity_threshold: 0.75
    buffer_size: 1
    breakpoint_method: threshold  # threshold, percentile, gradient
    percentile: 25

  # Code chunking
  code:
    language: python
    include_imports: true
    include_docstrings: true

  # Agentic chunking
  agentic:
    model: gpt-4o-mini
    enrich_metadata: true
    max_retries: 3

  # Metadata
  metadata:
    include_position: true
    include_word_count: true
    include_token_count: true
    custom_fields: []
```

### Environment-Specific Configurations

```yaml
# config/chunking/development.yaml
chunking:
  strategy: recursive
  chunk_size: 512
  chunk_overlap: 50
  logging:
    level: DEBUG
    log_chunks: true

---
# config/chunking/staging.yaml
chunking:
  strategy: semantic
  chunk_size: 512
  chunk_overlap: 50
  semantic:
    similarity_threshold: 0.75
  logging:
    level: INFO
    log_chunks: false

---
# config/chunking/production.yaml
chunking:
  strategy: auto
  chunk_size: 512
  chunk_overlap: 50
  fallback_strategy: recursive
  error_handling:
    retry_count: 3
    fallback_on_error: true
  logging:
    level: WARNING
    log_chunks: false
  monitoring:
    track_latency: true
    track_chunk_distribution: true
```

### Python Configuration Class

```python
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import yaml

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
class SemanticConfig:
    similarity_threshold: float = 0.75
    buffer_size: int = 1
    breakpoint_method: str = "threshold"
    percentile: int = 25

@dataclass
class CodeConfig:
    language: str = "python"
    include_imports: bool = True
    include_docstrings: bool = True

@dataclass
class AgenticConfig:
    model: str = "gpt-4o-mini"
    enrich_metadata: bool = True
    max_retries: int = 3

@dataclass
class ChunkingConfig:
    strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE
    chunk_size: int = 512
    chunk_overlap: int = 50
    min_chunk_size: int = 100
    max_chunk_size: int = 2000
    encoding: str = "cl100k_base"
    separators: List[str] = field(default_factory=lambda: ["\n\n", "\n", ". ", " "])
    semantic: SemanticConfig = field(default_factory=SemanticConfig)
    code: CodeConfig = field(default_factory=CodeConfig)
    agentic: AgenticConfig = field(default_factory=AgenticConfig)

    @classmethod
    def from_yaml(cls, path: str) -> "ChunkingConfig":
        """Load configuration from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)

        config_data = data.get("chunking", data)

        # Parse strategy
        strategy = ChunkingStrategy(config_data.get("strategy", "recursive"))

        # Parse nested configs
        semantic = SemanticConfig(**config_data.get("semantic", {}))
        code = CodeConfig(**config_data.get("code", {}))
        agentic = AgenticConfig(**config_data.get("agentic", {}))

        return cls(
            strategy=strategy,
            chunk_size=config_data.get("chunk_size", 512),
            chunk_overlap=config_data.get("chunk_overlap", 50),
            min_chunk_size=config_data.get("min_chunk_size", 100),
            max_chunk_size=config_data.get("max_chunk_size", 2000),
            encoding=config_data.get("encoding", "cl100k_base"),
            separators=config_data.get("separators", ["\n\n", "\n", ". ", " "]),
            semantic=semantic,
            code=code,
            agentic=agentic
        )

    def to_yaml(self, path: str):
        """Save configuration to YAML file."""
        data = {
            "chunking": {
                "strategy": self.strategy.value,
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap,
                "min_chunk_size": self.min_chunk_size,
                "max_chunk_size": self.max_chunk_size,
                "encoding": self.encoding,
                "separators": self.separators,
                "semantic": {
                    "similarity_threshold": self.semantic.similarity_threshold,
                    "buffer_size": self.semantic.buffer_size,
                    "breakpoint_method": self.semantic.breakpoint_method,
                    "percentile": self.semantic.percentile,
                },
                "code": {
                    "language": self.code.language,
                    "include_imports": self.code.include_imports,
                    "include_docstrings": self.code.include_docstrings,
                },
                "agentic": {
                    "model": self.agentic.model,
                    "enrich_metadata": self.agentic.enrich_metadata,
                    "max_retries": self.agentic.max_retries,
                },
            }
        }

        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

# Usage
config = ChunkingConfig.from_yaml("config/chunking/production.yaml")
```

---

## 2. Document Type Templates

### Technical Documentation Template

```python
def create_documentation_chunker() -> ChunkingConfig:
    """Configuration for technical documentation (Markdown/RST)."""
    return ChunkingConfig(
        strategy=ChunkingStrategy.MARKDOWN,
        chunk_size=512,
        chunk_overlap=50,
        min_chunk_size=100,
        separators=[
            "\n## ",   # H2 headers
            "\n### ",  # H3 headers
            "\n\n",    # Paragraphs
            "\n",      # Lines
            ". ",      # Sentences
        ]
    )

# Chunking function
def chunk_documentation(text: str, source: str) -> List[Dict]:
    """Chunk technical documentation."""
    config = create_documentation_chunker()
    chunker = MarkdownChunker(
        max_chunk_size=config.chunk_size,
        include_header_in_chunk=True
    )

    chunks = chunker.chunk(text)

    # Add metadata
    for i, chunk in enumerate(chunks):
        chunk["metadata"] = {
            "source": source,
            "type": "documentation",
            "chunk_index": i,
            "header_path": chunk.get("header_path", ""),
        }

    return chunks
```

### Legal Document Template

```python
def create_legal_chunker() -> ChunkingConfig:
    """Configuration for legal documents (contracts, agreements)."""
    return ChunkingConfig(
        strategy=ChunkingStrategy.SEMANTIC,
        chunk_size=1024,        # Larger chunks for legal context
        chunk_overlap=100,      # More overlap for continuity
        min_chunk_size=200,
        max_chunk_size=2000,
        semantic=SemanticConfig(
            similarity_threshold=0.8,  # Higher threshold for precise splits
            buffer_size=2,             # More context
        )
    )

def chunk_legal_document(
    text: str,
    source: str,
    embedding_func
) -> List[Dict]:
    """Chunk legal documents with semantic awareness."""
    config = create_legal_chunker()

    chunker = SemanticChunker(
        embedding_func=embedding_func,
        similarity_threshold=config.semantic.similarity_threshold,
        max_chunk_size=config.max_chunk_size,
        min_chunk_size=config.min_chunk_size,
        buffer_size=config.semantic.buffer_size
    )

    chunks = chunker.chunk(text)

    # Enrich with legal-specific metadata
    for i, chunk in enumerate(chunks):
        chunk["metadata"] = {
            "source": source,
            "type": "legal",
            "chunk_index": i,
            "requires_context": True,  # Flag for retrieval
        }

    return chunks
```

### Code Repository Template

```python
def create_code_chunker(language: str = "python") -> ChunkingConfig:
    """Configuration for code files."""
    return ChunkingConfig(
        strategy=ChunkingStrategy.CODE,
        chunk_size=800,
        chunk_overlap=0,  # No overlap for code
        code=CodeConfig(
            language=language,
            include_imports=True,
            include_docstrings=True
        )
    )

def chunk_code_file(
    code: str,
    file_path: str,
    language: str = "python"
) -> List[Dict]:
    """Chunk code by functions and classes."""
    config = create_code_chunker(language)

    if language == "python":
        chunker = PythonCodeChunker(
            max_chunk_size=config.chunk_size,
            include_imports=config.code.include_imports,
            include_docstrings=config.code.include_docstrings
        )
    elif language in ["javascript", "typescript"]:
        chunker = JavaScriptChunker(max_chunk_size=config.chunk_size)
    else:
        # Fallback to generic
        chunker = RecursiveChunker(
            chunk_size=config.chunk_size,
            overlap=0
        )

    chunks = chunker.chunk(code)

    # Add code-specific metadata
    for i, chunk in enumerate(chunks):
        chunk["metadata"] = {
            "source": file_path,
            "type": "code",
            "language": language,
            "chunk_type": chunk.get("type", "unknown"),
            "function_name": chunk.get("name", ""),
            "start_line": chunk.get("start_line", 0),
            "end_line": chunk.get("end_line", 0),
        }

    return chunks
```

### Research Paper Template

```python
def create_research_paper_chunker() -> ChunkingConfig:
    """Configuration for research papers (PDF)."""
    return ChunkingConfig(
        strategy=ChunkingStrategy.RECURSIVE,
        chunk_size=512,
        chunk_overlap=50,
        separators=[
            "\n\n\n",  # Section breaks
            "\n\n",    # Paragraphs
            "\n",      # Lines
            ". ",      # Sentences
        ]
    )

def chunk_research_paper(
    text: str,
    source: str,
    sections: Optional[List[str]] = None
) -> List[Dict]:
    """
    Chunk research paper with section awareness.

    Args:
        text: Paper text
        source: Source file path
        sections: Optional list of section names found in paper
    """
    # Common section names in research papers
    default_sections = [
        "Abstract", "Introduction", "Related Work", "Background",
        "Methodology", "Methods", "Experiments", "Results",
        "Discussion", "Conclusion", "References"
    ]
    sections = sections or default_sections

    config = create_research_paper_chunker()
    chunker = RecursiveChunker(
        chunk_size=config.chunk_size,
        overlap=config.chunk_overlap,
        separators=config.separators
    )

    chunks = chunker.chunk(text)

    # Detect section for each chunk
    for i, chunk in enumerate(chunks):
        detected_section = "Unknown"
        for section in sections:
            if section.lower() in chunk["text"].lower()[:200]:
                detected_section = section
                break

        chunk["metadata"] = {
            "source": source,
            "type": "research_paper",
            "section": detected_section,
            "chunk_index": i,
        }

    return chunks
```

### FAQ/Knowledge Base Template

```python
def create_faq_chunker() -> ChunkingConfig:
    """Configuration for FAQ/KB articles."""
    return ChunkingConfig(
        strategy=ChunkingStrategy.FIXED,
        chunk_size=256,      # Smaller chunks for specific answers
        chunk_overlap=0,     # No overlap needed
        min_chunk_size=50,
    )

def chunk_faq(
    questions: List[Dict[str, str]],
    source: str
) -> List[Dict]:
    """
    Chunk FAQ entries.
    Each Q&A pair becomes one chunk.

    Args:
        questions: List of {"question": str, "answer": str}
        source: Source identifier
    """
    chunks = []

    for i, qa in enumerate(questions):
        question = qa["question"]
        answer = qa["answer"]

        # Combine Q&A for retrieval
        chunk_text = f"Question: {question}\n\nAnswer: {answer}"

        chunks.append({
            "text": chunk_text,
            "question": question,
            "answer": answer,
            "metadata": {
                "source": source,
                "type": "faq",
                "chunk_index": i,
            }
        })

    return chunks
```

### Conversation/Chat Log Template

```python
def create_conversation_chunker() -> ChunkingConfig:
    """Configuration for conversation/chat logs."""
    return ChunkingConfig(
        strategy=ChunkingStrategy.RECURSIVE,
        chunk_size=512,
        chunk_overlap=100,  # Higher overlap for conversation context
        separators=[
            "\n\n",           # Message blocks
            "\nUser: ",       # User turns
            "\nAssistant: ",  # Assistant turns
            "\n",             # Lines
        ]
    )

def chunk_conversation(
    messages: List[Dict[str, str]],
    conversation_id: str,
    window_size: int = 5
) -> List[Dict]:
    """
    Chunk conversation with sliding window.

    Args:
        messages: List of {"role": str, "content": str}
        conversation_id: Unique conversation ID
        window_size: Number of messages per chunk
    """
    chunks = []

    for i in range(0, len(messages), window_size - 2):  # 2 message overlap
        window = messages[i:i + window_size]

        # Format messages
        chunk_text = "\n\n".join([
            f"{m['role'].title()}: {m['content']}"
            for m in window
        ])

        chunks.append({
            "text": chunk_text,
            "message_start": i,
            "message_end": i + len(window),
            "metadata": {
                "conversation_id": conversation_id,
                "type": "conversation",
                "chunk_index": len(chunks),
                "num_messages": len(window),
            }
        })

    return chunks
```

---

## 3. Pipeline Templates

### Basic Ingestion Pipeline

```python
from dataclasses import dataclass
from typing import List, Dict, Callable
from pathlib import Path

@dataclass
class Document:
    content: str
    source: str
    doc_type: str
    metadata: Dict = None

class ChunkingPipeline:
    """Complete document ingestion pipeline."""

    def __init__(
        self,
        chunking_service: ChunkingService,
        embedding_func: Callable,
        vector_store
    ):
        self.chunking_service = chunking_service
        self.embedding_func = embedding_func
        self.vector_store = vector_store

    def process_document(self, document: Document) -> List[Dict]:
        """Process a single document through the pipeline."""
        # Step 1: Preprocess
        cleaned_text = self._preprocess(document.content)

        # Step 2: Detect strategy or use provided type
        strategy = self._get_strategy(document.doc_type)

        # Step 3: Chunk
        chunks = self.chunking_service.chunk(
            text=cleaned_text,
            strategy=strategy,
            metadata={
                "source": document.source,
                "doc_type": document.doc_type,
                **(document.metadata or {})
            }
        )

        # Step 4: Embed
        for chunk in chunks:
            chunk["embedding"] = self.embedding_func(chunk["text"])

        # Step 5: Store
        self.vector_store.upsert(chunks)

        return chunks

    def process_batch(self, documents: List[Document]) -> List[List[Dict]]:
        """Process multiple documents."""
        return [self.process_document(doc) for doc in documents]

    def _preprocess(self, text: str) -> str:
        """Clean and preprocess text."""
        # Remove excessive whitespace
        text = " ".join(text.split())

        # Remove special characters that might cause issues
        text = text.replace("\x00", "")

        return text

    def _get_strategy(self, doc_type: str) -> ChunkingStrategy:
        """Map document type to chunking strategy."""
        strategy_map = {
            "documentation": ChunkingStrategy.MARKDOWN,
            "legal": ChunkingStrategy.SEMANTIC,
            "code": ChunkingStrategy.CODE,
            "faq": ChunkingStrategy.FIXED,
            "research": ChunkingStrategy.RECURSIVE,
            "conversation": ChunkingStrategy.RECURSIVE,
        }
        return strategy_map.get(doc_type, ChunkingStrategy.AUTO)

# Usage
pipeline = ChunkingPipeline(
    chunking_service=service,
    embedding_func=get_embedding,
    vector_store=qdrant_client
)

# Process single document
doc = Document(
    content=readme_text,
    source="docs/README.md",
    doc_type="documentation"
)
chunks = pipeline.process_document(doc)

# Process batch
documents = [
    Document(content=text1, source="doc1.pdf", doc_type="legal"),
    Document(content=text2, source="main.py", doc_type="code"),
]
all_chunks = pipeline.process_batch(documents)
```

### Chonkie Pipeline Template

```python
from chonkie import Pipeline
from chonkie.chunkers import RecursiveChunker, SemanticChunker
from chonkie.refiners import OverlapRefiner
from chonkie.embeddings import OpenAIEmbeddings
from chonkie.handshakes import QdrantHandshake

# Build pipeline
pipeline = Pipeline([
    # Stage 1: Initial chunking
    RecursiveChunker(
        chunk_size=1024,
        chunk_overlap=0,
        separators=["\n\n", "\n", ". ", " "]
    ),

    # Stage 2: Semantic refinement
    SemanticChunker(
        embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
        chunk_size=512,
        similarity_threshold=0.75
    ),

    # Stage 3: Add overlap
    OverlapRefiner(overlap_size=50),

    # Stage 4: Generate embeddings
    OpenAIEmbeddings(model="text-embedding-3-small"),

    # Stage 5: Store in Qdrant
    QdrantHandshake(
        url="http://localhost:6333",
        collection_name="documents"
    )
])

# Process documents
results = pipeline.process([document1, document2, document3])
```

### Multi-Stage Processing Pipeline

```python
class MultiStageChunkingPipeline:
    """
    Multi-stage pipeline with:
    1. Initial coarse chunking
    2. Semantic refinement
    3. Metadata enrichment
    4. Quality filtering
    """

    def __init__(
        self,
        coarse_chunker,
        semantic_chunker,
        metadata_enricher,
        quality_filter
    ):
        self.coarse_chunker = coarse_chunker
        self.semantic_chunker = semantic_chunker
        self.metadata_enricher = metadata_enricher
        self.quality_filter = quality_filter

    def process(self, text: str, metadata: Dict = None) -> List[Dict]:
        """Process text through all stages."""
        # Stage 1: Coarse chunking (fast, rule-based)
        coarse_chunks = self.coarse_chunker.chunk(text)
        print(f"Stage 1: {len(coarse_chunks)} coarse chunks")

        # Stage 2: Semantic refinement (split or merge based on similarity)
        refined_chunks = []
        for chunk in coarse_chunks:
            if len(chunk["text"].split()) > 200:
                # Further split large chunks semantically
                sub_chunks = self.semantic_chunker.chunk(chunk["text"])
                refined_chunks.extend(sub_chunks)
            else:
                refined_chunks.append(chunk)
        print(f"Stage 2: {len(refined_chunks)} refined chunks")

        # Stage 3: Metadata enrichment
        enriched_chunks = self.metadata_enricher.enrich(
            refined_chunks,
            base_metadata=metadata
        )
        print(f"Stage 3: Metadata added to {len(enriched_chunks)} chunks")

        # Stage 4: Quality filtering
        final_chunks = self.quality_filter.filter(enriched_chunks)
        print(f"Stage 4: {len(final_chunks)} chunks passed quality filter")

        return final_chunks

# Quality filter implementation
class QualityFilter:
    def __init__(
        self,
        min_words: int = 20,
        max_words: int = 2000,
        min_unique_words_ratio: float = 0.3
    ):
        self.min_words = min_words
        self.max_words = max_words
        self.min_unique_ratio = min_unique_words_ratio

    def filter(self, chunks: List[Dict]) -> List[Dict]:
        """Filter out low-quality chunks."""
        filtered = []

        for chunk in chunks:
            text = chunk.get("text", "")
            words = text.split()

            # Check word count
            if len(words) < self.min_words or len(words) > self.max_words:
                continue

            # Check uniqueness (avoid repetitive content)
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < self.min_unique_ratio:
                continue

            filtered.append(chunk)

        return filtered

# Metadata enricher implementation
class MetadataEnricher:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def enrich(
        self,
        chunks: List[Dict],
        base_metadata: Dict = None
    ) -> List[Dict]:
        """Add metadata to chunks."""
        enriched = []

        for i, chunk in enumerate(chunks):
            # Add base metadata
            chunk["metadata"] = {
                **(base_metadata or {}),
                "chunk_index": i,
                "word_count": len(chunk["text"].split()),
            }

            # Add computed metadata
            chunk["metadata"]["has_code"] = "```" in chunk["text"]
            chunk["metadata"]["has_list"] = any(
                line.strip().startswith(("- ", "* ", "1."))
                for line in chunk["text"].split("\n")
            )

            # Optional: LLM-generated summary
            if self.llm_client:
                chunk["metadata"]["summary"] = self._generate_summary(chunk["text"])

            enriched.append(chunk)

        return enriched

    def _generate_summary(self, text: str) -> str:
        """Generate summary using LLM."""
        # Implementation depends on LLM client
        pass
```

---

## 4. Testing Templates

### Unit Test Template

```python
import pytest
from typing import List, Dict

class TestChunkingStrategies:
    """Unit tests for chunking strategies."""

    @pytest.fixture
    def sample_text(self) -> str:
        return """
# Introduction

This is the first paragraph of the introduction.
It contains multiple sentences. Some are longer than others.

## Background

Here is some background information.
This section explains the context.

### Technical Details

Technical details go here with specific information.
"""

    @pytest.fixture
    def sample_code(self) -> str:
        return '''
def hello_world():
    """Say hello."""
    print("Hello, World!")

class Calculator:
    """Simple calculator class."""

    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Subtract b from a."""
        return a - b
'''

    # Fixed-size chunking tests
    def test_fixed_size_chunks_correct_size(self, sample_text):
        """Test that chunks are within size limits."""
        chunker = FixedSizeChunker(chunk_size=50, overlap=10)
        chunks = chunker.chunk(sample_text)

        for chunk in chunks:
            assert chunk["token_count"] <= 50 + 5  # Allow small variance

    def test_fixed_size_overlap_present(self, sample_text):
        """Test that overlap is present between chunks."""
        chunker = FixedSizeChunker(chunk_size=50, overlap=10)
        chunks = chunker.chunk(sample_text)

        if len(chunks) > 1:
            # Check that consecutive chunks share some content
            for i in range(1, len(chunks)):
                prev_text = chunks[i-1]["text"]
                curr_text = chunks[i]["text"]

                # Some overlap should exist
                prev_words = set(prev_text.split()[-20:])
                curr_words = set(curr_text.split()[:20])
                assert len(prev_words & curr_words) > 0

    # Recursive chunking tests
    def test_recursive_respects_separators(self, sample_text):
        """Test that recursive chunker uses separators."""
        chunker = RecursiveChunker(chunk_size=100, overlap=0)
        chunks = chunker.chunk(sample_text)

        # Chunks should not split mid-sentence (unless too long)
        for chunk in chunks:
            text = chunk["text"].strip()
            # Should end with sentence-ending punctuation or be a header
            assert (
                text.endswith(('.', '!', '?', ':')) or
                text.startswith('#') or
                len(text.split()) >= 100  # Large chunk exception
            )

    # Semantic chunking tests
    @pytest.fixture
    def mock_embedding_func(self):
        """Mock embedding function for testing."""
        import numpy as np

        def embed(text: str) -> np.ndarray:
            # Simple mock: hash-based embedding
            np.random.seed(hash(text) % 2**32)
            return np.random.randn(384)

        return embed

    def test_semantic_creates_coherent_chunks(
        self,
        sample_text,
        mock_embedding_func
    ):
        """Test that semantic chunker creates non-empty chunks."""
        chunker = SemanticChunker(
            embedding_func=mock_embedding_func,
            similarity_threshold=0.5,
            max_chunk_size=100,
            min_chunk_size=10
        )
        chunks = chunker.chunk(sample_text)

        assert len(chunks) > 0
        for chunk in chunks:
            assert len(chunk["text"].strip()) > 0

    # Code chunking tests
    def test_code_chunker_extracts_functions(self, sample_code):
        """Test that code chunker extracts functions."""
        chunker = PythonCodeChunker()
        chunks = chunker.chunk(sample_code)

        function_chunks = [c for c in chunks if c["type"] == "function"]
        class_chunks = [c for c in chunks if c["type"] == "class"]

        assert len(function_chunks) >= 1
        assert len(class_chunks) >= 1

    def test_code_chunker_preserves_structure(self, sample_code):
        """Test that code structure is preserved."""
        chunker = PythonCodeChunker()
        chunks = chunker.chunk(sample_code)

        for chunk in chunks:
            # Each chunk should be valid Python (parseable)
            try:
                import ast
                ast.parse(chunk["text"])
            except SyntaxError:
                pytest.fail(f"Chunk is not valid Python: {chunk['text'][:50]}...")

    # Markdown chunking tests
    def test_markdown_preserves_hierarchy(self, sample_text):
        """Test that markdown chunker preserves header hierarchy."""
        chunker = MarkdownChunker(max_chunk_size=100)
        chunks = chunker.chunk(sample_text)

        for chunk in chunks:
            # Each chunk should have header path
            assert "header_path" in chunk

    # Edge case tests
    def test_empty_text(self):
        """Test handling of empty text."""
        chunker = RecursiveChunker(chunk_size=100)
        chunks = chunker.chunk("")

        assert len(chunks) == 0 or chunks[0]["text"] == ""

    def test_very_long_sentence(self):
        """Test handling of text with no natural breaks."""
        long_text = "word " * 1000  # No sentence breaks
        chunker = RecursiveChunker(chunk_size=100, overlap=10)
        chunks = chunker.chunk(long_text)

        assert len(chunks) > 1
        for chunk in chunks:
            assert chunk["word_count"] <= 110  # Some tolerance

    def test_special_characters(self):
        """Test handling of special characters."""
        text_with_special = "Hello! How are you? I'm fine. What's up?"
        chunker = RecursiveChunker(chunk_size=10)
        chunks = chunker.chunk(text_with_special)

        # Should not crash and should produce chunks
        assert len(chunks) > 0

    def test_unicode_text(self):
        """Test handling of unicode text."""
        unicode_text = "Привет мир! 你好世界! مرحبا بالعالم!"
        chunker = RecursiveChunker(chunk_size=10)
        chunks = chunker.chunk(unicode_text)

        assert len(chunks) > 0
        # Unicode should be preserved
        combined = " ".join(c["text"] for c in chunks)
        assert "Привет" in combined

# Run with: pytest -v test_chunking.py
```

### Integration Test Template

```python
import pytest
from unittest.mock import Mock, patch
import numpy as np

class TestChunkingIntegration:
    """Integration tests for chunking with external services."""

    @pytest.fixture
    def mock_openai_client(self):
        """Mock OpenAI client for testing."""
        client = Mock()

        # Mock embeddings
        client.embeddings.create.return_value = Mock(
            data=[Mock(embedding=np.random.randn(1536).tolist())]
        )

        # Mock completions
        client.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content='{"chunks": []}'))]
        )

        return client

    @pytest.fixture
    def mock_vector_store(self):
        """Mock vector store for testing."""
        store = Mock()
        store.upsert.return_value = None
        store.search.return_value = []
        return store

    def test_full_pipeline_integration(
        self,
        mock_openai_client,
        mock_vector_store
    ):
        """Test complete ingestion pipeline."""
        # Setup
        def mock_embedding(text):
            return np.random.randn(1536)

        service = ChunkingService(
            config=ChunkingConfig(chunk_size=100),
            embedding_func=mock_embedding,
            llm_client=mock_openai_client
        )

        pipeline = ChunkingPipeline(
            chunking_service=service,
            embedding_func=mock_embedding,
            vector_store=mock_vector_store
        )

        # Execute
        doc = Document(
            content="This is a test document. It has multiple sentences.",
            source="test.txt",
            doc_type="documentation"
        )

        chunks = pipeline.process_document(doc)

        # Assert
        assert len(chunks) > 0
        mock_vector_store.upsert.assert_called_once()

    def test_batch_processing_integration(
        self,
        mock_openai_client,
        mock_vector_store
    ):
        """Test batch document processing."""
        def mock_embedding(text):
            return np.random.randn(1536)

        service = ChunkingService(
            config=ChunkingConfig(chunk_size=100),
            embedding_func=mock_embedding
        )

        pipeline = ChunkingPipeline(
            chunking_service=service,
            embedding_func=mock_embedding,
            vector_store=mock_vector_store
        )

        # Execute with multiple documents
        documents = [
            Document(content=f"Document {i} content.", source=f"doc{i}.txt", doc_type="documentation")
            for i in range(5)
        ]

        all_chunks = pipeline.process_batch(documents)

        # Assert
        assert len(all_chunks) == 5
        assert mock_vector_store.upsert.call_count == 5

    @pytest.mark.integration
    def test_real_openai_embedding(self):
        """Test with real OpenAI API (requires API key)."""
        from openai import OpenAI

        client = OpenAI()

        def get_embedding(text: str):
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return np.array(response.data[0].embedding)

        chunker = SemanticChunker(
            embedding_func=get_embedding,
            similarity_threshold=0.75,
            max_chunk_size=100
        )

        text = """
        Machine learning is a subset of artificial intelligence.
        It enables computers to learn from data.

        Deep learning is a subset of machine learning.
        It uses neural networks with many layers.
        """

        chunks = chunker.chunk(text)

        assert len(chunks) >= 1
        for chunk in chunks:
            assert "text" in chunk
            assert len(chunk["text"]) > 0

# Run integration tests: pytest -v -m integration test_chunking.py
```

### Benchmark Test Template

```python
import pytest
import time
from typing import List
import statistics

class TestChunkingBenchmarks:
    """Performance benchmarks for chunking strategies."""

    @pytest.fixture
    def large_text(self) -> str:
        """Generate large text for benchmarking."""
        paragraph = "This is a sample paragraph. " * 50
        return (paragraph + "\n\n") * 100  # ~500KB of text

    @pytest.fixture
    def benchmark_iterations(self) -> int:
        return 10

    def test_fixed_size_performance(self, large_text, benchmark_iterations):
        """Benchmark fixed-size chunking."""
        chunker = FixedSizeChunker(chunk_size=500, overlap=50)

        times = []
        for _ in range(benchmark_iterations):
            start = time.perf_counter()
            chunks = chunker.chunk(large_text)
            elapsed = time.perf_counter() - start
            times.append(elapsed)

        avg_time = statistics.mean(times)
        std_time = statistics.stdev(times)

        print(f"\nFixed-size chunking:")
        print(f"  Average time: {avg_time:.3f}s")
        print(f"  Std dev: {std_time:.3f}s")
        print(f"  Chunks created: {len(chunks)}")

        # Performance assertion
        assert avg_time < 1.0, f"Fixed-size chunking too slow: {avg_time:.3f}s"

    def test_recursive_performance(self, large_text, benchmark_iterations):
        """Benchmark recursive chunking."""
        chunker = RecursiveChunker(chunk_size=500, overlap=50)

        times = []
        for _ in range(benchmark_iterations):
            start = time.perf_counter()
            chunks = chunker.chunk(large_text)
            elapsed = time.perf_counter() - start
            times.append(elapsed)

        avg_time = statistics.mean(times)

        print(f"\nRecursive chunking:")
        print(f"  Average time: {avg_time:.3f}s")
        print(f"  Chunks created: {len(chunks)}")

        assert avg_time < 2.0, f"Recursive chunking too slow: {avg_time:.3f}s"

    def test_memory_usage(self, large_text):
        """Test memory efficiency of chunking."""
        import tracemalloc

        tracemalloc.start()

        chunker = RecursiveChunker(chunk_size=500, overlap=50)
        chunks = chunker.chunk(large_text)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"\nMemory usage:")
        print(f"  Current: {current / 1024 / 1024:.2f} MB")
        print(f"  Peak: {peak / 1024 / 1024:.2f} MB")
        print(f"  Input size: {len(large_text) / 1024:.2f} KB")

        # Memory should not exceed 10x input size
        assert peak < len(large_text) * 10

# Run benchmarks: pytest -v --benchmark test_chunking.py
```

---

## 5. Evaluation Templates

### Retrieval Evaluation Template

```python
from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass

@dataclass
class EvaluationResult:
    precision_at_k: float
    recall_at_k: float
    mrr: float
    ndcg: float
    avg_chunk_size: float
    chunk_count: int

class ChunkingEvaluator:
    """Evaluate chunking quality for retrieval."""

    def __init__(
        self,
        embedding_func,
        top_k: int = 5
    ):
        self.embedding_func = embedding_func
        self.top_k = top_k

    def evaluate(
        self,
        chunks: List[Dict],
        test_queries: List[str],
        ground_truth: List[List[int]]
    ) -> EvaluationResult:
        """
        Evaluate chunking quality.

        Args:
            chunks: List of chunk dictionaries
            test_queries: List of test queries
            ground_truth: List of relevant chunk indices for each query
        """
        # Embed chunks
        chunk_embeddings = [
            self.embedding_func(c["text"]) for c in chunks
        ]

        precision_scores = []
        recall_scores = []
        mrr_scores = []
        ndcg_scores = []

        for query, relevant_indices in zip(test_queries, ground_truth):
            query_embedding = self.embedding_func(query)

            # Calculate similarities
            similarities = [
                self._cosine_similarity(query_embedding, ce)
                for ce in chunk_embeddings
            ]

            # Get top-k
            top_indices = np.argsort(similarities)[-self.top_k:][::-1]

            # Calculate metrics
            precision = self._precision_at_k(top_indices, relevant_indices)
            recall = self._recall_at_k(top_indices, relevant_indices)
            mrr = self._mrr(top_indices, relevant_indices)
            ndcg = self._ndcg(top_indices, relevant_indices)

            precision_scores.append(precision)
            recall_scores.append(recall)
            mrr_scores.append(mrr)
            ndcg_scores.append(ndcg)

        # Calculate chunk statistics
        chunk_sizes = [len(c["text"].split()) for c in chunks]

        return EvaluationResult(
            precision_at_k=np.mean(precision_scores),
            recall_at_k=np.mean(recall_scores),
            mrr=np.mean(mrr_scores),
            ndcg=np.mean(ndcg_scores),
            avg_chunk_size=np.mean(chunk_sizes),
            chunk_count=len(chunks)
        )

    def _cosine_similarity(self, a, b) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def _precision_at_k(
        self,
        retrieved: List[int],
        relevant: List[int]
    ) -> float:
        relevant_in_top_k = len(set(retrieved) & set(relevant))
        return relevant_in_top_k / len(retrieved)

    def _recall_at_k(
        self,
        retrieved: List[int],
        relevant: List[int]
    ) -> float:
        if not relevant:
            return 0.0
        relevant_in_top_k = len(set(retrieved) & set(relevant))
        return relevant_in_top_k / len(relevant)

    def _mrr(
        self,
        retrieved: List[int],
        relevant: List[int]
    ) -> float:
        for i, idx in enumerate(retrieved):
            if idx in relevant:
                return 1 / (i + 1)
        return 0.0

    def _ndcg(
        self,
        retrieved: List[int],
        relevant: List[int]
    ) -> float:
        # Calculate DCG
        dcg = 0.0
        for i, idx in enumerate(retrieved):
            if idx in relevant:
                dcg += 1 / np.log2(i + 2)

        # Calculate ideal DCG
        idcg = sum(1 / np.log2(i + 2) for i in range(min(len(relevant), len(retrieved))))

        if idcg == 0:
            return 0.0
        return dcg / idcg

# Usage
evaluator = ChunkingEvaluator(
    embedding_func=get_embedding,
    top_k=5
)

# Test dataset
test_queries = [
    "What is the refund policy?",
    "How do I contact support?",
]

ground_truth = [
    [5, 6, 7],    # Relevant chunks for query 1
    [12, 13],     # Relevant chunks for query 2
]

result = evaluator.evaluate(chunks, test_queries, ground_truth)

print(f"Precision@5: {result.precision_at_k:.3f}")
print(f"Recall@5: {result.recall_at_k:.3f}")
print(f"MRR: {result.mrr:.3f}")
print(f"NDCG: {result.ndcg:.3f}")
```

### A/B Test Template

```python
from typing import Dict
import json
from datetime import datetime

class ChunkingABTest:
    """A/B testing framework for chunking strategies."""

    def __init__(
        self,
        strategy_a: ChunkingService,
        strategy_b: ChunkingService,
        evaluator: ChunkingEvaluator
    ):
        self.strategy_a = strategy_a
        self.strategy_b = strategy_b
        self.evaluator = evaluator

    def run_test(
        self,
        documents: List[str],
        test_queries: List[str],
        ground_truth: List[List[int]],
        test_name: str = "chunking_ab_test"
    ) -> Dict:
        """Run A/B test comparing two strategies."""
        results = {
            "test_name": test_name,
            "timestamp": datetime.now().isoformat(),
            "num_documents": len(documents),
            "num_queries": len(test_queries),
        }

        # Process with Strategy A
        chunks_a = []
        for doc in documents:
            chunks_a.extend(self.strategy_a.chunk(doc))

        eval_a = self.evaluator.evaluate(chunks_a, test_queries, ground_truth)
        results["strategy_a"] = {
            "precision": eval_a.precision_at_k,
            "recall": eval_a.recall_at_k,
            "mrr": eval_a.mrr,
            "ndcg": eval_a.ndcg,
            "chunk_count": eval_a.chunk_count,
            "avg_chunk_size": eval_a.avg_chunk_size,
        }

        # Process with Strategy B
        chunks_b = []
        for doc in documents:
            chunks_b.extend(self.strategy_b.chunk(doc))

        eval_b = self.evaluator.evaluate(chunks_b, test_queries, ground_truth)
        results["strategy_b"] = {
            "precision": eval_b.precision_at_k,
            "recall": eval_b.recall_at_k,
            "mrr": eval_b.mrr,
            "ndcg": eval_b.ndcg,
            "chunk_count": eval_b.chunk_count,
            "avg_chunk_size": eval_b.avg_chunk_size,
        }

        # Calculate improvements
        results["improvement"] = {
            "precision": (eval_b.precision_at_k - eval_a.precision_at_k) / eval_a.precision_at_k * 100 if eval_a.precision_at_k > 0 else 0,
            "recall": (eval_b.recall_at_k - eval_a.recall_at_k) / eval_a.recall_at_k * 100 if eval_a.recall_at_k > 0 else 0,
            "mrr": (eval_b.mrr - eval_a.mrr) / eval_a.mrr * 100 if eval_a.mrr > 0 else 0,
        }

        # Determine winner
        metrics = ["precision", "recall", "mrr"]
        a_wins = sum(1 for m in metrics if results["strategy_a"][m] > results["strategy_b"][m])
        b_wins = sum(1 for m in metrics if results["strategy_b"][m] > results["strategy_a"][m])

        if b_wins > a_wins:
            results["winner"] = "strategy_b"
        elif a_wins > b_wins:
            results["winner"] = "strategy_a"
        else:
            results["winner"] = "tie"

        return results

    def save_results(self, results: Dict, path: str):
        """Save test results to file."""
        with open(path, "w") as f:
            json.dump(results, f, indent=2)

# Usage
ab_test = ChunkingABTest(
    strategy_a=ChunkingService(ChunkingConfig(strategy=ChunkingStrategy.RECURSIVE)),
    strategy_b=ChunkingService(ChunkingConfig(strategy=ChunkingStrategy.SEMANTIC)),
    evaluator=evaluator
)

results = ab_test.run_test(
    documents=documents,
    test_queries=test_queries,
    ground_truth=ground_truth,
    test_name="recursive_vs_semantic"
)

print(f"Winner: {results['winner']}")
print(f"Precision improvement: {results['improvement']['precision']:.1f}%")
```

---

## 6. Integration Templates

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Chunking Service API")

# Request/Response models
class ChunkRequest(BaseModel):
    text: str
    strategy: Optional[str] = "auto"
    chunk_size: Optional[int] = 512
    overlap: Optional[int] = 50
    metadata: Optional[dict] = None

class Chunk(BaseModel):
    text: str
    chunk_index: int
    word_count: int
    metadata: dict

class ChunkResponse(BaseModel):
    chunks: List[Chunk]
    strategy_used: str
    total_chunks: int

# Initialize service
chunking_service = ChunkingService(
    config=ChunkingConfig(),
    embedding_func=get_embedding
)

@app.post("/chunk", response_model=ChunkResponse)
async def chunk_text(request: ChunkRequest):
    """Chunk text using specified strategy."""
    try:
        strategy = ChunkingStrategy(request.strategy)
    except ValueError:
        strategy = ChunkingStrategy.AUTO

    chunks = chunking_service.chunk(
        text=request.text,
        strategy=strategy,
        metadata=request.metadata
    )

    return ChunkResponse(
        chunks=[Chunk(**c) for c in chunks],
        strategy_used=strategy.value,
        total_chunks=len(chunks)
    )

@app.post("/chunk/batch")
async def chunk_batch(requests: List[ChunkRequest]):
    """Chunk multiple texts."""
    results = []

    for req in requests:
        try:
            strategy = ChunkingStrategy(req.strategy)
        except ValueError:
            strategy = ChunkingStrategy.AUTO

        chunks = chunking_service.chunk(
            text=req.text,
            strategy=strategy,
            metadata=req.metadata
        )
        results.append(chunks)

    return {"results": results, "total_documents": len(results)}

# Run with: uvicorn main:app --reload
```

### LangChain Integration

```python
from langchain.text_splitter import TextSplitter
from typing import List, Any

class CustomChunker(TextSplitter):
    """LangChain-compatible wrapper for custom chunking."""

    def __init__(
        self,
        chunking_service: ChunkingService,
        strategy: ChunkingStrategy = ChunkingStrategy.AUTO,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.chunking_service = chunking_service
        self.strategy = strategy

    def split_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        chunks = self.chunking_service.chunk(
            text=text,
            strategy=self.strategy
        )
        return [c["text"] for c in chunks]

# Usage with LangChain
from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma

# Create custom splitter
splitter = CustomChunker(
    chunking_service=chunking_service,
    strategy=ChunkingStrategy.SEMANTIC
)

# Load and split documents
loader = TextLoader("document.txt")
documents = loader.load()
chunks = splitter.split_documents(documents)

# Create vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings()
)
```

### LlamaIndex Integration

```python
from llama_index.core.node_parser import NodeParser
from llama_index.core.schema import BaseNode, TextNode

class CustomNodeParser(NodeParser):
    """LlamaIndex-compatible node parser."""

    def __init__(
        self,
        chunking_service: ChunkingService,
        strategy: ChunkingStrategy = ChunkingStrategy.AUTO,
        include_metadata: bool = True
    ):
        self.chunking_service = chunking_service
        self.strategy = strategy
        self.include_metadata = include_metadata

    def _parse_nodes(
        self,
        nodes: List[BaseNode],
        show_progress: bool = False
    ) -> List[TextNode]:
        """Parse nodes into text nodes."""
        result_nodes = []

        for node in nodes:
            text = node.get_content()

            chunks = self.chunking_service.chunk(
                text=text,
                strategy=self.strategy,
                metadata={"source_node_id": node.node_id}
            )

            for chunk in chunks:
                text_node = TextNode(
                    text=chunk["text"],
                    metadata=chunk.get("metadata", {}) if self.include_metadata else {}
                )
                result_nodes.append(text_node)

        return result_nodes

# Usage with LlamaIndex
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader("data").load_data()

# Create custom parser
parser = CustomNodeParser(
    chunking_service=chunking_service,
    strategy=ChunkingStrategy.SEMANTIC
)

# Parse into nodes
nodes = parser.get_nodes_from_documents(documents)

# Create index
index = VectorStoreIndex(nodes)
```
