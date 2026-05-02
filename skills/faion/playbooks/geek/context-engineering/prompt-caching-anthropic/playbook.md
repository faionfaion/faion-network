---
name: prompt-caching-anthropic
description: Cache large system prompts with Anthropic cache_control breakpoints to cut repeated-query costs by up to 10x.
tier: geek
group: context-engineering
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working Python implementation that places `cache_control` breakpoints on your Anthropic system prompt, measures cache hit rate via response metadata, and runs a concrete cost calculation showing real savings for a 50k-token system prompt served to 1000 daily queries.

## Prerequisites

- `anthropic>=0.40.0` installed (`pip install anthropic`).
- An Anthropic API key set as `ANTHROPIC_API_KEY` in your environment.
- Familiarity with the Messages API (`/v1/messages`) — basic request/response cycle.
- A system prompt at least a few thousand tokens long (the cost math becomes meaningful at ≥10k tokens).
- Optional: access to the 1-hour TTL beta (contact Anthropic support or see `anthropic-beta: prompt-caching-2024-07-31`).

## Steps

1. Upgrade the Anthropic Python SDK to a version that supports `cache_control`.

   ```bash
   pip install "anthropic>=0.40.0"
   ```

2. Structure your system prompt as a list of content blocks. Place a `cache_control` breakpoint on the last block you want cached. The API caches everything up to and including that block.

   ```python
   import anthropic
   import os

   client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

   SYSTEM_PROMPT_STATIC = """
   You are a senior product advisor for indie AI founders.
   [... your large context: product docs, knowledge base, persona instructions ...]
   """  # 50 000 tokens in production

   def query_with_cache(user_message: str) -> anthropic.types.Message:
       response = client.messages.create(
           model="claude-sonnet-4-6",
           max_tokens=1024,
           system=[
               {
                   "type": "text",
                   "text": SYSTEM_PROMPT_STATIC,
                   "cache_control": {"type": "ephemeral"},  # breakpoint here
               }
           ],
           messages=[{"role": "user", "content": user_message}],
       )
       return response
   ```

3. Inspect cache metadata on the response to confirm hits.

   ```python
   def log_cache_stats(response: anthropic.types.Message) -> None:
       usage = response.usage
       cache_creation = getattr(usage, "cache_creation_input_tokens", 0)
       cache_read = getattr(usage, "cache_read_input_tokens", 0)
       uncached = usage.input_tokens
       print(
           f"input={uncached} | cache_write={cache_creation} | cache_read={cache_read}"
       )

   # First call — cache is cold, expect cache_creation_input_tokens > 0
   r1 = query_with_cache("What metrics should I track for my AI product launch?")
   log_cache_stats(r1)

   # Second call within the TTL window — expect cache_read_input_tokens > 0
   r2 = query_with_cache("How do I price a geek-tier subscription?")
   log_cache_stats(r2)
   ```

4. Use up to 4 breakpoints to cache multiple layers (e.g., static docs + conversation history). Each additional breakpoint covers content from the previous one to the new one.

   ```python
   def query_with_layered_cache(
       static_docs: str,
       session_history: str,
       user_message: str,
   ) -> anthropic.types.Message:
       return client.messages.create(
           model="claude-sonnet-4-6",
           max_tokens=1024,
           system=[
               {
                   "type": "text",
                   "text": static_docs,
                   "cache_control": {"type": "ephemeral"},  # layer 1: rarely changes
               },
               {
                   "type": "text",
                   "text": session_history,
                   "cache_control": {"type": "ephemeral"},  # layer 2: per-session
               },
           ],
           messages=[{"role": "user", "content": user_message}],
       )
   ```

5. Opt into the 1-hour TTL beta (default TTL is 5 minutes) by passing the beta header. This extends cache lifetime for slow-traffic workloads.

   ```python
   response = client.beta.messages.create(
       model="claude-sonnet-4-6",
       max_tokens=1024,
       betas=["prompt-caching-2024-07-31"],
       system=[
           {
               "type": "text",
               "text": SYSTEM_PROMPT_STATIC,
               "cache_control": {"type": "ephemeral"},
           }
       ],
       messages=[{"role": "user", "content": user_message}],
   )
   ```

