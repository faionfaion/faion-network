---
name: faion-gemini-function-calling
user-invocable: false
description: "Gemini function calling, grounding, embeddings, advanced patterns"
---

# Gemini Function Calling & Advanced Features

**Function calling, Google Search grounding, embeddings, and advanced patterns.**

---

## Quick Reference

| Feature | Description |
|---------|-------------|
| **Function Calling** | Automatic and manual function execution |
| **Parallel Calls** | Multiple functions in one request |
| **Tool Config** | Control function calling behavior |
| **Search Grounding** | Google Search integration |
| **Embeddings** | text-embedding-004 (768 dimensions) |

---

## Function Calling

### Basic Function Calling

```python
import google.generativeai as genai

def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """Get the current weather in a given location.

    Args:
        location: The city and country, e.g. "London, UK"
        unit: Temperature unit - "celsius" or "fahrenheit"

    Returns:
        Weather information dictionary
    """
    # Simulated response
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "condition": "sunny"
    }

def search_products(query: str, max_results: int = 5) -> list:
    """Search for products in the catalog.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of matching products
    """
    # Simulated response
    return [{"name": f"Product {i}", "price": 10 * i} for i in range(max_results)]

# Create model with tools
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[get_current_weather, search_products]
)

# Automatic function calling
chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message("What's the weather in Tokyo?")
print(response.text)  # Model called get_current_weather and responded

response = chat.send_message("Find me 3 laptop products")
print(response.text)  # Model called search_products
```

### Manual Function Calling

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[get_current_weather]
)

chat = model.start_chat()
response = chat.send_message("What's the weather in Paris?")

# Check if model wants to call a function
for candidate in response.candidates:
    for part in candidate.content.parts:
        if hasattr(part, 'function_call'):
            fn_call = part.function_call
            print(f"Function: {fn_call.name}")
            print(f"Args: {dict(fn_call.args)}")

            # Execute function
            if fn_call.name == "get_current_weather":
                result = get_current_weather(**dict(fn_call.args))

                # Send result back to model
                response = chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=fn_call.name,
                                response={"result": result}
                            )
                        )]
                    )
                )
                print(response.text)
```

### Parallel Function Calling

```python
# Gemini can call multiple functions in parallel
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[get_current_weather, search_products]
)

chat = model.start_chat(enable_automatic_function_calling=True)

# This may trigger parallel calls
response = chat.send_message(
    "What's the weather in London and search for umbrellas if it's rainy"
)
```

### Tool Config (Controlled Generation)

```python
from google.generativeai.types import content_types

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[get_current_weather, search_products],
    tool_config={
        "function_calling_config": {
            # "AUTO" - model decides
            # "ANY" - must call a function
            # "NONE" - no function calling
            "mode": "ANY",
            # Restrict to specific functions
            "allowed_function_names": ["get_current_weather"]
        }
    }
)
```

---

## Grounding with Google Search

### Enable Search Grounding

```python
from google.generativeai import GenerativeModel
from google.generativeai.types import Tool

# Create search tool
search_tool = Tool.from_google_search_retrieval(
    google_search_retrieval={
        "dynamic_retrieval_config": {
            "mode": "MODE_DYNAMIC",  # or "MODE_UNSPECIFIED"
            "dynamic_threshold": 0.3  # 0-1, higher = more selective
        }
    }
)

model = GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[search_tool]
)

response = model.generate_content("What are the latest developments in AI in 2026?")
print(response.text)

# Access grounding metadata
if response.candidates[0].grounding_metadata:
    for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
        print(f"Source: {chunk.web.uri}")
        print(f"Title: {chunk.web.title}")
```

### Combining Search with Functions

```python
model = GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[search_tool, get_current_weather]
)

chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message(
    "What's the weather forecast for Tokyo this week according to recent reports?"
)
```

---

## Embeddings

### Text Embeddings

```python
# Using the embeddings model
result = genai.embed_content(
    model="models/text-embedding-004",
    content="What is machine learning?",
    task_type="RETRIEVAL_DOCUMENT"  # or "RETRIEVAL_QUERY", "SEMANTIC_SIMILARITY", etc.
)

embedding = result["embedding"]
print(f"Embedding dimension: {len(embedding)}")  # 768
```

### Batch Embeddings

```python
texts = [
    "Machine learning is a subset of AI",
    "Deep learning uses neural networks",
    "Python is popular for data science"
]

result = genai.embed_content(
    model="models/text-embedding-004",
    content=texts,
    task_type="RETRIEVAL_DOCUMENT"
)

