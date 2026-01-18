# M-RAG-007: Multimodal RAG

## Overview

Multimodal RAG handles documents containing images, tables, charts, and other non-text content. It combines text embeddings with visual understanding to retrieve and reason over mixed-media content. Essential for PDFs, slides, and technical documentation.

**When to use:** Documents with diagrams, charts, tables, screenshots, or any content where visual elements carry meaning.

## Core Concepts

### 1. Multimodal Content Types

| Type | Extraction Method | Embedding Strategy |
|------|-------------------|-------------------|
| **Text** | Direct extraction | Text embeddings |
| **Images** | Vision model | CLIP/multimodal embeddings |
| **Tables** | Structure extraction | Text + layout embeddings |
| **Charts** | Chart understanding | Vision + data extraction |
| **Diagrams** | Scene understanding | Vision embeddings |
| **Code** | Syntax parsing | Code-specific embeddings |

### 2. Processing Strategies

```
Document
    ├── Text → Text Chunker → Text Embeddings
    ├── Images → Vision Model → Image Embeddings + Descriptions
    ├── Tables → Table Parser → Structured Data + Embeddings
    └── Charts → Chart Reader → Data + Summary
                    ↓
              Unified Vector Store
                    ↓
              Multimodal Retrieval
```

### 3. Embedding Options

| Model | Modalities | Dimensions | Shared Space |
|-------|------------|------------|--------------|
| **CLIP** | Text, Image | 512 | Yes |
| **Jina CLIP v2** | Text, Image | 1024 | Yes |
| **ColPali** | Text, Document Images | 128 | Yes |
| **BGE-VL** | Text, Image | 768 | Yes |
| **LLaVA** | Text, Image (description) | N/A | Via description |

## Best Practices

### 1. Extract and Describe Images

```python
from openai import OpenAI
import base64

def process_image(image_path: str, context: str = "") -> dict:
    """Extract description from image using vision model."""

    client = OpenAI()

    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                        Describe this image in detail. Include:
                        1. What type of image it is (diagram, chart, photo, etc.)
                        2. Main content and key information
                        3. Any text visible in the image
                        4. Data or numbers if present

                        Context from document: {context}
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    )

    return {
        "description": response.choices[0].message.content,
        "image_path": image_path,
        "type": "image"
    }
```

### 2. Extract Tables Properly

```python
from unstructured.partition.pdf import partition_pdf

def extract_tables(pdf_path: str) -> list:
    """Extract tables with structure preserved."""

    elements = partition_pdf(
        filename=pdf_path,
        strategy="hi_res",
        infer_table_structure=True,
        extract_image_block_types=["Table"]
    )

    tables = []
    for element in elements:
        if element.category == "Table":
            # Get table as HTML for structure
            html_table = element.metadata.text_as_html

            # Convert to markdown for embedding
            markdown = html_to_markdown(html_table)

            # Get surrounding context
            context = get_surrounding_text(element)

            tables.append({
                "html": html_table,
                "markdown": markdown,
                "context": context,
                "type": "table"
            })

    return tables

def html_to_markdown(html: str) -> str:
    """Convert HTML table to markdown for better embedding."""

    from markdownify import markdownify
    return markdownify(html, heading_style="ATX")
```

### 3. Create Unified Index

```python
from transformers import CLIPProcessor, CLIPModel
import torch

class MultimodalIndexer:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
        self.text_embedder = load_text_embedder()

    def index_document(self, doc_path: str):
        """Index document with all modalities."""

        # Extract all elements
        elements = self._extract_elements(doc_path)

        for element in elements:
            if element["type"] == "text":
                # Standard text embedding
                embedding = self.text_embedder.embed(element["content"])
                self._store(element, embedding, modality="text")

            elif element["type"] == "image":
                # Dual storage: image embedding + description embedding
                # Image embedding for cross-modal search
                img_embedding = self._embed_image(element["image_data"])
                self._store(element, img_embedding, modality="image_visual")

                # Description embedding for text-to-image
                desc_embedding = self.text_embedder.embed(element["description"])
                self._store(element, desc_embedding, modality="image_text")

            elif element["type"] == "table":
                # Embed table as text
                embedding = self.text_embedder.embed(element["markdown"])
                self._store(element, embedding, modality="table")

    def _embed_image(self, image_data) -> list:
        """Embed image using CLIP."""

        inputs = self.clip_processor(images=image_data, return_tensors="pt")
        with torch.no_grad():
            embedding = self.clip_model.get_image_features(**inputs)
        return embedding[0].numpy().tolist()
```

