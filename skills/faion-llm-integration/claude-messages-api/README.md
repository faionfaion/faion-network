# Claude Messages API

**Messages, Streaming, Vision**

---

## Messages API

### Basic Request

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

### Parameters

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,           # Required: max response tokens
    messages=[...],

    # Optional
    system="System prompt",    # Set behavior
    temperature=1.0,           # 0-1, higher = more creative
    top_p=0.9,                 # Nucleus sampling (alternative to temp)
    top_k=40,                  # Top-k sampling
    stop_sequences=["END"],    # Stop generation at these
    metadata={"user_id": "123"}  # Track requests
)
```

### Response Structure

```python
message = client.messages.create(...)

# Response object
print(message.id)              # "msg_01XFDUDYJgAACzvnptvVoYEL"
print(message.type)            # "message"
print(message.role)            # "assistant"
print(message.content)         # [ContentBlock(type="text", text="...")]
print(message.model)           # "claude-sonnet-4-20250514"
print(message.stop_reason)     # "end_turn" | "max_tokens" | "stop_sequence" | "tool_use"
print(message.stop_sequence)   # The stop sequence that triggered (if any)
print(message.usage)           # Usage(input_tokens=X, output_tokens=Y)
```

### Content Blocks

```python
for block in message.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "tool_use":
        print(f"Tool: {block.name}")
        print(f"Input: {block.input}")
```

---

## Vision (Images and PDFs)

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

### Multiple Images

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Compare these two designs:"},
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": image1_b64}
                },
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": image2_b64}
                }
            ]
        }
    ]
)
```

### PDF Support

```python
# PDFs are sent as documents (up to 100 pages)
pdf_data = encode_image("document.pdf")  # Same base64 encoding

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

### Supported Formats

| Format | Media Type | Max Size |
|--------|------------|----------|
| JPEG | `image/jpeg` | 20MB |
| PNG | `image/png` | 20MB |
| GIF | `image/gif` | 20MB |
| WebP | `image/webp` | 20MB |
| PDF | `application/pdf` | 32MB / 100 pages |

### Vision Best Practices

1. **Place images before text** for better understanding
2. **Use high resolution** for text extraction (OCR)
3. **Describe what you need** specifically
4. **Combine multiple images** for comparisons

---

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

### Collect Full Response

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    response = stream.get_final_message()
    print(response.content[0].text)
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

### Server-Sent Events Format

Raw SSE format for custom implementations:

```
event: message_start
data: {"type":"message_start","message":{...}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{...}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hello"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: message_stop
data: {"type":"message_stop"}
```

---

## Related Files

- [claude-api-basics.md](claude-api-basics.md) - Authentication, models, rate limiting
- [claude-advanced-features.md](claude-advanced-features.md) - Extended Thinking, Computer Use, Caching, Batch
- [claude-tool-use.md](claude-tool-use.md) - Tool use, function calling, structured output
- [claude-best-practices.md](claude-best-practices.md) - Best practices, optimization, patterns

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Message formatting | haiku | Protocol application |
| Streaming setup | sonnet | Real-time pattern |
| Vision capabilities | sonnet | Multimodal implementation |
