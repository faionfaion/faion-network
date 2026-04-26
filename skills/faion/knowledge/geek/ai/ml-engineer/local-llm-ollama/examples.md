# Ollama Code Examples

## Basic Python Integration

### Using REST API

```python
import requests
import json
from typing import Optional

OLLAMA_URL = "http://localhost:11434"

def generate(
    prompt: str,
    model: str = "llama3.1:8b",
    system: str = "",
    temperature: float = 0.7
) -> str:
    """Simple text generation."""
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["response"]

def chat(
    messages: list[dict],
    model: str = "llama3.1:8b",
    temperature: float = 0.7
) -> str:
    """Chat completion with message history."""
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["message"]["content"]

# Usage
result = generate("Explain Docker in one paragraph")
print(result)

messages = [
    {"role": "system", "content": "You are a Python expert."},
    {"role": "user", "content": "What's the best way to handle exceptions?"}
]
result = chat(messages)
print(result)
```

### Using Official Python Library

```python
import ollama

# Simple generation
response = ollama.generate(
    model="llama3.1:8b",
    prompt="Write a haiku about programming"
)
print(response["response"])

# Chat with history
response = ollama.chat(
    model="llama3.1:8b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Why is the sky blue?"}
    ]
)
print(response["message"]["content"])
```

## Streaming Responses

### REST API Streaming

```python
def stream_generate(
    prompt: str,
    model: str = "llama3.1:8b",
    callback: Optional[callable] = None
) -> str:
    """Stream response tokens in real-time."""
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": True
        },
        stream=True,
        timeout=120
    )

    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            token = data.get("response", "")

            if callback:
                callback(token)
            else:
                print(token, end="", flush=True)

            full_response += token

            if data.get("done"):
                break

    return full_response

# Usage
result = stream_generate("Tell me a story")
```

### Library Streaming

```python
import ollama

stream = ollama.chat(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
```

## Async Implementation

```python
import aiohttp
import asyncio
from typing import AsyncIterator

class AsyncOllama:
    """Async Ollama client for concurrent requests."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    async def generate(
        self,
        prompt: str,
        model: str = "llama3.1:8b",
        **kwargs
    ) -> str:
        """Async generation."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    **kwargs
                },
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                data = await response.json()
                return data["response"]

    async def chat(
        self,
        messages: list[dict],
        model: str = "llama3.1:8b",
        **kwargs
    ) -> str:
        """Async chat completion."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    **kwargs
                },
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                data = await response.json()
                return data["message"]["content"]

    async def stream_generate(
        self,
        prompt: str,
        model: str = "llama3.1:8b"
    ) -> AsyncIterator[str]:
        """Async streaming generation."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": True}
            ) as response:
                async for line in response.content:
                    if line:
                        data = json.loads(line)
                        yield data.get("response", "")
                        if data.get("done"):
                            break

# Batch processing
async def batch_generate(prompts: list[str]) -> list[str]:
    """Process multiple prompts concurrently."""
    client = AsyncOllama()
    tasks = [client.generate(p) for p in prompts]
    return await asyncio.gather(*tasks)

# Usage
async def main():
    client = AsyncOllama()

    # Single request
    result = await client.generate("Hello!")
    print(result)

    # Batch processing
    prompts = ["Explain Python", "Explain JavaScript", "Explain Go"]
    results = await batch_generate(prompts)
    for prompt, result in zip(prompts, results):
        print(f"{prompt}: {result[:100]}...")

asyncio.run(main())
```

## Embeddings

```python
def get_embedding(text: str, model: str = "nomic-embed-text") -> list[float]:
    """Generate embeddings locally."""
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={
            "model": model,
            "prompt": text
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()["embedding"]

def get_batch_embeddings(
    texts: list[str],
    model: str = "nomic-embed-text"
) -> list[list[float]]:
    """Generate embeddings for multiple texts."""
    return [get_embedding(text, model) for text in texts]

# Using library
import ollama

response = ollama.embeddings(
    model="nomic-embed-text",
    prompt="Hello world"
)
embedding = response["embedding"]
print(f"Embedding dimension: {len(embedding)}")  # 768 for nomic-embed-text
```

