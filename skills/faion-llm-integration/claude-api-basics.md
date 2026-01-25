# Claude API Basics

**Authentication, Models, Rate Limiting, Token Counting, Cost Tracking**

---

## Authentication

### Setup

```bash
# Environment variable (recommended)
export ANTHROPIC_API_KEY="sk-ant-..."

# Or load from file
source ~/.secrets/anthropic  # Loads ANTHROPIC_API_KEY
```

### Headers

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json"
```

### Required Headers

| Header | Value | Purpose |
|--------|-------|---------|
| `x-api-key` | `sk-ant-...` | Authentication |
| `anthropic-version` | `2023-06-01` | API version |
| `content-type` | `application/json` | Request format |

### Optional Headers

| Header | Purpose |
|--------|---------|
| `anthropic-beta` | Enable beta features (e.g., `prompt-caching-2024-07-31`) |

---

## Models

### Available Models (2025-2026)

| Model | ID | Context | Input $/M | Output $/M | Best For |
|-------|-----|---------|-----------|------------|----------|
| **Claude Opus 4.5** | `claude-opus-4-5-20251101` | 200K | $15.00 | $75.00 | Complex reasoning, research |
| **Claude Sonnet 4** | `claude-sonnet-4-20250514` | 200K | $3.00 | $15.00 | Balanced (recommended) |
| **Claude Haiku 3.5** | `claude-3-5-haiku-20241022` | 200K | $0.80 | $4.00 | Fast, cost-effective |

### Model Selection Guide

| Task | Recommended Model | Why |
|------|-------------------|-----|
| General chat | claude-sonnet-4 | Best balance |
| Complex reasoning | claude-opus-4-5 | Highest capability |
| Code generation | claude-sonnet-4 | Fast, excellent coding |
| Quick classification | claude-3-5-haiku | Fastest, cheapest |
| Long documents | claude-sonnet-4 | Good 200K context |
| Extended thinking | claude-opus-4-5 | Deep reasoning |

### Legacy Models (Deprecated)

| Model | Status |
|-------|--------|
| claude-3-opus-20240229 | Replaced by Opus 4.5 |
| claude-3-sonnet-20240229 | Replaced by Sonnet 4 |
| claude-3-5-sonnet-20240620 | Replaced by Sonnet 4 |
| claude-3-haiku-20240307 | Replaced by Haiku 3.5 |

---

## Rate Limiting

### Limits

| Tier | Requests/min | Tokens/min | Tokens/day |
|------|--------------|------------|------------|
| **Tier 1** | 50 | 40,000 | 1,000,000 |
| **Tier 2** | 1,000 | 80,000 | 2,500,000 |
| **Tier 3** | 2,000 | 160,000 | 5,000,000 |
| **Tier 4** | 4,000 | 400,000 | 10,000,000 |

### Rate Limit Headers

```python
# Check headers in response
response = client.messages.with_raw_response.create(...)

print(response.headers.get("x-ratelimit-limit-requests"))
print(response.headers.get("x-ratelimit-remaining-requests"))
print(response.headers.get("x-ratelimit-reset-requests"))
print(response.headers.get("x-ratelimit-limit-tokens"))
print(response.headers.get("x-ratelimit-remaining-tokens"))
print(response.headers.get("x-ratelimit-reset-tokens"))
```

### Retry with Backoff

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

# Usage
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

---

## Error Handling

### Common Errors

| Error | HTTP Code | Cause | Solution |
|-------|-----------|-------|----------|
| `invalid_api_key` | 401 | Bad API key | Check ANTHROPIC_API_KEY |
| `rate_limit_error` | 429 | Too many requests | Implement backoff |
| `overloaded_error` | 529 | API overloaded | Retry with backoff |
| `invalid_request_error` | 400 | Bad parameters | Check request format |
| `not_found_error` | 404 | Invalid model | Check model name |
| `api_error` | 500 | Server issue | Retry with backoff |

### Error Response Structure

```python
try:
    response = client.messages.create(...)
except anthropic.BadRequestError as e:
    print(f"Status: {e.status_code}")
    print(f"Message: {e.message}")
    print(f"Type: {e.body.get('error', {}).get('type')}")
```

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

---

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

### With System and Tools

```python
count = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    system="You are a helpful assistant.",
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather?"}
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

---

## Cost Tracking

### Calculate Costs

```python
class ClaudeCostTracker:
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
        self.calls = []

    def track(self, model: str, usage) -> float:
        prices = self.PRICES.get(model, {"input": 0, "output": 0})
        cache_prices = self.CACHE_PRICES.get(model, {"write": 0, "read": 0})

        input_cost = usage.input_tokens * prices["input"] / 1_000_000
        output_cost = usage.output_tokens * prices["output"] / 1_000_000

        # Cache costs (if applicable)
        cache_write = getattr(usage, 'cache_creation_input_tokens', 0)
        cache_read = getattr(usage, 'cache_read_input_tokens', 0)
        cache_cost = (cache_write * cache_prices["write"] + cache_read * cache_prices["read"]) / 1_000_000

        total = input_cost + output_cost + cache_cost
        self.total_cost += total
        self.calls.append({"model": model, "cost": total})
        return total

    def report(self):
        print(f"Total cost: ${self.total_cost:.4f}")
        print(f"Total calls: {len(self.calls)}")

tracker = ClaudeCostTracker()

# Usage
response = client.messages.create(...)
cost = tracker.track(response.model, response.usage)
print(f"This call: ${cost:.4f}")
```

### Batch Cost Savings

```python
# Regular pricing
regular_cost = (input_tokens * 3.00 + output_tokens * 15.00) / 1_000_000

# Batch pricing (50% off)
batch_cost = regular_cost * 0.5

print(f"Saved: ${regular_cost - batch_cost:.4f}")
```

---

## Quick Commands

### curl Examples

```bash
# Basic message
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# With system prompt
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "system": "You are a helpful assistant.",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# Count tokens
curl https://api.anthropic.com/v1/messages/count_tokens \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### SDK Install

```bash
# Python
pip install anthropic

# Node.js
npm install @anthropic-ai/sdk
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

---

## Related Files

- [claude-messages-api.md](claude-messages-api.md) - Messages API, streaming, vision
- [claude-advanced-features.md](claude-advanced-features.md) - Extended Thinking, Computer Use, Caching, Batch
- [claude-tool-use.md](claude-tool-use.md) - Tool use, function calling, structured output
- [claude-best-practices.md](claude-best-practices.md) - Best practices, optimization, patterns