## Common Patterns

### Pattern 1: ColPali Document Embedding

```python
from colpali import ColPali

class ColPaliRAG:
    """Use ColPali for document-level visual embeddings."""

    def __init__(self, vector_store):
        self.model = ColPali.from_pretrained("vidore/colpali-v1.2")
        self.vector_store = vector_store

    def index_pdf(self, pdf_path: str):
        """Index PDF pages as images."""

        from pdf2image import convert_from_path

        pages = convert_from_path(pdf_path)

        for i, page in enumerate(pages):
            # Embed page image
            embedding = self.model.embed_image(page)

            # Also get text for hybrid search
            text = extract_text_from_image(page)

            self.vector_store.upsert({
                "id": f"{pdf_path}_{i}",
                "vector": embedding,
                "metadata": {
                    "source": pdf_path,
                    "page": i,
                    "text": text,
                    "type": "pdf_page"
                }
            })

    def search(self, query: str, k: int = 5) -> list:
        """Search using text query against document images."""

        # ColPali embeds text in same space as images
        query_embedding = self.model.embed_text(query)

        results = self.vector_store.search(
            vector=query_embedding,
            limit=k
        )

        return results
```

### Pattern 2: Vision-Language RAG

```python
class VisionLanguageRAG:
    """RAG with vision-language model for image understanding."""

    def __init__(self, vector_store, vlm_model="gpt-4o"):
        self.vector_store = vector_store
        self.vlm = vlm_model

    def query(self, question: str, include_images: bool = True) -> str:
        """Answer question using text and images."""

        # Retrieve relevant chunks (text and images)
        results = self.vector_store.search(
            vector=embed(question),
            limit=10
        )

        # Separate text and image results
        text_chunks = [r for r in results if r.metadata["type"] == "text"]
        image_chunks = [r for r in results if r.metadata["type"] in ["image", "pdf_page"]]

        # Build context
        text_context = "\n\n".join([r.content for r in text_chunks])

        # Prepare message with images
        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": f"Question: {question}\n\nText context:\n{text_context}"}
            ]
        }]

        # Add images to message
        if include_images and image_chunks:
            for img in image_chunks[:3]:  # Limit images
                messages[0]["content"].append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img.metadata['image_b64']}"}
                })

            messages[0]["content"].append({
                "type": "text",
                "text": "Use both the text and images to answer the question comprehensively."
            })

        response = self._call_vlm(messages)
        return response
```

### Pattern 3: Table-Aware RAG

```python
class TableAwareRAG:
    """RAG optimized for tabular data."""

    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm

    def index_table(self, table: dict, context: str):
        """Index table with multiple representations."""

        # 1. Full table as markdown
        self._store_chunk({
            "content": table["markdown"],
            "type": "table_full",
            "metadata": {"context": context}
        })

        # 2. Row-by-row with headers
        rows = self._table_to_rows(table["html"])
        for i, row in enumerate(rows):
            self._store_chunk({
                "content": f"Row {i}: {row}",
                "type": "table_row",
                "metadata": {"table_context": context, "row_index": i}
            })

        # 3. Summary/description
        summary = self._summarize_table(table["markdown"])
        self._store_chunk({
            "content": summary,
            "type": "table_summary",
            "metadata": {"full_table": table["markdown"]}
        })

    def query_table(self, question: str) -> str:
        """Answer question that may require table data."""

        # Retrieve
        results = self.vector_store.search(embed(question), limit=10)

        # Find full tables from matched rows
        tables = set()
        for r in results:
            if r.metadata["type"] in ["table_row", "table_full"]:
                tables.add(r.metadata.get("full_table") or r.content)

        # Use SQL-like reasoning for structured questions
        if self._is_aggregation_question(question):
            return self._answer_with_analysis(question, tables)
        else:
            return self._answer_with_context(question, tables)

    def _answer_with_analysis(self, question: str, tables: set) -> str:
        """Answer questions requiring table analysis."""

        prompt = f"""
        Analyze these tables to answer the question.

        Tables:
        {chr(10).join(tables)}

        Question: {question}

        If the question requires calculation (sum, average, count, etc.),
        perform the calculation and show your work.
        """

        return self.llm.invoke(prompt)
```

