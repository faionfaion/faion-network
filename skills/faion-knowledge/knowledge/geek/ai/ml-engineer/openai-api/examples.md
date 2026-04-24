# OpenAI API Code Examples

Production-ready code examples for all major OpenAI APIs.

## Table of Contents

1. [Chat Completions](#chat-completions)
2. [Streaming](#streaming)
3. [Structured Output](#structured-output)
4. [Function Calling / Tool Use](#function-calling--tool-use)
5. [Error Handling](#error-handling)
6. [Vision API](#vision-api)
7. [Embeddings](#embeddings)
8. [Audio APIs](#audio-apis)
9. [Batch API](#batch-api)
10. [Async Operations](#async-operations)

---

## Chat Completions

### Basic Request

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",  # Pin version for production
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain SDD methodology in 3 sentences."}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### With All Parameters

```python
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a technical writer."},
        {"role": "user", "content": "Write a function docstring."}
    ],

    # Generation parameters
    temperature=0.7,        # 0-2, higher = more creative
    top_p=1.0,              # Nucleus sampling (alternative to temp)
    max_tokens=1000,        # Max response length
    n=1,                    # Number of completions

    # Control parameters
    stop=["\n\n", "---"],   # Stop sequences
    presence_penalty=0.0,   # -2 to 2, penalize repeated topics
    frequency_penalty=0.0,  # -2 to 2, penalize repeated tokens

    # Output format
    response_format={"type": "text"},  # or "json_object"
    seed=42,                # Deterministic outputs

    # Tracking
    user="user-123"         # Track abuse
)
```

### Multi-Turn Conversation

```python
class Conversation:
    """Manage multi-turn chat conversation."""

    def __init__(self, system_prompt: str, model: str = "gpt-4o-2024-08-06"):
        self.client = OpenAI()
        self.model = model
        self.messages = [{"role": "system", "content": system_prompt}]

    def chat(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=1000
        )

        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def reset(self):
        self.messages = [self.messages[0]]  # Keep system prompt

# Usage
conv = Conversation("You are a Python expert.")
print(conv.chat("What is a decorator?"))
print(conv.chat("Show me an example."))
```

---

## Streaming

### Basic Streaming

```python
stream = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[{"role": "user", "content": "Write a haiku about coding"}],
    stream=True
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
print()  # Final newline
```

### Streaming with Content Accumulation

```python
def stream_with_accumulation(messages: list, model: str = "gpt-4o-2024-08-06") -> str:
    """Stream response while accumulating full content."""
    client = OpenAI()
    full_content = []

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta

        if delta.content:
            full_content.append(delta.content)
            print(delta.content, end="", flush=True)

        # Check for completion
        if chunk.choices[0].finish_reason:
            print(f"\n[Finished: {chunk.choices[0].finish_reason}]")

    return "".join(full_content)
```

### Streaming with Callback

```python
from typing import Callable, Optional

def stream_with_callback(
    messages: list,
    on_token: Callable[[str], None],
    on_complete: Optional[Callable[[str], None]] = None
) -> str:
    """Stream with token callback for UI integration."""
    client = OpenAI()
    full_content = []

    stream = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        stream=True
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            full_content.append(content)
            on_token(content)

    result = "".join(full_content)
    if on_complete:
        on_complete(result)

    return result

# Usage with FastAPI SSE
# stream_with_callback(messages, lambda t: yield f"data: {t}\n\n")
```

### Async Streaming

```python
from openai import AsyncOpenAI
import asyncio

async def async_stream(messages: list) -> str:
    """Async streaming for concurrent applications."""
    client = AsyncOpenAI()
    full_content = []

    stream = await client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        stream=True
    )

    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            full_content.append(content)
            print(content, end="", flush=True)

    return "".join(full_content)

# asyncio.run(async_stream([{"role": "user", "content": "Hello"}]))
```

---

## Structured Output

### Basic Structured Output with Pydantic

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Entity(BaseModel):
    """Extracted entity from text."""
    name: str = Field(description="Entity name")
    type: str = Field(description="Entity type: person, company, location")
    confidence: float = Field(ge=0, le=1, description="Confidence score")

class ExtractionResult(BaseModel):
    """Complete extraction result."""
    entities: List[Entity]
    summary: str
    language: str = Field(default="en")

# Use beta parse method
response = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract entities from text."},
        {"role": "user", "content": "OpenAI was founded by Sam Altman in San Francisco."}
    ],
    response_format=ExtractionResult
)

result = response.choices[0].message.parsed
print(f"Found {len(result.entities)} entities")
for entity in result.entities:
    print(f"  - {entity.name} ({entity.type}): {entity.confidence:.2f}")
```

### Structured Output with Enums

```python
from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(BaseModel):
    title: str = Field(description="Task title")
    description: str = Field(description="Task description")
    priority: Priority
    status: TaskStatus = TaskStatus.TODO
    tags: List[str] = Field(default_factory=list)

class TaskList(BaseModel):
    tasks: List[Task]
    total_count: int

response = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "user", "content": "Create 3 tasks for launching a SaaS product"}
    ],
    response_format=TaskList
)

tasks = response.choices[0].message.parsed
for task in tasks.tasks:
    print(f"[{task.priority.value}] {task.title}")
```

### Handling Refusals

```python
def safe_parse(messages: list, response_format: type) -> Optional[BaseModel]:
    """Parse with refusal handling."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=response_format
    )

    message = response.choices[0].message

    # Check for content policy refusal
    if message.refusal:
        print(f"Request refused: {message.refusal}")
        return None

    return message.parsed
```

### Streaming with Structured Output

```python
from openai import OpenAI

client = OpenAI()

class StepByStep(BaseModel):
    steps: List[str]
    final_answer: str

# Use streaming with parse
with client.beta.chat.completions.stream(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "user", "content": "Solve: 25 * 4 + 10"}
    ],
    response_format=StepByStep
) as stream:
    for event in stream:
        if event.type == "content.delta":
            print(event.delta, end="", flush=True)

    # Get final parsed result
    result = stream.get_final_completion()
    parsed = result.choices[0].message.parsed
    print(f"\n\nFinal answer: {parsed.final_answer}")
```

---

## Function Calling / Tool Use

### Define Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g., 'Kyiv'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Search product database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["query"]
            }
        }
    }
]
```

### Complete Tool Loop

```python
import json

def get_weather(location: str, unit: str = "celsius") -> dict:
    """Mock weather function."""
    return {"temperature": 15, "condition": "cloudy", "unit": unit}

def search_database(query: str, limit: int = 10) -> dict:
    """Mock database search."""
    return {"results": [f"Result for {query}"], "count": 1}

# Map function names to implementations
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "search_database": search_database
}

def chat_with_tools(user_message: str) -> str:
    """Complete tool use loop."""
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        messages.append(message)

        # Check if model wants to use tools
        if not message.tool_calls:
            return message.content

        # Execute each tool call
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            # Execute function
            func = TOOL_FUNCTIONS.get(func_name)
            if func:
                result = func(**func_args)
            else:
                result = {"error": f"Unknown function: {func_name}"}

            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

# Usage
response = chat_with_tools("What's the weather in Kyiv?")
print(response)
```

### Parallel Tool Calls

```python
def handle_parallel_tools(messages: list) -> list:
    """Handle multiple tool calls in parallel."""
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        tools=tools,
        parallel_tool_calls=True  # Enable parallel calls
    )

    message = response.choices[0].message

    if message.tool_calls:
        # Execute all tools (could use asyncio.gather for true parallelism)
        tool_results = []
        for tool_call in message.tool_calls:
            func = TOOL_FUNCTIONS.get(tool_call.function.name)
            args = json.loads(tool_call.function.arguments)
            result = func(**args) if func else {"error": "Unknown function"}

            tool_results.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        return [message] + tool_results

    return [message]
```

### Forcing Tool Use

```python
# Force specific function
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[{"role": "user", "content": "Tell me about Kyiv"}],
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_weather"}}
)

# Require any tool (no text-only response)
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[{"role": "user", "content": "Get weather for Paris and London"}],
    tools=tools,
    tool_choice="required"
)

# Disable tools
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[{"role": "user", "content": "Just chat, no tools"}],
    tools=tools,
    tool_choice="none"
)
```

---

## Error Handling

### Comprehensive Error Handler

```python
import time
from openai import (
    OpenAI,
    APIError,
    RateLimitError,
    APIConnectionError,
    AuthenticationError,
    BadRequestError
)

def robust_completion(
    messages: list,
    max_retries: int = 5,
    base_delay: float = 1.0
) -> str:
    """Make API call with comprehensive error handling."""
    client = OpenAI()

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=messages,
                max_tokens=1000,
                timeout=30.0
            )
            return response.choices[0].message.content

        except AuthenticationError as e:
            # Don't retry auth errors
            raise ValueError(f"Invalid API key: {e}")

        except BadRequestError as e:
            # Don't retry bad requests (invalid params, too many tokens)
            raise ValueError(f"Bad request: {e}")

        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)

        except APIConnectionError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Connection error. Retrying in {delay}s...")
            time.sleep(delay)

        except APIError as e:
            if e.status_code and e.status_code >= 500:
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2 ** attempt)
                print(f"Server error. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise

    raise RuntimeError("Max retries exceeded")
```

### Using tenacity Library

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from openai import RateLimitError, APIError, APIConnectionError

@retry(
    retry=retry_if_exception_type((RateLimitError, APIConnectionError, APIError)),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5)
)
def reliable_completion(messages: list) -> str:
    """Completion with automatic retry using tenacity."""
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages
    )
    return response.choices[0].message.content
```

### Circuit Breaker Pattern

```python
from datetime import datetime, timedelta
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, block requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        reset_timeout: int = 60
    ):
        self.failure_threshold = failure_threshold
        self.reset_timeout = timedelta(seconds=reset_timeout)
        self.failures = 0
        self.state = CircuitState.CLOSED
        self.last_failure = None

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure > self.reset_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failures = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failures += 1
        self.last_failure = datetime.now()
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
breaker = CircuitBreaker()
result = breaker.call(reliable_completion, messages)
```

---

## Vision API

### Image from URL

```python
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg",
                        "detail": "high"  # "low" | "high" | "auto"
                    }
                }
            ]
        }
    ],
    max_tokens=500
)

print(response.choices[0].message.content)
```

### Image from Base64

```python
import base64
from pathlib import Path

def encode_image(image_path: str) -> str:
    """Encode image to base64."""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

def analyze_image(image_path: str, prompt: str) -> str:
    """Analyze local image with GPT-4 Vision."""
    image_data = encode_image(image_path)

    # Determine media type
    suffix = Path(image_path).suffix.lower()
    media_types = {".png": "png", ".jpg": "jpeg", ".jpeg": "jpeg", ".gif": "gif", ".webp": "webp"}
    media_type = media_types.get(suffix, "png")

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{media_type};base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content

# Usage
result = analyze_image("screenshot.png", "Describe this UI screenshot")
```

### Multiple Images

```python
def compare_images(image_urls: list, comparison_prompt: str) -> str:
    """Compare multiple images."""
    content = [{"type": "text", "text": comparison_prompt}]

    for url in image_urls:
        content.append({
            "type": "image_url",
            "image_url": {"url": url, "detail": "high"}
        })

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": content}],
        max_tokens=1000
    )

    return response.choices[0].message.content

# Usage
result = compare_images(
    ["https://example.com/design_v1.png", "https://example.com/design_v2.png"],
    "Compare these two design versions. Which is better for usability?"
)
```

---

## Embeddings

### Generate Embeddings

```python
def get_embedding(text: str, model: str = "text-embedding-3-large") -> list[float]:
    """Get embedding vector for text."""
    response = client.embeddings.create(
        model=model,
        input=text,
        encoding_format="float"
    )
    return response.data[0].embedding

# Usage
embedding = get_embedding("What is SDD methodology?")
print(f"Dimensions: {len(embedding)}")
```

### Batch Embeddings

```python
def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Get embeddings for multiple texts in single request."""
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=texts
    )
    return [item.embedding for item in response.data]

# Usage
texts = ["First document", "Second document", "Third document"]
embeddings = get_embeddings_batch(texts)
```

### Cosine Similarity

```python
import numpy as np

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_most_similar(query: str, documents: list[str]) -> tuple[int, float]:
    """Find most similar document to query."""
    query_emb = get_embedding(query)
    doc_embs = get_embeddings_batch(documents)

    similarities = [cosine_similarity(query_emb, doc) for doc in doc_embs]
    best_idx = np.argmax(similarities)

    return best_idx, similarities[best_idx]

# Usage
docs = ["Python is a programming language", "The weather is nice", "AI is transforming industries"]
idx, score = find_most_similar("Tell me about coding", docs)
print(f"Most similar: '{docs[idx]}' (score: {score:.4f})")
```

### Reduced Dimensions

```python
def get_embedding_reduced(text: str, dimensions: int = 256) -> list[float]:
    """Get embedding with reduced dimensions for cost/performance."""
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text,
        dimensions=dimensions  # Reduce from 3072
    )
    return response.data[0].embedding
```

---

## Audio APIs

### Speech-to-Text (Whisper)

```python
def transcribe_audio(audio_path: str, language: str = None) -> str:
    """Transcribe audio file to text."""
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,  # ISO 639-1 code, e.g., "uk" for Ukrainian
            response_format="text"
        )
    return transcript

# With timestamps
def transcribe_with_timestamps(audio_path: str) -> dict:
    """Transcribe with word-level timestamps."""
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"]
        )
    return result
```

### Text-to-Speech

```python
def generate_speech(
    text: str,
    output_path: str,
    voice: str = "nova",  # alloy, echo, fable, onyx, nova, shimmer
    model: str = "tts-1-hd"
) -> None:
    """Generate speech from text."""
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format="mp3"
    )
    response.stream_to_file(output_path)

