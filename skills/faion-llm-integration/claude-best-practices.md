# Claude Best Practices

**Best Practices, Optimization Strategies, Prompt Engineering Patterns**

---

## Best Practices

### 1. Model Selection

| Task | Model | Reasoning |
|------|-------|-----------|
| Chat/general | Sonnet 4 | Best balance |
| Complex analysis | Opus 4.5 | Maximum capability |
| High volume | Haiku 3.5 | Cost-effective |
| Code generation | Sonnet 4 | Fast, accurate |

### 2. Prompt Engineering

```python
# Bad - vague
messages = [{"role": "user", "content": "Write something about AI"}]

# Good - specific
messages = [
    {
        "role": "user",
        "content": """Write a 200-word introduction about AI for developers.

Requirements:
- Focus on practical applications
- Include one Python code example
- Use technical but accessible language

Format: Markdown with code block"""
    }
]
```

### 3. System Prompts

```python
# Effective system prompt structure
system = """You are an expert SDD consultant.

Role: Help developers implement Specification-Driven Development

Behavior:
- Be concise and practical
- Use examples from real projects
- Provide actionable advice

Format:
- Use markdown for structure
- Include code examples when relevant
- Add links to resources when helpful"""
```

### 4. Tool Design

```python
# Good tool definition
{
    "name": "search_docs",
    "description": "Search Faion Network documentation. Use when user asks about SDD, agents, or skills.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (2-5 keywords)"
            },
            "category": {
                "type": "string",
                "enum": ["sdd", "agents", "skills", "methodology"],
                "description": "Documentation category"
            }
        },
        "required": ["query"]
    }
}
```

### 5. Cost Optimization

1. **Use caching** for repeated context
2. **Choose appropriate model** for task
3. **Use Batch API** for non-urgent work
4. **Set max_tokens** appropriately
5. **Pre-count tokens** for large inputs

---

## Optimization Strategies

### Prompt Caching Strategy

```python
# Structure prompts with cacheable prefix
system_with_cache = [
    {
        "type": "text",
        "text": """Long context that rarely changes:
- Product documentation (10K tokens)
- Codebase overview (5K tokens)
- Style guidelines (2K tokens)
""",
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": "Additional instructions that may change"
    }
]

# First call - creates cache
response1 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    betas=["prompt-caching-2024-07-31"],
    system=system_with_cache,
    messages=[{"role": "user", "content": "Question 1"}]
)

# Subsequent calls - use cache (90% savings)
response2 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    betas=["prompt-caching-2024-07-31"],
    system=system_with_cache,
    messages=[{"role": "user", "content": "Question 2"}]
)
```

### Batch Processing for Cost Savings

```python
# Prepare batch requests
batch_requests = []
for i, text in enumerate(texts_to_process):
    batch_requests.append({
        "custom_id": f"task-{i}",
        "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": f"Summarize: {text}"}]
        }
    })

# Submit batch (50% cost reduction)
batch = client.beta.messages.batches.create(requests=batch_requests)

# Poll for completion
while batch.processing_status != "ended":
    time.sleep(30)
    batch = client.beta.messages.batches.retrieve(batch.id)

# Collect results
for result in client.beta.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        print(f"{result.custom_id}: {result.result.message.content[0].text}")
```

### Token Optimization

```python
# Pre-count tokens to optimize
def optimize_prompt(prompt: str, max_tokens: int = 4000):
    count = client.messages.count_tokens(
        model="claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": prompt}]
    )

    if count.input_tokens > max_tokens:
        # Truncate or summarize
        words = prompt.split()
        truncated = " ".join(words[:int(len(words) * max_tokens / count.input_tokens)])
        return truncated

    return prompt

# Usage
optimized = optimize_prompt(long_prompt)
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": optimized}]
)
```

### Model Fallback Strategy

```python
def call_with_fallback(messages, max_retries=3):
    models = [
        "claude-sonnet-4-20250514",  # Try Sonnet first
        "claude-3-5-haiku-20241022"  # Fallback to Haiku if rate limited
    ]

    for model in models:
        for attempt in range(max_retries):
            try:
                return client.messages.create(
                    model=model,
                    max_tokens=1024,
                    messages=messages
                )
            except anthropic.RateLimitError:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                elif model != models[-1]:
                    break  # Try next model
                else:
                    raise

# Usage
response = call_with_fallback([
    {"role": "user", "content": "Hello"}
])
```

---

## Prompt Engineering Patterns

### Few-Shot Learning

