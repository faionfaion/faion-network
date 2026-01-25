# Claude Advanced Features

Extended Thinking, Computer Use, Prompt Caching, Batch API

---

## Extended Thinking

Claude shows reasoning process for complex problems.

### Basic Usage

```python
message = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{"role": "user", "content": "Solve step by step: If a train..."}]
)

# Access thinking
for block in message.content:
    if block.type == "thinking":
        print("Thinking:", block.thinking)
    elif block.type == "text":
        print("Answer:", block.text)
```

### Use Cases

| Use Case | Benefit |
|----------|---------|
| Math problems | Step-by-step reasoning |
| Logic puzzles | Explicit deduction |
| Code debugging | Trace through logic |
| Strategic planning | Consider alternatives |

### Best Practices

- Budget 5K-10K tokens for most problems
- Ask "step by step" to trigger deeper thinking
- Use for complex problems only
- Review thinking quality

---

## Computer Use

Control computer via screenshots and actions.

### Available Tools

| Tool | Purpose |
|------|---------|
| `computer` | Screen interaction (screenshot, click, type) |
| `text_editor` | File editing |
| `bash` | Shell commands |

### Computer Tool Setup

```python
computer_tool = {
    "type": "computer_20241022",
    "name": "computer",
    "display_width_px": 1920,
    "display_height_px": 1080,
    "display_number": 1
}

message = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=[computer_tool],
    betas=["computer-use-2024-10-22"],
    messages=[{"role": "user", "content": "Open Chrome and search for SDD"}]
)
```

### Handle Actions

```python
for block in message.content:
    if block.type == "tool_use" and block.name == "computer":
        action = block.input["action"]

        if action == "screenshot":
            screenshot = take_screenshot()
        elif action == "mouse_move":
            x, y = block.input["coordinate"]
            move_mouse(x, y)
        elif action == "left_click":
            click()
        elif action == "type":
            type_text(block.input["text"])
        elif action == "key":
            press_key(block.input["key"])
```

### Safety

1. Use VMs or containers
2. Limited permissions (no sudo)
3. Network isolation if needed
4. Human oversight
5. Timeout limits

---

## Prompt Caching

90% cost reduction on cached input tokens.

### Enable Caching

```python
message = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    betas=["prompt-caching-2024-07-31"],
    system=[
        {
            "type": "text",
            "text": "Long system prompt...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Question"}]
)

# Check usage
print(f"Cache creation: {message.usage.cache_creation_input_tokens}")
print(f"Cache read: {message.usage.cache_read_input_tokens}")
```

### Cacheable Content

```python
# System prompt
system = [
    {"type": "text", "text": "Long instructions...", "cache_control": {"type": "ephemeral"}}
]

# Messages with context
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Long document...", "cache_control": {"type": "ephemeral"}}
        ]
    }
]

# Tool definitions
tools = [
    {
        "name": "tool",
        "description": "...",
        "input_schema": {...},
        "cache_control": {"type": "ephemeral"}
    }
]
```

### Cache Pricing

| Model | Cache Write | Cache Read | Savings |
|-------|-------------|------------|---------|
| Opus 4.5 | $18.75/M | $1.50/M | 90% |
| Sonnet 4 | $3.75/M | $0.30/M | 90% |
| Haiku 3.5 | $1.00/M | $0.08/M | 90% |

### Cache Behavior

- TTL: 5 minutes (extends on use)
- Minimum: 1024 tokens
- Prefix matching required
- Org-scoped cache

---

## Batch API

50% cost reduction for non-urgent workloads.

### Create Batch

```python
requests = [
    {
        "custom_id": "req-001",
        "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Hello"}]
        }
    }
]

batch = client.beta.messages.batches.create(requests=requests)
print(f"Batch ID: {batch.id}")
```

### Check Status

```python
batch = client.beta.messages.batches.retrieve(batch.id)
print(f"Status: {batch.processing_status}")
print(f"Succeeded: {batch.request_counts.succeeded}")
print(f"Errored: {batch.request_counts.errored}")
```

### Get Results

```python
if batch.processing_status == "ended":
    for result in client.beta.messages.batches.results(batch.id):
        if result.result.type == "succeeded":
            print(result.result.message.content[0].text)
        else:
            print(f"Error: {result.result.error}")
```

### Batch Pricing

| Model | Regular | Batch (50% off) |
|-------|---------|-----------------|
| Opus 4.5 | $15/$75 | $7.50/$37.50 |
| Sonnet 4 | $3/$15 | $1.50/$7.50 |
| Haiku 3.5 | $0.80/$4 | $0.40/$2 |

### Use Cases

- Content generation (blogs, translations)
- Data processing (classification, extraction)
- Analysis (review, summarization)
- Testing (evaluation, benchmarks)

---

## Sources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Extended Thinking Guide](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Computer Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/computer-use)
- [Prompt Caching Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Batch API Reference](https://docs.anthropic.com/en/api/messages-batches)