# Streaming TTS
def stream_speech(text: str, output_path: str) -> None:
    """Stream speech generation for faster first byte."""
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=text
    ) as response:
        response.stream_to_file(output_path)
```

---

## Batch API

### Create Batch Job

```python
import json

def create_batch_file(requests: list[dict], output_path: str) -> str:
    """Create JSONL file for batch processing."""
    with open(output_path, "w") as f:
        for i, req in enumerate(requests):
            batch_req = {
                "custom_id": f"request-{i}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": req.get("model", "gpt-4o-mini"),
                    "messages": req["messages"],
                    "max_tokens": req.get("max_tokens", 100)
                }
            }
            f.write(json.dumps(batch_req) + "\n")
    return output_path

def submit_batch(requests_file: str) -> str:
    """Submit batch job and return batch ID."""
    # Upload file
    batch_file = client.files.create(
        file=open(requests_file, "rb"),
        purpose="batch"
    )

    # Create batch
    batch = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )

    return batch.id

def check_batch_status(batch_id: str) -> dict:
    """Check batch job status."""
    batch = client.batches.retrieve(batch_id)
    return {
        "status": batch.status,
        "completed": batch.request_counts.completed,
        "total": batch.request_counts.total,
        "failed": batch.request_counts.failed
    }

def get_batch_results(batch_id: str) -> list[dict]:
    """Get results from completed batch."""
    batch = client.batches.retrieve(batch_id)

    if batch.status != "completed":
        raise ValueError(f"Batch not completed: {batch.status}")

    result_file = client.files.content(batch.output_file_id)
    results = []

    for line in result_file.text.strip().split("\n"):
        result = json.loads(line)
        results.append({
            "custom_id": result["custom_id"],
            "content": result["response"]["body"]["choices"][0]["message"]["content"]
        })

    return results
