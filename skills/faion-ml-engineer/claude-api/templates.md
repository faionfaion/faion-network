# Claude API Templates

Reusable templates for common Claude API patterns.

## Client Setup

### Python Client

```python
import anthropic
import os

# Initialize client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Async client
async_client = anthropic.AsyncAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
```

### TypeScript Client

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

## Messages API Templates

### Basic Request Template

```python
def create_message(
    prompt: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024,
    system: str | None = None,
    temperature: float = 1.0
) -> str:
    """Create a basic Claude message."""
    params = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
```

### Conversation Template

```python
class ClaudeConversation:
    """Manage multi-turn conversations with Claude."""

    def __init__(
        self,
        model: str = "claude-sonnet-4-20250514",
        system: str | None = None,
        max_tokens: int = 1024
    ):
        self.model = model
        self.system = system
        self.max_tokens = max_tokens
        self.messages: list[dict] = []

    def send(self, user_message: str) -> str:
        """Send a message and get response."""
        self.messages.append({"role": "user", "content": user_message})

        params = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": self.messages,
        }
        if self.system:
            params["system"] = self.system

        response = client.messages.create(**params)
        assistant_message = response.content[0].text

        self.messages.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def clear(self):
        """Clear conversation history."""
        self.messages = []
```

## Tool Use Templates

### Tool Definition Template

```python
def create_tool(
    name: str,
    description: str,
    properties: dict,
    required: list[str] | None = None
) -> dict:
    """Create a tool definition."""
    return {
        "name": name,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required or []
        }
    }

# Example usage
weather_tool = create_tool(
    name="get_weather",
    description="Get current weather for a location",
    properties={
        "location": {
            "type": "string",
            "description": "City name, e.g., 'Kyiv, Ukraine'"
        },
        "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "description": "Temperature unit"
        }
    },
    required=["location"]
)
```

### Tool Executor Template

```python
import json
from typing import Callable, Any

class ToolExecutor:
    """Execute tools called by Claude."""

    def __init__(self):
        self.tools: dict[str, dict] = {}
        self.handlers: dict[str, Callable] = {}

    def register(self, tool: dict, handler: Callable):
        """Register a tool and its handler."""
        self.tools[tool["name"]] = tool
        self.handlers[tool["name"]] = handler

    def get_tools(self) -> list[dict]:
        """Get all registered tools."""
        return list(self.tools.values())

    def execute(self, tool_name: str, tool_input: dict) -> dict:
        """Execute a tool and return result."""
        if tool_name not in self.handlers:
            return {"error": f"Unknown tool: {tool_name}"}

        try:
            result = self.handlers[tool_name](**tool_input)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

    def process_response(self, response) -> list[dict]:
        """Process tool use blocks and return results."""
        results = []
        for block in response.content:
            if block.type == "tool_use":
                result = self.execute(block.name, block.input)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                    "is_error": "error" in result
                })
        return results
```

### Complete Tool Loop Template

```python
def run_with_tools(
    prompt: str,
    tools: list[dict],
    tool_executor: ToolExecutor,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024,
    max_iterations: int = 10
) -> str:
    """Run a conversation with tool use."""
    messages = [{"role": "user", "content": prompt}]

    for _ in range(max_iterations):
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            tools=tools,
            messages=messages
        )

        if response.stop_reason != "tool_use":
            # Final response
            return response.content[0].text

        # Add assistant response
        messages.append({"role": "assistant", "content": response.content})

        # Process tools and add results
        tool_results = tool_executor.process_response(response)
        messages.append({"role": "user", "content": tool_results})

    raise RuntimeError("Max iterations reached")
```

## Extended Thinking Template

```python
def think_and_respond(
    prompt: str,
    budget_tokens: int = 5000,
    model: str = "claude-opus-4-5-20251101",
    max_tokens: int = 16000
) -> tuple[str, str]:
    """Get response with extended thinking."""
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        thinking={
            "type": "enabled",
            "budget_tokens": budget_tokens
        },
        messages=[{"role": "user", "content": prompt}]
    )

    thinking = ""
    answer = ""

    for block in message.content:
        if block.type == "thinking":
            thinking = block.thinking
        elif block.type == "text":
            answer = block.text

    return thinking, answer
```

## Streaming Templates

### Text Streaming Template

```python
def stream_response(
    prompt: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024,
    on_text: Callable[[str], None] | None = None
) -> str:
    """Stream a response with optional callback."""
    full_text = ""

    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            full_text += text
            if on_text:
                on_text(text)

    return full_text

# Usage
response = stream_response(
    "Write a poem",
    on_text=lambda t: print(t, end="", flush=True)
)
```

### Async Streaming Template

```python
async def async_stream_response(
    prompt: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024
) -> str:
    """Async stream a response."""
    full_text = ""

    async with async_client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        async for text in stream.text_stream:
            full_text += text
            yield text

    return full_text
```

## Vision Template

