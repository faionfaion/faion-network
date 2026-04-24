# Claude API Examples

Code examples for Claude API integration.

## Messages API

### Basic Request (Python)

```python
import anthropic

client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain SDD methodology in 3 sentences."}
    ]
)

print(message.content[0].text)
```

### With System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are an expert on Specification-Driven Development. Be concise and practical.",
    messages=[
        {"role": "user", "content": "What are the key phases of SDD?"}
    ]
)
```

### Multi-turn Conversation

```python
messages = [
    {"role": "user", "content": "What is SDD?"},
    {"role": "assistant", "content": "SDD (Specification-Driven Development) is a methodology..."},
    {"role": "user", "content": "How does it compare to TDD?"}
]

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages
)
```

### TypeScript Example

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const message = await client.messages.create({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Hello!" }
  ]
});

console.log(message.content[0].text);
```

### curl Example

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Tool Use

### Define Tools

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location. Call this when user asks about weather.",
        "input_schema": {
            "type": "object",
            "properties": {
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
            "required": ["location"]
        }
    }
]
```

### Complete Tool Loop

```python
import json

def get_weather(location: str, unit: str = "celsius") -> dict:
    # Your implementation
    return {"temperature": 15, "condition": "cloudy", "unit": unit}

# Initial request
messages = [{"role": "user", "content": "What's the weather in Kyiv?"}]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

# Process tool calls
while response.stop_reason == "tool_use":
    # Add assistant message with tool use
    messages.append({"role": "assistant", "content": response.content})

    # Process each tool use
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = get_weather(**block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result)
            })

    # Add tool results
    messages.append({"role": "user", "content": tool_results})

    # Continue conversation
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

# Final response
print(response.content[0].text)
```

### Force Tool Use (Structured Output)

```python
json_tool = {
    "name": "output_json",
    "description": "Output the result as structured JSON",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["name", "age"]
    }
}

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[json_tool],
    tool_choice={"type": "tool", "name": "output_json"},
    messages=[
        {"role": "user", "content": "Extract: John Doe, 30, john@example.com"}
    ]
)

# Get structured data
tool_use = next(b for b in message.content if b.type == "tool_use")
data = tool_use.input  # {"name": "John Doe", "age": 30, "email": "john@example.com"}
```

### Handle Tool Errors

```python
# Success result
tool_result = {
    "type": "tool_result",
    "tool_use_id": "toolu_01...",
    "content": json.dumps({"temperature": 15})
}

# Error result
tool_result = {
    "type": "tool_result",
    "tool_use_id": "toolu_01...",
    "is_error": True,
    "content": "Error: Location not found"
}
```

## Extended Thinking

### Enable Extended Thinking

```python
message = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Max tokens for thinking
    },
    messages=[
        {"role": "user", "content": "Solve this step by step: If a train leaves..."}
    ]
)
```

### Access Thinking Content

```python
for block in message.content:
    if block.type == "thinking":
        print("Thinking:", block.thinking)
    elif block.type == "text":
        print("Answer:", block.text)
```

### Interleaved Thinking with Tools (Beta)

```python
# Add beta header for interleaved thinking
message = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    betas=["interleaved-thinking-2025-05-14"],
    thinking={
        "type": "enabled",
        "budget_tokens": 5000
    },
    tools=tools,
    messages=[
        {"role": "user", "content": "Calculate the weather impact on travel time to Kyiv"}
    ]
)
```

## Streaming

### Basic Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a poem about AI"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Event-Based Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            print(f"Block started: {event.content_block.type}")
        elif event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
        elif event.type == "message_stop":
            print("\n[Complete]")
```

### Stream with Tools

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Kyiv?"}]
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "tool_use":
                print(f"Tool: {event.content_block.name}")
        elif event.type == "content_block_delta":
            if event.delta.type == "input_json_delta":
                print(event.delta.partial_json, end="")
```

### Async Streaming

```python
import asyncio

async def stream_response():
    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

asyncio.run(stream_response())
```

### Stream Extended Thinking

```python
with client.messages.stream(
    model="claude-opus-4-5-20251101",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 5000},
    messages=[{"role": "user", "content": "Solve: x^2 + 5x + 6 = 0"}]
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(f"[Thinking] {event.delta.thinking}", end="")
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="")
```

## Vision

### Image from Base64

```python
import base64

def encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

image_data = encode_image("screenshot.png")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "Describe this screenshot"
                }
            ]
        }
    ]
)
```

### Image from URL

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://example.com/image.jpg"
                    }
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ]
        }
    ]
)
```

### PDF Support

```python
pdf_data = encode_image("document.pdf")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {
                    "type": "text",
                    "text": "Summarize this document"
                }
            ]
        }
    ]
)
```

## Prompt Caching

### Enable Caching

```python
message = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    betas=["prompt-caching-2024-07-31"],
    system=[
        {
            "type": "text",
            "text": "You are an expert on Faion Network and SDD methodology. [Long system prompt...]",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "What is SDD?"}
    ]
)

# Check cache usage
print(f"Cache creation: {message.usage.cache_creation_input_tokens}")
print(f"Cache read: {message.usage.cache_read_input_tokens}")
```

### Cache Long Context

```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Here is a long document: [10K tokens...]",
                "cache_control": {"type": "ephemeral"}
            }
        ]
    }
]
```

## Batch API

### Create Batch

```python
requests = [
    {
        "custom_id": "req-001",
        "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Hello!"}]
        }
    },
    {
        "custom_id": "req-002",
        "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "World!"}]
        }
    }
]

batch = client.beta.messages.batches.create(requests=requests)
print(f"Batch ID: {batch.id}")
```

### Check Status and Get Results

```python
batch = client.beta.messages.batches.retrieve(batch.id)

if batch.processing_status == "ended":
    for result in client.beta.messages.batches.results(batch.id):
        print(f"ID: {result.custom_id}")
        if result.result.type == "succeeded":
            print(f"Response: {result.result.message.content[0].text}")
        else:
            print(f"Error: {result.result.error}")
```

## Error Handling

### Handle Specific Errors

```python
import anthropic

try:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except anthropic.AuthenticationError:
    print("Invalid API key")
except anthropic.RateLimitError:
    print("Rate limited - wait and retry")
except anthropic.BadRequestError as e:
    print(f"Bad request: {e.message}")
except anthropic.APIStatusError as e:
    print(f"API error: {e.status_code}")
```

### Retry with Exponential Backoff

```python
import time
from anthropic import RateLimitError, APIError

def call_with_retry(func, max_retries=5, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)
        except APIError as e:
            if e.status_code >= 500:
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2 ** attempt)
                print(f"Server error. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise

response = call_with_retry(
    lambda: client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
)
```

### Using tenacity

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from anthropic import RateLimitError, APIError

@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5)
)
def make_request():
    return client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
```

## Token Counting

### Pre-count Tokens

```python
count = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

print(f"Input tokens: {count.input_tokens}")
```

### Usage from Response

```python
response = client.messages.create(...)

print(f"Input: {response.usage.input_tokens}")
print(f"Output: {response.usage.output_tokens}")
print(f"Cache creation: {getattr(response.usage, 'cache_creation_input_tokens', 0)}")
print(f"Cache read: {getattr(response.usage, 'cache_read_input_tokens', 0)}")
```
