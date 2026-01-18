# M-RAG-001: Document Ingestion

## Overview

Document ingestion is the first step in building RAG systems. It covers loading documents from various sources, parsing content, chunking strategies, and metadata extraction. Quality ingestion directly impacts retrieval accuracy.

**When to use:** Building any RAG system, knowledge base, or document Q&A application.

## Core Concepts

### 1. Ingestion Pipeline

```
Source → Loader → Parser → Chunker → Enricher → Store
  ↓         ↓        ↓         ↓          ↓         ↓
Files    Read     Extract   Split    Add meta   Vector DB
URLs     Bytes    Text      Chunks   Tags        + Text
APIs                                 Summary
```

### 2. Document Sources

| Source Type | Examples | Loader |
|-------------|----------|--------|
| **Files** | PDF, DOCX, TXT, MD | File loaders |
| **Web** | HTML pages, sitemaps | Web scrapers |
| **APIs** | Notion, Confluence, Slack | API connectors |
| **Databases** | SQL, MongoDB | DB connectors |
| **Cloud Storage** | S3, GCS, Azure Blob | Cloud loaders |

### 3. Document Types

| Type | Challenges | Strategy |
|------|------------|----------|
| **Plain text** | Simple | Direct chunk |
| **PDF** | Layout, tables, images | OCR + structure parsing |
| **HTML** | Noise, navigation | Content extraction |
| **Markdown** | Headers, code blocks | Structure-aware splitting |
| **Code** | Syntax, dependencies | AST-based parsing |
| **Tables** | Rows vs columns | Cell-level or row-level |

## Best Practices

### 1. Choose Appropriate Chunk Size

```python
# Guidelines for chunk sizes
chunk_sizes = {
    "qa_retrieval": {
        "size": 512,
        "overlap": 50,
        "reason": "Small for precise retrieval"
    },
    "summarization": {
        "size": 2048,
        "overlap": 200,
        "reason": "Larger for context"
    },
    "code": {
        "size": 1024,
        "overlap": 100,
        "reason": "Function-level"
    },
    "conversational": {
        "size": 256,
        "overlap": 25,
        "reason": "Quick retrieval"
    }
}
```

### 2. Preserve Document Structure

```python
def structure_aware_chunk(document: str, doc_type: str = "markdown"):
    """Chunk while respecting document structure."""

    if doc_type == "markdown":
        # Split on headers
        sections = re.split(r'\n(#{1,6}\s+[^\n]+)\n', document)

        chunks = []
        current_headers = []

        for section in sections:
            if section.startswith('#'):
                level = len(re.match(r'^#+', section).group())
                current_headers = current_headers[:level-1] + [section]
            else:
                # Include header hierarchy in chunk
                header_context = '\n'.join(current_headers)
                chunk = f"{header_context}\n\n{section}"
                chunks.append(chunk)

        return chunks
```

### 3. Extract Rich Metadata

```python
def extract_metadata(document: dict, source_path: str) -> dict:
    """Extract metadata for retrieval enhancement."""

    return {
        # Source info
        "source": source_path,
        "file_type": get_file_type(source_path),
        "file_size": os.path.getsize(source_path),

        # Temporal
        "created_at": get_creation_date(source_path),
        "modified_at": get_modification_date(source_path),
        "ingested_at": datetime.now().isoformat(),

        # Content
        "title": extract_title(document),
        "author": extract_author(document),
        "language": detect_language(document["text"]),
        "word_count": len(document["text"].split()),

        # Semantic
        "topics": extract_topics(document["text"]),
        "entities": extract_entities(document["text"]),
        "summary": generate_summary(document["text"], max_words=50)
    }
```

## Common Patterns

### Pattern 1: LlamaIndex Document Ingestion

```python
from llama_index.core import SimpleDirectoryReader, Document
from llama_index.core.node_parser import SentenceSplitter

# Load documents from directory
reader = SimpleDirectoryReader(
    input_dir="./data",
    recursive=True,
    required_exts=[".pdf", ".docx", ".txt", ".md"],
    file_metadata=lambda path: {"source": path}
)

documents = reader.load_data()

# Configure chunking
splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50,
    paragraph_separator="\n\n",
    secondary_chunking_regex="[.。!?！？]",
)

# Create nodes (chunks)
nodes = splitter.get_nodes_from_documents(documents)

print(f"Created {len(nodes)} chunks from {len(documents)} documents")
```

### Pattern 2: LangChain Document Loading

```python
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    WebBaseLoader,
    NotionDBLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Multi-source loading
def load_documents(sources: list[dict]) -> list:
    """Load documents from multiple sources."""

    documents = []

    for source in sources:
        if source["type"] == "pdf":
            loader = PyPDFLoader(source["path"])
        elif source["type"] == "docx":
            loader = UnstructuredWordDocumentLoader(source["path"])
        elif source["type"] == "web":
            loader = WebBaseLoader(source["url"])
        elif source["type"] == "notion":
            loader = NotionDBLoader(
                integration_token=source["token"],
                database_id=source["database_id"]
            )

        docs = loader.load()
        documents.extend(docs)

    return documents

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = text_splitter.split_documents(documents)
```

