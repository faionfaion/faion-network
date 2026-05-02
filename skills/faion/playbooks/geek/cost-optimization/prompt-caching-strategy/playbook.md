---
name: prompt-caching-strategy
description: Optimize prompt cache hit rate to ≥80% by ordering content stable→volatile, batching within TTL windows, and instrumenting cache metrics for real cost diff calculation.
tier: geek
group: cost-optimization
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a measurable prompt caching strategy: stable content placed before volatile content in every request, reads batched within the 5-minute default TTL window, a `CacheMetricsCollector` class that tracks `cache_read_input_tokens / cache_creation_input_tokens` ratio in real time, and a cost diff calculation showing actual savings versus uncached baseline. Target: cache hit rate ≥80% in production.

## Prerequisites

- `anthropic>=0.40.0` installed (`pip install "anthropic>=0.40.0"`).
- `ANTHROPIC_API_KEY` set in the environment.
- At least one large system prompt (≥2048 tokens) that is reused across calls — this is where caching pays off.
- Baseline cost data: your current `input_tokens` spend per day (pull from Anthropic usage dashboard or your own logs).
- Familiarity with `cache_control` breakpoints from `prompt-caching-anthropic` (that playbook covers the API mechanics; this one covers strategy).

## Steps

1. Audit your request structure and identify the stable/volatile boundary.

   Stable content (cache it): system prompt, tool definitions, large reference documents, few-shot examples, persona instructions.
   Volatile content (do NOT cache): user message, session-specific context, timestamps, per-request variables.

   Draw the boundary explicitly in code:

   ```python
   STABLE_SYSTEM = """
   You are a senior product advisor for an indie SaaS founder.
   [... 3000+ tokens of instructions, examples, reference data ...]
   """

   def build_messages(user_query: str, session_ctx: str) -> list[dict]:
       return [
           {
               "role": "user",
               "content": [
                   # Volatile part — no cache_control
                   {"type": "text", "text": f"Session context: {session_ctx}"},
                   {"type": "text", "text": user_query},
               ],
           }
       ]

   def build_system_with_cache() -> list[dict]:
       return [
           {
               "type": "text",
               "text": STABLE_SYSTEM,
               "cache_control": {"type": "ephemeral"},  # breakpoint here
           }
       ]
   ```

2. Place `cache_control` breakpoints at the LAST token of each stable block, not mid-block.

   The Anthropic caching model stores everything UP TO AND INCLUDING the breakpoint. Any token after the breakpoint is re-sent uncached. So a breakpoint must be the final element of a stable region:

   ```python
   # CORRECT: breakpoint on the last element of the stable list
   system_blocks = [
       {"type": "text", "text": PERSONA_BLOCK},
       {"type": "text", "text": TOOLS_REFERENCE_BLOCK},
       {
           "type": "text",
           "text": FEW_SHOT_EXAMPLES,
           "cache_control": {"type": "ephemeral"},  # ← last stable item
       },
   ]

   # WRONG: breakpoint mid-stable, volatile appended after
   # This would re-create the cache every call.
   ```

3. Batch reads within the 5-minute TTL window.

   The default cache TTL is 5 minutes. If your pipeline sends multiple calls for the same user session (e.g., multi-turn chat, agentic loop), send them within that window. For batch-style workloads (offline document processing), use the 1-hour TTL beta header:

   ```python
   import anthropic

   client = anthropic.Anthropic()

   def call_with_cache(system_blocks: list[dict], messages: list[dict],
                       use_1h_ttl: bool = False) -> anthropic.types.Message:
       extra_headers = {}
       if use_1h_ttl:
           extra_headers["anthropic-beta"] = "prompt-caching-2024-07-31"

       return client.messages.create(
           model="claude-sonnet-4-6",
           max_tokens=1024,
           system=system_blocks,
           messages=messages,
           extra_headers=extra_headers,
       )
   ```

   For multi-turn chat: reuse the same `system_blocks` object across turns in the same session. The cache key is the exact token sequence up to the breakpoint — any change invalidates it.

4. Instrument cache metrics on every response.

   ```python
   from dataclasses import dataclass, field
   from typing import Optional
   import anthropic

   @dataclass
   class CacheSnapshot:
       input_tokens: int = 0
       cache_creation_input_tokens: int = 0
       cache_read_input_tokens: int = 0
       calls: int = 0

       @property
       def hit_rate(self) -> Optional[float]:
           total_cache = self.cache_creation_input_tokens + self.cache_read_input_tokens
           if total_cache == 0:
               return None
           return self.cache_read_input_tokens / total_cache

   class CacheMetricsCollector:
       def __init__(self) -> None:
           self._snap = CacheSnapshot()

       def record(self, usage: anthropic.types.Usage) -> None:
           self._snap.input_tokens += usage.input_tokens
           self._snap.cache_creation_input_tokens += getattr(
               usage, "cache_creation_input_tokens", 0
           ) or 0
           self._snap.cache_read_input_tokens += getattr(
               usage, "cache_read_input_tokens", 0
           ) or 0
           self._snap.calls += 1

       def snapshot(self) -> CacheSnapshot:
           return CacheSnapshot(
               input_tokens=self._snap.input_tokens,
               cache_creation_input_tokens=self._snap.cache_creation_input_tokens,
               cache_read_input_tokens=self._snap.cache_read_input_tokens,
               calls=self._snap.calls,
           )

       def report(self) -> str:
           s = self._snap
           hr = s.hit_rate
           hr_str = f"{hr:.1%}" if hr is not None else "n/a"
           return (
               f"calls={s.calls} "
               f"input={s.input_tokens} "
               f"cache_creation={s.cache_creation_input_tokens} "
               f"cache_read={s.cache_read_input_tokens} "
               f"hit_rate={hr_str}"
           )

   metrics = CacheMetricsCollector()

   # Usage:
   response = call_with_cache(system_blocks, messages)
   metrics.record(response.usage)
   print(metrics.report())
   # → calls=42 input=5180 cache_creation=4800 cache_read=38400 hit_rate=88.9%
   ```

