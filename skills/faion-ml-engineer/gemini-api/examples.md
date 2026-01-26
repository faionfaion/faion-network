# Gemini API Examples

Complete code examples for all Gemini API features.

---

## Table of Contents

1. [Basic Generation](#basic-generation)
2. [Chat Conversations](#chat-conversations)
3. [Streaming](#streaming)
4. [Multimodal Input](#multimodal-input)
5. [Function Calling](#function-calling)
6. [Live API (Real-time)](#live-api-real-time)
7. [Context Caching](#context-caching)
8. [Embeddings](#embeddings)
9. [Code Execution](#code-execution)
10. [Grounding with Search](#grounding-with-search)
11. [Safety Settings](#safety-settings)
12. [Advanced Patterns](#advanced-patterns)

---

## Basic Generation

### Simple Request

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("Explain quantum computing in simple terms")
print(response.text)
```

### With Generation Config

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
)

response = model.generate_content("Write a product description for a smartwatch")
```

### Gemini 3 with Thinking Level

```python
model = genai.GenerativeModel(
    model_name="gemini-3-pro",
    generation_config={
        "thinking_level": "high",  # low, medium (Flash), high, minimal (Flash)
    }
)

response = model.generate_content("Solve this complex math problem: ...")
```

### JSON Output

```python
import json

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "number"},
                "features": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["name", "price"]
        }
    }
)

response = model.generate_content("Create a product listing for wireless earbuds")
product = json.loads(response.text)
```

---

## Chat Conversations

### Basic Chat

```python
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat()

response = chat.send_message("Hello! I'm learning Python.")
print(response.text)

response = chat.send_message("What should I learn first?")
print(response.text)

# Access history
for message in chat.history:
    print(f"{message.role}: {message.parts[0].text}")
```

### Chat with System Instruction

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="""You are a helpful Python tutor.
    Always provide code examples.
    Explain concepts step by step.
    Use beginner-friendly language."""
)

chat = model.start_chat()
response = chat.send_message("What are decorators?")
```

### Multimodal Chat

```python
import PIL.Image

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# Text message
response = chat.send_message("I'll show you some code screenshots")

# Image message
image = PIL.Image.open("code_screenshot.png")
response = chat.send_message([
    "What's wrong with this code?",
    image
])
```

---

## Streaming

### Text Streaming

```python
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(
    "Write a long story about space exploration",
    stream=True
)

for chunk in response:
    print(chunk.text, end="", flush=True)
```

### Chat Streaming

```python
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat()

response = chat.send_message("Tell me about Mars", stream=True)

for chunk in response:
    print(chunk.text, end="")
```

### Async Streaming

```python
import asyncio
import google.generativeai as genai

async def stream_response():
    model = genai.GenerativeModel("gemini-2.0-flash")

    response = await model.generate_content_async(
        "Explain machine learning",
        stream=True
    )

    async for chunk in response:
        print(chunk.text, end="")

asyncio.run(stream_response())
```

---

## Multimodal Input

### Image Analysis

```python
import PIL.Image

model = genai.GenerativeModel("gemini-2.0-flash")

# From file
image = PIL.Image.open("photo.jpg")
response = model.generate_content([
    "Describe this image in detail",
    image
])

# From URL (upload first)
image_file = genai.upload_file("photo.jpg")
response = model.generate_content([
    "What objects are in this image?",
    image_file
])
```

### Multiple Images

```python
image1 = PIL.Image.open("before.jpg")
image2 = PIL.Image.open("after.jpg")

response = model.generate_content([
    "Compare these two images and describe the differences",
    image1,
    image2
])
```

### Video Understanding

```python
import time

# Upload video (supports MP4, MPEG, MOV, AVI, etc.)
video_file = genai.upload_file("presentation.mp4")

# Wait for processing
while video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = genai.get_file(video_file.name)

# Analyze video
model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content([
    "Summarize the key points of this video presentation",
    video_file
])
print(response.text)

# With timestamps
response = model.generate_content([
    "What happens at the 2:30 mark in this video?",
    video_file
])
```

### Audio Understanding

```python
import time

# Upload audio (supports MP3, WAV, AIFF, AAC, OGG, FLAC)
audio_file = genai.upload_file("podcast.mp3")

# Wait for processing
while audio_file.state.name == "PROCESSING":
    time.sleep(5)
    audio_file = genai.get_file(audio_file.name)

model = genai.GenerativeModel("gemini-1.5-pro")

# Transcription
response = model.generate_content([
    "Transcribe this audio recording",
    audio_file
])

# Analysis
response = model.generate_content([
    "What are the main topics discussed in this podcast?",
    audio_file
])
```

### PDF Processing

```python
pdf_file = genai.upload_file("document.pdf")

model = genai.GenerativeModel("gemini-1.5-pro")

# Summarize
response = model.generate_content([
    "Summarize this document",
    pdf_file
])

# Extract information
response = model.generate_content([
    "Extract all dates and deadlines mentioned",
    pdf_file
])

# Q&A
response = model.generate_content([
    "What is the total budget mentioned?",
    pdf_file
])
```

### Combined Modalities

```python
image = PIL.Image.open("chart.png")
audio_file = genai.upload_file("explanation.mp3")

response = model.generate_content([
    "This chart shows Q4 results. Listen to the audio and create a summary.",
    image,
    audio_file
])
```

### Gemini 3 Media Resolution

```python
model = genai.GenerativeModel(
    model_name="gemini-3-pro",
    generation_config={
        "media_resolution": "high",  # low, medium, high, ultra-high
    }
)

image = PIL.Image.open("detailed_diagram.png")
response = model.generate_content([
    "Analyze this technical diagram in detail",
    image
])
```

---

## Function Calling

### Basic Function Calling

```python
def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """Get the current weather in a given location.

    Args:
        location: The city and country, e.g. "London, UK"
        unit: Temperature unit - "celsius" or "fahrenheit"

    Returns:
        Weather information dictionary
    """
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
        max_results: Maximum number of results

    Returns:
        List of matching products
    """
    return [{"name": f"Product {i}", "price": 10 * i} for i in range(max_results)]

# Create model with tools
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[get_current_weather, search_products]
)

# Automatic function calling
chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message("What's the weather in Tokyo?")
print(response.text)  # Model called get_current_weather automatically
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

                # Send result back
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
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[get_current_weather, search_products]
)

chat = model.start_chat(enable_automatic_function_calling=True)

# Triggers parallel calls
response = chat.send_message(
    "What's the weather in London and search for umbrellas if it's rainy"
)
```

### Tool Config (Controlled Generation)

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[get_current_weather, search_products],
    tool_config={
        "function_calling_config": {
            # "AUTO" - model decides
            # "ANY" - must call a function
            # "NONE" - no function calling
            # "VALIDATED" - schema adherence
            "mode": "ANY",
            "allowed_function_names": ["get_current_weather"]
        }
    }
)
```

### Multimodal Function Responses (Gemini 3)

```python
# Function that returns image data
def get_product_image(product_id: str) -> dict:
    """Get product details with image."""
    return {
        "name": "Widget Pro",
        "image_path": "/path/to/image.jpg"
    }

# When sending function response, include image
import base64

with open("product.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Include image in function response
response = chat.send_message(
    genai.protos.Content(
        parts=[
            genai.protos.Part(
                function_response=genai.protos.FunctionResponse(
                    name="get_product_image",
                    response={
                        "result": {"name": "Widget Pro"},
                        "image": image_data  # Gemini 3 can process this
                    }
                )
            )
        ]
    )
)
```

---

## Live API (Real-time)

### Python Live API Setup

```python
import asyncio
import pyaudio
import google.generativeai as genai
from google.generativeai import types

async def live_audio_session():
    """Real-time audio conversation with Gemini."""

    # Audio configuration
    INPUT_SAMPLE_RATE = 16000   # 16kHz for input
    OUTPUT_SAMPLE_RATE = 24000  # 24kHz for output
    CHUNK_SIZE = 1024

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Input stream (microphone)
    input_stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=INPUT_SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )

    # Output stream (speaker)
    output_stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=OUTPUT_SAMPLE_RATE,
        output=True
    )

    # Connect to Live API
    async with genai.LiveSession(
        model="gemini-2.0-flash",
        config=types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Puck"  # Available voices: Puck, Charon, etc.
                    )
                )
            )
        )
    ) as session:

        async def send_audio():
            """Send audio from microphone to Gemini."""
            while True:
                data = input_stream.read(CHUNK_SIZE, exception_on_overflow=False)
                await session.send_audio(data)
                await asyncio.sleep(0.01)

        async def receive_audio():
            """Receive and play audio from Gemini."""
            async for response in session.receive():
                if response.audio:
                    output_stream.write(response.audio)

        # Run both tasks concurrently
        await asyncio.gather(send_audio(), receive_audio())

# Run the session
asyncio.run(live_audio_session())
```

### Live API with Function Calling

```python
async def live_with_tools():
    """Live session with function calling."""

    tools = [
        {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    ]

    async with genai.LiveSession(
        model="gemini-2.0-flash",
        config=types.LiveConnectConfig(
            tools=tools,
            response_modalities=["AUDIO", "TEXT"]
        )
    ) as session:

        async for response in session.receive():
            if response.function_calls:
                for call in response.function_calls:
                    # Execute function
                    result = execute_function(call.name, call.args)
                    # Send result back
                    await session.send_tool_response(call.id, result)
```

### Ephemeral Tokens (Client-side Auth)

```python
# Server-side: Generate ephemeral token
import google.auth

credentials, project = google.auth.default()
token = credentials.token  # Short-lived token

# Client-side: Use ephemeral token
config = types.LiveConnectConfig(
    ephemeral_token=token,  # Instead of API key
    response_modalities=["AUDIO"]
)
```

---

## Context Caching

### Creating a Cache

```python
from google.generativeai import caching

# Upload large document
document = genai.upload_file("large_document.pdf")

# Create cache (minimum 32K tokens)
cache = caching.CachedContent.create(
    model="gemini-1.5-pro",
    display_name="Large document cache",
    system_instruction="You are an expert document analyzer.",
    contents=[document],
    ttl="3600s"  # 1 hour
)

print(f"Cache created: {cache.name}")
print(f"Token count: {cache.usage_metadata.total_token_count}")
```

### Using Cached Content

```python
# Create model from cache
model = genai.GenerativeModel.from_cached_content(cache)

# Queries use cached context (faster, cheaper)
response = model.generate_content("Summarize the main points")
response = model.generate_content("What are the key dates?")
```

### Managing Caches

```python
# List caches
for c in caching.CachedContent.list():
    print(f"{c.name}: {c.display_name}")

# Get specific cache
cache = caching.CachedContent.get("cachedContents/xxxxx")

# Update TTL
cache.update(ttl="7200s")  # Extend to 2 hours

# Delete cache
cache.delete()
```

---

## Embeddings

### Text Embeddings

```python
result = genai.embed_content(
    model="models/text-embedding-004",
    content="What is machine learning?",
    task_type="RETRIEVAL_DOCUMENT"
)

embedding = result["embedding"]
print(f"Dimension: {len(embedding)}")  # 768
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

| Task Type | Use Case |
|-----------|----------|
| `RETRIEVAL_DOCUMENT` | Indexing documents |
| `RETRIEVAL_QUERY` | Search queries |
| `SEMANTIC_SIMILARITY` | Deduplication |
| `CLASSIFICATION` | Categorization |
| `CLUSTERING` | Topic modeling |
| `QUESTION_ANSWERING` | Q&A systems |
| `FACT_VERIFICATION` | Fact checking |

### Similarity Search

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Index documents
documents = [
    "How to learn Python programming",
    "Best practices for machine learning",
    "Introduction to web development"
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

# Find best match
similarities = [cosine_similarity(query_embedding, doc) for doc in doc_embeddings]
best_idx = np.argmax(similarities)
print(f"Best match: {documents[best_idx]}")
```

---

## Code Execution

### Python Sandbox

```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=["code_execution"]
)

response = model.generate_content(
    "Calculate the first 20 Fibonacci numbers"
)

# Access executed code and output
for part in response.candidates[0].content.parts:
    if hasattr(part, 'executable_code'):
        print("Code:")
        print(part.executable_code.code)
    if hasattr(part, 'code_execution_result'):
        print("Output:")
        print(part.code_execution_result.output)
```

### Data Analysis

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=["code_execution"]
)

csv_file = genai.upload_file("sales_data.csv")

response = model.generate_content([
    "Analyze this data. Calculate averages, find trends, create summary.",
    csv_file
])
```

### Chart Generation

```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=["code_execution"]
)

response = model.generate_content("""
Create a bar chart showing programming language popularity:
- Python: 35%
- JavaScript: 28%
- Java: 15%
- C++: 12%
- Other: 10%
""")
```

---

## Grounding with Search

### Enable Search Grounding

```python
from google.generativeai.types import Tool

search_tool = Tool.from_google_search_retrieval(
    google_search_retrieval={
        "dynamic_retrieval_config": {
            "mode": "MODE_DYNAMIC",
            "dynamic_threshold": 0.3  # 0-1, higher = more selective
        }
    }
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[search_tool]
)

response = model.generate_content("What are the latest AI developments in 2026?")
print(response.text)

# Access sources
if response.candidates[0].grounding_metadata:
    for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
        print(f"Source: {chunk.web.uri}")
        print(f"Title: {chunk.web.title}")
```

### Combining Search with Functions

```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[search_tool, get_current_weather]
)

chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message(
    "What's the weather forecast for Tokyo according to recent reports?"
)
```

---

## Safety Settings

### Configuring Safety

```python
from google.generativeai.types import HarmCategory, HarmBlockThreshold

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
)

response = model.generate_content("Your prompt")

# Check safety ratings
if response.prompt_feedback.block_reason:
    print(f"Blocked: {response.prompt_feedback.block_reason}")
else:
    for rating in response.candidates[0].safety_ratings:
        print(f"{rating.category}: {rating.probability}")
```

### Block Thresholds

| Threshold | Description |
|-----------|-------------|
| `BLOCK_NONE` | Always show |
| `BLOCK_LOW_AND_ABOVE` | Block low+ |
| `BLOCK_MEDIUM_AND_ABOVE` | Block medium+ (default) |
| `BLOCK_ONLY_HIGH` | Block high only |

---

## Advanced Patterns

### RAG with Gemini

```python
def rag_query(question: str):
    # Get query embedding
    query_emb = genai.embed_content(
        model="models/text-embedding-004",
        content=question,
        task_type="RETRIEVAL_QUERY"
    )["embedding"]

    # Retrieve relevant documents
    relevant_docs = vector_store.similarity_search(query_emb, k=5)

    # Generate answer
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
def run_agent(user_query: str, max_iterations: int = 5):
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        tools=[search_web, get_weather, calculate],
        system_instruction="You are a helpful assistant. Use tools when needed."
    )

    chat = model.start_chat()

    for i in range(max_iterations):
        response = chat.send_message(user_query if i == 0 else "Continue")

        has_function_call = False
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                has_function_call = True
                fn = part.function_call
                result = execute_function(fn.name, dict(fn.args))

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
from pydantic import BaseModel
from typing import List

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
Maria Garcia (28), a designer from New York, on January 15, 2026.
"""

response = model.generate_content(f"Extract all entities: {text}")
data = ExtractedData.model_validate_json(response.text)
```

### Error Handling

```python
from google.generativeai.types import StopCandidateException, BlockedPromptException
from google.api_core.exceptions import ResourceExhausted
import time

def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text

        except BlockedPromptException as e:
            print(f"Prompt blocked: {e}")
            return None

        except StopCandidateException as e:
            print(f"Generation stopped: {e}")
            if e.args and e.args[0].content:
                return e.args[0].content.parts[0].text
            return None

        except ResourceExhausted:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

### Vertex AI Integration

```python
import vertexai
from vertexai.generative_models import GenerativeModel, Part

vertexai.init(project="your-gcp-project", location="us-central1")

model = GenerativeModel("gemini-1.5-pro")
response = model.generate_content("Explain quantum computing")

# Using GCS for large files
video_part = Part.from_uri(
    uri="gs://your-bucket/video.mp4",
    mime_type="video/mp4"
)

response = model.generate_content([
    "Summarize this video",
    video_part
])
```

---

*Last updated: 2026-01-25*