### Pattern 3: Table and Image Handling

```python
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title

def process_complex_pdf(pdf_path: str):
    """Handle PDFs with tables and images."""

    # Extract all elements including tables and images
    elements = partition_pdf(
        filename=pdf_path,
        strategy="hi_res",  # OCR for images
        extract_images_in_pdf=True,
        extract_image_block_types=["Image", "Table"],
        extract_image_block_to_payload=True,
        infer_table_structure=True
    )

    chunks = []

    for element in elements:
        if element.category == "Table":
            # Convert table to markdown for better retrieval
            table_md = element.metadata.text_as_html
            chunks.append({
                "text": f"Table:\n{table_md}",
                "type": "table",
                "metadata": element.metadata
            })
        elif element.category == "Image":
            # Store image with caption
            chunks.append({
                "text": f"Image: {element.text}",
                "image_data": element.metadata.image_base64,
                "type": "image",
                "metadata": element.metadata
            })
        else:
            chunks.append({
                "text": element.text,
                "type": "text",
                "metadata": element.metadata
            })

    return chunks
```

### Pattern 4: Incremental Ingestion

```python
class IncrementalIngester:
    def __init__(self, vector_store, checksum_db):
        self.vector_store = vector_store
        self.checksum_db = checksum_db

    def ingest(self, source_path: str):
        """Only ingest new or modified documents."""

        files = list_files(source_path)

        for file_path in files:
            current_hash = compute_hash(file_path)
            stored_hash = self.checksum_db.get(file_path)

            if current_hash == stored_hash:
                # Skip unchanged files
                continue

            # Remove old chunks if file was modified
            if stored_hash:
                self.vector_store.delete(filter={"source": file_path})

            # Ingest new/modified file
            chunks = self._process_file(file_path)
            self.vector_store.add(chunks)

            # Update checksum
            self.checksum_db.set(file_path, current_hash)

    def _process_file(self, file_path: str) -> list:
        """Process single file into chunks."""
        document = load_document(file_path)
        metadata = extract_metadata(document, file_path)
        chunks = chunk_document(document)

        return [
            {"text": chunk, "metadata": {**metadata, "chunk_index": i}}
            for i, chunk in enumerate(chunks)
        ]
```

### Pattern 5: Quality Validation

```python
def validate_chunks(chunks: list) -> tuple[list, list]:
    """Validate chunk quality, return valid and invalid chunks."""

    valid = []
    invalid = []

    for chunk in chunks:
        issues = []

        # Check minimum content
        if len(chunk["text"].split()) < 10:
            issues.append("too_short")

        # Check for garbage
        if detect_garbage(chunk["text"]):
            issues.append("garbage_detected")

        # Check encoding issues
        if has_encoding_issues(chunk["text"]):
            issues.append("encoding_error")

        # Check for duplicate content
        if is_duplicate(chunk["text"], valid):
            issues.append("duplicate")

        if issues:
            chunk["issues"] = issues
            invalid.append(chunk)
        else:
            valid.append(chunk)

    return valid, invalid

def detect_garbage(text: str) -> bool:
    """Detect OCR errors, encoding issues, etc."""

    # High ratio of special characters
    special_ratio = len(re.findall(r'[^\w\s]', text)) / max(len(text), 1)
    if special_ratio > 0.3:
        return True

    # Repeated characters
    if re.search(r'(.)\1{10,}', text):
        return True

    # No actual words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
    if len(words) < 3:
        return True

    return False
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Fixed chunk size | Breaks sentences | Semantic chunking |
| No overlap | Lost context | 10-20% overlap |
| Ignoring structure | Poor retrieval | Structure-aware splitting |
| No metadata | Can't filter | Extract rich metadata |
| No validation | Garbage in vector DB | Quality checks |
| Full reindex | Slow, expensive | Incremental ingestion |

## Tools & References

### Related Skills
- faion-llamaindex-skill
- faion-langchain-skill
- faion-vector-db-skill

### Related Agents
- faion-rag-agent

### External Resources
- [LlamaIndex Document Loaders](https://docs.llamaindex.ai/en/stable/module_guides/loading/)
- [LangChain Document Loaders](https://python.langchain.com/docs/integrations/document_loaders/)
- [Unstructured.io](https://unstructured.io/) - Document parsing
- [Docling](https://github.com/DS4SD/docling) - IBM document conversion

## Checklist

- [ ] Identified all document sources
- [ ] Selected appropriate loaders
- [ ] Configured chunking strategy
- [ ] Set chunk size and overlap
- [ ] Added metadata extraction
- [ ] Implemented structure preservation
- [ ] Added quality validation
- [ ] Set up incremental ingestion
- [ ] Tested with sample documents
- [ ] Documented ingestion pipeline

---

*Methodology: M-RAG-001 | Category: RAG/Vector DB*
*Related: faion-rag-agent, faion-llamaindex-skill, faion-vector-db-skill*