## Tool Calling / Function Calling

```python
import ollama
import json

# Define tools
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
                        "description": "City name, e.g., 'London'"
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
            "description": "Search the product database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results to return"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Tool implementations
def get_weather(location: str, unit: str = "celsius") -> dict:
    # Mock implementation
    return {"location": location, "temperature": 22, "unit": unit}

def search_database(query: str, limit: int = 10) -> list:
    # Mock implementation
    return [{"id": 1, "name": f"Result for: {query}"}]

TOOL_HANDLERS = {
    "get_weather": get_weather,
    "search_database": search_database
}

def chat_with_tools(user_message: str, model: str = "llama3.1:8b") -> str:
    """Chat with tool calling support."""
    messages = [{"role": "user", "content": user_message}]

    response = ollama.chat(
        model=model,
        messages=messages,
        tools=tools,
        options={"num_ctx": 32768}  # Larger context improves tool calling
    )

    # Check if model wants to call a tool
    if response["message"].get("tool_calls"):
        for tool_call in response["message"]["tool_calls"]:
            func_name = tool_call["function"]["name"]
            func_args = tool_call["function"]["arguments"]

            # Execute tool
            if func_name in TOOL_HANDLERS:
                result = TOOL_HANDLERS[func_name](**func_args)

                # Add tool result to messages
                messages.append(response["message"])
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result)
                })

        # Get final response with tool results
        final_response = ollama.chat(
            model=model,
            messages=messages,
            tools=tools
        )
        return final_response["message"]["content"]

    return response["message"]["content"]

# Usage
result = chat_with_tools("What's the weather in Tokyo?")
print(result)
```

## Structured Outputs

```python
from pydantic import BaseModel
import ollama
import json

# Define output schema with Pydantic
class ProductReview(BaseModel):
    sentiment: str  # positive, negative, neutral
    score: float    # 0.0 to 1.0
    summary: str
    pros: list[str]
    cons: list[str]

def analyze_review(review_text: str, model: str = "llama3.1:8b") -> ProductReview:
    """Analyze a review and return structured data."""
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a review analyzer. Return your analysis as JSON."
            },
            {
                "role": "user",
                "content": f"Analyze this review:\n\n{review_text}"
            }
        ],
        format=ProductReview.model_json_schema()
    )

    # Parse response
    data = json.loads(response["message"]["content"])
    return ProductReview(**data)

# Usage
review = """
Great laptop! Fast performance, beautiful display, and excellent battery life.
The keyboard could be better though, and it runs a bit hot under load.
Overall, very satisfied with my purchase.
"""

analysis = analyze_review(review)
print(f"Sentiment: {analysis.sentiment}")
print(f"Score: {analysis.score}")
print(f"Pros: {analysis.pros}")
print(f"Cons: {analysis.cons}")
```

## OpenAI-Compatible API

```python
from openai import OpenAI

# Use OpenAI client with Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required but not used
)

# Chat completion
response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7
)
print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Tell me a joke"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## Vision Models

```python
import ollama
import base64

def analyze_image(image_path: str, prompt: str, model: str = "llava:7b") -> str:
    """Analyze an image with a vision model."""
    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [image_data]
            }
        ]
    )

    return response["message"]["content"]

# Usage
result = analyze_image(
    "/path/to/image.jpg",
    "What's in this image? Describe in detail."
)
print(result)
```

## Production Service Class

```python
from dataclasses import dataclass, field
from typing import Optional, Any
import logging
import time

@dataclass
class OllamaConfig:
    model: str = "llama3.1:8b"
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    num_ctx: int = 4096
    base_url: str = "http://localhost:11434"
    timeout: int = 120
    max_retries: int = 3

