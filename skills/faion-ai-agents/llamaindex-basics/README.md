---
name: faion-llamaindex-basics
user-invocable: false
description: ""
---

# LlamaIndex Basics

**Core Concepts and Setup**

---

## Quick Reference

| Component | Purpose |
|-----------|---------|
| **Data Connectors** | Load documents from files, web, databases, APIs |
| **Node Parsers** | Chunk documents into nodes with metadata |
| **Index Types** | VectorStore, Keyword, KnowledgeGraph, Tree, Summary |
| **Query Engines** | Process queries and synthesize responses |

---

## Core Concepts

### RAG Pipeline Architecture

```
Documents → Data Connectors → Node Parser → Nodes
                                              ↓
                                      Embedding Model
                                              ↓
                                          Index
                                              ↓
Query → Query Engine → Retriever → Response Synthesizer → Response
```

### LlamaIndex vs LangChain

| Aspect | LlamaIndex | LangChain |
|--------|------------|-----------|
| **Focus** | Data/retrieval | Orchestration |
| **Strength** | RAG pipelines, indexing | Chains, agents, tools |
| **When to use** | Knowledge bases, document Q&A | Complex workflows, multi-step reasoning |
| **Integration** | Works well together | Works well together |

---

## Installation

```bash
# Core package
pip install llama-index

# With specific integrations
pip install llama-index-llms-openai
pip install llama-index-embeddings-openai
pip install llama-index-vector-stores-qdrant
pip install llama-index-readers-file
```

### Environment Setup

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."

# Or use Settings
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

Settings.llm = OpenAI(model="gpt-4o", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
```

---

## Data Connectors (Readers)

### SimpleDirectoryReader

```python
from llama_index.core import SimpleDirectoryReader

# Load all supported files from directory
documents = SimpleDirectoryReader(
    input_dir="./data",
    recursive=True,
    required_exts=[".pdf", ".docx", ".md", ".txt"],
    exclude_hidden=True,
).load_data()

# Load specific files
documents = SimpleDirectoryReader(
    input_files=["./doc1.pdf", "./doc2.txt"]
).load_data()

print(f"Loaded {len(documents)} documents")
```

**Supported Formats:**
- PDF, DOCX, PPTX, XLSX
- TXT, MD, HTML, JSON, CSV
- Images (with vision models)
- Audio (with whisper)

### Specialized Readers

```python
# PDF with page-level metadata
from llama_index.readers.file import PDFReader
reader = PDFReader()
documents = reader.load_data(file="./report.pdf")

# Web pages
from llama_index.readers.web import SimpleWebPageReader
documents = SimpleWebPageReader().load_data(
    urls=["https://example.com/page1", "https://example.com/page2"]
)

# Beautiful Soup for complex HTML
from llama_index.readers.web import BeautifulSoupWebReader
documents = BeautifulSoupWebReader().load_data(
    urls=["https://example.com"],
    custom_hostname="example.com"
)

# Notion
from llama_index.readers.notion import NotionPageReader
reader = NotionPageReader(integration_token="secret_...")
documents = reader.load_data(page_ids=["page_id_1", "page_id_2"])

# Database
from llama_index.readers.database import DatabaseReader
reader = DatabaseReader(
    sql_database=sql_database,  # SQLAlchemy connection
    engine=engine,
)
documents = reader.load_data(query="SELECT * FROM articles")

# GitHub
from llama_index.readers.github import GithubRepositoryReader
reader = GithubRepositoryReader(
    github_token="ghp_...",
    owner="owner",
    repo="repo",
)
documents = reader.load_data(branch="main")
```

### LlamaHub (1500+ Connectors)

```python
# Install from LlamaHub
from llama_index.readers.slack import SlackReader
from llama_index.readers.discord import DiscordReader
from llama_index.readers.confluence import ConfluenceReader
from llama_index.readers.google import GoogleDocsReader

# Browse: https://llamahub.ai/
```

---

## Node Parsers (Chunking)

### SentenceSplitter (Default)

```python
from llama_index.core.node_parser import SentenceSplitter

parser = SentenceSplitter(
    chunk_size=1024,      # Characters per chunk
    chunk_overlap=200,    # Overlap between chunks
    paragraph_separator="\n\n",
)

nodes = parser.get_nodes_from_documents(documents)
print(f"Created {len(nodes)} nodes")
```

### Semantic Chunking

```python
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding()
parser = SemanticSplitterNodeParser(
    buffer_size=1,              # Sentences to group
    breakpoint_percentile_threshold=95,  # Similarity threshold
    embed_model=embed_model,
)

nodes = parser.get_nodes_from_documents(documents)
```

### Hierarchical Chunking

```python
from llama_index.core.node_parser import HierarchicalNodeParser

parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128],  # Parent → child hierarchy
)