```python
import base64
from pathlib import Path

def analyze_image(
    image_path: str | Path,
    prompt: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024
) -> str:
    """Analyze an image with Claude."""
    path = Path(image_path)

    # Determine media type
    suffix_to_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".pdf": "application/pdf"
    }
    media_type = suffix_to_type.get(path.suffix.lower(), "image/png")
    content_type = "document" if path.suffix.lower() == ".pdf" else "image"

    # Encode image
    with open(path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": content_type,
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {"type": "text", "text": prompt}
                ]
            }
        ]
    )

    return message.content[0].text
```

## Prompt Caching Template

```python
class CachedConversation:
    """Conversation with cached system prompt."""

    def __init__(
        self,
        system_prompt: str,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 1024
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.system = [
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}
            }
        ]
        self.messages: list[dict] = []
        self.total_cache_read = 0
        self.total_cache_write = 0

    def send(self, user_message: str) -> str:
        """Send message with cached system prompt."""
        self.messages.append({"role": "user", "content": user_message})

        response = client.beta.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            betas=["prompt-caching-2024-07-31"],
            system=self.system,
            messages=self.messages
        )

        # Track cache usage
        self.total_cache_read += getattr(response.usage, 'cache_read_input_tokens', 0)
        self.total_cache_write += getattr(response.usage, 'cache_creation_input_tokens', 0)

        assistant_message = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message
```

## Batch Processing Template

```python
from typing import Iterator

class BatchProcessor:
    """Process multiple requests via Batch API."""

    def __init__(self, model: str = "claude-sonnet-4-20250514", max_tokens: int = 1024):
        self.model = model
        self.max_tokens = max_tokens

    def create_batch(self, prompts: list[str]) -> str:
        """Create a batch from prompts."""
        requests = [
            {
                "custom_id": f"req-{i:04d}",
                "params": {
                    "model": self.model,
                    "max_tokens": self.max_tokens,
                    "messages": [{"role": "user", "content": prompt}]
                }
            }
            for i, prompt in enumerate(prompts)
        ]

        batch = client.beta.messages.batches.create(requests=requests)
        return batch.id

    def wait_for_completion(self, batch_id: str, poll_interval: int = 10) -> dict:
        """Wait for batch completion."""
        import time

        while True:
            batch = client.beta.messages.batches.retrieve(batch_id)
            if batch.processing_status == "ended":
                return {
                    "succeeded": batch.request_counts.succeeded,
                    "errored": batch.request_counts.errored
                }
            time.sleep(poll_interval)

    def get_results(self, batch_id: str) -> Iterator[tuple[str, str | None]]:
        """Get batch results as (custom_id, response) pairs."""
        for result in client.beta.messages.batches.results(batch_id):
            if result.result.type == "succeeded":
                yield result.custom_id, result.result.message.content[0].text
            else:
                yield result.custom_id, None
```

## Cost Tracking Template

```python
class CostTracker:
    """Track API costs."""

    PRICES = {
        "claude-opus-4-5-20251101": {"input": 15.00, "output": 75.00},
        "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
        "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    }

    CACHE_PRICES = {
        "claude-opus-4-5-20251101": {"write": 18.75, "read": 1.50},
        "claude-sonnet-4-20250514": {"write": 3.75, "read": 0.30},
        "claude-3-5-haiku-20241022": {"write": 1.00, "read": 0.08},
    }

    def __init__(self):
        self.total_cost = 0.0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.call_count = 0

    def track(self, model: str, usage) -> float:
        """Track cost from a response."""
        prices = self.PRICES.get(model, {"input": 0, "output": 0})
        cache_prices = self.CACHE_PRICES.get(model, {"write": 0, "read": 0})

        input_cost = usage.input_tokens * prices["input"] / 1_000_000
        output_cost = usage.output_tokens * prices["output"] / 1_000_000

        cache_write = getattr(usage, 'cache_creation_input_tokens', 0)
        cache_read = getattr(usage, 'cache_read_input_tokens', 0)
        cache_cost = (cache_write * cache_prices["write"] + cache_read * cache_prices["read"]) / 1_000_000

        cost = input_cost + output_cost + cache_cost

        self.total_cost += cost
        self.total_input_tokens += usage.input_tokens
        self.total_output_tokens += usage.output_tokens
        self.call_count += 1

        return cost

    def report(self) -> dict:
        """Get cost report."""
        return {
            "total_cost": f"${self.total_cost:.4f}",
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "call_count": self.call_count,
            "avg_cost_per_call": f"${self.total_cost / max(self.call_count, 1):.4f}"
        }
```

## Error Handling Template

```python
import time
from functools import wraps
from typing import TypeVar, Callable
import anthropic

T = TypeVar('T')

def with_retry(
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for retry with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except anthropic.RateLimitError:
                    if attempt == max_retries - 1:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    time.sleep(delay)
                except anthropic.APIError as e:
                    if e.status_code >= 500:
                        if attempt == max_retries - 1:
                            raise
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        time.sleep(delay)
                    else:
                        raise
            raise RuntimeError("Max retries exceeded")
        return wrapper
    return decorator

# Usage
@with_retry(max_retries=5)
def make_request(prompt: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```