class OllamaService:
    """Production-ready Ollama service with error handling and retries."""

    def __init__(self, config: Optional[OllamaConfig] = None):
        self.config = config or OllamaConfig()
        self.logger = logging.getLogger(__name__)

    def is_available(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(
                f"{self.config.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False

    def list_models(self) -> list[str]:
        """Get available models."""
        response = requests.get(
            f"{self.config.base_url}/api/tags",
            timeout=10
        )
        response.raise_for_status()
        return [m["name"] for m in response.json().get("models", [])]

    def _make_request(
        self,
        endpoint: str,
        payload: dict
    ) -> dict:
        """Make request with retries."""
        last_error = None

        for attempt in range(self.config.max_retries):
            try:
                response = requests.post(
                    f"{self.config.base_url}{endpoint}",
                    json=payload,
                    timeout=self.config.timeout
                )
                response.raise_for_status()
                return response.json()

            except requests.exceptions.Timeout as e:
                last_error = e
                self.logger.warning(
                    f"Timeout on attempt {attempt + 1}/{self.config.max_retries}"
                )
                time.sleep(2 ** attempt)

            except requests.exceptions.RequestException as e:
                last_error = e
                self.logger.warning(
                    f"Request failed on attempt {attempt + 1}: {e}"
                )
                time.sleep(2 ** attempt)

        raise last_error

    def generate(
        self,
        prompt: str,
        system: str = "",
        **kwargs
    ) -> dict[str, Any]:
        """Generate completion with metrics."""
        options = {
            "temperature": kwargs.get("temperature", self.config.temperature),
            "top_p": kwargs.get("top_p", self.config.top_p),
            "top_k": kwargs.get("top_k", self.config.top_k),
            "num_ctx": kwargs.get("num_ctx", self.config.num_ctx)
        }

        start_time = time.time()

        data = self._make_request(
            "/api/generate",
            {
                "model": kwargs.get("model", self.config.model),
                "prompt": prompt,
                "system": system,
                "stream": False,
                "options": options
            }
        )

        elapsed = time.time() - start_time

        return {
            "content": data["response"],
            "model": data["model"],
            "done": data["done"],
            "total_duration_ms": data.get("total_duration", 0) / 1_000_000,
            "eval_count": data.get("eval_count", 0),
            "tokens_per_second": data.get("eval_count", 0) / elapsed if elapsed > 0 else 0
        }

    def chat(
        self,
        messages: list[dict],
        tools: Optional[list] = None,
        **kwargs
    ) -> dict[str, Any]:
        """Chat completion with optional tool support."""
        payload = {
            "model": kwargs.get("model", self.config.model),
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_ctx": kwargs.get("num_ctx", self.config.num_ctx)
            }
        }

        if tools:
            payload["tools"] = tools

        data = self._make_request("/api/chat", payload)

        return {
            "content": data["message"]["content"],
            "role": data["message"]["role"],
            "tool_calls": data["message"].get("tool_calls"),
            "model": data["model"]
        }

    def pull_model(self, model: str) -> bool:
        """Pull a model from Ollama library with progress logging."""
        try:
            response = requests.post(
                f"{self.config.base_url}/api/pull",
                json={"name": model},
                stream=True,
                timeout=3600  # 1 hour for large models
            )

            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    status = data.get("status", "")
                    self.logger.info(f"Pulling {model}: {status}")

                    if status == "success":
                        return True

            return False

        except Exception as e:
            self.logger.error(f"Failed to pull {model}: {e}")
            return False

# Usage
service = OllamaService(OllamaConfig(
    model="llama3.1:8b",
    temperature=0.7,
    num_ctx=8192
))

if service.is_available():
    result = service.generate("Hello!")
    print(f"Response: {result['content']}")
    print(f"Tokens/s: {result['tokens_per_second']:.1f}")
```