nodes = parser.get_nodes_from_documents(documents)

# Nodes have parent-child relationships
for node in nodes:
    print(f"Level: {node.metadata.get('level')}")
    print(f"Parent: {node.relationships.get('parent')}")
```

### Token-Based Splitting

```python
from llama_index.core.node_parser import TokenTextSplitter

parser = TokenTextSplitter(
    chunk_size=256,       # Tokens (not characters)
    chunk_overlap=50,
    separator=" ",
)

nodes = parser.get_nodes_from_documents(documents)
```

### Markdown/Code Splitting

```python
from llama_index.core.node_parser import MarkdownNodeParser

# Splits by headers, preserves structure
parser = MarkdownNodeParser()
nodes = parser.get_nodes_from_documents(documents)

# Code-aware splitting
from llama_index.core.node_parser import CodeSplitter

parser = CodeSplitter(
    language="python",
    chunk_lines=40,
    chunk_lines_overlap=15,
)
```

### Metadata Extraction

```python
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
    SummaryExtractor,
    KeywordExtractor,
)
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512, chunk_overlap=50),
        TitleExtractor(nodes=5),
        QuestionsAnsweredExtractor(questions=3),
        SummaryExtractor(summaries=["self"]),
        KeywordExtractor(keywords=5),
    ]
)

nodes = pipeline.run(documents=documents)

# Each node now has rich metadata
for node in nodes:
    print(node.metadata)  # title, questions, summary, keywords
```

---

## Quick Start Template

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import os

# Configuration
os.environ["OPENAI_API_KEY"] = "sk-..."
Settings.llm = OpenAI(model="gpt-4o", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)

# Query
query_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="compact",
)

response = query_engine.query("What is the main topic?")
print(response)

# With sources
for node in response.source_nodes:
    print(f"\n--- Source (score: {node.score:.2f}) ---")
    print(node.text[:200] + "...")
```

---

## Chunking Strategy Guide

| Strategy | Chunk Size | Overlap | Use Case |
|----------|------------|---------|----------|
| **Small chunks** | 256-512 | 50-100 | Precise retrieval, Q&A |
| **Medium chunks** | 512-1024 | 100-200 | General purpose |
| **Large chunks** | 1024-2048 | 200-400 | Summarization, context |
| **Semantic** | Variable | N/A | Topic-based retrieval |
| **Hierarchical** | Multi-level | N/A | Complex documents |

### Choosing Chunk Size

```python
# Rule of thumb
# chunk_size = context_window / top_k / 2

# Example: GPT-4 (128k), top_k=5
# chunk_size = 128000 / 5 / 2 = 12800 tokens ~ 8000-10000 chars

# For typical RAG with GPT-4o:
# chunk_size = 512-1024 tokens (good balance)
# overlap = 10-20% of chunk_size
```

---

## Related

- [llamaindex-indexes.md](llamaindex-indexes.md) - Index types and storage
- [llamaindex-retrieval.md](llamaindex-retrieval.md) - Query engines, retrievers, evaluation
- [llamaindex.md](llamaindex.md) - Original comprehensive reference

---

*LlamaIndex Basics - Part 1 of 3*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement llamaindex-basics pattern | haiku | Straightforward implementation |
| Review llamaindex-basics implementation | sonnet | Requires code analysis |
| Optimize llamaindex-basics design | opus | Complex trade-offs |