### Pattern 4: Chart Understanding

```python
class ChartRAG:
    """RAG with chart understanding capabilities."""

    def __init__(self, vector_store, vision_model):
        self.vector_store = vector_store
        self.vision = vision_model

    def process_chart(self, image_data, context: str) -> dict:
        """Extract data and meaning from chart."""

        prompt = """
        Analyze this chart and extract:
        1. Chart type (bar, line, pie, scatter, etc.)
        2. Title and axis labels
        3. All data points/values visible
        4. Key trends or insights
        5. Any annotations or callouts

        Format as JSON with structure:
        {
            "chart_type": "...",
            "title": "...",
            "x_axis": "...",
            "y_axis": "...",
            "data": [...],
            "insights": ["...", "..."]
        }
        """

        analysis = self.vision.analyze(image_data, prompt)
        parsed = json.loads(analysis)

        return {
            "type": "chart",
            "analysis": parsed,
            "context": context,
            "image_data": image_data,
            "searchable_text": self._to_searchable_text(parsed)
        }

    def _to_searchable_text(self, analysis: dict) -> str:
        """Convert chart analysis to searchable text."""

        parts = [
            f"Chart: {analysis['title']}",
            f"Type: {analysis['chart_type']}",
            f"Shows: {analysis['x_axis']} vs {analysis['y_axis']}",
            f"Key insights: {', '.join(analysis['insights'])}"
        ]

        if analysis.get("data"):
            parts.append(f"Data points: {analysis['data']}")

        return "\n".join(parts)
```

### Pattern 5: Screenshot RAG

```python
class ScreenshotRAG:
    """RAG for application screenshots and UI documentation."""

    def __init__(self, vector_store, ocr_model, vision_model):
        self.vector_store = vector_store
        self.ocr = ocr_model
        self.vision = vision_model

    def process_screenshot(self, image_path: str, app_context: str) -> dict:
        """Process screenshot for RAG indexing."""

        # OCR: Extract text
        ocr_text = self.ocr.extract(image_path)

        # Vision: Describe UI
        ui_description = self.vision.analyze(image_path, """
        Describe this application screenshot:
        1. What application/screen is shown?
        2. What UI elements are visible (buttons, forms, menus)?
        3. What actions can the user take?
        4. What state or data is displayed?
        """)

        # Combined representation
        combined = f"""
        Application: {app_context}

        Visible text:
        {ocr_text}

        UI Description:
        {ui_description}
        """

        return {
            "type": "screenshot",
            "ocr_text": ocr_text,
            "ui_description": ui_description,
            "combined": combined,
            "image_path": image_path
        }

    def search(self, query: str, k: int = 5) -> list:
        """Search screenshots by description or text."""

        results = self.vector_store.search(embed(query), limit=k)

        # Filter to screenshots
        screenshots = [r for r in results if r.metadata["type"] == "screenshot"]

        return screenshots
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Ignoring images | Missing key information | Process all visual content |
| Text-only table search | Poor table retrieval | Index multiple representations |
| No visual context | Disconnected chunks | Link images to surrounding text |
| Large image base64 in prompts | Token waste | Resize, use references |
| Single modality search | Incomplete results | Unified multimodal index |

## Tools & References

### Related Skills
- faion-llamaindex-skill
- faion-vector-db-skill
- faion-image-gen-skill

### Related Agents
- faion-rag-agent
- faion-multimodal-agent

### External Resources
- [ColPali](https://github.com/illuin-tech/colpali)
- [LlamaIndex Multimodal](https://docs.llamaindex.ai/en/stable/examples/multi_modal/)
- [Unstructured.io](https://unstructured.io/)
- [CLIP](https://openai.com/research/clip)

## Checklist

- [ ] Identified document content types
- [ ] Implemented image extraction
- [ ] Added table structure parsing
- [ ] Set up chart understanding
- [ ] Created multimodal embeddings
- [ ] Built unified vector index
- [ ] Linked visual elements to context
- [ ] Tested cross-modal retrieval
- [ ] Optimized for query types
- [ ] Documented processing pipeline

---

*Methodology: M-RAG-007 | Category: RAG/Vector DB*
*Related: faion-multimodal-agent, faion-rag-agent*