5. Calculate real cost savings versus uncached baseline.

   Anthropic pricing (Sonnet 4.6 as of May 2026):
   - Input: $3.00 / 1M tokens
   - Cache write: $3.75 / 1M tokens (25% surcharge on first write)
   - Cache read: $0.30 / 1M tokens (10% of input price)

   ```python
   def cost_diff(snap: CacheSnapshot) -> dict:
       INPUT_PRICE = 3.00 / 1_000_000       # $/token
       CACHE_WRITE_PRICE = 3.75 / 1_000_000
       CACHE_READ_PRICE = 0.30 / 1_000_000

       # Actual cost with caching
       actual = (
           snap.input_tokens * INPUT_PRICE
           + snap.cache_creation_input_tokens * CACHE_WRITE_PRICE
           + snap.cache_read_input_tokens * CACHE_READ_PRICE
       )

       # Hypothetical cost if cache_read tokens had been billed as input tokens
       baseline_tokens = (
           snap.input_tokens
           + snap.cache_creation_input_tokens
           + snap.cache_read_input_tokens
       )
       baseline = baseline_tokens * INPUT_PRICE

       savings = baseline - actual
       pct = savings / baseline * 100 if baseline > 0 else 0.0
       return {
           "baseline_usd": round(baseline, 4),
           "actual_usd": round(actual, 4),
           "savings_usd": round(savings, 4),
           "savings_pct": round(pct, 1),
       }

   snap = metrics.snapshot()
   print(cost_diff(snap))
   # → {'baseline_usd': 0.1284, 'actual_usd': 0.0302, 'savings_usd': 0.0982, 'savings_pct': 76.5}
   ```

6. Tune toward ≥80% hit rate.

   If `hit_rate < 0.80` after 20+ calls, diagnose using this checklist:

   - Is the system prompt changing between calls? Any dynamic string in the stable block (timestamp, user ID, A/B variant flag) will bust the cache every time.
   - Are calls arriving outside the TTL window? Add timestamps to logs and compare `created_at` across consecutive calls. If gap > 5 minutes, switch to 1h-TTL beta.
   - Is the breakpoint on the correct (last) element? Log `len(system_blocks)` and confirm `cache_control` is only on the last item.
   - Is the stable block below 2048 tokens? Anthropic requires a minimum 2048-token block to be cache-eligible. Check with `len(tokenizer.encode(STABLE_SYSTEM)) >= 2048`.

## Verify

After ≥20 production calls, run:

```python
snap = metrics.snapshot()
assert snap.hit_rate is not None and snap.hit_rate >= 0.80, (
    f"Cache hit rate {snap.hit_rate:.1%} is below 80% target. "
    f"Diagnose with Step 6."
)
print("PASS:", metrics.report())
# PASS: calls=25 input=6250 cache_creation=4950 cache_read=44550 hit_rate=90.0%
```

Also confirm in the Anthropic console (Usage → Prompt Caching tab) that `cache_read_input_tokens` is growing faster than `cache_creation_input_tokens` after the first day.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `cache_read_input_tokens` always 0 | `cache_control` key missing or wrong position | Print `system_blocks` before the call; confirm the last block has `"cache_control": {"type": "ephemeral"}` |
| Hit rate stuck at ~50% | Calls interleaved from two different system prompt variants (A/B test) | Assign one variant per session; do not alternate per call |
| Hit rate drops overnight | Daily cron job changes stable block (date, version string, config) | Move dynamic values out of the stable block into the user message |
| `cache_creation_input_tokens` grows unbounded | TTL expiry + high call gap | Enable 1h-TTL beta for batch workloads; for chat, ensure turns happen within 5 minutes |
| `anthropic.BadRequestError` on 1h-TTL header | Beta not enabled for your key | Contact Anthropic support; fall back to 5-minute TTL as interim |
| Cost savings less than expected despite high hit rate | Stable block is small (<5k tokens) | Cost savings are proportional to stable block size; small prompts have limited upside regardless of hit rate |

## Next

- `model-routing-cheap-vs-strong` — combine prompt caching with model routing: cache hits reduce input cost; routing to Haiku/Sonnet reduces per-call cost further; both strategies stack.
- `prompt-caching-anthropic` — if you skipped the API mechanics playbook, read it for `cache_control` placement syntax and TTL details before tuning the strategy here.

## References

- [knowledge/geek/ai/llm-integration/claude-advanced-features](../../../knowledge/geek/ai/llm-integration/claude-advanced-features) — covers `cache_control` breakpoint semantics, minimum token threshold (2048), and TTL variants (5m default, 1h beta) that this playbook's batching and breakpoint-placement steps are built on top of.
- [knowledge/geek/ai/llm-integration/claude-api-basics](../../../knowledge/geek/ai/llm-integration/claude-api-basics) — documents the `usage` response object fields (`cache_creation_input_tokens`, `cache_read_input_tokens`) that `CacheMetricsCollector` reads to compute hit rate and cost diff.
