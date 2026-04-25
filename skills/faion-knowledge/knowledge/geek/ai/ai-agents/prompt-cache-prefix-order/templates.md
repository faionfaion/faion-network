# Templates — Prompt-Cache Prefix Order

## Anthropic — explicit cache_control

```python
from anthropic import Anthropic
client = Anthropic()

system_prompt = [
    {
        "type": "text",
        "text": LONG_STABLE_SYSTEM_PROMPT,    # 5000 tokens
        "cache_control": {"type": "ephemeral"}
    }
]

tools = [
    {
        "name": "search_docs",
        "description": "...",
        "input_schema": {...},
        "cache_control": {"type": "ephemeral"}    # cache the tool block too
    },
    # other tools, no cache_control needed if part of same block
]

messages = [
    # conversation history (older, may be cacheable if stable)
    *history,
    # latest user message (NEVER cached — it's the volatile tip)
    {"role": "user", "content": user_message}
]

response = client.messages.create(
    model="claude-...",
    system=system_prompt,
    tools=tools,
    messages=messages,
    max_tokens=2048,
)

# Inspect savings
print(response.usage.cache_creation_input_tokens)  # first call: > 0
print(response.usage.cache_read_input_tokens)      # subsequent: > 0
```

## Anthropic — 1-hour TTL for batch

```python
system_prompt = [
    {
        "type": "text",
        "text": LONG_STABLE_SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral", "ttl": "1h"}
    }
]
```

## OpenAI Responses API — automatic + key

```python
response = openai.responses.create(
    model="gpt-...",
    instructions=LONG_STABLE_SYSTEM_PROMPT,
    tools=tools,
    input=user_message,
    prompt_cache_key="agent-v3-system-prompt"   # opt-in cache routing
)
```

## Gemini — explicit context caching

```python
from google import genai

client = genai.Client()

cached = client.caches.create(
    model="gemini-...",
    config={
        "contents": [LONG_STABLE_CONTEXT],
        "system_instruction": LONG_STABLE_SYSTEM,
        "ttl": "3600s"
    }
)

response = client.models.generate_content(
    model="gemini-...",
    contents=user_message,
    config={"cached_content": cached.name}
)
```

## Pattern: per-conversation cache + fresh user turn

```python
def chat_turn(history, user_msg):
    system = [{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}]
    return client.messages.create(
        model="claude-...",
        system=system,
        tools=TOOLS_WITH_CACHE,
        messages=[*history, {"role": "user", "content": user_msg}]
    )
```

## Pattern: codebase-as-context (large stable retrieval block)

```python
codebase_manifest = "\n".join(f"- {p}" for p in repo.iter_paths())  # 50K tokens

response = client.messages.create(
    system=[
        {"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}},
    ],
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": codebase_manifest, "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": user_question}
            ]
        }
    ],
    ...
)
```

The codebase manifest is cached separately from the system prompt. Both reused next call.

## Anti-template (don't do this)

```python
# BAD: user name interpolated in system prompt — cache breaks per user
system = f"You are an assistant for {user.name}. ..."

# BAD: tools defined AFTER user message — caches don't compose
messages = [{"role": "user", "content": "..."}]
tools = [...]
```