```python
system = """You are a code reviewer. Analyze code and provide structured feedback."""

messages = [
    {
        "role": "user",
        "content": """Example 1:
Code: `def add(a, b): return a + b`
Feedback: Simple, correct. Consider type hints: `def add(a: int, b: int) -> int:`"""
    },
    {
        "role": "assistant",
        "content": "Understood. I'll provide concise feedback with specific improvements."
    },
    {
        "role": "user",
        "content": """Review this:
```python
def process(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
```"""
    }
]
```

### Chain of Thought

```python
# Trigger step-by-step reasoning
messages = [
    {
        "role": "user",
        "content": """Solve this problem step by step:

Problem: A train leaves station A at 60 mph. Another train leaves station B at 40 mph. Stations are 300 miles apart. When do they meet?

Show your work:
1. Define variables
2. Write equations
3. Solve step by step
4. Verify answer"""
    }
]

# For complex problems, use Extended Thinking
response = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 8000},
    messages=messages
)
```

### Output Formatting

```python
# Structured output with examples
messages = [
    {
        "role": "user",
        "content": """Extract user data and format as JSON array.

Example:
Input: "John (Developer), Sara (Designer)"
Output: [{"name": "John", "role": "Developer"}, {"name": "Sara", "role": "Designer"}]

Now process:
"Alice (Manager), Bob (Engineer), Charlie (Designer)"

Return only the JSON array."""
    }
]

# Or use tool for guaranteed structure
json_tool = {
    "name": "format_output",
    "input_schema": {
        "type": "object",
        "properties": {
            "users": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "role": {"type": "string"}
                    },
                    "required": ["name", "role"]
                }
            }
        },
        "required": ["users"]
    }
}
```

### Conversation Memory Pattern

```python
class ConversationManager:
    def __init__(self, system_prompt: str, max_history: int = 10):
        self.system = system_prompt
        self.messages = []
        self.max_history = max_history

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
        self._trim_history()

    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})
        self._trim_history()

    def _trim_history(self):
        # Keep only last N messages
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]

    def get_response(self) -> str:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system,
            messages=self.messages
        )
        self.add_assistant_message(response.content[0].text)
        return response.content[0].text

# Usage
conv = ConversationManager("You are a helpful assistant.")
conv.add_user_message("What is SDD?")
response1 = conv.get_response()

conv.add_user_message("How does it compare to TDD?")
response2 = conv.get_response()  # Has context from previous exchange
```

---

## Production Patterns

### Async Processing

```python
import asyncio
from anthropic import AsyncAnthropic

async_client = AsyncAnthropic()

async def process_batch(prompts: list[str]) -> list[str]:
    tasks = [
        async_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        for prompt in prompts
    ]

    responses = await asyncio.gather(*tasks)
    return [r.content[0].text for r in responses]

# Usage
prompts = ["Question 1", "Question 2", "Question 3"]
results = asyncio.run(process_batch(prompts))
```

### Error Recovery Pattern

```python
class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic()

    def create_with_retry(self, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return self.client.messages.create(**kwargs)
            except anthropic.RateLimitError:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise
            except anthropic.APIError as e:
                if e.status_code >= 500 and attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise

    def create_with_fallback(self, messages, **kwargs):
        # Try Sonnet first
        try:
            return self.create_with_retry(
                model="claude-sonnet-4-20250514",
                messages=messages,
                **kwargs
            )
        except anthropic.RateLimitError:
            # Fallback to Haiku
            return self.create_with_retry(
                model="claude-3-5-haiku-20241022",
                messages=messages,
                **kwargs
            )
```

### Logging and Monitoring

```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MonitoredClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.total_tokens = 0
        self.total_cost = 0.0

    def create(self, **kwargs):
        start = datetime.now()

        try:
            response = self.client.messages.create(**kwargs)

            # Track usage
            duration = (datetime.now() - start).total_seconds()
            self.total_tokens += response.usage.input_tokens + response.usage.output_tokens

            # Calculate cost
            cost = self._calculate_cost(kwargs["model"], response.usage)
            self.total_cost += cost

            # Log
            logger.info(f"Claude API call: {duration:.2f}s, {response.usage.input_tokens + response.usage.output_tokens} tokens, ${cost:.4f}")

            return response

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise

    def _calculate_cost(self, model, usage):
        prices = {
            "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
            "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
        }
        p = prices.get(model, {"input": 0, "output": 0})
        return (usage.input_tokens * p["input"] + usage.output_tokens * p["output"]) / 1_000_000
```

---

## Quick Reference

### API Endpoints

| API | Endpoint | Best Model | Use Case |
|-----|----------|------------|----------|
| **Messages** | `/v1/messages` | claude-sonnet-4 | Text generation, conversation |
| **Tool Use** | `/v1/messages` | claude-sonnet-4 | Function calling, structured output |
| **Vision** | `/v1/messages` | claude-sonnet-4 | Image/PDF understanding |
| **Extended Thinking** | `/v1/messages` | claude-opus-4-5 | Complex reasoning |
| **Computer Use** | `/v1/messages` | claude-sonnet-4 | Browser/desktop automation |
| **Batch** | `/v1/messages/batches` | All models | 50% cost savings |
| **Prompt Caching** | `/v1/messages` | All models | 90% cached input savings |
| **Token Counting** | `/v1/messages/count_tokens` | All models | Pre-flight token estimation |

---

## Related Files

- [claude-api-basics.md](claude-api-basics.md) - Authentication, models, rate limiting
- [claude-messages-api.md](claude-messages-api.md) - Messages API, streaming, vision
- [claude-advanced-features.md](claude-advanced-features.md) - Extended Thinking, Computer Use, Caching, Batch
- [claude-tool-use.md](claude-tool-use.md) - Tool use, function calling, structured output

## Sources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Anthropic API Reference](https://docs.anthropic.com/en/api)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [MCP Documentation](https://modelcontextprotocol.io/)
