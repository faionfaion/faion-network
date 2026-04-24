# OpenAI Chat Completions API

**Complete guide to Chat Completions, models, streaming, and vision**

---

## Quick Reference

| Feature | Endpoint | Best Model |
|---------|----------|------------|
| **Chat** | `/v1/chat/completions` | gpt-4o |
| **Vision** | `/v1/chat/completions` | gpt-4o |
| **Streaming** | `/v1/chat/completions` (stream=true) | gpt-4o |

---

## Authentication

### Setup

```bash
# Environment variable (recommended)
export OPENAI_API_KEY="sk-proj-..."

# Or load from file
source ~/.secrets/openai  # Loads OPENAI_API_KEY
```

### API Key Types

| Type | Prefix | Scope |
|------|--------|-------|
| **Project Key** | `sk-proj-` | Single project, recommended |
| **User Key** | `sk-` | All projects (legacy) |
| **Service Account** | `sk-svcacct-` | Automated systems |

### Headers

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -H "OpenAI-Organization: org-xxxxx" \  # Optional
  -H "OpenAI-Project: proj-xxxxx"         # Optional
```

---

## Chat Completions API

### Basic Request

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain SDD methodology in 3 sentences."}
    ]
)

print(response.choices[0].message.content)
```

### Models

| Model | Context | Input $/M | Output $/M | Best For |
|-------|---------|-----------|------------|----------|
| **gpt-4o** | 128K | $2.50 | $10.00 | General purpose, best quality |
| **gpt-4o-mini** | 128K | $0.15 | $0.60 | Cost-effective, fast |
| **gpt-4o-audio-preview** | 128K | $2.50 | $10.00 | Audio input/output |
| **gpt-4-turbo** | 128K | $10.00 | $30.00 | Legacy, replaced by 4o |
| **o1** | 128K | $15.00 | $60.00 | Complex reasoning |
| **o1-mini** | 128K | $1.10 | $4.40 | Reasoning, lower cost |
| **o3-mini** | 200K | $1.10 | $4.40 | Latest reasoning model |

### Parameters

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],

    # Generation
    temperature=0.7,        # 0-2, higher = more creative
    top_p=1.0,              # Nucleus sampling (alternative to temp)
    max_tokens=4096,        # Max response length
    n=1,                    # Number of completions

    # Control
    stop=["\n\n", "END"],   # Stop sequences
    presence_penalty=0.0,   # -2 to 2, penalize repeated topics
    frequency_penalty=0.0,  # -2 to 2, penalize repeated tokens

    # Format
    response_format={"type": "json_object"},  # Force JSON output
    seed=42,                # Deterministic outputs

    # Advanced
    logprobs=True,          # Return token probabilities
    top_logprobs=5,         # Number of logprobs per position
    user="user-123"         # Track abuse
)
```

### Streaming

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a poem"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Message Roles

| Role | Purpose |
|------|---------|
| **system** | Set behavior, persona, instructions |
| **user** | User input |
| **assistant** | Model responses (for context) |
| **tool** | Tool/function results |

---

## Vision API

### Image from URL

```python
response = client.chat.completions.create(
    model="gpt-4o",
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
    ]
)
```

### Image from Base64

```python
import base64

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

image_data = encode_image("screenshot.png")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this screenshot"},
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
```

### Multiple Images

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Compare these two designs"},
                {"type": "image_url", "image_url": {"url": "https://example.com/design1.png"}},
                {"type": "image_url", "image_url": {"url": "https://example.com/design2.png"}}
            ]
        }
    ]
)
```

### Detail Levels

| Level | Tokens | Best For |
|-------|--------|----------|
| **low** | 85 | Quick overview, thumbnails |
| **high** | 85-1105+ | OCR, detailed analysis |
| **auto** | Varies | Model decides |

### Vision Limitations

- Max 20MB per image
- Supported: PNG, JPEG, GIF, WebP
- No video (extract frames)
- May struggle with: rotated text, small text, spatial reasoning

