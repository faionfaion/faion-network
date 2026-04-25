# Examples — Prompt-Cache Prefix Order

## Example 1: Agent loop, 10 turns

System prompt: 5,000 tokens. Tools: 2,000 tokens. Each user message: ~200 tokens. Each model output: ~500 tokens.

Without caching: each turn costs 5,000 + 2,000 + 200 input + 500 output ≈ 7,700 input tokens + 500 output, every turn.

With caching after turn 1: 5,000 + 2,000 cached at 10% rate, plus history + 200 + 500. Cached portion drops from 7,000 input × normal rate to 7,000 input × 10% rate.

10-turn savings: ~$0.20 per session at GPT-4o rates → cents per session at Sonnet-prefix cached.

## Example 2: Codebase Q&A

70K-token codebase manifest. Without caching, every question pays 70K × normal rate. With caching, first question creates the cache (1.25× normal write rate), all subsequent in 5 min pay 0.10× rate.

3 questions in 5 min:
- Without: 3 × 70K = 210K paid
- With: 1 × 70K × 1.25 + 2 × 70K × 0.10 = 87.5K + 14K = 101.5K — half the cost

10 questions in 5 min:
- Without: 700K
- With: 70K × 1.25 + 9 × 70K × 0.10 = 87.5K + 63K = 150.5K — 78% saved

## Example 3: Claude Code session

Claude Code system prompt + skills + tool definitions ≈ 25K tokens. The CLI sets cache_control on the system block automatically. Every tool call after the first reads from cache.

## Example 4: Anti-example — name interpolation

```python
system = f"You are NERO, helping {user_name} with their tasks."
```

Cache hit rate: 0% across users. Each user's first call pays full price every time.

Fix:
```python
system = "You are NERO. The user's name is in their first message; address them by it."
```

Now the system prompt is universal and cacheable.

## Example 5: Anti-example — version string

```python
system = f"NERO version {VERSION_STRING}. ..."
```

If `VERSION_STRING` changes when you deploy, every deploy invalidates the cache for every user. Either pin the system prompt or move the version into a side channel.

## Example 6: 1-hour TTL for batch processing

Processing 10,000 documents in a 30-minute batch. Default 5-min TTL means the cache rewrites ~6 times. Setting `ttl: "1h"` keeps it warm for the whole batch.

## Example 7: Multiple cache breakpoints (legitimate use)

```python
system = [
    {"type": "text", "text": ROLE_PROMPT, "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": COMPANY_KNOWLEDGE, "cache_control": {"type": "ephemeral"}},
]
```

ROLE_PROMPT changes rarely; COMPANY_KNOWLEDGE changes on knowledge updates. Two breakpoints let you invalidate one without the other.

## Example 8: Cache verification

```python
print({
    "cached_read": response.usage.cache_read_input_tokens,
    "cached_create": response.usage.cache_creation_input_tokens,
    "fresh_input": response.usage.input_tokens,
})
# After warm-up, expect cached_read > 0 and cached_create == 0
```

If cached_read stays 0 in a hot loop, your prefix is volatile — diff prefix bytes between calls.