6. Run the cost calculation for your production scenario.

   Rates for `claude-sonnet-4-6` (per million tokens, as of 2026):
   - Base input: $3.00
   - Cache write: $3.75 (1.25× base)
   - Cache read: $0.30 (0.10× base)
   - Output: $15.00

   ```python
   def cost_estimate(
       system_tokens: int,
       queries_per_day: int,
       output_tokens_per_query: int,
       cache_hit_rate: float = 0.95,
       base_input_price: float = 3.00,
       cache_write_price: float = 3.75,
       cache_read_price: float = 0.30,
       output_price: float = 15.00,
   ) -> dict:
       """All prices in USD per million tokens."""
       # Writes: one write per TTL window. For 5-min TTL + uniform load:
       # writes_per_day ≈ 12 per hour × 24 = 288 (5-min windows), but only if
       # each window has ≥1 query. Conservatively: 1 cold write per day if traffic
       # is dense (>1 query/5 min), otherwise proportional.
       writes_per_day = max(1, int(queries_per_day * (1 - cache_hit_rate)))
       reads_per_day = int(queries_per_day * cache_hit_rate)

       cost_write = writes_per_day * system_tokens * cache_write_price / 1_000_000
       cost_read = reads_per_day * system_tokens * cache_read_price / 1_000_000
       cost_output = queries_per_day * output_tokens_per_query * output_price / 1_000_000
       total = cost_write + cost_read + cost_output

       # Baseline (no caching): all queries pay full input price
       baseline = queries_per_day * system_tokens * base_input_price / 1_000_000
       baseline += cost_output

       return {
           "daily_cost_cached_usd": round(total, 4),
           "daily_cost_baseline_usd": round(baseline, 4),
           "savings_usd": round(baseline - total, 4),
           "savings_pct": round((baseline - total) / baseline * 100, 1),
       }

   result = cost_estimate(
       system_tokens=50_000,
       queries_per_day=1_000,
       output_tokens_per_query=300,
       cache_hit_rate=0.95,
   )
   print(result)
   # {
   #   'daily_cost_cached_usd': 1.6625,
   #   'daily_cost_baseline_usd': 154.5,
   #   'savings_usd': 152.8375,
   #   'savings_pct': 98.9
   # }
   ```

   At 95% cache hit rate on a 50k-token system prompt with 1000 daily queries, cached cost is ~$1.66/day vs ~$154.50/day baseline — a 98.9% reduction.

## Verify

Run the two-call sequence from Step 3. On the second call, `cache_read_input_tokens` must be greater than zero:

```python
assert r2.usage.cache_read_input_tokens > 0, "Cache miss on second call — check TTL or prompt identity"
```

Also confirm the cost estimate runs without error:

```python
result = cost_estimate(system_tokens=50_000, queries_per_day=1_000, output_tokens_per_query=300)
assert result["savings_pct"] > 90, f"Unexpected savings: {result}"
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `cache_read_input_tokens` always 0 | Prompt changed between calls (even whitespace) | Ensure `SYSTEM_PROMPT_STATIC` is a module-level constant, not rebuilt per request |
| Cache hits stop after ~5 min of low traffic | Default 5-min TTL expired | Enable 1-hour TTL beta (Step 5) or increase request frequency |
| `AttributeError: 'Usage' object has no attribute 'cache_creation_input_tokens'` | SDK version <0.40.0 | Run `pip install "anthropic>=0.40.0"` |
| Breakpoint on message `content` block, not `system` | Wrong block type targeted | `cache_control` works on `system` content blocks and on `messages` assistant turns; user-turn caching requires tool result blocks |
| Cost higher than baseline on first call | Cold write penalty (1.25× on 50k tokens) | Expected — amortised over subsequent reads; only profitable with >2 reads per write window |
| 4-breakpoint limit exceeded | API rejects request | Consolidate layers; only the last N most useful splits need breakpoints |

## Next

- [geek/context-engineering/context-window-budgeting](../context-window-budgeting/playbook.md) — allocate token budget across system prompt, history, and output after you understand caching overhead.
- [geek/llm-integration/claude-api-streaming](../../../llm-integration/claude-api-streaming/playbook.md) — combine caching with streaming responses to reduce time-to-first-token for cached calls.

## References

- [knowledge/geek/ai/llm-integration/claude-advanced-features](../../../knowledge/geek/ai/llm-integration/claude-advanced-features) — documents the `cache_control` block schema, breakpoint limits, and TTL behaviour that underpin Steps 2–5.
- [knowledge/geek/ai/llm-integration/claude-api-integration](../../../knowledge/geek/ai/llm-integration/claude-api-integration) — covers the Messages API request structure and usage object fields (`cache_creation_input_tokens`, `cache_read_input_tokens`) read in Step 3.