```

---

## Async Operations

### Async Client

```python
from openai import AsyncOpenAI
import asyncio

async def async_completion(messages: list) -> str:
    """Async completion request."""
    client = AsyncOpenAI()
    response = await client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages
    )
    return response.choices[0].message.content

# Run multiple completions concurrently
async def parallel_completions(prompts: list[str]) -> list[str]:
    """Run multiple completions in parallel."""
    client = AsyncOpenAI()

    async def single_completion(prompt: str) -> str:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    return await asyncio.gather(*[single_completion(p) for p in prompts])

# Usage
# results = asyncio.run(parallel_completions(["Hello", "World", "!"]))
```

### Async with Rate Limiting

```python
import asyncio
from asyncio import Semaphore

async def rate_limited_completions(
    prompts: list[str],
    max_concurrent: int = 10
) -> list[str]:
    """Run completions with concurrency limit."""
    client = AsyncOpenAI()
    semaphore = Semaphore(max_concurrent)

    async def limited_completion(prompt: str) -> str:
        async with semaphore:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

    return await asyncio.gather(*[limited_completion(p) for p in prompts])
```

---

## Quick Reference

### Common Patterns

| Pattern | When to Use |
|---------|-------------|
| Streaming | Real-time UI, long responses |
| Structured Output | JSON APIs, data extraction |
| Tool Use | External systems, calculations |
| Batch API | Bulk processing, cost savings |
| Async | High concurrency, multiple requests |

### Token Estimation

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Count tokens in text."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def estimate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    model: str = "gpt-4o"
) -> float:
    """Estimate cost in USD."""
    prices = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60}
    }
    p = prices.get(model, prices["gpt-4o"])
    return (prompt_tokens * p["input"] + completion_tokens * p["output"]) / 1_000_000
```