---

## Error Handling

### Common Errors

| Error | HTTP Code | Cause | Solution |
|-------|-----------|-------|----------|
| `invalid_api_key` | 401 | Bad API key | Check OPENAI_API_KEY |
| `rate_limit_exceeded` | 429 | Too many requests | Implement exponential backoff |
| `insufficient_quota` | 429 | Usage limit reached | Add credits or wait for reset |
| `model_not_found` | 404 | Invalid model name | Check available models |
| `context_length_exceeded` | 400 | Too many tokens | Reduce input or use larger context model |
| `server_error` | 500 | OpenAI issue | Retry with backoff |

### Retry with Backoff

```python
import time
from openai import RateLimitError, APIError

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

# Usage
response = call_with_retry(
    lambda: client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
)
```

### Using tenacity Library

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import RateLimitError, APIError

@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5)
)
def make_request():
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
```

---

## Rate Limiting

### Limits by Tier

| Tier | RPM | TPM | Daily |
|------|-----|-----|-------|
| **Free** | 3 | 200 | Limited |
| **Tier 1** | 500 | 30,000 | $100 |
| **Tier 2** | 5,000 | 450,000 | $500 |
| **Tier 3** | 5,000 | 800,000 | $1,000 |
| **Tier 4** | 10,000 | 2,000,000 | $5,000 |
| **Tier 5** | 10,000 | 10,000,000 | $50,000 |

### Check Rate Limit Headers

```python
response = client.chat.completions.with_raw_response.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hi"}]
)

# Access headers
print(f"Requests remaining: {response.headers.get('x-ratelimit-remaining-requests')}")
print(f"Tokens remaining: {response.headers.get('x-ratelimit-remaining-tokens')}")
print(f"Reset in: {response.headers.get('x-ratelimit-reset-requests')}")
```

---

## Cost Tracking

### Token Counting

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Count message tokens
messages = [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello world!"}
]

total = sum(count_tokens(m["content"]) for m in messages)
total += 3  # Overhead per message
print(f"Input tokens: {total}")
```

### Usage from Response

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

usage = response.usage
print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Calculate cost
input_cost = usage.prompt_tokens * 2.50 / 1_000_000
output_cost = usage.completion_tokens * 10.00 / 1_000_000
total_cost = input_cost + output_cost
print(f"Cost: ${total_cost:.6f}")
```

---

## Best Practices

### 1. Model Selection

| Task | Recommended Model | Why |
|------|-------------------|-----|
| General chat | gpt-4o-mini | Cost-effective |
| Complex reasoning | gpt-4o or o1 | Better accuracy |
| Code generation | gpt-4o | Strong coding |
| Quick classification | gpt-4o-mini | Fast, cheap |

### 2. Prompt Engineering

```python
# Bad
messages = [{"role": "user", "content": "Write something about AI"}]

# Good
messages = [
    {
        "role": "system",
        "content": "You are a technical writer specializing in AI. Write clear, concise content for developers."
    },
    {
        "role": "user",
        "content": """Write a 200-word introduction about AI for a developer audience.

Requirements:
- Focus on practical applications
- Include one code example
- Use simple language"""
    }
]
```

### 3. Parallel Requests

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def parallel_completions(prompts: list[str]) -> list:
    async def get_completion(prompt):
        return await async_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

    return await asyncio.gather(*[get_completion(p) for p in prompts])

# Usage
prompts = ["Hello", "World", "!"]
responses = asyncio.run(parallel_completions(prompts))
```

---

## Quick Commands

### curl Examples

```bash
# Chat completion
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## Related

- [openai-function-calling.md](openai-function-calling.md) - Tool use and structured outputs
- [openai-embeddings.md](openai-embeddings.md) - Text embeddings
- [openai-assistants.md](openai-assistants.md) - Assistants API

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Chat format usage | haiku | API usage |
| Temperature tuning | sonnet | Quality optimization |