embeddings = result["embedding"]  # List of embeddings
```

### Task Types

| Task Type | Description | Use Case |
|-----------|-------------|----------|
| `RETRIEVAL_DOCUMENT` | Embed documents for retrieval | Indexing documents |
| `RETRIEVAL_QUERY` | Embed search queries | Search queries |
| `SEMANTIC_SIMILARITY` | Compare text similarity | Deduplication |
| `CLASSIFICATION` | Text classification | Categorization |
| `CLUSTERING` | Group similar texts | Topic modeling |
| `QUESTION_ANSWERING` | Q&A embeddings | Q&A systems |
| `FACT_VERIFICATION` | Verify facts | Fact checking |

### Similarity Search Example

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Index documents
documents = [
    "How to learn Python programming",
    "Best practices for machine learning",
    "Introduction to web development",
    "Guide to cloud computing"
]

doc_embeddings = genai.embed_content(
    model="models/text-embedding-004",
    content=documents,
    task_type="RETRIEVAL_DOCUMENT"
)["embedding"]

# Search
query = "I want to learn AI"
query_embedding = genai.embed_content(
    model="models/text-embedding-004",
    content=query,
    task_type="RETRIEVAL_QUERY"
)["embedding"]

# Find most similar
similarities = [cosine_similarity(query_embedding, doc_emb) for doc_emb in doc_embeddings]
best_match_idx = np.argmax(similarities)
print(f"Best match: {documents[best_match_idx]}")
```

---

## Advanced Patterns

### RAG with Gemini

```python
# 1. Index documents with embeddings
documents = load_documents()  # Your document loader
doc_embeddings = genai.embed_content(
    model="models/text-embedding-004",
    content=[doc.text for doc in documents],
    task_type="RETRIEVAL_DOCUMENT"
)["embedding"]

# 2. Store in vector database (Chroma, Pinecone, etc.)
vector_store.add(doc_embeddings, documents)

# 3. Query
def rag_query(question: str):
    # Get query embedding
    query_emb = genai.embed_content(
        model="models/text-embedding-004",
        content=question,
        task_type="RETRIEVAL_QUERY"
    )["embedding"]

    # Retrieve relevant documents
    relevant_docs = vector_store.similarity_search(query_emb, k=5)

    # Generate answer with context
    model = genai.GenerativeModel("gemini-1.5-pro")
    context = "\n\n".join([doc.text for doc in relevant_docs])

    response = model.generate_content(f"""
    Context: {context}

    Question: {question}

    Answer based on the context above:
    """)

    return response.text
```

### Agent Loop

```python
import json

def run_agent(user_query: str, max_iterations: int = 5):
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        tools=[search_web, get_weather, calculate],
        system_instruction="You are a helpful assistant. Use tools when needed."
    )

    chat = model.start_chat()

    for i in range(max_iterations):
        response = chat.send_message(user_query if i == 0 else "Continue")

        # Check for function calls
        has_function_call = False
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                has_function_call = True
                fn = part.function_call

                # Execute function
                result = execute_function(fn.name, dict(fn.args))

                # Send result back
                chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=fn.name,
                                response={"result": result}
                            )
                        )]
                    )
                )

        if not has_function_call:
            return response.text

    return "Max iterations reached"
```

### Structured Extraction

```python
from typing import List
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    occupation: str

class ExtractedData(BaseModel):
    people: List[Person]
    locations: List[str]
    dates: List[str]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": ExtractedData.model_json_schema()
    }
)

text = """
John Smith (35), a software engineer from San Francisco, met
Maria Garcia (28), a designer from New York, at a conference
on January 15, 2026.
"""

response = model.generate_content(f"Extract all entities from this text: {text}")
data = ExtractedData.model_validate_json(response.text)
```

---

## Best Practices

### Function Calling

1. **Clear docstrings** - Model uses docstrings to understand functions
2. **Type hints** - Required for function declarations
3. **Automatic mode** - Use automatic function calling for simplicity
4. **Error handling** - Handle function execution errors gracefully

### Grounding

1. **Dynamic mode** - Let model decide when to search
2. **Check sources** - Always verify grounding metadata
3. **Combine with tools** - Use search with custom functions
4. **Set threshold** - Adjust dynamic_threshold for selectivity

### Embeddings

1. **Right task type** - Use RETRIEVAL_DOCUMENT for indexing, RETRIEVAL_QUERY for search
2. **Batch processing** - Embed multiple texts in one call
3. **Normalize vectors** - For cosine similarity
4. **Cache embeddings** - Store computed embeddings

---

## Sources

- [Gemini Function Calling](https://ai.google.dev/docs/function_calling)
- [Gemini Grounding](https://ai.google.dev/docs/grounding)
- [Gemini Embeddings](https://ai.google.dev/docs/embeddings)

---

*Part of faion-ml-engineer skill*
*Last updated: 2026-01-23*
